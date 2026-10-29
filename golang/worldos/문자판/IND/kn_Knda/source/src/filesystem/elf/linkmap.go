/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "ಸ್ಮೃತಿ"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vಗಾತ್ರ	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vಆರಂಭಿಸು(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vಆರಂಭಿಸು(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vಪಟ್ಟಿಯ_ಕೊನೆಯಲ್ಲಿ_ಸೇರಿಸು(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vಪಟ್ಟಿಯ_ಆರಂಭದಲ್ಲಿ_ಸೇರಿಸು(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಹಂಚು(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vಗಾತ್ರ++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vಪಟ್ಟಿಯ_ಕೊನೆಯಲ್ಲಿ_ಸೇರಿಸು(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vಗಾತ್ರ == 0 {
		self.Vಪಟ್ಟಿಯ_ಆರಂಭದಲ್ಲಿ_ಸೇರಿಸು(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಹಂಚು(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vಗಾತ್ರ++
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
