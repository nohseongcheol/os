package paging

import unsafe "unsafe"
import . "interrupt"
import . "minnimanager"
import . "util"

type Síðamappaentry_2 uintptr

const (
	Síðapresent	uint32	= 0x001
	Síðawritable	uint32	= 0x002
	SíðaNotandi	uint32	= 0x004
	SíðaRammi	uint32	= 0xFFFFF000
	Síðacow		uint32	= 0x200
)

func Setjabyteataddress(x byte, address uint32)
func Setjaunsignedinteger8ataddress(x uint8, address uint32)
func Setjaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setjacr3(síðamappa uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowRammimanager struct {
	mem		*TMinnimanager
	refs		[]uint16
	rammicount	uint32
}

var (
	Síðamappaentry	uintptr
	SíðaTaflaentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowRammimanager	TcowRammimanager
)

func (sjálft *TcowRammimanager) Init(mem *TMinnimanager, rammicount uint32) bool {
	sjálft.mem = mem
	sjálft.rammicount = rammicount
	referenceBæti := rammicount * uint32(unsafe.Sizeof(uint16(0)))
	referenceBendill := mem.Malloc(referenceBæti)
	if referenceBendill == nil {
		sjálft.refs = nil
		sjálft.rammicount = 0
		return false
	}
	sjálft.refs = (*[1 << 28]uint16)(referenceBendill)[:rammicount:rammicount]
	for i := uint32(0); i < rammicount; i++ {
		sjálft.refs[i] = 0
	}
	return true
}

func (sjálft *TcowRammimanager) Reference(rammi uint32) uint16 {
	idx := rammi >> 12
	if idx >= sjálft.rammicount || sjálft.refs == nil {
		return 0
	}
	return sjálft.refs[idx]
}

func (sjálft *TcowRammimanager) Increment(rammi uint32) {
	idx := rammi >> 12
	if idx >= sjálft.rammicount || sjálft.refs == nil {
		return
	}
	if sjálft.refs[idx] == 0 {
		sjálft.refs[idx] = 2
	} else {
		sjálft.refs[idx]++
	}
}

func (sjálft *TcowRammimanager) Decrement(rammi uint32) {
	idx := rammi >> 12
	if idx >= sjálft.rammicount || sjálft.refs == nil || sjálft.refs[idx] == 0 {
		return
	}
	sjálft.refs[idx]--
}

func (sjálft *Paging) Init(síðamappaentry uintptr, síðaTaflaentry uint32, minnimanager *TMinnimanager) {

	Síðamappaentry = síðamappaentry
	SíðaTaflaentry = síðaTaflaentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRammimanager.Init(minnimanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressBendill, _ := minnimanager.Alignedmalloc(0x1000)
			if addressBendill == nil {
				return
			}
			address := uint32(uintptr(addressBendill))

			Setjaunsignedinteger32ataddress(address|0x87, uint32(síðamappaentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setjaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		síðamappaentry = síðamappaentry + 0x1000
	}

}
func (sjálft *Paging) SharedMinniregion() {

	síðamappaentry := Síðamappaentry
	ksíðamappaentry := Síðamappaentry

	for i := uint32(1); i <= virtlen; i++ {

		síðamappaentry = síðamappaentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetGildi(uint32(ksíðamappaentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setjaunsignedinteger32ataddress(v|0x87, uint32(síðamappaentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetGildi(uint32(ksíðamappaentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setjaunsignedinteger32ataddress(v|0x87, uint32(síðamappaentry)+pde*4)

		}

	}
}
func (sjálft *Paging) Síðafault(manager *TInterruptmanager) {
	interrupthandler = haldfangpaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	sjálft.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func haldfangpaginginterrupt(esp uint32) uint32 {
	if ResolveAfritaNotaSkriftfault() {
		return esp
	}
	return HaldfangfatalinterruptRammi(esp, 0x0E)
}

func CloneaddressBilslácow(upprunisíðamappa uint32) uint32 {
	if VirktMinnimanager == nil || upprunisíðamappa == 0 {
		return 0
	}
	áfangastaðurBendill, _ := VirktMinnimanager.Alignedmalloc(0x1000)
	if áfangastaðurBendill == nil {
		return 0
	}
	áfangastaðursíðamappa := uint32(uintptr(áfangastaðurBendill))
	for i := uint32(0); i < 1024; i++ {
		Setjaunsignedinteger32ataddress(0, áfangastaðursíðamappa+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		upprunipdeaddress := upprunisíðamappa + pde*4
		upprunipde := GetGildi(upprunipdeaddress)
		if (upprunipde & Síðapresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setjaunsignedinteger32ataddress(upprunipde, áfangastaðursíðamappa+pde*4)
			continue
		}

		áfangastaðurptBendill, _ := VirktMinnimanager.Alignedmalloc(0x1000)
		if áfangastaðurptBendill == nil {
			continue
		}
		upprunipt := upprunipde & SíðaRammi
		áfangastaðurpt := uint32(uintptr(áfangastaðurptBendill))
		Setjaunsignedinteger32ataddress((áfangastaðurpt | (upprunipde & 0xFFF)), áfangastaðursíðamappa+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := upprunipt + pte*4
			entry := GetGildi(pteaddress)
			if (entry & Síðapresent) != 0 {
				if (entry & Síðawritable) != 0 {
					entry = (entry &^ Síðawritable) | Síðacow
					Setjaunsignedinteger32ataddress(entry, pteaddress)
					cowRammimanager.Increment(entry & SíðaRammi)
				} else if (entry & Síðacow) != 0 {
					cowRammimanager.Increment(entry & SíðaRammi)
				}
			}
			Setjaunsignedinteger32ataddress(entry, áfangastaðurpt+pte*4)
		}
	}
	endurhlaðacr3()
	return áfangastaðursíðamappa
}

func ResolveAfritaNotaSkriftfault() bool {
	if VirktMinnimanager == nil {
		return false
	}
	faultaddress := getcr2()
	síðamappa := getcr3()
	pdeaddress := síðamappa + ((faultaddress>>22)&0x3FF)*4
	pde := GetGildi(pdeaddress)
	if (pde & Síðapresent) == 0 {
		return false
	}
	pt := pde & SíðaRammi
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetGildi(pteaddress)
	if (pte&Síðacow) == 0 || (pte&Síðapresent) == 0 {
		return false
	}
	oldRammi := pte & SíðaRammi
	if cowRammimanager.Reference(oldRammi) <= 1 {
		Setjaunsignedinteger32ataddress((pte|Síðawritable)&^Síðacow, pteaddress)
		endurhlaðacr3()
		return true
	}

	nýttBendill, _ := VirktMinnimanager.Alignedmalloc(0x1000)
	if nýttBendill == nil {
		return false
	}
	nýttRammi := uint32(uintptr(nýttBendill)) & SíðaRammi

	uppruni_2 := GetBætifromBendill(uintptr(faultaddress&SíðaRammi), 0x1000, 0x1000)
	áfangastaður_2 := GetBætifromBendill(uintptr(nýttRammi), 0x1000, 0x1000)
	copy(áfangastaður_2, uppruni_2)
	cowRammimanager.Decrement(oldRammi)
	Setjaunsignedinteger32ataddress((nýttRammi|(pte&0xFFF)|Síðawritable)&^Síðacow, pteaddress)
	endurhlaðacr3()
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

func endurhlaðacr3() {
	cr3 := getcr3()
	setjacr3(cr3)
}

func SetjabyteInnsíðamappa(x byte, address uint32, síðamappa uint32) {
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	Setjabyteataddress(x, address)
	setjacr3(oldcr3)
}

func SetjaBlokkInnsíðamappa(uppruni_2 []byte, áfangastaður_2 []byte, stærð uint32, síðamappa uint32) {
	if stærð == 0 || síðamappa == 0 {
		return
	}
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	makeSviðLokaðprivatewritableNúverandi(síðamappa, uint32(uintptr(unsafe.Pointer(&áfangastaður_2[0]))), stærð)

	for i := uint32(0); i < stærð; i++ {
		áfangastaður_2[i] = uppruni_2[i]
	}
	setjacr3(oldcr3)
}

func ZeroBlokkInnsíðamappa(address uint32, stærð uint32, síðamappa uint32) {
	if stærð == 0 || síðamappa == 0 {
		return
	}
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	makeSviðLokaðprivatewritableNúverandi(síðamappa, address, stærð)
	áfangastaður_2 := GetBætifromBendill(uintptr(address), int(stærð), int(stærð))
	for i := uint32(0); i < stærð; i++ {
		áfangastaður_2[i] = 0
	}
	setjacr3(oldcr3)
}

func makesíðaLokaðprivatewritableNúverandi(síðamappa uint32, sýndaraddress uint32) bool {
	pde := GetGildi(síðamappa + ((sýndaraddress>>22)&0x3FF)*4)
	if (pde & Síðapresent) == 0 {
		return false
	}
	pteaddress := (pde & SíðaRammi) + ((sýndaraddress>>12)&0x3FF)*4
	pte := GetGildi(pteaddress)
	if (pte & Síðapresent) == 0 {
		return false
	}
	if (pte & Síðacow) == 0 {
		return (pte & Síðawritable) != 0
	}
	if VirktMinnimanager == nil {
		return false
	}
	nýttBendill, _ := VirktMinnimanager.Alignedmalloc(0x1000)
	if nýttBendill == nil {
		return false
	}
	nýttRammi := uint32(uintptr(nýttBendill)) & SíðaRammi
	uppruni_2 := GetBætifromBendill(uintptr(sýndaraddress&SíðaRammi), 0x1000, 0x1000)
	áfangastaður_2 := GetBætifromBendill(uintptr(nýttRammi), 0x1000, 0x1000)
	copy(áfangastaður_2, uppruni_2)
	cowRammimanager.Decrement(pte & SíðaRammi)
	Setjaunsignedinteger32ataddress((nýttRammi|(pte&0xFFF)|Síðawritable)&^Síðacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	endurhlaðacr3()
	return true
}

func makeSviðLokaðprivatewritableNúverandi(síðamappa uint32, address uint32, stærð uint32) bool {
	if stærð == 0 {
		return true
	}
	síðasta := address + stærð - 1
	if síðasta < address {
		return false
	}
	for síða := address & SíðaRammi; ; síða += 0x1000 {
		if !makesíðaLokaðprivatewritableNúverandi(síðamappa, síða) {
			return false
		}
		if síða == (síðasta & SíðaRammi) {
			break
		}
	}
	return true
}

func MakeSviðLokaðprivatewritable(síðamappa uint32, address uint32, stærð uint32) bool {
	if síðamappa == 0 {
		return false
	}
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	ílagi := makeSviðLokaðprivatewritableNúverandi(síðamappa, address, stærð)
	setjacr3(oldcr3)
	return ílagi
}

func Setjaunsignedinteger32Innsíðamappa(x uint32, address uint32, síðamappa uint32) {
	if síðamappa == 0 {
		return
	}
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	Setjaunsignedinteger32ataddress(x, address)
	setjacr3(oldcr3)
}

func GetGildi(address uint32) uint32 {
	var orgGildi uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgGildi
}
func GetGildiInnsíðamappa(address uint32, síðamappa uint32) uint32 {
	if síðamappa == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setjacr3(síðamappa)
	v := GetGildi(address)
	setjacr3(oldcr3)
	return v
}

var v uint32 = 0

func AfritasíðaRammiBlokk(xsíðamappa uint32, ysíðamappa uint32, vaddress uint32) {
	if xsíðamappa == 0 || ysíðamappa == 0 {
		return
	}
	oldcr3 := getcr3()
	setjacr3(xsíðamappa)
	v = GetGildi(vaddress)
	Setjaunsignedinteger32Innsíðamappa(v, vaddress, ysíðamappa)

	setjacr3(oldcr3)
}
