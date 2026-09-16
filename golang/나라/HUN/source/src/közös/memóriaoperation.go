/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package közös

type Memóriaoper struct {
}

func (self *Memóriaoper) Memhalmaz(bufferMutató uintptr, érték byte, méret uint32) uintptr {
	return bufferMutató
}
func (self *Memóriaoper) MemÁthelyezés(célMutató_2 uintptr, srcptr uintptr, méret uint32) uintptr {
	return célMutató_2
}

func (self *Memóriaoper) MemMásolás(célMutató_2 uintptr, srcptr uintptr, méret uint32) uintptr {
	return célMutató_2
}
func (self *Memóriaoper) Memcmp(célMutató_2 uintptr, srcptr uintptr, méret uint32) bool {
	return true
}
