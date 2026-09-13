package paging

import unsafe "unsafe"
import . "keskeytys"
import . "muistimanager"
import . "util"

type SivuKansiohakusana_2 uintptr

const (
	SivuLiitetty	uint32	= 0x001
	Sivuwritable	uint32	= 0x002
	SivuKäyttäjä	uint32	= 0x004
	SivuKehys	uint32	= 0xFFFFF000
	Sivucow		uint32	= 0x200
)

func Asetabyteataddress(x byte, address uint32)
func Asetaunsignedinteger8ataddress(x uint8, address uint32)
func Asetaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func asetacr3(sivuhakemisto uint32)
func getcr3() uint32

type Paging struct {
	TKeskeytyshandler
}
type TcowKehysmanager struct {
	mem		*TMuistimanager
	refs		[]uint16
	kehyscount	uint32
}

var (
	SivuKansiohakusana	uintptr
	SivuTaulukkohakusana	uint32
	pdelen			uint32
	virtlen			uint32
	cowKehysmanager		TcowKehysmanager
)

func (itse *TcowKehysmanager) Init(mem *TMuistimanager, kehyscount uint32) bool {
	itse.mem = mem
	itse.kehyscount = kehyscount
	referencetavua := kehyscount * uint32(unsafe.Sizeof(uint16(0)))
	referenceOsoitin := mem.Varaa_muistia(referencetavua)
	if referenceOsoitin == nil {
		itse.refs = nil
		itse.kehyscount = 0
		return false
	}
	itse.refs = (*[1 << 28]uint16)(referenceOsoitin)[:kehyscount:kehyscount]
	for i := uint32(0); i < kehyscount; i++ {
		itse.refs[i] = 0
	}
	return true
}

func (itse *TcowKehysmanager) Reference(kehys uint32) uint16 {
	idx := kehys >> 12
	if idx >= itse.kehyscount || itse.refs == nil {
		return 0
	}
	return itse.refs[idx]
}

func (itse *TcowKehysmanager) Increment(kehys uint32) {
	idx := kehys >> 12
	if idx >= itse.kehyscount || itse.refs == nil {
		return
	}
	if itse.refs[idx] == 0 {
		itse.refs[idx] = 2
	} else {
		itse.refs[idx]++
	}
}

func (itse *TcowKehysmanager) Decrement(kehys uint32) {
	idx := kehys >> 12
	if idx >= itse.kehyscount || itse.refs == nil || itse.refs[idx] == 0 {
		return
	}
	itse.refs[idx]--
}

func (itse *Paging) Init(sivuKansiohakusana uintptr, sivuTaulukkohakusana uint32, muistimanager *TMuistimanager) {

	SivuKansiohakusana = sivuKansiohakusana
	SivuTaulukkohakusana = sivuTaulukkohakusana

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowKehysmanager.Init(muistimanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressOsoitin, _ := muistimanager.Alignedmalloc(0x1000)
			if addressOsoitin == nil {
				return
			}
			address := uint32(uintptr(addressOsoitin))

			Asetaunsignedinteger32ataddress(address|0x87, uint32(sivuKansiohakusana)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Asetaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sivuKansiohakusana = sivuKansiohakusana + 0x1000
	}

}
func (itse *Paging) SharedMuistiregion() {

	sivuKansiohakusana := SivuKansiohakusana
	kSivuKansiohakusana := SivuKansiohakusana

	for i := uint32(1); i <= virtlen; i++ {

		sivuKansiohakusana = sivuKansiohakusana + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetArvo(uint32(kSivuKansiohakusana) + pde*4)
			v = (v & 0xFFFFF000)
			Asetaunsignedinteger32ataddress(v|0x87, uint32(sivuKansiohakusana)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetArvo(uint32(kSivuKansiohakusana) + pde*4)
			v = (v & 0xFFFFF000)
			Asetaunsignedinteger32ataddress(v|0x87, uint32(sivuKansiohakusana)+pde*4)

		}

	}
}
func (itse *Paging) Sivufault(manager *TKeskeytysmanager) {
	keskeytyshandler = kahvapagingKeskeytys

	var address uintptr
	address = uintptr(unsafe.Pointer(&keskeytyshandler))
	itse.TKeskeytyshandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var keskeytyshandler func(uint32) uint32

func kahvapagingKeskeytys(esp uint32) uint32 {
	if ResolveKopioiPäälläKirjoitusfault() {
		return esp
	}
	return KahvafatalKeskeytysKehys(esp, 0x0E)
}

func CloneaddressVälicow(lähdeSivuKansio uint32) uint32 {
	if AktiivinenMuistimanager == nil || lähdeSivuKansio == 0 {
		return 0
	}
	kohdeOsoitin, _ := AktiivinenMuistimanager.Alignedmalloc(0x1000)
	if kohdeOsoitin == nil {
		return 0
	}
	kohdeSivuKansio := uint32(uintptr(kohdeOsoitin))
	for i := uint32(0); i < 1024; i++ {
		Asetaunsignedinteger32ataddress(0, kohdeSivuKansio+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		lähdepdeaddress := lähdeSivuKansio + pde*4
		lähdepde := GetArvo(lähdepdeaddress)
		if (lähdepde & SivuLiitetty) == 0 {
			continue
		}
		if issharedpde(pde) {
			Asetaunsignedinteger32ataddress(lähdepde, kohdeSivuKansio+pde*4)
			continue
		}

		kohdeptOsoitin, _ := AktiivinenMuistimanager.Alignedmalloc(0x1000)
		if kohdeptOsoitin == nil {
			continue
		}
		lähdept := lähdepde & SivuKehys
		kohdept := uint32(uintptr(kohdeptOsoitin))
		Asetaunsignedinteger32ataddress((kohdept | (lähdepde & 0xFFF)), kohdeSivuKansio+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := lähdept + pte*4
			hakusana := GetArvo(pteaddress)
			if (hakusana & SivuLiitetty) != 0 {
				if (hakusana & Sivuwritable) != 0 {
					hakusana = (hakusana &^ Sivuwritable) | Sivucow
					Asetaunsignedinteger32ataddress(hakusana, pteaddress)
					cowKehysmanager.Increment(hakusana & SivuKehys)
				} else if (hakusana & Sivucow) != 0 {
					cowKehysmanager.Increment(hakusana & SivuKehys)
				}
			}
			Asetaunsignedinteger32ataddress(hakusana, kohdept+pte*4)
		}
	}
	lataauudelleencr3()
	return kohdeSivuKansio
}

func ResolveKopioiPäälläKirjoitusfault() bool {
	if AktiivinenMuistimanager == nil {
		return false
	}
	faultaddress := getcr2()
	sivuhakemisto := getcr3()
	pdeaddress := sivuhakemisto + ((faultaddress>>22)&0x3FF)*4
	pde := GetArvo(pdeaddress)
	if (pde & SivuLiitetty) == 0 {
		return false
	}
	pt := pde & SivuKehys
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetArvo(pteaddress)
	if (pte&Sivucow) == 0 || (pte&SivuLiitetty) == 0 {
		return false
	}
	oldKehys := pte & SivuKehys
	if cowKehysmanager.Reference(oldKehys) <= 1 {
		Asetaunsignedinteger32ataddress((pte|Sivuwritable)&^Sivucow, pteaddress)
		lataauudelleencr3()
		return true
	}

	uusiOsoitin, _ := AktiivinenMuistimanager.Alignedmalloc(0x1000)
	if uusiOsoitin == nil {
		return false
	}
	uusiKehys := uint32(uintptr(uusiOsoitin)) & SivuKehys

	lähde_2 := GettavualähteestäOsoitin(uintptr(faultaddress&SivuKehys), 0x1000, 0x1000)
	kohde_2 := GettavualähteestäOsoitin(uintptr(uusiKehys), 0x1000, 0x1000)
	copy(kohde_2, lähde_2)
	cowKehysmanager.Decrement(oldKehys)
	Asetaunsignedinteger32ataddress((uusiKehys|(pte&0xFFF)|Sivuwritable)&^Sivucow, pteaddress)
	lataauudelleencr3()
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

func lataauudelleencr3() {
	cr3 := getcr3()
	asetacr3(cr3)
}

func AsetabyteSaapuvaSivuKansio(x byte, address uint32, sivuhakemisto uint32) {
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	Asetabyteataddress(x, address)
	asetacr3(oldcr3)
}

func AsetaLohkoSaapuvaSivuKansio(lähde_2 []byte, kohde_2 []byte, koko uint32, sivuhakemisto uint32) {
	if koko == 0 || sivuhakemisto == 0 {
		return
	}
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	makeAlueYksityinenwritableNykyinen(sivuhakemisto, uint32(uintptr(unsafe.Pointer(&kohde_2[0]))), koko)

	for i := uint32(0); i < koko; i++ {
		kohde_2[i] = lähde_2[i]
	}
	asetacr3(oldcr3)
}

func ZeroLohkoSaapuvaSivuKansio(address uint32, koko uint32, sivuhakemisto uint32) {
	if koko == 0 || sivuhakemisto == 0 {
		return
	}
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	makeAlueYksityinenwritableNykyinen(sivuhakemisto, address, koko)
	kohde_2 := GettavualähteestäOsoitin(uintptr(address), int(koko), int(koko))
	for i := uint32(0); i < koko; i++ {
		kohde_2[i] = 0
	}
	asetacr3(oldcr3)
}

func makeSivuYksityinenwritableNykyinen(sivuhakemisto uint32, virtuaalinenaddress uint32) bool {
	pde := GetArvo(sivuhakemisto + ((virtuaalinenaddress>>22)&0x3FF)*4)
	if (pde & SivuLiitetty) == 0 {
		return false
	}
	pteaddress := (pde & SivuKehys) + ((virtuaalinenaddress>>12)&0x3FF)*4
	pte := GetArvo(pteaddress)
	if (pte & SivuLiitetty) == 0 {
		return false
	}
	if (pte & Sivucow) == 0 {
		return (pte & Sivuwritable) != 0
	}
	if AktiivinenMuistimanager == nil {
		return false
	}
	uusiOsoitin, _ := AktiivinenMuistimanager.Alignedmalloc(0x1000)
	if uusiOsoitin == nil {
		return false
	}
	uusiKehys := uint32(uintptr(uusiOsoitin)) & SivuKehys
	lähde_2 := GettavualähteestäOsoitin(uintptr(virtuaalinenaddress&SivuKehys), 0x1000, 0x1000)
	kohde_2 := GettavualähteestäOsoitin(uintptr(uusiKehys), 0x1000, 0x1000)
	copy(kohde_2, lähde_2)
	cowKehysmanager.Decrement(pte & SivuKehys)
	Asetaunsignedinteger32ataddress((uusiKehys|(pte&0xFFF)|Sivuwritable)&^Sivucow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	lataauudelleencr3()
	return true
}

func makeAlueYksityinenwritableNykyinen(sivuhakemisto uint32, address uint32, koko uint32) bool {
	if koko == 0 {
		return true
	}
	viimeinen := address + koko - 1
	if viimeinen < address {
		return false
	}
	for sivu := address & SivuKehys; ; sivu += 0x1000 {
		if !makeSivuYksityinenwritableNykyinen(sivuhakemisto, sivu) {
			return false
		}
		if sivu == (viimeinen & SivuKehys) {
			break
		}
	}
	return true
}

func MakeAlueYksityinenwritable(sivuhakemisto uint32, address uint32, koko uint32) bool {
	if sivuhakemisto == 0 {
		return false
	}
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	ok := makeAlueYksityinenwritableNykyinen(sivuhakemisto, address, koko)
	asetacr3(oldcr3)
	return ok
}

func Asetaunsignedinteger32SaapuvaSivuKansio(x uint32, address uint32, sivuhakemisto uint32) {
	if sivuhakemisto == 0 {
		return
	}
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	Asetaunsignedinteger32ataddress(x, address)
	asetacr3(oldcr3)
}

func GetArvo(address uint32) uint32 {
	var orgArvo uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgArvo
}
func GetArvoSaapuvaSivuKansio(address uint32, sivuhakemisto uint32) uint32 {
	if sivuhakemisto == 0 {
		return 0
	}
	oldcr3 := getcr3()
	asetacr3(sivuhakemisto)
	v := GetArvo(address)
	asetacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopioiSivuKehysLohko(xSivuKansio uint32, ySivuKansio uint32, vaddress uint32) {
	if xSivuKansio == 0 || ySivuKansio == 0 {
		return
	}
	oldcr3 := getcr3()
	asetacr3(xSivuKansio)
	v = GetArvo(vaddress)
	Asetaunsignedinteger32SaapuvaSivuKansio(v, vaddress, ySivuKansio)

	asetacr3(oldcr3)
}
