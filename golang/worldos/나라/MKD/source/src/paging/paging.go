/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package paging

import unsafe "unsafe"
import . "interrupt"
import . "меморијаmanager"
import . "util"

type СтраницаДиректориумentry_2 uintptr

const (
	Страницаpresent		uint32	= 0x001
	Страницаwritable	uint32	= 0x002
	СтраницаКорисник	uint32	= 0x004
	СтраницаРамка		uint32	= 0xFFFFF000
	Страницаcow		uint32	= 0x200
)

func Поставиbyteataddress(x byte, address uint32)
func Поставиunsignedinteger8ataddress(x uint8, address uint32)
func Поставиunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func поставиcr3(страницаДиректориум uint32)
func getcr3() uint32

type Paging struct {
	TInterrupthandler
}
type TcowРамкаmanager struct {
	mem		*TМеморијаmanager
	refs		[]uint16
	рамкаcount	uint32
}

var (
	СтраницаДиректориумentry	uintptr
	СтраницаТабелаentry		uint32
	pdelen				uint32
	virtlen				uint32
	cowРамкаmanager			TcowРамкаmanager
)

func (само *TcowРамкаmanager) Init(mem *TМеморијаmanager, рамкаcount uint32) bool {
	само.mem = mem
	само.рамкаcount = рамкаcount
	referenceбајти := рамкаcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceСтрелка := mem.Malloc(referenceбајти)
	if referenceСтрелка == nil {
		само.refs = nil
		само.рамкаcount = 0
		return false
	}
	само.refs = (*[1 << 28]uint16)(referenceСтрелка)[:рамкаcount:рамкаcount]
	for i := uint32(0); i < рамкаcount; i++ {
		само.refs[i] = 0
	}
	return true
}

func (само *TcowРамкаmanager) Reference(рамка uint32) uint16 {
	idx := рамка >> 12
	if idx >= само.рамкаcount || само.refs == nil {
		return 0
	}
	return само.refs[idx]
}

func (само *TcowРамкаmanager) Increment(рамка uint32) {
	idx := рамка >> 12
	if idx >= само.рамкаcount || само.refs == nil {
		return
	}
	if само.refs[idx] == 0 {
		само.refs[idx] = 2
	} else {
		само.refs[idx]++
	}
}

func (само *TcowРамкаmanager) Decrement(рамка uint32) {
	idx := рамка >> 12
	if idx >= само.рамкаcount || само.refs == nil || само.refs[idx] == 0 {
		return
	}
	само.refs[idx]--
}

func (само *Paging) Init(страницаДиректориумentry uintptr, страницаТабелаentry uint32, меморијаmanager *TМеморијаmanager) {

	СтраницаДиректориумentry = страницаДиректориумentry
	СтраницаТабелаentry = страницаТабелаentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowРамкаmanager.Init(меморијаmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressСтрелка, _ := меморијаmanager.Alignedmalloc(0x1000)
			if addressСтрелка == nil {
				return
			}
			address := uint32(uintptr(addressСтрелка))

			Поставиunsignedinteger32ataddress(address|0x87, uint32(страницаДиректориумentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Поставиunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		страницаДиректориумentry = страницаДиректориумentry + 0x1000
	}

}
func (само *Paging) SharedМеморијаregion() {

	страницаДиректориумentry := СтраницаДиректориумentry
	kСтраницаДиректориумentry := СтраницаДиректориумentry

	for i := uint32(1); i <= virtlen; i++ {

		страницаДиректориумentry = страницаДиректориумentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetВредност(uint32(kСтраницаДиректориумentry) + pde*4)
			v = (v & 0xFFFFF000)
			Поставиunsignedinteger32ataddress(v|0x87, uint32(страницаДиректориумentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetВредност(uint32(kСтраницаДиректориумentry) + pde*4)
			v = (v & 0xFFFFF000)
			Поставиunsignedinteger32ataddress(v|0x87, uint32(страницаДиректориумentry)+pde*4)

		}

	}
}
func (само *Paging) Страницаfault(manager *TInterruptmanager) {
	interrupthandler = handlepaginginterrupt

	var address uintptr
	address = uintptr(unsafe.Pointer(&interrupthandler))
	само.TInterrupthandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handlepaginginterrupt(esp uint32) uint32 {
	if ResolveКопирајВклученоЗапишиfault() {
		return esp
	}
	return HandlefatalinterruptРамка(esp, 0x0E)
}

func Cloneaddressspacecow(изворСтраницаДиректориум uint32) uint32 {
	if АктивноМеморијаmanager == nil || изворСтраницаДиректориум == 0 {
		return 0
	}
	одредиштеСтрелка, _ := АктивноМеморијаmanager.Alignedmalloc(0x1000)
	if одредиштеСтрелка == nil {
		return 0
	}
	одредиштеСтраницаДиректориум := uint32(uintptr(одредиштеСтрелка))
	for i := uint32(0); i < 1024; i++ {
		Поставиunsignedinteger32ataddress(0, одредиштеСтраницаДиректориум+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		изворpdeaddress := изворСтраницаДиректориум + pde*4
		изворpde := GetВредност(изворpdeaddress)
		if (изворpde & Страницаpresent) == 0 {
			continue
		}
		if issharedpde(pde) {
			Поставиunsignedinteger32ataddress(изворpde, одредиштеСтраницаДиректориум+pde*4)
			continue
		}

		одредиштеptСтрелка, _ := АктивноМеморијаmanager.Alignedmalloc(0x1000)
		if одредиштеptСтрелка == nil {
			continue
		}
		изворpt := изворpde & СтраницаРамка
		одредиштеpt := uint32(uintptr(одредиштеptСтрелка))
		Поставиunsignedinteger32ataddress((одредиштеpt | (изворpde & 0xFFF)), одредиштеСтраницаДиректориум+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := изворpt + pte*4
			entry := GetВредност(pteaddress)
			if (entry & Страницаpresent) != 0 {
				if (entry & Страницаwritable) != 0 {
					entry = (entry &^ Страницаwritable) | Страницаcow
					Поставиunsignedinteger32ataddress(entry, pteaddress)
					cowРамкаmanager.Increment(entry & СтраницаРамка)
				} else if (entry & Страницаcow) != 0 {
					cowРамкаmanager.Increment(entry & СтраницаРамка)
				}
			}
			Поставиunsignedinteger32ataddress(entry, одредиштеpt+pte*4)
		}
	}
	освежиcr3()
	return одредиштеСтраницаДиректориум
}

func ResolveКопирајВклученоЗапишиfault() bool {
	if АктивноМеморијаmanager == nil {
		return false
	}
	faultaddress := getcr2()
	страницаДиректориум := getcr3()
	pdeaddress := страницаДиректориум + ((faultaddress>>22)&0x3FF)*4
	pde := GetВредност(pdeaddress)
	if (pde & Страницаpresent) == 0 {
		return false
	}
	pt := pde & СтраницаРамка
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte&Страницаcow) == 0 || (pte&Страницаpresent) == 0 {
		return false
	}
	oldРамка := pte & СтраницаРамка
	if cowРамкаmanager.Reference(oldРамка) <= 1 {
		Поставиunsignedinteger32ataddress((pte|Страницаwritable)&^Страницаcow, pteaddress)
		освежиcr3()
		return true
	}

	новСтрелка, _ := АктивноМеморијаmanager.Alignedmalloc(0x1000)
	if новСтрелка == nil {
		return false
	}
	новРамка := uint32(uintptr(новСтрелка)) & СтраницаРамка

	извор_2 := GetбајтиfromСтрелка(uintptr(faultaddress&СтраницаРамка), 0x1000, 0x1000)
	одредиште_2 := GetбајтиfromСтрелка(uintptr(новРамка), 0x1000, 0x1000)
	copy(одредиште_2, извор_2)
	cowРамкаmanager.Decrement(oldРамка)
	Поставиunsignedinteger32ataddress((новРамка|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	освежиcr3()
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

func освежиcr3() {
	cr3 := getcr3()
	поставиcr3(cr3)
}

func ПоставиbyteвоСтраницаДиректориум(x byte, address uint32, страницаДиректориум uint32) {
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	Поставиbyteataddress(x, address)
	поставиcr3(oldcr3)
}

func ПоставиblockвоСтраницаДиректориум(извор_2 []byte, одредиште_2 []byte, големина uint32, страницаДиректориум uint32) {
	if големина == 0 || страницаДиректориум == 0 {
		return
	}
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	makeОпсегПриватноwritablecurrent(страницаДиректориум, uint32(uintptr(unsafe.Pointer(&одредиште_2[0]))), големина)

	for i := uint32(0); i < големина; i++ {
		одредиште_2[i] = извор_2[i]
	}
	поставиcr3(oldcr3)
}

func ZeroblockвоСтраницаДиректориум(address uint32, големина uint32, страницаДиректориум uint32) {
	if големина == 0 || страницаДиректориум == 0 {
		return
	}
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	makeОпсегПриватноwritablecurrent(страницаДиректориум, address, големина)
	одредиште_2 := GetбајтиfromСтрелка(uintptr(address), int(големина), int(големина))
	for i := uint32(0); i < големина; i++ {
		одредиште_2[i] = 0
	}
	поставиcr3(oldcr3)
}

func makeСтраницаПриватноwritablecurrent(страницаДиректориум uint32, виртуелноaddress uint32) bool {
	pde := GetВредност(страницаДиректориум + ((виртуелноaddress>>22)&0x3FF)*4)
	if (pde & Страницаpresent) == 0 {
		return false
	}
	pteaddress := (pde & СтраницаРамка) + ((виртуелноaddress>>12)&0x3FF)*4
	pte := GetВредност(pteaddress)
	if (pte & Страницаpresent) == 0 {
		return false
	}
	if (pte & Страницаcow) == 0 {
		return (pte & Страницаwritable) != 0
	}
	if АктивноМеморијаmanager == nil {
		return false
	}
	новСтрелка, _ := АктивноМеморијаmanager.Alignedmalloc(0x1000)
	if новСтрелка == nil {
		return false
	}
	новРамка := uint32(uintptr(новСтрелка)) & СтраницаРамка
	извор_2 := GetбајтиfromСтрелка(uintptr(виртуелноaddress&СтраницаРамка), 0x1000, 0x1000)
	одредиште_2 := GetбајтиfromСтрелка(uintptr(новРамка), 0x1000, 0x1000)
	copy(одредиште_2, извор_2)
	cowРамкаmanager.Decrement(pte & СтраницаРамка)
	Поставиunsignedinteger32ataddress((новРамка|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	освежиcr3()
	return true
}

func makeОпсегПриватноwritablecurrent(страницаДиректориум uint32, address uint32, големина uint32) bool {
	if големина == 0 {
		return true
	}
	последно := address + големина - 1
	if последно < address {
		return false
	}
	for страница := address & СтраницаРамка; ; страница += 0x1000 {
		if !makeСтраницаПриватноwritablecurrent(страницаДиректориум, страница) {
			return false
		}
		if страница == (последно & СтраницаРамка) {
			break
		}
	}
	return true
}

func MakeОпсегПриватноwritable(страницаДиректориум uint32, address uint32, големина uint32) bool {
	if страницаДиректориум == 0 {
		return false
	}
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	воред := makeОпсегПриватноwritablecurrent(страницаДиректориум, address, големина)
	поставиcr3(oldcr3)
	return воред
}

func Поставиunsignedinteger32воСтраницаДиректориум(x uint32, address uint32, страницаДиректориум uint32) {
	if страницаДиректориум == 0 {
		return
	}
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	Поставиunsignedinteger32ataddress(x, address)
	поставиcr3(oldcr3)
}

func GetВредност(address uint32) uint32 {
	var orgВредност uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgВредност
}
func GetВредноствоСтраницаДиректориум(address uint32, страницаДиректориум uint32) uint32 {
	if страницаДиректориум == 0 {
		return 0
	}
	oldcr3 := getcr3()
	поставиcr3(страницаДиректориум)
	v := GetВредност(address)
	поставиcr3(oldcr3)
	return v
}

var v uint32 = 0

func КопирајСтраницаРамкаblock(xСтраницаДиректориум uint32, yСтраницаДиректориум uint32, vaddress uint32) {
	if xСтраницаДиректориум == 0 || yСтраницаДиректориум == 0 {
		return
	}
	oldcr3 := getcr3()
	поставиcr3(xСтраницаДиректориум)
	v = GetВредност(vaddress)
	Поставиunsignedinteger32воСтраницаДиректориум(v, vaddress, yСтраницаДиректориум)

	поставиcr3(oldcr3)
}
