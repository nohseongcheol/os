package memorymananger

import . "unsafe"

const M最大佇列大小 uint32 = 0x1FFFFFF
const Q佇列啟動address uint32 = 0x1000000

type T記憶體chunk struct {
	下一個		*T記憶體chunk
	previous	*T記憶體chunk
	allocated	bool

	大小	uint32
}

type T記憶體管理器 struct {
}

var first *T記憶體chunk
var A啟用記憶體管理器 *T記憶體管理器 = nil
var 記憶體chunk大小 uint32

func (self *T記憶體管理器) Init(啟動 uint32, 大小 uint32) {

	A啟用記憶體管理器 = self

	記憶體chunk大小 = uint32(Sizeof(T記憶體chunk{}))

	if 大小 < 記憶體chunk大小 {
		first = nil
	} else {
		first = (*T記憶體chunk)(Pointer(uintptr(Q佇列啟動address) + uintptr(啟動)))
		first.allocated = false
		first.previous = nil
		first.下一個 = nil
		first.大小 = 大小 - 記憶體chunk大小
	}
}
func (self *T記憶體管理器) D銷毀() {
	if A啟用記憶體管理器 == self {
		A啟用記憶體管理器 = nil
	}
}
func (self *T記憶體管理器) M配置記憶體(大小 uint32) Pointer {
	var 結果 *T記憶體chunk = nil

	var chunk *T記憶體chunk = first
	for ; chunk != nil && 結果 == nil; chunk = chunk.下一個 {
		if chunk.大小 > 大小 && !chunk.allocated {
			結果 = chunk
		}
	}

	if 結果 == nil {
		return nil
	}

	if 結果.大小 >= (大小 + 記憶體chunk大小 + 1) {

		var temporary *T記憶體chunk
		temporary = (*T記憶體chunk)(Pointer(uintptr(uint32(uintptr(Pointer(結果))) + 記憶體chunk大小 + 大小)))

		temporary.allocated = false
		temporary.大小 = 結果.大小 - 大小 - 記憶體chunk大小
		temporary.previous = 結果
		temporary.下一個 = 結果.下一個

		if temporary.下一個 != nil {
			temporary.下一個.previous = temporary
		}

		結果.大小 = 大小
		結果.下一個 = temporary
	}
	結果.allocated = true

	return Pointer(uintptr(Pointer(結果)) + uintptr(記憶體chunk大小))
}
func (self *T記憶體管理器) Alignedmalloc(大小 uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if 大小 == 0 || 大小 > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var 結果 *T記憶體chunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.下一個 {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(記憶體chunk大小))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.大小 && 大小 <= chunk.大小-diff {
			結果 = chunk
			break
		}
	}
	if 結果 == nil {
		return nil, 0
	}
	大小 += diff
	if 結果.大小-大小 >= 記憶體chunk大小+1 {
		temporary := (*T記憶體chunk)(Pointer(uintptr(Pointer(結果)) + uintptr(記憶體chunk大小) + uintptr(大小)))
		temporary.allocated = false
		temporary.大小 = 結果.大小 - 大小 - 記憶體chunk大小
		temporary.previous = 結果
		temporary.下一個 = 結果.下一個
		if temporary.下一個 != nil {
			temporary.下一個.previous = temporary
		}
		結果.大小 = 大小
		結果.下一個 = temporary
	}
	結果.allocated = true
	return Pointer(uintptr(Pointer(結果)) + uintptr(記憶體chunk大小) + uintptr(diff)), diff
}
func (self *T記憶體管理器) F剩餘(位址參照_2 Pointer) {
	var chunk *T記憶體chunk = (*T記憶體chunk)(Pointer(uintptr(位址參照_2) - uintptr(記憶體chunk大小)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.下一個 = chunk.下一個
		chunk.previous.大小 += chunk.大小 + 記憶體chunk大小
		if chunk.下一個 != nil {
			chunk.下一個.previous = chunk.previous
		}
	}

	if chunk.下一個 != nil && !chunk.下一個.allocated {
		chunk.大小 += chunk.下一個.大小 + 記憶體chunk大小
		chunk.下一個 = chunk.下一個.下一個
		if chunk.下一個 != nil {
			chunk.下一個.previous = chunk
		}
	}
}
func N新增(大小 int) Pointer {
	if A啟用記憶體管理器 == nil {
		return nil
	}
	return A啟用記憶體管理器.M配置記憶體(uint32(大小))
}
func D刪除(位址參照_2 Pointer) {
	if A啟用記憶體管理器 != nil {
		A啟用記憶體管理器.F剩餘(位址參照_2)
	}
}
