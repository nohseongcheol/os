package elf

import . "unsafe"
import . "console"

import mem "நினைவகம்"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vஅளவு	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vதொடங்கு(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vதொடங்கு(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vபட்டியலின்_முடிவில்_சேர்(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vபட்டியலின்_தொடக்கத்தில்_சேர்(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vநினைவகத்தை_ஒதுக்கு(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vஅளவு++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vபட்டியலின்_முடிவில்_சேர்(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vஅளவு == 0 {
		self.Vபட்டியலின்_தொடக்கத்தில்_சேர்(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vநினைவகத்தை_ஒதுக்கு(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vஅளவு++
	}
}
func (self *LinkMap) Print(x uint16, y uint16) {
	Link := self.First
	콘솔 := T콘솔{}
	콘솔.M출력XY("linkmap : ", x, y)
	for ; Link != nil; Link = Link.Next {
		콘솔.MUint32출력(uint32(Link.Dynamic))
		콘솔.M출력("+")

	}
}
