/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package imbonerahamwe

import . "unsafe"
import . "console"

var nodeImbonerahamwe [100]uintptr

type TImbonerahamwe struct {
	Ingano_2 int
}

func (self *TImbonerahamwe) Kongera(pointer uintptr) {
	nodeImbonerahamwe[self.Ingano_2] = pointer
	self.Ingano_2++
}
func (self *TImbonerahamwe) Getat(umubarendanga int) Pointer {
	return Pointer(nodeImbonerahamwe[umubarendanga])
}
func (self *TImbonerahamwe) Umubarendangaof(pointer uintptr) int {
	i := 0
	for ; i < self.Ingano_2; i++ {
		if pointer == nodeImbonerahamwe[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TImbonerahamwe) Gucapa() {
	console_2.MGucapaxy("array:", 1, 1)

	for i := 0; i < self.Ingano_2; i++ {
		console_2.MUnsignedinteger32Gucapa(uint32(nodeImbonerahamwe[i]))
		console_2.MGucapa(":")
	}
}
