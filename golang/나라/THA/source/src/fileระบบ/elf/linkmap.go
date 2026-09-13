package elf

import . "unsafe"
import . "console"

import mem "memorymanager"

type Link struct {
	Dynamic		uintptr
	Previous	*Link
	Next		*Link
}
type Linkmap struct {
	First	*Link
	Last	*Link

	Sขนาด_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkmap) Init(mem *mem.TMemorymanager) {
	self.mem = mem
}
func (self *Linkmap) Clone() Linkmap {
	var linkmap Linkmap

	linkmap.Init(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkmap.Append_to_list(Link.Dynamic)
	}
	return linkmap
}
func (self *Linkmap) Prepend_to_list(Dynamic uintptr) {
	newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
	newlink.Dynamic = Dynamic
	newlink.Next = self.First
	self.First = newlink
	self.Sขนาด_2++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *Linkmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Sขนาด_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
		newlink.Dynamic = Dynamic
		newlink.Next = nil
		self.Last.Next = newlink
		self.Last = newlink
		self.Sขนาด_2++
	}
}
func (self *Linkmap) Print(x uint16, y uint16) {
	Link := self.First
	console_2 := TConsole{}
	console_2.MPrintxy("linkmap : ", x, y)
	for ; Link != nil; Link = Link.Next {
		console_2.MUnsignedinteger32print(uint32(Link.Dynamic))
		console_2.MPrint("+")

	}
}
