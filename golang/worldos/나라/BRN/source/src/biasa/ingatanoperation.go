/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package biasa

type Ingatanoper struct {
}

func (diri *Ingatanoper) MemTetapkan(bufferPenuding uintptr, nilai byte, saiz uint32) uintptr {
	return bufferPenuding
}
func (diri *Ingatanoper) MemAlih(destinationPenuding_2 uintptr, srcptr uintptr, saiz uint32) uintptr {
	return destinationPenuding_2
}

func (diri *Ingatanoper) MemSalin(destinationPenuding_2 uintptr, srcptr uintptr, saiz uint32) uintptr {
	return destinationPenuding_2
}
func (diri *Ingatanoper) Memcmp(destinationPenuding_2 uintptr, srcptr uintptr, saiz uint32) bool {
	return true
}
