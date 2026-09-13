package elf

import . "unsafe"
import . "console"

import mem "ububikomanager"

type Link struct {
	Dynamic		uintptr
	Previous	*Link
	Ikurikira	*Link
}
type Linkmap struct {
	First	*Link
	Last	*Link

	Ingano_2	int

	mem	*mem.TUbubikomanager
}

func (self *Linkmap) Init(mem *mem.TUbubikomanager) {
	self.mem = mem
}
func (self *Linkmap) Clone() Linkmap {
	var linkmap Linkmap

	linkmap.Init(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Ikurikira {
		linkmap.Append_to_list(Link.Dynamic)
	}
	return linkmap
}
func (self *Linkmap) Prepend_to_list(Dynamic uintptr) {
	newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
	newlink.Dynamic = Dynamic
	newlink.Ikurikira = self.First
	self.First = newlink
	self.Ingano_2++

	if self.First.Ikurikira == nil {
		self.Last = self.First
	}
}
func (self *Linkmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Ingano_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		newlink := (*Link)(self.mem.Malloc(uint32(Sizeof(Link{}))))
		newlink.Dynamic = Dynamic
		newlink.Ikurikira = nil
		self.Last.Ikurikira = newlink
		self.Last = newlink
		self.Ingano_2++
	}
}
func (self *Linkmap) Gucapa(x uint16, y uint16) {
	Link := self.First
	console_2 := TConsole{}
	console_2.MGucapaxy("linkmap : ", x, y)
	for ; Link != nil; Link = Link.Ikurikira {
		console_2.MUnsignedinteger32Gucapa(uint32(Link.Dynamic))
		console_2.MGucapa("+")

	}
}
