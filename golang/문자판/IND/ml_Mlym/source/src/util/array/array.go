/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vവലുപ്പം int
}

func (self *TArray) Add(വിലാസ_സൂചിക uintptr) {
	nodeArray[self.Vവലുപ്പം] = വിലാസ_സൂചിക
	self.Vവലുപ്പം++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(വിലാസ_സൂചിക uintptr) int {
	i := 0
	for ; i < self.Vവലുപ്പം; i++ {
		if വിലാസ_സൂചിക == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vവലുപ്പം; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
