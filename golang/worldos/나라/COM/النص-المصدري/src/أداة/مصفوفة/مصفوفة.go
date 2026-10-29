/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package مصفوفة

import . "unsafe"
import . "طرفية"

var العقدةمصفوفة [100]uintptr

type Tمصفوفة struct {
	Sالحجم_2 int
}

func (نفسه *Tمصفوفة) Aأضف(مرجع_عنوان uintptr) {
	العقدةمصفوفة[نفسه.Sالحجم_2] = مرجع_عنوان
	نفسه.Sالحجم_2++
}
func (نفسه *Tمصفوفة) Getat(فهرس int) Pointer {
	return Pointer(العقدةمصفوفة[فهرس])
}
func (نفسه *Tمصفوفة) Iفهرسof(مرجع_عنوان uintptr) int {
	i := 0
	for ; i < نفسه.Sالحجم_2; i++ {
		if مرجع_عنوان == العقدةمصفوفة[i] {
			return i
		}
	}
	return -1
}

var طرفية_2 = Tطرفية{}

func (نفسه *Tمصفوفة) Pاطبع() {
	طرفية_2.Mاطبعxy("array:", 1, 1)

	for i := 0; i < نفسه.Sالحجم_2; i++ {
		طرفية_2.MUnsignedinteger32اطبع(uint32(العقدةمصفوفة[i]))
		طرفية_2.Mاطبع(":")
	}
}
