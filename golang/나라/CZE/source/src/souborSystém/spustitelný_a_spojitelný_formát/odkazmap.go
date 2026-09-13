package spustitelný_a_spojitelný_formát

import . "unsafe"
import . "konzole"

import mem "paměťmanager"

type Odkaz struct {
	Dynamické	uintptr
	Previous	*Odkaz
	Následující	*Odkaz
}
type Odkazmap struct {
	First		*Odkaz
	Poslední	*Odkaz

	Velikost_2	int

	mem	*mem.TPaměťmanager
}

func (self *Odkazmap) Init(mem *mem.TPaměťmanager) {
	self.mem = mem
}
func (self *Odkazmap) Clone() Odkazmap {
	var odkazmap Odkazmap

	odkazmap.Init(self.mem)

	Odkaz := self.First

	for ; Odkaz != nil; Odkaz = Odkaz.Následující {
		odkazmap.Přidat_na_konec_seznamu(Odkaz.Dynamické)
	}
	return odkazmap
}
func (self *Odkazmap) Přidat_na_začátek_seznamu(Dynamické uintptr) {
	novýOdkaz := (*Odkaz)(self.mem.Přidělit_paměť(uint32(Sizeof(Odkaz{}))))
	novýOdkaz.Dynamické = Dynamické
	novýOdkaz.Následující = self.First
	self.First = novýOdkaz
	self.Velikost_2++

	if self.First.Následující == nil {
		self.Poslední = self.First
	}
}
func (self *Odkazmap) Přidat_na_konec_seznamu(Dynamické uintptr) {
	if Dynamické == 0 {
		return
	}

	if self.Velikost_2 == 0 {
		self.Přidat_na_začátek_seznamu(Dynamické)
	} else {
		novýOdkaz := (*Odkaz)(self.mem.Přidělit_paměť(uint32(Sizeof(Odkaz{}))))
		novýOdkaz.Dynamické = Dynamické
		novýOdkaz.Následující = nil
		self.Poslední.Následující = novýOdkaz
		self.Poslední = novýOdkaz
		self.Velikost_2++
	}
}
func (self *Odkazmap) Tisknout(x uint16, y uint16) {
	Odkaz := self.First
	konzole_2 := TKonzole{}
	konzole_2.MTisknoutxy("linkmap : ", x, y)
	for ; Odkaz != nil; Odkaz = Odkaz.Následující {
		konzole_2.MUnsignedinteger32Tisknout(uint32(Odkaz.Dynamické))
		konzole_2.MTisknout("+")

	}
}
