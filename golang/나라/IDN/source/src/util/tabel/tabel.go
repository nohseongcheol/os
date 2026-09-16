/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tabel

import . "unsafe"
import . "console"
import mem "memorimanager"

type TSimpul_daftar struct {
	acuan_alamat	uintptr
	previous	*TSimpul_daftar
	berikutnya	*TSimpul_daftar
}

type LinkedTabel struct {
	head		*TSimpul_daftar
	tail		*TSimpul_daftar
	Ukuran_2	int

	mem	*mem.TMemorimanager
}

func (dirisendiri *LinkedTabel) Init(mem *mem.TMemorimanager) {
	dirisendiri.head = nil
	dirisendiri.tail = nil
	dirisendiri.Ukuran_2 = 0

	dirisendiri.mem = mem
}
func (dirisendiri *LinkedTabel) Tambah_di_awal_daftar(acuan_alamat uintptr) {
	barunode := (*TSimpul_daftar)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(TSimpul_daftar{}))))
	if barunode == nil {
		return
	}
	barunode.acuan_alamat = acuan_alamat
	barunode.previous = nil
	barunode.berikutnya = dirisendiri.head
	if dirisendiri.head != nil {
		dirisendiri.head.previous = barunode
	}
	dirisendiri.head = barunode
	dirisendiri.Ukuran_2++

	if dirisendiri.head.berikutnya == nil {
		dirisendiri.tail = dirisendiri.head
	}

}
func (dirisendiri *LinkedTabel) Tambah_di_akhir_daftar(acuan_alamat uintptr) {
	if dirisendiri.Ukuran_2 == 0 {
		dirisendiri.Tambah_di_awal_daftar(acuan_alamat)
	} else {
		barunode := (*TSimpul_daftar)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(TSimpul_daftar{}))))
		if barunode == nil {
			return
		}
		barunode.acuan_alamat = acuan_alamat
		barunode.previous = dirisendiri.tail
		barunode.berikutnya = nil
		dirisendiri.tail.berikutnya = barunode
		dirisendiri.tail = barunode
		dirisendiri.Ukuran_2++
	}
}
func (dirisendiri *LinkedTabel) Sisipkan_pada_indeks(indeks int, acuan_alamat uintptr) {
	if indeks == 0 {
		dirisendiri.Tambah_di_awal_daftar(acuan_alamat)
	} else {
		previousnode := dirisendiri.Getnodeat(indeks - 1)
		berikutnyanode := previousnode.berikutnya
		barunode := (*TSimpul_daftar)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(TSimpul_daftar{}))))
		if barunode == nil {
			return
		}
		barunode.acuan_alamat = acuan_alamat

		previousnode.berikutnya = barunode
		barunode.previous = previousnode
		barunode.berikutnya = berikutnyanode
		if berikutnyanode != nil {
			berikutnyanode.previous = barunode
		}

		dirisendiri.Ukuran_2++

		if barunode.berikutnya == nil {
			dirisendiri.tail = barunode
		}
	}
}
func (dirisendiri *LinkedTabel) Getnodeat(indeks int) *TSimpul_daftar {
	if indeks < 0 || indeks >= dirisendiri.Ukuran_2 {
		return nil
	}
	var x *TSimpul_daftar = dirisendiri.head
	for i := 0; i < indeks; i++ {
		x = x.berikutnya
	}
	return x
}

func (dirisendiri *LinkedTabel) Aturnodeat(indeks int, acuan_alamat uintptr) {
	var x *TSimpul_daftar = dirisendiri.head
	for i := 0; i < indeks; i++ {
		x = x.berikutnya
	}
	if x != nil {
		x.acuan_alamat = acuan_alamat
	}
}
func (dirisendiri *LinkedTabel) Getat(indeks int) Pointer {
	simpul_daftar := dirisendiri.Getnodeat(indeks)
	if simpul_daftar == nil {
		return nil
	}
	var acuan_alamat uintptr = simpul_daftar.acuan_alamat
	return Pointer(acuan_alamat)
}
func (dirisendiri *LinkedTabel) Indeksdari(acuan_alamat uintptr) int {
	var n *TSimpul_daftar = dirisendiri.head
	i := 0
	for ; i < dirisendiri.Ukuran_2; i++ {
		if acuan_alamat == n.acuan_alamat {
			return i
		}
		n = n.berikutnya
	}
	return -1
}
func (dirisendiri *LinkedTabel) Buang(acuan_alamat uintptr) {
	indeks := dirisendiri.Indeksdari(acuan_alamat)
	if indeks < 0 {
		return
	}
	dirisendiri.Buangat(indeks)
}
func (dirisendiri *LinkedTabel) Buangat(indeks int) {
	if indeks < 0 || indeks >= dirisendiri.Ukuran_2 {
		return
	}
	simpul_daftar := dirisendiri.Getnodeat(indeks)
	if simpul_daftar == nil {
		return
	}
	if simpul_daftar.previous != nil {
		simpul_daftar.previous.berikutnya = simpul_daftar.berikutnya
	} else {
		dirisendiri.head = simpul_daftar.berikutnya
	}
	if simpul_daftar.berikutnya != nil {
		simpul_daftar.berikutnya.previous = simpul_daftar.previous
	} else {
		dirisendiri.tail = simpul_daftar.previous
	}
	dirisendiri.Ukuran_2 = dirisendiri.Ukuran_2 - 1

	if dirisendiri.mem != nil {
		dirisendiri.mem.Bebas(Pointer(simpul_daftar))
	}
}

var console_2 = TConsole{}

func (dirisendiri *LinkedTabel) Cetak() {
	console_2.MCetakxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(dirisendiri))))
	for i := 0; i < dirisendiri.Ukuran_2; i++ {
		simpul_daftar := (*TSimpul_daftar)(dirisendiri.Getat(i))
		console_2.MUnsignedinteger32Cetak(uint32(simpul_daftar.acuan_alamat))
		console_2.MCetak(":")
	}
}
