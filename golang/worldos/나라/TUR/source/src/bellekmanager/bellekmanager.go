/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MakqueueBoyut uint32 = 0x1FFFFFF
const QueueBaşlataddress uint32 = 0x1000000

type TBellekchunk struct {
	sonraki		*TBellekchunk
	previous	*TBellekchunk
	allocated	bool

	boyut	uint32
}

type TBellekmanager struct {
}

var first *TBellekchunk
var AktifBellekmanager *TBellekmanager = nil
var bellekchunkBoyut uint32

func (self *TBellekmanager) Init(başlat uint32, boyut uint32) {

	AktifBellekmanager = self

	bellekchunkBoyut = uint32(Sizeof(TBellekchunk{}))

	if boyut < bellekchunkBoyut {
		first = nil
	} else {
		first = (*TBellekchunk)(Pointer(uintptr(QueueBaşlataddress) + uintptr(başlat)))
		first.allocated = false
		first.previous = nil
		first.sonraki = nil
		first.boyut = boyut - bellekchunkBoyut
	}
}
func (self *TBellekmanager) YokEt() {
	if AktifBellekmanager == self {
		AktifBellekmanager = nil
	}
}
func (self *TBellekmanager) Bellek_ayır(boyut uint32) Pointer {
	var sONUÇ *TBellekchunk = nil

	var chunk *TBellekchunk = first
	for ; chunk != nil && sONUÇ == nil; chunk = chunk.sonraki {
		if chunk.boyut > boyut && !chunk.allocated {
			sONUÇ = chunk
		}
	}

	if sONUÇ == nil {
		return nil
	}

	if sONUÇ.boyut >= (boyut + bellekchunkBoyut + 1) {

		var temporary *TBellekchunk
		temporary = (*TBellekchunk)(Pointer(uintptr(uint32(uintptr(Pointer(sONUÇ))) + bellekchunkBoyut + boyut)))

		temporary.allocated = false
		temporary.boyut = sONUÇ.boyut - boyut - bellekchunkBoyut
		temporary.previous = sONUÇ
		temporary.sonraki = sONUÇ.sonraki

		if temporary.sonraki != nil {
			temporary.sonraki.previous = temporary
		}

		sONUÇ.boyut = boyut
		sONUÇ.sonraki = temporary
	}
	sONUÇ.allocated = true

	return Pointer(uintptr(Pointer(sONUÇ)) + uintptr(bellekchunkBoyut))
}
func (self *TBellekmanager) Alignedmalloc(boyut uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if boyut == 0 || boyut > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var sONUÇ *TBellekchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.sonraki {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(bellekchunkBoyut))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.boyut && boyut <= chunk.boyut-diff {
			sONUÇ = chunk
			break
		}
	}
	if sONUÇ == nil {
		return nil, 0
	}
	boyut += diff
	if sONUÇ.boyut-boyut >= bellekchunkBoyut+1 {
		temporary := (*TBellekchunk)(Pointer(uintptr(Pointer(sONUÇ)) + uintptr(bellekchunkBoyut) + uintptr(boyut)))
		temporary.allocated = false
		temporary.boyut = sONUÇ.boyut - boyut - bellekchunkBoyut
		temporary.previous = sONUÇ
		temporary.sonraki = sONUÇ.sonraki
		if temporary.sonraki != nil {
			temporary.sonraki.previous = temporary
		}
		sONUÇ.boyut = boyut
		sONUÇ.sonraki = temporary
	}
	sONUÇ.allocated = true
	return Pointer(uintptr(Pointer(sONUÇ)) + uintptr(bellekchunkBoyut) + uintptr(diff)), diff
}
func (self *TBellekmanager) Boş(adres_başvurusu_2 Pointer) {
	var chunk *TBellekchunk = (*TBellekchunk)(Pointer(uintptr(adres_başvurusu_2) - uintptr(bellekchunkBoyut)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.sonraki = chunk.sonraki
		chunk.previous.boyut += chunk.boyut + bellekchunkBoyut
		if chunk.sonraki != nil {
			chunk.sonraki.previous = chunk.previous
		}
	}

	if chunk.sonraki != nil && !chunk.sonraki.allocated {
		chunk.boyut += chunk.sonraki.boyut + bellekchunkBoyut
		chunk.sonraki = chunk.sonraki.sonraki
		if chunk.sonraki != nil {
			chunk.sonraki.previous = chunk
		}
	}
}
func Yeni(boyut int) Pointer {
	if AktifBellekmanager == nil {
		return nil
	}
	return AktifBellekmanager.Bellek_ayır(uint32(boyut))
}
func Sil(adres_başvurusu_2 Pointer) {
	if AktifBellekmanager != nil {
		AktifBellekmanager.Boş(adres_başvurusu_2)
	}
}
