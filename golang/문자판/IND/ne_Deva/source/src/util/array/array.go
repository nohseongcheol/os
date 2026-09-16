/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vआकार int
}

func (self *TArray) Add(ठेगाना_सूचक uintptr) {
	nodeArray[self.Vआकार] = ठेगाना_सूचक
	self.Vआकार++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(ठेगाना_सूचक uintptr) int {
	i := 0
	for ; i < self.Vआकार; i++ {
		if ठेगाना_सूचक == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vआकार; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
