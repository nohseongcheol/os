package elf

import . "unsafe"
import . "console"

import mem "జ్ఞాపకస్థలం"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vపరిమాణం	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vప్రారంభించు(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vప్రారంభించు(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vజాబితా_చివర_చేర్చు(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vజాబితా_మొదట_చేర్చు(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vజ్ఞాపకస్థలాన్ని_కేటాయించు(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vపరిమాణం++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vజాబితా_చివర_చేర్చు(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vపరిమాణం == 0 {
		self.Vజాబితా_మొదట_చేర్చు(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vజ్ఞాపకస్థలాన్ని_కేటాయించు(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vపరిమాణం++
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
