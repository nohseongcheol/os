/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package almen

type Hukommelseoper struct {
}

func (selv *Hukommelseoper) Memsat(bufferMarkør uintptr, værdi byte, størrelse uint32) uintptr {
	return bufferMarkør
}
func (selv *Hukommelseoper) MemFlyt(destinationMarkør_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return destinationMarkør_2
}

func (selv *Hukommelseoper) MemKopiér(destinationMarkør_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return destinationMarkør_2
}
func (selv *Hukommelseoper) Memcmp(destinationMarkør_2 uintptr, srcptr uintptr, størrelse uint32) bool {
	return true
}
