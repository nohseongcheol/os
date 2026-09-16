/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package comú

type Memòriaoper struct {
}

func (unmateix *Memòriaoper) Memestableix(bufferPunter uintptr, valor byte, mida uint32) uintptr {
	return bufferPunter
}
func (unmateix *Memòriaoper) MemMou(destinacióPunter_2 uintptr, srcptr uintptr, mida uint32) uintptr {
	return destinacióPunter_2
}

func (unmateix *Memòriaoper) MemCopia(destinacióPunter_2 uintptr, srcptr uintptr, mida uint32) uintptr {
	return destinacióPunter_2
}
func (unmateix *Memòriaoper) Memcmp(destinacióPunter_2 uintptr, srcptr uintptr, mida uint32) bool {
	return true
}
