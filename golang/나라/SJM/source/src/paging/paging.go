package paging

import unsafe "unsafe"
import . "avbrudd"
import . "minnemanager"
import . "util"

type SideKatalogentry_2 uintptr

const (
	SideTilstede	uint32	= 0x001
	Sidewritable	uint32	= 0x002
	SideBruker	uint32	= 0x004
	SideRamme	uint32	= 0xFFFFF000
	Sidecow		uint32	= 0x200
)

func Settbyteataddress(x byte, address uint32)
func Settunsignedinteger8ataddress(x uint8, address uint32)
func Settunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func settcr3(sideKatalog uint32)
func getcr3() uint32

type Paging struct {
	TAvbruddhandler
}
type TcowRammemanager struct {
	mem		*TMinnemanager
	refs		[]uint16
	rammeAntall	uint32
}

var (
	SideKatalogentry	uintptr
	SideTabellentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowRammemanager		TcowRammemanager
)

func (selv *TcowRammemanager) Init(mem *TMinnemanager, rammeAntall uint32) bool {
	selv.mem = mem
	selv.rammeAntall = rammeAntall
	referenceByte := rammeAntall * uint32(unsafe.Sizeof(uint16(0)))
	referencePeker := mem.Malloc(referenceByte)
	if referencePeker == nil {
		selv.refs = nil
		selv.rammeAntall = 0
		return false
	}
	selv.refs = (*[1 << 28]uint16)(referencePeker)[:rammeAntall:rammeAntall]
	for i := uint32(0); i < rammeAntall; i++ {
		selv.refs[i] = 0
	}
	return true
}

func (selv *TcowRammemanager) Reference(ramme uint32) uint16 {
	idx := ramme >> 12
	if idx >= selv.rammeAntall || selv.refs == nil {
		return 0
	}
	return selv.refs[idx]
}

func (selv *TcowRammemanager) Increment(ramme uint32) {
	idx := ramme >> 12
	if idx >= selv.rammeAntall || selv.refs == nil {
		return
	}
	if selv.refs[idx] == 0 {
		selv.refs[idx] = 2
	} else {
		selv.refs[idx]++
	}
}

func (selv *TcowRammemanager) Decrement(ramme uint32) {
	idx := ramme >> 12
	if idx >= selv.rammeAntall || selv.refs == nil || selv.refs[idx] == 0 {
		return
	}
	selv.refs[idx]--
}

func (selv *Paging) Init(sideKatalogentry uintptr, sideTabellentry uint32, minnemanager *TMinnemanager) {

	SideKatalogentry = sideKatalogentry
	SideTabellentry = sideTabellentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRammemanager.Init(minnemanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPeker, _ := minnemanager.Alignedmalloc(0x1000)
			if addressPeker == nil {
				return
			}
			address := uint32(uintptr(addressPeker))

			Settunsignedinteger32ataddress(address|0x87, uint32(sideKatalogentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Settunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sideKatalogentry = sideKatalogentry + 0x1000
	}

}
func (selv *Paging) SharedMinneregion() {

	sideKatalogentry := SideKatalogentry
	kSideKatalogentry := SideKatalogentry

	for i := uint32(1); i <= virtlen; i++ {

		sideKatalogentry = sideKatalogentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVerdi(uint32(kSideKatalogentry) + pde*4)
			v = (v & 0xFFFFF000)
			Settunsignedinteger32ataddress(v|0x87, uint32(sideKatalogentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVerdi(uint32(kSideKatalogentry) + pde*4)
			v = (v & 0xFFFFF000)
			Settunsignedinteger32ataddress(v|0x87, uint32(sideKatalogentry)+pde*4)

		}

	}
}
func (selv *Paging) Sidefault(manager *TAvbruddmanager) {
	avbruddhandler = håndtakpagingAvbrudd

	var address uintptr
	address = uintptr(unsafe.Pointer(&avbruddhandler))
	selv.TAvbruddhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var avbruddhandler func(uint32) uint32

func håndtakpagingAvbrudd(esp uint32) uint32 {
	if ResolveKopierPåSkrivfault() {
		return esp
	}
	return HåndtakfatalAvbruddRamme(esp, 0x0E)
}

func CloneaddressMellomromcow(kildeSideKatalog uint32) uint32 {
	if AktivMinnemanager == nil || kildeSideKatalog == 0 {
		return 0
	}
	målPeker, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if målPeker == nil {
		return 0
	}
	målSideKatalog := uint32(uintptr(målPeker))
	for i := uint32(0); i < 1024; i++ {
		Settunsignedinteger32ataddress(0, målSideKatalog+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		kildepdeaddress := kildeSideKatalog + pde*4
		kildepde := GetVerdi(kildepdeaddress)
		if (kildepde & SideTilstede) == 0 {
			continue
		}
		if issharedpde(pde) {
			Settunsignedinteger32ataddress(kildepde, målSideKatalog+pde*4)
			continue
		}

		målptPeker, _ := AktivMinnemanager.Alignedmalloc(0x1000)
		if målptPeker == nil {
			continue
		}
		kildept := kildepde & SideRamme
		målpt := uint32(uintptr(målptPeker))
		Settunsignedinteger32ataddress((målpt | (kildepde & 0xFFF)), målSideKatalog+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := kildept + pte*4
			entry := GetVerdi(pteaddress)
			if (entry & SideTilstede) != 0 {
				if (entry & Sidewritable) != 0 {
					entry = (entry &^ Sidewritable) | Sidecow
					Settunsignedinteger32ataddress(entry, pteaddress)
					cowRammemanager.Increment(entry & SideRamme)
				} else if (entry & Sidecow) != 0 {
					cowRammemanager.Increment(entry & SideRamme)
				}
			}
			Settunsignedinteger32ataddress(entry, målpt+pte*4)
		}
	}
	lastpånyttcr3()
	return målSideKatalog
}

func ResolveKopierPåSkrivfault() bool {
	if AktivMinnemanager == nil {
		return false
	}
	faultaddress := getcr2()
	sideKatalog := getcr3()
	pdeaddress := sideKatalog + ((faultaddress>>22)&0x3FF)*4
	pde := GetVerdi(pdeaddress)
	if (pde & SideTilstede) == 0 {
		return false
	}
	pt := pde & SideRamme
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVerdi(pteaddress)
	if (pte&Sidecow) == 0 || (pte&SideTilstede) == 0 {
		return false
	}
	gammelRamme := pte & SideRamme
	if cowRammemanager.Reference(gammelRamme) <= 1 {
		Settunsignedinteger32ataddress((pte|Sidewritable)&^Sidecow, pteaddress)
		lastpånyttcr3()
		return true
	}

	nyPeker, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if nyPeker == nil {
		return false
	}
	nyRamme := uint32(uintptr(nyPeker)) & SideRamme

	kilde_2 := GetBytefromPeker(uintptr(faultaddress&SideRamme), 0x1000, 0x1000)
	mål_2 := GetBytefromPeker(uintptr(nyRamme), 0x1000, 0x1000)
	copy(mål_2, kilde_2)
	cowRammemanager.Decrement(gammelRamme)
	Settunsignedinteger32ataddress((nyRamme|(pte&0xFFF)|Sidewritable)&^Sidecow, pteaddress)
	lastpånyttcr3()
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

func lastpånyttcr3() {
	cr3 := getcr3()
	settcr3(cr3)
}

func SettbyteInnSideKatalog(x byte, address uint32, sideKatalog uint32) {
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	Settbyteataddress(x, address)
	settcr3(gammelcr3)
}

func SettBlokkInnSideKatalog(kilde_2 []byte, mål_2 []byte, størrelse uint32, sideKatalog uint32) {
	if størrelse == 0 || sideKatalog == 0 {
		return
	}
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	makeOmrådePrivatwritableGjeldende(sideKatalog, uint32(uintptr(unsafe.Pointer(&mål_2[0]))), størrelse)

	for i := uint32(0); i < størrelse; i++ {
		mål_2[i] = kilde_2[i]
	}
	settcr3(gammelcr3)
}

func ZeroBlokkInnSideKatalog(address uint32, størrelse uint32, sideKatalog uint32) {
	if størrelse == 0 || sideKatalog == 0 {
		return
	}
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	makeOmrådePrivatwritableGjeldende(sideKatalog, address, størrelse)
	mål_2 := GetBytefromPeker(uintptr(address), int(størrelse), int(størrelse))
	for i := uint32(0); i < størrelse; i++ {
		mål_2[i] = 0
	}
	settcr3(gammelcr3)
}

func makeSidePrivatwritableGjeldende(sideKatalog uint32, virtuelladdress uint32) bool {
	pde := GetVerdi(sideKatalog + ((virtuelladdress>>22)&0x3FF)*4)
	if (pde & SideTilstede) == 0 {
		return false
	}
	pteaddress := (pde & SideRamme) + ((virtuelladdress>>12)&0x3FF)*4
	pte := GetVerdi(pteaddress)
	if (pte & SideTilstede) == 0 {
		return false
	}
	if (pte & Sidecow) == 0 {
		return (pte & Sidewritable) != 0
	}
	if AktivMinnemanager == nil {
		return false
	}
	nyPeker, _ := AktivMinnemanager.Alignedmalloc(0x1000)
	if nyPeker == nil {
		return false
	}
	nyRamme := uint32(uintptr(nyPeker)) & SideRamme
	kilde_2 := GetBytefromPeker(uintptr(virtuelladdress&SideRamme), 0x1000, 0x1000)
	mål_2 := GetBytefromPeker(uintptr(nyRamme), 0x1000, 0x1000)
	copy(mål_2, kilde_2)
	cowRammemanager.Decrement(pte & SideRamme)
	Settunsignedinteger32ataddress((nyRamme|(pte&0xFFF)|Sidewritable)&^Sidecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	lastpånyttcr3()
	return true
}

func makeOmrådePrivatwritableGjeldende(sideKatalog uint32, address uint32, størrelse uint32) bool {
	if størrelse == 0 {
		return true
	}
	siste := address + størrelse - 1
	if siste < address {
		return false
	}
	for side := address & SideRamme; ; side += 0x1000 {
		if !makeSidePrivatwritableGjeldende(sideKatalog, side) {
			return false
		}
		if side == (siste & SideRamme) {
			break
		}
	}
	return true
}

func MakeOmrådePrivatwritable(sideKatalog uint32, address uint32, størrelse uint32) bool {
	if sideKatalog == 0 {
		return false
	}
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	ok := makeOmrådePrivatwritableGjeldende(sideKatalog, address, størrelse)
	settcr3(gammelcr3)
	return ok
}

func Settunsignedinteger32InnSideKatalog(x uint32, address uint32, sideKatalog uint32) {
	if sideKatalog == 0 {
		return
	}
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	Settunsignedinteger32ataddress(x, address)
	settcr3(gammelcr3)
}

func GetVerdi(address uint32) uint32 {
	var orgVerdi uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVerdi
}
func GetVerdiInnSideKatalog(address uint32, sideKatalog uint32) uint32 {
	if sideKatalog == 0 {
		return 0
	}
	gammelcr3 := getcr3()
	settcr3(sideKatalog)
	v := GetVerdi(address)
	settcr3(gammelcr3)
	return v
}

var v uint32 = 0

func KopierSideRammeBlokk(xSideKatalog uint32, ySideKatalog uint32, vaddress uint32) {
	if xSideKatalog == 0 || ySideKatalog == 0 {
		return
	}
	gammelcr3 := getcr3()
	settcr3(xSideKatalog)
	v = GetVerdi(vaddress)
	Settunsignedinteger32InnSideKatalog(v, vaddress, ySideKatalog)

	settcr3(gammelcr3)
}
