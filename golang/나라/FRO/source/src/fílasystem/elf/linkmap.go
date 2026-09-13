package elf

import . "unsafe"
import . "console"

import mem "memorymanager"

type Link struct {
	Rakstrarmáttur	uintptr
	Previous	*Link
	Næsta		*Link
}
type Linkmap struct {
	First	*Link
	Last	*Link

	Stødd_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkmap) Init(mem *mem.TMemorymanager) {
	self.mem = mem
}
func (self *Linkmap) Clone() Linkmap {
	var linkmap Linkmap

	linkmap.Init(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Næsta {
		linkmap.Append_to_list(Link.Rakstrarmáttur)
	}
	return linkmap
}
func (self *Linkmap) Prepend_to_list(Rakstrarmáttur uintptr) {
	newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
	newlink.Rakstrarmáttur = Rakstrarmáttur
	newlink.Næsta = self.First
	self.First = newlink
	self.Stødd_2++

	if self.First.Næsta == nil {
		self.Last = self.First
	}
}
func (self *Linkmap) Append_to_list(Rakstrarmáttur uintptr) {
	if Rakstrarmáttur == 0 {
		return
	}

	if self.Stødd_2 == 0 {
		self.Prepend_to_list(Rakstrarmáttur)
	} else {
		newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
		newlink.Rakstrarmáttur = Rakstrarmáttur
		newlink.Næsta = nil
		self.Last.Næsta = newlink
		self.Last = newlink
		self.Stødd_2++
	}
}
func (self *Linkmap) Print(x uint16, y uint16) {
	Link := self.First
	console_2 := TConsole{}
	console_2.MPrintxy("linkmap : ", x, y)
	for ; Link != nil; Link = Link.Næsta {
		console_2.MUnsignedinteger32print(uint32(Link.Rakstrarmáttur))
		console_2.MPrint("+")

	}
}
