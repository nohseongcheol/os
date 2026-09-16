/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
