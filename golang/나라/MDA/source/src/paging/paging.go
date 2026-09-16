/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "intrerupere"
import . "memoriemanager"
import . "util"

type PAGINĂDirectorînregistrare_2 uintptr

const (
	PAGINĂPrezent		uint32	= 0x001
	PAGINĂwritable		uint32	= 0x002
	PAGINĂUtilizator	uint32	= 0x004
	PAGINĂCadru		uint32	= 0xFFFFF000
	PAGINĂcow		uint32	= 0x200
)

func Definitbyteataddress(x byte, address uint32)
func Definitunsignedinteger8ataddress(x uint8, address uint32)
func Definitunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func definitcr3(pAGINĂDirector uint32)
func getcr3() uint32

type Paging struct {
	TIntreruperehandler
}
type TcowCadrumanager struct {
	mem		*TMemoriemanager
	refs		[]uint16
	cadrucount	uint32
}

var (
	PAGINĂDirectorînregistrare	uintptr
	PAGINĂTabelînregistrare		uint32
	pdelen				uint32
	virtlen				uint32
	cowCadrumanager			TcowCadrumanager
)

func (sine *TcowCadrumanager) Init(mem *TMemoriemanager, cadrucount uint32) bool {
	sine.mem = mem
	sine.cadrucount = cadrucount
	referenceOcteți := cadrucount * uint32(unsafe.Sizeof(uint16(0)))
	referenceIndicator := mem.Malloc(referenceOcteți)
	if referenceIndicator == nil {
		sine.refs = nil
		sine.cadrucount = 0
		return false
	}
	sine.refs = (*[1 << 28]uint16)(referenceIndicator)[:cadrucount:cadrucount]
	for i := uint32(0); i < cadrucount; i++ {
		sine.refs[i] = 0
	}
	return true
}

func (sine *TcowCadrumanager) Reference(cadru uint32) uint16 {
	idx := cadru >> 12
	if idx >= sine.cadrucount || sine.refs == nil {
		return 0
	}
	return sine.refs[idx]
}

func (sine *TcowCadrumanager) Increment(cadru uint32) {
	idx := cadru >> 12
	if idx >= sine.cadrucount || sine.refs == nil {
		return
	}
	if sine.refs[idx] == 0 {
		sine.refs[idx] = 2
	} else {
		sine.refs[idx]++
	}
}

func (sine *TcowCadrumanager) Decrement(cadru uint32) {
	idx := cadru >> 12
	if idx >= sine.cadrucount || sine.refs == nil || sine.refs[idx] == 0 {
		return
	}
	sine.refs[idx]--
}

func (sine *Paging) Init(pAGINĂDirectorînregistrare uintptr, pAGINĂTabelînregistrare uint32, memoriemanager *TMemoriemanager) {

	PAGINĂDirectorînregistrare = pAGINĂDirectorînregistrare
	PAGINĂTabelînregistrare = pAGINĂTabelînregistrare

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowCadrumanager.Init(memoriemanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressIndicator, _ := memoriemanager.Alignedmalloc(0x1000)
			if addressIndicator == nil {
				return
			}
			address := uint32(uintptr(addressIndicator))

			Definitunsignedinteger32ataddress(address|0x87, uint32(pAGINĂDirectorînregistrare)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Definitunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		pAGINĂDirectorînregistrare = pAGINĂDirectorînregistrare + 0x1000
	}

}
func (sine *Paging) SharedMemorieregion() {

	pAGINĂDirectorînregistrare := PAGINĂDirectorînregistrare
	kPAGINĂDirectorînregistrare := PAGINĂDirectorînregistrare

	for i := uint32(1); i <= virtlen; i++ {

		pAGINĂDirectorînregistrare = pAGINĂDirectorînregistrare + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetValoare(uint32(kPAGINĂDirectorînregistrare) + pde*4)
			v = (v & 0xFFFFF000)
			Definitunsignedinteger32ataddress(v|0x87, uint32(pAGINĂDirectorînregistrare)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetValoare(uint32(kPAGINĂDirectorînregistrare) + pde*4)
			v = (v & 0xFFFFF000)
			Definitunsignedinteger32ataddress(v|0x87, uint32(pAGINĂDirectorînregistrare)+pde*4)

		}

	}
}
func (sine *Paging) PAGINĂfault(manager *TIntreruperemanager) {
	intreruperehandler = mânerpagingIntrerupere

	var address uintptr
	address = uintptr(unsafe.Pointer(&intreruperehandler))
	sine.TIntreruperehandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var intreruperehandler func(uint32) uint32

func mânerpagingIntrerupere(esp uint32) uint32 {
	if ResolveCopiazăPornitScrierefault() {
		return esp
	}
	return MânerfatalIntrerupereCadru(esp, 0x0E)
}

func CloneaddressSpațiucow(sursăPAGINĂDirector uint32) uint32 {
	if ActivMemoriemanager == nil || sursăPAGINĂDirector == 0 {
		return 0
	}
	destinațieIndicator, _ := ActivMemoriemanager.Alignedmalloc(0x1000)
	if destinațieIndicator == nil {
		return 0
	}
	destinațiePAGINĂDirector := uint32(uintptr(destinațieIndicator))
	for i := uint32(0); i < 1024; i++ {
		Definitunsignedinteger32ataddress(0, destinațiePAGINĂDirector+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		sursăpdeaddress := sursăPAGINĂDirector + pde*4
		sursăpde := GetValoare(sursăpdeaddress)
		if (sursăpde & PAGINĂPrezent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Definitunsignedinteger32ataddress(sursăpde, destinațiePAGINĂDirector+pde*4)
			continue
		}

		destinațieptIndicator, _ := ActivMemoriemanager.Alignedmalloc(0x1000)
		if destinațieptIndicator == nil {
			continue
		}
		sursăpt := sursăpde & PAGINĂCadru
		destinațiept := uint32(uintptr(destinațieptIndicator))
		Definitunsignedinteger32ataddress((destinațiept | (sursăpde & 0xFFF)), destinațiePAGINĂDirector+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := sursăpt + pte*4
			înregistrare := GetValoare(pteaddress)
			if (înregistrare & PAGINĂPrezent) != 0 {
				if (înregistrare & PAGINĂwritable) != 0 {
					înregistrare = (înregistrare &^ PAGINĂwritable) | PAGINĂcow
					Definitunsignedinteger32ataddress(înregistrare, pteaddress)
					cowCadrumanager.Increment(înregistrare & PAGINĂCadru)
				} else if (înregistrare & PAGINĂcow) != 0 {
					cowCadrumanager.Increment(înregistrare & PAGINĂCadru)
				}
			}
			Definitunsignedinteger32ataddress(înregistrare, destinațiept+pte*4)
		}
	}
	reîncarcăcr3()
	return destinațiePAGINĂDirector
}

func ResolveCopiazăPornitScrierefault() bool {
	if ActivMemoriemanager == nil {
		return false
	}
	faultaddress := getcr2()
	pAGINĂDirector := getcr3()
	pdeaddress := pAGINĂDirector + ((faultaddress>>22)&0x3FF)*4
	pde := GetValoare(pdeaddress)
	if (pde & PAGINĂPrezent) == 0 {
		return false
	}
	pt := pde & PAGINĂCadru
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetValoare(pteaddress)
	if (pte&PAGINĂcow) == 0 || (pte&PAGINĂPrezent) == 0 {
		return false
	}
	oldCadru := pte & PAGINĂCadru
	if cowCadrumanager.Reference(oldCadru) <= 1 {
		Definitunsignedinteger32ataddress((pte|PAGINĂwritable)&^PAGINĂcow, pteaddress)
		reîncarcăcr3()
		return true
	}

	nouIndicator, _ := ActivMemoriemanager.Alignedmalloc(0x1000)
	if nouIndicator == nil {
		return false
	}
	nouCadru := uint32(uintptr(nouIndicator)) & PAGINĂCadru

	sursă_2 := GetOctețifromIndicator(uintptr(faultaddress&PAGINĂCadru), 0x1000, 0x1000)
	destinație_2 := GetOctețifromIndicator(uintptr(nouCadru), 0x1000, 0x1000)
	copy(destinație_2, sursă_2)
	cowCadrumanager.Decrement(oldCadru)
	Definitunsignedinteger32ataddress((nouCadru|(pte&0xFFF)|PAGINĂwritable)&^PAGINĂcow, pteaddress)
	reîncarcăcr3()
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

func reîncarcăcr3() {
	cr3 := getcr3()
	definitcr3(cr3)
}

func DefinitbyteIntrarePAGINĂDirector(x byte, address uint32, pAGINĂDirector uint32) {
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	Definitbyteataddress(x, address)
	definitcr3(oldcr3)
}

func DefinitBlocIntrarePAGINĂDirector(sursă_2 []byte, destinație_2 []byte, mărime uint32, pAGINĂDirector uint32) {
	if mărime == 0 || pAGINĂDirector == 0 {
		return
	}
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	makeIntervalPrivatwritableCurentă(pAGINĂDirector, uint32(uintptr(unsafe.Pointer(&destinație_2[0]))), mărime)

	for i := uint32(0); i < mărime; i++ {
		destinație_2[i] = sursă_2[i]
	}
	definitcr3(oldcr3)
}

func ZeroBlocIntrarePAGINĂDirector(address uint32, mărime uint32, pAGINĂDirector uint32) {
	if mărime == 0 || pAGINĂDirector == 0 {
		return
	}
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	makeIntervalPrivatwritableCurentă(pAGINĂDirector, address, mărime)
	destinație_2 := GetOctețifromIndicator(uintptr(address), int(mărime), int(mărime))
	for i := uint32(0); i < mărime; i++ {
		destinație_2[i] = 0
	}
	definitcr3(oldcr3)
}

func makePAGINĂPrivatwritableCurentă(pAGINĂDirector uint32, virtualăaddress uint32) bool {
	pde := GetValoare(pAGINĂDirector + ((virtualăaddress>>22)&0x3FF)*4)
	if (pde & PAGINĂPrezent) == 0 {
		return false
	}
	pteaddress := (pde & PAGINĂCadru) + ((virtualăaddress>>12)&0x3FF)*4
	pte := GetValoare(pteaddress)
	if (pte & PAGINĂPrezent) == 0 {
		return false
	}
	if (pte & PAGINĂcow) == 0 {
		return (pte & PAGINĂwritable) != 0
	}
	if ActivMemoriemanager == nil {
		return false
	}
	nouIndicator, _ := ActivMemoriemanager.Alignedmalloc(0x1000)
	if nouIndicator == nil {
		return false
	}
	nouCadru := uint32(uintptr(nouIndicator)) & PAGINĂCadru
	sursă_2 := GetOctețifromIndicator(uintptr(virtualăaddress&PAGINĂCadru), 0x1000, 0x1000)
	destinație_2 := GetOctețifromIndicator(uintptr(nouCadru), 0x1000, 0x1000)
	copy(destinație_2, sursă_2)
	cowCadrumanager.Decrement(pte & PAGINĂCadru)
	Definitunsignedinteger32ataddress((nouCadru|(pte&0xFFF)|PAGINĂwritable)&^PAGINĂcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	reîncarcăcr3()
	return true
}

func makeIntervalPrivatwritableCurentă(pAGINĂDirector uint32, address uint32, mărime uint32) bool {
	if mărime == 0 {
		return true
	}
	ultima := address + mărime - 1
	if ultima < address {
		return false
	}
	for pAGINĂ := address & PAGINĂCadru; ; pAGINĂ += 0x1000 {
		if !makePAGINĂPrivatwritableCurentă(pAGINĂDirector, pAGINĂ) {
			return false
		}
		if pAGINĂ == (ultima & PAGINĂCadru) {
			break
		}
	}
	return true
}

func MakeIntervalPrivatwritable(pAGINĂDirector uint32, address uint32, mărime uint32) bool {
	if pAGINĂDirector == 0 {
		return false
	}
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	ok := makeIntervalPrivatwritableCurentă(pAGINĂDirector, address, mărime)
	definitcr3(oldcr3)
	return ok
}

func Definitunsignedinteger32IntrarePAGINĂDirector(x uint32, address uint32, pAGINĂDirector uint32) {
	if pAGINĂDirector == 0 {
		return
	}
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	Definitunsignedinteger32ataddress(x, address)
	definitcr3(oldcr3)
}

func GetValoare(address uint32) uint32 {
	var orgValoare uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgValoare
}
func GetValoareIntrarePAGINĂDirector(address uint32, pAGINĂDirector uint32) uint32 {
	if pAGINĂDirector == 0 {
		return 0
	}
	oldcr3 := getcr3()
	definitcr3(pAGINĂDirector)
	v := GetValoare(address)
	definitcr3(oldcr3)
	return v
}

var v uint32 = 0

func CopiazăPAGINĂCadruBloc(xPAGINĂDirector uint32, yPAGINĂDirector uint32, vaddress uint32) {
	if xPAGINĂDirector == 0 || yPAGINĂDirector == 0 {
		return
	}
	oldcr3 := getcr3()
	definitcr3(xPAGINĂDirector)
	v = GetValoare(vaddress)
	Definitunsignedinteger32IntrarePAGINĂDirector(v, vaddress, yPAGINĂDirector)

	definitcr3(oldcr3)
}
