/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package zwykły

type Pamięćoper struct {
}

func (bieżący *Pamięćoper) Memzbiór(bufferKursor uintptr, wartość byte, rozmiar uint32) uintptr {
	return bufferKursor
}
func (bieżący *Pamięćoper) MemPrzenoszenie(celKursor_2 uintptr, srcptr uintptr, rozmiar uint32) uintptr {
	return celKursor_2
}

func (bieżący *Pamięćoper) MemKopiuj(celKursor_2 uintptr, srcptr uintptr, rozmiar uint32) uintptr {
	return celKursor_2
}
func (bieżący *Pamięćoper) Memcmp(celKursor_2 uintptr, srcptr uintptr, rozmiar uint32) bool {
	return true
}
