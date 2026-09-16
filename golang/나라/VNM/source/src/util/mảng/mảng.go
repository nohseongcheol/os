/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package mảng

import . "unsafe"
import . "console"

var nodeMảng [100]uintptr

type TMảng struct {
	Cỡ_2 int
}

func (mình *TMảng) Thêm(tham_chiếu_địa_chỉ uintptr) {
	nodeMảng[mình.Cỡ_2] = tham_chiếu_địa_chỉ
	mình.Cỡ_2++
}
func (mình *TMảng) Getat(chỉmục int) Pointer {
	return Pointer(nodeMảng[chỉmục])
}
func (mình *TMảng) Chỉmụctrên(tham_chiếu_địa_chỉ uintptr) int {
	i := 0
	for ; i < mình.Cỡ_2; i++ {
		if tham_chiếu_địa_chỉ == nodeMảng[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (mình *TMảng) In() {
	console_2.MInxy("array:", 1, 1)

	for i := 0; i < mình.Cỡ_2; i++ {
		console_2.MUnsignedinteger32In(uint32(nodeMảng[i]))
		console_2.MIn(":")
	}
}
