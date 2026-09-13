package 通用

type M記憶體oper struct {
}

func (self *M記憶體oper) Mem設定(buffer指標 uintptr, 數值 byte, 大小 uint32) uintptr {
	return buffer指標
}
func (self *M記憶體oper) Mem移動(目的地指標_2 uintptr, srcptr uintptr, 大小 uint32) uintptr {
	return 目的地指標_2
}

func (self *M記憶體oper) Mem複製(目的地指標_2 uintptr, srcptr uintptr, 大小 uint32) uintptr {
	return 目的地指標_2
}
func (self *M記憶體oper) Memcmp(目的地指標_2 uintptr, srcptr uintptr, 大小 uint32) bool {
	return true
}
