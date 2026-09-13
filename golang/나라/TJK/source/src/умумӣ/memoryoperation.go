package умумӣ

type Memoryoper struct {
}

func (self *Memoryoper) Memset(bufferpointer uintptr, value byte, size uint32) uintptr {
	return bufferpointer
}
func (self *Memoryoper) MemТаҳвил(destinationpointer_2 uintptr, srcptr uintptr, size uint32) uintptr {
	return destinationpointer_2
}

func (self *Memoryoper) MemНусхабардоштан(destinationpointer_2 uintptr, srcptr uintptr, size uint32) uintptr {
	return destinationpointer_2
}
func (self *Memoryoper) Memcmp(destinationpointer_2 uintptr, srcptr uintptr, size uint32) bool {
	return true
}
