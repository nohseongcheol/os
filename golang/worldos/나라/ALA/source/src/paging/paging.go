/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "avbrott"
import . "minnemanager"
import . "util"

type SidaKatalogpost_2 uintptr

const (
	SidaAnsluten	uint32	= 0x001
	Sidawritable	uint32	= 0x002
	SidaAnvändare	uint32	= 0x004
	SidaRam		uint32	= 0xFFFFF000
	Sidacow		uint32	= 0x200
)

func MängdbyteatAdress(x byte, adress uint32)
func Mängdunsignedinteger8atAdress(x uint8, adress uint32)
func Mängdunsignedinteger32atAdress(x uint32, adress uint32)

func getcr2() uint32

func mängdcr3(sidkatalog uint32)
func getcr3() uint32

type Paging struct {
	TAvbrotthandler
}
type TcowRammanager struct {
	mem		*TMinnemanager
	refs		[]uint16
	ramAntal	uint32
}

var (
	SidaKatalogpost	uintptr
	SidaTabellpost	uint32
	pdelen		uint32
	virtlen		uint32
	cowRammanager	TcowRammanager
)

func (själv *TcowRammanager) Init(mem *TMinnemanager, ramAntal uint32) bool {
	själv.mem = mem
	själv.ramAntal = ramAntal
	referenceByte := ramAntal * uint32(unsafe.Sizeof(uint16(0)))
	referenceMuspekare := mem.Tilldela_minne(referenceByte)
	if referenceMuspekare == nil {
		själv.refs = nil
		själv.ramAntal = 0
		return false
	}
	själv.refs = (*[1 << 28]uint16)(referenceMuspekare)[:ramAntal:ramAntal]
	for i := uint32(0); i < ramAntal; i++ {
		själv.refs[i] = 0
	}
	return true
}

func (själv *TcowRammanager) Reference(ram uint32) uint16 {
	idx := ram >> 12
	if idx >= själv.ramAntal || själv.refs == nil {
		return 0
	}
	return själv.refs[idx]
}

func (själv *TcowRammanager) Increment(ram uint32) {
	idx := ram >> 12
	if idx >= själv.ramAntal || själv.refs == nil {
		return
	}
	if själv.refs[idx] == 0 {
		själv.refs[idx] = 2
	} else {
		själv.refs[idx]++
	}
}

func (själv *TcowRammanager) Decrement(ram uint32) {
	idx := ram >> 12
	if idx >= själv.ramAntal || själv.refs == nil || själv.refs[idx] == 0 {
		return
	}
	själv.refs[idx]--
}

func (själv *Paging) Init(sidaKatalogpost uintptr, sidaTabellpost uint32, minnemanager *TMinnemanager) {

	SidaKatalogpost = sidaKatalogpost
	SidaTabellpost = sidaTabellpost

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRammanager.Init(minnemanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			adressMuspekare, _ := minnemanager.Alignedmalloc(0x1000)
			if adressMuspekare == nil {
				return
			}
			adress := uint32(uintptr(adressMuspekare))

			Mängdunsignedinteger32atAdress(adress|0x87, uint32(sidaKatalogpost)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Mängdunsignedinteger32atAdress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, adress+pte*4)
			}
		}
		sidaKatalogpost = sidaKatalogpost + 0x1000
	}

}
func (själv *Paging) SharedMinneregion() {

	sidaKatalogpost := SidaKatalogpost
	kSidaKatalogpost := SidaKatalogpost

	for i := uint32(1); i <= virtlen; i++ {

		sidaKatalogpost = sidaKatalogpost + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVärde(uint32(kSidaKatalogpost) + pde*4)
			v = (v & 0xFFFFF000)
			Mängdunsignedinteger32atAdress(v|0x87, uint32(sidaKatalogpost)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVärde(uint32(kSidaKatalogpost) + pde*4)
			v = (v & 0xFFFFF000)
			Mängdunsignedinteger32atAdress(v|0x87, uint32(sidaKatalogpost)+pde*4)

		}

	}
}
func (själv *Paging) Sidafault(manager *TAvbrottmanager) {
	avbrotthandler = handtagpagingAvbrott

	var adress uintptr
	adress = uintptr(unsafe.Pointer(&avbrotthandler))
	själv.TAvbrotthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), adress)
}

var avbrotthandler func(uint32) uint32

func handtagpagingAvbrott(esp uint32) uint32 {
	if ResolveKopieraPåSkrivfault() {
		return esp
	}
	return HandtagfatalAvbrottRam(esp, 0x0E)
}

func CloneAdressMellanslagcow(källaSidaKatalog uint32) uint32 {
	if AktivMinnemanager == nil || källaSidaKatalog == 0 {
		return 0
	}
	målMuspekare, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if målMuspekare == nil {
		return 0
	}
	målSidaKatalog := uint32(uintptr(målMuspekare))
	for i := uint32(0); i < 1024; i++ {
		Mängdunsignedinteger32atAdress(0, målSidaKatalog+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		källapdeAdress := källaSidaKatalog + pde*4
		källapde := GetVärde(källapdeAdress)
		if (källapde & SidaAnsluten) == 0 {
			continue
		}
		if issharedpde(pde) {
			Mängdunsignedinteger32atAdress(källapde, målSidaKatalog+pde*4)
			continue
		}

		målptMuspekare, _ := AktivMinnemanager.Alignedmalloc(0x1000)
		if målptMuspekare == nil {
			continue
		}
		källapt := källapde & SidaRam
		målpt := uint32(uintptr(målptMuspekare))
		Mängdunsignedinteger32atAdress((målpt | (källapde & 0xFFF)), målSidaKatalog+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteAdress := källapt + pte*4
			post := GetVärde(pteAdress)
			if (post & SidaAnsluten) != 0 {
				if (post & Sidawritable) != 0 {
					post = (post &^ Sidawritable) | Sidacow
					Mängdunsignedinteger32atAdress(post, pteAdress)
					cowRammanager.Increment(post & SidaRam)
				} else if (post & Sidacow) != 0 {
					cowRammanager.Increment(post & SidaRam)
				}
			}
			Mängdunsignedinteger32atAdress(post, målpt+pte*4)
		}
	}
	uppdateracr3()
	return målSidaKatalog
}

func ResolveKopieraPåSkrivfault() bool {
	if AktivMinnemanager == nil {
		return false
	}
	faultAdress := getcr2()
	sidkatalog := getcr3()
	pdeAdress := sidkatalog + ((faultAdress>>22)&0x3FF)*4
	pde := GetVärde(pdeAdress)
	if (pde & SidaAnsluten) == 0 {
		return false
	}
	pt := pde & SidaRam
	pteAdress := pt + ((faultAdress>>12)&0x3FF)*4
	pte := GetVärde(pteAdress)
	if (pte&Sidacow) == 0 || (pte&SidaAnsluten) == 0 {
		return false
	}
	oldRam := pte & SidaRam
	if cowRammanager.Reference(oldRam) <= 1 {
		Mängdunsignedinteger32atAdress((pte|Sidawritable)&^Sidacow, pteAdress)
		uppdateracr3()
		return true
	}

	nyMuspekare, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if nyMuspekare == nil {
		return false
	}
	nyRam := uint32(uintptr(nyMuspekare)) & SidaRam

	källa_2 := GetBytefromMuspekare(uintptr(faultAdress&SidaRam), 0x1000, 0x1000)
	mål_2 := GetBytefromMuspekare(uintptr(nyRam), 0x1000, 0x1000)
	copy(mål_2, källa_2)
	cowRammanager.Decrement(oldRam)
	Mängdunsignedinteger32atAdress((nyRam|(pte&0xFFF)|Sidawritable)&^Sidacow, pteAdress)
	uppdateracr3()
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

func uppdateracr3() {
	cr3 := getcr3()
	mängdcr3(cr3)
}

func MängdbyteiSidaKatalog(x byte, adress uint32, sidkatalog uint32) {
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	MängdbyteatAdress(x, adress)
	mängdcr3(oldcr3)
}

func MängdblockiSidaKatalog(källa_2 []byte, mål_2 []byte, storlek uint32, sidkatalog uint32) {
	if storlek == 0 || sidkatalog == 0 {
		return
	}
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	makeIntervallPrivatwritableAktuell(sidkatalog, uint32(uintptr(unsafe.Pointer(&mål_2[0]))), storlek)

	for i := uint32(0); i < storlek; i++ {
		mål_2[i] = källa_2[i]
	}
	mängdcr3(oldcr3)
}

func NollblockiSidaKatalog(adress uint32, storlek uint32, sidkatalog uint32) {
	if storlek == 0 || sidkatalog == 0 {
		return
	}
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	makeIntervallPrivatwritableAktuell(sidkatalog, adress, storlek)
	mål_2 := GetBytefromMuspekare(uintptr(adress), int(storlek), int(storlek))
	for i := uint32(0); i < storlek; i++ {
		mål_2[i] = 0
	}
	mängdcr3(oldcr3)
}

func makeSidaPrivatwritableAktuell(sidkatalog uint32, virtuellAdress uint32) bool {
	pde := GetVärde(sidkatalog + ((virtuellAdress>>22)&0x3FF)*4)
	if (pde & SidaAnsluten) == 0 {
		return false
	}
	pteAdress := (pde & SidaRam) + ((virtuellAdress>>12)&0x3FF)*4
	pte := GetVärde(pteAdress)
	if (pte & SidaAnsluten) == 0 {
		return false
	}
	if (pte & Sidacow) == 0 {
		return (pte & Sidawritable) != 0
	}
	if AktivMinnemanager == nil {
		return false
	}
	nyMuspekare, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if nyMuspekare == nil {
		return false
	}
	nyRam := uint32(uintptr(nyMuspekare)) & SidaRam
	källa_2 := GetBytefromMuspekare(uintptr(virtuellAdress&SidaRam), 0x1000, 0x1000)
	mål_2 := GetBytefromMuspekare(uintptr(nyRam), 0x1000, 0x1000)
	copy(mål_2, källa_2)
	cowRammanager.Decrement(pte & SidaRam)
	Mängdunsignedinteger32atAdress((nyRam|(pte&0xFFF)|Sidawritable)&^Sidacow, pteAdress)
	// Publish the new physical frame before writing through its virtual address.
	uppdateracr3()
	return true
}

func makeIntervallPrivatwritableAktuell(sidkatalog uint32, adress uint32, storlek uint32) bool {
	if storlek == 0 {
		return true
	}
	sista := adress + storlek - 1
	if sista < adress {
		return false
	}
	for sida := adress & SidaRam; ; sida += 0x1000 {
		if !makeSidaPrivatwritableAktuell(sidkatalog, sida) {
			return false
		}
		if sida == (sista & SidaRam) {
			break
		}
	}
	return true
}

func MakeIntervallPrivatwritable(sidkatalog uint32, adress uint32, storlek uint32) bool {
	if sidkatalog == 0 {
		return false
	}
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	ok := makeIntervallPrivatwritableAktuell(sidkatalog, adress, storlek)
	mängdcr3(oldcr3)
	return ok
}

func Mängdunsignedinteger32iSidaKatalog(x uint32, adress uint32, sidkatalog uint32) {
	if sidkatalog == 0 {
		return
	}
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	Mängdunsignedinteger32atAdress(x, adress)
	mängdcr3(oldcr3)
}

func GetVärde(adress uint32) uint32 {
	var orgVärde uint32 = *(*uint32)(unsafe.Pointer(uintptr(adress)))
	return orgVärde
}
func GetVärdeiSidaKatalog(adress uint32, sidkatalog uint32) uint32 {
	if sidkatalog == 0 {
		return 0
	}
	oldcr3 := getcr3()
	mängdcr3(sidkatalog)
	v := GetVärde(adress)
	mängdcr3(oldcr3)
	return v
}

var v uint32 = 0

func KopieraSidaRamblock(xSidaKatalog uint32, ySidaKatalog uint32, vAdress uint32) {
	if xSidaKatalog == 0 || ySidaKatalog == 0 {
		return
	}
	oldcr3 := getcr3()
	mängdcr3(xSidaKatalog)
	v = GetVärde(vAdress)
	Mängdunsignedinteger32iSidaKatalog(v, vAdress, ySidaKatalog)

	mängdcr3(oldcr3)
}
