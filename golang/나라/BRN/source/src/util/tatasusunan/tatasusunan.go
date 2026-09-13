package tatasusunan

import . "unsafe"
import . "console"

var nodTatasusunan [100]uintptr

type TTatasusunan struct {
	Saiz_2 int
}

func (diri *TTatasusunan) Tambah(rujukan_alamat uintptr) {
	nodTatasusunan[diri.Saiz_2] = rujukan_alamat
	diri.Saiz_2++
}
func (diri *TTatasusunan) Getat(indeks int) Pointer {
	return Pointer(nodTatasusunan[indeks])
}
func (diri *TTatasusunan) Indeksdari(rujukan_alamat uintptr) int {
	i := 0
	for ; i < diri.Saiz_2; i++ {
		if rujukan_alamat == nodTatasusunan[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (diri *TTatasusunan) Cetak() {
	console_2.MCetakxy("array:", 1, 1)

	for i := 0; i < diri.Saiz_2; i++ {
		console_2.MUnsignedinteger32Cetak(uint32(nodTatasusunan[i]))
		console_2.MCetak(":")
	}
}
