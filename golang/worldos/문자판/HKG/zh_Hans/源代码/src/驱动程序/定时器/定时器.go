/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 定时器

import . "unsafe"

import . "中断"
import . "控制台"

type I定时器事件handler interface {
	O时tick()
}

var i定时器事件handler I定时器事件handler

type T默认定时器事件handler struct {
}

func (self *T默认定时器事件handler) O时tick() {
}

type T定时器驱动程序 struct {
	T中断handler
}

var 中断handler func(*T定时器驱动程序, uint32) uint32

func (self *T定时器驱动程序) Init(管理器 *T中断管理器, 键盘事件handler I定时器事件handler) {
	i定时器事件handler = &T默认定时器事件handler{}
	if 键盘事件handler != nil {
		i定时器事件handler = 键盘事件handler
	}

	中断handler = (*T定时器驱动程序).H控制器中断
	var address uintptr
	address = uintptr(Pointer(&中断handler))

	self.T中断handler.Init(0x20, uintptr(Pointer(管理器)), address)

}

var tick计数 uint32 = 0

func (self *T定时器驱动程序) H控制器中断(esp uint32) uint32 {
	控制台_2 := T控制台{}
	控制台_2.MUnsignedinteger32打印xy(tick计数, 3, 1)
	tick计数++

	return esp
}
