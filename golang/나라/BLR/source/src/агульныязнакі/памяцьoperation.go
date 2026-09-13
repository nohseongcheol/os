package агульныязнакі

type Памяцьoper struct {
}

func (self *Памяцьoper) Memвызначана(bufferПаказальнік uintptr, значэнне byte, памер uint32) uintptr {
	return bufferПаказальнік
}
func (self *Памяцьoper) MemПеранесці(destinationПаказальнік_2 uintptr, srcptr uintptr, памер uint32) uintptr {
	return destinationПаказальнік_2
}

func (self *Памяцьoper) MemСкапіяваць(destinationПаказальнік_2 uintptr, srcptr uintptr, памер uint32) uintptr {
	return destinationПаказальнік_2
}
func (self *Памяцьoper) Memcmp(destinationПаказальнік_2 uintptr, srcptr uintptr, памер uint32) bool {
	return true
}
