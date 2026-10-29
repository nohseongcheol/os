/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package senarai

import . "unsafe"
import . "console"
import mem "ingatanmanager"

type TNod_senarai struct {
	rujukan_alamat	uintptr
	previous	*TNod_senarai
	berikutnya	*TNod_senarai
}

type LinkedSenarai struct {
	head	*TNod_senarai
	tail	*TNod_senarai
	Saiz_2	int

	mem	*mem.TIngatanmanager
}

func (diri *LinkedSenarai) Init(mem *mem.TIngatanmanager) {
	diri.head = nil
	diri.tail = nil
	diri.Saiz_2 = 0

	diri.mem = mem
}
func (diri *LinkedSenarai) Tambah_di_awal_senarai(rujukan_alamat uintptr) {
	baharuNod := (*TNod_senarai)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(TNod_senarai{}))))
	if baharuNod == nil {
		return
	}
	baharuNod.rujukan_alamat = rujukan_alamat
	baharuNod.previous = nil
	baharuNod.berikutnya = diri.head
	if diri.head != nil {
		diri.head.previous = baharuNod
	}
	diri.head = baharuNod
	diri.Saiz_2++

	if diri.head.berikutnya == nil {
		diri.tail = diri.head
	}

}
func (diri *LinkedSenarai) Tambah_di_hujung_senarai(rujukan_alamat uintptr) {
	if diri.Saiz_2 == 0 {
		diri.Tambah_di_awal_senarai(rujukan_alamat)
	} else {
		baharuNod := (*TNod_senarai)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(TNod_senarai{}))))
		if baharuNod == nil {
			return
		}
		baharuNod.rujukan_alamat = rujukan_alamat
		baharuNod.previous = diri.tail
		baharuNod.berikutnya = nil
		diri.tail.berikutnya = baharuNod
		diri.tail = baharuNod
		diri.Saiz_2++
	}
}
func (diri *LinkedSenarai) Sisip_pada_indeks(indeks int, rujukan_alamat uintptr) {
	if indeks == 0 {
		diri.Tambah_di_awal_senarai(rujukan_alamat)
	} else {
		previousNod := diri.GetNodat(indeks - 1)
		berikutnyaNod := previousNod.berikutnya
		baharuNod := (*TNod_senarai)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(TNod_senarai{}))))
		if baharuNod == nil {
			return
		}
		baharuNod.rujukan_alamat = rujukan_alamat

		previousNod.berikutnya = baharuNod
		baharuNod.previous = previousNod
		baharuNod.berikutnya = berikutnyaNod
		if berikutnyaNod != nil {
			berikutnyaNod.previous = baharuNod
		}

		diri.Saiz_2++

		if baharuNod.berikutnya == nil {
			diri.tail = baharuNod
		}
	}
}
func (diri *LinkedSenarai) GetNodat(indeks int) *TNod_senarai {
	if indeks < 0 || indeks >= diri.Saiz_2 {
		return nil
	}
	var x *TNod_senarai = diri.head
	for i := 0; i < indeks; i++ {
		x = x.berikutnya
	}
	return x
}

func (diri *LinkedSenarai) TetapkanNodat(indeks int, rujukan_alamat uintptr) {
	var x *TNod_senarai = diri.head
	for i := 0; i < indeks; i++ {
		x = x.berikutnya
	}
	if x != nil {
		x.rujukan_alamat = rujukan_alamat
	}
}
func (diri *LinkedSenarai) Getat(indeks int) Pointer {
	nod_senarai := diri.GetNodat(indeks)
	if nod_senarai == nil {
		return nil
	}
	var rujukan_alamat uintptr = nod_senarai.rujukan_alamat
	return Pointer(rujukan_alamat)
}
func (diri *LinkedSenarai) Indeksdari(rujukan_alamat uintptr) int {
	var n *TNod_senarai = diri.head
	i := 0
	for ; i < diri.Saiz_2; i++ {
		if rujukan_alamat == n.rujukan_alamat {
			return i
		}
		n = n.berikutnya
	}
	return -1
}
func (diri *LinkedSenarai) Buang(rujukan_alamat uintptr) {
	indeks := diri.Indeksdari(rujukan_alamat)
	if indeks < 0 {
		return
	}
	diri.Buangat(indeks)
}
func (diri *LinkedSenarai) Buangat(indeks int) {
	if indeks < 0 || indeks >= diri.Saiz_2 {
		return
	}
	nod_senarai := diri.GetNodat(indeks)
	if nod_senarai == nil {
		return
	}
	if nod_senarai.previous != nil {
		nod_senarai.previous.berikutnya = nod_senarai.berikutnya
	} else {
		diri.head = nod_senarai.berikutnya
	}
	if nod_senarai.berikutnya != nil {
		nod_senarai.berikutnya.previous = nod_senarai.previous
	} else {
		diri.tail = nod_senarai.previous
	}
	diri.Saiz_2 = diri.Saiz_2 - 1

	if diri.mem != nil {
		diri.mem.Bebas(Pointer(nod_senarai))
	}
}

var console_2 = TConsole{}

func (diri *LinkedSenarai) Cetak() {
	console_2.MCetakxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(diri))))
	for i := 0; i < diri.Saiz_2; i++ {
		nod_senarai := (*TNod_senarai)(diri.Getat(i))
		console_2.MUnsignedinteger32Cetak(uint32(nod_senarai.rujukan_alamat))
		console_2.MCetak(":")
	}
}
