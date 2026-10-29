/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "утилита"
import . "gdt"
import . "консоль"
import . "прерывание"
import . "многоуправлениеЗадачами"
import . "управлениеЗадачами/tss"

import . "виртуальныйпамять"
import . "управлениеСтраницами"
import . "управлениеЗадачами/поток"
import . "управлениеЗадачами/планировщик"
import . "управлениеЗадачами/процесс"
import . "драйвер/драйвер"

import . "драйвер/клавиатура"
import . "драйвер/устройство_указания"

import . "драйвер/ata"
import . "файлсистема/msdosразделДиска"
import . "файлсистема/fat"

import . "файлсистема/исполняемый_и_компонуемый_формат"

import . "системавызов"

import . "памятьдиспетчер"
import . "pci"

func halt()

var iклавиатурасобытиеhandler IКлавиатурасобытиеhandler

type TMyклавиатурасобытиеhandler struct {
}

var myклавиатурасобытиеhandler TMyклавиатурасобытиеhandler
var клавиатурадрайвер TКлавиатурадрайвер
var мышьдрайвер TМышьдрайвер
var pciконтроллер TPeripheralcomponentinterconnectконтроллер

var клавиатураконсоль TКонсоль = TКонсоль{}

func (текущий *TMyклавиатурасобытиеhandler) ПриКлючВниз(ключ byte) {
	foo := [1]byte{' '}
	foo[0] = ключ

	клавиатураконсоль.MПечатьБайтxy(foo[:], 1000, 1000)
}

func (текущий *TMyклавиатурасобытиеhandler) ПриКлючВверх(ключ byte)	{}

var iмышьсобытиеhandler IМышьсобытиеhandler

type TMyмышьсобытиеhandler struct {
}

var мышьконсоль TКонсоль = TКонсоль{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (текущий *TMyмышьсобытиеhandler) ПримышьВниз(кнопка int8) {
	buffer := []byte("x")
	мышьконсоль.MПечатьxy(buffer, uint16(previousx), uint16(previousy))
}
func (текущий *TMyмышьсобытиеhandler) ПримышьВверх(кнопка int8)	{}
func (текущий *TMyмышьсобытиеhandler) ПримышьПереместить(x int8, y int8) {

	xПозиция += int16(x)
	if xПозиция < 0 {
		xПозиция = 0
	}
	if xПозиция >= 80 {
		xПозиция = 79
	}

	yПозиция -= int16(y)

	if yПозиция < 0 {
		yПозиция = 0
	}
	if yПозиция >= 25 {
		yПозиция = 24
	}

	buffer := []byte(" ")
	мышьконсоль.MПечатьxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мышьконсоль.MПечатьxy(buffer, uint16(xПозиция), uint16(yПозиция))

	previousx = xПозиция
	previousy = yПозиция
}

var устройствоdescriptor TPeripheralcomponentinterconnectУстройствоdescriptor
var ipciконтроллерhandler Ipciконтроллерhandler

type TMypciконтроллерhandler struct {
}

var консоль TКонсоль = TКонсоль{}
var драйверКоличество uint16 = 0

func (текущий TMypciконтроллерhandler) Приgetдрайвер(устройство TPeripheralcomponentinterconnectУстройствоdescriptor) {
	if устройство.ПроизводительИДЕНТИФИКАТОР == 0x1022 && устройство.УстройствоИДЕНТИФИКАТОР == 0x2000 {
		консоль.MПечатьxy([]byte("["), 0, 12)
		консоль.MПечать(([]byte)("AMD am79c973"))
		консоль.MПечать([]byte(":"))
		консоль.MUnsignedinteger16Печать(устройство.ПроизводительИДЕНТИФИКАТОР)
		консоль.MПечать([]byte(":"))
		консоль.MUnsignedinteger16Печать(устройство.УстройствоИДЕНТИФИКАТОР)
		консоль.MПечать([]byte(":"))
		консоль.MUnsignedinteger16Печать(uint16(устройство.Портbase))
		консоль.MПечать([]byte(":"))
		консоль.MUnsignedinteger32Печать(устройство.Прерывание)

		консоль.MПечать([]byte("]\n"))
		устройствоdescriptor = устройство
		драйверКоличество++
	}
}
func (текущий TMypciконтроллерhandler) Getдрайвер() TPeripheralcomponentinterconnectУстройствоdescriptor {
	return устройствоdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Печатьstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	консоль.MПечать(str)
}

func GetфайлРазмер(имяфайла []byte) uint32 {
	var ata0s = TДополнительноТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	разделДиска := TmsdosразделДискаТаблица{}
	разделДиска.ЧитатьразделДиска(&ata0s)

	bios := TПараметры_файловой_системы32{}

	var размер uint32 = bios.Len(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла)
	ata0s.Flush()

	return размер
}

func Прочитать_файл(имяфайла []byte, данные []byte) {
	var ata0s = TДополнительноТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	разделДиска := TmsdosразделДискаТаблица{}
	разделДиска.ЧитатьразделДиска(&ata0s)

	bios := TПараметры_файловой_системы32{}
	bios.Читать(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла, данные)

	ata0s.Flush()
}
func Загрузитьelf() {

	var ata0s = TДополнительноТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	разделДиска := TmsdosразделДискаТаблица{}
	разделДиска.ЧитатьразделДиска(&ata0s)

	bios := TПараметры_файловой_системы32{}

	var имяфайла []byte = ([]byte)("TEST")
	var размер uint32 = bios.Len(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла)
	var данныеbuffer [100 * 1024]byte
	var данные []byte = данныеbuffer[:]
	bios.Читать(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла, данные)

	исполняемый_и_компонуемый_формат := Elf{}

	исполняемый_и_компонуемый_формат.Parse(данные[:размер], 0x4f00000)

}

var задачаконсоль TКонсоль = TКонсоль{}

func TФункция1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func задачаa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func задачаb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func задачаc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func задачаd()

func задачаd0() {
	esi := getesi()
	for {

		SysПечатьunsignedinteger32(esi)

	}
}

func задачаd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func вводсобытиезадача() {
	for {
		Процессожидающийклавиатурасобытия()
		Процессожидающиймышьсобытия()
		halt()
	}
}

func memorytest(y int) {
	памятьдиспетчер := &TПамятьдиспетчер{}
	allocated := uint32(uintptr(памятьдиспетчер.Выделить_память(1024)))
	консоль.MUnsignedinteger32Печатьxy(allocated, 10, uint16(y))
	if y == 11 {
		памятьдиспетчер.Свободно(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Приостановитьloop()
func Обновитьcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Указатьcr3(cr3 uint32)
func Getcr4() uint32
func ВключитьуправлениеСтраницами()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetФункцияИмя(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcИмя = runtime.FuncForPC(address).Name()
	var funcБайт []byte = []byte(funcИмя)

	задачаконсоль.MПечатьxy(funcБайт, 1, 5)
	задачаконсоль.MПечать(([]byte)(":"))
	задачаконсоль.MUnsignedinteger32Печать(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	задачаконсоль.MПечатьunsignedinteger32(cr0, 2, 1)
}

var tss *Tssзапись = &Tssзапись{}

func KKernelEntry(Страницакаталогзапись uintptr, stacktop uintptr, stackbottom uintptr) {

	MПоследовательныйЖурналinit()
	консоль.MПечать("\n=== RUS BOOT ===\n")

	консоль.MПечатьunsignedinteger32(uint32(Страницакаталогзапись), 0, 2)
	консоль.MПечатьunsignedinteger32(uint32(Страницакаталогзапись), 10, 2)
	консоль.MПечатьunsignedinteger32(uint32(stacktop), 0, 3)
	консоль.MПечатьunsignedinteger32(uint32(stackbottom), 10, 3)

	памятьдиспетчер := &TПамятьдиспетчер{}
	памятьдиспетчер.Init(0, МаксимумочередьРазмер)

	управлениеСтраницами := &УправлениеСтраницами{}
	управлениеСтраницами.Init(Страницакаталогзапись, 0x500000, памятьдиспетчер)
	управлениеСтраницами.Sharedпамятьregion()

	Указатьcr3(uint32(Страницакаталогзапись))
	ВключитьуправлениеСтраницами()

	shareddescriptorТаблица := &TShareddescriptorТаблица{}
	shareddescriptorТаблица.Init()

	консоль.MПечать("esp:")

	esp := getesp()
	консоль.MUnsignedinteger32Печать(uint32(esp))

	tls := gettls()
	консоль.MПечать(([]byte)("tls:"))
	консоль.MUnsignedinteger32Печать(tls)

	tss.Установить(shareddescriptorТаблица, 7, Segядроданные, esp)

	VirtПроверить()

	cr3 := Обновитьcr3()
	консоль.MПечать(([]byte)(":cr3:"))
	консоль.MUnsignedinteger32Печать(cr3)

	cr0 := Getcr0()
	консоль.MПечать(([]byte)(":cr0:"))
	консоль.MUnsignedinteger32Печать(cr0)

	cr4 := Getcr4()
	консоль.MПечать(([]byte)(":cr4:"))
	консоль.MUnsignedinteger32Печать(cr4)

	задачадиспетчер_2 := &TЗадачадиспетчер{}
	задачадиспетчер_2.Init()

	Прерываниедиспетчер := &TПрерываниедиспетчер{}
	Прерываниедиспетчер.Init(0x20, shareddescriptorТаблица, задачадиспетчер_2)

	управлениеСтраницами.Страницаошибка(Прерываниедиспетчер)

	Драйвердиспетчер := TДрайвердиспетчер{}
	Драйвердиспетчер.Init()

	потокhelper := &TПотокhelper{}
	потокhelper.Init(памятьдиспетчер)

	процессhelper := Процессhelper{}
	процессhelper.Init(памятьдиспетчер, Страницакаталогзапись)

	sche := &Планировщик{}
	sche.Init(Прерываниедиспетчер, памятьдиспетчер, tss)

	sysвызов := &TSyscall{}
	sysвызов.Init(Прерываниедиспетчер)

	процессhelper.Spawn(задачаa, потокhelper, sche, uint32(Страницакаталогзапись), true)
	процессhelper.Spawn(задачаb, потокhelper, sche, uint32(Страницакаталогзапись), true)
	процессhelper.Spawn(задачаc, потокhelper, sche, uint32(Страницакаталогзапись), true)
	процессhelper.Spawn(задачаd1, потокhelper, sche, uint32(Страницакаталогзапись), true)
	процессhelper.Spawn(вводсобытиезадача, потокhelper, sche, uint32(Страницакаталогзапись), true)

	var размер uint32

	var linkerфайл []byte = ([]byte)("LINKER")
	размер = GetфайлРазмер(linkerфайл)
	linkeraddress := памятьдиспетчер.Выделить_память(размер)
	linkerданные := GetБайтfromУказатели(uintptr(linkeraddress), int(размер), int(размер))
	Прочитать_файл(linkerфайл, linkerданные)

	elf0 := Elf{}
	linkerзапись := elf0.Getзапись(linkerданные)
	elf0.Parse(linkerданные[:], uint32(Страницакаталогзапись))

	ссылкакарта := Ссылкакарта{}
	ссылкакарта.Init(памятьдиспетчер)

	var lib1файл []byte = ([]byte)("LIB1")
	размер = GetфайлРазмер(lib1файл)

	lib1address := памятьдиспетчер.Выделить_память(размер)
	lib1данные := GetБайтfromУказатели(uintptr(lib1address), int(размер), int(размер))
	Прочитать_файл(lib1файл, lib1данные)

	lib1elf := Elf{}
	lib1elf.Parse(lib1данные[:], uint32(Страницакаталогзапись))
	памятьдиспетчер.Свободно(lib1address)

	ссылкакарта.Добавить_в_конец_списка(uintptr(lib1elf.Динамически))

	var lib2файл []byte = ([]byte)("LIB2")
	размер = GetфайлРазмер(lib2файл)

	lib2address := памятьдиспетчер.Выделить_память(размер)
	lib2данные := GetБайтfromУказатели(uintptr(lib2address), int(размер), int(размер))
	Прочитать_файл(lib2файл, lib2данные)

	lib2elf := Elf{}
	lib2elf.Parse(lib2данные[:], uint32(Страницакаталогзапись))
	памятьдиспетчер.Свободно(lib2address)

	ссылкакарта.Добавить_в_конец_списка(uintptr(lib2elf.Динамически))

	libссылкакарта := ссылкакарта.Clone()
	ссылкакартаaddress := uint32(uintptr(Pointer(libссылкакарта.First)))

	lib1got := Getunsignedinteger32массивfromУказатели(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = ссылкакартаaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32массивfromУказатели(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = ссылкакартаaddress
	lib2got[2] = 0x4000000

	консоль.MПечатьxy("lib1: ", 1, 8)
	консоль.MUnsignedinteger32Печать(lib1elf.Got)
	консоль.MПечать(":")
	консоль.MUnsignedinteger32Печать(lib1elf.Динамически)

	консоль.MПечатьxy("lib2: ", 1, 9)
	консоль.MUnsignedinteger32Печать(lib2elf.Got)
	консоль.MПечать(":")
	консоль.MUnsignedinteger32Печать(lib2elf.Динамически)

	var пользователь1файл []byte = ([]byte)("USER1")
	размер = GetфайлРазмер(пользователь1файл)
	пользователь1address := памятьдиспетчер.Выделить_память(размер)
	пользователь1данные := GetБайтfromУказатели(uintptr(пользователь1address), int(размер), int(размер))
	Прочитать_файл(пользователь1файл, пользователь1данные)

	elf2 := Elf{}

	пользователь1запись := elf2.Getзапись(пользователь1данные)
	elf2.Parse(пользователь1данные[:], uint32(Страницакаталогзапись+0x1000))
	глобальныеoffsetТаблица := elf2.Got

	PЗначение1ссылкакарта := ссылкакарта.Clone()
	PЗначение1ссылкакарта.Добавить_в_конец_списка(uintptr(elf2.Динамически))

	памятьдиспетчер.Свободно(пользователь1address)

	var code1Указатели *uintptr
	var func1val func()

	code1Указатели = (*uintptr)(памятьдиспетчер.Выделить_память(4))
	*code1Указатели = uintptr(linkerзапись)
	func1val = *(*func())(Pointer(&code1Указатели))

	proc2 := процессhelper.Spawn(func1val, потокhelper, sche, uint32(Страницакаталогзапись+0x1000), false)
	thr2 := (*TПоток)(proc2.Threads.Getat(0))
	thr2.ЦПСостояние.Ecx = пользователь1запись
	thr2.ЦПСостояние.Edx = глобальныеoffsetТаблица
	thr2.ЦПСостояние.Esi = uint32(uintptr(Pointer(PЗначение1ссылкакарта.First)))

	консоль.MПечатьxy("user1: ", 1, 10)
	консоль.MUnsignedinteger32Печать(elf2.Got)

	var пользователь2файл []byte = ([]byte)("USER2")
	размер = GetфайлРазмер(пользователь2файл)
	пользователь2address := памятьдиспетчер.Выделить_память(размер)
	пользователь2данные := GetБайтfromУказатели(uintptr(пользователь2address), int(размер), int(размер))
	Прочитать_файл(пользователь2файл, пользователь2данные)

	elf3 := Elf{}

	пользователь2запись := elf3.Getзапись(пользователь2данные)
	elf3.Parse(пользователь2данные[:], uint32(Страницакаталогзапись+0x2000))
	глобальныеoffsetТаблица = elf3.Got

	PЗначение2ссылкакарта := ссылкакарта.Clone()
	PЗначение2ссылкакарта.Добавить_в_конец_списка(uintptr(elf3.Динамически))

	памятьдиспетчер.Свободно(пользователь2address)

	var code2Указатели *uintptr
	var func2val func()

	code2Указатели = (*uintptr)(памятьдиспетчер.Выделить_память(4))
	*code2Указатели = uintptr(linkerзапись)
	func2val = *(*func())(Pointer(&code2Указатели))

	proc3 := процессhelper.Spawn(func2val, потокhelper, sche, uint32(Страницакаталогзапись+0x2000), false)
	thr3 := (*TПоток)(proc3.Threads.Getat(0))
	thr3.ЦПСостояние.Ecx = пользователь2запись
	thr3.ЦПСостояние.Edx = глобальныеoffsetТаблица
	thr3.ЦПСостояние.Esi = uint32(uintptr(Pointer(PЗначение2ссылкакарта.First)))

	консоль.MПечатьxy("user2: ", 1, 11)
	консоль.MUnsignedinteger32Печать(thr3.ЦПСостояние.Esi)

	libссылкакарта.Печать(1, 11)

	var пользователь3файл []byte = ([]byte)("USER3")
	размер = GetфайлРазмер(пользователь3файл)
	пользователь3address := памятьдиспетчер.Выделить_память(размер)
	пользователь3данные := GetБайтfromУказатели(uintptr(пользователь3address), int(размер), int(размер))
	Прочитать_файл(пользователь3файл, пользователь3данные)

	elf4 := Elf{}

	пользователь3запись := elf4.Getзапись(пользователь3данные)
	elf4.Parse(пользователь3данные[:], uint32(Страницакаталогзапись+0x3000))
	глобальныеoffsetТаблица = elf4.Got

	PЗначение3ссылкакарта := ссылкакарта.Clone()
	PЗначение3ссылкакарта.Добавить_в_конец_списка(uintptr(elf4.Динамически))

	памятьдиспетчер.Свободно(пользователь3address)

	var code3Указатели *uintptr
	var func3val func()

	code3Указатели = (*uintptr)(памятьдиспетчер.Выделить_память(4))
	*code3Указатели = uintptr(linkerзапись)
	func3val = *(*func())(Pointer(&code3Указатели))

	proc4 := процессhelper.Spawn(func3val, потокhelper, sche, uint32(Страницакаталогзапись+0x3000), false)
	thr4 := (*TПоток)(proc4.Threads.Getat(0))
	thr4.ЦПСостояние.Ecx = пользователь3запись
	thr4.ЦПСостояние.Edx = глобальныеoffsetТаблица
	thr4.ЦПСостояние.Esi = uint32(uintptr(Pointer(PЗначение3ссылкакарта.First)))

	процессhelper.Spawn(TФункция1, потокhelper, sche, uint32(Страницакаталогзапись+0x4000), true)

	iклавиатурасобытиеhandler = &myклавиатурасобытиеhandler
	клавиатурадрайвер.Initдрайвер(Прерываниедиспетчер, iклавиатурасобытиеhandler)

	мышьдрайвер.Initдрайвер(Прерываниедиспетчер, nil)

	mypciконтроллерhandler := TMypciконтроллерhandler{}
	pciконтроллер.Init(mypciконтроллерhandler)
	pciконтроллер.Выбратьдрайвер(&Драйвердиспетчер, Прерываниедиспетчер)
	устройствоdescriptor = mypciконтроллерhandler.Getдрайвер()

	sche.Включено(true)
	Прерываниедиспетчер.Активно()

	for {
		halt()
	}

}
