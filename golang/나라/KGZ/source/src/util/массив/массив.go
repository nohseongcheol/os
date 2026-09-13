package массив

import . "unsafe"
import . "console"

var nodeМассив [100]uintptr

type TМассив struct {
	Өлчөм_2 int
}

func (self *TМассив) Кошуу(көрсөткүч uintptr) {
	nodeМассив[self.Өлчөм_2] = көрсөткүч
	self.Өлчөм_2++
}
func (self *TМассив) Getat(мазмун int) Pointer {
	return Pointer(nodeМассив[мазмун])
}
func (self *TМассив) Мазмунof(көрсөткүч uintptr) int {
	i := 0
	for ; i < self.Өлчөм_2; i++ {
		if көрсөткүч == nodeМассив[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TМассив) Басма() {
	console_2.MБасмаxy("array:", 1, 1)

	for i := 0; i < self.Өлчөм_2; i++ {
		console_2.MUnsignedinteger32Басма(uint32(nodeМассив[i]))
		console_2.MБасма(":")
	}
}
