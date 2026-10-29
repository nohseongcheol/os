/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package masīvs

import . "unsafe"
import . "console"

var nodeMasīvs [100]uintptr

type TMasīvs struct {
	Izmērs_2 int
}

func (pats *TMasīvs) Pievienot(kursors uintptr) {
	nodeMasīvs[pats.Izmērs_2] = kursors
	pats.Izmērs_2++
}
func (pats *TMasīvs) Getat(saturs int) Pointer {
	return Pointer(nodeMasīvs[saturs])
}
func (pats *TMasīvs) Satursno(kursors uintptr) int {
	i := 0
	for ; i < pats.Izmērs_2; i++ {
		if kursors == nodeMasīvs[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (pats *TMasīvs) Drukāt() {
	console_2.MDrukātxy("array:", 1, 1)

	for i := 0; i < pats.Izmērs_2; i++ {
		console_2.MUnsignedinteger32Drukāt(uint32(nodeMasīvs[i]))
		console_2.MDrukāt(":")
	}
}
