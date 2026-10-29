/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 通用

type M内存oper struct {
}

func (self *M内存oper) Mem集合(buffer指针 uintptr, 值 byte, 大小 uint32) uintptr {
	return buffer指针
}
func (self *M内存oper) Mem移动(目的指针_2 uintptr, srcptr uintptr, 大小 uint32) uintptr {
	return 目的指针_2
}

func (self *M内存oper) Mem复制(目的指针_2 uintptr, srcptr uintptr, 大小 uint32) uintptr {
	return 目的指针_2
}
func (self *M内存oper) Mem位取反(目的指针_2 uintptr, srcptr uintptr, 大小 uint32) bool {
	return true
}
