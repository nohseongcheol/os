/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package massiiv

import . "unsafe"
import . "console"

var sõlmMassiiv [100]uintptr

type TMassiiv struct {
	Suurus_2 int
}

func (ise *TMassiiv) Lisa(kursor uintptr) {
	sõlmMassiiv[ise.Suurus_2] = kursor
	ise.Suurus_2++
}
func (ise *TMassiiv) Getat(sisukord int) Pointer {
	return Pointer(sõlmMassiiv[sisukord])
}
func (ise *TMassiiv) Sisukordof(kursor uintptr) int {
	i := 0
	for ; i < ise.Suurus_2; i++ {
		if kursor == sõlmMassiiv[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (ise *TMassiiv) Prindi() {
	console_2.MPrindixy("array:", 1, 1)

	for i := 0; i < ise.Suurus_2; i++ {
		console_2.MUnsignedinteger32Prindi(uint32(sõlmMassiiv[i]))
		console_2.MPrindi(":")
	}
}
