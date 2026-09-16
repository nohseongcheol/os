/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Mサイダイマチギョウレツサイズ uint32 = 0x1FFFFFF
const Qマチギョウレツカイシaddress uint32 = 0x1000000

type Tメモリchunk struct {
	ツギ		*Tメモリchunk
	previous	*Tメモリchunk
	allocated	bool

	サイズ	uint32
}

type Tメモリカンリシャ struct {
}

var first *Tメモリchunk
var Aユウコウメモリカンリシャ *Tメモリカンリシャ = nil
var メモリchunkサイズ uint32

func (self *Tメモリカンリシャ) Init(カイシ uint32, サイズ uint32) {

	Aユウコウメモリカンリシャ = self

	メモリchunkサイズ = uint32(Sizeof(Tメモリchunk{}))

	if サイズ < メモリchunkサイズ {
		first = nil
	} else {
		first = (*Tメモリchunk)(Pointer(uintptr(Qマチギョウレツカイシaddress) + uintptr(カイシ)))
		first.allocated = false
		first.previous = nil
		first.ツギ = nil
		first.サイズ = サイズ - メモリchunkサイズ
	}
}
func (self *Tメモリカンリシャ) Dハキ() {
	if Aユウコウメモリカンリシャ == self {
		Aユウコウメモリカンリシャ = nil
	}
}
func (self *Tメモリカンリシャ) Mキオクリョウイキヲカクホ(サイズ uint32) Pointer {
	var セイセイサキ *Tメモリchunk = nil

	var chunk *Tメモリchunk = first
	for ; chunk != nil && セイセイサキ == nil; chunk = chunk.ツギ {
		if chunk.サイズ > サイズ && !chunk.allocated {
			セイセイサキ = chunk
		}
	}

	if セイセイサキ == nil {
		return nil
	}

	if セイセイサキ.サイズ >= (サイズ + メモリchunkサイズ + 1) {

		var temporary *Tメモリchunk
		temporary = (*Tメモリchunk)(Pointer(uintptr(uint32(uintptr(Pointer(セイセイサキ))) + メモリchunkサイズ + サイズ)))

		temporary.allocated = false
		temporary.サイズ = セイセイサキ.サイズ - サイズ - メモリchunkサイズ
		temporary.previous = セイセイサキ
		temporary.ツギ = セイセイサキ.ツギ

		if temporary.ツギ != nil {
			temporary.ツギ.previous = temporary
		}

		セイセイサキ.サイズ = サイズ
		セイセイサキ.ツギ = temporary
	}
	セイセイサキ.allocated = true

	return Pointer(uintptr(Pointer(セイセイサキ)) + uintptr(メモリchunkサイズ))
}
func (self *Tメモリカンリシャ) Alignedmalloc(サイズ uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if サイズ == 0 || サイズ > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var セイセイサキ *Tメモリchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.ツギ {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(メモリchunkサイズ))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.サイズ && サイズ <= chunk.サイズ-diff {
			セイセイサキ = chunk
			break
		}
	}
	if セイセイサキ == nil {
		return nil, 0
	}
	サイズ += diff
	if セイセイサキ.サイズ-サイズ >= メモリchunkサイズ+1 {
		temporary := (*Tメモリchunk)(Pointer(uintptr(Pointer(セイセイサキ)) + uintptr(メモリchunkサイズ) + uintptr(サイズ)))
		temporary.allocated = false
		temporary.サイズ = セイセイサキ.サイズ - サイズ - メモリchunkサイズ
		temporary.previous = セイセイサキ
		temporary.ツギ = セイセイサキ.ツギ
		if temporary.ツギ != nil {
			temporary.ツギ.previous = temporary
		}
		セイセイサキ.サイズ = サイズ
		セイセイサキ.ツギ = temporary
	}
	セイセイサキ.allocated = true
	return Pointer(uintptr(Pointer(セイセイサキ)) + uintptr(メモリchunkサイズ) + uintptr(diff)), diff
}
func (self *Tメモリカンリシャ) Fアキ(バンチサンショウ_2 Pointer) {
	var chunk *Tメモリchunk = (*Tメモリchunk)(Pointer(uintptr(バンチサンショウ_2) - uintptr(メモリchunkサイズ)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.ツギ = chunk.ツギ
		chunk.previous.サイズ += chunk.サイズ + メモリchunkサイズ
		if chunk.ツギ != nil {
			chunk.ツギ.previous = chunk.previous
		}
	}

	if chunk.ツギ != nil && !chunk.ツギ.allocated {
		chunk.サイズ += chunk.ツギ.サイズ + メモリchunkサイズ
		chunk.ツギ = chunk.ツギ.ツギ
		if chunk.ツギ != nil {
			chunk.ツギ.previous = chunk
		}
	}
}
func Nシンキ(サイズ int) Pointer {
	if Aユウコウメモリカンリシャ == nil {
		return nil
	}
	return Aユウコウメモリカンリシャ.Mキオクリョウイキヲカクホ(uint32(サイズ))
}
func Dサクジョ(バンチサンショウ_2 Pointer) {
	if Aユウコウメモリカンリシャ != nil {
		Aユウコウメモリカンリシャ.Fアキ(バンチサンショウ_2)
	}
}
