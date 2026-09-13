package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Size_2 int
}

func (self *TArray) Add(address_reference uintptr) {
	nodearray[self.Size_2] = address_reference
	self.Size_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(address_reference uintptr) int {
	i := 0
	for ; i < self.Size_2; i++ {
		if address_reference == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Print() {
	console_2.MPrintxy("array:", 1, 1)

	for i := 0; i < self.Size_2; i++ {
		console_2.MUnsignedinteger32print(uint32(nodearray[i]))
		console_2.MPrint(":")
	}
}
