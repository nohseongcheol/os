/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 驱动程序

type I驱动程序 interface {
	A激活()
	R重置() int
	D禁用()
}

type T驱动程序管理器 struct {
}

var i驱动程序 [256]I驱动程序
var 数字驱动程序 int

func (self *T驱动程序管理器) Init() {
	数字驱动程序 = 0
}

func (self *T驱动程序管理器) A添加驱动程序(驱动程序_2 I驱动程序) {
	i驱动程序[数字驱动程序] = 驱动程序_2
	数字驱动程序++
}
func (self *T驱动程序管理器) A激活全部() {
	for i := 0; i < 数字驱动程序; i++ {
		i驱动程序[i].A激活()
	}
}
