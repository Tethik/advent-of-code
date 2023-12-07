package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestComparison(t *testing.T) {
	assert.True(t, rank("33332").Compare(rank("2AAAA")) > 0)
	assert.True(t, rank("77888").Compare(rank("77788")) > 0)
	assert.True(t, rank("KK677").Compare(rank("KTJJT")) > 0) // KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
	assert.True(t, rank("K6666").Compare(rank("K5KKK")) > 0)
	assert.True(t, rank("T55J5").Compare(rank("QQQJA")) < 0) // T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
}