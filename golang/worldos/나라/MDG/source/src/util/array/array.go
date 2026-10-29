/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package array

import . "unsafe"
import . "konsoly"

var nodearray [100]uintptr

type TArray struct {
	Habe_2 int
}

func (nytena *TArray) Ampidiro(pointer uintptr) {
	nodearray[nytena.Habe_2] = pointer
	nytena.Habe_2++
}
func (nytena *TArray) Getat(fizahantakila int) Pointer {
	return Pointer(nodearray[fizahantakila])
}
func (nytena *TArray) Fizahantakilaaminny(pointer uintptr) int {
	i := 0
	for ; i < nytena.Habe_2; i++ {
		if pointer == nodearray[i] {
			return i
		}
	}
	return -1
}

var konsoly_2 = TKonsoly{}

func (nytena *TArray) Atontay() {
	konsoly_2.MAtontayxy("array:", 1, 1)

	for i := 0; i < nytena.Habe_2; i++ {
		konsoly_2.MUnsignedinteger32Atontay(uint32(nodearray[i]))
		konsoly_2.MAtontay(":")
	}
}
