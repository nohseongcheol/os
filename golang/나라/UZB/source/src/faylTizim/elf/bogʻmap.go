/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "xotiramanager"

type Bogʻ struct {
	Dynamic		uintptr
	Previous	*Bogʻ
	Keyingi		*Bogʻ
}
type Bogʻmap struct {
	First	*Bogʻ
	Last	*Bogʻ

	Hajmi_2	int

	mem	*mem.TXotiramanager
}

func (self *Bogʻmap) Init(mem *mem.TXotiramanager) {
	self.mem = mem
}
func (self *Bogʻmap) Clone() Bogʻmap {
	var bogʻmap Bogʻmap

	bogʻmap.Init(self.mem)

	Bogʻ := self.First

	for ; Bogʻ != nil; Bogʻ = Bogʻ.Keyingi {
		bogʻmap.Append_to_list(Bogʻ.Dynamic)
	}
	return bogʻmap
}
func (self *Bogʻmap) Prepend_to_list(Dynamic uintptr) {
	yangiBogʻ := (*Bogʻ)(self.mem.Malloc(uint32(Sizeof(Bogʻ{}))))
	yangiBogʻ.Dynamic = Dynamic
	yangiBogʻ.Keyingi = self.First
	self.First = yangiBogʻ
	self.Hajmi_2++

	if self.First.Keyingi == nil {
		self.Last = self.First
	}
}
func (self *Bogʻmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Hajmi_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		yangiBogʻ := (*Bogʻ)(self.mem.Malloc(uint32(Sizeof(Bogʻ{}))))
		yangiBogʻ.Dynamic = Dynamic
		yangiBogʻ.Keyingi = nil
		self.Last.Keyingi = yangiBogʻ
		self.Last = yangiBogʻ
		self.Hajmi_2++
	}
}
func (self *Bogʻmap) Chopetish(x uint16, y uint16) {
	Bogʻ := self.First
	console_2 := TConsole{}
	console_2.MChopetishxy("linkmap : ", x, y)
	for ; Bogʻ != nil; Bogʻ = Bogʻ.Keyingi {
		console_2.MUnsignedinteger32Chopetish(uint32(Bogʻ.Dynamic))
		console_2.MChopetish("+")

	}
}
