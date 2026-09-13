package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Böyüklük_2 int
}

func (self *TArray) ƏlavəEt(pointer uintptr) {
	nodearray[self.Böyüklük_2] = pointer
	self.Böyüklük_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(pointer uintptr) int {
	i := 0
	for ; i < self.Böyüklük_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) ÇapEt() {
	console_2.MÇapEtxy("array:", 1, 1)

	for i := 0; i < self.Böyüklük_2; i++ {
		console_2.MUnsignedinteger32ÇapEt(uint32(nodearray[i]))
		console_2.MÇapEt(":")
	}
}
