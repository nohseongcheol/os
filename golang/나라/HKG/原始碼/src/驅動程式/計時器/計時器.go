package 計時器

import . "unsafe"

import . "中斷"
import . "控制台"

type I計時器事件handler interface {
	O時tick()
}

var i計時器事件handler I計時器事件handler

type T預設計時器事件handler struct {
}

func (self *T預設計時器事件handler) O時tick() {
}

type T計時器驅動程式 struct {
	T中斷handler
}

var 中斷handler func(*T計時器驅動程式, uint32) uint32

func (self *T計時器驅動程式) Init(管理器 *T中斷管理器, 鍵盤事件handler I計時器事件handler) {
	i計時器事件handler = &T預設計時器事件handler{}
	if 鍵盤事件handler != nil {
		i計時器事件handler = 鍵盤事件handler
	}

	中斷handler = (*T計時器驅動程式).H控制把中斷
	var address uintptr
	address = uintptr(Pointer(&中斷handler))

	self.T中斷handler.Init(0x20, uintptr(Pointer(管理器)), address)

}

var tick計數 uint32 = 0

func (self *T計時器驅動程式) H控制把中斷(esp uint32) uint32 {
	控制台_2 := T控制台{}
	控制台_2.MUnsignedinteger32列印xy(tick計數, 3, 1)
	tick計數++

	return esp
}
