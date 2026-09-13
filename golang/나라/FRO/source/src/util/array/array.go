package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Stødd_2 int
}

func (self *TArray) Add(pointer uintptr) {
	nodearray[self.Stødd_2] = pointer
	self.Stødd_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(pointer uintptr) int {
	i := 0
	for ; i < self.Stødd_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Print() {
	console_2.MPrintxy("array:", 1, 1)

	for i := 0; i < self.Stødd_2; i++ {
		console_2.MUnsignedinteger32print(uint32(nodearray[i]))
		console_2.MPrint(":")
	}
}
