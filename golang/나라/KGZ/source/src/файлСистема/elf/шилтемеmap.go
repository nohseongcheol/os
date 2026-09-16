/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "эсиmanager"

type Шилтеме struct {
	Dynamic		uintptr
	Previous	*Шилтеме
	Кийинки		*Шилтеме
}
type Шилтемеmap struct {
	First	*Шилтеме
	Last	*Шилтеме

	Өлчөм_2	int

	mem	*mem.TЭсиmanager
}

func (self *Шилтемеmap) Init(mem *mem.TЭсиmanager) {
	self.mem = mem
}
func (self *Шилтемеmap) Clone() Шилтемеmap {
	var шилтемеmap Шилтемеmap

	шилтемеmap.Init(self.mem)

	Шилтеме := self.First

	for ; Шилтеме != nil; Шилтеме = Шилтеме.Кийинки {
		шилтемеmap.Append_to_list(Шилтеме.Dynamic)
	}
	return шилтемеmap
}
func (self *Шилтемеmap) Prepend_to_list(Dynamic uintptr) {
	жаңышилтеме := (*Шилтеме)(self.mem.Malloc(uint32(Sizeof(Шилтеме{}))))
	жаңышилтеме.Dynamic = Dynamic
	жаңышилтеме.Кийинки = self.First
	self.First = жаңышилтеме
	self.Өлчөм_2++

	if self.First.Кийинки == nil {
		self.Last = self.First
	}
}
func (self *Шилтемеmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Өлчөм_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		жаңышилтеме := (*Шилтеме)(self.mem.Malloc(uint32(Sizeof(Шилтеме{}))))
		жаңышилтеме.Dynamic = Dynamic
		жаңышилтеме.Кийинки = nil
		self.Last.Кийинки = жаңышилтеме
		self.Last = жаңышилтеме
		self.Өлчөм_2++
	}
}
func (self *Шилтемеmap) Басма(x uint16, y uint16) {
	Шилтеме := self.First
	console_2 := TConsole{}
	console_2.MБасмаxy("linkmap : ", x, y)
	for ; Шилтеме != nil; Шилтеме = Шилтеме.Кийинки {
		console_2.MUnsignedinteger32Басма(uint32(Шилтеме.Dynamic))
		console_2.MБасма("+")

	}
}
