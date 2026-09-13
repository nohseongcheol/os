package paging

import unsafe "unsafe"
import . "interrupt"
import . "hukommelsemanager"
import . "util"

type SideMappeemne_2 uintptr

const (
	SideTilstedeværende	uint32	= 0x001
	Sidewritable		uint32	= 0x002
	SideBruger		uint32	= 0x004
	SideRamme		uint32	= 0xFFFFF000
	Sidecow			uint32	= 0x200
)

func Satbyteataddress(x byte, address uint32)
func Satunsignedinteger8ataddress(x uint8, address uint32)
func Satunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func satcr3(sideMappe uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowRammemanager struct {
	mem		*THukommelsemanager
	refs		[]uint16
	rammeAntal	uint32
}

var (
	SideMappeemne	uintptr
	SideTabelemne	uint32
	pdelen		uint32
	virtlen		uint32
	cowRammemanager	TcowRammemanager
)

func (selv *TcowRammemanager) Init(mem *THukommelsemanager, rammeAntal uint32) bool {
	selv.mem = mem
	selv.rammeAntal = rammeAntal
	referenceByte := rammeAntal * uint32(unsafe.Sizeof(uint16(0)))
	referenceMarkør := mem.Malloc(referenceByte)
	if referenceMarkør == nil {
		selv.refs = nil
		selv.rammeAntal = 0
		return false
	}
	selv.refs = (*[1 << 28]uint16)(referenceMarkør)[:rammeAntal:rammeAntal]
	for i := uint32(0); i < rammeAntal; i++ {
		selv.refs[i] = 0
	}
	return true
}

func (selv *TcowRammemanager) Reference(ramme uint32) uint16 {
	idx := ramme >> 12
	if idx >= selv.rammeAntal || selv.refs == nil {
		return 0
	}
	return selv.refs[idx]
}

func (selv *TcowRammemanager) Increment(ramme uint32) {
	idx := ramme >> 12
	if idx >= selv.rammeAntal || selv.refs == nil {
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
	if idx >= selv.rammeAntal || selv.refs == nil || selv.refs[idx] == 0 {
		return
	}
	selv.refs[idx]--
}

func (selv *Paging) Init(sideMappeemne uintptr, sideTabelemne uint32, hukommelsemanager *THukommelsemanager) {

	SideMappeemne = sideMappeemne
	SideTabelemne = sideTabelemne

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRammemanager.Init(hukommelsemanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressMarkør, _ := hukommelsemanager.Alignedmalloc(0x1000)
			if addressMarkør == nil {
				return
			}
			address := uint32(uintptr(addressMarkør))

			Satunsignedinteger32ataddress(address|0x87, uint32(sideMappeemne)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Satunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sideMappeemne = sideMappeemne + 0x1000
	}

}
func (selv *Paging) SharedHukommelseregion() {

	sideMappeemne := SideMappeemne
	kSideMappeemne := SideMappeemne

	for i := uint32(1); i <= virtlen; i++ {

		sideMappeemne = sideMappeemne + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVærdi(uint32(kSideMappeemne) + pde*4)
			v = (v & 0xFFFFF000)
			Satunsignedinteger32ataddress(v|0x87, uint32(sideMappeemne)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVærdi(uint32(kSideMappeemne) + pde*4)
			v = (v & 0xFFFFF000)
			Satunsignedinteger32ataddress(v|0x87, uint32(sideMappeemne)+pde*4)

		}

	}
}
func (selv *Paging) Sidefault(manager *TInterruptmanager) {
	interrupthandler = håndtagpaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	selv.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func håndtagpaginginterrupt(esp uint32) uint32 {
	if ResolveKopiértændtSkrivefault() {
		return esp
	}
	return HåndtagfatalinterruptRamme(esp, 0x0E)
}

func CloneaddressMellemrumcow(kildeSideMappe uint32) uint32 {
	if AktivHukommelsemanager == nil || kildeSideMappe == 0 {
		return 0
	}
	destinationMarkør, _ := AktivHukommelsemanager.Alignedmalloc(0x1000)
	if destinationMarkør == nil {
		return 0
	}
	destinationSideMappe := uint32(uintptr(destinationMarkør))
	for i := uint32(0); i < 1024; i++ {
		Satunsignedinteger32ataddress(0, destinationSideMappe+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		kildepdeaddress := kildeSideMappe + pde*4
		kildepde := GetVærdi(kildepdeaddress)
		if (kildepde & SideTilstedeværende) == 0 {
			continue
		}
		if issharedpde(pde) {
			Satunsignedinteger32ataddress(kildepde, destinationSideMappe+pde*4)
			continue
		}

		destinationptMarkør, _ := AktivHukommelsemanager.Alignedmalloc(0x1000)
		if destinationptMarkør == nil {
			continue
		}
		kildept := kildepde & SideRamme
		destinationpt := uint32(uintptr(destinationptMarkør))
		Satunsignedinteger32ataddress((destinationpt | (kildepde & 0xFFF)), destinationSideMappe+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := kildept + pte*4
			emne := GetVærdi(pteaddress)
			if (emne & SideTilstedeværende) != 0 {
				if (emne & Sidewritable) != 0 {
					emne = (emne &^ Sidewritable) | Sidecow
					Satunsignedinteger32ataddress(emne, pteaddress)
					cowRammemanager.Increment(emne & SideRamme)
				} else if (emne & Sidecow) != 0 {
					cowRammemanager.Increment(emne & SideRamme)
				}
			}
			Satunsignedinteger32ataddress(emne, destinationpt+pte*4)
		}
	}
	genindlæscr3()
	return destinationSideMappe
}

func ResolveKopiértændtSkrivefault() bool {
	if AktivHukommelsemanager == nil {
		return false
	}
	faultaddress := getcr2()
	sideMappe := getcr3()
	pdeaddress := sideMappe + ((faultaddress>>22)&0x3FF)*4
	pde := GetVærdi(pdeaddress)
	if (pde & SideTilstedeværende) == 0 {
		return false
	}
	pt := pde & SideRamme
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVærdi(pteaddress)
	if (pte&Sidecow) == 0 || (pte&SideTilstedeværende) == 0 {
		return false
	}
	gammelRamme := pte & SideRamme
	if cowRammemanager.Reference(gammelRamme) <= 1 {
		Satunsignedinteger32ataddress((pte|Sidewritable)&^Sidecow, pteaddress)
		genindlæscr3()
		return true
	}

	nyMarkør, _ := AktivHukommelsemanager.Alignedmalloc(0x1000)
	if nyMarkør == nil {
		return false
	}
	nyRamme := uint32(uintptr(nyMarkør)) & SideRamme

	kilde_2 := GetBytefraMarkør(uintptr(faultaddress&SideRamme), 0x1000, 0x1000)
	destination_2 := GetBytefraMarkør(uintptr(nyRamme), 0x1000, 0x1000)
	copy(destination_2, kilde_2)
	cowRammemanager.Decrement(gammelRamme)
	Satunsignedinteger32ataddress((nyRamme|(pte&0xFFF)|Sidewritable)&^Sidecow, pteaddress)
	genindlæscr3()
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

func genindlæscr3() {
	cr3 := getcr3()
	satcr3(cr3)
}

func SatbyteIndSideMappe(x byte, address uint32, sideMappe uint32) {
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	Satbyteataddress(x, address)
	satcr3(gammelcr3)
}

func SatBlokIndSideMappe(kilde_2 []byte, destination_2 []byte, størrelse uint32, sideMappe uint32) {
	if størrelse == 0 || sideMappe == 0 {
		return
	}
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	makeIntervalPrivatwritableAktive(sideMappe, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), størrelse)

	for i := uint32(0); i < størrelse; i++ {
		destination_2[i] = kilde_2[i]
	}
	satcr3(gammelcr3)
}

func ZeroBlokIndSideMappe(address uint32, størrelse uint32, sideMappe uint32) {
	if størrelse == 0 || sideMappe == 0 {
		return
	}
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	makeIntervalPrivatwritableAktive(sideMappe, address, størrelse)
	destination_2 := GetBytefraMarkør(uintptr(address), int(størrelse), int(størrelse))
	for i := uint32(0); i < størrelse; i++ {
		destination_2[i] = 0
	}
	satcr3(gammelcr3)
}

func makeSidePrivatwritableAktive(sideMappe uint32, virtueladdress uint32) bool {
	pde := GetVærdi(sideMappe + ((virtueladdress>>22)&0x3FF)*4)
	if (pde & SideTilstedeværende) == 0 {
		return false
	}
	pteaddress := (pde & SideRamme) + ((virtueladdress>>12)&0x3FF)*4
	pte := GetVærdi(pteaddress)
	if (pte & SideTilstedeværende) == 0 {
		return false
	}
	if (pte & Sidecow) == 0 {
		return (pte & Sidewritable) != 0
	}
	if AktivHukommelsemanager == nil {
		return false
	}
	nyMarkør, _ := AktivHukommelsemanager.Alignedmalloc(0x1000)
	if nyMarkør == nil {
		return false
	}
	nyRamme := uint32(uintptr(nyMarkør)) & SideRamme
	kilde_2 := GetBytefraMarkør(uintptr(virtueladdress&SideRamme), 0x1000, 0x1000)
	destination_2 := GetBytefraMarkør(uintptr(nyRamme), 0x1000, 0x1000)
	copy(destination_2, kilde_2)
	cowRammemanager.Decrement(pte & SideRamme)
	Satunsignedinteger32ataddress((nyRamme|(pte&0xFFF)|Sidewritable)&^Sidecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	genindlæscr3()
	return true
}

func makeIntervalPrivatwritableAktive(sideMappe uint32, address uint32, størrelse uint32) bool {
	if størrelse == 0 {
		return true
	}
	sidste := address + størrelse - 1
	if sidste < address {
		return false
	}
	for side := address & SideRamme; ; side += 0x1000 {
		if !makeSidePrivatwritableAktive(sideMappe, side) {
			return false
		}
		if side == (sidste & SideRamme) {
			break
		}
	}
	return true
}

func MakeIntervalPrivatwritable(sideMappe uint32, address uint32, størrelse uint32) bool {
	if sideMappe == 0 {
		return false
	}
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	ok := makeIntervalPrivatwritableAktive(sideMappe, address, størrelse)
	satcr3(gammelcr3)
	return ok
}

func Satunsignedinteger32IndSideMappe(x uint32, address uint32, sideMappe uint32) {
	if sideMappe == 0 {
		return
	}
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	Satunsignedinteger32ataddress(x, address)
	satcr3(gammelcr3)
}

func GetVærdi(address uint32) uint32 {
	var orgVærdi uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVærdi
}
func GetVærdiIndSideMappe(address uint32, sideMappe uint32) uint32 {
	if sideMappe == 0 {
		return 0
	}
	gammelcr3 := getcr3()
	satcr3(sideMappe)
	v := GetVærdi(address)
	satcr3(gammelcr3)
	return v
}

var v uint32 = 0

func KopiérSideRammeBlok(xSideMappe uint32, ySideMappe uint32, vaddress uint32) {
	if xSideMappe == 0 || ySideMappe == 0 {
		return
	}
	gammelcr3 := getcr3()
	satcr3(xSideMappe)
	v = GetVærdi(vaddress)
	Satunsignedinteger32IndSideMappe(v, vaddress, ySideMappe)

	satcr3(gammelcr3)
}
