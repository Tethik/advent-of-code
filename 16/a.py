from collections import namedtuple
from os import read
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
        return read_packet(stream, n=subs)  # can return just one


def read_packet(stream, n=None):
    if n is not None and not n == 1:
        return [read_packet(stream, n=1) for _ in range(n)]

    version = read_version(stream)
    # print(version)
    tid = read_type_id(stream)

    if tid == 4:
        read_function = read_literal_value
    else:
        read_function = read_operator
    # read_function = types[tid]
    # print(tid, read_function)
    value = read_function(stream)
    return Packet(version, tid, value)


types = {
    4: read_literal_value,
    6: read_operator,
    3: read_operator
}


l = input()
stream = BitStream(bytes.fromhex(l))
packet = read_packet(stream)
# print(packet)

q = [packet]
s = 0
while q:
    p = q.pop()
    print(p)
    s += p.version
    if isinstance(p.value, list):
        for subpacket in p.value:
            q.append(subpacket)
    elif isinstance(p.value, Packet):
        q.append(p.value)
print(s)

# version_sum = sum()
# version = read_version(stream)
# type_id = read_type_id(stream)
# print(version)
# print(type_id)

# op = read_operator(stream)
# print(op)

# print(stream[:6])
# could probably use bytes here and parse the whole thing... but we'll see..
# print(read_literal_value(stream))
