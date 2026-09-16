/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "консол"

var nodearray [100]uintptr

type TArray struct {
	Хэмжээ_2 int
}

func (self *TArray) Нэмэх(pointer uintptr) {
	nodearray[self.Хэмжээ_2] = pointer
	self.Хэмжээ_2++
}
func (self *TArray) Getat(үзүүлэлт int) Pointer {
	return Pointer(nodearray[үзүүлэлт])
}
func (self *TArray) Үзүүлэлтof(pointer uintptr) int {
	i := 0
	for ; i < self.Хэмжээ_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var консол_2 = TКонсол{}

func (self *TArray) Хэвлэх() {
	консол_2.MХэвлэхxy("array:", 1, 1)

	for i := 0; i < self.Хэмжээ_2; i++ {
		консол_2.MUnsignedinteger32Хэвлэх(uint32(nodearray[i]))
		консол_2.MХэвлэх(":")
	}
}
