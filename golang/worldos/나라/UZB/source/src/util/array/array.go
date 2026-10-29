/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodearray [100]uintptr

type TArray struct {
	Hajmi_2 int
}

func (self *TArray) Qoʻshish(korsatgich uintptr) {
	nodearray[self.Hajmi_2] = korsatgich
	self.Hajmi_2++
}
func (self *TArray) Getat(index int) Pointer {
	return Pointer(nodearray[index])
}
func (self *TArray) Indexof(korsatgich uintptr) int {
	i := 0
	for ; i < self.Hajmi_2; i++ {
		if korsatgich == nodearray[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TArray) Chopetish() {
	console_2.MChopetishxy("array:", 1, 1)

	for i := 0; i < self.Hajmi_2; i++ {
		console_2.MUnsignedinteger32Chopetish(uint32(nodearray[i]))
		console_2.MChopetish(":")
	}
}
