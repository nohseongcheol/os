/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaksqueueUkuran uint32 = 0x1FFFFFF
const QueueMulaiaddress uint32 = 0x1000000

type TMemorichunk struct {
	berikutnya	*TMemorichunk
	previous	*TMemorichunk
	allocated	bool

	ukuran	uint32
}

type TMemorimanager struct {
}

var first *TMemorichunk
var AktifMemorimanager *TMemorimanager = nil
var memorichunkUkuran uint32

func (dirisendiri *TMemorimanager) Init(mulai uint32, ukuran uint32) {

	AktifMemorimanager = dirisendiri

	memorichunkUkuran = uint32(Sizeof(TMemorichunk{}))

	if ukuran < memorichunkUkuran {
		first = nil
	} else {
		first = (*TMemorichunk)(Pointer(uintptr(QueueMulaiaddress) + uintptr(mulai)))
		first.allocated = false
		first.previous = nil
		first.berikutnya = nil
		first.ukuran = ukuran - memorichunkUkuran
	}
}
func (dirisendiri *TMemorimanager) Lenyapkan() {
	if AktifMemorimanager == dirisendiri {
		AktifMemorimanager = nil
	}
}
func (dirisendiri *TMemorimanager) Alokasikan_memori(ukuran uint32) Pointer {
	var hASIL *TMemorichunk = nil

	var chunk *TMemorichunk = first
	for ; chunk != nil && hASIL == nil; chunk = chunk.berikutnya {
		if chunk.ukuran > ukuran && !chunk.allocated {
			hASIL = chunk
		}
	}

	if hASIL == nil {
		return nil
	}

	if hASIL.ukuran >= (ukuran + memorichunkUkuran + 1) {

		var temporary *TMemorichunk
		temporary = (*TMemorichunk)(Pointer(uintptr(uint32(uintptr(Pointer(hASIL))) + memorichunkUkuran + ukuran)))

		temporary.allocated = false
		temporary.ukuran = hASIL.ukuran - ukuran - memorichunkUkuran
		temporary.previous = hASIL
		temporary.berikutnya = hASIL.berikutnya

		if temporary.berikutnya != nil {
			temporary.berikutnya.previous = temporary
		}

		hASIL.ukuran = ukuran
		hASIL.berikutnya = temporary
	}
	hASIL.allocated = true

	return Pointer(uintptr(Pointer(hASIL)) + uintptr(memorichunkUkuran))
}
func (dirisendiri *TMemorimanager) Alignedmalloc(ukuran uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ukuran == 0 || ukuran > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var hASIL *TMemorichunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.berikutnya {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorichunkUkuran))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ukuran && ukuran <= chunk.ukuran-diff {
			hASIL = chunk
			break
		}
	}
	if hASIL == nil {
		return nil, 0
	}
	ukuran += diff
	if hASIL.ukuran-ukuran >= memorichunkUkuran+1 {
		temporary := (*TMemorichunk)(Pointer(uintptr(Pointer(hASIL)) + uintptr(memorichunkUkuran) + uintptr(ukuran)))
		temporary.allocated = false
		temporary.ukuran = hASIL.ukuran - ukuran - memorichunkUkuran
		temporary.previous = hASIL
		temporary.berikutnya = hASIL.berikutnya
		if temporary.berikutnya != nil {
			temporary.berikutnya.previous = temporary
		}
		hASIL.ukuran = ukuran
		hASIL.berikutnya = temporary
	}
	hASIL.allocated = true
	return Pointer(uintptr(Pointer(hASIL)) + uintptr(memorichunkUkuran) + uintptr(diff)), diff
}
func (dirisendiri *TMemorimanager) Bebas(acuan_alamat_2 Pointer) {
	var chunk *TMemorichunk = (*TMemorichunk)(Pointer(uintptr(acuan_alamat_2) - uintptr(memorichunkUkuran)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.berikutnya = chunk.berikutnya
		chunk.previous.ukuran += chunk.ukuran + memorichunkUkuran
		if chunk.berikutnya != nil {
			chunk.berikutnya.previous = chunk.previous
		}
	}

	if chunk.berikutnya != nil && !chunk.berikutnya.allocated {
		chunk.ukuran += chunk.berikutnya.ukuran + memorichunkUkuran
		chunk.berikutnya = chunk.berikutnya.berikutnya
		if chunk.berikutnya != nil {
			chunk.berikutnya.previous = chunk
		}
	}
}
func Baru(ukuran int) Pointer {
	if AktifMemorimanager == nil {
		return nil
	}
	return AktifMemorimanager.Alokasikan_memori(uint32(ukuran))
}
func Hapus(acuan_alamat_2 Pointer) {
	if AktifMemorimanager != nil {
		AktifMemorimanager.Bebas(acuan_alamat_2)
	}
}
