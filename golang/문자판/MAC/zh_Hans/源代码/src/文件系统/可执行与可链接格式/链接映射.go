package 可执行与可链接格式

import . "unsafe"
import . "控制台"

import mem "内存管理器"

type L链接 struct {
	D动态		uintptr
	Previous	*L链接
	N下一个		*L链接
}
type L链接映射 struct {
	First	*L链接
	L最近	*L链接

	S大小_2	int

	mem	*mem.T内存管理器
}

func (self *L链接映射) Init(mem *mem.T内存管理器) {
	self.mem = mem
}
func (self *L链接映射) Clone() L链接映射 {
	var 链接映射 L链接映射

	链接映射.Init(self.mem)

	L链接 := self.First

	for ; L链接 != nil; L链接 = L链接.N下一个 {
		链接映射.M追加到表尾(L链接.D动态)
	}
	return 链接映射
}
func (self *L链接映射) M添加到表头(D动态 uintptr) {
	新建链接 := (*L链接)(self.mem.M分配内存(uint32(Sizeof(L链接{}))))
	新建链接.D动态 = D动态
	新建链接.N下一个 = self.First
	self.First = 新建链接
	self.S大小_2++

	if self.First.N下一个 == nil {
		self.L最近 = self.First
	}
}
func (self *L链接映射) M追加到表尾(D动态 uintptr) {
	if D动态 == 0 {
		return
	}

	if self.S大小_2 == 0 {
		self.M添加到表头(D动态)
	} else {
		新建链接 := (*L链接)(self.mem.M分配内存(uint32(Sizeof(L链接{}))))
		新建链接.D动态 = D动态
		新建链接.N下一个 = nil
		self.L最近.N下一个 = 新建链接
		self.L最近 = 新建链接
		self.S大小_2++
	}
}
func (self *L链接映射) P打印(x uint16, y uint16) {
	L链接 := self.First
	控制台_2 := T控制台{}
	控制台_2.M打印xy("linkmap : ", x, y)
	for ; L链接 != nil; L链接 = L链接.N下一个 {
		控制台_2.MUnsignedinteger32打印(uint32(L链接.D动态))
		控制台_2.M打印("+")

	}
}
