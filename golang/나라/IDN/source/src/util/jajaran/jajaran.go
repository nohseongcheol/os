/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package jajaran

import . "unsafe"
import . "console"

var nodeJajaran [100]uintptr

type TJajaran struct {
	Ukuran_2 int
}

func (dirisendiri *TJajaran) Tambah(acuan_alamat uintptr) {
	nodeJajaran[dirisendiri.Ukuran_2] = acuan_alamat
	dirisendiri.Ukuran_2++
}
func (dirisendiri *TJajaran) Getat(indeks int) Pointer {
	return Pointer(nodeJajaran[indeks])
}
func (dirisendiri *TJajaran) Indeksdari(acuan_alamat uintptr) int {
	i := 0
	for ; i < dirisendiri.Ukuran_2; i++ {
		if acuan_alamat == nodeJajaran[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (dirisendiri *TJajaran) Cetak() {
	console_2.MCetakxy("array:", 1, 1)

	for i := 0; i < dirisendiri.Ukuran_2; i++ {
		console_2.MUnsignedinteger32Cetak(uint32(nodeJajaran[i]))
		console_2.MCetak(":")
	}
}
