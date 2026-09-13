package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Veličina_2 int
}

func (self *TArray) Dodaj(pointer uintptr) {
	nodearray[self.Veličina_2] = pointer
	self.Veličina_2++
}
func (self *TArray) Getat(indeks int) Pointer {
	return Pointer(nodearray[indeks])
}
func (self *TArray) Indeksof(pointer uintptr) int {
	i := 0
	for ; i < self.Veličina_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Štampaj() {
	console_2.MŠtampajxy("array:", 1, 1)

	for i := 0; i < self.Veličina_2; i++ {
		console_2.MUnsignedinteger32Štampaj(uint32(nodearray[i]))
		console_2.MŠtampaj(":")
	}
}
