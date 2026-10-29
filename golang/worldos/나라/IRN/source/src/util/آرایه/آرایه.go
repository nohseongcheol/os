/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package آرایه

import . "unsafe"
import . "console"

var nodeآرایه [100]uintptr

type Tآرایه struct {
	Sاندازه_2 int
}

func (خود *Tآرایه) Aاضافهکردن(pointer uintptr) {
	nodeآرایه[خود.Sاندازه_2] = pointer
	خود.Sاندازه_2++
}
func (خود *Tآرایه) Getat(نمایه int) Pointer {
	return Pointer(nodeآرایه[نمایه])
}
func (خود *Tآرایه) Iنمایهof(pointer uintptr) int {
	i := 0
	for ; i < خود.Sاندازه_2; i++ {
		if pointer == nodeآرایه[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (خود *Tآرایه) Pچاپ() {
	console_2.Mچاپxy("array:", 1, 1)

	for i := 0; i < خود.Sاندازه_2; i++ {
		console_2.MUnsignedinteger32چاپ(uint32(nodeآرایه[i]))
		console_2.Mچاپ(":")
	}
}
