package lib

import (
	"sort"
	"strconv"
)

func MustAtoi(s string) int {
	v, e := strconv.Atoi(s)
	if e != nil {
		panic(e)
	}
	return v
}

type mapSorter[K comparable, V int] struct {
	Map map[K]V
	Values []K
}

// implement sort.Interface for mapSorter
func (m mapSorter[K, V]) Len() int {
	return len(m.Map)
}

func (m mapSorter[K, V]) Less(i, j int) bool {
	return m.Map[m.Values[i]] < m.Map[m.Values[j]]
}

func (m mapSorter[K, V]) Swap(i, j int) {
	m.Values[i], m.Values[j] = m.Values[j], m.Values[i]
}

func SortMap[K comparable, V int](m map[K]V) []K {
	sorted := mapSorter[K, V]{
		Map: m,
		Values: make([]K, len(m)),
	}
	i := 0
	for k := range m {
		sorted.Values[i] = k
		i++
	}
	sort.Sort(sorted)
	return sorted.Values
} 