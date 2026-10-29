/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "memorymanager"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Size	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Init(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Init(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.PushBack(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) PushFront(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Size++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) PushBack(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Size == 0 {
		self.PushFront(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Size++
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
