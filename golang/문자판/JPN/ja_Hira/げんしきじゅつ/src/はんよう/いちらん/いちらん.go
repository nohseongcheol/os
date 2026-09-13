package いちらん

import . "unsafe"
import . "こんそーる"
import mem "めもりかんりしゃ"

type Tれんけつようそ struct {
	ばんちさんしょう		uintptr
	previous	*Tれんけつようそ
	つぎ		*Tれんけつようそ
}

type Linkedいちらん struct {
	head	*Tれんけつようそ
	tail	*Tれんけつようそ
	Sさいず_2	int

	mem	*mem.Tめもりかんりしゃ
}

func (self *Linkedいちらん) Init(mem *mem.Tめもりかんりしゃ) {
	self.head = nil
	self.tail = nil
	self.Sさいず_2 = 0

	self.mem = mem
}
func (self *Linkedいちらん) Mせんとうについか(ばんちさんしょう uintptr) {
	しんきのーど := (*Tれんけつようそ)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Tれんけつようそ{}))))
	if しんきのーど == nil {
		return
	}
	しんきのーど.ばんちさんしょう = ばんちさんしょう
	しんきのーど.previous = nil
	しんきのーど.つぎ = self.head
	if self.head != nil {
		self.head.previous = しんきのーど
	}
	self.head = しんきのーど
	self.Sさいず_2++

	if self.head.つぎ == nil {
		self.tail = self.head
	}

}
func (self *Linkedいちらん) Mまつびについか(ばんちさんしょう uintptr) {
	if self.Sさいず_2 == 0 {
		self.Mせんとうについか(ばんちさんしょう)
	} else {
		しんきのーど := (*Tれんけつようそ)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Tれんけつようそ{}))))
		if しんきのーど == nil {
			return
		}
		しんきのーど.ばんちさんしょう = ばんちさんしょう
		しんきのーど.previous = self.tail
		しんきのーど.つぎ = nil
		self.tail.つぎ = しんきのーど
		self.tail = しんきのーど
		self.Sさいず_2++
	}
}
func (self *Linkedいちらん) Mしていいちにそうにゅう(もくじ int, ばんちさんしょう uintptr) {
	if もくじ == 0 {
		self.Mせんとうについか(ばんちさんしょう)
	} else {
		previousのーど := self.Getのーどat(もくじ - 1)
		つぎのーど := previousのーど.つぎ
		しんきのーど := (*Tれんけつようそ)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Tれんけつようそ{}))))
		if しんきのーど == nil {
			return
		}
		しんきのーど.ばんちさんしょう = ばんちさんしょう

		previousのーど.つぎ = しんきのーど
		しんきのーど.previous = previousのーど
		しんきのーど.つぎ = つぎのーど
		if つぎのーど != nil {
			つぎのーど.previous = しんきのーど
		}

		self.Sさいず_2++

		if しんきのーど.つぎ == nil {
			self.tail = しんきのーど
		}
	}
}
func (self *Linkedいちらん) Getのーどat(もくじ int) *Tれんけつようそ {
	if もくじ < 0 || もくじ >= self.Sさいず_2 {
		return nil
	}
	var x *Tれんけつようそ = self.head
	for i := 0; i < もくじ; i++ {
		x = x.つぎ
	}
	return x
}

func (self *Linkedいちらん) Sありのーどat(もくじ int, ばんちさんしょう uintptr) {
	var x *Tれんけつようそ = self.head
	for i := 0; i < もくじ; i++ {
		x = x.つぎ
	}
	if x != nil {
		x.ばんちさんしょう = ばんちさんしょう
	}
}
func (self *Linkedいちらん) Getat(もくじ int) Pointer {
	れんけつようそ := self.Getのーどat(もくじ)
	if れんけつようそ == nil {
		return nil
	}
	var ばんちさんしょう uintptr = れんけつようそ.ばんちさんしょう
	return Pointer(ばんちさんしょう)
}
func (self *Linkedいちらん) Iもくじof(ばんちさんしょう uintptr) int {
	var n *Tれんけつようそ = self.head
	i := 0
	for ; i < self.Sさいず_2; i++ {
		if ばんちさんしょう == n.ばんちさんしょう {
			return i
		}
		n = n.つぎ
	}
	return -1
}
func (self *Linkedいちらん) Rさくじょ(ばんちさんしょう uintptr) {
	もくじ := self.Iもくじof(ばんちさんしょう)
	if もくじ < 0 {
		return
	}
	self.Rさくじょat(もくじ)
}
func (self *Linkedいちらん) Rさくじょat(もくじ int) {
	if もくじ < 0 || もくじ >= self.Sさいず_2 {
		return
	}
	れんけつようそ := self.Getのーどat(もくじ)
	if れんけつようそ == nil {
		return
	}
	if れんけつようそ.previous != nil {
		れんけつようそ.previous.つぎ = れんけつようそ.つぎ
	} else {
		self.head = れんけつようそ.つぎ
	}
	if れんけつようそ.つぎ != nil {
		れんけつようそ.つぎ.previous = れんけつようそ.previous
	} else {
		self.tail = れんけつようそ.previous
	}
	self.Sさいず_2 = self.Sさいず_2 - 1

	if self.mem != nil {
		self.mem.Fあき(Pointer(れんけつようそ))
	}
}

var こんそーる_2 = Tこんそーる{}

func (self *Linkedいちらん) Pいんさつ() {
	こんそーる_2.Mいんさつxy("LinkedList:", 1, 1)
	こんそーる_2.MUnsignedinteger32いんさつ(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sさいず_2; i++ {
		れんけつようそ := (*Tれんけつようそ)(self.Getat(i))
		こんそーる_2.MUnsignedinteger32いんさつ(uint32(れんけつようそ.ばんちさんしょう))
		こんそーる_2.Mいんさつ(":")
	}
}
