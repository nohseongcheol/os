package memorymananger

import . "unsafe"

const M最大待ち行列サイズ uint32 = 0x1FFFFFF
const Q待ち行列開始address uint32 = 0x1000000

type Tメモリchunk struct {
	次		*Tメモリchunk
	previous	*Tメモリchunk
	allocated	bool

	サイズ	uint32
}

type Tメモリ管理者 struct {
}

var first *Tメモリchunk
var A有効メモリ管理者 *Tメモリ管理者 = nil
var メモリchunkサイズ uint32

func (self *Tメモリ管理者) Init(開始 uint32, サイズ uint32) {

	A有効メモリ管理者 = self

	メモリchunkサイズ = uint32(Sizeof(Tメモリchunk{}))

	if サイズ < メモリchunkサイズ {
		first = nil
	} else {
		first = (*Tメモリchunk)(Pointer(uintptr(Q待ち行列開始address) + uintptr(開始)))
		first.allocated = false
		first.previous = nil
		first.次 = nil
		first.サイズ = サイズ - メモリchunkサイズ
	}
}
func (self *Tメモリ管理者) D破棄() {
	if A有効メモリ管理者 == self {
		A有効メモリ管理者 = nil
	}
}
func (self *Tメモリ管理者) M記憶領域を確保(サイズ uint32) Pointer {
	var 生成先 *Tメモリchunk = nil

	var chunk *Tメモリchunk = first
	for ; chunk != nil && 生成先 == nil; chunk = chunk.次 {
		if chunk.サイズ > サイズ && !chunk.allocated {
			生成先 = chunk
		}
	}

	if 生成先 == nil {
		return nil
	}

	if 生成先.サイズ >= (サイズ + メモリchunkサイズ + 1) {

		var temporary *Tメモリchunk
		temporary = (*Tメモリchunk)(Pointer(uintptr(uint32(uintptr(Pointer(生成先))) + メモリchunkサイズ + サイズ)))

		temporary.allocated = false
		temporary.サイズ = 生成先.サイズ - サイズ - メモリchunkサイズ
		temporary.previous = 生成先
		temporary.次 = 生成先.次

		if temporary.次 != nil {
			temporary.次.previous = temporary
		}

		生成先.サイズ = サイズ
		生成先.次 = temporary
	}
	生成先.allocated = true

	return Pointer(uintptr(Pointer(生成先)) + uintptr(メモリchunkサイズ))
}
func (self *Tメモリ管理者) Alignedmalloc(サイズ uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if サイズ == 0 || サイズ > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var 生成先 *Tメモリchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.次 {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(メモリchunkサイズ))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.サイズ && サイズ <= chunk.サイズ-diff {
			生成先 = chunk
			break
		}
	}
	if 生成先 == nil {
		return nil, 0
	}
	サイズ += diff
	if 生成先.サイズ-サイズ >= メモリchunkサイズ+1 {
		temporary := (*Tメモリchunk)(Pointer(uintptr(Pointer(生成先)) + uintptr(メモリchunkサイズ) + uintptr(サイズ)))
		temporary.allocated = false
		temporary.サイズ = 生成先.サイズ - サイズ - メモリchunkサイズ
		temporary.previous = 生成先
		temporary.次 = 生成先.次
		if temporary.次 != nil {
			temporary.次.previous = temporary
		}
		生成先.サイズ = サイズ
		生成先.次 = temporary
	}
	生成先.allocated = true
	return Pointer(uintptr(Pointer(生成先)) + uintptr(メモリchunkサイズ) + uintptr(diff)), diff
}
func (self *Tメモリ管理者) F空き(番地参照_2 Pointer) {
	var chunk *Tメモリchunk = (*Tメモリchunk)(Pointer(uintptr(番地参照_2) - uintptr(メモリchunkサイズ)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.次 = chunk.次
		chunk.previous.サイズ += chunk.サイズ + メモリchunkサイズ
		if chunk.次 != nil {
			chunk.次.previous = chunk.previous
		}
	}

	if chunk.次 != nil && !chunk.次.allocated {
		chunk.サイズ += chunk.次.サイズ + メモリchunkサイズ
		chunk.次 = chunk.次.次
		if chunk.次 != nil {
			chunk.次.previous = chunk
		}
	}
}
func N新規(サイズ int) Pointer {
	if A有効メモリ管理者 == nil {
		return nil
	}
	return A有効メモリ管理者.M記憶領域を確保(uint32(サイズ))
}
func D削除(番地参照_2 Pointer) {
	if A有効メモリ管理者 != nil {
		A有効メモリ管理者.F空き(番地参照_2)
	}
}
