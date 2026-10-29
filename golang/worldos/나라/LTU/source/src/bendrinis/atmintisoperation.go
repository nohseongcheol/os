/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package bendrinis

type Atmintisoper struct {
}

func (self *Atmintisoper) Memnustatyta(bufferRodyklė uintptr, reikšmė byte, dydis uint32) uintptr {
	return bufferRodyklė
}
func (self *Atmintisoper) MemPerkelti(tikslasRodyklė_2 uintptr, srcptr uintptr, dydis uint32) uintptr {
	return tikslasRodyklė_2
}

func (self *Atmintisoper) MemKopijuoti(tikslasRodyklė_2 uintptr, srcptr uintptr, dydis uint32) uintptr {
	return tikslasRodyklė_2
}
func (self *Atmintisoper) Memcmp(tikslasRodyklė_2 uintptr, srcptr uintptr, dydis uint32) bool {
	return true
}
