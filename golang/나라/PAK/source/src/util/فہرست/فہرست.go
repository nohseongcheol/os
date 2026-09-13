package فہرست

import . "unsafe"
import . "console"
import mem "یادداشتmanager"

type Nگرہ struct {
	پؤائنٹر		uintptr
	previous	*Nگرہ
	اگلا		*Nگرہ
}

type Linkedفہرست struct {
	head	*Nگرہ
	tail	*Nگرہ
	Sحجم_2	int

	mem	*mem.Tیادداشتmanager
}

func (self *Linkedفہرست) Init(mem *mem.Tیادداشتmanager) {
	self.head = nil
	self.tail = nil
	self.Sحجم_2 = 0

	self.mem = mem
}
func (self *Linkedفہرست) Prepend_to_list(پؤائنٹر uintptr) {
	نیاگرہ := (*Nگرہ)(self.mem.Malloc(uint32(Sizeof(Nگرہ{}))))
	if نیاگرہ == nil {
		return
	}
	نیاگرہ.پؤائنٹر = پؤائنٹر
	نیاگرہ.previous = nil
	نیاگرہ.اگلا = self.head
	if self.head != nil {
		self.head.previous = نیاگرہ
	}
	self.head = نیاگرہ
	self.Sحجم_2++

	if self.head.اگلا == nil {
		self.tail = self.head
	}

}
func (self *Linkedفہرست) Append_to_list(پؤائنٹر uintptr) {
	if self.Sحجم_2 == 0 {
		self.Prepend_to_list(پؤائنٹر)
	} else {
		نیاگرہ := (*Nگرہ)(self.mem.Malloc(uint32(Sizeof(Nگرہ{}))))
		if نیاگرہ == nil {
			return
		}
		نیاگرہ.پؤائنٹر = پؤائنٹر
		نیاگرہ.previous = self.tail
		نیاگرہ.اگلا = nil
		self.tail.اگلا = نیاگرہ
		self.tail = نیاگرہ
		self.Sحجم_2++
	}
}
func (self *Linkedفہرست) Insert_at_index(index int, پؤائنٹر uintptr) {
	if index == 0 {
		self.Prepend_to_list(پؤائنٹر)
	} else {
		previousگرہ := self.Getگرہat(index - 1)
		اگلاگرہ := previousگرہ.اگلا
		نیاگرہ := (*Nگرہ)(self.mem.Malloc(uint32(Sizeof(Nگرہ{}))))
		if نیاگرہ == nil {
			return
		}
		نیاگرہ.پؤائنٹر = پؤائنٹر

		previousگرہ.اگلا = نیاگرہ
		نیاگرہ.previous = previousگرہ
		نیاگرہ.اگلا = اگلاگرہ
		if اگلاگرہ != nil {
			اگلاگرہ.previous = نیاگرہ
		}

		self.Sحجم_2++

		if نیاگرہ.اگلا == nil {
			self.tail = نیاگرہ
		}
	}
}
func (self *Linkedفہرست) Getگرہat(index int) *Nگرہ {
	if index < 0 || index >= self.Sحجم_2 {
		return nil
	}
	var x *Nگرہ = self.head
	for i := 0; i < index; i++ {
		x = x.اگلا
	}
	return x
}

func (self *Linkedفہرست) Sسیٹگرہat(index int, پؤائنٹر uintptr) {
	var x *Nگرہ = self.head
	for i := 0; i < index; i++ {
		x = x.اگلا
	}
	if x != nil {
		x.پؤائنٹر = پؤائنٹر
	}
}
func (self *Linkedفہرست) Getat(index int) Pointer {
	گرہ := self.Getگرہat(index)
	if گرہ == nil {
		return nil
	}
	var پؤائنٹر uintptr = گرہ.پؤائنٹر
	return Pointer(پؤائنٹر)
}
func (self *Linkedفہرست) Indexبرائے(پؤائنٹر uintptr) int {
	var n *Nگرہ = self.head
	i := 0
	for ; i < self.Sحجم_2; i++ {
		if پؤائنٹر == n.پؤائنٹر {
			return i
		}
		n = n.اگلا
	}
	return -1
}
func (self *Linkedفہرست) Rحذفکریں(پؤائنٹر uintptr) {
	index := self.Indexبرائے(پؤائنٹر)
	if index < 0 {
		return
	}
	self.Rحذفکریںat(index)
}
func (self *Linkedفہرست) Rحذفکریںat(index int) {
	if index < 0 || index >= self.Sحجم_2 {
		return
	}
	گرہ := self.Getگرہat(index)
	if گرہ == nil {
		return
	}
	if گرہ.previous != nil {
		گرہ.previous.اگلا = گرہ.اگلا
	} else {
		self.head = گرہ.اگلا
	}
	if گرہ.اگلا != nil {
		گرہ.اگلا.previous = گرہ.previous
	} else {
		self.tail = گرہ.previous
	}
	self.Sحجم_2 = self.Sحجم_2 - 1

	if self.mem != nil {
		self.mem.Fخالی(Pointer(گرہ))
	}
}

var console_2 = TConsole{}

func (self *Linkedفہرست) Pچھاپیں() {
	console_2.Mچھاپیںxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sحجم_2; i++ {
		گرہ := (*Nگرہ)(self.Getat(i))
		console_2.MUnsignedinteger32چھاپیں(uint32(گرہ.پؤائنٹر))
		console_2.Mچھاپیں(":")
	}
}
