package common

type Эсиoper struct {
}

func (self *Эсиoper) Memset(bufferКөрсөткүч uintptr, мааниси byte, өлчөм uint32) uintptr {
	return bufferКөрсөткүч
}
func (self *Эсиoper) MemТашуу(destinationКөрсөткүч_2 uintptr, srcptr uintptr, өлчөм uint32) uintptr {
	return destinationКөрсөткүч_2
}

func (self *Эсиoper) MemКөчүрүү(destinationКөрсөткүч_2 uintptr, srcptr uintptr, өлчөм uint32) uintptr {
	return destinationКөрсөткүч_2
}
func (self *Эсиoper) Memcmp(destinationКөрсөткүч_2 uintptr, srcptr uintptr, өлчөм uint32) bool {
	return true
}
