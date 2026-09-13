package キョウツウ

type Mメモリoper struct {
}

func (self *Mメモリoper) Memアリ(bufferポインタ uintptr, アタイ byte, サイズ uint32) uintptr {
	return bufferポインタ
}
func (self *Mメモリoper) Memイドウ(テンソウサキポインタ_2 uintptr, srcptr uintptr, サイズ uint32) uintptr {
	return テンソウサキポインタ_2
}

func (self *Mメモリoper) Memフクセイ(テンソウサキポインタ_2 uintptr, srcptr uintptr, サイズ uint32) uintptr {
	return テンソウサキポインタ_2
}
func (self *Mメモリoper) Memcmp(テンソウサキポインタ_2 uintptr, srcptr uintptr, サイズ uint32) bool {
	return true
}
