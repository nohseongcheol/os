/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "console"

var nodeArray [100]uintptr

type TArray struct {
	Vಗಾತ್ರ int
}

func (self *TArray) Add(ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	nodeArray[self.Vಗಾತ್ರ] = ವಿಳಾಸ_ಸೂಚಕ
	self.Vಗಾತ್ರ++
}
func (self *TArray) GetAt(index int) Pointer {
	return Pointer(nodeArray[index])
}
func (self *TArray) IndexOf(ವಿಳಾಸ_ಸೂಚಕ uintptr) int {
	i := 0
	for ; i < self.Vಗಾತ್ರ; i++ {
		if ವಿಳಾಸ_ಸೂಚಕ == nodeArray[i] {
			return i
		}
	}
	return -1
}

var 콘솔 = T콘솔{}

func (self *TArray) Print() {
	콘솔.M출력XY("array:", 1, 1)

	for i := 0; i < self.Vಗಾತ್ರ; i++ {
		콘솔.MUint32출력(uint32(nodeArray[i]))
		콘솔.M출력(":")
	}
}
