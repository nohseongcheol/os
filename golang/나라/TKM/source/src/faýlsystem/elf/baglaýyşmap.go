package elf

import . "unsafe"
import . "console"

import mem "memorymanager"

type Baglaýyş struct {
	Dynamic		uintptr
	Previous	*Baglaýyş
	Next		*Baglaýyş
}
type Baglaýyşmap struct {
	First	*Baglaýyş
	Last	*Baglaýyş

	Ululyk_2	int

	mem	*mem.TMemorymanager
}

func (self *Baglaýyşmap) Init(mem *mem.TMemorymanager) {
	self.mem = mem
}
func (self *Baglaýyşmap) Clone() Baglaýyşmap {
	var baglaýyşmap Baglaýyşmap

	baglaýyşmap.Init(self.mem)

	Baglaýyş := self.First

	for ; Baglaýyş != nil; Baglaýyş = Baglaýyş.Next {
		baglaýyşmap.Append_to_list(Baglaýyş.Dynamic)
	}
	return baglaýyşmap
}
func (self *Baglaýyşmap) Prepend_to_list(Dynamic uintptr) {
	täzebaglaýyş := (*Baglaýyş)(self.mem.Malloc(uint32(Sizeof(Baglaýyş{}))))
	täzebaglaýyş.Dynamic = Dynamic
	täzebaglaýyş.Next = self.First
	self.First = täzebaglaýyş
	self.Ululyk_2++

	if self.First.Next == nil {
		self.Last = self.First
	}
}
func (self *Baglaýyşmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Ululyk_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		täzebaglaýyş := (*Baglaýyş)(self.mem.Malloc(uint32(Sizeof(Baglaýyş{}))))
		täzebaglaýyş.Dynamic = Dynamic
		täzebaglaýyş.Next = nil
		self.Last.Next = täzebaglaýyş
		self.Last = täzebaglaýyş
		self.Ululyk_2++
	}
}
func (self *Baglaýyşmap) Çap(x uint16, y uint16) {
	Baglaýyş := self.First
	console_2 := TConsole{}
	console_2.MÇapxy("linkmap : ", x, y)
	for ; Baglaýyş != nil; Baglaýyş = Baglaýyş.Next {
		console_2.MUnsignedinteger32Çap(uint32(Baglaýyş.Dynamic))
		console_2.MÇap("+")

	}
}
