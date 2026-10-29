/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package управлениеСтраницами

import unsafe "unsafe"
import . "прерывание"
import . "памятьдиспетчер"
import . "утилита"

type Страницакаталогзапись_2 uintptr

const (
	СтраницаПрисутствует	uint32	= 0x001
	Страницаwritable	uint32	= 0x002
	Страницапользователь	uint32	= 0x004
	Страницакадр		uint32	= 0xFFFFF000
	Страницаcow		uint32	= 0x200
)

func Указатьбайтataddress(x byte, address uint32)
func Указатьunsignedinteger8ataddress(x uint8, address uint32)
func Указатьunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func указатьcr3(каталог_страниц uint32)
func getcr3() uint32

type УправлениеСтраницами struct {
	TПрерываниеhandler
}
type Tcowкадрдиспетчер struct {
	mem		*TПамятьдиспетчер
	refs		[]uint16
	кадрКоличество	uint32
}

var (
	Страницакаталогзапись	uintptr
	СтраницаТаблицазапись	uint32
	pdelen			uint32
	virtlen			uint32
	cowкадрдиспетчер	Tcowкадрдиспетчер
)

func (текущий *Tcowкадрдиспетчер) Init(mem *TПамятьдиспетчер, кадрКоличество uint32) bool {
	текущий.mem = mem
	текущий.кадрКоличество = кадрКоличество
	referenceБайт := кадрКоличество * uint32(unsafe.Sizeof(uint16(0)))
	referenceУказатели := mem.Выделить_память(referenceБайт)
	if referenceУказатели == nil {
		текущий.refs = nil
		текущий.кадрКоличество = 0
		return false
	}
	текущий.refs = (*[1 << 28]uint16)(referenceУказатели)[:кадрКоличество:кадрКоличество]
	for i := uint32(0); i < кадрКоличество; i++ {
		текущий.refs[i] = 0
	}
	return true
}

func (текущий *Tcowкадрдиспетчер) Reference(кадр uint32) uint16 {
	idx := кадр >> 12
	if idx >= текущий.кадрКоличество || текущий.refs == nil {
		return 0
	}
	return текущий.refs[idx]
}

func (текущий *Tcowкадрдиспетчер) Increment(кадр uint32) {
	idx := кадр >> 12
	if idx >= текущий.кадрКоличество || текущий.refs == nil {
		return
	}
	if текущий.refs[idx] == 0 {
		текущий.refs[idx] = 2
	} else {
		текущий.refs[idx]++
	}
}

func (текущий *Tcowкадрдиспетчер) Decrement(кадр uint32) {
	idx := кадр >> 12
	if idx >= текущий.кадрКоличество || текущий.refs == nil || текущий.refs[idx] == 0 {
		return
	}
	текущий.refs[idx]--
}

func (текущий *УправлениеСтраницами) Init(страницакаталогзапись uintptr, страницаТаблицазапись uint32, памятьдиспетчер *TПамятьдиспетчер) {

	Страницакаталогзапись = страницакаталогзапись
	СтраницаТаблицазапись = страницаТаблицазапись

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowкадрдиспетчер.Init(памятьдиспетчер, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressУказатели, _ := памятьдиспетчер.Alignedmalloc(0x1000)
			if addressУказатели == nil {
				return
			}
			address := uint32(uintptr(addressУказатели))

			Указатьunsignedinteger32ataddress(address|0x87, uint32(страницакаталогзапись)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Указатьunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		страницакаталогзапись = страницакаталогзапись + 0x1000
	}

}
func (текущий *УправлениеСтраницами) Sharedпамятьregion() {

	страницакаталогзапись := Страницакаталогзапись
	kстраницакаталогзапись := Страницакаталогзапись

	for i := uint32(1); i <= virtlen; i++ {

		страницакаталогзапись = страницакаталогзапись + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := GetЗначение(uint32(kстраницакаталогзапись) + pde*4)
			v = (v & 0xFFFFF000)
			Указатьunsignedinteger32ataddress(v|0x87, uint32(страницакаталогзапись)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := GetЗначение(uint32(kстраницакаталогзапись) + pde*4)
			v = (v & 0xFFFFF000)
			Указатьunsignedinteger32ataddress(v|0x87, uint32(страницакаталогзапись)+pde*4)

		}

	}
}
func (текущий *УправлениеСтраницами) Страницаошибка(диспетчер *TПрерываниедиспетчер) {
	прерываниеhandler = ручкауправлениеСтраницамипрерывание

	var address uintptr
	address = uintptr(unsafe.Pointer(&прерываниеhandler))
	текущий.TПрерываниеhandler.Init(0xE, uintptr(unsafe.Pointer(диспетчер)), address)
}

var прерываниеhandler func(uint32) uint32

func ручкауправлениеСтраницамипрерывание(esp uint32) uint32 {
	if Разрешитькопироватьприписатьошибка() {
		return esp
	}
	return Ручкаfatalпрерываниекадр(esp, 0x0E)
}

func CloneaddressПробелcow(источникстраницакаталог uint32) uint32 {
	if Активнопамятьдиспетчер == nil || источникстраницакаталог == 0 {
		return 0
	}
	назначениеУказатели, _ := Активнопамятьдиспетчер.Alignedmalloc(0x1000)
	if назначениеУказатели == nil {
		return 0
	}
	назначениестраницакаталог := uint32(uintptr(назначениеУказатели))
	for i := uint32(0); i < 1024; i++ {
		Указатьunsignedinteger32ataddress(0, назначениестраницакаталог+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		источникpdeaddress := источникстраницакаталог + pde*4
		источникpde := GetЗначение(источникpdeaddress)
		if (источникpde & СтраницаПрисутствует) == 0 {
			continue
		}
		if issharedpde(pde) {
			Указатьunsignedinteger32ataddress(источникpde, назначениестраницакаталог+pde*4)
			continue
		}

		назначениеptУказатели, _ := Активнопамятьдиспетчер.Alignedmalloc(0x1000)
		if назначениеptУказатели == nil {
			continue
		}
		источникpt := источникpde & Страницакадр
		назначениеpt := uint32(uintptr(назначениеptУказатели))
		Указатьunsignedinteger32ataddress((назначениеpt | (источникpde & 0xFFF)), назначениестраницакаталог+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := источникpt + pte*4
			запись := GetЗначение(pteaddress)
			if (запись & СтраницаПрисутствует) != 0 {
				if (запись & Страницаwritable) != 0 {
					запись = (запись &^ Страницаwritable) | Страницаcow
					Указатьunsignedinteger32ataddress(запись, pteaddress)
					cowкадрдиспетчер.Increment(запись & Страницакадр)
				} else if (запись & Страницаcow) != 0 {
					cowкадрдиспетчер.Increment(запись & Страницакадр)
				}
			}
			Указатьunsignedinteger32ataddress(запись, назначениеpt+pte*4)
		}
	}
	обновитьcr3()
	return назначениестраницакаталог
}

func Разрешитькопироватьприписатьошибка() bool {
	if Активнопамятьдиспетчер == nil {
		return false
	}
	ошибкаaddress := getcr2()
	каталог_страниц := getcr3()
	pdeaddress := каталог_страниц + ((ошибкаaddress>>22)&0x3FF)*4
	pde := GetЗначение(pdeaddress)
	if (pde & СтраницаПрисутствует) == 0 {
		return false
	}
	pt := pde & Страницакадр
	pteaddress := pt + ((ошибкаaddress>>12)&0x3FF)*4
	pte := GetЗначение(pteaddress)
	if (pte&Страницаcow) == 0 || (pte&СтраницаПрисутствует) == 0 {
		return false
	}
	oldкадр := pte & Страницакадр
	if cowкадрдиспетчер.Reference(oldкадр) <= 1 {
		Указатьunsignedinteger32ataddress((pte|Страницаwritable)&^Страницаcow, pteaddress)
		обновитьcr3()
		return true
	}

	новыйУказатели, _ := Активнопамятьдиспетчер.Alignedmalloc(0x1000)
	if новыйУказатели == nil {
		return false
	}
	новыйкадр := uint32(uintptr(новыйУказатели)) & Страницакадр

	источник_2 := GetБайтfromУказатели(uintptr(ошибкаaddress&Страницакадр), 0x1000, 0x1000)
	назначение_2 := GetБайтfromУказатели(uintptr(новыйкадр), 0x1000, 0x1000)
	copy(назначение_2, источник_2)
	cowкадрдиспетчер.Decrement(oldкадр)
	Указатьunsignedinteger32ataddress((новыйкадр|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	обновитьcr3()
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

func обновитьcr3() {
	cr3 := getcr3()
	указатьcr3(cr3)
}

func УказатьбайтИсходящийстраницакаталог(x byte, address uint32, каталог_страниц uint32) {
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	Указатьбайтataddress(x, address)
	указатьcr3(oldcr3)
}

func УказатьБлокИсходящийстраницакаталог(источник_2 []byte, назначение_2 []byte, размер uint32, каталог_страниц uint32) {
	if размер == 0 || каталог_страниц == 0 {
		return
	}
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	makeДиапазонЧастнаяwritableТекущаядата(каталог_страниц, uint32(uintptr(unsafe.Pointer(&назначение_2[0]))), размер)

	for i := uint32(0); i < размер; i++ {
		назначение_2[i] = источник_2[i]
	}
	указатьcr3(oldcr3)
}

func НольБлокИсходящийстраницакаталог(address uint32, размер uint32, каталог_страниц uint32) {
	if размер == 0 || каталог_страниц == 0 {
		return
	}
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	makeДиапазонЧастнаяwritableТекущаядата(каталог_страниц, address, размер)
	назначение_2 := GetБайтfromУказатели(uintptr(address), int(размер), int(размер))
	for i := uint32(0); i < размер; i++ {
		назначение_2[i] = 0
	}
	указатьcr3(oldcr3)
}

func makeстраницаЧастнаяwritableТекущаядата(каталог_страниц uint32, виртуальныйaddress uint32) bool {
	pde := GetЗначение(каталог_страниц + ((виртуальныйaddress>>22)&0x3FF)*4)
	if (pde & СтраницаПрисутствует) == 0 {
		return false
	}
	pteaddress := (pde & Страницакадр) + ((виртуальныйaddress>>12)&0x3FF)*4
	pte := GetЗначение(pteaddress)
	if (pte & СтраницаПрисутствует) == 0 {
		return false
	}
	if (pte & Страницаcow) == 0 {
		return (pte & Страницаwritable) != 0
	}
	if Активнопамятьдиспетчер == nil {
		return false
	}
	новыйУказатели, _ := Активнопамятьдиспетчер.Alignedmalloc(0x1000)
	if новыйУказатели == nil {
		return false
	}
	новыйкадр := uint32(uintptr(новыйУказатели)) & Страницакадр
	источник_2 := GetБайтfromУказатели(uintptr(виртуальныйaddress&Страницакадр), 0x1000, 0x1000)
	назначение_2 := GetБайтfromУказатели(uintptr(новыйкадр), 0x1000, 0x1000)
	copy(назначение_2, источник_2)
	cowкадрдиспетчер.Decrement(pte & Страницакадр)
	Указатьunsignedinteger32ataddress((новыйкадр|(pte&0xFFF)|Страницаwritable)&^Страницаcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	обновитьcr3()
	return true
}

func makeДиапазонЧастнаяwritableТекущаядата(каталог_страниц uint32, address uint32, размер uint32) bool {
	if размер == 0 {
		return true
	}
	последнее := address + размер - 1
	if последнее < address {
		return false
	}
	for страница := address & Страницакадр; ; страница += 0x1000 {
		if !makeстраницаЧастнаяwritableТекущаядата(каталог_страниц, страница) {
			return false
		}
		if страница == (последнее & Страницакадр) {
			break
		}
	}
	return true
}

func MakeДиапазонЧастнаяwritable(каталог_страниц uint32, address uint32, размер uint32) bool {
	if каталог_страниц == 0 {
		return false
	}
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	оК := makeДиапазонЧастнаяwritableТекущаядата(каталог_страниц, address, размер)
	указатьcr3(oldcr3)
	return оК
}

func Указатьunsignedinteger32Исходящийстраницакаталог(x uint32, address uint32, каталог_страниц uint32) {
	if каталог_страниц == 0 {
		return
	}
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	Указатьunsignedinteger32ataddress(x, address)
	указатьcr3(oldcr3)
}

func GetЗначение(address uint32) uint32 {
	var orgЗначение uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgЗначение
}
func GetЗначениеИсходящийстраницакаталог(address uint32, каталог_страниц uint32) uint32 {
	if каталог_страниц == 0 {
		return 0
	}
	oldcr3 := getcr3()
	указатьcr3(каталог_страниц)
	v := GetЗначение(address)
	указатьcr3(oldcr3)
	return v
}

var v uint32 = 0

func КопироватьстраницакадрБлок(xстраницакаталог uint32, yстраницакаталог uint32, vaddress uint32) {
	if xстраницакаталог == 0 || yстраницакаталог == 0 {
		return
	}
	oldcr3 := getcr3()
	указатьcr3(xстраницакаталог)
	v = GetЗначение(vaddress)
	Указатьunsignedinteger32Исходящийстраницакаталог(v, vaddress, yстраницакаталог)

	указатьcr3(oldcr3)
}
