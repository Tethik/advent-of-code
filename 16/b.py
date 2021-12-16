from collections import namedtuple
import math
from bitstream import BitStream


Packet = namedtuple("Packet", ["version", "type_id", "value"])


def to_int(b):
    return int(str(b), 2)


def read_version(stream, n=None):
    return to_int(stream.read(BitStream, n=3))


def read_type_id(stream, n=None):
    return to_int(stream.read(BitStream, n=3))


def read_literal_value(stream, n=None):
    if n is not None and n > 1:
        values = [read_literal_value(stream, n=1) for _ in range(n)]
        return values

    literal_value = BitStream()
    while True:
        packet = stream.read(BitStream, 5)
        _continue = packet.read(bool)
        literal_value.write(packet)
        if not _continue:
            break

    stream.read(len(literal_value) % 4)
    return to_int(literal_value)


def read_operator(stream, n=None):
    if n is not None and not n == 1:
        error = "unsupported argument n = {0!r}".format(n)
        raise ValueError(error)

    length_type_ID = stream.read(bool)
    if not length_type_ID:
        sub_length = to_int(stream.read(n=15))
        sub = stream.read(sub_length)
        p = []
        while len(sub) > 0:
            p.append(read_packet(sub))
        return p
    else:
        subs = to_int(stream.read(n=11))
        if subs == 1:
            # can return just one, which will not so nicely not be an array
            return [read_packet(stream)]
        return read_packet(stream, n=subs)


def read_sum(stream, n=None):
    packets = read_operator(stream)
    return sum(p.value for p in packets)


def read_product(stream, n=None):
    packets = read_operator(stream)
    return math.prod(p.value for p in packets)


def read_min(stream, n=None):
    packets = read_operator(stream)
    return min(p.value for p in packets)


def read_max(stream, n=None):
    packets = read_operator(stream)
    return max(p.value for p in packets)


def read_greater_than(stream, n=None):
    packets = read_operator(stream)
    if packets[0].value > packets[1].value:
        return 1
    return 0


def read_less_than(stream, n=None):
    packets = read_operator(stream)
    if packets[0].value < packets[1].value:
        return 1
    return 0


def read_equals(stream, n=None):
    packets = read_operator(stream)
    if packets[0].value == packets[1].value:
        return 1
    return 0


def read_packet(stream, n=None):
    if n is not None and not n == 1:
        return [read_packet(stream, n=1) for _ in range(n)]

    version = read_version(stream)
    tid = read_type_id(stream)
    read_function = types[tid]
    value = read_function(stream)
    return Packet(version, tid, value)


types = {
    0: read_sum,  # "sum",
    1: read_product,  # product
    2: read_min,  # min
    3: read_max,  # max
    4: read_literal_value,
    5: read_greater_than,  # greater than
    6: read_less_than,  # less
    7: read_equals,  # equal
}

l = input()
stream = BitStream(bytes.fromhex(l))
packet = read_packet(stream)
print(packet)
