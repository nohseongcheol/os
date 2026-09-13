package ジッコウレンケツケイシキ

import . "unsafe"
import . "コンソール"

import mem "メモリカンリシャ"

type Lレンケツ struct {
	Dドウテキニ		uintptr
	Previous	*Lレンケツ
	Nツギ		*Lレンケツ
}
type Lレンケツタイオウヒョウ struct {
	First	*Lレンケツ
	Lサイゴ	*Lレンケツ

	Sサイズ_2	int

	mem	*mem.Tメモリカンリシャ
}

func (self *Lレンケツタイオウヒョウ) Init(mem *mem.Tメモリカンリシャ) {
	self.mem = mem
}
func (self *Lレンケツタイオウヒョウ) Clone() Lレンケツタイオウヒョウ {
	var レンケツタイオウヒョウ Lレンケツタイオウヒョウ

	レンケツタイオウヒョウ.Init(self.mem)

	Lレンケツ := self.First

	for ; Lレンケツ != nil; Lレンケツ = Lレンケツ.Nツギ {
		レンケツタイオウヒョウ.Mマツビニツイカ(Lレンケツ.Dドウテキニ)
	}
	return レンケツタイオウヒョウ
}
func (self *Lレンケツタイオウヒョウ) Mセントウニツイカ(Dドウテキニ uintptr) {
	シンキレンケツ := (*Lレンケツ)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Lレンケツ{}))))
	シンキレンケツ.Dドウテキニ = Dドウテキニ
	シンキレンケツ.Nツギ = self.First
	self.First = シンキレンケツ
	self.Sサイズ_2++

	if self.First.Nツギ == nil {
		self.Lサイゴ = self.First
	}
}
func (self *Lレンケツタイオウヒョウ) Mマツビニツイカ(Dドウテキニ uintptr) {
	if Dドウテキニ == 0 {
		return
	}

	if self.Sサイズ_2 == 0 {
		self.Mセントウニツイカ(Dドウテキニ)
	} else {
		シンキレンケツ := (*Lレンケツ)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Lレンケツ{}))))
		シンキレンケツ.Dドウテキニ = Dドウテキニ
		シンキレンケツ.Nツギ = nil
		self.Lサイゴ.Nツギ = シンキレンケツ
		self.Lサイゴ = シンキレンケツ
		self.Sサイズ_2++
	}
}
func (self *Lレンケツタイオウヒョウ) Pインサツ(x uint16, y uint16) {
	Lレンケツ := self.First
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツxy("linkmap : ", x, y)
	for ; Lレンケツ != nil; Lレンケツ = Lレンケツ.Nツギ {
		コンソール_2.MUnsignedinteger32インサツ(uint32(Lレンケツ.Dドウテキニ))
		コンソール_2.Mインサツ("+")

	}
}
