package main

import (
	"fmt"
	"slices"
	"sort"
	"strings"

	"github.com/Tethik/adventofcode/lib"
)

/*
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
*/
func value(c rune) int {
	switch c {
	case 'A':
		return 14
	case 'K':
		return 13
	case 'Q':
		return 12
	case 'J':
		return 0
	case 'T':
		return 10
	default:
		return int(c - '0')
	}
}

type Hand struct {
	Type int
	Cards []rune
	Bid int
}

func (r Hand) String() string {
	return fmt.Sprintf("%d%s", r.Type, string(r.Cards))
}

func (r Hand) Score() int {
	return r.Type
}

func (r Hand) Compare(other Hand) int {
	if r.Type == other.Type {
		for i := range r.Cards {
			if r.Cards[i] != other.Cards[i] {
				return value(r.Cards[i]) - value(other.Cards[i])
			}
		}
	}
	return r.Type - other.Type
}


/*
6 = Five of a kind, where all five cards have the same label: AAAAA -> 6A
5 = Four of a kind, where four cards have the same label and one card has a different label: AA8AA -> 5A8
4 = Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
3 = Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
2 = Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
1 = One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
0 = High card, where all cards' labels are distinct: 23456
*/
func rank(hand string) Hand {
	// construct a rank string where first char == the type of hand, and the rest is each label in descending order
	r := Hand{}	
	r.Cards = []rune(hand)
	count := map[rune]int{}
	for _, c := range hand {
		count[c]++
	}	

	orderedCounts := lib.SortMap[rune, int](count)
	slices.Reverse(orderedCounts)

	if count['J'] > 0 {		
		// This should recurse until no more jokers. Probably.
		max := 0
		j := slices.Index(r.Cards, 'J') // gets first joker
		for _, c := range "AKQT98765432" {			
			r.Cards[j] = c
			// fmt.Println(r.Cards, newCards)
			candidate := rank(string(r.Cards))
			if candidate.Type > max {
				max = candidate.Type
			}
			r.Cards[j] = 'J' // reset
		}
	
		r.Type = max
		return r
	}

	highestCount := count[orderedCounts[0]]
	
	// Five of a kind
	if highestCount == 5 {
		r.Type = 6
		// return r
	} else if highestCount == 4 {
		r.Type = 5
		// Special case / shortcut: Joker makes it a five of a kind
		// if anyJokers {
		// 	r.Type = 6
		// }
		// return r
	} else if highestCount == 3 {
		r.Type = 3
		if count[orderedCounts[1]] == 2 {
			r.Type = 4
		}
	} else if highestCount == 2 {
		r.Type = 1
		if count[orderedCounts[1]] == 2 {
			r.Type = 2
		}
	} else {
		r.Type = 0
	}

	return r
}

type ByRank []Hand

func (a ByRank) Len() int           { return len(a) }
func (a ByRank) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByRank) Less(i, j int) bool { return a[i].Compare(a[j]) < 0 }

func b(content string) {
	lines := strings.Split(content, "\n")	
	
	ranks := []Hand{}

	for _, line := range lines {
		parts := strings.Split(line, " ")
		hand, bid := parts[0], lib.MustAtoi(parts[1])
		r := rank(hand)		
		r.Bid = bid		
		ranks = append(ranks, r)
	}

	sort.Sort(ByRank(ranks))
	slices.Reverse(ranks)

	sum := 0	
	for i, h := range ranks {	
		rank := len(ranks) - i
		fmt.Println(string(h.Cards), rank, h.Bid, h.Bid * rank)	
		sum += h.Bid * rank
	}	
	fmt.Println(sum)
}
