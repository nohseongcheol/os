package elf

import . "unsafe"
import . "console"

import mem "ማስታወሻmanager"

type Lአገናኝ struct {
	Dynamic		uintptr
	Previous	*Lአገናኝ
	Nየሚቀጥለው		*Lአገናኝ
}
type Lአገናኝmap struct {
	First	*Lአገናኝ
	Last	*Lአገናኝ

	Sመጠን_2	int

	mem	*mem.Tማስታወሻmanager
}

func (self *Lአገናኝmap) Init(mem *mem.Tማስታወሻmanager) {
	self.mem = mem
}
func (self *Lአገናኝmap) Clone() Lአገናኝmap {
	var አገናኝmap Lአገናኝmap

	አገናኝmap.Init(self.mem)

	Lአገናኝ := self.First

	for ; Lአገናኝ != nil; Lአገናኝ = Lአገናኝ.Nየሚቀጥለው {
		አገናኝmap.Append_to_list(Lአገናኝ.Dynamic)
	}
	return አገናኝmap
}
func (self *Lአገናኝmap) Prepend_to_list(Dynamic uintptr) {
	አዲስአገናኝ := (*Lአገናኝ)(self.mem.Malloc(uint32(Sizeof(Lአገናኝ{}))))
	አዲስአገናኝ.Dynamic = Dynamic
	አዲስአገናኝ.Nየሚቀጥለው = self.First
	self.First = አዲስአገናኝ
	self.Sመጠን_2++

	if self.First.Nየሚቀጥለው == nil {
		self.Last = self.First
	}
}
func (self *Lአገናኝmap) Append_to_list(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if self.Sመጠን_2 == 0 {
		self.Prepend_to_list(Dynamic)
	} else {
		አዲስአገናኝ := (*Lአገናኝ)(self.mem.Malloc(uint32(Sizeof(Lአገናኝ{}))))
		አዲስአገናኝ.Dynamic = Dynamic
		አዲስአገናኝ.Nየሚቀጥለው = nil
		self.Last.Nየሚቀጥለው = አዲስአገናኝ
		self.Last = አዲስአገናኝ
		self.Sመጠን_2++
	}
}
func (self *Lአገናኝmap) Pማተሚያ(x uint16, y uint16) {
	Lአገናኝ := self.First
	console_2 := TConsole{}
	console_2.Mማተሚያxy("linkmap : ", x, y)
	for ; Lአገናኝ != nil; Lአገናኝ = Lአገናኝ.Nየሚቀጥለው {
		console_2.MUnsignedinteger32ማተሚያ(uint32(Lአገናኝ.Dynamic))
		console_2.Mማተሚያ("+")

	}
}
