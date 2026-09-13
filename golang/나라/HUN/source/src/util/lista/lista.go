package lista

import . "unsafe"
import . "konzol"
import mem "memóriamanager"

type Csomópont struct {
	mutató		uintptr
	previous	*Csomópont
	következő	*Csomópont
}

type LinkedLista struct {
	head	*Csomópont
	tail	*Csomópont
	Méret_2	int

	mem	*mem.TMemóriamanager
}

func (self *LinkedLista) Init(mem *mem.TMemóriamanager) {
	self.head = nil
	self.tail = nil
	self.Méret_2 = 0

	self.mem = mem
}
func (self *LinkedLista) Prepend_to_list(mutató uintptr) {
	újCsomópont := (*Csomópont)(self.mem.Malloc(uint32(Sizeof(Csomópont{}))))
	if újCsomópont == nil {
		return
	}
	újCsomópont.mutató = mutató
	újCsomópont.previous = nil
	újCsomópont.következő = self.head
	if self.head != nil {
		self.head.previous = újCsomópont
	}
	self.head = újCsomópont
	self.Méret_2++

	if self.head.következő == nil {
		self.tail = self.head
	}

}
func (self *LinkedLista) Append_to_list(mutató uintptr) {
	if self.Méret_2 == 0 {
		self.Prepend_to_list(mutató)
	} else {
		újCsomópont := (*Csomópont)(self.mem.Malloc(uint32(Sizeof(Csomópont{}))))
		if újCsomópont == nil {
			return
		}
		újCsomópont.mutató = mutató
		újCsomópont.previous = self.tail
		újCsomópont.következő = nil
		self.tail.következő = újCsomópont
		self.tail = újCsomópont
		self.Méret_2++
	}
}
func (self *LinkedLista) Insert_at_index(index int, mutató uintptr) {
	if index == 0 {
		self.Prepend_to_list(mutató)
	} else {
		previousCsomópont := self.GetCsomópontat(index - 1)
		következőCsomópont := previousCsomópont.következő
		újCsomópont := (*Csomópont)(self.mem.Malloc(uint32(Sizeof(Csomópont{}))))
		if újCsomópont == nil {
			return
		}
		újCsomópont.mutató = mutató

		previousCsomópont.következő = újCsomópont
		újCsomópont.previous = previousCsomópont
		újCsomópont.következő = következőCsomópont
		if következőCsomópont != nil {
			következőCsomópont.previous = újCsomópont
		}

		self.Méret_2++

		if újCsomópont.következő == nil {
			self.tail = újCsomópont
		}
	}
}
func (self *LinkedLista) GetCsomópontat(index int) *Csomópont {
	if index < 0 || index >= self.Méret_2 {
		return nil
	}
	var x *Csomópont = self.head
	for i := 0; i < index; i++ {
		x = x.következő
	}
	return x
}

func (self *LinkedLista) HalmazCsomópontat(index int, mutató uintptr) {
	var x *Csomópont = self.head
	for i := 0; i < index; i++ {
		x = x.következő
	}
	if x != nil {
		x.mutató = mutató
	}
}
func (self *LinkedLista) Getat(index int) Pointer {
	csomópont := self.GetCsomópontat(index)
	if csomópont == nil {
		return nil
	}
	var mutató uintptr = csomópont.mutató
	return Pointer(mutató)
}
func (self *LinkedLista) Indexof(mutató uintptr) int {
	var n *Csomópont = self.head
	i := 0
	for ; i < self.Méret_2; i++ {
		if mutató == n.mutató {
			return i
		}
		n = n.következő
	}
	return -1
}
func (self *LinkedLista) Eltávolítás(mutató uintptr) {
	index := self.Indexof(mutató)
	if index < 0 {
		return
	}
	self.Eltávolításat(index)
}
func (self *LinkedLista) Eltávolításat(index int) {
	if index < 0 || index >= self.Méret_2 {
		return
	}
	csomópont := self.GetCsomópontat(index)
	if csomópont == nil {
		return
	}
	if csomópont.previous != nil {
		csomópont.previous.következő = csomópont.következő
	} else {
		self.head = csomópont.következő
	}
	if csomópont.következő != nil {
		csomópont.következő.previous = csomópont.previous
	} else {
		self.tail = csomópont.previous
	}
	self.Méret_2 = self.Méret_2 - 1

	if self.mem != nil {
		self.mem.Szabad(Pointer(csomópont))
	}
}

var konzol_2 = TKonzol{}

func (self *LinkedLista) Nyomtatás() {
	konzol_2.MNyomtatásxy("LinkedList:", 1, 1)
	konzol_2.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Méret_2; i++ {
		csomópont := (*Csomópont)(self.Getat(i))
		konzol_2.MUnsignedinteger32Nyomtatás(uint32(csomópont.mutató))
		konzol_2.MNyomtatás(":")
	}
}
