/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package umum

type Memorioper struct {
}

func (dirisendiri *Memorioper) MemAtur(bufferPenunjuk uintptr, nilai byte, ukuran uint32) uintptr {
	return bufferPenunjuk
}
func (dirisendiri *Memorioper) MemPindah(tujuanPenunjuk_2 uintptr, srcptr uintptr, ukuran uint32) uintptr {
	return tujuanPenunjuk_2
}

func (dirisendiri *Memorioper) MemSalin(tujuanPenunjuk_2 uintptr, srcptr uintptr, ukuran uint32) uintptr {
	return tujuanPenunjuk_2
}
func (dirisendiri *Memorioper) Memcmp(tujuanPenunjuk_2 uintptr, srcptr uintptr, ukuran uint32) bool {
	return true
}
