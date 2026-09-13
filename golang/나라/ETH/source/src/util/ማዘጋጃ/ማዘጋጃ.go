package ማዘጋጃ

import . "unsafe"
import . "console"

var nodeማዘጋጃ [100]uintptr

type Tማዘጋጃ struct {
	Sመጠን_2 int
}

func (self *Tማዘጋጃ) Aመጨመሪያ(ጠቋሚ uintptr) {
	nodeማዘጋጃ[self.Sመጠን_2] = ጠቋሚ
	self.Sመጠን_2++
}
func (self *Tማዘጋጃ) Getat(ማውጫ int) Pointer {
	return Pointer(nodeማዘጋጃ[ማውጫ])
}
func (self *Tማዘጋጃ) Iማውጫከ(ጠቋሚ uintptr) int {
	i := 0
	for ; i < self.Sመጠን_2; i++ {
		if ጠቋሚ == nodeማዘጋጃ[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *Tማዘጋጃ) Pማተሚያ() {
	console_2.Mማተሚያxy("array:", 1, 1)

	for i := 0; i < self.Sመጠን_2; i++ {
		console_2.MUnsignedinteger32ማተሚያ(uint32(nodeማዘጋጃ[i]))
		console_2.Mማተሚያ(":")
	}
}
