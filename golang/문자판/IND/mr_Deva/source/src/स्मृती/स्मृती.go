package memorymananger

import . "unsafe"

const MAX_QUEUE_SIZE uint32 = 0x1FFFFFF
const QUEUE_START_ADDR uint32 = 0x1000000

type TMemoryChunk struct {
	next		*TMemoryChunk
	prev	*TMemoryChunk
	allocated	bool

	आकार	uint32
}

type TMemoryManager struct {
}

var first *TMemoryChunk
var ActiveMemoryManager *TMemoryManager = nil
var memoryChunkSize uint32

func (self *TMemoryManager) Vआरंभ_करणे(start uint32, आकार uint32) {

	ActiveMemoryManager = self

	memoryChunkSize = uint32(Sizeof(TMemoryChunk{}))

	if आकार < memoryChunkSize {
		first = nil
	} else {
		first = (*TMemoryChunk)(Pointer(uintptr(QUEUE_START_ADDR) + uintptr(start)))
		first.allocated = false
		first.prev = nil
		first.next = nil
		first.आकार = आकार - memoryChunkSize
	}
}
func (self *TMemoryManager) Destroy() {
	if ActiveMemoryManager == self {
		ActiveMemoryManager = nil
	}
}
func (self *TMemoryManager) Vस्मृती_वाटप_करणे(आकार uint32) Pointer {
	var result *TMemoryChunk = nil

	var chunk *TMemoryChunk = first
	for ; chunk != nil && result == nil; chunk = chunk.next {
		if chunk.आकार > आकार && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.आकार >= (आकार + memoryChunkSize + 1) {

		var temp *TMemoryChunk
		temp = (*TMemoryChunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memoryChunkSize + आकार)))

		temp.allocated = false
		temp.आकार = result.आकार - आकार - memoryChunkSize
		temp.prev = result
		temp.next = result.next

		if temp.next != nil {
			temp.next.prev = temp
		}

		result.आकार = आकार
		result.next = temp
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize))
}
func (self *TMemoryManager) AlignedMalloc(आकार uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if आकार == 0 || आकार > ^uint32(0)-0x1000 {
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
		if diff <= chunk.आकार && आकार <= chunk.आकार-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	आकार += diff
	if result.आकार-आकार >= memoryChunkSize+1 {
		temp := (*TMemoryChunk)(Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize) + uintptr(आकार)))
		temp.allocated = false
		temp.आकार = result.आकार - आकार - memoryChunkSize
		temp.prev = result
		temp.next = result.next
		if temp.next != nil {
			temp.next.prev = temp
		}
		result.आकार = आकार
		result.next = temp
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize) + uintptr(diff)), diff
}
func (self *TMemoryManager) Vस्मृती_मुक्त_करणे(पत्ता_संदर्भ_2 Pointer) {
	var chunk *TMemoryChunk = (*TMemoryChunk)(Pointer(uintptr(पत्ता_संदर्भ_2) - uintptr(memoryChunkSize)))
	chunk.allocated = false

	if chunk.prev != nil && !chunk.prev.allocated {
		chunk.prev.next = chunk.next
		chunk.prev.आकार += chunk.आकार + memoryChunkSize
		if chunk.next != nil {
			chunk.next.prev = chunk.prev
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.आकार += chunk.next.आकार + memoryChunkSize
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.prev = chunk
		}
	}
}
func New(आकार int) Pointer {
	if ActiveMemoryManager == nil {
		return nil
	}
	return ActiveMemoryManager.Vस्मृती_वाटप_करणे(uint32(आकार))
}
func Delete(पत्ता_संदर्भ_2 Pointer) {
	if ActiveMemoryManager != nil {
		ActiveMemoryManager.Vस्मृती_मुक्त_करणे(पत्ता_संदर्भ_2)
	}
}
