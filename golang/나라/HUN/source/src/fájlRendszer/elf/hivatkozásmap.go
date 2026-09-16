/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "konzol"

import mem "memóriamanager"

type Hivatkozás struct {
	Dinamikus	uintptr
	Previous	*Hivatkozás
	Következő	*Hivatkozás
}
type Hivatkozásmap struct {
	First	*Hivatkozás
	Utolsó	*Hivatkozás

	Méret_2	int

	mem	*mem.TMemóriamanager
}

func (self *Hivatkozásmap) Init(mem *mem.TMemóriamanager) {
	self.mem = mem
}
func (self *Hivatkozásmap) Clone() Hivatkozásmap {
	var hivatkozásmap Hivatkozásmap

	hivatkozásmap.Init(self.mem)

	Hivatkozás := self.First

	for ; Hivatkozás != nil; Hivatkozás = Hivatkozás.Következő {
		hivatkozásmap.Append_to_list(Hivatkozás.Dinamikus)
	}
	return hivatkozásmap
}
func (self *Hivatkozásmap) Prepend_to_list(Dinamikus uintptr) {
	újHivatkozás := (*Hivatkozás)(self.mem.Malloc(uint32(Sizeof(Hivatkozás{}))))
	újHivatkozás.Dinamikus = Dinamikus
	újHivatkozás.Következő = self.First
	self.First = újHivatkozás
	self.Méret_2++

	if self.First.Következő == nil {
		self.Utolsó = self.First
	}
}
func (self *Hivatkozásmap) Append_to_list(Dinamikus uintptr) {
	if Dinamikus == 0 {
		return
	}

	if self.Méret_2 == 0 {
		self.Prepend_to_list(Dinamikus)
	} else {
		újHivatkozás := (*Hivatkozás)(self.mem.Malloc(uint32(Sizeof(Hivatkozás{}))))
		újHivatkozás.Dinamikus = Dinamikus
		újHivatkozás.Következő = nil
		self.Utolsó.Következő = újHivatkozás
		self.Utolsó = újHivatkozás
		self.Méret_2++
	}
}
func (self *Hivatkozásmap) Nyomtatás(x uint16, y uint16) {
	Hivatkozás := self.First
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatásxy("linkmap : ", x, y)
	for ; Hivatkozás != nil; Hivatkozás = Hivatkozás.Következő {
		konzol_2.MUnsignedinteger32Nyomtatás(uint32(Hivatkozás.Dinamikus))
		konzol_2.MNyomtatás("+")

	}
}
