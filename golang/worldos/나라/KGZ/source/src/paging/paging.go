/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "эсиmanager"
import . "util"

type БАРАКкаталогentry_2 uintptr

const (
	БАРАКpresent	uint32	= 0x001
	БАРАКwritable	uint32	= 0x002
	БАРАККолдонуучу	uint32	= 0x004
	БАРАКframe	uint32	= 0xFFFFF000
	БАРАКcow	uint32	= 0x200
)

func Setbyteataddress(x byte, address uint32)
func Setunsignedinteger8ataddress(x uint8, address uint32)
func Setunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func setcr3(бАРАКкаталог uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type Tcowframemanager struct {
	mem		*TЭсиmanager
	refs		[]uint16
	framecount	uint32
}

var (
	БАРАКкаталогentry	uintptr
	БАРАКЖадыбалentry	uint32
	pdelen			uint32
	virtlen			uint32
	cowframemanager		Tcowframemanager
)

func (self *Tcowframemanager) Init(mem *TЭсиmanager, framecount uint32) bool {
	self.mem = mem
	self.framecount = framecount
	referenceБайт := framecount * uint32(unsafe.Sizeof(uint16(0)))
	referenceКөрсөткүч := mem.Malloc(referenceБайт)
	if referenceКөрсөткүч == nil {
		self.refs = nil
		self.framecount = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceКөрсөткүч)[:framecount:framecount]
	for i := uint32(0); i < framecount; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowframemanager) Reference(frame uint32) uint16 {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowframemanager) Increment(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowframemanager) Decrement(frame uint32) {
	idx := frame >> 12
	if idx >= self.framecount || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Paging) Init(бАРАКкаталогentry uintptr, бАРАКЖадыбалentry uint32, эсиmanager *TЭсиmanager) {

	БАРАКкаталогentry = бАРАКкаталогentry
	БАРАКЖадыбалentry = бАРАКЖадыбалentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowframemanager.Init(эсиmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressКөрсөткүч, _ := эсиmanager.Alignedmalloc(0x1000)
			if addressКөрсөткүч == nil {
				return
			}
			address := uint32(uintptr(addressКөрсөткүч))

			Setunsignedinteger32ataddress(address|0x87, uint32(бАРАКкаталогentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Setunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		бАРАКкаталогentry = бАРАКкаталогentry + 0x1000
	}

}
func (self *Paging) SharedЭсиregion() {

	бАРАКкаталогentry := БАРАКкаталогentry
	kБАРАКкаталогentry := БАРАКкаталогentry

	for i := uint32(1); i <= virtlen; i++ {

		бАРАКкаталогentry = бАРАКкаталогentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetМааниси(uint32(kБАРАКкаталогentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(бАРАКкаталогentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetМааниси(uint32(kБАРАКкаталогentry) + pde*4)
			v = (v & 0xFFFFF000)
			Setunsignedinteger32ataddress(v|0x87, uint32(бАРАКкаталогentry)+pde*4)

		}

	}
}
func (self *Paging) БАРАКfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveКөчүрүүonЖазууfault() {
		return esp
	}
	return Handlefatalinterruptframe(esp, 0x0E)
}

func Cloneaddressspacecow(баштапкытекстБАРАКкаталог uint32) uint32 {
	if АктивдүүЭсиmanager == nil || баштапкытекстБАРАКкаталог == 0 {
		return 0
	}
	destinationКөрсөткүч, _ := АктивдүүЭсиmanager.Alignedmalloc(0x1000)
	if destinationКөрсөткүч == nil {
		return 0
	}
	destinationБАРАКкаталог := uint32(uintptr(destinationКөрсөткүч))
	for i := uint32(0); i < 1024; i++ {
		Setunsignedinteger32ataddress(0, destinationБАРАКкаталог+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		баштапкытекстpdeaddress := баштапкытекстБАРАКкаталог + pde*4
		баштапкытекстpde := GetМааниси(баштапкытекстpdeaddress)
		if (баштапкытекстpde & БАРАКpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Setunsignedinteger32ataddress(баштапкытекстpde, destinationБАРАКкаталог+pde*4)
			continue
		}

		destinationptКөрсөткүч, _ := АктивдүүЭсиmanager.Alignedmalloc(0x1000)
		if destinationptКөрсөткүч == nil {
			continue
		}
		баштапкытекстpt := баштапкытекстpde & БАРАКframe
		destinationpt := uint32(uintptr(destinationptКөрсөткүч))
		Setunsignedinteger32ataddress((destinationpt | (баштапкытекстpde & 0xFFF)), destinationБАРАКкаталог+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := баштапкытекстpt + pte*4
			entry := GetМааниси(pteaddress)
			if (entry & БАРАКpresent) != 0 {
				if (entry & БАРАКwritable) != 0 {
					entry = (entry &^ БАРАКwritable) | БАРАКcow
					Setunsignedinteger32ataddress(entry, pteaddress)
					cowframemanager.Increment(entry & БАРАКframe)
				} else if (entry & БАРАКcow) != 0 {
					cowframemanager.Increment(entry & БАРАКframe)
				}
			}
			Setunsignedinteger32ataddress(entry, destinationpt+pte*4)
		}
	}
	кайтаданжүктөөcr3()
	return destinationБАРАКкаталог
}

func ResolveКөчүрүүonЖазууfault() bool {
	if АктивдүүЭсиmanager == nil {
		return false
	}
	faultaddress := getcr2()
	бАРАКкаталог := getcr3()
	pdeaddress := бАРАКкаталог + ((faultaddress>>22)&0x3FF)*4
	pde := GetМааниси(pdeaddress)
	if (pde & БАРАКpresent) == 0 {
		return false
	}
	pt := pde & БАРАКframe
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetМааниси(pteaddress)
	if (pte&БАРАКcow) == 0 || (pte&БАРАКpresent) == 0 {
		return false
	}
	oldframe := pte & БАРАКframe
	if cowframemanager.Reference(oldframe) <= 1 {
		Setunsignedinteger32ataddress((pte|БАРАКwritable)&^БАРАКcow, pteaddress)
		кайтаданжүктөөcr3()
		return true
	}

	жаңыКөрсөткүч, _ := АктивдүүЭсиmanager.Alignedmalloc(0x1000)
	if жаңыКөрсөткүч == nil {
		return false
	}
	жаңыframe := uint32(uintptr(жаңыКөрсөткүч)) & БАРАКframe

	баштапкытекст_2 := GetБайтfromКөрсөткүч(uintptr(faultaddress&БАРАКframe), 0x1000, 0x1000)
	destination_2 := GetБайтfromКөрсөткүч(uintptr(жаңыframe), 0x1000, 0x1000)
	copy(destination_2, баштапкытекст_2)
	cowframemanager.Decrement(oldframe)
	Setunsignedinteger32ataddress((жаңыframe|(pte&0xFFF)|БАРАКwritable)&^БАРАКcow, pteaddress)
	кайтаданжүктөөcr3()
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

func кайтаданжүктөөcr3() {
	cr3 := getcr3()
	setcr3(cr3)
}

func SetbyteЧоңойтууБАРАКкаталог(x byte, address uint32, бАРАКкаталог uint32) {
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	Setbyteataddress(x, address)
	setcr3(oldcr3)
}

func SetБлокЧоңойтууБАРАКкаталог(баштапкытекст_2 []byte, destination_2 []byte, өлчөм uint32, бАРАКкаталог uint32) {
	if өлчөм == 0 || бАРАКкаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	makeДиапазонprivatewritablecurrent(бАРАКкаталог, uint32(uintptr(unsafe.Pointer(&destination_2[0]))), өлчөм)

	for i := uint32(0); i < өлчөм; i++ {
		destination_2[i] = баштапкытекст_2[i]
	}
	setcr3(oldcr3)
}

func ZeroБлокЧоңойтууБАРАКкаталог(address uint32, өлчөм uint32, бАРАКкаталог uint32) {
	if өлчөм == 0 || бАРАКкаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	makeДиапазонprivatewritablecurrent(бАРАКкаталог, address, өлчөм)
	destination_2 := GetБайтfromКөрсөткүч(uintptr(address), int(өлчөм), int(өлчөм))
	for i := uint32(0); i < өлчөм; i++ {
		destination_2[i] = 0
	}
	setcr3(oldcr3)
}

func makeБАРАКprivatewritablecurrent(бАРАКкаталог uint32, virtualaddress uint32) bool {
	pde := GetМааниси(бАРАКкаталог + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & БАРАКpresent) == 0 {
		return false
	}
	pteaddress := (pde & БАРАКframe) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetМааниси(pteaddress)
	if (pte & БАРАКpresent) == 0 {
		return false
	}
	if (pte & БАРАКcow) == 0 {
		return (pte & БАРАКwritable) != 0
	}
	if АктивдүүЭсиmanager == nil {
		return false
	}
	жаңыКөрсөткүч, _ := АктивдүүЭсиmanager.Alignedmalloc(0x1000)
	if жаңыКөрсөткүч == nil {
		return false
	}
	жаңыframe := uint32(uintptr(жаңыКөрсөткүч)) & БАРАКframe
	баштапкытекст_2 := GetБайтfromКөрсөткүч(uintptr(virtualaddress&БАРАКframe), 0x1000, 0x1000)
	destination_2 := GetБайтfromКөрсөткүч(uintptr(жаңыframe), 0x1000, 0x1000)
	copy(destination_2, баштапкытекст_2)
	cowframemanager.Decrement(pte & БАРАКframe)
	Setunsignedinteger32ataddress((жаңыframe|(pte&0xFFF)|БАРАКwritable)&^БАРАКcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	кайтаданжүктөөcr3()
	return true
}

func makeДиапазонprivatewritablecurrent(бАРАКкаталог uint32, address uint32, өлчөм uint32) bool {
	if өлчөм == 0 {
		return true
	}
	last := address + өлчөм - 1
	if last < address {
		return false
	}
	for бАРАК := address & БАРАКframe; ; бАРАК += 0x1000 {
		if !makeБАРАКprivatewritablecurrent(бАРАКкаталог, бАРАК) {
			return false
		}
		if бАРАК == (last & БАРАКframe) {
			break
		}
	}
	return true
}

func MakeДиапазонprivatewritable(бАРАКкаталог uint32, address uint32, өлчөм uint32) bool {
	if бАРАКкаталог == 0 {
		return false
	}
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	ok := makeДиапазонprivatewritablecurrent(бАРАКкаталог, address, өлчөм)
	setcr3(oldcr3)
	return ok
}

func Setunsignedinteger32ЧоңойтууБАРАКкаталог(x uint32, address uint32, бАРАКкаталог uint32) {
	if бАРАКкаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	Setunsignedinteger32ataddress(x, address)
	setcr3(oldcr3)
}

func GetМааниси(address uint32) uint32 {
	var orgМааниси uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgМааниси
}
func GetМаанисиЧоңойтууБАРАКкаталог(address uint32, бАРАКкаталог uint32) uint32 {
	if бАРАКкаталог == 0 {
		return 0
	}
	oldcr3 := getcr3()
	setcr3(бАРАКкаталог)
	v := GetМааниси(address)
	setcr3(oldcr3)
	return v
}

var v uint32 = 0

func КөчүрүүБАРАКframeБлок(xБАРАКкаталог uint32, yБАРАКкаталог uint32, vaddress uint32) {
	if xБАРАКкаталог == 0 || yБАРАКкаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	setcr3(xБАРАКкаталог)
	v = GetМааниси(vaddress)
	Setunsignedinteger32ЧоңойтууБАРАКкаталог(v, vaddress, yБАРАКкаталог)

	setcr3(oldcr3)
}
