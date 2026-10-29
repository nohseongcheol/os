/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupció"
import . "memòriamanager"
import . "util"

type PàginaDirectorientrada_2 uintptr

const (
	Pàginapresent	uint32	= 0x001
	Pàginawritable	uint32	= 0x002
	PàginaUsuari	uint32	= 0x004
	PàginaMarc	uint32	= 0xFFFFF000
	Pàginacow	uint32	= 0x200
)

func EstableixbyteatAdreça(x byte, adreça uint32)
func Estableixunsignedinteger8atAdreça(x uint8, adreça uint32)
func Estableixunsignedinteger32atAdreça(x uint32, adreça uint32)

func getcr2() uint32

func estableixcr3(pàginaDirectori uint32)
func getcr3() uint32

type Paging struct {
	TInterrupcióhandler
}
type TcowMarcmanager struct {
	mem		*TMemòriamanager
	refs		[]uint16
	marcRecompte	uint32
}

var (
	PàginaDirectorientrada	uintptr
	PàginaTaulaentrada	uint32
	pdelen			uint32
	virtlen			uint32
	cowMarcmanager		TcowMarcmanager
)

func (unmateix *TcowMarcmanager) Init(mem *TMemòriamanager, marcRecompte uint32) bool {
	unmateix.mem = mem
	unmateix.marcRecompte = marcRecompte
	referencebytes := marcRecompte * uint32(unsafe.Sizeof(uint16(0)))
	referencePunter := mem.Malloc(referencebytes)
	if referencePunter == nil {
		unmateix.refs = nil
		unmateix.marcRecompte = 0
		return false
	}
	unmateix.refs = (*[1 << 28]uint16)(referencePunter)[:marcRecompte:marcRecompte]
	for i := uint32(0); i < marcRecompte; i++ {
		unmateix.refs[i] = 0
	}
	return true
}

func (unmateix *TcowMarcmanager) Reference(marc uint32) uint16 {
	idx := marc >> 12
	if idx >= unmateix.marcRecompte || unmateix.refs == nil {
		return 0
	}
	return unmateix.refs[idx]
}

func (unmateix *TcowMarcmanager) Increment(marc uint32) {
	idx := marc >> 12
	if idx >= unmateix.marcRecompte || unmateix.refs == nil {
		return
	}
	if unmateix.refs[idx] == 0 {
		unmateix.refs[idx] = 2
	} else {
		unmateix.refs[idx]++
	}
}

func (unmateix *TcowMarcmanager) Decrement(marc uint32) {
	idx := marc >> 12
	if idx >= unmateix.marcRecompte || unmateix.refs == nil || unmateix.refs[idx] == 0 {
		return
	}
	unmateix.refs[idx]--
}

func (unmateix *Paging) Init(pàginaDirectorientrada uintptr, pàginaTaulaentrada uint32, memòriamanager *TMemòriamanager) {

	PàginaDirectorientrada = pàginaDirectorientrada
	PàginaTaulaentrada = pàginaTaulaentrada

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowMarcmanager.Init(memòriamanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			adreçaPunter, _ := memòriamanager.Alignedmalloc(0x1000)
			if adreçaPunter == nil {
				return
			}
			adreça := uint32(uintptr(adreçaPunter))

			Estableixunsignedinteger32atAdreça(adreça|0x87, uint32(pàginaDirectorientrada)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Estableixunsignedinteger32atAdreça((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, adreça+pte*4)
			}
		}
		pàginaDirectorientrada = pàginaDirectorientrada + 0x1000
	}

}
func (unmateix *Paging) SharedMemòriaregion() {

	pàginaDirectorientrada := PàginaDirectorientrada
	kPàginaDirectorientrada := PàginaDirectorientrada

	for i := uint32(1); i <= virtlen; i++ {

		pàginaDirectorientrada = pàginaDirectorientrada + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValor(uint32(kPàginaDirectorientrada) + pde*4)
			v = (v & 0xFFFFF000)
			Estableixunsignedinteger32atAdreça(v|0x87, uint32(pàginaDirectorientrada)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValor(uint32(kPàginaDirectorientrada) + pde*4)
			v = (v & 0xFFFFF000)
			Estableixunsignedinteger32atAdreça(v|0x87, uint32(pàginaDirectorientrada)+pde*4)

		}

	}
}
func (unmateix *Paging) Pàginafault(manager *TInterrupciómanager) {
	interrupcióhandler = gestorpagingInterrupció

	var adreça uintptr
	adreça = uintptr(unsafe.Pointer(&interrupcióhandler))
	unmateix.TInterrupcióhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), adreça)
}

var interrupcióhandler func(uint32) uint32

func gestorpagingInterrupció(esp uint32) uint32 {
	if ResolveCopiaEngegatEscripturafault() {
		return esp
	}
	return GestorfatalInterrupcióMarc(esp, 0x0E)
}

func CloneAdreçaEspaicow(origenPàginaDirectori uint32) uint32 {
	if ActiuMemòriamanager == nil || origenPàginaDirectori == 0 {
		return 0
	}
	destinacióPunter, _ := ActiuMemòriamanager.Alignedmalloc(0x1000)
	if destinacióPunter == nil {
		return 0
	}
	destinacióPàginaDirectori := uint32(uintptr(destinacióPunter))
	for i := uint32(0); i < 1024; i++ {
		Estableixunsignedinteger32atAdreça(0, destinacióPàginaDirectori+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		origenpdeAdreça := origenPàginaDirectori + pde*4
		origenpde := GetValor(origenpdeAdreça)
		if (origenpde & Pàginapresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Estableixunsignedinteger32atAdreça(origenpde, destinacióPàginaDirectori+pde*4)
			continue
		}

		destinacióptPunter, _ := ActiuMemòriamanager.Alignedmalloc(0x1000)
		if destinacióptPunter == nil {
			continue
		}
		origenpt := origenpde & PàginaMarc
		destinaciópt := uint32(uintptr(destinacióptPunter))
		Estableixunsignedinteger32atAdreça((destinaciópt | (origenpde & 0xFFF)), destinacióPàginaDirectori+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteAdreça := origenpt + pte*4
			entrada := GetValor(pteAdreça)
			if (entrada & Pàginapresent) != 0 {
				if (entrada & Pàginawritable) != 0 {
					entrada = (entrada &^ Pàginawritable) | Pàginacow
					Estableixunsignedinteger32atAdreça(entrada, pteAdreça)
					cowMarcmanager.Increment(entrada & PàginaMarc)
				} else if (entrada & Pàginacow) != 0 {
					cowMarcmanager.Increment(entrada & PàginaMarc)
				}
			}
			Estableixunsignedinteger32atAdreça(entrada, destinaciópt+pte*4)
		}
	}
	tornaacarregarcr3()
	return destinacióPàginaDirectori
}

func ResolveCopiaEngegatEscripturafault() bool {
	if ActiuMemòriamanager == nil {
		return false
	}
	faultAdreça := getcr2()
	pàginaDirectori := getcr3()
	pdeAdreça := pàginaDirectori + ((faultAdreça>>22)&0x3FF)*4
	pde := GetValor(pdeAdreça)
	if (pde & Pàginapresent) == 0 {
		return false
	}
	pt := pde & PàginaMarc
	pteAdreça := pt + ((faultAdreça>>12)&0x3FF)*4
	pte := GetValor(pteAdreça)
	if (pte&Pàginacow) == 0 || (pte&Pàginapresent) == 0 {
		return false
	}
	oldMarc := pte & PàginaMarc
	if cowMarcmanager.Reference(oldMarc) <= 1 {
		Estableixunsignedinteger32atAdreça((pte|Pàginawritable)&^Pàginacow, pteAdreça)
		tornaacarregarcr3()
		return true
	}

	nouPunter, _ := ActiuMemòriamanager.Alignedmalloc(0x1000)
	if nouPunter == nil {
		return false
	}
	nouMarc := uint32(uintptr(nouPunter)) & PàginaMarc

	origen_2 := GetbytesdesdePunter(uintptr(faultAdreça&PàginaMarc), 0x1000, 0x1000)
	destinació_2 := GetbytesdesdePunter(uintptr(nouMarc), 0x1000, 0x1000)
	copy(destinació_2, origen_2)
	cowMarcmanager.Decrement(oldMarc)
	Estableixunsignedinteger32atAdreça((nouMarc|(pte&0xFFF)|Pàginawritable)&^Pàginacow, pteAdreça)
	tornaacarregarcr3()
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

func tornaacarregarcr3() {
	cr3 := getcr3()
	estableixcr3(cr3)
}

func EstableixbyteaPàginaDirectori(x byte, adreça uint32, pàginaDirectori uint32) {
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	EstableixbyteatAdreça(x, adreça)
	estableixcr3(oldcr3)
}

func EstableixBlocaPàginaDirectori(origen_2 []byte, destinació_2 []byte, mida uint32, pàginaDirectori uint32) {
	if mida == 0 || pàginaDirectori == 0 {
		return
	}
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	makeIntervalPrivatwritableActual(pàginaDirectori, uint32(uintptr(unsafe.Pointer(&destinació_2[0]))), mida)

	for i := uint32(0); i < mida; i++ {
		destinació_2[i] = origen_2[i]
	}
	estableixcr3(oldcr3)
}

func ZeroBlocaPàginaDirectori(adreça uint32, mida uint32, pàginaDirectori uint32) {
	if mida == 0 || pàginaDirectori == 0 {
		return
	}
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	makeIntervalPrivatwritableActual(pàginaDirectori, adreça, mida)
	destinació_2 := GetbytesdesdePunter(uintptr(adreça), int(mida), int(mida))
	for i := uint32(0); i < mida; i++ {
		destinació_2[i] = 0
	}
	estableixcr3(oldcr3)
}

func makePàginaPrivatwritableActual(pàginaDirectori uint32, virtualAdreça uint32) bool {
	pde := GetValor(pàginaDirectori + ((virtualAdreça>>22)&0x3FF)*4)
	if (pde & Pàginapresent) == 0 {
		return false
	}
	pteAdreça := (pde & PàginaMarc) + ((virtualAdreça>>12)&0x3FF)*4
	pte := GetValor(pteAdreça)
	if (pte & Pàginapresent) == 0 {
		return false
	}
	if (pte & Pàginacow) == 0 {
		return (pte & Pàginawritable) != 0
	}
	if ActiuMemòriamanager == nil {
		return false
	}
	nouPunter, _ := ActiuMemòriamanager.Alignedmalloc(0x1000)
	if nouPunter == nil {
		return false
	}
	nouMarc := uint32(uintptr(nouPunter)) & PàginaMarc
	origen_2 := GetbytesdesdePunter(uintptr(virtualAdreça&PàginaMarc), 0x1000, 0x1000)
	destinació_2 := GetbytesdesdePunter(uintptr(nouMarc), 0x1000, 0x1000)
	copy(destinació_2, origen_2)
	cowMarcmanager.Decrement(pte & PàginaMarc)
	Estableixunsignedinteger32atAdreça((nouMarc|(pte&0xFFF)|Pàginawritable)&^Pàginacow, pteAdreça)
	// Publish the new physical frame before writing through its virtual address.
	tornaacarregarcr3()
	return true
}

func makeIntervalPrivatwritableActual(pàginaDirectori uint32, adreça uint32, mida uint32) bool {
	if mida == 0 {
		return true
	}
	últim := adreça + mida - 1
	if últim < adreça {
		return false
	}
	for pàgina := adreça & PàginaMarc; ; pàgina += 0x1000 {
		if !makePàginaPrivatwritableActual(pàginaDirectori, pàgina) {
			return false
		}
		if pàgina == (últim & PàginaMarc) {
			break
		}
	}
	return true
}

func MakeIntervalPrivatwritable(pàginaDirectori uint32, adreça uint32, mida uint32) bool {
	if pàginaDirectori == 0 {
		return false
	}
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	dacord := makeIntervalPrivatwritableActual(pàginaDirectori, adreça, mida)
	estableixcr3(oldcr3)
	return dacord
}

func Estableixunsignedinteger32aPàginaDirectori(x uint32, adreça uint32, pàginaDirectori uint32) {
	if pàginaDirectori == 0 {
		return
	}
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	Estableixunsignedinteger32atAdreça(x, adreça)
	estableixcr3(oldcr3)
}

func GetValor(adreça uint32) uint32 {
	var orgValor uint32 = *(*uint32)(unsafe.Pointer(uintptr(adreça)))
	return orgValor
}
func GetValoraPàginaDirectori(adreça uint32, pàginaDirectori uint32) uint32 {
	if pàginaDirectori == 0 {
		return 0
	}
	oldcr3 := getcr3()
	estableixcr3(pàginaDirectori)
	v := GetValor(adreça)
	estableixcr3(oldcr3)
	return v
}

var v uint32 = 0

func CopiaPàginaMarcBloc(xPàginaDirectori uint32, yPàginaDirectori uint32, vAdreça uint32) {
	if xPàginaDirectori == 0 || yPàginaDirectori == 0 {
		return
	}
	oldcr3 := getcr3()
	estableixcr3(xPàginaDirectori)
	v = GetValor(vAdreça)
	Estableixunsignedinteger32aPàginaDirectori(v, vAdreça, yPàginaDirectori)

	estableixcr3(oldcr3)
}
