/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package заједнички

type Меморијаoper struct {
}

func (исти *Меморијаoper) Memскуп(bufferПоказивач uintptr, вредност byte, величина uint32) uintptr {
	return bufferПоказивач
}
func (исти *Меморијаoper) MemПремести(одредиштеПоказивач_2 uintptr, srcptr uintptr, величина uint32) uintptr {
	return одредиштеПоказивач_2
}

func (исти *Меморијаoper) MemУмножи(одредиштеПоказивач_2 uintptr, srcptr uintptr, величина uint32) uintptr {
	return одредиштеПоказивач_2
}
func (исти *Меморијаoper) Memcmp(одредиштеПоказивач_2 uintptr, srcptr uintptr, величина uint32) bool {
	return true
}
