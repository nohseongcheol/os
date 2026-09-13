package common

type Memoryoper struct {
}

func (self *Memoryoper) Memกำหนด(bufferpointer uintptr, value byte, ขนาด uint32) uintptr {
	return bufferpointer
}
func (self *Memoryoper) Memmove(ปลายทางpointer_2 uintptr, srcptr uintptr, ขนาด uint32) uintptr {
	return ปลายทางpointer_2
}

func (self *Memoryoper) Memcopy(ปลายทางpointer_2 uintptr, srcptr uintptr, ขนาด uint32) uintptr {
	return ปลายทางpointer_2
}
func (self *Memoryoper) Memcmp(ปลายทางpointer_2 uintptr, srcptr uintptr, ขนาด uint32) bool {
	return true
}
