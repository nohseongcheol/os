package comum

type Memóriaoper struct {
}

func (próprio *Memóriaoper) Memconjunto(bufferPonteiro uintptr, valor byte, tamanho uint32) uintptr {
	return bufferPonteiro
}
func (próprio *Memóriaoper) MemMover(destinoPonteiro_2 uintptr, srcptr uintptr, tamanho uint32) uintptr {
	return destinoPonteiro_2
}

func (próprio *Memóriaoper) Memcopiar(destinoPonteiro_2 uintptr, srcptr uintptr, tamanho uint32) uintptr {
	return destinoPonteiro_2
}
func (próprio *Memóriaoper) Memcmp(destinoPonteiro_2 uintptr, srcptr uintptr, tamanho uint32) bool {
	return true
}
