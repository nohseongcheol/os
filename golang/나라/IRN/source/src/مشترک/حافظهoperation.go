package مشترک

type Mحافظهoper struct {
}

func (خود *Mحافظهoper) Memset(bufferpointer uintptr, مقدار byte, اندازه uint32) uintptr {
	return bufferpointer
}
func (خود *Mحافظهoper) Memانتقال(مقصدpointer_2 uintptr, srcptr uintptr, اندازه uint32) uintptr {
	return مقصدpointer_2
}

func (خود *Mحافظهoper) Memکپی(مقصدpointer_2 uintptr, srcptr uintptr, اندازه uint32) uintptr {
	return مقصدpointer_2
}
func (خود *Mحافظهoper) Memcmp(مقصدpointer_2 uintptr, srcptr uintptr, اندازه uint32) bool {
	return true
}
