package paging

import unsafe "unsafe"
import . "prekid"
import . "memorijamanager"
import . "util"

type StranicaDirektorijentry_2 uintptr

const (
	StranicaPrisutno	uint32	= 0x001
	Stranicawritable	uint32	= 0x002
	StranicaKorisnik	uint32	= 0x004
	Stranicaframe		uint32	= 0xFFFFF000
	Stranicacow		uint32	= 0x200
)

func Postavibyteataddress(x byte, address uint32)
func Postaviunsignedinteger8ataddress(x uint8, address uint32)
func Postaviunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func postavicr3(stranicaDirektorij uint32)
func getcr3() uint32

type Paging struct {
	TPrekidhandler
}
type Tcowframemanager struct {
	mem		*TMemorijamanager
	refs		[]uint16
	framecount	uint32
}

var (
	StranicaDirektorijentry	uintptr
	StranicaTablicaentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (sam *Tcowframemanager) Init(mem *TMemorijamanager, framecount uint32) bool {
	sam.mem = mem
	sam.framecount = framecount
	referenceBajtova := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referencePokazivač := mem.Malloc(referenceBajtova)
	if referencePokazivač == nil {
		sam.refs = nil
		sam.framecount = 0
		return false
	}
	sam.refs = (*[1 << 28]uint16)(referencePokazivač)[:framecount:framecount]
	for i := uint32(0); i < framecount; i++ {
		sam.refs[i] = 0
	}
	return true
}

func (sam *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= sam.framecount || sam.refs == nil {
		return 0
	}
	return sam.refs[idx]
}

func (sam *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= sam.framecount || sam.refs == nil {
		return
	}
	if sam.refs[idx] == 0 {
		sam.refs[idx] = 2
	} else {
		sam.refs[idx]++
	}
}

func (sam *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= sam.framecount || sam.refs == nil || sam.refs[idx] == 0 {
		return
	}
	sam.refs[idx]--
}

func (sam *Paging) Init(stranicaDirektorijentry uintptr, stranicaTablicaentry uint32, memorijamanager *TMemorijamanager) {

	StranicaDirektorijentry = stranicaDirektorijentry
	StranicaTablicaentry = stranicaTablicaentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(memorijamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressPokazivač, _ := memorijamanager.Alignedmalloc(0x1000)
			if addressPokazivač == nil {
				return
			}
			address := uint32(uintptr(addressPokazivač))

			Postaviunsignedinteger32ataddress(address|0x87, uint32(stranicaDirektorijentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Postaviunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		stranicaDirektorijentry = stranicaDirektorijentry + 0x1000
	}

}
func (sam *Paging) SharedMemorijaregion() {

	stranicaDirektorijentry := StranicaDirektorijentry
	kStranicaDirektorijentry := StranicaDirektorijentry

	for i := uint32(1); i <= virtlen; i++ {

		stranicaDirektorijentry = stranicaDirektorijentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVrijednost(uint32(kStranicaDirektorijentry) + pde*4)
			v = (v & 0xFFFFF000)
			Postaviunsignedinteger32ataddress(v|0x87, uint32(stranicaDirektorijentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVrijednost(uint32(kStranicaDirektorijentry) + pde*4)
			v = (v & 0xFFFFF000)
			Postaviunsignedinteger32ataddress(v|0x87, uint32(stranicaDirektorijentry)+pde*4)

		}

	}
}
func (sam *Paging) Stranicafault(manager *TPrekidmanager) {
	prekidhandler = ručkapagingPrekid

	var address uintptr
	address = uintptr(unsafe.Pointer(&prekidhandler))
	sam.TPrekidhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var prekidhandler func(uint32) uint32

func ručkapagingPrekid(esp uint32) uint32 {
	if ResolveKopirajUključenoZapišifault() {
		return esp
	}
	return RučkafatalPrekidframe(esp, 0x0E)
}

func CloneaddressRazmaknicacow(izvorStranicaDirektorij uint32) uint32 {
	if AktivanMemorijamanager == nil || izvorStranicaDirektorij == 0 {
		return 0
	}
	odredištePokazivač, _ := AktivanMemorijamanager.Alignedmalloc(0x1000)
	if odredištePokazivač == nil {
		return 0
	}
	odredišteStranicaDirektorij := uint32(uintptr(odredištePokazivač))
	for i := uint32(0); i < 1024; i++ {
		Postaviunsignedinteger32ataddress(0, odredišteStranicaDirektorij+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		izvorpdeaddress := izvorStranicaDirektorij + pde*4
		izvorpde := GetVrijednost(izvorpdeaddress)
		if (izvorpde & StranicaPrisutno) == 0 {
			continue
		}
		if issharedpde(pde) {
			Postaviunsignedinteger32ataddress(izvorpde, odredišteStranicaDirektorij+pde*4)
			continue
		}

		odredišteptPokazivač, _ := AktivanMemorijamanager.Alignedmalloc(0x1000)
		if odredišteptPokazivač == nil {
			continue
		}
		izvorpt := izvorpde & Stranicaframe
		odredištept := uint32(uintptr(odredišteptPokazivač))
		Postaviunsignedinteger32ataddress((odredištept | (izvorpde & 0xFFF)), odredišteStranicaDirektorij+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := izvorpt + pte*4
			entry := GetVrijednost(pteaddress)
			if (entry & StranicaPrisutno) != 0 {
				if (entry & Stranicawritable) != 0 {
					entry = (entry &^ Stranicawritable) | Stranicacow
					Postaviunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & Stranicaframe)
				} else if (entry & Stranicacow) != 0 {
					cowframemanager.Increment(entry & Stranicaframe)
				}
			}
			Postaviunsignedinteger32ataddress(entry, odredištept+pte*4)
		}
	}
	ponovnoučitavanjecr3()
	return odredišteStranicaDirektorij
}

func ResolveKopirajUključenoZapišifault() bool {
	if AktivanMemorijamanager == nil {
		return false
	}
	faultaddress := getcr2()
	stranicaDirektorij := getcr3()
	pdeaddress := stranicaDirektorij + ((faultaddress>>22)&0x3FF)*4
	pde := GetVrijednost(pdeaddress)
	if (pde & StranicaPrisutno) == 0 {
		return false
	}
	pt := pde & Stranicaframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVrijednost(pteaddress)
	if (pte&Stranicacow) == 0 || (pte&StranicaPrisutno) == 0 {
		return false
	}
	oldframe := pte & Stranicaframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Postaviunsignedinteger32ataddress((pte|Stranicawritable)&^Stranicacow, pteaddress)
		ponovnoučitavanjecr3()
		return true
	}

	noviPokazivač, _ := AktivanMemorijamanager.Alignedmalloc(0x1000)
	if noviPokazivač == nil {
		return false
	}
	noviframe := uint32(uintptr(noviPokazivač)) & Stranicaframe

	izvor_2 := GetBajtovafromPokazivač(uintptr(faultaddress&Stranicaframe), 0x1000, 0x1000)
	odredište_2 := GetBajtovafromPokazivač(uintptr(noviframe), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowframemanager.Decrement(oldframe)
	Postaviunsignedinteger32ataddress((noviframe|(pte&0xFFF)|Stranicawritable)&^Stranicacow, pteaddress)
	ponovnoučitavanjecr3()
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

func ponovnoučitavanjecr3() {
	cr3 := getcr3()
	postavicr3(cr3)
}

func PostavibytePovećajStranicaDirektorij(x byte, address uint32, stranicaDirektorij uint32) {
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	Postavibyteataddress(x, address)
	postavicr3(oldcr3)
}

func PostaviBlokirajPovećajStranicaDirektorij(izvor_2 []byte, odredište_2 []byte, veličina uint32, stranicaDirektorij uint32) {
	if veličina == 0 || stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	makeOpsegPrivatnowritableTrenutno(stranicaDirektorij, uint32(uintptr(unsafe.Pointer(&odredište_2[0]))), veličina)

	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = izvor_2[i]
	}
	postavicr3(oldcr3)
}

func ZeroBlokirajPovećajStranicaDirektorij(address uint32, veličina uint32, stranicaDirektorij uint32) {
	if veličina == 0 || stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	makeOpsegPrivatnowritableTrenutno(stranicaDirektorij, address, veličina)
	odredište_2 := GetBajtovafromPokazivač(uintptr(address), int(veličina), int(veličina))
	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = 0
	}
	postavicr3(oldcr3)
}

func makeStranicaPrivatnowritableTrenutno(stranicaDirektorij uint32, virtualnoaddress uint32) bool {
	pde := GetVrijednost(stranicaDirektorij + ((virtualnoaddress>>22)&0x3FF)*4)
	if (pde & StranicaPrisutno) == 0 {
		return false
	}
	pteaddress := (pde & Stranicaframe) + ((virtualnoaddress>>12)&0x3FF)*4
	pte := GetVrijednost(pteaddress)
	if (pte & StranicaPrisutno) == 0 {
		return false
	}
	if (pte & Stranicacow) == 0 {
		return (pte & Stranicawritable) != 0
	}
	if AktivanMemorijamanager == nil {
		return false
	}
	noviPokazivač, _ := AktivanMemorijamanager.Alignedmalloc(0x1000)
	if noviPokazivač == nil {
		return false
	}
	noviframe := uint32(uintptr(noviPokazivač)) & Stranicaframe
	izvor_2 := GetBajtovafromPokazivač(uintptr(virtualnoaddress&Stranicaframe), 0x1000, 0x1000)
	odredište_2 := GetBajtovafromPokazivač(uintptr(noviframe), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowframemanager.Decrement(pte & Stranicaframe)
	Postaviunsignedinteger32ataddress((noviframe|(pte&0xFFF)|Stranicawritable)&^Stranicacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	ponovnoučitavanjecr3()
	return true
}

func makeOpsegPrivatnowritableTrenutno(stranicaDirektorij uint32, address uint32, veličina uint32) bool {
	if veličina == 0 {
		return true
	}
	zadnje := address + veličina - 1
	if zadnje < address {
		return false
	}
	for stranica := address & Stranicaframe; ; stranica += 0x1000 {
		if !makeStranicaPrivatnowritableTrenutno(stranicaDirektorij, stranica) {
			return false
		}
		if stranica == (zadnje & Stranicaframe) {
			break
		}
	}
	return true
}

func MakeOpsegPrivatnowritable(stranicaDirektorij uint32, address uint32, veličina uint32) bool {
	if stranicaDirektorij == 0 {
		return false
	}
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	uredu := makeOpsegPrivatnowritableTrenutno(stranicaDirektorij, address, veličina)
	postavicr3(oldcr3)
	return uredu
}

func Postaviunsignedinteger32PovećajStranicaDirektorij(x uint32, address uint32, stranicaDirektorij uint32) {
	if stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	Postaviunsignedinteger32ataddress(x, address)
	postavicr3(oldcr3)
}

func GetVrijednost(address uint32) uint32 {
	var orgVrijednost uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVrijednost
}
func GetVrijednostPovećajStranicaDirektorij(address uint32, stranicaDirektorij uint32) uint32 {
	if stranicaDirektorij == 0 {
		return 0
	}
	oldcr3 := getcr3()
	postavicr3(stranicaDirektorij)
	v := GetVrijednost(address)
	postavicr3(oldcr3)
	return v
}

var v uint32 = 0

func KopirajStranicaframeBlokiraj(xStranicaDirektorij uint32, yStranicaDirektorij uint32, vaddress uint32) {
	if xStranicaDirektorij == 0 || yStranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	postavicr3(xStranicaDirektorij)
	v = GetVrijednost(vaddress)
	Postaviunsignedinteger32PovećajStranicaDirektorij(v, vaddress, yStranicaDirektorij)

	postavicr3(oldcr3)
}
