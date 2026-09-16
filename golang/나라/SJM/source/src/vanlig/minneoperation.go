/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package vanlig

type Minneoper struct {
}

func (selv *Minneoper) MemSett(bufferPeker uintptr, verdi byte, størrelse uint32) uintptr {
	return bufferPeker
}
func (selv *Minneoper) MemFlytt(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return målPeker_2
}

func (selv *Minneoper) MemKopier(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) uintptr {
	return målPeker_2
}
func (selv *Minneoper) Memcmp(målPeker_2 uintptr, srcptr uintptr, størrelse uint32) bool {
	return true
}
