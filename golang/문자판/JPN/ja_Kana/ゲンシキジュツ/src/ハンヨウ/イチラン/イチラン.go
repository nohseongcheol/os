package イチラン

import . "unsafe"
import . "コンソール"
import mem "メモリカンリシャ"

type Tレンケツヨウソ struct {
	バンチサンショウ		uintptr
	previous	*Tレンケツヨウソ
	ツギ		*Tレンケツヨウソ
}

type Linkedイチラン struct {
	head	*Tレンケツヨウソ
	tail	*Tレンケツヨウソ
	Sサイズ_2	int

	mem	*mem.Tメモリカンリシャ
}

func (self *Linkedイチラン) Init(mem *mem.Tメモリカンリシャ) {
	self.head = nil
	self.tail = nil
	self.Sサイズ_2 = 0

	self.mem = mem
}
func (self *Linkedイチラン) Mセントウニツイカ(バンチサンショウ uintptr) {
	シンキノード := (*Tレンケツヨウソ)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Tレンケツヨウソ{}))))
	if シンキノード == nil {
		return
	}
	シンキノード.バンチサンショウ = バンチサンショウ
	シンキノード.previous = nil
	シンキノード.ツギ = self.head
	if self.head != nil {
		self.head.previous = シンキノード
	}
	self.head = シンキノード
	self.Sサイズ_2++

	if self.head.ツギ == nil {
		self.tail = self.head
	}

}
func (self *Linkedイチラン) Mマツビニツイカ(バンチサンショウ uintptr) {
	if self.Sサイズ_2 == 0 {
		self.Mセントウニツイカ(バンチサンショウ)
	} else {
		シンキノード := (*Tレンケツヨウソ)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Tレンケツヨウソ{}))))
		if シンキノード == nil {
			return
		}
		シンキノード.バンチサンショウ = バンチサンショウ
		シンキノード.previous = self.tail
		シンキノード.ツギ = nil
		self.tail.ツギ = シンキノード
		self.tail = シンキノード
		self.Sサイズ_2++
	}
}
func (self *Linkedイチラン) Mシテイイチニソウニュウ(モクジ int, バンチサンショウ uintptr) {
	if モクジ == 0 {
		self.Mセントウニツイカ(バンチサンショウ)
	} else {
		previousノード := self.Getノードat(モクジ - 1)
		ツギノード := previousノード.ツギ
		シンキノード := (*Tレンケツヨウソ)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Tレンケツヨウソ{}))))
		if シンキノード == nil {
			return
		}
		シンキノード.バンチサンショウ = バンチサンショウ

		previousノード.ツギ = シンキノード
		シンキノード.previous = previousノード
		シンキノード.ツギ = ツギノード
		if ツギノード != nil {
			ツギノード.previous = シンキノード
		}

		self.Sサイズ_2++

		if シンキノード.ツギ == nil {
			self.tail = シンキノード
		}
	}
}
func (self *Linkedイチラン) Getノードat(モクジ int) *Tレンケツヨウソ {
	if モクジ < 0 || モクジ >= self.Sサイズ_2 {
		return nil
	}
	var x *Tレンケツヨウソ = self.head
	for i := 0; i < モクジ; i++ {
		x = x.ツギ
	}
	return x
}

func (self *Linkedイチラン) Sアリノードat(モクジ int, バンチサンショウ uintptr) {
	var x *Tレンケツヨウソ = self.head
	for i := 0; i < モクジ; i++ {
		x = x.ツギ
	}
	if x != nil {
		x.バンチサンショウ = バンチサンショウ
	}
}
func (self *Linkedイチラン) Getat(モクジ int) Pointer {
	レンケツヨウソ := self.Getノードat(モクジ)
	if レンケツヨウソ == nil {
		return nil
	}
	var バンチサンショウ uintptr = レンケツヨウソ.バンチサンショウ
	return Pointer(バンチサンショウ)
}
func (self *Linkedイチラン) Iモクジof(バンチサンショウ uintptr) int {
	var n *Tレンケツヨウソ = self.head
	i := 0
	for ; i < self.Sサイズ_2; i++ {
		if バンチサンショウ == n.バンチサンショウ {
			return i
		}
		n = n.ツギ
	}
	return -1
}
func (self *Linkedイチラン) Rサクジョ(バンチサンショウ uintptr) {
	モクジ := self.Iモクジof(バンチサンショウ)
	if モクジ < 0 {
		return
	}
	self.Rサクジョat(モクジ)
}
func (self *Linkedイチラン) Rサクジョat(モクジ int) {
	if モクジ < 0 || モクジ >= self.Sサイズ_2 {
		return
	}
	レンケツヨウソ := self.Getノードat(モクジ)
	if レンケツヨウソ == nil {
		return
	}
	if レンケツヨウソ.previous != nil {
		レンケツヨウソ.previous.ツギ = レンケツヨウソ.ツギ
	} else {
		self.head = レンケツヨウソ.ツギ
	}
	if レンケツヨウソ.ツギ != nil {
		レンケツヨウソ.ツギ.previous = レンケツヨウソ.previous
	} else {
		self.tail = レンケツヨウソ.previous
	}
	self.Sサイズ_2 = self.Sサイズ_2 - 1

	if self.mem != nil {
		self.mem.Fアキ(Pointer(レンケツヨウソ))
	}
}

var コンソール_2 = Tコンソール{}

func (self *Linkedイチラン) Pインサツ() {
	コンソール_2.Mインサツxy("LinkedList:", 1, 1)
	コンソール_2.MUnsignedinteger32インサツ(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sサイズ_2; i++ {
		レンケツヨウソ := (*Tレンケツヨウソ)(self.Getat(i))
		コンソール_2.MUnsignedinteger32インサツ(uint32(レンケツヨウソ.バンチサンショウ))
		コンソール_2.Mインサツ(":")
	}
}
