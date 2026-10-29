/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package զանգված

import . "unsafe"
import . "console"

var nodeԶանգված [100]uintptr

type TԶանգված struct {
	Չափս_2 int
}

func (ինքնուրույն *TԶանգված) Ավելացնել(ցուցիչ uintptr) {
	nodeԶանգված[ինքնուրույն.Չափս_2] = ցուցիչ
	ինքնուրույն.Չափս_2++
}
func (ինքնուրույն *TԶանգված) Getat(ինդեքս int) Pointer {
	return Pointer(nodeԶանգված[ինդեքս])
}
func (ինքնուրույն *TԶանգված) Ինդեքսof(ցուցիչ uintptr) int {
	i := 0
	for ; i < ինքնուրույն.Չափս_2; i++ {
		if ցուցիչ == nodeԶանգված[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (ինքնուրույն *TԶանգված) Տպել() {
	console_2.MՏպելxy("array:", 1, 1)

	for i := 0; i < ինքնուրույն.Չափս_2; i++ {
		console_2.MUnsignedinteger32Տպել(uint32(nodeԶանգված[i]))
		console_2.MՏպել(":")
	}
}
