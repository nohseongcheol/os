/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
