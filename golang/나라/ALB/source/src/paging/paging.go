/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "memoriaManazhuesi"
import . "util"

type FaqeDosjeentry_2 uintptr

const (
	Faqepresent	uint32	= 0x001
	Faqewritable	uint32	= 0x002
	FaqePërdoruesi	uint32	= 0x004
	FaqeKornizë	uint32	= 0xFFFFF000
	Faqecow		uint32	= 0x200
)

func Caktonibyteataddress(x byte, address uint32)
func Caktoniunsignedinteger8ataddress(x uint8, address uint32)
func Caktoniunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func caktonicr3(faqeDosje uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowKornizëManazhuesi struct {
	mem		*TMemoriaManazhuesi
	refs		[]uint16
	kornizëcount	uint32
}

var (
	FaqeDosjeentry		uintptr
	FaqeTabelaentry		uint32
	pdelen			uint32
	virtlen			uint32
	cowKornizëManazhuesi	TcowKornizëManazhuesi
)

func (vetvetja *TcowKornizëManazhuesi) Init(mem *TMemoriaManazhuesi, kornizëcount uint32) bool {
	vetvetja.mem = mem
	vetvetja.kornizëcount = kornizëcount
	referencebytes := kornizëcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceKursori := mem.Malloc(referencebytes)
	if referenceKursori == nil {
		vetvetja.refs = nil
		vetvetja.kornizëcount = 0
		return false
	}
	vetvetja.refs = (*[1 << 28]uint16)(referenceKursori)[:kornizëcount:kornizëcount]
	for i := uint32(0); i < kornizëcount; i++ {
		vetvetja.refs[i] = 0
	}
	return true
}

func (vetvetja *TcowKornizëManazhuesi) Reference(kornizë uint32) uint16 {
	idx := kornizë >> 12
	if idx >= vetvetja.kornizëcount || vetvetja.refs == nil {
		return 0
	}
	return vetvetja.refs[idx]
}

func (vetvetja *TcowKornizëManazhuesi) Increment(kornizë uint32) {
	idx := kornizë >> 12
	if idx >= vetvetja.kornizëcount || vetvetja.refs == nil {
		return
	}
	if vetvetja.refs[idx] == 0 {
		vetvetja.refs[idx] = 2
	} else {
		vetvetja.refs[idx]++
	}
}

func (vetvetja *TcowKornizëManazhuesi) Decrement(kornizë uint32) {
	idx := kornizë >> 12
	if idx >= vetvetja.kornizëcount || vetvetja.refs == nil || vetvetja.refs[idx] == 0 {
		return
	}
	vetvetja.refs[idx]--
}

func (vetvetja *Paging) Init(faqeDosjeentry uintptr, faqeTabelaentry uint32, memoriaManazhuesi *TMemoriaManazhuesi) {

	FaqeDosjeentry = faqeDosjeentry
	FaqeTabelaentry = faqeTabelaentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowKornizëManazhuesi.Init(memoriaManazhuesi, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressKursori, _ := memoriaManazhuesi.Alignedmalloc(0x1000)
			if addressKursori == nil {
				return
			}
			address := uint32(uintptr(addressKursori))

			Caktoniunsignedinteger32ataddress(address|0x87, uint32(faqeDosjeentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Caktoniunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		faqeDosjeentry = faqeDosjeentry + 0x1000
	}

}
func (vetvetja *Paging) SharedMemoriaregion() {

	faqeDosjeentry := FaqeDosjeentry
	kfaqeDosjeentry := FaqeDosjeentry

	for i := uint32(1); i <= virtlen; i++ {

		faqeDosjeentry = faqeDosjeentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetVlera(uint32(kfaqeDosjeentry) + pde*4)
			v = (v & 0xFFFFF000)
			Caktoniunsignedinteger32ataddress(v|0x87, uint32(faqeDosjeentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetVlera(uint32(kfaqeDosjeentry) + pde*4)
			v = (v & 0xFFFFF000)
			Caktoniunsignedinteger32ataddress(v|0x87, uint32(faqeDosjeentry)+pde*4)

		}

	}
}
func (vetvetja *Paging) Faqefault(manazhuesi *TInterruptManazhuesi) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	vetvetja.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manazhuesi)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveKopjoonShkrimifault() {
		return esp
	}
	return HandlefatalinterruptKornizë(esp, 0x0E)
}

func CloneaddressHapësiracow(burimifaqeDosje uint32) uint32 {
	if AktivMemoriaManazhuesi == nil || burimifaqeDosje == 0 {
		return 0
	}
	destinacioniKursori, _ := AktivMemoriaManazhuesi.Alignedmalloc(0x1000)
	if destinacioniKursori == nil {
		return 0
	}
	destinacionifaqeDosje := uint32(uintptr(destinacioniKursori))
	for i := uint32(0); i < 1024; i++ {
		Caktoniunsignedinteger32ataddress(0, destinacionifaqeDosje+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		burimipdeaddress := burimifaqeDosje + pde*4
		burimipde := GetVlera(burimipdeaddress)
		if (burimipde & Faqepresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Caktoniunsignedinteger32ataddress(burimipde, destinacionifaqeDosje+pde*4)
			continue
		}

		destinacioniptKursori, _ := AktivMemoriaManazhuesi.Alignedmalloc(0x1000)
		if destinacioniptKursori == nil {
			continue
		}
		burimipt := burimipde & FaqeKornizë
		destinacionipt := uint32(uintptr(destinacioniptKursori))
		Caktoniunsignedinteger32ataddress((destinacionipt | (burimipde & 0xFFF)), destinacionifaqeDosje+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := burimipt + pte*4
			entry := GetVlera(pteaddress)
			if (entry & Faqepresent) != 0 {
				if (entry & Faqewritable) != 0 {
					entry = (entry &^ Faqewritable) | Faqecow
					Caktoniunsignedinteger32ataddress(entry, pteaddress)
					cowKornizëManazhuesi.Increment(entry & FaqeKornizë)
				} else if (entry & Faqecow) != 0 {
					cowKornizëManazhuesi.Increment(entry & FaqeKornizë)
				}
			}
			Caktoniunsignedinteger32ataddress(entry, destinacionipt+pte*4)
		}
	}
	ringarkocr3()
	return destinacionifaqeDosje
}

func ResolveKopjoonShkrimifault() bool {
	if AktivMemoriaManazhuesi == nil {
		return false
	}
	faultaddress := getcr2()
	faqeDosje := getcr3()
	pdeaddress := faqeDosje + ((faultaddress>>22)&0x3FF)*4
	pde := GetVlera(pdeaddress)
	if (pde & Faqepresent) == 0 {
		return false
	}
	pt := pde & FaqeKornizë
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetVlera(pteaddress)
	if (pte&Faqecow) == 0 || (pte&Faqepresent) == 0 {
		return false
	}
	oldKornizë := pte & FaqeKornizë
	if cowKornizëManazhuesi.Reference(oldKornizë) <= 1 {
		Caktoniunsignedinteger32ataddress((pte|Faqewritable)&^Faqecow, pteaddress)
		ringarkocr3()
		return true
	}

	iRiKursori, _ := AktivMemoriaManazhuesi.Alignedmalloc(0x1000)
	if iRiKursori == nil {
		return false
	}
	iRiKornizë := uint32(uintptr(iRiKursori)) & FaqeKornizë

	burimi_2 := GetbytesfromKursori(uintptr(faultaddress&FaqeKornizë), 0x1000, 0x1000)
	destinacioni_2 := GetbytesfromKursori(uintptr(iRiKornizë), 0x1000, 0x1000)
	copy(destinacioni_2, burimi_2)
	cowKornizëManazhuesi.Decrement(oldKornizë)
	Caktoniunsignedinteger32ataddress((iRiKornizë|(pte&0xFFF)|Faqewritable)&^Faqecow, pteaddress)
	ringarkocr3()
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

func ringarkocr3() {
	cr3 := getcr3()
	caktonicr3(cr3)
}

func CaktonibyteZmadhofaqeDosje(x byte, address uint32, faqeDosje uint32) {
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	Caktonibyteataddress(x, address)
	caktonicr3(oldcr3)
}

func CaktoniblockZmadhofaqeDosje(burimi_2 []byte, destinacioni_2 []byte, madhësia uint32, faqeDosje uint32) {
	if madhësia == 0 || faqeDosje == 0 {
		return
	}
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	makeIntervalPrivatwritableEtanishme(faqeDosje, uint32(uintptr(unsafe.Pointer(&destinacioni_2[0]))), madhësia)

	for i := uint32(0); i < madhësia; i++ {
		destinacioni_2[i] = burimi_2[i]
	}
	caktonicr3(oldcr3)
}

func ZeroblockZmadhofaqeDosje(address uint32, madhësia uint32, faqeDosje uint32) {
	if madhësia == 0 || faqeDosje == 0 {
		return
	}
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	makeIntervalPrivatwritableEtanishme(faqeDosje, address, madhësia)
	destinacioni_2 := GetbytesfromKursori(uintptr(address), int(madhësia), int(madhësia))
	for i := uint32(0); i < madhësia; i++ {
		destinacioni_2[i] = 0
	}
	caktonicr3(oldcr3)
}

func makefaqePrivatwritableEtanishme(faqeDosje uint32, virtualaddress uint32) bool {
	pde := GetVlera(faqeDosje + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & Faqepresent) == 0 {
		return false
	}
	pteaddress := (pde & FaqeKornizë) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetVlera(pteaddress)
	if (pte & Faqepresent) == 0 {
		return false
	}
	if (pte & Faqecow) == 0 {
		return (pte & Faqewritable) != 0
	}
	if AktivMemoriaManazhuesi == nil {
		return false
	}
	iRiKursori, _ := AktivMemoriaManazhuesi.Alignedmalloc(0x1000)
	if iRiKursori == nil {
		return false
	}
	iRiKornizë := uint32(uintptr(iRiKursori)) & FaqeKornizë
	burimi_2 := GetbytesfromKursori(uintptr(virtualaddress&FaqeKornizë), 0x1000, 0x1000)
	destinacioni_2 := GetbytesfromKursori(uintptr(iRiKornizë), 0x1000, 0x1000)
	copy(destinacioni_2, burimi_2)
	cowKornizëManazhuesi.Decrement(pte & FaqeKornizë)
	Caktoniunsignedinteger32ataddress((iRiKornizë|(pte&0xFFF)|Faqewritable)&^Faqecow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	ringarkocr3()
	return true
}

func makeIntervalPrivatwritableEtanishme(faqeDosje uint32, address uint32, madhësia uint32) bool {
	if madhësia == 0 {
		return true
	}
	efundit := address + madhësia - 1
	if efundit < address {
		return false
	}
	for faqe := address & FaqeKornizë; ; faqe += 0x1000 {
		if !makefaqePrivatwritableEtanishme(faqeDosje, faqe) {
			return false
		}
		if faqe == (efundit & FaqeKornizë) {
			break
		}
	}
	return true
}

func MakeIntervalPrivatwritable(faqeDosje uint32, address uint32, madhësia uint32) bool {
	if faqeDosje == 0 {
		return false
	}
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	ok := makeIntervalPrivatwritableEtanishme(faqeDosje, address, madhësia)
	caktonicr3(oldcr3)
	return ok
}

func Caktoniunsignedinteger32ZmadhofaqeDosje(x uint32, address uint32, faqeDosje uint32) {
	if faqeDosje == 0 {
		return
	}
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	Caktoniunsignedinteger32ataddress(x, address)
	caktonicr3(oldcr3)
}

func GetVlera(address uint32) uint32 {
	var orgVlera uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgVlera
}
func GetVleraZmadhofaqeDosje(address uint32, faqeDosje uint32) uint32 {
	if faqeDosje == 0 {
		return 0
	}
	oldcr3 := getcr3()
	caktonicr3(faqeDosje)
	v := GetVlera(address)
	caktonicr3(oldcr3)
	return v
}

var v uint32 = 0

func KopjofaqeKornizëblock(xfaqeDosje uint32, yfaqeDosje uint32, vaddress uint32) {
	if xfaqeDosje == 0 || yfaqeDosje == 0 {
		return
	}
	oldcr3 := getcr3()
	caktonicr3(xfaqeDosje)
	v = GetVlera(vaddress)
	Caktoniunsignedinteger32ZmadhofaqeDosje(v, vaddress, yfaqeDosje)

	caktonicr3(oldcr3)
}
