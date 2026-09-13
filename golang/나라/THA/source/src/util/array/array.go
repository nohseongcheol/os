package array

import . "unsafe"
import . "console"

var โหนดarray [100]uintptr

type TArray struct {
	Sขนาด_2 int
}

func (self *TArray) Add(pointer uintptr) {
	โหนดarray[self.Sขนาด_2] = pointer
	self.Sขนาด_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(โหนดarray[index])
}
func (self *TArray) Indexจาก(pointer uintptr) int {
	i := 0
	for ; i < self.Sขนาด_2; i++ {
		if pointer == โหนดarray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Print() {
	console_2.MPrintxy("array:", 1, 1)

	for i := 0; i < self.Sขนาด_2; i++ {
		console_2.MUnsignedinteger32print(uint32(โหนดarray[i]))
		console_2.MPrint(":")
	}
}
