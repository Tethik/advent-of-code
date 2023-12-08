package main

type Node struct {
	value string
	left *Node
	right *Node
}

func (n *Node) String() string {
	return n.value
}