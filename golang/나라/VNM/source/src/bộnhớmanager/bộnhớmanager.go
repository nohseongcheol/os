package memorymananger

import . "unsafe"

const MaxqueueCỡ uint32 = 0x1FFFFFF
const QueueChạyaddress uint32 = 0x1000000

type TBộnhớchunk struct {
	kế		*TBộnhớchunk
	previous	*TBộnhớchunk
	allocated	bool

	cỡ	uint32
}

type TBộnhớmanager struct {
}

var đầu *TBộnhớchunk
var HoạtđộngBộnhớmanager *TBộnhớmanager = nil
var bộnhớchunkCỡ uint32

func (mình *TBộnhớmanager) Init(chạy uint32, cỡ uint32) {

	HoạtđộngBộnhớmanager = mình

	bộnhớchunkCỡ = uint32(Sizeof(TBộnhớchunk{}))

	if cỡ < bộnhớchunkCỡ {
		đầu = nil
	} else {
		đầu = (*TBộnhớchunk)(Pointer(uintptr(QueueChạyaddress) + uintptr(chạy)))
		đầu.allocated = false
		đầu.previous = nil
		đầu.kế = nil
		đầu.cỡ = cỡ - bộnhớchunkCỡ
	}
}
func (mình *TBộnhớmanager) Huỷbỏ() {
	if HoạtđộngBộnhớmanager == mình {
		HoạtđộngBộnhớmanager = nil
	}
}
func (mình *TBộnhớmanager) Cấp_phát_bộ_nhớ(cỡ uint32) Pointer {
	var result *TBộnhớchunk = nil

	var chunk *TBộnhớchunk = đầu
	for ; chunk != nil && result == nil; chunk = chunk.kế {
		if chunk.cỡ > cỡ && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.cỡ >= (cỡ + bộnhớchunkCỡ + 1) {

		var temporary *TBộnhớchunk
		temporary = (*TBộnhớchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + bộnhớchunkCỡ + cỡ)))

		temporary.allocated = false
		temporary.cỡ = result.cỡ - cỡ - bộnhớchunkCỡ
		temporary.previous = result
		temporary.kế = result.kế

		if temporary.kế != nil {
			temporary.kế.previous = temporary
		}

		result.cỡ = cỡ
		result.kế = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(bộnhớchunkCỡ))
}
func (mình *TBộnhớmanager) Alignedmalloc(cỡ uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if cỡ == 0 || cỡ > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TBộnhớchunk
	var diff uint32
	for chunk := đầu; chunk != nil; chunk = chunk.kế {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(bộnhớchunkCỡ))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.cỡ && cỡ <= chunk.cỡ-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	cỡ += diff
	if result.cỡ-cỡ >= bộnhớchunkCỡ+1 {
		temporary := (*TBộnhớchunk)(Pointer(uintptr(Pointer(result)) + uintptr(bộnhớchunkCỡ) + uintptr(cỡ)))
		temporary.allocated = false
		temporary.cỡ = result.cỡ - cỡ - bộnhớchunkCỡ
		temporary.previous = result
		temporary.kế = result.kế
		if temporary.kế != nil {
			temporary.kế.previous = temporary
		}
		result.cỡ = cỡ
		result.kế = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(bộnhớchunkCỡ) + uintptr(diff)), diff
}
func (mình *TBộnhớmanager) Rảnh(tham_chiếu_địa_chỉ_2 Pointer) {
	var chunk *TBộnhớchunk = (*TBộnhớchunk)(Pointer(uintptr(tham_chiếu_địa_chỉ_2) - uintptr(bộnhớchunkCỡ)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.kế = chunk.kế
		chunk.previous.cỡ += chunk.cỡ + bộnhớchunkCỡ
		if chunk.kế != nil {
			chunk.kế.previous = chunk.previous
		}
	}

	if chunk.kế != nil && !chunk.kế.allocated {
		chunk.cỡ += chunk.kế.cỡ + bộnhớchunkCỡ
		chunk.kế = chunk.kế.kế
		if chunk.kế != nil {
			chunk.kế.previous = chunk
		}
	}
}
func Mới(cỡ int) Pointer {
	if HoạtđộngBộnhớmanager == nil {
		return nil
	}
	return HoạtđộngBộnhớmanager.Cấp_phát_bộ_nhớ(uint32(cỡ))
}
func Xoá_2(tham_chiếu_địa_chỉ_2 Pointer) {
	if HoạtđộngBộnhớmanager != nil {
		HoạtđộngBộnhớmanager.Rảnh(tham_chiếu_địa_chỉ_2)
	}
}
