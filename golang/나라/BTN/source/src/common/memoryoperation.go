package common

type Memoryoper struct {
}

func (self *Memoryoper) Memset(bufferpointer uintptr, value byte, ཚད uint32) uintptr {
	return bufferpointer
}
func (self *Memoryoper) Memmove(destinationpointer_2 uintptr, srcptr uintptr, ཚད uint32) uintptr {
	return destinationpointer_2
}

func (self *Memoryoper) Memcopy(destinationpointer_2 uintptr, srcptr uintptr, ཚད uint32) uintptr {
	return destinationpointer_2
}
func (self *Memoryoper) Memcmp(destinationpointer_2 uintptr, srcptr uintptr, ཚད uint32) bool {
	return true
}
