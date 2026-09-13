package elf

import . "unsafe"
import . "console"

import mem "memorymanager"

type Алоқа struct {
	Dynamic		uintptr
	Previous	*Алоқа
	Навбатӣ		*Алоқа
}
type Алоқаmap struct {
	First	*Алоқа
	Last	*Алоқа

	Size_2	int

	mem	*mem.TMemorymanager
}

func (self *Алоқаmap) Init(mem *mem.TMemorymanager) {
	self.mem = mem
}
func (self *Алоқаmap) Clone() Алоқаmap {
	var алоқаmap Алоқаmap

	алоқаmap.Init(self.mem)

	Алоқа := self.First

	for ; Алоқа != nil; Алоқа = Алоқа.Навбатӣ {
		алоқаmap.Append_to_list(Алоқа.Dynamic)
	}
	return алоқаmap
}
func (self *Алоқаmap) Prepend_to_list(Dynamic uintptr) {
	навАлоқа := (*Алоқа)(self.mem.Malloc(uint32(Sizeof(Алоқа{}))))
	навАлоқа.Dynamic = Dynamic
	навАлоқа.Навбатӣ = self.First
	self.First = навАлоқа
	self.Size_2++

	if self.First.Навбатӣ == nil {
		self.Last = self.First
	}
}
func (self *Алоқаmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Size_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		навАлоқа := (*Алоқа)(self.mem.Malloc(uint32(Sizeof(Алоқа{}))))
		навАлоқа.Dynamic = Dynamic
		навАлоқа.Навбатӣ = nil
		self.Last.Навбатӣ = навАлоқа
		self.Last = навАлоқа
		self.Size_2++
	}
}
func (self *Алоқаmap) Чопкардан(x uint16, y uint16) {
	Алоқа := self.First
	console_2 := TConsole{}
	console_2.MЧопкарданxy("linkmap : ", x, y)
	for ; Алоқа != nil; Алоқа = Алоқа.Навбатӣ {
		console_2.MUnsignedinteger32Чопкардан(uint32(Алоқа.Dynamic))
		console_2.MЧопкардан("+")

	}
}
