package elf

import . "unsafe"
import . "console"

import mem "μνήμηmanager"

type Δεσμός struct {
	Δυναμικό	uintptr
	Previous	*Δεσμός
	Επόμενο		*Δεσμός
}
type Δεσμόςmap struct {
	First		*Δεσμός
	Τελευταία	*Δεσμός

	Μέγεθος_2	int

	mem	*mem.TΜνήμηmanager
}

func (self *Δεσμόςmap) Init(mem *mem.TΜνήμηmanager) {
	self.mem = mem
}
func (self *Δεσμόςmap) Clone() Δεσμόςmap {
	var δεσμόςmap Δεσμόςmap

	δεσμόςmap.Init(self.mem)

	Δεσμός := self.First

	for ; Δεσμός != nil; Δεσμός = Δεσμός.Επόμενο {
		δεσμόςmap.Append_to_list(Δεσμός.Δυναμικό)
	}
	return δεσμόςmap
}
func (self *Δεσμόςmap) Prepend_to_list(Δυναμικό uintptr) {
	νέοΔεσμός := (*Δεσμός)(self.mem.Malloc(uint32(Sizeof(Δεσμός{}))))
	νέοΔεσμός.Δυναμικό = Δυναμικό
	νέοΔεσμός.Επόμενο = self.First
	self.First = νέοΔεσμός
	self.Μέγεθος_2++

	if self.First.Επόμενο == nil {
		self.Τελευταία = self.First
	}
}
func (self *Δεσμόςmap) Append_to_list(Δυναμικό uintptr) {
	if Δυναμικό == 0 {
		return
	}

	if self.Μέγεθος_2 == 0 {
		self.Prepend_to_list(Δυναμικό)
	} else {
		νέοΔεσμός := (*Δεσμός)(self.mem.Malloc(uint32(Sizeof(Δεσμός{}))))
		νέοΔεσμός.Δυναμικό = Δυναμικό
		νέοΔεσμός.Επόμενο = nil
		self.Τελευταία.Επόμενο = νέοΔεσμός
		self.Τελευταία = νέοΔεσμός
		self.Μέγεθος_2++
	}
}
func (self *Δεσμόςmap) Εκτύπωση(x uint16, y uint16) {
	Δεσμός := self.First
	console_2 := TConsole{}
	console_2.MΕκτύπωσηxy("linkmap : ", x, y)
	for ; Δεσμός != nil; Δεσμός = Δεσμός.Επόμενο {
		console_2.MUnsignedinteger32Εκτύπωση(uint32(Δεσμός.Δυναμικό))
		console_2.MΕκτύπωση("+")

	}
}
