package elf

import . "unsafe"
import . "console"

import mem "স্মৃতি"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vআকার	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vআরম্ভ_করা(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vআরম্ভ_করা(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vতালিকার_শেষে_যোগ_করা(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vতালিকার_শুরুতে_যোগ_করা(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vআকার++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vতালিকার_শেষে_যোগ_করা(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vআকার == 0 {
		self.Vতালিকার_শুরুতে_যোগ_করা(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vআকার++
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
