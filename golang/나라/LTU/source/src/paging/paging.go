package paging

import unsafe "unsafe"
import . "pertraukimas"
import . "atmintismanager"
import . "util"

type Puslapiskatalogasįrašas_2 uintptr

const (
	PuslapisYra		uint32	= 0x001
	Puslapiswritable	uint32	= 0x002
	PuslapisNaudotojas	uint32	= 0x004
	PuslapisKadras		uint32	= 0xFFFFF000
	Puslapiscow		uint32	= 0x200
)

func Nustatytabyteataddress(x byte, address uint32)
func Nustatytaunsignedinteger8ataddress(x uint8, address uint32)
func Nustatytaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func nustatytacr3(puslapiskatalogas uint32)
func getcr3() uint32

type Paging struct {
	TPertraukimashandler
}
type TcowKadrasmanager struct {
	mem		*TAtmintismanager
	refs		[]uint16
	kadrascount	uint32
}

var (
	Puslapiskatalogasįrašas	uintptr
	PuslapisLentelėįrašas	uint32
	pdelen			uint32
	virtlen			uint32
	cowKadrasmanager	TcowKadrasmanager
)

func (self *TcowKadrasmanager) Init(mem *TAtmintismanager, kadrascount uint32) bool {
	self.mem = mem
	self.kadrascount = kadrascount
	referenceBaitų := kadrascount * uint32(unsafe.Sizeof(uint16(0)))
	referenceRodyklė := mem.Malloc(referenceBaitų)
	if referenceRodyklė == nil {
		self.refs = nil
		self.kadrascount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceRodyklė)[:kadrascount:kadrascount]
	for i := uint32(0); i < kadrascount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowKadrasmanager) Reference(kadras uint32) uint16 {
	idx := kadras >> 12
	if idx >= self.kadrascount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowKadrasmanager) Increment(kadras uint32) {
	idx := kadras >> 12
	if idx >= self.kadrascount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowKadrasmanager) Decrement(kadras uint32) {
	idx := kadras >> 12
	if idx >= self.kadrascount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(puslapiskatalogasįrašas uintptr, puslapisLentelėįrašas uint32, atmintismanager *TAtmintismanager) {

	Puslapiskatalogasįrašas = puslapiskatalogasįrašas
	PuslapisLentelėįrašas = puslapisLentelėįrašas

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowKadrasmanager.Init(atmintismanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressRodyklė, _ := atmintismanager.Alignedmalloc(0x1000)
			if addressRodyklė == nil {
				return
			}
			address := uint32(uintptr(addressRodyklė))

			Nustatytaunsignedinteger32ataddress(address|0x87, uint32(puslapiskatalogasįrašas)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Nustatytaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		puslapiskatalogasįrašas = puslapiskatalogasįrašas + 0x1000
	}

}
func (self *Paging) SharedAtmintisregion() {

	puslapiskatalogasįrašas := Puslapiskatalogasįrašas
	kPuslapiskatalogasįrašas := Puslapiskatalogasįrašas

	for i := uint32(1); i <= virtlen; i++ {

		puslapiskatalogasįrašas = puslapiskatalogasįrašas + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetReikšmė(uint32(kPuslapiskatalogasįrašas) + pde*4)
			v = (v & 0xFFFFF000)
			Nustatytaunsignedinteger32ataddress(v|0x87, uint32(puslapiskatalogasįrašas)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetReikšmė(uint32(kPuslapiskatalogasįrašas) + pde*4)
			v = (v & 0xFFFFF000)
			Nustatytaunsignedinteger32ataddress(v|0x87, uint32(puslapiskatalogasįrašas)+pde*4)

		}

	}
}
func (self *Paging) Puslapisfault(manager *TPertraukimasmanager) {
	pertraukimashandler = pozicijapagingPertraukimas

	var address uintptr
	address = uintptr(unsafe.Pointer(&pertraukimashandler))
	self.TPertraukimashandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var pertraukimashandler func(uint32) uint32

func pozicijapagingPertraukimas(esp uint32) uint32 {
	if ResolveKopijuotiĮjungtaRašymasfault() {
		return esp
	}
	return PozicijafatalPertraukimasKadras(esp, 0x0E)
}

func CloneaddressTarpascow(šaltinisPuslapiskatalogas uint32) uint32 {
	if AktyvusAtmintismanager == nil || šaltinisPuslapiskatalogas == 0 {
		return 0
	}
	tikslasRodyklė, _ := AktyvusAtmintismanager.Alignedmalloc(0x1000)
	if tikslasRodyklė == nil {
		return 0
	}
	tikslasPuslapiskatalogas := uint32(uintptr(tikslasRodyklė))
	for i := uint32(0); i < 1024; i++ {
		Nustatytaunsignedinteger32ataddress(0, tikslasPuslapiskatalogas+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		šaltinispdeaddress := šaltinisPuslapiskatalogas + pde*4
		šaltinispde := GetReikšmė(šaltinispdeaddress)
		if (šaltinispde & PuslapisYra) == 0 {
			continue
		}
		if issharedpde(pde) {
			Nustatytaunsignedinteger32ataddress(šaltinispde, tikslasPuslapiskatalogas+pde*4)
			continue
		}

		tikslasptRodyklė, _ := AktyvusAtmintismanager.Alignedmalloc(0x1000)
		if tikslasptRodyklė == nil {
			continue
		}
		šaltinispt := šaltinispde & PuslapisKadras
		tikslaspt := uint32(uintptr(tikslasptRodyklė))
		Nustatytaunsignedinteger32ataddress((tikslaspt | (šaltinispde & 0xFFF)), tikslasPuslapiskatalogas+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := šaltinispt + pte*4
			įrašas := GetReikšmė(pteaddress)
			if (įrašas & PuslapisYra) != 0 {
				if (įrašas & Puslapiswritable) != 0 {
					įrašas = (įrašas &^ Puslapiswritable) | Puslapiscow
					Nustatytaunsignedinteger32ataddress(įrašas, pteaddress)
					cowKadrasmanager.Increment(įrašas & PuslapisKadras)
				} else if (įrašas & Puslapiscow) != 0 {
					cowKadrasmanager.Increment(įrašas & PuslapisKadras)
				}
			}
			Nustatytaunsignedinteger32ataddress(įrašas, tikslaspt+pte*4)
		}
	}
	įkeltiišnaujocr3()
	return tikslasPuslapiskatalogas
}

func ResolveKopijuotiĮjungtaRašymasfault() bool {
	if AktyvusAtmintismanager == nil {
		return false
	}
	faultaddress := getcr2()
	puslapiskatalogas := getcr3()
	pdeaddress := puslapiskatalogas + ((faultaddress>>22)&0x3FF)*4
	pde := GetReikšmė(pdeaddress)
	if (pde & PuslapisYra) == 0 {
		return false
	}
	pt := pde & PuslapisKadras
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetReikšmė(pteaddress)
	if (pte&Puslapiscow) == 0 || (pte&PuslapisYra) == 0 {
		return false
	}
	oldKadras := pte & PuslapisKadras
	if cowKadrasmanager.Reference(oldKadras) <= 1 {
		Nustatytaunsignedinteger32ataddress((pte|Puslapiswritable)&^Puslapiscow, pteaddress)
		įkeltiišnaujocr3()
		return true
	}

	naujasRodyklė, _ := AktyvusAtmintismanager.Alignedmalloc(0x1000)
	if naujasRodyklė == nil {
		return false
	}
	naujasKadras := uint32(uintptr(naujasRodyklė)) & PuslapisKadras

	šaltinis_2 := GetBaitųfromRodyklė(uintptr(faultaddress&PuslapisKadras), 0x1000, 0x1000)
	tikslas_2 := GetBaitųfromRodyklė(uintptr(naujasKadras), 0x1000, 0x1000)
	copy(tikslas_2, šaltinis_2)
	cowKadrasmanager.Decrement(oldKadras)
	Nustatytaunsignedinteger32ataddress((naujasKadras|(pte&0xFFF)|Puslapiswritable)&^Puslapiscow, pteaddress)
	įkeltiišnaujocr3()
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

func įkeltiišnaujocr3() {
	cr3 := getcr3()
	nustatytacr3(cr3)
}

func NustatytabyteĮPuslapiskatalogas(x byte, address uint32, puslapiskatalogas uint32) {
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	Nustatytabyteataddress(x, address)
	nustatytacr3(oldcr3)
}

func NustatytaBlokasĮPuslapiskatalogas(šaltinis_2 []byte, tikslas_2 []byte, dydis uint32, puslapiskatalogas uint32) {
	if dydis == 0 || puslapiskatalogas == 0 {
		return
	}
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	makeSritisPrivatuswritableDabartinis(puslapiskatalogas, uint32(uintptr(unsafe.Pointer(&tikslas_2[0]))), dydis)

	for i := uint32(0); i < dydis; i++ {
		tikslas_2[i] = šaltinis_2[i]
	}
	nustatytacr3(oldcr3)
}

func NulisBlokasĮPuslapiskatalogas(address uint32, dydis uint32, puslapiskatalogas uint32) {
	if dydis == 0 || puslapiskatalogas == 0 {
		return
	}
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	makeSritisPrivatuswritableDabartinis(puslapiskatalogas, address, dydis)
	tikslas_2 := GetBaitųfromRodyklė(uintptr(address), int(dydis), int(dydis))
	for i := uint32(0); i < dydis; i++ {
		tikslas_2[i] = 0
	}
	nustatytacr3(oldcr3)
}

func makePuslapisPrivatuswritableDabartinis(puslapiskatalogas uint32, virtualiaddress uint32) bool {
	pde := GetReikšmė(puslapiskatalogas + ((virtualiaddress>>22)&0x3FF)*4)
	if (pde & PuslapisYra) == 0 {
		return false
	}
	pteaddress := (pde & PuslapisKadras) + ((virtualiaddress>>12)&0x3FF)*4
	pte := GetReikšmė(pteaddress)
	if (pte & PuslapisYra) == 0 {
		return false
	}
	if (pte & Puslapiscow) == 0 {
		return (pte & Puslapiswritable) != 0
	}
	if AktyvusAtmintismanager == nil {
		return false
	}
	naujasRodyklė, _ := AktyvusAtmintismanager.Alignedmalloc(0x1000)
	if naujasRodyklė == nil {
		return false
	}
	naujasKadras := uint32(uintptr(naujasRodyklė)) & PuslapisKadras
	šaltinis_2 := GetBaitųfromRodyklė(uintptr(virtualiaddress&PuslapisKadras), 0x1000, 0x1000)
	tikslas_2 := GetBaitųfromRodyklė(uintptr(naujasKadras), 0x1000, 0x1000)
	copy(tikslas_2, šaltinis_2)
	cowKadrasmanager.Decrement(pte & PuslapisKadras)
	Nustatytaunsignedinteger32ataddress((naujasKadras|(pte&0xFFF)|Puslapiswritable)&^Puslapiscow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	įkeltiišnaujocr3()
	return true
}

func makeSritisPrivatuswritableDabartinis(puslapiskatalogas uint32, address uint32, dydis uint32) bool {
	if dydis == 0 {
		return true
	}
	paskutinis := address + dydis - 1
	if paskutinis < address {
		return false
	}
	for puslapis := address & PuslapisKadras; ; puslapis += 0x1000 {
		if !makePuslapisPrivatuswritableDabartinis(puslapiskatalogas, puslapis) {
			return false
		}
		if puslapis == (paskutinis & PuslapisKadras) {
			break
		}
	}
	return true
}

func MakeSritisPrivatuswritable(puslapiskatalogas uint32, address uint32, dydis uint32) bool {
	if puslapiskatalogas == 0 {
		return false
	}
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	gerai := makeSritisPrivatuswritableDabartinis(puslapiskatalogas, address, dydis)
	nustatytacr3(oldcr3)
	return gerai
}

func Nustatytaunsignedinteger32ĮPuslapiskatalogas(x uint32, address uint32, puslapiskatalogas uint32) {
	if puslapiskatalogas == 0 {
		return
	}
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	Nustatytaunsignedinteger32ataddress(x, address)
	nustatytacr3(oldcr3)
}

func GetReikšmė(address uint32) uint32 {
	var orgReikšmė uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgReikšmė
}
func GetReikšmėĮPuslapiskatalogas(address uint32, puslapiskatalogas uint32) uint32 {
	if puslapiskatalogas == 0 {
		return 0
	}
	oldcr3 := getcr3()
	nustatytacr3(puslapiskatalogas)
	v := GetReikšmė(address)
	nustatytacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopijuotiPuslapisKadrasBlokas(xPuslapiskatalogas uint32, yPuslapiskatalogas uint32, vaddress uint32) {
	if xPuslapiskatalogas == 0 || yPuslapiskatalogas == 0 {
		return
	}
	oldcr3 := getcr3()
	nustatytacr3(xPuslapiskatalogas)
	v = GetReikšmė(vaddress)
	Nustatytaunsignedinteger32ĮPuslapiskatalogas(v, vaddress, yPuslapiskatalogas)

	nustatytacr3(oldcr3)
}
