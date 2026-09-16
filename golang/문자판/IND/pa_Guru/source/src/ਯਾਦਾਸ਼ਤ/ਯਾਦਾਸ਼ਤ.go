/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MAX_QUEUE_SIZE uint32 = 0x1FFFFFF
const QUEUE_START_ADDR uint32 = 0x1000000

type TMemoryChunk struct {
	next		*TMemoryChunk
	prev	*TMemoryChunk
	allocated	bool

	ਆਕਾਰ	uint32
}

type TMemoryManager struct {
}

var first *TMemoryChunk
var ActiveMemoryManager *TMemoryManager = nil
var memoryChunkSize uint32

func (self *TMemoryManager) Vਆਰੰਭ_ਕਰਨਾ(start uint32, ਆਕਾਰ uint32) {

	ActiveMemoryManager = self

	memoryChunkSize = uint32(Sizeof(TMemoryChunk{}))

	if ਆਕਾਰ < memoryChunkSize {
		first = nil
	} else {
		first = (*TMemoryChunk)(Pointer(uintptr(QUEUE_START_ADDR) + uintptr(start)))
		first.allocated = false
		first.prev = nil
		first.next = nil
		first.ਆਕਾਰ = ਆਕਾਰ - memoryChunkSize
	}
}
func (self *TMemoryManager) Destroy() {
	if ActiveMemoryManager == self {
		ActiveMemoryManager = nil
	}
}
func (self *TMemoryManager) Malloc(ਆਕਾਰ uint32) Pointer {
	var result *TMemoryChunk = nil

	var chunk *TMemoryChunk = first
	for ; chunk != nil && result == nil; chunk = chunk.next {
		if chunk.ਆਕਾਰ > ਆਕਾਰ && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ਆਕਾਰ >= (ਆਕਾਰ + memoryChunkSize + 1) {

		var temp *TMemoryChunk
		temp = (*TMemoryChunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memoryChunkSize + ਆਕਾਰ)))

		temp.allocated = false
		temp.ਆਕਾਰ = result.ਆਕਾਰ - ਆਕਾਰ - memoryChunkSize
		temp.prev = result
		temp.next = result.next

		if temp.next != nil {
			temp.next.prev = temp
		}

		result.ਆਕਾਰ = ਆਕਾਰ
		result.next = temp
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize))
}
func (self *TMemoryManager) AlignedMalloc(ਆਕਾਰ uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ਆਕਾਰ == 0 || ਆਕਾਰ > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemoryChunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.next {
		if chunk.allocated {
			continue
		}
		addr := uint32(uintptr(Pointer(chunk)) + uintptr(memoryChunkSize))
		diff = (0x1000 - (addr & 0xFFF)) & 0xFFF
		if addr+diff < addr {
			continue
		}
		if diff <= chunk.ਆਕਾਰ && ਆਕਾਰ <= chunk.ਆਕਾਰ-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ਆਕਾਰ += diff
	if result.ਆਕਾਰ-ਆਕਾਰ >= memoryChunkSize+1 {
		temp := (*TMemoryChunk)(Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize) + uintptr(ਆਕਾਰ)))
		temp.allocated = false
		temp.ਆਕਾਰ = result.ਆਕਾਰ - ਆਕਾਰ - memoryChunkSize
		temp.prev = result
		temp.next = result.next
		if temp.next != nil {
			temp.next.prev = temp
		}
		result.ਆਕਾਰ = ਆਕਾਰ
		result.next = temp
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize) + uintptr(diff)), diff
}
func (self *TMemoryManager) Free(ਪਤੇ_ਦਾ_ਹਵਾਲਾ_2 Pointer) {
	var chunk *TMemoryChunk = (*TMemoryChunk)(Pointer(uintptr(ਪਤੇ_ਦਾ_ਹਵਾਲਾ_2) - uintptr(memoryChunkSize)))
	chunk.allocated = false

	if chunk.prev != nil && !chunk.prev.allocated {
		chunk.prev.next = chunk.next
		chunk.prev.ਆਕਾਰ += chunk.ਆਕਾਰ + memoryChunkSize
		if chunk.next != nil {
			chunk.next.prev = chunk.prev
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.ਆਕਾਰ += chunk.next.ਆਕਾਰ + memoryChunkSize
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.prev = chunk
		}
	}
}
func New(ਆਕਾਰ int) Pointer {
	if ActiveMemoryManager == nil {
		return nil
	}
	return ActiveMemoryManager.Malloc(uint32(ਆਕਾਰ))
}
func Delete(ਪਤੇ_ਦਾ_ਹਵਾਲਾ_2 Pointer) {
	if ActiveMemoryManager != nil {
		ActiveMemoryManager.Free(ਪਤੇ_ਦਾ_ਹਵਾਲਾ_2)
	}
}
