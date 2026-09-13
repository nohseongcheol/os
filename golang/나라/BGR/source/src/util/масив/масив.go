package масив

import . "unsafe"
import . "console"

var възловаточкаМасив [100]uintptr

type TМасив struct {
	Размер_2 int
}

func (себеси *TМасив) Добавяне(показалци uintptr) {
	възловаточкаМасив[себеси.Размер_2] = показалци
	себеси.Размер_2++
}
func (себеси *TМасив) Getat(съдържание int) Pointer {
	return Pointer(възловаточкаМасив[съдържание])
}
func (себеси *TМасив) Съдържаниеот(показалци uintptr) int {
	i := 0
	for ; i < себеси.Размер_2; i++ {
		if показалци == възловаточкаМасив[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (себеси *TМасив) Печат() {
	console_2.MПечатxy("array:", 1, 1)

	for i := 0; i < себеси.Размер_2; i++ {
		console_2.MUnsignedinteger32Печат(uint32(възловаточкаМасив[i]))
		console_2.MПечат(":")
	}
}
