package common

type MemoryOper struct {
}

func (self *MemoryOper) MemSet(bufptr uintptr, value byte, ಗಾತ್ರ uint32) uintptr {
	return bufptr
}
func (self *MemoryOper) MemMove(dstptr uintptr, srcptr uintptr, ಗಾತ್ರ uint32) uintptr {
	return dstptr
}

func (self *MemoryOper) MemCpy(dstptr uintptr, srcptr uintptr, ಗಾತ್ರ uint32) uintptr {
	return dstptr
}
func (self *MemoryOper) MemCmp(dstptr uintptr, srcptr uintptr, ಗಾತ್ರ uint32) bool {
	return true
}
