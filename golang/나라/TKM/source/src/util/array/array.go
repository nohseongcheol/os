package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Ululyk_2 int
}

func (self *TArray) Ekle(pointer uintptr) {
	nodearray[self.Ululyk_2] = pointer
	self.Ululyk_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(pointer uintptr) int {
	i := 0
	for ; i < self.Ululyk_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Çap() {
	console_2.MÇapxy("array:", 1, 1)

	for i := 0; i < self.Ululyk_2; i++ {
		console_2.MUnsignedinteger32Çap(uint32(nodearray[i]))
		console_2.MÇap(":")
	}
}
