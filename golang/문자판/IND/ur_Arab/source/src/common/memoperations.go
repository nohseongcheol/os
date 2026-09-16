/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package common

type MemoryOper struct {
}

func (self *MemoryOper) MemSet(bufptr uintptr, value byte, حجم uint32) uintptr {
	return bufptr
}
func (self *MemoryOper) MemMove(dstptr uintptr, srcptr uintptr, حجم uint32) uintptr {
	return dstptr
}

func (self *MemoryOper) MemCpy(dstptr uintptr, srcptr uintptr, حجم uint32) uintptr {
	return dstptr
}
func (self *MemoryOper) MemCmp(dstptr uintptr, srcptr uintptr, حجم uint32) bool {
	return true
}
