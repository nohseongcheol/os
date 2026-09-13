package 配列

import . "unsafe"
import . "コンソール"

var ノード配列 [100]uintptr

type T配列 struct {
	Sサイズ_2 int
}

func (self *T配列) A追加(番地参照 uintptr) {
	ノード配列[self.Sサイズ_2] = 番地参照
	self.Sサイズ_2++
}
func (self *T配列) Getat(目次 int) Pointer {
	return Pointer(ノード配列[目次])
}
func (self *T配列) I目次of(番地参照 uintptr) int {
	i := 0
	for ; i < self.Sサイズ_2; i++ {
		if 番地参照 == ノード配列[i] {
			return i
		}
	}
	return -1
}

var コンソール_2 = Tコンソール{}

func (self *T配列) P印刷() {
	コンソール_2.M印刷xy("array:", 1, 1)

	for i := 0; i < self.Sサイズ_2; i++ {
		コンソール_2.MUnsignedinteger32印刷(uint32(ノード配列[i]))
		コンソール_2.M印刷(":")
	}
}
