/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interupsi"
import . "memorimanager"
import . "util"

type HalamanDirektorientri_2 uintptr

const (
	HalamanAda	uint32	= 0x001
	Halamanwritable	uint32	= 0x002
	HalamanPengguna	uint32	= 0x004
	HalamanBingkai	uint32	= 0xFFFFF000
	Halamancow	uint32	= 0x200
)

func Aturbyteataddress(x byte, address uint32)
func Aturunsignedinteger8ataddress(x uint8, address uint32)
func Aturunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func aturcr3(direktori_halaman uint32)
func getcr3() uint32

type Paging struct {
	TInterupsihandler
}
type TcowBingkaimanager struct {
	mem		*TMemorimanager
	refs		[]uint16
	bingkaicount	uint32
}

var (
	HalamanDirektorientri	uintptr
	HalamanTabelentri	uint32
	pdelen			uint32
	virtlen			uint32
	cowBingkaimanager	TcowBingkaimanager
)

func (dirisendiri *TcowBingkaimanager) Init(mem *TMemorimanager, bingkaicount uint32) bool {
	dirisendiri.mem = mem
	dirisendiri.bingkaicount = bingkaicount
	referenceByte := bingkaicount * uint32(unsafe.Sizeof(uint16(0)))
	referencePenunjuk := mem.Alokasikan_memori(referenceByte)
	if referencePenunjuk == nil {
		dirisendiri.refs = nil
		dirisendiri.bingkaicount = 0
		return false
	}
	dirisendiri.refs = (*[1 << 28]uint16)(referencePenunjuk)[:bingkaicount:bingkaicount]
	for i := uint32(0); i < bingkaicount; i++ {
		dirisendiri.refs[i] = 0
	}
	return true
}

func (dirisendiri *TcowBingkaimanager) Reference(bingkai uint32) uint16 {
	idx := bingkai >> 12
	if idx >= dirisendiri.bingkaicount || dirisendiri.refs == nil {
		return 0
	}
	return dirisendiri.refs[idx]
}

func (dirisendiri *TcowBingkaimanager) Increment(bingkai uint32) {
	idx := bingkai >> 12
	if idx >= dirisendiri.bingkaicount || dirisendiri.refs == nil {
		return
	}
	if dirisendiri.refs[idx] == 0 {
		dirisendiri.refs[idx] = 2
	} else {
		dirisendiri.refs[idx]++
	}
}

func (dirisendiri *TcowBingkaimanager) Decrement(bingkai uint32) {
	idx := bingkai >> 12
	if idx >= dirisendiri.bingkaicount || dirisendiri.refs == nil || dirisendiri.refs[idx] == 0 {
		return
	}
	dirisendiri.refs[idx]--
}

func (dirisendiri *Paging) Init(halamanDirektorientri uintptr, halamanTabelentri uint32, memorimanager *TMemorimanager) {

	HalamanDirektorientri = halamanDirektorientri
	HalamanTabelentri = halamanTabelentri

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowBingkaimanager.Init(memorimanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPenunjuk, _ := memorimanager.Alignedmalloc(0x1000)
			if addressPenunjuk == nil {
				return
			}
			address := uint32(uintptr(addressPenunjuk))

			Aturunsignedinteger32ataddress(address|0x87, uint32(halamanDirektorientri)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Aturunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		halamanDirektorientri = halamanDirektorientri + 0x1000
	}

}
func (dirisendiri *Paging) SharedMemoriregion() {

	halamanDirektorientri := HalamanDirektorientri
	kHalamanDirektorientri := HalamanDirektorientri

	for i := uint32(1); i <= virtlen; i++ {

		halamanDirektorientri = halamanDirektorientri + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetNilai(uint32(kHalamanDirektorientri) + pde*4)
			v = (v & 0xFFFFF000)
			Aturunsignedinteger32ataddress(v|0x87, uint32(halamanDirektorientri)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetNilai(uint32(kHalamanDirektorientri) + pde*4)
			v = (v & 0xFFFFF000)
			Aturunsignedinteger32ataddress(v|0x87, uint32(halamanDirektorientri)+pde*4)

		}

	}
}
func (dirisendiri *Paging) Halamanfault(manager *TInterupsimanager) {
	interupsihandler = penangananpagingInterupsi

	var address uintptr
	address = uintptr(unsafe.Pointer(&interupsihandler))
	dirisendiri.TInterupsihandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interupsihandler func(uint32) uint32

func penangananpagingInterupsi(esp uint32) uint32 {
	if ResolveSalinHidupTulisfault() {
		return esp
	}
	return PenangananfatalInterupsiBingkai(esp, 0x0E)
}

func CloneaddressSpasicow(sumberHalamanDirektori uint32) uint32 {
	if AktifMemorimanager == nil || sumberHalamanDirektori == 0 {
		return 0
	}
	tujuanPenunjuk, _ := AktifMemorimanager.Alignedmalloc(0x1000)
	if tujuanPenunjuk == nil {
		return 0
	}
	tujuanHalamanDirektori := uint32(uintptr(tujuanPenunjuk))
	for i := uint32(0); i < 1024; i++ {
		Aturunsignedinteger32ataddress(0, tujuanHalamanDirektori+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sumberpdeaddress := sumberHalamanDirektori + pde*4
		sumberpde := GetNilai(sumberpdeaddress)
		if (sumberpde & HalamanAda) == 0 {
			continue
		}
		if issharedpde(pde) {
			Aturunsignedinteger32ataddress(sumberpde, tujuanHalamanDirektori+pde*4)
			continue
		}

		tujuanptPenunjuk, _ := AktifMemorimanager.Alignedmalloc(0x1000)
		if tujuanptPenunjuk == nil {
			continue
		}
		sumberpt := sumberpde & HalamanBingkai
		tujuanpt := uint32(uintptr(tujuanptPenunjuk))
		Aturunsignedinteger32ataddress((tujuanpt | (sumberpde & 0xFFF)), tujuanHalamanDirektori+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sumberpt + pte*4
			entri := GetNilai(pteaddress)
			if (entri & HalamanAda) != 0 {
				if (entri & Halamanwritable) != 0 {
					entri = (entri &^ Halamanwritable) | Halamancow
					Aturunsignedinteger32ataddress(entri, pteaddress)
					cowBingkaimanager.Increment(entri & HalamanBingkai)
				} else if (entri & Halamancow) != 0 {
					cowBingkaimanager.Increment(entri & HalamanBingkai)
				}
			}
			Aturunsignedinteger32ataddress(entri, tujuanpt+pte*4)
		}
	}
	muatUlangcr3()
	return tujuanHalamanDirektori
}

func ResolveSalinHidupTulisfault() bool {
	if AktifMemorimanager == nil {
		return false
	}
	faultaddress := getcr2()
	direktori_halaman := getcr3()
	pdeaddress := direktori_halaman + ((faultaddress>>22)&0x3FF)*4
	pde := GetNilai(pdeaddress)
	if (pde & HalamanAda) == 0 {
		return false
	}
	pt := pde & HalamanBingkai
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetNilai(pteaddress)
	if (pte&Halamancow) == 0 || (pte&HalamanAda) == 0 {
		return false
	}
	oldBingkai := pte & HalamanBingkai
	if cowBingkaimanager.Reference(oldBingkai) <= 1 {
		Aturunsignedinteger32ataddress((pte|Halamanwritable)&^Halamancow, pteaddress)
		muatUlangcr3()
		return true
	}

	baruPenunjuk, _ := AktifMemorimanager.Alignedmalloc(0x1000)
	if baruPenunjuk == nil {
		return false
	}
	baruBingkai := uint32(uintptr(baruPenunjuk)) & HalamanBingkai

	sumber_2 := GetBytefromPenunjuk(uintptr(faultaddress&HalamanBingkai), 0x1000, 0x1000)
	tujuan_2 := GetBytefromPenunjuk(uintptr(baruBingkai), 0x1000, 0x1000)
	copy(tujuan_2, sumber_2)
	cowBingkaimanager.Decrement(oldBingkai)
	Aturunsignedinteger32ataddress((baruBingkai|(pte&0xFFF)|Halamanwritable)&^Halamancow, pteaddress)
	muatUlangcr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func muatUlangcr3() {
	cr3 := getcr3()
	aturcr3(cr3)
}

func AturbyteMasukHalamanDirektori(x byte, address uint32, direktori_halaman uint32) {
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	Aturbyteataddress(x, address)
	aturcr3(oldcr3)
}

func AturBlokMasukHalamanDirektori(sumber_2 []byte, tujuan_2 []byte, ukuran uint32, direktori_halaman uint32) {
	if ukuran == 0 || direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	makeCakupanprivatewritableSekarang(direktori_halaman, uint32(uintptr(unsafe.Pointer(&tujuan_2[0]))), ukuran)

	for i := uint32(0); i < ukuran; i++ {
		tujuan_2[i] = sumber_2[i]
	}
	aturcr3(oldcr3)
}

func NolBlokMasukHalamanDirektori(address uint32, ukuran uint32, direktori_halaman uint32) {
	if ukuran == 0 || direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	makeCakupanprivatewritableSekarang(direktori_halaman, address, ukuran)
	tujuan_2 := GetBytefromPenunjuk(uintptr(address), int(ukuran), int(ukuran))
	for i := uint32(0); i < ukuran; i++ {
		tujuan_2[i] = 0
	}
	aturcr3(oldcr3)
}

func makeHalamanprivatewritableSekarang(direktori_halaman uint32, virtualaddress uint32) bool {
	pde := GetNilai(direktori_halaman + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & HalamanAda) == 0 {
		return false
	}
	pteaddress := (pde & HalamanBingkai) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetNilai(pteaddress)
	if (pte & HalamanAda) == 0 {
		return false
	}
	if (pte & Halamancow) == 0 {
		return (pte & Halamanwritable) != 0
	}
	if AktifMemorimanager == nil {
		return false
	}
	baruPenunjuk, _ := AktifMemorimanager.Alignedmalloc(0x1000)
	if baruPenunjuk == nil {
		return false
	}
	baruBingkai := uint32(uintptr(baruPenunjuk)) & HalamanBingkai
	sumber_2 := GetBytefromPenunjuk(uintptr(virtualaddress&HalamanBingkai), 0x1000, 0x1000)
	tujuan_2 := GetBytefromPenunjuk(uintptr(baruBingkai), 0x1000, 0x1000)
	copy(tujuan_2, sumber_2)
	cowBingkaimanager.Decrement(pte & HalamanBingkai)
	Aturunsignedinteger32ataddress((baruBingkai|(pte&0xFFF)|Halamanwritable)&^Halamancow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	muatUlangcr3()
	return true
}

func makeCakupanprivatewritableSekarang(direktori_halaman uint32, address uint32, ukuran uint32) bool {
	if ukuran == 0 {
		return true
	}
	terakhir := address + ukuran - 1
	if terakhir < address {
		return false
	}
	for halaman := address & HalamanBingkai; ; halaman += 0x1000 {
		if !makeHalamanprivatewritableSekarang(direktori_halaman, halaman) {
			return false
		}
		if halaman == (terakhir & HalamanBingkai) {
			break
		}
	}
	return true
}

func MakeCakupanprivatewritable(direktori_halaman uint32, address uint32, ukuran uint32) bool {
	if direktori_halaman == 0 {
		return false
	}
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	oke := makeCakupanprivatewritableSekarang(direktori_halaman, address, ukuran)
	aturcr3(oldcr3)
	return oke
}

func Aturunsignedinteger32MasukHalamanDirektori(x uint32, address uint32, direktori_halaman uint32) {
	if direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	Aturunsignedinteger32ataddress(x, address)
	aturcr3(oldcr3)
}

func GetNilai(address uint32) uint32 {
	var orgNilai uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgNilai
}
func GetNilaiMasukHalamanDirektori(address uint32, direktori_halaman uint32) uint32 {
	if direktori_halaman == 0 {
		return 0
	}
	oldcr3 := getcr3()
	aturcr3(direktori_halaman)
	v := GetNilai(address)
	aturcr3(oldcr3)
	return v
}

var v uint32 = 0

func SalinHalamanBingkaiBlok(xHalamanDirektori uint32, yHalamanDirektori uint32, vaddress uint32) {
	if xHalamanDirektori == 0 || yHalamanDirektori == 0 {
		return
	}
	oldcr3 := getcr3()
	aturcr3(xHalamanDirektori)
	v = GetNilai(vaddress)
	Aturunsignedinteger32MasukHalamanDirektori(v, vaddress, yHalamanDirektori)

	aturcr3(oldcr3)
}
