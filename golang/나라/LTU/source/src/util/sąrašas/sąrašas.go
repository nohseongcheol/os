package sąrašas

import . "unsafe"
import . "console"
import mem "atmintismanager"

type Mazgas struct {
	rodyklė_2	uintptr
	previous	*Mazgas
	kitas		*Mazgas
}

type LinkedSąrašas struct {
	head	*Mazgas
	tail	*Mazgas
	Dydis_2	int

	mem	*mem.TAtmintismanager
}

func (self *LinkedSąrašas) Init(mem *mem.TAtmintismanager) {
	self.head = nil
	self.tail = nil
	self.Dydis_2 = 0

	self.mem = mem
}
func (self *LinkedSąrašas) Prepend_to_list(rodyklė_2 uintptr) {
	naujasMazgas := (*Mazgas)(self.mem.Malloc(uint32(Sizeof(Mazgas{}))))
	if naujasMazgas == nil {
		return
	}
	naujasMazgas.rodyklė_2 = rodyklė_2
	naujasMazgas.previous = nil
	naujasMazgas.kitas = self.head
	if self.head != nil {
		self.head.previous = naujasMazgas
	}
	self.head = naujasMazgas
	self.Dydis_2++

	if self.head.kitas == nil {
		self.tail = self.head
	}

}
func (self *LinkedSąrašas) Append_to_list(rodyklė_2 uintptr) {
	if self.Dydis_2 == 0 {
		self.Prepend_to_list(rodyklė_2)
	} else {
		naujasMazgas := (*Mazgas)(self.mem.Malloc(uint32(Sizeof(Mazgas{}))))
		if naujasMazgas == nil {
			return
		}
		naujasMazgas.rodyklė_2 = rodyklė_2
		naujasMazgas.previous = self.tail
		naujasMazgas.kitas = nil
		self.tail.kitas = naujasMazgas
		self.tail = naujasMazgas
		self.Dydis_2++
	}
}
func (self *LinkedSąrašas) Insert_at_index(rodyklė int, rodyklė_2 uintptr) {
	if rodyklė == 0 {
		self.Prepend_to_list(rodyklė_2)
	} else {
		previousMazgas := self.GetMazgasat(rodyklė - 1)
		kitasMazgas := previousMazgas.kitas
		naujasMazgas := (*Mazgas)(self.mem.Malloc(uint32(Sizeof(Mazgas{}))))
		if naujasMazgas == nil {
			return
		}
		naujasMazgas.rodyklė_2 = rodyklė_2

		previousMazgas.kitas = naujasMazgas
		naujasMazgas.previous = previousMazgas
		naujasMazgas.kitas = kitasMazgas
		if kitasMazgas != nil {
			kitasMazgas.previous = naujasMazgas
		}

		self.Dydis_2++

		if naujasMazgas.kitas == nil {
			self.tail = naujasMazgas
		}
	}
}
func (self *LinkedSąrašas) GetMazgasat(rodyklė int) *Mazgas {
	if rodyklė < 0 || rodyklė >= self.Dydis_2 {
		return nil
	}
	var x *Mazgas = self.head
	for i := 0; i < rodyklė; i++ {
		x = x.kitas
	}
	return x
}

func (self *LinkedSąrašas) NustatytaMazgasat(rodyklė int, rodyklė_2 uintptr) {
	var x *Mazgas = self.head
	for i := 0; i < rodyklė; i++ {
		x = x.kitas
	}
	if x != nil {
		x.rodyklė_2 = rodyklė_2
	}
}
func (self *LinkedSąrašas) Getat(rodyklė int) Pointer {
	mazgas := self.GetMazgasat(rodyklė)
	if mazgas == nil {
		return nil
	}
	var rodyklė_2 uintptr = mazgas.rodyklė_2
	return Pointer(rodyklė_2)
}
func (self *LinkedSąrašas) Rodyklėiš(rodyklė_2 uintptr) int {
	var n *Mazgas = self.head
	i := 0
	for ; i < self.Dydis_2; i++ {
		if rodyklė_2 == n.rodyklė_2 {
			return i
		}
		n = n.kitas
	}
	return -1
}
func (self *LinkedSąrašas) Pašalinti(rodyklė_2 uintptr) {
	rodyklė := self.Rodyklėiš(rodyklė_2)
	if rodyklė < 0 {
		return
	}
	self.Pašalintiat(rodyklė)
}
func (self *LinkedSąrašas) Pašalintiat(rodyklė int) {
	if rodyklė < 0 || rodyklė >= self.Dydis_2 {
		return
	}
	mazgas := self.GetMazgasat(rodyklė)
	if mazgas == nil {
		return
	}
	if mazgas.previous != nil {
		mazgas.previous.kitas = mazgas.kitas
	} else {
		self.head = mazgas.kitas
	}
	if mazgas.kitas != nil {
		mazgas.kitas.previous = mazgas.previous
	} else {
		self.tail = mazgas.previous
	}
	self.Dydis_2 = self.Dydis_2 - 1

	if self.mem != nil {
		self.mem.Laisva(Pointer(mazgas))
	}
}

var console_2 = TConsole{}

func (self *LinkedSąrašas) Spausdinti() {
	console_2.MSpausdintixy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Dydis_2; i++ {
		mazgas := (*Mazgas)(self.Getat(i))
		console_2.MUnsignedinteger32Spausdinti(uint32(mazgas.rodyklė_2))
		console_2.MSpausdinti(":")
	}
}
