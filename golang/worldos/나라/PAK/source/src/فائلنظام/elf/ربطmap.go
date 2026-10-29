/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "یادداشتmanager"

type Lربط struct {
	Dمحرک		uintptr
	Previous	*Lربط
	Nاگلا		*Lربط
}
type Lربطmap struct {
	First	*Lربط
	Last	*Lربط

	Sحجم_2	int

	mem	*mem.Tیادداشتmanager
}

func (self *Lربطmap) Init(mem *mem.Tیادداشتmanager) {
	self.mem = mem
}
func (self *Lربطmap) Clone() Lربطmap {
	var ربطmap Lربطmap

	ربطmap.Init(self.mem)

	Lربط := self.First

	for ; Lربط != nil; Lربط = Lربط.Nاگلا {
		ربطmap.Append_to_list(Lربط.Dمحرک)
	}
	return ربطmap
}
func (self *Lربطmap) Prepend_to_list(Dمحرک uintptr) {
	نیاربط := (*Lربط)(self.mem.Malloc(uint32(Sizeof(Lربط{}))))
	نیاربط.Dمحرک = Dمحرک
	نیاربط.Nاگلا = self.First
	self.First = نیاربط
	self.Sحجم_2++

	if self.First.Nاگلا == nil {
		self.Last = self.First
	}
}
func (self *Lربطmap) Append_to_list(Dمحرک uintptr) {
	if Dمحرک == 0 {
		return
	}

	if self.Sحجم_2 == 0 {
		self.Prepend_to_list(Dمحرک)
	} else {
		نیاربط := (*Lربط)(self.mem.Malloc(uint32(Sizeof(Lربط{}))))
		نیاربط.Dمحرک = Dمحرک
		نیاربط.Nاگلا = nil
		self.Last.Nاگلا = نیاربط
		self.Last = نیاربط
		self.Sحجم_2++
	}
}
func (self *Lربطmap) Pچھاپیں(x uint16, y uint16) {
	Lربط := self.First
	console_2 := TConsole{}
	console_2.Mچھاپیںxy("linkmap : ", x, y)
	for ; Lربط != nil; Lربط = Lربط.Nاگلا {
		console_2.MUnsignedinteger32چھاپیں(uint32(Lربط.Dمحرک))
		console_2.Mچھاپیں("+")

	}
}
