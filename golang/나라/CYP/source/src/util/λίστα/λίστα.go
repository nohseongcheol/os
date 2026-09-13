package λίστα

import . "unsafe"
import . "console"
import mem "μνήμηmanager"

type Κόμβος struct {
	δείκτης		uintptr
	previous	*Κόμβος
	επόμενο		*Κόμβος
}

type LinkedΛίστα struct {
	head		*Κόμβος
	tail		*Κόμβος
	Μέγεθος_2	int

	mem	*mem.TΜνήμηmanager
}

func (self *LinkedΛίστα) Init(mem *mem.TΜνήμηmanager) {
	self.head = nil
	self.tail = nil
	self.Μέγεθος_2 = 0

	self.mem = mem
}
func (self *LinkedΛίστα) Prepend_to_list(δείκτης uintptr) {
	νέοΚόμβος := (*Κόμβος)(self.mem.Malloc(uint32(Sizeof(Κόμβος{}))))
	if νέοΚόμβος == nil {
		return
	}
	νέοΚόμβος.δείκτης = δείκτης
	νέοΚόμβος.previous = nil
	νέοΚόμβος.επόμενο = self.head
	if self.head != nil {
		self.head.previous = νέοΚόμβος
	}
	self.head = νέοΚόμβος
	self.Μέγεθος_2++

	if self.head.επόμενο == nil {
		self.tail = self.head
	}

}
func (self *LinkedΛίστα) Append_to_list(δείκτης uintptr) {
	if self.Μέγεθος_2 == 0 {
		self.Prepend_to_list(δείκτης)
	} else {
		νέοΚόμβος := (*Κόμβος)(self.mem.Malloc(uint32(Sizeof(Κόμβος{}))))
		if νέοΚόμβος == nil {
			return
		}
		νέοΚόμβος.δείκτης = δείκτης
		νέοΚόμβος.previous = self.tail
		νέοΚόμβος.επόμενο = nil
		self.tail.επόμενο = νέοΚόμβος
		self.tail = νέοΚόμβος
		self.Μέγεθος_2++
	}
}
func (self *LinkedΛίστα) Insert_at_index(κατάλογος int, δείκτης uintptr) {
	if κατάλογος == 0 {
		self.Prepend_to_list(δείκτης)
	} else {
		previousΚόμβος := self.GetΚόμβοςat(κατάλογος - 1)
		επόμενοΚόμβος := previousΚόμβος.επόμενο
		νέοΚόμβος := (*Κόμβος)(self.mem.Malloc(uint32(Sizeof(Κόμβος{}))))
		if νέοΚόμβος == nil {
			return
		}
		νέοΚόμβος.δείκτης = δείκτης

		previousΚόμβος.επόμενο = νέοΚόμβος
		νέοΚόμβος.previous = previousΚόμβος
		νέοΚόμβος.επόμενο = επόμενοΚόμβος
		if επόμενοΚόμβος != nil {
			επόμενοΚόμβος.previous = νέοΚόμβος
		}

		self.Μέγεθος_2++

		if νέοΚόμβος.επόμενο == nil {
			self.tail = νέοΚόμβος
		}
	}
}
func (self *LinkedΛίστα) GetΚόμβοςat(κατάλογος int) *Κόμβος {
	if κατάλογος < 0 || κατάλογος >= self.Μέγεθος_2 {
		return nil
	}
	var x *Κόμβος = self.head
	for i := 0; i < κατάλογος; i++ {
		x = x.επόμενο
	}
	return x
}

func (self *LinkedΛίστα) ΣύνολοΚόμβοςat(κατάλογος int, δείκτης uintptr) {
	var x *Κόμβος = self.head
	for i := 0; i < κατάλογος; i++ {
		x = x.επόμενο
	}
	if x != nil {
		x.δείκτης = δείκτης
	}
}
func (self *LinkedΛίστα) Getat(κατάλογος int) Pointer {
	κόμβος_2 := self.GetΚόμβοςat(κατάλογος)
	if κόμβος_2 == nil {
		return nil
	}
	var δείκτης uintptr = κόμβος_2.δείκτης
	return Pointer(δείκτης)
}
func (self *LinkedΛίστα) Κατάλογοςαπό(δείκτης uintptr) int {
	var n *Κόμβος = self.head
	i := 0
	for ; i < self.Μέγεθος_2; i++ {
		if δείκτης == n.δείκτης {
			return i
		}
		n = n.επόμενο
	}
	return -1
}
func (self *LinkedΛίστα) Αφαίρεση(δείκτης uintptr) {
	κατάλογος := self.Κατάλογοςαπό(δείκτης)
	if κατάλογος < 0 {
		return
	}
	self.Αφαίρεσηat(κατάλογος)
}
func (self *LinkedΛίστα) Αφαίρεσηat(κατάλογος int) {
	if κατάλογος < 0 || κατάλογος >= self.Μέγεθος_2 {
		return
	}
	κόμβος_2 := self.GetΚόμβοςat(κατάλογος)
	if κόμβος_2 == nil {
		return
	}
	if κόμβος_2.previous != nil {
		κόμβος_2.previous.επόμενο = κόμβος_2.επόμενο
	} else {
		self.head = κόμβος_2.επόμενο
	}
	if κόμβος_2.επόμενο != nil {
		κόμβος_2.επόμενο.previous = κόμβος_2.previous
	} else {
		self.tail = κόμβος_2.previous
	}
	self.Μέγεθος_2 = self.Μέγεθος_2 - 1

	if self.mem != nil {
		self.mem.Ελεύθερα(Pointer(κόμβος_2))
	}
}

var console_2 = TConsole{}

func (self *LinkedΛίστα) Εκτύπωση() {
	console_2.MΕκτύπωσηxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Μέγεθος_2; i++ {
		κόμβος_2 := (*Κόμβος)(self.Getat(i))
		console_2.MUnsignedinteger32Εκτύπωση(uint32(κόμβος_2.δείκτης))
		console_2.MΕκτύπωση(":")
	}
}
