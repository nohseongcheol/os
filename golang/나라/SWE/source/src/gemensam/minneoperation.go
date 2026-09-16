/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gemensam

type Minneoper struct {
}

func (själv *Minneoper) Memmängd(bufferMuspekare uintptr, värde byte, storlek uint32) uintptr {
	return bufferMuspekare
}
func (själv *Minneoper) MemFlytta(målMuspekare_2 uintptr, srcptr uintptr, storlek uint32) uintptr {
	return målMuspekare_2
}

func (själv *Minneoper) MemKopiera(målMuspekare_2 uintptr, srcptr uintptr, storlek uint32) uintptr {
	return målMuspekare_2
}
func (själv *Minneoper) Memcmp(målMuspekare_2 uintptr, srcptr uintptr, storlek uint32) bool {
	return true
}
