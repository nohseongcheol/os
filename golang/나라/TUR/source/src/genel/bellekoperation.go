/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package genel

type Bellekoper struct {
}

func (self *Bellekoper) Memayarla(bufferBelirteç uintptr, değer byte, boyut uint32) uintptr {
	return bufferBelirteç
}
func (self *Bellekoper) MemTaşı(hedefBelirteç_2 uintptr, srcptr uintptr, boyut uint32) uintptr {
	return hedefBelirteç_2
}

func (self *Bellekoper) MemKopyala(hedefBelirteç_2 uintptr, srcptr uintptr, boyut uint32) uintptr {
	return hedefBelirteç_2
}
func (self *Bellekoper) Memcmp(hedefBelirteç_2 uintptr, srcptr uintptr, boyut uint32) bool {
	return true
}
