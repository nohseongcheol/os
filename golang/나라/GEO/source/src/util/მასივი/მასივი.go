package მასივი

import . "unsafe"
import . "console"

var nodeმასივი [100]uintptr

type Tმასივი struct {
	Sზომა_2 int
}

func (self *Tმასივი) Aდამატება(კურსორი uintptr) {
	nodeმასივი[self.Sზომა_2] = კურსორი
	self.Sზომა_2++
}
func (self *Tმასივი) Getat(ინდექსი int) Pointer {
	return Pointer(nodeმასივი[ინდექსი])
}
func (self *Tმასივი) Iინდექსიof(კურსორი uintptr) int {
	i := 0
	for ; i < self.Sზომა_2; i++ {
		if კურსორი == nodeმასივი[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *Tმასივი) Pბეჭდვა() {
	console_2.Mბეჭდვაxy("array:", 1, 1)

	for i := 0; i < self.Sზომა_2; i++ {
		console_2.MUnsignedinteger32ბეჭდვა(uint32(nodeმასივი[i]))
		console_2.Mბეჭდვა(":")
	}
}
