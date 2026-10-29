/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "přerušení"
import . "paměťmanager"
import . "util"

type StránkaadresářZáznam_2 uintptr

const (
	StránkaSoučasný	uint32	= 0x001
	Stránkawritable	uint32	= 0x002
	StránkaUživatel	uint32	= 0x004
	StránkaRám	uint32	= 0xFFFFF000
	Stránkacow	uint32	= 0x200
)

func NastavitbyteatAdresa(x byte, adresa uint32)
func Nastavitunsignedinteger8atAdresa(x uint8, adresa uint32)
func Nastavitunsignedinteger32atAdresa(x uint32, adresa uint32)

func getcr2() uint32

func nastavitcr3(adresář_stránek uint32)
func getcr3() uint32

type Paging struct {
	TPřerušeníhandler
}
type TcowRámmanager struct {
	mem		*TPaměťmanager
	refs		[]uint16
	rámPočet	uint32
}

var (
	StránkaadresářZáznam	uintptr
	StránkaTabulkaZáznam	uint32
	pdelen			uint32
	virtlen			uint32
	cowRámmanager		TcowRámmanager
)

func (self *TcowRámmanager) Init(mem *TPaměťmanager, rámPočet uint32) bool {
	self.mem = mem
	self.rámPočet = rámPočet
	referenceBytů := rámPočet * uint32(unsafe.Sizeof(uint16(0)))
	referenceKurzor := mem.Přidělit_paměť(referenceBytů)
	if referenceKurzor == nil {
		self.refs = nil
		self.rámPočet = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceKurzor)[:rámPočet:rámPočet]
	for i := uint32(0); i < rámPočet; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *TcowRámmanager) Reference(rám uint32) uint16 {
	idx := rám >> 12
	if idx >= self.rámPočet || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *TcowRámmanager) Increment(rám uint32) {
	idx := rám >> 12
	if idx >= self.rámPočet || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *TcowRámmanager) Decrement(rám uint32) {
	idx := rám >> 12
	if idx >= self.rámPočet || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(stránkaadresářZáznam uintptr, stránkaTabulkaZáznam uint32, paměťmanager *TPaměťmanager) {

	StránkaadresářZáznam = stránkaadresářZáznam
	StránkaTabulkaZáznam = stránkaTabulkaZáznam

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRámmanager.Init(paměťmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			adresaKurzor, _ := paměťmanager.Alignedmalloc(0x1000)
			if adresaKurzor == nil {
				return
			}
			adresa := uint32(uintptr(adresaKurzor))

			Nastavitunsignedinteger32atAdresa(adresa|0x87, uint32(stránkaadresářZáznam)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Nastavitunsignedinteger32atAdresa((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, adresa+pte*4)
			}
		}
		stránkaadresářZáznam = stránkaadresářZáznam + 0x1000
	}

}
func (self *Paging) SharedPaměťregion() {

	stránkaadresářZáznam := StránkaadresářZáznam
	kStránkaadresářZáznam := StránkaadresářZáznam

	for i := uint32(1); i <= virtlen; i++ {

		stránkaadresářZáznam = stránkaadresářZáznam + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetHodnota(uint32(kStránkaadresářZáznam) + pde*4)
			v = (v & 0xFFFFF000)
			Nastavitunsignedinteger32atAdresa(v|0x87, uint32(stránkaadresářZáznam)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetHodnota(uint32(kStránkaadresářZáznam) + pde*4)
			v = (v & 0xFFFFF000)
			Nastavitunsignedinteger32atAdresa(v|0x87, uint32(stránkaadresářZáznam)+pde*4)

		}

	}
}
func (self *Paging) Stránkafault(manager *TPřerušenímanager) {
	přerušeníhandler = úchytkapagingPřerušení

	var adresa uintptr
	adresa = uintptr(unsafe.Pointer(&přerušeníhandler))
	self.TPřerušeníhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), adresa)
}

var přerušeníhandler func(uint32) uint32

func úchytkapagingPřerušení(esp uint32) uint32 {
	if ResolveKopírovatZapnutoZápisfault() {
		return esp
	}
	return ÚchytkafatalPřerušeníRám(esp, 0x0E)
}

func CloneAdresaMezeracow(zdrojStránkaadresář uint32) uint32 {
	if AktivníPaměťmanager == nil || zdrojStránkaadresář == 0 {
		return 0
	}
	cílKurzor, _ := AktivníPaměťmanager.Alignedmalloc(0x1000)
	if cílKurzor == nil {
		return 0
	}
	cílStránkaadresář := uint32(uintptr(cílKurzor))
	for i := uint32(0); i < 1024; i++ {
		Nastavitunsignedinteger32atAdresa(0, cílStránkaadresář+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		zdrojpdeAdresa := zdrojStránkaadresář + pde*4
		zdrojpde := GetHodnota(zdrojpdeAdresa)
		if (zdrojpde & StránkaSoučasný) == 0 {
			continue
		}
		if issharedpde(pde) {
			Nastavitunsignedinteger32atAdresa(zdrojpde, cílStránkaadresář+pde*4)
			continue
		}

		cílptKurzor, _ := AktivníPaměťmanager.Alignedmalloc(0x1000)
		if cílptKurzor == nil {
			continue
		}
		zdrojpt := zdrojpde & StránkaRám
		cílpt := uint32(uintptr(cílptKurzor))
		Nastavitunsignedinteger32atAdresa((cílpt | (zdrojpde & 0xFFF)), cílStránkaadresář+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteAdresa := zdrojpt + pte*4
			záznam := GetHodnota(pteAdresa)
			if (záznam & StránkaSoučasný) != 0 {
				if (záznam & Stránkawritable) != 0 {
					záznam = (záznam &^ Stránkawritable) | Stránkacow
					Nastavitunsignedinteger32atAdresa(záznam, pteAdresa)
					cowRámmanager.Increment(záznam & StránkaRám)
				} else if (záznam & Stránkacow) != 0 {
					cowRámmanager.Increment(záznam & StránkaRám)
				}
			}
			Nastavitunsignedinteger32atAdresa(záznam, cílpt+pte*4)
		}
	}
	znovunačístcr3()
	return cílStránkaadresář
}

func ResolveKopírovatZapnutoZápisfault() bool {
	if AktivníPaměťmanager == nil {
		return false
	}
	faultAdresa := getcr2()
	adresář_stránek := getcr3()
	pdeAdresa := adresář_stránek + ((faultAdresa>>22)&0x3FF)*4
	pde := GetHodnota(pdeAdresa)
	if (pde & StránkaSoučasný) == 0 {
		return false
	}
	pt := pde & StránkaRám
	pteAdresa := pt + ((faultAdresa>>12)&0x3FF)*4
	pte := GetHodnota(pteAdresa)
	if (pte&Stránkacow) == 0 || (pte&StránkaSoučasný) == 0 {
		return false
	}
	oldRám := pte & StránkaRám
	if cowRámmanager.Reference(oldRám) <= 1 {
		Nastavitunsignedinteger32atAdresa((pte|Stránkawritable)&^Stránkacow, pteAdresa)
		znovunačístcr3()
		return true
	}

	novýKurzor, _ := AktivníPaměťmanager.Alignedmalloc(0x1000)
	if novýKurzor == nil {
		return false
	}
	novýRám := uint32(uintptr(novýKurzor)) & StránkaRám

	zdroj_2 := GetBytůzKurzor(uintptr(faultAdresa&StránkaRám), 0x1000, 0x1000)
	cíl_2 := GetBytůzKurzor(uintptr(novýRám), 0x1000, 0x1000)
	copy(cíl_2, zdroj_2)
	cowRámmanager.Decrement(oldRám)
	Nastavitunsignedinteger32atAdresa((novýRám|(pte&0xFFF)|Stránkawritable)&^Stránkacow, pteAdresa)
	znovunačístcr3()
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

func znovunačístcr3() {
	cr3 := getcr3()
	nastavitcr3(cr3)
}

func NastavitbyteVstupStránkaadresář(x byte, adresa uint32, adresář_stránek uint32) {
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	NastavitbyteatAdresa(x, adresa)
	nastavitcr3(oldcr3)
}

func NastavitBlokovýVstupStránkaadresář(zdroj_2 []byte, cíl_2 []byte, velikost uint32, adresář_stránek uint32) {
	if velikost == 0 || adresář_stránek == 0 {
		return
	}
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	makeRozsahPrivátníwritableSoučasný(adresář_stránek, uint32(uintptr(unsafe.Pointer(&cíl_2[0]))), velikost)

	for i := uint32(0); i < velikost; i++ {
		cíl_2[i] = zdroj_2[i]
	}
	nastavitcr3(oldcr3)
}

func NulaBlokovýVstupStránkaadresář(adresa uint32, velikost uint32, adresář_stránek uint32) {
	if velikost == 0 || adresář_stránek == 0 {
		return
	}
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	makeRozsahPrivátníwritableSoučasný(adresář_stránek, adresa, velikost)
	cíl_2 := GetBytůzKurzor(uintptr(adresa), int(velikost), int(velikost))
	for i := uint32(0); i < velikost; i++ {
		cíl_2[i] = 0
	}
	nastavitcr3(oldcr3)
}

func makeStránkaPrivátníwritableSoučasný(adresář_stránek uint32, virtuálníAdresa uint32) bool {
	pde := GetHodnota(adresář_stránek + ((virtuálníAdresa>>22)&0x3FF)*4)
	if (pde & StránkaSoučasný) == 0 {
		return false
	}
	pteAdresa := (pde & StránkaRám) + ((virtuálníAdresa>>12)&0x3FF)*4
	pte := GetHodnota(pteAdresa)
	if (pte & StránkaSoučasný) == 0 {
		return false
	}
	if (pte & Stránkacow) == 0 {
		return (pte & Stránkawritable) != 0
	}
	if AktivníPaměťmanager == nil {
		return false
	}
	novýKurzor, _ := AktivníPaměťmanager.Alignedmalloc(0x1000)
	if novýKurzor == nil {
		return false
	}
	novýRám := uint32(uintptr(novýKurzor)) & StránkaRám
	zdroj_2 := GetBytůzKurzor(uintptr(virtuálníAdresa&StránkaRám), 0x1000, 0x1000)
	cíl_2 := GetBytůzKurzor(uintptr(novýRám), 0x1000, 0x1000)
	copy(cíl_2, zdroj_2)
	cowRámmanager.Decrement(pte & StránkaRám)
	Nastavitunsignedinteger32atAdresa((novýRám|(pte&0xFFF)|Stránkawritable)&^Stránkacow, pteAdresa)
	// Publish the new physical frame before writing through its virtual address.
	znovunačístcr3()
	return true
}

func makeRozsahPrivátníwritableSoučasný(adresář_stránek uint32, adresa uint32, velikost uint32) bool {
	if velikost == 0 {
		return true
	}
	poslední := adresa + velikost - 1
	if poslední < adresa {
		return false
	}
	for stránka := adresa & StránkaRám; ; stránka += 0x1000 {
		if !makeStránkaPrivátníwritableSoučasný(adresář_stránek, stránka) {
			return false
		}
		if stránka == (poslední & StránkaRám) {
			break
		}
	}
	return true
}

func MakeRozsahPrivátníwritable(adresář_stránek uint32, adresa uint32, velikost uint32) bool {
	if adresář_stránek == 0 {
		return false
	}
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	budiž := makeRozsahPrivátníwritableSoučasný(adresář_stránek, adresa, velikost)
	nastavitcr3(oldcr3)
	return budiž
}

func Nastavitunsignedinteger32VstupStránkaadresář(x uint32, adresa uint32, adresář_stránek uint32) {
	if adresář_stránek == 0 {
		return
	}
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	Nastavitunsignedinteger32atAdresa(x, adresa)
	nastavitcr3(oldcr3)
}

func GetHodnota(adresa uint32) uint32 {
	var orgHodnota uint32 = *(*uint32)(unsafe.Pointer(uintptr(adresa)))
	return orgHodnota
}
func GetHodnotaVstupStránkaadresář(adresa uint32, adresář_stránek uint32) uint32 {
	if adresář_stránek == 0 {
		return 0
	}
	oldcr3 := getcr3()
	nastavitcr3(adresář_stránek)
	v := GetHodnota(adresa)
	nastavitcr3(oldcr3)
	return v
}

var v uint32 = 0

func KopírovatStránkaRámBlokový(xStránkaadresář uint32, yStránkaadresář uint32, vAdresa uint32) {
	if xStránkaadresář == 0 || yStránkaadresář == 0 {
		return
	}
	oldcr3 := getcr3()
	nastavitcr3(xStránkaadresář)
	v = GetHodnota(vAdresa)
	Nastavitunsignedinteger32VstupStránkaadresář(v, vAdresa, yStránkaadresář)

	nastavitcr3(oldcr3)
}
