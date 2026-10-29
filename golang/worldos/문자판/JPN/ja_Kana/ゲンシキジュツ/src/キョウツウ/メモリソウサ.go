/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
