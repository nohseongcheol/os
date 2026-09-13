package רשימה

import . "unsafe"
import . "console"
import mem "זיכרוןmanager"

type Nצומת struct {
	סמן		uintptr
	previous	*Nצומת
	הבא		*Nצומת
}

type Linkedרשימה struct {
	head	*Nצומת
	tail	*Nצומת
	Sגודל_2	int

	mem	*mem.Tזיכרוןmanager
}

func (self *Linkedרשימה) Init(mem *mem.Tזיכרוןmanager) {
	self.head = nil
	self.tail = nil
	self.Sגודל_2 = 0

	self.mem = mem
}
func (self *Linkedרשימה) Prepend_to_list(סמן uintptr) {
	חדשצומת := (*Nצומת)(self.mem.Malloc(uint32(Sizeof(Nצומת{}))))
	if חדשצומת == nil {
		return
	}
	חדשצומת.סמן = סמן
	חדשצומת.previous = nil
	חדשצומת.הבא = self.head
	if self.head != nil {
		self.head.previous = חדשצומת
	}
	self.head = חדשצומת
	self.Sגודל_2++

	if self.head.הבא == nil {
		self.tail = self.head
	}

}
func (self *Linkedרשימה) Append_to_list(סמן uintptr) {
	if self.Sגודל_2 == 0 {
		self.Prepend_to_list(סמן)
	} else {
		חדשצומת := (*Nצומת)(self.mem.Malloc(uint32(Sizeof(Nצומת{}))))
		if חדשצומת == nil {
			return
		}
		חדשצומת.סמן = סמן
		חדשצומת.previous = self.tail
		חדשצומת.הבא = nil
		self.tail.הבא = חדשצומת
		self.tail = חדשצומת
		self.Sגודל_2++
	}
}
func (self *Linkedרשימה) Insert_at_index(מפתח int, סמן uintptr) {
	if מפתח == 0 {
		self.Prepend_to_list(סמן)
	} else {
		previousצומת := self.Getצומתat(מפתח - 1)
		הבאצומת := previousצומת.הבא
		חדשצומת := (*Nצומת)(self.mem.Malloc(uint32(Sizeof(Nצומת{}))))
		if חדשצומת == nil {
			return
		}
		חדשצומת.סמן = סמן

		previousצומת.הבא = חדשצומת
		חדשצומת.previous = previousצומת
		חדשצומת.הבא = הבאצומת
		if הבאצומת != nil {
			הבאצומת.previous = חדשצומת
		}

		self.Sגודל_2++

		if חדשצומת.הבא == nil {
			self.tail = חדשצומת
		}
	}
}
func (self *Linkedרשימה) Getצומתat(מפתח int) *Nצומת {
	if מפתח < 0 || מפתח >= self.Sגודל_2 {
		return nil
	}
	var x *Nצומת = self.head
	for i := 0; i < מפתח; i++ {
		x = x.הבא
	}
	return x
}

func (self *Linkedרשימה) Sקבעצומתat(מפתח int, סמן uintptr) {
	var x *Nצומת = self.head
	for i := 0; i < מפתח; i++ {
		x = x.הבא
	}
	if x != nil {
		x.סמן = סמן
	}
}
func (self *Linkedרשימה) Getat(מפתח int) Pointer {
	צומת := self.Getצומתat(מפתח)
	if צומת == nil {
		return nil
	}
	var סמן uintptr = צומת.סמן
	return Pointer(סמן)
}
func (self *Linkedרשימה) Iמפתחמתוך(סמן uintptr) int {
	var n *Nצומת = self.head
	i := 0
	for ; i < self.Sגודל_2; i++ {
		if סמן == n.סמן {
			return i
		}
		n = n.הבא
	}
	return -1
}
func (self *Linkedרשימה) Rהסר(סמן uintptr) {
	מפתח := self.Iמפתחמתוך(סמן)
	if מפתח < 0 {
		return
	}
	self.Rהסרat(מפתח)
}
func (self *Linkedרשימה) Rהסרat(מפתח int) {
	if מפתח < 0 || מפתח >= self.Sגודל_2 {
		return
	}
	צומת := self.Getצומתat(מפתח)
	if צומת == nil {
		return
	}
	if צומת.previous != nil {
		צומת.previous.הבא = צומת.הבא
	} else {
		self.head = צומת.הבא
	}
	if צומת.הבא != nil {
		צומת.הבא.previous = צומת.previous
	} else {
		self.tail = צומת.previous
	}
	self.Sגודל_2 = self.Sגודל_2 - 1

	if self.mem != nil {
		self.mem.Fפנוי(Pointer(צומת))
	}
}

var console_2 = TConsole{}

func (self *Linkedרשימה) Pהדפסה() {
	console_2.Mהדפסהxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sגודל_2; i++ {
		צומת := (*Nצומת)(self.Getat(i))
		console_2.MUnsignedinteger32הדפסה(uint32(צומת.סמן))
		console_2.Mהדפסה(":")
	}
}
