# Advent of Code

My solutions for Advent of Code.

## 2023 Learnings

- Copilot is awesome for writing filler (i.e. see [lib/xy.go](lib/xy.go)).

- Copilot is not so awesome for creating off by one errors. I had issues with the filler on day 5 because it generated an incorrect
  `Contains` function that was kind of annoying to debug.

- Probably need something better than `string.Split` to parse strings (quickly).

- Using a compiled regex pattern was actually fairly nice with Go's if syntax:

```go
if matched := numberPattern.FindStringSubmatch(line); len(matched) > 0 {
    dst := lib.MustAtoi(matched[1])
    src := lib.MustAtoi(matched[2])
    ran := lib.MustAtoi(matched[3])
    currMap.Ranges = append(currMap.Ranges, Range{Src: src, Dst: dst, Ran: ran})
}
```

- Must pattern helps clean up `if err != nil -> panic` statements (see above)

- To organize data I'm leaning towards putting everything into structs and implementing interfaces around them. It's a bit too painful otherwise without tuples and easy dictionaries.

- Sorting is a bit odd. Seems you need to fulfill an interfaces which can be a bit cumbersome.

- `slices.Reverse(someSlice)` reverses in place. Useful after sorting.

- pointers are worth keeping in mind. Ended up accidentally passing a slice by reference accidentally on day 7 and being weirded out when value was still retained. `slices.Clone()` to clone a slice, but on the other hand passing references has a lot of benefit. New little hack learned, instead of cloning change value, run function, then reset back to original value. Probably cheaper than clone ;)
