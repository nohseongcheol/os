/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package rreshtimi

import . "unsafe"
import . "konsolë"

var nyjeRreshtimi [100]uintptr

type TRreshtimi struct {
	Madhësia_2 int
}

func (vetvetja *TRreshtimi) Shto(kursori uintptr) {
	nyjeRreshtimi[vetvetja.Madhësia_2] = kursori
	vetvetja.Madhësia_2++
}
func (vetvetja *TRreshtimi) Getat(treguesi int) Pointer {
	return Pointer(nyjeRreshtimi[treguesi])
}
func (vetvetja *TRreshtimi) Treguesinga(kursori uintptr) int {
	i := 0
	for ; i < vetvetja.Madhësia_2; i++ {
		if kursori == nyjeRreshtimi[i] {
			return i
		}
	}
	return -1
}

var konsolë_2 = TKonsolë{}

func (vetvetja *TRreshtimi) Printo() {
	konsolë_2.MPrintoxy("array:", 1, 1)

	for i := 0; i < vetvetja.Madhësia_2; i++ {
		konsolë_2.MUnsignedinteger32Printo(uint32(nyjeRreshtimi[i]))
		konsolë_2.MPrinto(":")
	}
}
