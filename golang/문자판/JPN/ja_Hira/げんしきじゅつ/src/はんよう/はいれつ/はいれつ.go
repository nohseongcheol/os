package はいれつ

import . "unsafe"
import . "こんそーる"

var のーどはいれつ [100]uintptr

type Tはいれつ struct {
	Sさいず_2 int
}

func (self *Tはいれつ) Aついか(ばんちさんしょう uintptr) {
	のーどはいれつ[self.Sさいず_2] = ばんちさんしょう
	self.Sさいず_2++
}
func (self *Tはいれつ) Getat(もくじ int) Pointer {
	return Pointer(のーどはいれつ[もくじ])
}
func (self *Tはいれつ) Iもくじof(ばんちさんしょう uintptr) int {
	i := 0
	for ; i < self.Sさいず_2; i++ {
		if ばんちさんしょう == のーどはいれつ[i] {
			return i
		}
	}
	return -1
}

var こんそーる_2 = Tこんそーる{}

func (self *Tはいれつ) Pいんさつ() {
	こんそーる_2.Mいんさつxy("array:", 1, 1)

	for i := 0; i < self.Sさいず_2; i++ {
		こんそーる_2.MUnsignedinteger32いんさつ(uint32(のーどはいれつ[i]))
		こんそーる_2.Mいんさつ(":")
	}
}
