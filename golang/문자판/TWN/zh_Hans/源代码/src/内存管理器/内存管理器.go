/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const M最大值队列大小 uint32 = 0x1FFFFFF
const Q队列开始address uint32 = 0x1000000

type T内存chunk struct {
	下一个		*T内存chunk
	previous	*T内存chunk
	allocated	bool

	大小	uint32
}

type T内存管理器 struct {
}

var first *T内存chunk
var A活跃内存管理器 *T内存管理器 = nil
var 内存chunk大小 uint32

func (self *T内存管理器) Init(开始 uint32, 大小 uint32) {

	A活跃内存管理器 = self

	内存chunk大小 = uint32(Sizeof(T内存chunk{}))

	if 大小 < 内存chunk大小 {
		first = nil
	} else {
		first = (*T内存chunk)(Pointer(uintptr(Q队列开始address) + uintptr(开始)))
		first.allocated = false
		first.previous = nil
		first.下一个 = nil
		first.大小 = 大小 - 内存chunk大小
	}
}
func (self *T内存管理器) D摧毁() {
	if A活跃内存管理器 == self {
		A活跃内存管理器 = nil
	}
}
func (self *T内存管理器) M分配内存(大小 uint32) Pointer {
	var 结果 *T内存chunk = nil

	var chunk *T内存chunk = first
	for ; chunk != nil && 结果 == nil; chunk = chunk.下一个 {
		if chunk.大小 > 大小 && !chunk.allocated {
			结果 = chunk
		}
	}

	if 结果 == nil {
		return nil
	}

	if 结果.大小 >= (大小 + 内存chunk大小 + 1) {

		var temporary *T内存chunk
		temporary = (*T内存chunk)(Pointer(uintptr(uint32(uintptr(Pointer(结果))) + 内存chunk大小 + 大小)))

		temporary.allocated = false
		temporary.大小 = 结果.大小 - 大小 - 内存chunk大小
		temporary.previous = 结果
		temporary.下一个 = 结果.下一个

		if temporary.下一个 != nil {
			temporary.下一个.previous = temporary
		}

		结果.大小 = 大小
		结果.下一个 = temporary
	}
	结果.allocated = true

	return Pointer(uintptr(Pointer(结果)) + uintptr(内存chunk大小))
}
func (self *T内存管理器) Alignedmalloc(大小 uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if 大小 == 0 || 大小 > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var 结果 *T内存chunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.下一个 {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(内存chunk大小))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.大小 && 大小 <= chunk.大小-diff {
			结果 = chunk
			break
		}
	}
	if 结果 == nil {
		return nil, 0
	}
	大小 += diff
	if 结果.大小-大小 >= 内存chunk大小+1 {
		temporary := (*T内存chunk)(Pointer(uintptr(Pointer(结果)) + uintptr(内存chunk大小) + uintptr(大小)))
		temporary.allocated = false
		temporary.大小 = 结果.大小 - 大小 - 内存chunk大小
		temporary.previous = 结果
		temporary.下一个 = 结果.下一个
		if temporary.下一个 != nil {
			temporary.下一个.previous = temporary
		}
		结果.大小 = 大小
		结果.下一个 = temporary
	}
	结果.allocated = true
	return Pointer(uintptr(Pointer(结果)) + uintptr(内存chunk大小) + uintptr(diff)), diff
}
func (self *T内存管理器) F空闲(地址引用_2 Pointer) {
	var chunk *T内存chunk = (*T内存chunk)(Pointer(uintptr(地址引用_2) - uintptr(内存chunk大小)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.下一个 = chunk.下一个
		chunk.previous.大小 += chunk.大小 + 内存chunk大小
		if chunk.下一个 != nil {
			chunk.下一个.previous = chunk.previous
		}
	}

	if chunk.下一个 != nil && !chunk.下一个.allocated {
		chunk.大小 += chunk.下一个.大小 + 内存chunk大小
		chunk.下一个 = chunk.下一个.下一个
		if chunk.下一个 != nil {
			chunk.下一个.previous = chunk
		}
	}
}
func N新建(大小 int) Pointer {
	if A活跃内存管理器 == nil {
		return nil
	}
	return A活跃内存管理器.M分配内存(uint32(大小))
}
func D删除(地址引用_2 Pointer) {
	if A活跃内存管理器 != nil {
		A活跃内存管理器.F空闲(地址引用_2)
	}
}
