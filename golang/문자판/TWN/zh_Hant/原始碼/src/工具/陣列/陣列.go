package 陣列

import . "unsafe"
import . "控制台"

var 節點陣列 [100]uintptr

type T陣列 struct {
	S大小_2 int
}

func (self *T陣列) A加入(位址參照 uintptr) {
	節點陣列[self.S大小_2] = 位址參照
	self.S大小_2++
}
func (self *T陣列) Getat(索引 int) Pointer {
	return Pointer(節點陣列[索引])
}
func (self *T陣列) I索引of(位址參照 uintptr) int {
	i := 0
	for ; i < self.S大小_2; i++ {
		if 位址參照 == 節點陣列[i] {
			return i
		}
	}
	return -1
}

var 控制台_2 = T控制台{}

func (self *T陣列) P列印() {
	控制台_2.M列印xy("array:", 1, 1)

	for i := 0; i < self.S大小_2; i++ {
		控制台_2.MUnsignedinteger32列印(uint32(節點陣列[i]))
		控制台_2.M列印(":")
	}
}
