package paging

import unsafe "unsafe"
import . "прекъсване"
import . "паметmanager"
import . "util"

type Страницапапказапис_2 uintptr

const (
	СтраницаНалична		uint32	= 0x001
	Страницаwritable	uint32	= 0x002
	СтраницаСобственик	uint32	= 0x004
	СтраницаРамка		uint32	= 0xFFFFF000
	Страницаcow		uint32	= 0x200
)

func Задайbyteataddress(x byte, address uint32)
func Задайunsignedinteger8ataddress(x uint8, address uint32)
func Задайunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func задайcr3(страницапапка uint32)
func getcr3() uint32

type Paging struct {
	TПрекъсванеhandler
}
type TcowРамкаmanager struct {
	mem		*TПаметmanager
	refs		[]uint16
	рамкаcount	uint32
}

var (
	Страницапапказапис	uintptr
	СтраницаТаблицазапис	uint32
	pdelen			uint32
	virtlen			uint32
	cowРамкаmanager		TcowРамкаmanager
)

func (себеси *TcowРамкаmanager) Init(mem *TПаметmanager, рамкаcount uint32) bool {
	себеси.mem = mem
	себеси.рамкаcount = рамкаcount
	referenceБайтове := рамкаcount * uint32(unsafe.Sizeof(uint16(0)))
	referenceПоказалци := mem.Malloc(referenceБайтове)
	if referenceПоказалци == nil {
		себеси.refs = nil
		себеси.рамкаcount = 0
		return false
	}
	себеси.refs = (*[1 << 28]uint16)(referenceПоказалци)[:рамкаcount:рамкаcount]
	for i := uint32(0); i < рамкаcount; i++ {
		себеси.refs[i] = 0
	}
	return true
}

func (себеси *TcowРамкаmanager) Reference(рамка uint32) uint16 {
	idx := рамка >> 12
	if idx >= себеси.рамкаcount || себеси.refs == nil {
		return 0
	}
	return себеси.refs[idx]
}

func (себеси *TcowРамкаmanager) Increment(рамка uint32) {
	idx := рамка >> 12
	if idx >= себеси.рамкаcount || себеси.refs == nil {
		return
	}
	if себеси.refs[idx] == 0 {
		себеси.refs[idx] = 2
	} else {
		себеси.refs[idx]++
	}
}

func (себеси *TcowРамкаmanager) Decrement(рамка uint32) {
	idx := рамка >> 12
	if idx >= себеси.рамкаcount || себеси.refs == nil || себеси.refs[idx] == 0 {
		return
	}
	себеси.refs[idx]--
}

func (себеси *Paging) Init(страницапапказапис uintptr, страницаТаблицазапис uint32, паметmanager *TПаметmanager) {

	Страницапапказапис = страницапапказапис
	СтраницаТаблицазапис = страницаТаблицазапис

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowРамкаmanager.Init(паметmanager, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressПоказалци, _ := паметmanager.Alignedmalloc(0x1000)
			if addressПоказалци == nil {
				return
			}
			address := uint32(uintptr(addressПоказалци))

			Задайunsignedinteger32ataddress(address|0x87, uint32(страницапапказапис)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Задайunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		страницапапказапис = страницапапказапис + 0x1000
	}

}
func (себеси *Paging) SharedПаметregion() {

	страницапапказапис := Страницапапказапис
	kСтраницапапказапис := Страницапапказапис

	for i := uint32(1); i <= virtlen; i++ {

		страницапапказапис = страницапапказапис + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetСтойност(uint32(kСтраницапапказапис) + pde*4)
			v = (v & 0xFFFFF000)
			Задайunsignedinteger32ataddress(v|0x87, uint32(страницапапказапис)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetСтойност(uint32(kСтраницапапказапис) + pde*4)
			v = (v & 0xFFFFF000)
			Задайunsignedinteger32ataddress(v|0x87, uint32(страницапапказапис)+pde*4)

		}

	}
}
func (себеси *Paging) Страницаfault(manager *TПрекъсванеmanager) {
	прекъсванеhandler = ръкохваткаpagingПрекъсване

	var address uintptr
	address = uintptr(unsafe.Pointer(&прекъсванеhandler))
	себеси.TПрекъсванеhandler.Init(0xE, uintptr(unsafe.Pointer(manager)), address)
}

var прекъсванеhandler func(uint32) uint32

func ръкохваткаpagingПрекъсване(esp uint32) uint32 {
	if ResolveКопиранеВклПисанеfault() {
		return esp
	}
	return РъкохваткаfatalПрекъсванеРамка(esp, 0x0E)
}

func CloneaddressИнтервалcow(източникСтраницапапка uint32) uint32 {
	if АктивнаПаметmanager == nil || източникСтраницапапка == 0 {
		return 0
	}
	назначениеПоказалци, _ := АктивнаПаметmanager.Alignedmalloc(0x1000)
	if назначениеПоказалци == nil {
		return 0
	}
	назначениеСтраницапапка := uint32(uintptr(назначениеПоказалци))
	for i := uint32(0); i < 1024; i++ {
		Задайunsignedinteger32ataddress(0, назначениеСтраницапапка+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		източникpdeaddress := източникСтраницапапка + pde*4
		източникpde := GetСтойност(източникpdeaddress)
		if (източникpde & СтраницаНалична) == 0 {
			continue
		}
		if issharedpde(pde) {
			Задайunsignedinteger32ataddress(източникpde, назначениеСтраницапапка+pde*4)
			continue
		}

		назначениеptПоказалци, _ := АктивнаПаметmanager.Alignedmalloc(0x1000)
		if назначениеptПоказалци == nil {
			continue
		}
		източникpt := източникpde & СтраницаРамка
		назначениеpt := uint32(uintptr(назначениеptПоказалци))
		Задайunsignedinteger32ataddress((назначениеpt | (източникpde & 0xFFF)), назначениеСтраницапапка+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := източникpt + pte*4
			запис := GetСтойност(pteaddress)
			if (запис & СтраницаНалична) != 0 {
				if (запис & Страницаwritable) != 0 {
					запис = (запис &^ Страницаwritable) | Страницаcow
					Задайunsignedinteger32ataddress(запис, pteaddress)
					cowРамкаmanager.Increment(запис & СтраницаРамка)
				} else if (запис & Страницаcow) != 0 {
					cowРамкаmanager.Increment(запис & СтраницаРамка)
				}
			}
			Задайunsignedinteger32ataddress(запис, назначениеpt+pte*4)
		}
	}
	презарежданеcr3()
	return назначениеСтраницапапка
}

func ResolveКопиранеВклПисанеfault() bool {
	if АктивнаПаметmanager == nil {
		return false
	}
	faultaddress := getcr2()
	страницапапка := getcr3()
	pdeaddress := страницапапка + ((faultaddress>>22)&0x3FF)*4
	pde := GetСтойност(pdeaddress)
	if (pde & СтраницаНалична) == 0 {
		return false
	}
	pt := pde & СтраницаРамка
	pteaddress := pt + ((faultaddress>>12)&0x3FF)*4
	pte := GetСтойност(pteaddress)
	if (pte&Страницаcow) == 0 || (pte&СтраницаНалична) == 0 {
		return false
	}
	oldРамка := pte & СтраницаРамка
	if cowРамкаmanager.Reference(oldРамка) <= 1 {
		Задайunsignedinteger32ataddress((pte|Страницаwritable)&^Страницаcow, pteaddress)
		презарежданеcr3()
		return true
	}

	новПоказалци, _ := АктивнаПаметmanager.Alignedmalloc(0x1000)
	if новПоказалци == nil {
		return false
	}
	новРамка := uint32(uintptr(новПоказалци)) & СтраницаРамка

	източник_2 := GetБайтовеfromПоказалци(uintptr(faultaddress&СтраницаРамка), 0x1000, 0x1000)
	назначение_2 := GetБайтовеfromПоказалци(uintptr(новРамка), 0x1000, 0x1000)
	copy(назначение_2, източник_2)
	cowРамкаmanager.Decrement(oldРамка)
	Задайunsignedinteger32ataddress((новРамка|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	презарежданеcr3()
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

func презарежданеcr3() {
	cr3 := getcr3()
	задайcr3(cr3)
}

func ЗадайbyteВходящСтраницапапка(x byte, address uint32, страницапапка uint32) {
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	Задайbyteataddress(x, address)
	задайcr3(oldcr3)
}

func ЗадайБлокВходящСтраницапапка(източник_2 []byte, назначение_2 []byte, размер uint32, страницапапка uint32) {
	if размер == 0 || страницапапка == 0 {
		return
	}
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	makeДиапазонЧастноwritableТекущадата(страницапапка, uint32(uintptr(unsafe.Pointer(&назначение_2[0]))), размер)

	for i := uint32(0); i < размер; i++ {
		назначение_2[i] = източник_2[i]
	}
	задайcr3(oldcr3)
}

func ZeroБлокВходящСтраницапапка(address uint32, размер uint32, страницапапка uint32) {
	if размер == 0 || страницапапка == 0 {
		return
	}
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	makeДиапазонЧастноwritableТекущадата(страницапапка, address, размер)
	назначение_2 := GetБайтовеfromПоказалци(uintptr(address), int(размер), int(размер))
	for i := uint32(0); i < размер; i++ {
		назначение_2[i] = 0
	}
	задайcr3(oldcr3)
}

func makeСтраницаЧастноwritableТекущадата(страницапапка uint32, virtualaddress uint32) bool {
	pde := GetСтойност(страницапапка + ((virtualaddress>>22)&0x3FF)*4)
	if (pde & СтраницаНалична) == 0 {
		return false
	}
	pteaddress := (pde & СтраницаРамка) + ((virtualaddress>>12)&0x3FF)*4
	pte := GetСтойност(pteaddress)
	if (pte & СтраницаНалична) == 0 {
		return false
	}
	if (pte & Страницаcow) == 0 {
		return (pte & Страницаwritable) != 0
	}
	if АктивнаПаметmanager == nil {
		return false
	}
	новПоказалци, _ := АктивнаПаметmanager.Alignedmalloc(0x1000)
	if новПоказалци == nil {
		return false
	}
	новРамка := uint32(uintptr(новПоказалци)) & СтраницаРамка
	източник_2 := GetБайтовеfromПоказалци(uintptr(virtualaddress&СтраницаРамка), 0x1000, 0x1000)
	назначение_2 := GetБайтовеfromПоказалци(uintptr(новРамка), 0x1000, 0x1000)
	copy(назначение_2, източник_2)
	cowРамкаmanager.Decrement(pte & СтраницаРамка)
	Задайunsignedinteger32ataddress((новРамка|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	презарежданеcr3()
	return true
}

func makeДиапазонЧастноwritableТекущадата(страницапапка uint32, address uint32, размер uint32) bool {
	if размер == 0 {
		return true
	}
	последно := address + размер - 1
	if последно < address {
		return false
	}
	for страница := address & СтраницаРамка; ; страница += 0x1000 {
		if !makeСтраницаЧастноwritableТекущадата(страницапапка, страница) {
			return false
		}
		if страница == (последно & СтраницаРамка) {
			break
		}
	}
	return true
}

func MakeДиапазонЧастноwritable(страницапапка uint32, address uint32, размер uint32) bool {
	if страницапапка == 0 {
		return false
	}
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	приеми := makeДиапазонЧастноwritableТекущадата(страницапапка, address, размер)
	задайcr3(oldcr3)
	return приеми
}

func Задайunsignedinteger32ВходящСтраницапапка(x uint32, address uint32, страницапапка uint32) {
	if страницапапка == 0 {
		return
	}
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	Задайunsignedinteger32ataddress(x, address)
	задайcr3(oldcr3)
}

func GetСтойност(address uint32) uint32 {
	var orgСтойност uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgСтойност
}
func GetСтойностВходящСтраницапапка(address uint32, страницапапка uint32) uint32 {
	if страницапапка == 0 {
		return 0
	}
	oldcr3 := getcr3()
	задайcr3(страницапапка)
	v := GetСтойност(address)
	задайcr3(oldcr3)
	return v
}

var v uint32 = 0

func КопиранеСтраницаРамкаБлок(xСтраницапапка uint32, yСтраницапапка uint32, vaddress uint32) {
	if xСтраницапапка == 0 || yСтраницапапка == 0 {
		return
	}
	oldcr3 := getcr3()
	задайcr3(xСтраницапапка)
	v = GetСтойност(vaddress)
	Задайunsignedinteger32ВходящСтраницапапка(v, vaddress, yСтраницапапка)

	задайcr3(oldcr3)
}
