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
