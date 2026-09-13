package 共通

type Mメモリoper struct {
}

func (self *Mメモリoper) Memあり(bufferポインタ uintptr, 値 byte, サイズ uint32) uintptr {
	return bufferポインタ
}
func (self *Mメモリoper) Mem移動(転送先ポインタ_2 uintptr, srcptr uintptr, サイズ uint32) uintptr {
	return 転送先ポインタ_2
}

func (self *Mメモリoper) Mem複製(転送先ポインタ_2 uintptr, srcptr uintptr, サイズ uint32) uintptr {
	return 転送先ポインタ_2
}
func (self *Mメモリoper) Memcmp(転送先ポインタ_2 uintptr, srcptr uintptr, サイズ uint32) bool {
	return true
}
