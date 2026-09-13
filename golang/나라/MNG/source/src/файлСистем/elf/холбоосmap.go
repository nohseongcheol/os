package elf

import . "unsafe"
import . "консол"

import mem "санахойЗохицуулагч"

type Холбоос struct {
	Dynamic		uintptr
	Previous	*Холбоос
	Дараах		*Холбоос
}
type Холбоосmap struct {
	First	*Холбоос
	Last	*Холбоос

	Хэмжээ_2	int

	mem	*mem.TСанахойЗохицуулагч
}

func (self *Холбоосmap) Init(mem *mem.TСанахойЗохицуулагч) {
	self.mem = mem
}
func (self *Холбоосmap) Clone() Холбоосmap {
	var холбоосmap Холбоосmap

	холбоосmap.Init(self.mem)

	Холбоос := self.First

	for ; Холбоос != nil; Холбоос = Холбоос.Дараах {
		холбоосmap.Append_to_list(Холбоос.Dynamic)
	}
	return холбоосmap
}
func (self *Холбоосmap) Prepend_to_list(Dynamic uintptr) {
	шинэХолбоос := (*Холбоос)(self.mem.Malloc(uint32(Sizeof(Холбоос{}))))
	шинэХолбоос.Dynamic = Dynamic
	шинэХолбоос.Дараах = self.First
	self.First = шинэХолбоос
	self.Хэмжээ_2++

	if self.First.Дараах == nil {
		self.Last = self.First
	}
}
func (self *Холбоосmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Хэмжээ_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		шинэХолбоос := (*Холбоос)(self.mem.Malloc(uint32(Sizeof(Холбоос{}))))
		шинэХолбоос.Dynamic = Dynamic
		шинэХолбоос.Дараах = nil
		self.Last.Дараах = шинэХолбоос
		self.Last = шинэХолбоос
		self.Хэмжээ_2++
	}
}
func (self *Холбоосmap) Хэвлэх(x uint16, y uint16) {
	Холбоос := self.First
	консол_2 := TКонсол{}
	консол_2.MХэвлэхxy("linkmap : ", x, y)
	for ; Холбоос != nil; Холбоос = Холбоос.Дараах {
		консол_2.MUnsignedinteger32Хэвлэх(uint32(Холбоос.Dynamic))
		консол_2.MХэвлэх("+")

	}
}
