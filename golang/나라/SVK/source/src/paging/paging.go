package paging

import unsafe "unsafe"
import . "prerušenie"
import . "pamäťmanager"
import . "util"

type STRANAAdresárpoložka_2 uintptr

const (
	STRANAPrítomné		uint32	= 0x001
	STRANAwritable		uint32	= 0x002
	STRANAPoužívateľ	uint32	= 0x004
	STRANARámec		uint32	= 0xFFFFF000
	STRANAcow		uint32	= 0x200
)

func Sadabyteataddress(x byte, address uint32)
func Sadaunsignedinteger8ataddress(x uint8, address uint32)
func Sadaunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func sadacr3(sTRANAAdresár uint32)
func getcr3() uint32

type Paging struct {
	TPrerušeniehandler
}
type TcowRámecmanager struct {
	mem		*TPamäťmanager
	refs		[]uint16
	rámeccount	uint32
}

var (
	STRANAAdresárpoložka	uintptr
	STRANATabuľkapoložka	uint32
	pdelen			uint32
	virtlen			uint32
	cowRámecmanager		TcowRámecmanager
)

func (vlastný *TcowRámecmanager) Init(mem *TPamäťmanager, rámeccount uint32) bool {
	vlastný.mem = mem
	vlastný.rámeccount = rámeccount
	referenceBajty := rámeccount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKurzor := mem.Malloc(referenceBajty)
	if referenceKurzor == nil {
		vlastný.refs = nil
		vlastný.rámeccount = 0
		return false
	}
	vlastný.refs = (*[1 << 28]uint16)(referenceKurzor)[:rámeccount:rámeccount]
	for i := uint32(0); i < rámeccount; i++ {
		vlastný.refs[i] = 0
	}
	return true
}

func (vlastný *TcowRámecmanager) Reference(rámec uint32) uint16 {
	idx := rámec >> 12
	if idx >= vlastný.rámeccount || vlastný.refs == nil {
		return 0
	}
	return vlastný.refs[idx]
}

func (vlastný *TcowRámecmanager) Increment(rámec uint32) {
	idx := rámec >> 12
	if idx >= vlastný.rámeccount || vlastný.refs == nil {
		return
	}
	if vlastný.refs[idx] == 0 {
		vlastný.refs[idx] = 2
	} else {
		vlastný.refs[idx]++
	}
}

func (vlastný *TcowRámecmanager) Decrement(rámec uint32) {
	idx := rámec >> 12
	if idx >= vlastný.rámeccount || vlastný.refs == nil || vlastný.refs[idx] == 0 {
		return
	}
	vlastný.refs[idx]--
}

func (vlastný *Paging) Init(sTRANAAdresárpoložka uintptr, sTRANATabuľkapoložka uint32, pamäťmanager *TPamäťmanager) {

	STRANAAdresárpoložka = sTRANAAdresárpoložka
	STRANATabuľkapoložka = sTRANATabuľkapoložka

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowRámecmanager.Init(pamäťmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKurzor, _ := pamäťmanager.Alignedmalloc(0x1000)
			if addressKurzor == nil {
				return
			}
			address := uint32(uintptr(addressKurzor))

			Sadaunsignedinteger32ataddress(address|0x87, uint32(sTRANAAdresárpoložka)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sadaunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		sTRANAAdresárpoložka = sTRANAAdresárpoložka + 0x1000
	}

}
func (vlastný *Paging) SharedPamäťregion() {

	sTRANAAdresárpoložka := STRANAAdresárpoložka
	kSTRANAAdresárpoložka := STRANAAdresárpoložka

	for i := uint32(1); i <= virtlen; i++ {

		sTRANAAdresárpoložka = sTRANAAdresárpoložka + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetHodnota(uint32(kSTRANAAdresárpoložka) + pde*4)
			v = (v & 0xFFFFF000)
			Sadaunsignedinteger32ataddress(v|0x87, uint32(sTRANAAdresárpoložka)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetHodnota(uint32(kSTRANAAdresárpoložka) + pde*4)
			v = (v & 0xFFFFF000)
			Sadaunsignedinteger32ataddress(v|0x87, uint32(sTRANAAdresárpoložka)+pde*4)

		}

	}
}
func (vlastný *Paging) STRANAfault(manager *TPrerušeniemanager) {
	prerušeniehandler = uškopagingPrerušenie

	var address uintptr
	address = uintptr(unsafe.Pointer(&prerušeniehandler))
	vlastný.TPrerušeniehandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var prerušeniehandler func(uint32) uint32

func uškopagingPrerušenie(esp uint32) uint32 {
	if ResolveKopírovaťZapnutéZápisfault() {
		return esp
	}
	return UškofatalPrerušenieRámec(esp, 0x0E)
}

func CloneaddressMedzeracow(zdrojSTRANAAdresár uint32) uint32 {
	if AktívnyPamäťmanager == nil || zdrojSTRANAAdresár == 0 {
		return 0
	}
	cieľKurzor, _ := AktívnyPamäťmanager.Alignedmalloc(0x1000)
	if cieľKurzor == nil {
		return 0
	}
	cieľSTRANAAdresár := uint32(uintptr(cieľKurzor))
	for i := uint32(0); i < 1024; i++ {
		Sadaunsignedinteger32ataddress(0, cieľSTRANAAdresár+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		zdrojpdeaddress := zdrojSTRANAAdresár + pde*4
		zdrojpde := GetHodnota(zdrojpdeaddress)
		if (zdrojpde & STRANAPrítomné) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sadaunsignedinteger32ataddress(zdrojpde, cieľSTRANAAdresár+pde*4)
			continue
		}

		cieľptKurzor, _ := AktívnyPamäťmanager.Alignedmalloc(0x1000)
		if cieľptKurzor == nil {
			continue
		}
		zdrojpt := zdrojpde & STRANARámec
		cieľpt := uint32(uintptr(cieľptKurzor))
		Sadaunsignedinteger32ataddress((cieľpt | (zdrojpde & 0xFFF)), cieľSTRANAAdresár+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := zdrojpt + pte*4
			položka := GetHodnota(pteaddress)
			if (položka & STRANAPrítomné) != 0 {
				if (položka & STRANAwritable) != 0 {
					položka = (položka &^ STRANAwritable) | STRANAcow
					Sadaunsignedinteger32ataddress(položka, pteaddress)
					cowRámecmanager.Increment(položka & STRANARámec)
				} else if (položka & STRANAcow) != 0 {
					cowRámecmanager.Increment(položka & STRANARámec)
				}
			}
			Sadaunsignedinteger32ataddress(položka, cieľpt+pte*4)
		}
	}
	znovunačítaťcr3()
	return cieľSTRANAAdresár
}

func ResolveKopírovaťZapnutéZápisfault() bool {
	if AktívnyPamäťmanager == nil {
		return false
	}
	faultaddress := getcr2()
	sTRANAAdresár := getcr3()
	pdeaddress := sTRANAAdresár + ((faultaddress>>22)&0x3FF)*4
	pde := GetHodnota(pdeaddress)
	if (pde & STRANAPrítomné) == 0 {
		return false
	}
	pt := pde & STRANARámec
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetHodnota(pteaddress)
	if (pte&STRANAcow) == 0 || (pte&STRANAPrítomné) == 0 {
		return false
	}
	oldRámec := pte & STRANARámec
	if cowRámecmanager.Reference(oldRámec) <= 1 {
		Sadaunsignedinteger32ataddress((pte|STRANAwritable)&^STRANAcow, pteaddress)
		znovunačítaťcr3()
		return true
	}

	novýKurzor, _ := AktívnyPamäťmanager.Alignedmalloc(0x1000)
	if novýKurzor == nil {
		return false
	}
	novýRámec := uint32(uintptr(novýKurzor)) & STRANARámec

	zdroj_2 := GetBajtyzKurzor(uintptr(faultaddress&STRANARámec), 0x1000, 0x1000)
	cieľ_2 := GetBajtyzKurzor(uintptr(novýRámec), 0x1000, 0x1000)
	copy(cieľ_2, zdroj_2)
	cowRámecmanager.Decrement(oldRámec)
	Sadaunsignedinteger32ataddress((novýRámec|(pte&0xFFF)|STRANAwritable)&^STRANAcow, pteaddress)
	znovunačítaťcr3()
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

func znovunačítaťcr3() {
	cr3 := getcr3()
	sadacr3(cr3)
}

func SadabytenaSTRANAAdresár(x byte, address uint32, sTRANAAdresár uint32) {
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	Sadabyteataddress(x, address)
	sadacr3(oldcr3)
}

func SadaBloknaSTRANAAdresár(zdroj_2 []byte, cieľ_2 []byte, veľkosť uint32, sTRANAAdresár uint32) {
	if veľkosť == 0 || sTRANAAdresár == 0 {
		return
	}
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	makeRozsahSúkromnáwritableAktuálny(sTRANAAdresár, uint32(uintptr(unsafe.Pointer(&cieľ_2[0]))), veľkosť)

	for i := uint32(0); i < veľkosť; i++ {
		cieľ_2[i] = zdroj_2[i]
	}
	sadacr3(oldcr3)
}

func NulaBloknaSTRANAAdresár(address uint32, veľkosť uint32, sTRANAAdresár uint32) {
	if veľkosť == 0 || sTRANAAdresár == 0 {
		return
	}
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	makeRozsahSúkromnáwritableAktuálny(sTRANAAdresár, address, veľkosť)
	cieľ_2 := GetBajtyzKurzor(uintptr(address), int(veľkosť), int(veľkosť))
	for i := uint32(0); i < veľkosť; i++ {
		cieľ_2[i] = 0
	}
	sadacr3(oldcr3)
}

func makeSTRANASúkromnáwritableAktuálny(sTRANAAdresár uint32, virtuálnyaddress uint32) bool {
	pde := GetHodnota(sTRANAAdresár + ((virtuálnyaddress>>22)&0x3FF)*4)
	if (pde & STRANAPrítomné) == 0 {
		return false
	}
	pteaddress := (pde & STRANARámec) + ((virtuálnyaddress>>12)&0x3FF)*4
	pte := GetHodnota(pteaddress)
	if (pte & STRANAPrítomné) == 0 {
		return false
	}
	if (pte & STRANAcow) == 0 {
		return (pte & STRANAwritable) != 0
	}
	if AktívnyPamäťmanager == nil {
		return false
	}
	novýKurzor, _ := AktívnyPamäťmanager.Alignedmalloc(0x1000)
	if novýKurzor == nil {
		return false
	}
	novýRámec := uint32(uintptr(novýKurzor)) & STRANARámec
	zdroj_2 := GetBajtyzKurzor(uintptr(virtuálnyaddress&STRANARámec), 0x1000, 0x1000)
	cieľ_2 := GetBajtyzKurzor(uintptr(novýRámec), 0x1000, 0x1000)
	copy(cieľ_2, zdroj_2)
	cowRámecmanager.Decrement(pte & STRANARámec)
	Sadaunsignedinteger32ataddress((novýRámec|(pte&0xFFF)|STRANAwritable)&^STRANAcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	znovunačítaťcr3()
	return true
}

func makeRozsahSúkromnáwritableAktuálny(sTRANAAdresár uint32, address uint32, veľkosť uint32) bool {
	if veľkosť == 0 {
		return true
	}
	posledné := address + veľkosť - 1
	if posledné < address {
		return false
	}
	for sTRANA := address & STRANARámec; ; sTRANA += 0x1000 {
		if !makeSTRANASúkromnáwritableAktuálny(sTRANAAdresár, sTRANA) {
			return false
		}
		if sTRANA == (posledné & STRANARámec) {
			break
		}
	}
	return true
}

func MakeRozsahSúkromnáwritable(sTRANAAdresár uint32, address uint32, veľkosť uint32) bool {
	if sTRANAAdresár == 0 {
		return false
	}
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	ok := makeRozsahSúkromnáwritableAktuálny(sTRANAAdresár, address, veľkosť)
	sadacr3(oldcr3)
	return ok
}

func Sadaunsignedinteger32naSTRANAAdresár(x uint32, address uint32, sTRANAAdresár uint32) {
	if sTRANAAdresár == 0 {
		return
	}
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	Sadaunsignedinteger32ataddress(x, address)
	sadacr3(oldcr3)
}

func GetHodnota(address uint32) uint32 {
	var orgHodnota uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgHodnota
}
func GetHodnotanaSTRANAAdresár(address uint32, sTRANAAdresár uint32) uint32 {
	if sTRANAAdresár == 0 {
		return 0
	}
	oldcr3 := getcr3()
	sadacr3(sTRANAAdresár)
	v := GetHodnota(address)
	sadacr3(oldcr3)
	return v
}

var v uint32 = 0

func KopírovaťSTRANARámecBlok(xSTRANAAdresár uint32, ySTRANAAdresár uint32, vaddress uint32) {
	if xSTRANAAdresár == 0 || ySTRANAAdresár == 0 {
		return
	}
	oldcr3 := getcr3()
	sadacr3(xSTRANAAdresár)
	v = GetHodnota(vaddress)
	Sadaunsignedinteger32naSTRANAAdresár(v, vaddress, ySTRANAAdresár)

	sadacr3(oldcr3)
}
