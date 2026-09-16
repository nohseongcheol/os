/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "მეხსიერებაmanager"

type Lბმული struct {
	Dynamic		uintptr
	Previous	*Lბმული
	Nშემდეგი	*Lბმული
}
type Lბმულიmap struct {
	First	*Lბმული
	Last	*Lბმული

	Sზომა_2	int

	mem	*mem.Tმეხსიერებაmanager
}

func (self *Lბმულიmap) Init(mem *mem.Tმეხსიერებაmanager) {
	self.mem = mem
}
func (self *Lბმულიmap) Clone() Lბმულიmap {
	var ბმულიmap Lბმულიmap

	ბმულიmap.Init(self.mem)

	Lბმული := self.First

	for ; Lბმული != nil; Lბმული = Lბმული.Nშემდეგი {
		ბმულიmap.Append_to_list(Lბმული.Dynamic)
	}
	return ბმულიmap
}
func (self *Lბმულიmap) Prepend_to_list(Dynamic uintptr) {
	ახალიბმული := (*Lბმული)(self.mem.Malloc(uint32(Sizeof(Lბმული{}))))
	ახალიბმული.Dynamic = Dynamic
	ახალიბმული.Nშემდეგი = self.First
	self.First = ახალიბმული
	self.Sზომა_2++

	if self.First.Nშემდეგი == nil {
		self.Last = self.First
	}
}
func (self *Lბმულიmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Sზომა_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		ახალიბმული := (*Lბმული)(self.mem.Malloc(uint32(Sizeof(Lბმული{}))))
		ახალიბმული.Dynamic = Dynamic
		ახალიბმული.Nშემდეგი = nil
		self.Last.Nშემდეგი = ახალიბმული
		self.Last = ახალიბმული
		self.Sზომა_2++
	}
}
func (self *Lბმულიmap) Pბეჭდვა(x uint16, y uint16) {
	Lბმული := self.First
	console_2 := TConsole{}
	console_2.Mბეჭდვაxy("linkmap : ", x, y)
	for ; Lბმული != nil; Lბმული = Lბმული.Nშემდეგი {
		console_2.MUnsignedinteger32ბეჭდვა(uint32(Lბმული.Dynamic))
		console_2.Mბეჭდვა("+")

	}
}
