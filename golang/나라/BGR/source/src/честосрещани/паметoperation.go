/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package честосрещани

type Паметoper struct {
}

func (себеси *Паметoper) MemЗадай(bufferПоказалци uintptr, стойност byte, размер uint32) uintptr {
	return bufferПоказалци
}
func (себеси *Паметoper) MemПреместване(назначениеПоказалци_2 uintptr, srcptr uintptr, размер uint32) uintptr {
	return назначениеПоказалци_2
}

func (себеси *Паметoper) MemКопиране(назначениеПоказалци_2 uintptr, srcptr uintptr, размер uint32) uintptr {
	return назначениеПоказалци_2
}
func (себеси *Паметoper) Memcmp(назначениеПоказалци_2 uintptr, srcptr uintptr, размер uint32) bool {
	return true
}
