package масіў

import . "unsafe"
import . "console"

var nodeМасіў [100]uintptr

type TМасіў struct {
	Памер_2 int
}

func (self *TМасіў) Дадаць(паказальнік uintptr) {
	nodeМасіў[self.Памер_2] = паказальнік
	self.Памер_2++
}
func (self *TМасіў) Getat(змест int) Pointer {
	return Pointer(nodeМасіў[змест])
}
func (self *TМасіў) Зместз(паказальнік uintptr) int {
	i := 0
	for ; i < self.Памер_2; i++ {
		if паказальнік == nodeМасіў[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TМасіў) Друкаваць() {
	console_2.MДрукавацьxy("array:", 1, 1)

	for i := 0; i < self.Памер_2; i++ {
		console_2.MUnsignedinteger32Друкаваць(uint32(nodeМасіў[i]))
		console_2.MДрукаваць(":")
	}
}
