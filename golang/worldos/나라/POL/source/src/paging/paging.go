/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "przerwanie"
import . "pamięćmanager"
import . "util"

type StronaKatalogwpis_2 uintptr

const (
	StronaObecny		uint32	= 0x001
	Stronawritable		uint32	= 0x002
	StronaUżytkownik	uint32	= 0x004
	StronaRamka		uint32	= 0xFFFFF000
	Stronacow		uint32	= 0x200
)

func ZbiórbyteatAdres(x byte, adres uint32)
func Zbiórunsignedinteger8atAdres(x uint8, adres uint32)
func Zbiórunsignedinteger32atAdres(x uint32, adres uint32)

func getcr2() uint32

func zbiórcr3(katalog_stron uint32)
func getcr3() uint32

type Paging struct {
	TPrzerwaniehandler
}
type TcowRamkamanager struct {
	mem		*TPamięćmanager
	refs		[]uint16
	ramkaLiczba	uint32
}

var (
	StronaKatalogwpis	uintptr
	StronaTabelawpis	uint32
	pdelen			uint32
	virtlen			uint32
	cowRamkamanager		TcowRamkamanager
)

func (bieżący *TcowRamkamanager) Init(mem *TPamięćmanager, ramkaLiczba uint32) bool {
	bieżący.mem = mem
	bieżący.ramkaLiczba = ramkaLiczba
	referenceBajty := ramkaLiczba * uint32(unsafe.Sizeof(uint16(0)))
	referenceKursor := mem.Przydziel_pamięć(referenceBajty)
	if referenceKursor == nil {
		bieżący.refs = nil
		bieżący.ramkaLiczba = 0
		return false
	}
	bieżący.refs = (*[1 << 28]uint16)(referenceKursor)[:ramkaLiczba:ramkaLiczba]
	for i := uint32(0); i < ramkaLiczba; i++ {
		bieżący.refs[i] = 0
	}
	return true
}

func (bieżący *TcowRamkamanager) Reference(ramka uint32) uint16 {
	idx := ramka >> 12
	if idx >= bieżący.ramkaLiczba || bieżący.refs == nil {
		return 0
	}
	return bieżący.refs[idx]
}

func (bieżący *TcowRamkamanager) Increment(ramka uint32) {
	idx := ramka >> 12
	if idx >= bieżący.ramkaLiczba || bieżący.refs == nil {
		return
	}
	if bieżący.refs[idx] == 0 {
		bieżący.refs[idx] = 2
	} else {
		bieżący.refs[idx]++
	}
}

func (bieżący *TcowRamkamanager) Decrement(ramka uint32) {
	idx := ramka >> 12
	if idx >= bieżący.ramkaLiczba || bieżący.refs == nil || bieżący.refs[idx] == 0 {
		return
	}
	bieżący.refs[idx]--
}

func (bieżący *Paging) Init(stronaKatalogwpis uintptr, stronaTabelawpis uint32, pamięćmanager *TPamięćmanager) {

	StronaKatalogwpis = stronaKatalogwpis
	StronaTabelawpis = stronaTabelawpis

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRamkamanager.Init(pamięćmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			adresKursor, _ := pamięćmanager.Alignedmalloc(0x1000)
			if adresKursor == nil {
				return
			}
			adres := uint32(uintptr(adresKursor))

			Zbiórunsignedinteger32atAdres(adres|0x87, uint32(stronaKatalogwpis)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Zbiórunsignedinteger32atAdres((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, adres+pte*4)
			}
		}
		stronaKatalogwpis = stronaKatalogwpis + 0x1000
	}

}
func (bieżący *Paging) SharedPamięćregion() {

	stronaKatalogwpis := StronaKatalogwpis
	kStronaKatalogwpis := StronaKatalogwpis

	for i := uint32(1); i <= virtlen; i++ {

		stronaKatalogwpis = stronaKatalogwpis + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetWartość(uint32(kStronaKatalogwpis) + pde*4)
			v = (v & 0xFFFFF000)
			Zbiórunsignedinteger32atAdres(v|0x87, uint32(stronaKatalogwpis)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetWartość(uint32(kStronaKatalogwpis) + pde*4)
			v = (v & 0xFFFFF000)
			Zbiórunsignedinteger32atAdres(v|0x87, uint32(stronaKatalogwpis)+pde*4)

		}

	}
}
func (bieżący *Paging) Stronafault(manager *TPrzerwaniemanager) {
	przerwaniehandler = uchwytpagingPrzerwanie

	var adres uintptr
	adres = uintptr(unsafe.Pointer(&przerwaniehandler))
	bieżący.TPrzerwaniehandler.Init(0xE, uintptr(unsafe.Pointer(manager)), adres)
}

var przerwaniehandler func(uint32) uint32

func uchwytpagingPrzerwanie(esp uint32) uint32 {
	if ResolveKopiujWłączZapisfault() {
		return esp
	}
	return UchwytfatalPrzerwanieRamka(esp, 0x0E)
}

func CloneAdresSpacjacow(źródłoStronaKatalog uint32) uint32 {
	if AktywnePamięćmanager == nil || źródłoStronaKatalog == 0 {
		return 0
	}
	celKursor, _ := AktywnePamięćmanager.Alignedmalloc(0x1000)
	if celKursor == nil {
		return 0
	}
	celStronaKatalog := uint32(uintptr(celKursor))
	for i := uint32(0); i < 1024; i++ {
		Zbiórunsignedinteger32atAdres(0, celStronaKatalog+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		źródłopdeAdres := źródłoStronaKatalog + pde*4
		źródłopde := GetWartość(źródłopdeAdres)
		if (źródłopde & StronaObecny) == 0 {
			continue
		}
		if issharedpde(pde) {
			Zbiórunsignedinteger32atAdres(źródłopde, celStronaKatalog+pde*4)
			continue
		}

		celptKursor, _ := AktywnePamięćmanager.Alignedmalloc(0x1000)
		if celptKursor == nil {
			continue
		}
		źródłopt := źródłopde & StronaRamka
		celpt := uint32(uintptr(celptKursor))
		Zbiórunsignedinteger32atAdres((celpt | (źródłopde & 0xFFF)), celStronaKatalog+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteAdres := źródłopt + pte*4
			wpis := GetWartość(pteAdres)
			if (wpis & StronaObecny) != 0 {
				if (wpis & Stronawritable) != 0 {
					wpis = (wpis &^ Stronawritable) | Stronacow
					Zbiórunsignedinteger32atAdres(wpis, pteAdres)
					cowRamkamanager.Increment(wpis & StronaRamka)
				} else if (wpis & Stronacow) != 0 {
					cowRamkamanager.Increment(wpis & StronaRamka)
				}
			}
			Zbiórunsignedinteger32atAdres(wpis, celpt+pte*4)
		}
	}
	wczytajponowniecr3()
	return celStronaKatalog
}

func ResolveKopiujWłączZapisfault() bool {
	if AktywnePamięćmanager == nil {
		return false
	}
	faultAdres := getcr2()
	katalog_stron := getcr3()
	pdeAdres := katalog_stron + ((faultAdres>>22)&0x3FF)*4
	pde := GetWartość(pdeAdres)
	if (pde & StronaObecny) == 0 {
		return false
	}
	pt := pde & StronaRamka
	pteAdres := pt + ((faultAdres>>12)&0x3FF)*4
	pte := GetWartość(pteAdres)
	if (pte&Stronacow) == 0 || (pte&StronaObecny) == 0 {
		return false
	}
	oldRamka := pte & StronaRamka
	if cowRamkamanager.Reference(oldRamka) <= 1 {
		Zbiórunsignedinteger32atAdres((pte|Stronawritable)&^Stronacow, pteAdres)
		wczytajponowniecr3()
		return true
	}

	nowyKursor, _ := AktywnePamięćmanager.Alignedmalloc(0x1000)
	if nowyKursor == nil {
		return false
	}
	nowyRamka := uint32(uintptr(nowyKursor)) & StronaRamka

	źródło_2 := GetBajtyzKursor(uintptr(faultAdres&StronaRamka), 0x1000, 0x1000)
	cel_2 := GetBajtyzKursor(uintptr(nowyRamka), 0x1000, 0x1000)
	copy(cel_2, źródło_2)
	cowRamkamanager.Decrement(oldRamka)
	Zbiórunsignedinteger32atAdres((nowyRamka|(pte&0xFFF)|Stronawritable)&^Stronacow, pteAdres)
	wczytajponowniecr3()
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

func wczytajponowniecr3() {
	cr3 := getcr3()
	zbiórcr3(cr3)
}

func ZbiórbyteWchodzącyStronaKatalog(x byte, adres uint32, katalog_stron uint32) {
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	ZbiórbyteatAdres(x, adres)
	zbiórcr3(oldcr3)
}

func ZbiórBlokWchodzącyStronaKatalog(źródło_2 []byte, cel_2 []byte, rozmiar uint32, katalog_stron uint32) {
	if rozmiar == 0 || katalog_stron == 0 {
		return
	}
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	makeZakresPrywatnewritableBieżący(katalog_stron, uint32(uintptr(unsafe.Pointer(&cel_2[0]))), rozmiar)

	for i := uint32(0); i < rozmiar; i++ {
		cel_2[i] = źródło_2[i]
	}
	zbiórcr3(oldcr3)
}

func ZeroBlokWchodzącyStronaKatalog(adres uint32, rozmiar uint32, katalog_stron uint32) {
	if rozmiar == 0 || katalog_stron == 0 {
		return
	}
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	makeZakresPrywatnewritableBieżący(katalog_stron, adres, rozmiar)
	cel_2 := GetBajtyzKursor(uintptr(adres), int(rozmiar), int(rozmiar))
	for i := uint32(0); i < rozmiar; i++ {
		cel_2[i] = 0
	}
	zbiórcr3(oldcr3)
}

func makeStronaPrywatnewritableBieżący(katalog_stron uint32, wirtualneAdres uint32) bool {
	pde := GetWartość(katalog_stron + ((wirtualneAdres>>22)&0x3FF)*4)
	if (pde & StronaObecny) == 0 {
		return false
	}
	pteAdres := (pde & StronaRamka) + ((wirtualneAdres>>12)&0x3FF)*4
	pte := GetWartość(pteAdres)
	if (pte & StronaObecny) == 0 {
		return false
	}
	if (pte & Stronacow) == 0 {
		return (pte & Stronawritable) != 0
	}
	if AktywnePamięćmanager == nil {
		return false
	}
	nowyKursor, _ := AktywnePamięćmanager.Alignedmalloc(0x1000)
	if nowyKursor == nil {
		return false
	}
	nowyRamka := uint32(uintptr(nowyKursor)) & StronaRamka
	źródło_2 := GetBajtyzKursor(uintptr(wirtualneAdres&StronaRamka), 0x1000, 0x1000)
	cel_2 := GetBajtyzKursor(uintptr(nowyRamka), 0x1000, 0x1000)
	copy(cel_2, źródło_2)
	cowRamkamanager.Decrement(pte & StronaRamka)
	Zbiórunsignedinteger32atAdres((nowyRamka|(pte&0xFFF)|Stronawritable)&^Stronacow, pteAdres)
	// Publish the new physical frame before writing through its virtual address.
	wczytajponowniecr3()
	return true
}

func makeZakresPrywatnewritableBieżący(katalog_stron uint32, adres uint32, rozmiar uint32) bool {
	if rozmiar == 0 {
		return true
	}
	ostatni := adres + rozmiar - 1
	if ostatni < adres {
		return false
	}
	for strona := adres & StronaRamka; ; strona += 0x1000 {
		if !makeStronaPrywatnewritableBieżący(katalog_stron, strona) {
			return false
		}
		if strona == (ostatni & StronaRamka) {
			break
		}
	}
	return true
}

func MakeZakresPrywatnewritable(katalog_stron uint32, adres uint32, rozmiar uint32) bool {
	if katalog_stron == 0 {
		return false
	}
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	ok := makeZakresPrywatnewritableBieżący(katalog_stron, adres, rozmiar)
	zbiórcr3(oldcr3)
	return ok
}

func Zbiórunsignedinteger32WchodzącyStronaKatalog(x uint32, adres uint32, katalog_stron uint32) {
	if katalog_stron == 0 {
		return
	}
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	Zbiórunsignedinteger32atAdres(x, adres)
	zbiórcr3(oldcr3)
}

func GetWartość(adres uint32) uint32 {
	var orgWartość uint32 = *(*uint32)(unsafe.Pointer(uintptr(adres)))
	return orgWartość
}
func GetWartośćWchodzącyStronaKatalog(adres uint32, katalog_stron uint32) uint32 {
	if katalog_stron == 0 {
		return 0
	}
	oldcr3 := getcr3()
	zbiórcr3(katalog_stron)
	v := GetWartość(adres)
	zbiórcr3(oldcr3)
	return v
}

var v uint32 = 0

func KopiujStronaRamkaBlok(xStronaKatalog uint32, yStronaKatalog uint32, vAdres uint32) {
	if xStronaKatalog == 0 || yStronaKatalog == 0 {
		return
	}
	oldcr3 := getcr3()
	zbiórcr3(xStronaKatalog)
	v = GetWartość(vAdres)
	Zbiórunsignedinteger32WchodzącyStronaKatalog(v, vAdres, yStronaKatalog)

	zbiórcr3(oldcr3)
}
