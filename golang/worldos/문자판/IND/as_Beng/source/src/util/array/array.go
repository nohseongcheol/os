/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vআকাৰ int
}

func (self *TArray) Add(ঠিকনা_সূচক uintptr) {
	nodeArray[self.Vআকাৰ] = ঠিকনা_সূচক
	self.Vআকাৰ++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(ঠিকনা_সূচক uintptr) int {
	i := 0
	for ; i < self.Vআকাৰ; i++ {
		if ঠিকনা_সূচক == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vআকাৰ; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
