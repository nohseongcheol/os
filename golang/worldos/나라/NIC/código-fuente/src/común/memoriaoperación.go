/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package común

type Memoriaoper struct {
}

func (propio *Memoriaoper) Memestablecer(bufferPuntero uintptr, valor byte, tamaño uint32) uintptr {
	return bufferPuntero
}
func (propio *Memoriaoper) MemMover(destinoPuntero_2 uintptr, srcptr uintptr, tamaño uint32) uintptr {
	return destinoPuntero_2
}

func (propio *Memoriaoper) Memcopiar(destinoPuntero_2 uintptr, srcptr uintptr, tamaño uint32) uintptr {
	return destinoPuntero_2
}
func (propio *Memoriaoper) Memcmp(destinoPuntero_2 uintptr, srcptr uintptr, tamaño uint32) bool {
	return true
}
