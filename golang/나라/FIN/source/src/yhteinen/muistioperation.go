/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package yhteinen

type Muistioper struct {
}

func (itse *Muistioper) Memaseta(bufferOsoitin uintptr, arvo byte, koko uint32) uintptr {
	return bufferOsoitin
}
func (itse *Muistioper) MemSiirrä(kohdeOsoitin_2 uintptr, srcptr uintptr, koko uint32) uintptr {
	return kohdeOsoitin_2
}

func (itse *Muistioper) MemKopioi(kohdeOsoitin_2 uintptr, srcptr uintptr, koko uint32) uintptr {
	return kohdeOsoitin_2
}
func (itse *Muistioper) Memcmp(kohdeOsoitin_2 uintptr, srcptr uintptr, koko uint32) bool {
	return true
}
