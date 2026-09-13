package vector

import . "unsafe"
import . "console"

var nodeVector [100]uintptr

type TVector struct {
	Mărime_2 int
}

func (sine *TVector) Adaugă(indicator uintptr) {
	nodeVector[sine.Mărime_2] = indicator
	sine.Mărime_2++
}
func (sine *TVector) Getat(index int) Pointer {
	return Pointer(nodeVector[index])
}
func (sine *TVector) Indexdin(indicator uintptr) int {
	i := 0
	for ; i < sine.Mărime_2; i++ {
		if indicator == nodeVector[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (sine *TVector) Tipărește() {
	console_2.MTipăreștexy("array:", 1, 1)

	for i := 0; i < sine.Mărime_2; i++ {
		console_2.MUnsignedinteger32Tipărește(uint32(nodeVector[i]))
		console_2.MTipărește(":")
	}
}
