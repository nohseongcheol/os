package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vআকার int
}

func (self *TArray) Add(ঠিকানা_নির্দেশক uintptr) {
	nodeArray[self.Vআকার] = ঠিকানা_নির্দেশক
	self.Vআকার++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(ঠিকানা_নির্দেশক uintptr) int {
	i := 0
	for ; i < self.Vআকার; i++ {
		if ঠিকানা_নির্দেশক == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vআকার; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
