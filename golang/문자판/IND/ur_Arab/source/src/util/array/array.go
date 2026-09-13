package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vحجم int
}

func (self *TArray) Add(پتے_کا_حوالہ uintptr) {
	nodeArray[self.Vحجم] = پتے_کا_حوالہ
	self.Vحجم++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(پتے_کا_حوالہ uintptr) int {
	i := 0
	for ; i < self.Vحجم; i++ {
		if پتے_کا_حوالہ == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vحجم; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
