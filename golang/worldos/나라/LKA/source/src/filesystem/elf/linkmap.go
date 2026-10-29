/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "මතකයmanager"

type Link struct {
	Dynamic		uintptr
	Previous	*Link
	Nඊලඟ		*Link
}
type Linkmap struct {
	First	*Link
	Last	*Link

	Size_2	int

	mem	*mem.Tමතකයmanager
}

func (self *Linkmap) Init(mem *mem.Tමතකයmanager) {
	self.mem = mem
}
func (self *Linkmap) Clone() Linkmap {
	var linkmap Linkmap

	linkmap.Init(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Nඊලඟ {
		linkmap.Append_to_list(Link.Dynamic)
	}
	return linkmap
}
func (self *Linkmap) Prepend_to_list(Dynamic uintptr) {
	නවlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
	නවlink.Dynamic = Dynamic
	නවlink.Nඊලඟ = self.First
	self.First = නවlink
	self.Size_2++

	if self.First.Nඊලඟ == nil {
		self.Last = self.First
	}
}
func (self *Linkmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Size_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		නවlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
		නවlink.Dynamic = Dynamic
		නවlink.Nඊලඟ = nil
		self.Last.Nඊලඟ = නවlink
		self.Last = නවlink
		self.Size_2++
	}
}
func (self *Linkmap) Print(x uint16, y uint16) {
	Link := self.First
	console_2 := TConsole{}
	console_2.MPrintxy("linkmap : ", x, y)
	for ; Link != nil; Link = Link.Nඊලඟ {
		console_2.MUnsignedinteger32print(uint32(Link.Dynamic))
		console_2.MPrint("+")

	}
}
