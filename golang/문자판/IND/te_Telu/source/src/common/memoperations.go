package common

type MemoryOper struct {
}

func (self *MemoryOper) MemSet(bufptr uintptr, value byte, పరిమాణం uint32) uintptr {
	return bufptr
}
func (self *MemoryOper) MemMove(dstptr uintptr, srcptr uintptr, పరిమాణం uint32) uintptr {
	return dstptr
}

func (self *MemoryOper) MemCpy(dstptr uintptr, srcptr uintptr, పరిమాణం uint32) uintptr {
	return dstptr
}
func (self *MemoryOper) MemCmp(dstptr uintptr, srcptr uintptr, పరిమాణం uint32) bool {
	return true
}
