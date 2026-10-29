/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package üldine

type Mäluoper struct {
}

func (ise *Mäluoper) MemMäära(bufferKursor uintptr, väärtus byte, suurus uint32) uintptr {
	return bufferKursor
}
func (ise *Mäluoper) MemLiiguta(sihtfailKursor_2 uintptr, srcptr uintptr, suurus uint32) uintptr {
	return sihtfailKursor_2
}

func (ise *Mäluoper) MemKopeeri(sihtfailKursor_2 uintptr, srcptr uintptr, suurus uint32) uintptr {
	return sihtfailKursor_2
}
func (ise *Mäluoper) Memcmp(sihtfailKursor_2 uintptr, srcptr uintptr, suurus uint32) bool {
	return true
}
