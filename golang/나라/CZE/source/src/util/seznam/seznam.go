package seznam

import . "unsafe"
import . "konzole"
import mem "paměťmanager"

type TUzel_seznamu struct {
	odkaz_na_adresu		uintptr
	previous	*TUzel_seznamu
	následující	*TUzel_seznamu
}

type LinkedSeznam struct {
	head		*TUzel_seznamu
	tail		*TUzel_seznamu
	Velikost_2	int

	mem	*mem.TPaměťmanager
}

func (self *LinkedSeznam) Init(mem *mem.TPaměťmanager) {
	self.head = nil
	self.tail = nil
	self.Velikost_2 = 0

	self.mem = mem
}
func (self *LinkedSeznam) Přidat_na_začátek_seznamu(odkaz_na_adresu uintptr) {
	novýUzel := (*TUzel_seznamu)(self.mem.Přidělit_paměť(uint32(Sizeof(TUzel_seznamu{}))))
	if novýUzel == nil {
		return
	}
	novýUzel.odkaz_na_adresu = odkaz_na_adresu
	novýUzel.previous = nil
	novýUzel.následující = self.head
	if self.head != nil {
		self.head.previous = novýUzel
	}
	self.head = novýUzel
	self.Velikost_2++

	if self.head.následující == nil {
		self.tail = self.head
	}

}
func (self *LinkedSeznam) Přidat_na_konec_seznamu(odkaz_na_adresu uintptr) {
	if self.Velikost_2 == 0 {
		self.Přidat_na_začátek_seznamu(odkaz_na_adresu)
	} else {
		novýUzel := (*TUzel_seznamu)(self.mem.Přidělit_paměť(uint32(Sizeof(TUzel_seznamu{}))))
		if novýUzel == nil {
			return
		}
		novýUzel.odkaz_na_adresu = odkaz_na_adresu
		novýUzel.previous = self.tail
		novýUzel.následující = nil
		self.tail.následující = novýUzel
		self.tail = novýUzel
		self.Velikost_2++
	}
}
func (self *LinkedSeznam) Vložit_na_pozici(rejstřík int, odkaz_na_adresu uintptr) {
	if rejstřík == 0 {
		self.Přidat_na_začátek_seznamu(odkaz_na_adresu)
	} else {
		previousUzel := self.GetUzelat(rejstřík - 1)
		následujícíUzel := previousUzel.následující
		novýUzel := (*TUzel_seznamu)(self.mem.Přidělit_paměť(uint32(Sizeof(TUzel_seznamu{}))))
		if novýUzel == nil {
			return
		}
		novýUzel.odkaz_na_adresu = odkaz_na_adresu

		previousUzel.následující = novýUzel
		novýUzel.previous = previousUzel
		novýUzel.následující = následujícíUzel
		if následujícíUzel != nil {
			následujícíUzel.previous = novýUzel
		}

		self.Velikost_2++

		if novýUzel.následující == nil {
			self.tail = novýUzel
		}
	}
}
func (self *LinkedSeznam) GetUzelat(rejstřík int) *TUzel_seznamu {
	if rejstřík < 0 || rejstřík >= self.Velikost_2 {
		return nil
	}
	var x *TUzel_seznamu = self.head
	for i := 0; i < rejstřík; i++ {
		x = x.následující
	}
	return x
}

func (self *LinkedSeznam) NastavitUzelat(rejstřík int, odkaz_na_adresu uintptr) {
	var x *TUzel_seznamu = self.head
	for i := 0; i < rejstřík; i++ {
		x = x.následující
	}
	if x != nil {
		x.odkaz_na_adresu = odkaz_na_adresu
	}
}
func (self *LinkedSeznam) Getat(rejstřík int) Pointer {
	uzel_seznamu := self.GetUzelat(rejstřík)
	if uzel_seznamu == nil {
		return nil
	}
	var odkaz_na_adresu uintptr = uzel_seznamu.odkaz_na_adresu
	return Pointer(odkaz_na_adresu)
}
func (self *LinkedSeznam) Rejstříkz(odkaz_na_adresu uintptr) int {
	var n *TUzel_seznamu = self.head
	i := 0
	for ; i < self.Velikost_2; i++ {
		if odkaz_na_adresu == n.odkaz_na_adresu {
			return i
		}
		n = n.následující
	}
	return -1
}
func (self *LinkedSeznam) Odstranit(odkaz_na_adresu uintptr) {
	rejstřík := self.Rejstříkz(odkaz_na_adresu)
	if rejstřík < 0 {
		return
	}
	self.Odstranitat(rejstřík)
}
func (self *LinkedSeznam) Odstranitat(rejstřík int) {
	if rejstřík < 0 || rejstřík >= self.Velikost_2 {
		return
	}
	uzel_seznamu := self.GetUzelat(rejstřík)
	if uzel_seznamu == nil {
		return
	}
	if uzel_seznamu.previous != nil {
		uzel_seznamu.previous.následující = uzel_seznamu.následující
	} else {
		self.head = uzel_seznamu.následující
	}
	if uzel_seznamu.následující != nil {
		uzel_seznamu.následující.previous = uzel_seznamu.previous
	} else {
		self.tail = uzel_seznamu.previous
	}
	self.Velikost_2 = self.Velikost_2 - 1

	if self.mem != nil {
		self.mem.Volné(Pointer(uzel_seznamu))
	}
}

var konzole_2 = TKonzole{}

func (self *LinkedSeznam) Tisknout() {
	konzole_2.MTisknoutxy("LinkedList:", 1, 1)
	konzole_2.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Velikost_2; i++ {
		uzel_seznamu := (*TUzel_seznamu)(self.Getat(i))
		konzole_2.MUnsignedinteger32Tisknout(uint32(uzel_seznamu.odkaz_na_adresu))
		konzole_2.MTisknout(":")
	}
}
