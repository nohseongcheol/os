/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "yaddaşmanager"

type Körpü struct {
	Dynamic		uintptr
	Previous	*Körpü
	Sonrakı		*Körpü
}
type Körpümap struct {
	First	*Körpü
	Last	*Körpü

	Böyüklük_2	int

	mem	*mem.TYaddaşmanager
}

func (self *Körpümap) Init(mem *mem.TYaddaşmanager) {
	self.mem = mem
}
func (self *Körpümap) Clone() Körpümap {
	var körpümap Körpümap

	körpümap.Init(self.mem)

	Körpü := self.First

	for ; Körpü != nil; Körpü = Körpü.Sonrakı {
		körpümap.Append_to_list(Körpü.Dynamic)
	}
	return körpümap
}
func (self *Körpümap) Prepend_to_list(Dynamic uintptr) {
	yenikörpü := (*Körpü)(self.mem.Malloc(uint32(Sizeof(Körpü{}))))
	yenikörpü.Dynamic = Dynamic
	yenikörpü.Sonrakı = self.First
	self.First = yenikörpü
	self.Böyüklük_2++

	if self.First.Sonrakı == nil {
		self.Last = self.First
	}
}
func (self *Körpümap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Böyüklük_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		yenikörpü := (*Körpü)(self.mem.Malloc(uint32(Sizeof(Körpü{}))))
		yenikörpü.Dynamic = Dynamic
		yenikörpü.Sonrakı = nil
		self.Last.Sonrakı = yenikörpü
		self.Last = yenikörpü
		self.Böyüklük_2++
	}
}
func (self *Körpümap) ÇapEt(x uint16, y uint16) {
	Körpü := self.First
	console_2 := TConsole{}
	console_2.MÇapEtxy("linkmap : ", x, y)
	for ; Körpü != nil; Körpü = Körpü.Sonrakı {
		console_2.MUnsignedinteger32ÇapEt(uint32(Körpü.Dynamic))
		console_2.MÇapEt("+")

	}
}
