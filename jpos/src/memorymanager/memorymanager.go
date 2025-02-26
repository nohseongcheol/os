package memorymananger

import . "unsafe"

const MAX_QUEUE_SIZE uint32 = 10*1024*1024
var queue [MAX_QUEUE_SIZE]byte

type TMemoryChunk struct {
	next *TMemoryChunk
	prev *TMemoryChunk
	allocated bool

	size uint32
}

type TMemoryManager struct {
}
var first *TMemoryChunk
var ActiveMemoryManager *TMemoryManager = nil
var memoryChunkSize uint32
func (self *TMemoryManager) Init(start uint32, size uint32) {
	//ActiveMemoryManager = (*TMemoryManager)(Pointer(&queue))
	ActiveMemoryManager = self

	memoryChunkSize = uint32(Sizeof(TMemoryChunk{}))

	if size < memoryChunkSize {
		first = nil
	}else {
		//first = (*TMemoryChunk)(Pointer(uintptr(Pointer(&queue))+uintptr(start)))
		first = (*TMemoryChunk)(Pointer(uintptr(Pointer(&queue)) + uintptr(start)))
		//first = (*TMemoryChunk)(Pointer(&queue))
		first.allocated = false
		first.prev = nil
		first.next = nil
		first.size = size - memoryChunkSize
	}
	
	//first = (*TMemoryChunk)(Pointer(uintptr(Pointer(&queue))+uintptr(start)))
	first = (*TMemoryChunk)(Pointer(uintptr(Pointer(&queue)) + uintptr(start)))
	//first = (*TMemoryChunk)(Pointer(&queue))
}
func (self *TMemoryManager) Destroy() {
	if ActiveMemoryManager == self {
		ActiveMemoryManager = nil
	}
}
func (self *TMemoryManager) Malloc(size uint32) Pointer{
	var result *TMemoryChunk = nil

	var chunk *TMemoryChunk = first
	for ; chunk!=nil && result==nil; chunk=chunk.next {
		if chunk.size > size && !chunk.allocated {
			result = chunk
		}
	}
	
	if result == nil {
		return nil
	}

	if result.size >= (size+memoryChunkSize+1) {
		var temp *TMemoryChunk
		temp = (*TMemoryChunk)(Pointer(uintptr(uint32(uintptr(Pointer(result)))+memoryChunkSize+size)))
		
		temp.allocated = false
		temp.size = result.size - size - memoryChunkSize
		temp.prev = result
		temp.next = result.next

		if temp.next != nil {
			temp.next.prev = temp
		}

		result.size = size
		result.next = temp
	}
	result.allocated = true
		
	return Pointer(uintptr(Pointer(result)) + uintptr(memoryChunkSize))
}
func (self *TMemoryManager) Free(ptr Pointer) {
	var chunk *TMemoryChunk = (*TMemoryChunk)(Pointer(uintptr(ptr) - uintptr(memoryChunkSize)))
	chunk.allocated = false
	
	if chunk.prev != nil && !chunk.prev.allocated {
		chunk.prev.next = chunk.next
		chunk.prev.size += chunk.size + memoryChunkSize
		if chunk.next != nil {
			chunk.next.prev = chunk.prev
		}
	}

	if chunk.next != nil && !chunk.next.allocated {
		chunk.size += chunk.next.size + memoryChunkSize
		chunk.next = chunk.next.next
		if chunk.next != nil {
			chunk.next.prev = chunk
		}
	}
}
func New(size int) Pointer{
	if ActiveMemoryManager == nil {
		return nil
	}
	return ActiveMemoryManager.Malloc(uint32(size))
}
func Delete(ptr Pointer) {
	if ActiveMemoryManager == nil {
		ActiveMemoryManager.Free(ptr)
	}
}
