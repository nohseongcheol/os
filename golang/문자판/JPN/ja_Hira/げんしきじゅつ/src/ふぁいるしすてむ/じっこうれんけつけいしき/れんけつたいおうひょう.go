package じっこうれんけつけいしき

import . "unsafe"
import . "こんそーる"

import mem "めもりかんりしゃ"

type Lれんけつ struct {
	Dどうてきに		uintptr
	Previous	*Lれんけつ
	Nつぎ		*Lれんけつ
}
type Lれんけつたいおうひょう struct {
	First	*Lれんけつ
	Lさいご	*Lれんけつ

	Sさいず_2	int

	mem	*mem.Tめもりかんりしゃ
}

func (self *Lれんけつたいおうひょう) Init(mem *mem.Tめもりかんりしゃ) {
	self.mem = mem
}
func (self *Lれんけつたいおうひょう) Clone() Lれんけつたいおうひょう {
	var れんけつたいおうひょう Lれんけつたいおうひょう

	れんけつたいおうひょう.Init(self.mem)

	Lれんけつ := self.First

	for ; Lれんけつ != nil; Lれんけつ = Lれんけつ.Nつぎ {
		れんけつたいおうひょう.Mまつびについか(Lれんけつ.Dどうてきに)
	}
	return れんけつたいおうひょう
}
func (self *Lれんけつたいおうひょう) Mせんとうについか(Dどうてきに uintptr) {
	しんきれんけつ := (*Lれんけつ)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Lれんけつ{}))))
	しんきれんけつ.Dどうてきに = Dどうてきに
	しんきれんけつ.Nつぎ = self.First
	self.First = しんきれんけつ
	self.Sさいず_2++

	if self.First.Nつぎ == nil {
		self.Lさいご = self.First
	}
}
func (self *Lれんけつたいおうひょう) Mまつびについか(Dどうてきに uintptr) {
	if Dどうてきに == 0 {
		return
	}

	if self.Sさいず_2 == 0 {
		self.Mせんとうについか(Dどうてきに)
	} else {
		しんきれんけつ := (*Lれんけつ)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Lれんけつ{}))))
		しんきれんけつ.Dどうてきに = Dどうてきに
		しんきれんけつ.Nつぎ = nil
		self.Lさいご.Nつぎ = しんきれんけつ
		self.Lさいご = しんきれんけつ
		self.Sさいず_2++
	}
}
func (self *Lれんけつたいおうひょう) Pいんさつ(x uint16, y uint16) {
	Lれんけつ := self.First
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつxy("linkmap : ", x, y)
	for ; Lれんけつ != nil; Lれんけつ = Lれんけつ.Nつぎ {
		こんそーる_2.MUnsignedinteger32いんさつ(uint32(Lれんけつ.Dどうてきに))
		こんそーる_2.Mいんさつ("+")

	}
}
