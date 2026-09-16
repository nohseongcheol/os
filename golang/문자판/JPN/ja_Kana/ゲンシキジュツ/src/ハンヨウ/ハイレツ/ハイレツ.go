/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ハイレツ

import . "unsafe"
import . "コンソール"

var ノードハイレツ [100]uintptr

type Tハイレツ struct {
	Sサイズ_2 int
}

func (self *Tハイレツ) Aツイカ(バンチサンショウ uintptr) {
	ノードハイレツ[self.Sサイズ_2] = バンチサンショウ
	self.Sサイズ_2++
}
func (self *Tハイレツ) Getat(モクジ int) Pointer {
	return Pointer(ノードハイレツ[モクジ])
}
func (self *Tハイレツ) Iモクジof(バンチサンショウ uintptr) int {
	i := 0
	for ; i < self.Sサイズ_2; i++ {
		if バンチサンショウ == ノードハイレツ[i] {
			return i
		}
	}
	return -1
}

var コンソール_2 = Tコンソール{}

func (self *Tハイレツ) Pインサツ() {
	コンソール_2.Mインサツxy("array:", 1, 1)

	for i := 0; i < self.Sサイズ_2; i++ {
		コンソール_2.MUnsignedinteger32インサツ(uint32(ノードハイレツ[i]))
		コンソール_2.Mインサツ(":")
	}
}
