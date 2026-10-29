/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "સ્મૃતિ"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vકદ	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vઆરંભ_કરવો(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vઆરંભ_કરવો(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vસૂચિના_અંતે_ઉમેરવું(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vસૂચિની_શરૂઆતમાં_ઉમેરવું(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vકદ++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vસૂચિના_અંતે_ઉમેરવું(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vકદ == 0 {
		self.Vસૂચિની_શરૂઆતમાં_ઉમેરવું(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vકદ++
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
