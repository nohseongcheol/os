package format_pelaksanaan_dan_pemautan

import . "unsafe"
import . "console"

import mem "ingatanmanager"

type Pautan struct {
	Dynamic		uintptr
	Previous	*Pautan
	Berikutnya	*Pautan
}
type Pautanmap struct {
	First		*Pautan
	Terakhir	*Pautan

	Saiz_2	int

	mem	*mem.TIngatanmanager
}

func (diri *Pautanmap) Init(mem *mem.TIngatanmanager) {
	diri.mem = mem
}
func (diri *Pautanmap) Clone() Pautanmap {
	var pautanmap Pautanmap

	pautanmap.Init(diri.mem)

	Pautan := diri.First

	for ; Pautan != nil; Pautan = Pautan.Berikutnya {
		pautanmap.Tambah_di_hujung_senarai(Pautan.Dynamic)
	}
	return pautanmap
}
func (diri *Pautanmap) Tambah_di_awal_senarai(Dynamic uintptr) {
	baharuPautan := (*Pautan)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(Pautan{}))))
	baharuPautan.Dynamic = Dynamic
	baharuPautan.Berikutnya = diri.First
	diri.First = baharuPautan
	diri.Saiz_2++

	if diri.First.Berikutnya == nil {
		diri.Terakhir = diri.First
	}
}
func (diri *Pautanmap) Tambah_di_hujung_senarai(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if diri.Saiz_2 == 0 {
		diri.Tambah_di_awal_senarai(Dynamic)
	} else {
		baharuPautan := (*Pautan)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(Pautan{}))))
		baharuPautan.Dynamic = Dynamic
		baharuPautan.Berikutnya = nil
		diri.Terakhir.Berikutnya = baharuPautan
		diri.Terakhir = baharuPautan
		diri.Saiz_2++
	}
}
func (diri *Pautanmap) Cetak(x uint16, y uint16) {
	Pautan := diri.First
	console_2 := TConsole{}
	console_2.MCetakxy("linkmap : ", x, y)
	for ; Pautan != nil; Pautan = Pautan.Berikutnya {
		console_2.MUnsignedinteger32Cetak(uint32(Pautan.Dynamic))
		console_2.MCetak("+")

	}
}
