package format_eksekusi_dan_penautan

import . "unsafe"
import . "console"

import mem "memorimanager"

type Taut struct {
	Dinamis		uintptr
	Previous	*Taut
	Berikutnya	*Taut
}
type Tautmap struct {
	First		*Taut
	Terakhir	*Taut

	Ukuran_2	int

	mem	*mem.TMemorimanager
}

func (dirisendiri *Tautmap) Init(mem *mem.TMemorimanager) {
	dirisendiri.mem = mem
}
func (dirisendiri *Tautmap) Clone() Tautmap {
	var tautmap Tautmap

	tautmap.Init(dirisendiri.mem)

	Taut := dirisendiri.First

	for ; Taut != nil; Taut = Taut.Berikutnya {
		tautmap.Tambah_di_akhir_daftar(Taut.Dinamis)
	}
	return tautmap
}
func (dirisendiri *Tautmap) Tambah_di_awal_daftar(Dinamis uintptr) {
	baruTaut := (*Taut)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(Taut{}))))
	baruTaut.Dinamis = Dinamis
	baruTaut.Berikutnya = dirisendiri.First
	dirisendiri.First = baruTaut
	dirisendiri.Ukuran_2++

	if dirisendiri.First.Berikutnya == nil {
		dirisendiri.Terakhir = dirisendiri.First
	}
}
func (dirisendiri *Tautmap) Tambah_di_akhir_daftar(Dinamis uintptr) {
	if Dinamis == 0 {
		return
	}

	if dirisendiri.Ukuran_2 == 0 {
		dirisendiri.Tambah_di_awal_daftar(Dinamis)
	} else {
		baruTaut := (*Taut)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(Taut{}))))
		baruTaut.Dinamis = Dinamis
		baruTaut.Berikutnya = nil
		dirisendiri.Terakhir.Berikutnya = baruTaut
		dirisendiri.Terakhir = baruTaut
		dirisendiri.Ukuran_2++
	}
}
func (dirisendiri *Tautmap) Cetak(x uint16, y uint16) {
	Taut := dirisendiri.First
	console_2 := TConsole{}
	console_2.MCetakxy("linkmap : ", x, y)
	for ; Taut != nil; Taut = Taut.Berikutnya {
		console_2.MUnsignedinteger32Cetak(uint32(Taut.Dinamis))
		console_2.MCetak("+")

	}
}
