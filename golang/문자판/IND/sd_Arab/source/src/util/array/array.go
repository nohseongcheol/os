package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Size int
}

func (self *TArray) Add(pointer uintptr) {
	nodeArray[self.Size] = pointer
	self.Size++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(pointer uintptr) int {
	i := 0
	for ; i < self.Size; i++ {
		if pointer == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Size; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
