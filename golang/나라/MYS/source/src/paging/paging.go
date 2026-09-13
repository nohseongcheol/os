package paging

import unsafe "unsafe"
import . "sampuk"
import . "ingatanmanager"
import . "util"

type Halamandirektorientry_2 uintptr

const (
	HalamanHadir	uint32	= 0x001
	Halamanwritable	uint32	= 0x002
	HalamanPengguna	uint32	= 0x004
	HalamanBingkai	uint32	= 0xFFFFF000
	Halamancow	uint32	= 0x200
)

func Tetapkanbyteataddress(x byte, address uint32)
func Tetapkanunsignedinteger8ataddress(x uint8, address uint32)
func Tetapkanunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func tetapkancr3(direktori_halaman uint32)
func getcr3() uint32

type Paging struct {
	TSampukhandler
}
type TcowBingkaimanager struct {
	mem		*TIngatanmanager
	refs		[]uint16
	bingkaicount	uint32
}

var (
	Halamandirektorientry	uintptr
	HalamanJadualentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowBingkaimanager	TcowBingkaimanager
)

func (diri *TcowBingkaimanager) Init(mem *TIngatanmanager, bingkaicount uint32) bool {
	diri.mem = mem
	diri.bingkaicount = bingkaicount
	referenceBait := bingkaicount * uint32(unsafe.Sizeof(uint16(0)))
	referencePenuding := mem.Peruntukkan_ingatan(referenceBait)
	if referencePenuding == nil {
		diri.refs = nil
		diri.bingkaicount = 0
		return false
	}
	diri.refs = (*[1 << 28]uint16)(referencePenuding)[:bingkaicount:bingkaicount]
	for i := uint32(0); i < bingkaicount; i++ {
		diri.refs[i] = 0
	}
	return true
}

func (diri *TcowBingkaimanager) Reference(bingkai uint32) uint16 {
	idx := bingkai >> 12
	if idx >= diri.bingkaicount || diri.refs == nil {
		return 0
	}
	return diri.refs[idx]
}

func (diri *TcowBingkaimanager) Increment(bingkai uint32) {
	idx := bingkai >> 12
	if idx >= diri.bingkaicount || diri.refs == nil {
		return
	}
	if diri.refs[idx] == 0 {
		diri.refs[idx] = 2
	} else {
		diri.refs[idx]++
	}
}

func (diri *TcowBingkaimanager) Decrement(bingkai uint32) {
	idx := bingkai >> 12
	if idx >= diri.bingkaicount || diri.refs == nil || diri.refs[idx] == 0 {
		return
	}
	diri.refs[idx]--
}

func (diri *Paging) Init(halamandirektorientry uintptr, halamanJadualentry uint32, ingatanmanager *TIngatanmanager) {

	Halamandirektorientry = halamandirektorientry
	HalamanJadualentry = halamanJadualentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowBingkaimanager.Init(ingatanmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPenuding, _ := ingatanmanager.Alignedmalloc(0x1000)
			if addressPenuding == nil {
				return
			}
			address := uint32(uintptr(addressPenuding))

			Tetapkanunsignedinteger32ataddress(address|0x87, uint32(halamandirektorientry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Tetapkanunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		halamandirektorientry = halamandirektorientry + 0x1000
	}

}
func (diri *Paging) SharedIngatanregion() {

	halamandirektorientry := Halamandirektorientry
	kHalamandirektorientry := Halamandirektorientry

	for i := uint32(1); i <= virtlen; i++ {

		halamandirektorientry = halamandirektorientry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetNilai(uint32(kHalamandirektorientry) + pde*4)
			v = (v & 0xFFFFF000)
			Tetapkanunsignedinteger32ataddress(v|0x87, uint32(halamandirektorientry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetNilai(uint32(kHalamandirektorientry) + pde*4)
			v = (v & 0xFFFFF000)
			Tetapkanunsignedinteger32ataddress(v|0x87, uint32(halamandirektorientry)+pde*4)

		}

	}
}
func (diri *Paging) Halamanfault(manager *TSampukmanager) {
	sampukhandler = kendalipagingSampuk

	var address uintptr
	address = uintptr(unsafe.Pointer(&sampukhandler))
	diri.TSampukhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var sampukhandler func(uint32) uint32

func kendalipagingSampuk(esp uint32) uint32 {
	if ResolveSalinBukaTulisfault() {
		return esp
	}
	return KendalifatalSampukBingkai(esp, 0x0E)
}

func CloneaddressRuangcow(sumberHalamandirektori uint32) uint32 {
	if AktifIngatanmanager == nil || sumberHalamandirektori == 0 {
		return 0
	}
	destinationPenuding, _ := AktifIngatanmanager.Alignedmalloc(0x1000)
	if destinationPenuding == nil {
		return 0
	}
	destinationHalamandirektori := uint32(uintptr(destinationPenuding))
	for i := uint32(0); i < 1024; i++ {
		Tetapkanunsignedinteger32ataddress(0, destinationHalamandirektori+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sumberpdeaddress := sumberHalamandirektori + pde*4
		sumberpde := GetNilai(sumberpdeaddress)
		if (sumberpde & HalamanHadir) == 0 {
			continue
		}
		if issharedpde(pde) {
			Tetapkanunsignedinteger32ataddress(sumberpde, destinationHalamandirektori+pde*4)
			continue
		}

		destinationptPenuding, _ := AktifIngatanmanager.Alignedmalloc(0x1000)
		if destinationptPenuding == nil {
			continue
		}
		sumberpt := sumberpde & HalamanBingkai
		destinationpt := uint32(uintptr(destinationptPenuding))
		Tetapkanunsignedinteger32ataddress((destinationpt | (sumberpde & 0xFFF)), destinationHalamandirektori+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sumberpt + pte*4
			entry := GetNilai(pteaddress)
			if (entry & HalamanHadir) != 0 {
				if (entry & Halamanwritable) != 0 {
					entry = (entry &^ Halamanwritable) | Halamancow
					Tetapkanunsignedinteger32ataddress(entry, pteaddress)
					cowBingkaimanager.Increment(entry & HalamanBingkai)
				} else if (entry & Halamancow) != 0 {
					cowBingkaimanager.Increment(entry & HalamanBingkai)
				}
			}
			Tetapkanunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	muatSemulacr3()
	return destinationHalamandirektori
}

func ResolveSalinBukaTulisfault() bool {
	if AktifIngatanmanager == nil {
		return false
	}
	faultaddress := getcr2()
	direktori_halaman := getcr3()
	pdeaddress := direktori_halaman + ((faultaddress>>22)&0x3FF)*4
	pde := GetNilai(pdeaddress)
	if (pde & HalamanHadir) == 0 {
		return false
	}
	pt := pde & HalamanBingkai
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetNilai(pteaddress)
	if (pte&Halamancow) == 0 || (pte&HalamanHadir) == 0 {
		return false
	}
	oldBingkai := pte & HalamanBingkai
	if cowBingkaimanager.Reference(oldBingkai) <= 1 {
		Tetapkanunsignedinteger32ataddress((pte|Halamanwritable)&^Halamancow, pteaddress)
		muatSemulacr3()
		return true
	}

	baharuPenuding, _ := AktifIngatanmanager.Alignedmalloc(0x1000)
	if baharuPenuding == nil {
		return false
	}
	baharuBingkai := uint32(uintptr(baharuPenuding)) & HalamanBingkai

	sumber_2 := GetBaitfromPenuding(uintptr(faultaddress&HalamanBingkai), 0x1000, 0x1000)
	destination_2 := GetBaitfromPenuding(uintptr(baharuBingkai), 0x1000, 0x1000)
	copy(destination_2, sumber_2)
	cowBingkaimanager.Decrement(oldBingkai)
	Tetapkanunsignedinteger32ataddress((baharuBingkai|(pte&0xFFF)|Halamanwritable)&^Halamancow, pteaddress)
	muatSemulacr3()
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

func muatSemulacr3() {
	cr3 := getcr3()
	tetapkancr3(cr3)
}

func TetapkanbyteMasukHalamandirektori(x byte, address uint32, direktori_halaman uint32) {
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	Tetapkanbyteataddress(x, address)
	tetapkancr3(oldcr3)
}

func TetapkanBlokMasukHalamandirektori(sumber_2 []byte, destination_2 []byte, saiz uint32, direktori_halaman uint32) {
	if saiz == 0 || direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	makeJulatprivatewritableSemasa(direktori_halaman, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), saiz)

	for i := uint32(0); i < saiz; i++ {
		destination_2[i] = sumber_2[i]
	}
	tetapkancr3(oldcr3)
}

func ZeroBlokMasukHalamandirektori(address uint32, saiz uint32, direktori_halaman uint32) {
	if saiz == 0 || direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	makeJulatprivatewritableSemasa(direktori_halaman, address, saiz)
	destination_2 := GetBaitfromPenuding(uintptr(address), int(saiz), int(saiz))
	for i := uint32(0); i < saiz; i++ {
		destination_2[i] = 0
	}
	tetapkancr3(oldcr3)
}

func makeHalamanprivatewritableSemasa(direktori_halaman uint32, virtualaddress uint32) bool {
	pde := GetNilai(direktori_halaman + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & HalamanHadir) == 0 {
		return false
	}
	pteaddress := (pde & HalamanBingkai) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetNilai(pteaddress)
	if (pte & HalamanHadir) == 0 {
		return false
	}
	if (pte & Halamancow) == 0 {
		return (pte & Halamanwritable) != 0
	}
	if AktifIngatanmanager == nil {
		return false
	}
	baharuPenuding, _ := AktifIngatanmanager.Alignedmalloc(0x1000)
	if baharuPenuding == nil {
		return false
	}
	baharuBingkai := uint32(uintptr(baharuPenuding)) & HalamanBingkai
	sumber_2 := GetBaitfromPenuding(uintptr(virtualaddress&HalamanBingkai), 0x1000, 0x1000)
	destination_2 := GetBaitfromPenuding(uintptr(baharuBingkai), 0x1000, 0x1000)
	copy(destination_2, sumber_2)
	cowBingkaimanager.Decrement(pte & HalamanBingkai)
	Tetapkanunsignedinteger32ataddress((baharuBingkai|(pte&0xFFF)|Halamanwritable)&^Halamancow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	muatSemulacr3()
	return true
}

func makeJulatprivatewritableSemasa(direktori_halaman uint32, address uint32, saiz uint32) bool {
	if saiz == 0 {
		return true
	}
	terakhir := address + saiz - 1
	if terakhir < address {
		return false
	}
	for halaman := address & HalamanBingkai; ; halaman += 0x1000 {
		if !makeHalamanprivatewritableSemasa(direktori_halaman, halaman) {
			return false
		}
		if halaman == (terakhir & HalamanBingkai) {
			break
		}
	}
	return true
}

func MakeJulatprivatewritable(direktori_halaman uint32, address uint32, saiz uint32) bool {
	if direktori_halaman == 0 {
		return false
	}
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	ok := makeJulatprivatewritableSemasa(direktori_halaman, address, saiz)
	tetapkancr3(oldcr3)
	return ok
}

func Tetapkanunsignedinteger32MasukHalamandirektori(x uint32, address uint32, direktori_halaman uint32) {
	if direktori_halaman == 0 {
		return
	}
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	Tetapkanunsignedinteger32ataddress(x, address)
	tetapkancr3(oldcr3)
}

func GetNilai(address uint32) uint32 {
	var orgNilai uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgNilai
}
func GetNilaiMasukHalamandirektori(address uint32, direktori_halaman uint32) uint32 {
	if direktori_halaman == 0 {
		return 0
	}
	oldcr3 := getcr3()
	tetapkancr3(direktori_halaman)
	v := GetNilai(address)
	tetapkancr3(oldcr3)
	return v
}

var v uint32 = 0

func SalinHalamanBingkaiBlok(xHalamandirektori uint32, yHalamandirektori uint32, vaddress uint32) {
	if xHalamandirektori == 0 || yHalamandirektori == 0 {
		return
	}
	oldcr3 := getcr3()
	tetapkancr3(xHalamandirektori)
	v = GetNilai(vaddress)
	Tetapkanunsignedinteger32MasukHalamandirektori(v, vaddress, yHalamandirektori)

	tetapkancr3(oldcr3)
}
