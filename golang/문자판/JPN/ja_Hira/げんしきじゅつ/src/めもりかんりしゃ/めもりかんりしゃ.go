package memorymananger

import . "unsafe"

const Mさいだいまちぎょうれつさいず uint32 = 0x1FFFFFF
const Qまちぎょうれつかいしaddress uint32 = 0x1000000

type Tめもりchunk struct {
	つぎ		*Tめもりchunk
	previous	*Tめもりchunk
	allocated	bool

	さいず	uint32
}

type Tめもりかんりしゃ struct {
}

var first *Tめもりchunk
var Aゆうこうめもりかんりしゃ *Tめもりかんりしゃ = nil
var めもりchunkさいず uint32

func (self *Tめもりかんりしゃ) Init(かいし uint32, さいず uint32) {

	Aゆうこうめもりかんりしゃ = self

	めもりchunkさいず = uint32(Sizeof(Tめもりchunk{}))

	if さいず < めもりchunkさいず {
		first = nil
	} else {
		first = (*Tめもりchunk)(Pointer(uintptr(Qまちぎょうれつかいしaddress) + uintptr(かいし)))
		first.allocated = false
		first.previous = nil
		first.つぎ = nil
		first.さいず = さいず - めもりchunkさいず
	}
}
func (self *Tめもりかんりしゃ) Dはき() {
	if Aゆうこうめもりかんりしゃ == self {
		Aゆうこうめもりかんりしゃ = nil
	}
}
func (self *Tめもりかんりしゃ) Mきおくりょういきをかくほ(さいず uint32) Pointer {
	var せいせいさき *Tめもりchunk = nil

	var chunk *Tめもりchunk = first
	for ; chunk != nil && せいせいさき == nil; chunk = chunk.つぎ {
		if chunk.さいず > さいず && !chunk.allocated {
			せいせいさき = chunk
		}
	}

	if せいせいさき == nil {
		return nil
	}

	if せいせいさき.さいず >= (さいず + めもりchunkさいず + 1) {

		var temporary *Tめもりchunk
		temporary = (*Tめもりchunk)(Pointer(uintptr(uint32(uintptr(Pointer(せいせいさき))) + めもりchunkさいず + さいず)))

		temporary.allocated = false
		temporary.さいず = せいせいさき.さいず - さいず - めもりchunkさいず
		temporary.previous = せいせいさき
		temporary.つぎ = せいせいさき.つぎ

		if temporary.つぎ != nil {
			temporary.つぎ.previous = temporary
		}

		せいせいさき.さいず = さいず
		せいせいさき.つぎ = temporary
	}
	せいせいさき.allocated = true

	return Pointer(uintptr(Pointer(せいせいさき)) + uintptr(めもりchunkさいず))
}
func (self *Tめもりかんりしゃ) Alignedmalloc(さいず uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if さいず == 0 || さいず > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var せいせいさき *Tめもりchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.つぎ {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(めもりchunkさいず))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.さいず && さいず <= chunk.さいず-diff {
			せいせいさき = chunk
			break
		}
	}
	if せいせいさき == nil {
		return nil, 0
	}
	さいず += diff
	if せいせいさき.さいず-さいず >= めもりchunkさいず+1 {
		temporary := (*Tめもりchunk)(Pointer(uintptr(Pointer(せいせいさき)) + uintptr(めもりchunkさいず) + uintptr(さいず)))
		temporary.allocated = false
		temporary.さいず = せいせいさき.さいず - さいず - めもりchunkさいず
		temporary.previous = せいせいさき
		temporary.つぎ = せいせいさき.つぎ
		if temporary.つぎ != nil {
			temporary.つぎ.previous = temporary
		}
		せいせいさき.さいず = さいず
		せいせいさき.つぎ = temporary
	}
	せいせいさき.allocated = true
	return Pointer(uintptr(Pointer(せいせいさき)) + uintptr(めもりchunkさいず) + uintptr(diff)), diff
}
func (self *Tめもりかんりしゃ) Fあき(ばんちさんしょう_2 Pointer) {
	var chunk *Tめもりchunk = (*Tめもりchunk)(Pointer(uintptr(ばんちさんしょう_2) - uintptr(めもりchunkさいず)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.つぎ = chunk.つぎ
		chunk.previous.さいず += chunk.さいず + めもりchunkさいず
		if chunk.つぎ != nil {
			chunk.つぎ.previous = chunk.previous
		}
	}

	if chunk.つぎ != nil && !chunk.つぎ.allocated {
		chunk.さいず += chunk.つぎ.さいず + めもりchunkさいず
		chunk.つぎ = chunk.つぎ.つぎ
		if chunk.つぎ != nil {
			chunk.つぎ.previous = chunk
		}
	}
}
func Nしんき(さいず int) Pointer {
	if Aゆうこうめもりかんりしゃ == nil {
		return nil
	}
	return Aゆうこうめもりかんりしゃ.Mきおくりょういきをかくほ(uint32(さいず))
}
func Dさくじょ(ばんちさんしょう_2 Pointer) {
	if Aゆうこうめもりかんりしゃ != nil {
		Aゆうこうめもりかんりしゃ.Fあき(ばんちさんしょう_2)
	}
}
