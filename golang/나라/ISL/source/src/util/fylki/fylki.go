package fylki

import . "unsafe"
import . "console"

var hnúturFylki [100]uintptr

type TFylki struct {
	Stærð_2 int
}

func (sjálft *TFylki) Bætavið(bendill uintptr) {
	hnúturFylki[sjálft.Stærð_2] = bendill
	sjálft.Stærð_2++
}
func (sjálft *TFylki) Getat(index int) Pointer {
	return Pointer(hnúturFylki[index])
}
func (sjálft *TFylki) Indexaf(bendill uintptr) int {
	i := 0
	for ; i < sjálft.Stærð_2; i++ {
		if bendill == hnúturFylki[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (sjálft *TFylki) Prenta() {
	console_2.MPrentaxy("array:", 1, 1)

	for i := 0; i < sjálft.Stærð_2; i++ {
		console_2.MUnsignedinteger32Prenta(uint32(hnúturFylki[i]))
		console_2.MPrenta(":")
	}
}
