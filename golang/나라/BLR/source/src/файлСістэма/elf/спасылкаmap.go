/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "памяцьmanager"

type Спасылка struct {
	Данамічна	uintptr
	Previous	*Спасылка
	Наступны	*Спасылка
}
type Спасылкаmap struct {
	First	*Спасылка
	Last	*Спасылка

	Памер_2	int

	mem	*mem.TПамяцьmanager
}

func (self *Спасылкаmap) Init(mem *mem.TПамяцьmanager) {
	self.mem = mem
}
func (self *Спасылкаmap) Clone() Спасылкаmap {
	var спасылкаmap Спасылкаmap

	спасылкаmap.Init(self.mem)

	Спасылка := self.First

	for ; Спасылка != nil; Спасылка = Спасылка.Наступны {
		спасылкаmap.Append_to_list(Спасылка.Данамічна)
	}
	return спасылкаmap
}
func (self *Спасылкаmap) Prepend_to_list(Данамічна uintptr) {
	новыСпасылка := (*Спасылка)(self.mem.Malloc(uint32(Sizeof(Спасылка{}))))
	новыСпасылка.Данамічна = Данамічна
	новыСпасылка.Наступны = self.First
	self.First = новыСпасылка
	self.Памер_2++

	if self.First.Наступны == nil {
		self.Last = self.First
	}
}
func (self *Спасылкаmap) Append_to_list(Данамічна uintptr) {
	if Данамічна == 0 {
		return
	}

	if self.Памер_2 == 0 {
		self.Prepend_to_list(Данамічна)
	} else {
		новыСпасылка := (*Спасылка)(self.mem.Malloc(uint32(Sizeof(Спасылка{}))))
		новыСпасылка.Данамічна = Данамічна
		новыСпасылка.Наступны = nil
		self.Last.Наступны = новыСпасылка
		self.Last = новыСпасылка
		self.Памер_2++
	}
}
func (self *Спасылкаmap) Друкаваць(x uint16, y uint16) {
	Спасылка := self.First
	console_2 := TConsole{}
	console_2.MДрукавацьxy("linkmap : ", x, y)
	for ; Спасылка != nil; Спасылка = Спасылка.Наступны {
		console_2.MUnsignedinteger32Друкаваць(uint32(Спасылка.Данамічна))
		console_2.MДрукаваць("+")

	}
}
