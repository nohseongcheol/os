/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package заједнички

type Memorijaoper struct {
}

func (isti *Memorijaoper) Memскуп(bufferPokazivač uintptr, вредност byte, величина uint32) uintptr {
	return bufferPokazivač
}
func (isti *Memorijaoper) MemПремести(odredištePokazivač_2 uintptr, srcptr uintptr, величина uint32) uintptr {
	return odredištePokazivač_2
}

func (isti *Memorijaoper) MemУмножи(odredištePokazivač_2 uintptr, srcptr uintptr, величина uint32) uintptr {
	return odredištePokazivač_2
}
func (isti *Memorijaoper) Memcmp(odredištePokazivač_2 uintptr, srcptr uintptr, величина uint32) bool {
	return true
}
