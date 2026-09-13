package 数组

import . "unsafe"
import . "控制台"

var 节点数组 [100]uintptr

type T数组 struct {
	S大小_2 int
}

func (self *T数组) A添加(地址引用 uintptr) {
	节点数组[self.S大小_2] = 地址引用
	self.S大小_2++
}
func (self *T数组) Getat(索引 int) Pointer {
	return Pointer(节点数组[索引])
}
func (self *T数组) I索引of(地址引用 uintptr) int {
	i := 0
	for ; i < self.S大小_2; i++ {
		if 地址引用 == 节点数组[i] {
			return i
		}
	}
	return -1
}

var 控制台_2 = T控制台{}

func (self *T数组) P打印() {
	控制台_2.M打印xy("array:", 1, 1)

	for i := 0; i < self.S大小_2; i++ {
		控制台_2.MUnsignedinteger32打印(uint32(节点数组[i]))
		控制台_2.M打印(":")
	}
}
