package chung

type Bộnhớoper struct {
}

func (mình *Bộnhớoper) MemĐặt(bufferContrỏ uintptr, giátrị byte, cỡ uint32) uintptr {
	return bufferContrỏ
}
func (mình *Bộnhớoper) MemDichuyển(destinationContrỏ_2 uintptr, srcptr uintptr, cỡ uint32) uintptr {
	return destinationContrỏ_2
}

func (mình *Bộnhớoper) MemSaochép(destinationContrỏ_2 uintptr, srcptr uintptr, cỡ uint32) uintptr {
	return destinationContrỏ_2
}
func (mình *Bộnhớoper) Memcmp(destinationContrỏ_2 uintptr, srcptr uintptr, cỡ uint32) bool {
	return true
}
