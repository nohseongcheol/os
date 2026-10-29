/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Sཚད_2 int
}

func (self *TArray) Add(pointer uintptr) {
	nodearray[self.Sཚད_2] = pointer
	self.Sཚད_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(pointer uintptr) int {
	i := 0
	for ; i < self.Sཚད_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Print() {
	console_2.MPrintxy("array:", 1, 1)

	for i := 0; i < self.Sཚད_2; i++ {
		console_2.MUnsignedinteger32print(uint32(nodearray[i]))
		console_2.MPrint(":")
	}
}
