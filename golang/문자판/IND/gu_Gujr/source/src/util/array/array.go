package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vકદ int
}

func (self *TArray) Add(સરનામા_નિર્દેશક uintptr) {
	nodeArray[self.Vકદ] = સરનામા_નિર્દેશક
	self.Vકદ++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(સરનામા_નિર્દેશક uintptr) int {
	i := 0
	for ; i < self.Vકદ; i++ {
		if સરનામા_નિર્દેશક == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vકદ; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
