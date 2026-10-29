/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "memorijamanager"
import . "util"

type StranicaDirektorijunos_2 uintptr

const (
	Stranicapresent		uint32	= 0x001
	Stranicawritable	uint32	= 0x002
	StranicaKorisnik	uint32	= 0x004
	StranicaOkvir		uint32	= 0xFFFFF000
	Stranicacow		uint32	= 0x200
)

func Skupbyteataddress(x byte, address uint32)
func Skupunsignedinteger8ataddress(x uint8, address uint32)
func Skupunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func skupcr3(stranicaDirektorij uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowOkvirmanager struct {
	mem		*TMemorijamanager
	refs		[]uint16
	okvircount	uint32
}

var (
	StranicaDirektorijunos	uintptr
	Stranicatableunos	uint32
	pdelen			uint32
	virtlen			uint32
	cowOkvirmanager		TcowOkvirmanager
)

func (self *TcowOkvirmanager) Init(mem *TMemorijamanager, okvircount uint32) bool {
	self.mem = mem
	self.okvircount = okvircount
	referenceBajtova := okvircount * uint32(unsafe.Sizeof(uint16(0)))
	referencepointer := mem.Malloc(referenceBajtova)
	if referencepointer == nil {
		self.refs = nil
		self.okvircount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referencepointer)[:okvircount:okvircount]
	for i := uint32(0); i < okvircount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowOkvirmanager) Reference(okvir uint32) uint16 {
	idx := okvir >> 12
	if idx >= self.okvircount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowOkvirmanager) Increment(okvir uint32) {
	idx := okvir >> 12
	if idx >= self.okvircount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowOkvirmanager) Decrement(okvir uint32) {
	idx := okvir >> 12
	if idx >= self.okvircount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(stranicaDirektorijunos uintptr, stranicatableunos uint32, memorijamanager *TMemorijamanager) {

	StranicaDirektorijunos = stranicaDirektorijunos
	Stranicatableunos = stranicatableunos

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowOkvirmanager.Init(memorijamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addresspointer, _ := memorijamanager.Alignedmalloc(0x1000)
			if addresspointer == nil {
				return
			}
			address := uint32(uintptr(addresspointer))

			Skupunsignedinteger32ataddress(address|0x87, uint32(stranicaDirektorijunos)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Skupunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		stranicaDirektorijunos = stranicaDirektorijunos + 0x1000
	}

}
func (self *Paging) SharedMemorijaregion() {

	stranicaDirektorijunos := StranicaDirektorijunos
	kStranicaDirektorijunos := StranicaDirektorijunos

	for i := uint32(1); i <= virtlen; i++ {

		stranicaDirektorijunos = stranicaDirektorijunos + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVrijednost(uint32(kStranicaDirektorijunos) + pde*4)
			v = (v & 0xFFFFF000)
			Skupunsignedinteger32ataddress(v|0x87, uint32(stranicaDirektorijunos)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVrijednost(uint32(kStranicaDirektorijunos) + pde*4)
			v = (v & 0xFFFFF000)
			Skupunsignedinteger32ataddress(v|0x87, uint32(stranicaDirektorijunos)+pde*4)

		}

	}
}
func (self *Paging) Stranicafault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveKopirajUključenPišifault() {
		return esp
	}
	return HandlefatalinterruptOkvir(esp, 0x0E)
}

func Cloneaddressspacecow(izvorStranicaDirektorij uint32) uint32 {
	if ActiveMemorijamanager == nil || izvorStranicaDirektorij == 0 {
		return 0
	}
	odredištepointer, _ := ActiveMemorijamanager.Alignedmalloc(0x1000)
	if odredištepointer == nil {
		return 0
	}
	odredišteStranicaDirektorij := uint32(uintptr(odredištepointer))
	for i := uint32(0); i < 1024; i++ {
		Skupunsignedinteger32ataddress(0, odredišteStranicaDirektorij+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		izvorpdeaddress := izvorStranicaDirektorij + pde*4
		izvorpde := GetVrijednost(izvorpdeaddress)
		if (izvorpde & Stranicapresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Skupunsignedinteger32ataddress(izvorpde, odredišteStranicaDirektorij+pde*4)
			continue
		}

		odredišteptpointer, _ := ActiveMemorijamanager.Alignedmalloc(0x1000)
		if odredišteptpointer == nil {
			continue
		}
		izvorpt := izvorpde & StranicaOkvir
		odredištept := uint32(uintptr(odredišteptpointer))
		Skupunsignedinteger32ataddress((odredištept | (izvorpde & 0xFFF)), odredišteStranicaDirektorij+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := izvorpt + pte*4
			unos := GetVrijednost(pteaddress)
			if (unos & Stranicapresent) != 0 {
				if (unos & Stranicawritable) != 0 {
					unos = (unos &^ Stranicawritable) | Stranicacow
					Skupunsignedinteger32ataddress(unos, pteaddress)
					cowOkvirmanager.Increment(unos & StranicaOkvir)
				} else if (unos & Stranicacow) != 0 {
					cowOkvirmanager.Increment(unos & StranicaOkvir)
				}
			}
			Skupunsignedinteger32ataddress(unos, odredištept+pte*4)
		}
	}
	učitajponovocr3()
	return odredišteStranicaDirektorij
}

func ResolveKopirajUključenPišifault() bool {
	if ActiveMemorijamanager == nil {
		return false
	}
	faultaddress := getcr2()
	stranicaDirektorij := getcr3()
	pdeaddress := stranicaDirektorij + ((faultaddress>>22)&0x3FF)*4
	pde := GetVrijednost(pdeaddress)
	if (pde & Stranicapresent) == 0 {
		return false
	}
	pt := pde & StranicaOkvir
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVrijednost(pteaddress)
	if (pte&Stranicacow) == 0 || (pte&Stranicapresent) == 0 {
		return false
	}
	oldOkvir := pte & StranicaOkvir
	if cowOkvirmanager.Reference(oldOkvir) <= 1 {
		Skupunsignedinteger32ataddress((pte|Stranicawritable)&^Stranicacow, pteaddress)
		učitajponovocr3()
		return true
	}

	novapointer, _ := ActiveMemorijamanager.Alignedmalloc(0x1000)
	if novapointer == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novapointer)) & StranicaOkvir

	izvor_2 := GetBajtovafrompointer(uintptr(faultaddress&StranicaOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovafrompointer(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(oldOkvir)
	Skupunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|Stranicawritable)&^Stranicacow, pteaddress)
	učitajponovocr3()
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

func učitajponovocr3() {
	cr3 := getcr3()
	skupcr3(cr3)
}

func SkupbytePrimljenoStranicaDirektorij(x byte, address uint32, stranicaDirektorij uint32) {
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	Skupbyteataddress(x, address)
	skupcr3(oldcr3)
}

func SkupblokPrimljenoStranicaDirektorij(izvor_2 []byte, odredište_2 []byte, veličina uint32, stranicaDirektorij uint32) {
	if veličina == 0 || stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	makerangePrivatnowritablecurrent(stranicaDirektorij, uint32(uintptr(unsafe.Pointer(&odredište_2[0]))), veličina)

	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = izvor_2[i]
	}
	skupcr3(oldcr3)
}

func ZeroblokPrimljenoStranicaDirektorij(address uint32, veličina uint32, stranicaDirektorij uint32) {
	if veličina == 0 || stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	makerangePrivatnowritablecurrent(stranicaDirektorij, address, veličina)
	odredište_2 := GetBajtovafrompointer(uintptr(address), int(veličina), int(veličina))
	for i := uint32(0); i < veličina; i++ {
		odredište_2[i] = 0
	}
	skupcr3(oldcr3)
}

func makeStranicaPrivatnowritablecurrent(stranicaDirektorij uint32, virtuelnoaddress uint32) bool {
	pde := GetVrijednost(stranicaDirektorij + ((virtuelnoaddress>>22)&0x3FF)*4)
	if (pde & Stranicapresent) == 0 {
		return false
	}
	pteaddress := (pde & StranicaOkvir) + ((virtuelnoaddress>>12)&0x3FF)*4
	pte := GetVrijednost(pteaddress)
	if (pte & Stranicapresent) == 0 {
		return false
	}
	if (pte & Stranicacow) == 0 {
		return (pte & Stranicawritable) != 0
	}
	if ActiveMemorijamanager == nil {
		return false
	}
	novapointer, _ := ActiveMemorijamanager.Alignedmalloc(0x1000)
	if novapointer == nil {
		return false
	}
	novaOkvir := uint32(uintptr(novapointer)) & StranicaOkvir
	izvor_2 := GetBajtovafrompointer(uintptr(virtuelnoaddress&StranicaOkvir), 0x1000, 0x1000)
	odredište_2 := GetBajtovafrompointer(uintptr(novaOkvir), 0x1000, 0x1000)
	copy(odredište_2, izvor_2)
	cowOkvirmanager.Decrement(pte & StranicaOkvir)
	Skupunsignedinteger32ataddress((novaOkvir|(pte&0xFFF)|Stranicawritable)&^Stranicacow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	učitajponovocr3()
	return true
}

func makerangePrivatnowritablecurrent(stranicaDirektorij uint32, address uint32, veličina uint32) bool {
	if veličina == 0 {
		return true
	}
	zadnja := address + veličina - 1
	if zadnja < address {
		return false
	}
	for stranica := address & StranicaOkvir; ; stranica += 0x1000 {
		if !makeStranicaPrivatnowritablecurrent(stranicaDirektorij, stranica) {
			return false
		}
		if stranica == (zadnja & StranicaOkvir) {
			break
		}
	}
	return true
}

func MakerangePrivatnowritable(stranicaDirektorij uint32, address uint32, veličina uint32) bool {
	if stranicaDirektorij == 0 {
		return false
	}
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	uredu := makerangePrivatnowritablecurrent(stranicaDirektorij, address, veličina)
	skupcr3(oldcr3)
	return uredu
}

func Skupunsignedinteger32PrimljenoStranicaDirektorij(x uint32, address uint32, stranicaDirektorij uint32) {
	if stranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	Skupunsignedinteger32ataddress(x, address)
	skupcr3(oldcr3)
}

func GetVrijednost(address uint32) uint32 {
	var orgVrijednost uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVrijednost
}
func GetVrijednostPrimljenoStranicaDirektorij(address uint32, stranicaDirektorij uint32) uint32 {
	if stranicaDirektorij == 0 {
		return 0
	}
	oldcr3 := getcr3()
	skupcr3(stranicaDirektorij)
	v := GetVrijednost(address)
	skupcr3(oldcr3)
	return v
}

var v uint32 = 0

func KopirajStranicaOkvirblok(xStranicaDirektorij uint32, yStranicaDirektorij uint32, vaddress uint32) {
	if xStranicaDirektorij == 0 || yStranicaDirektorij == 0 {
		return
	}
	oldcr3 := getcr3()
	skupcr3(xStranicaDirektorij)
	v = GetVrijednost(vaddress)
	Skupunsignedinteger32PrimljenoStranicaDirektorij(v, vaddress, yStranicaDirektorij)

	skupcr3(oldcr3)
}
