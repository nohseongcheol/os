package elf

import . "unsafe"
import . "console"

import mem "ഓർമ്മ"

type Link struct {
	Dynamic		uintptr
	Prev	*Link
	Next		*Link
}
type LinkMap struct {
	First	*Link
	Last	*Link

	Vവലുപ്പം	int

	mem	*mem.TMemoryManager
}

func (self *LinkMap) Vആരംഭിക്കുക(mem *mem.TMemoryManager) {
	self.mem = mem
}
func (self *LinkMap) Clone() LinkMap {
	var linkMap LinkMap

	linkMap.Vആരംഭിക്കുക(self.mem)

	Link := self.First

	for ; Link != nil; Link = Link.Next {
		linkMap.Vപട്ടികയുടെ_അവസാനം_ചേർക്കുക(Link.Dynamic)
	}
	return linkMap
}
func (self *LinkMap) Vപട്ടികയുടെ_തുടക്കത്തിൽ_ചേർക്കുക(Dynamic uintptr) {
	newLink := (*Link)(self.mem.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(uint32(Sizeof(Link{}))))
	newLink.Dynamic = Dynamic
	newLink.Next = self.First
	self.First = newLink
	self.Vവലുപ്പം++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *LinkMap) Vപട്ടികയുടെ_അവസാനം_ചേർക്കുക(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Vവലുപ്പം == 0 {
		self.Vപട്ടികയുടെ_തുടക്കത്തിൽ_ചേർക്കുക(Dynamic)
	} else {
		newLink := (*Link)(self.mem.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(uint32(Sizeof(Link{}))))
		newLink.Dynamic = Dynamic
		newLink.Next = nil
		self.Last.Next = newLink
		self.Last = newLink
		self.Vവലുപ്പം++
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
