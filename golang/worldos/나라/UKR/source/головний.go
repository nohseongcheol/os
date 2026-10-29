/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "консоль"
import . "переривання"
import . "multitasking"
import . "tasking/tss"

import . "віртуальнийПамять"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/процеси"
import . "driver/driver"

import . "driver/клавіатура"
import . "driver/вказівний_пристрій"

import . "driver/ата"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"

import . "файлСистема/виконуваний_і_компонований_формат"

import . "системаcall"

import . "памятьmanager"
import . "pci"

func halt()

var iКлавіатураПодіяhandler IКлавіатураПодіяhandler

type TMyКлавіатураПодіяhandler struct {
}

var myКлавіатураПодіяhandler TMyКлавіатураПодіяhandler
var клавіатураdriver TКлавіатураdriver
var мишаdriver TМишаdriver
var pciКонтролер TPeripheralcomponentinterconnectКонтролер

var клавіатураКонсоль TКонсоль = TКонсоль{}

func (поточний *TMyКлавіатураПодіяhandler) УвімкненоКлючВниз(ключ byte) {
	тест := [1]byte{' '}
	тест[0] = ключ

	клавіатураКонсоль.MДрукБайтxy(тест[:], 1000, 1000)
}

func (поточний *TMyКлавіатураПодіяhandler) УвімкненоКлючВгору(ключ byte)	{}

var iМишаПодіяhandler IМишаПодіяhandler

type TMyМишаПодіяhandler struct {
}

var мишаКонсоль TКонсоль = TКонсоль{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиція int16 = 0
var yПозиція int16 = 0

func (поточний *TMyМишаПодіяhandler) УвімкненоМишаВниз(кнопка int8) {
	buffer := []byte("x")
	мишаКонсоль.MДрукxy(buffer, uint16(previousx), uint16(previousy))
}
func (поточний *TMyМишаПодіяhandler) УвімкненоМишаВгору(кнопка int8)	{}
func (поточний *TMyМишаПодіяhandler) УвімкненоМишаПеремістити(x int8, y int8) {

	xПозиція += int16(x)
	if xПозиція < 0 {
		xПозиція = 0
	}
	if xПозиція >= 80 {
		xПозиція = 79
	}

	yПозиція -= int16(y)

	if yПозиція < 0 {
		yПозиція = 0
	}
	if yПозиція >= 25 {
		yПозиція = 24
	}

	buffer := []byte(" ")
	мишаКонсоль.MДрукxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мишаКонсоль.MДрукxy(buffer, uint16(xПозиція), uint16(yПозиція))

	previousx = xПозиція
	previousy = yПозиція
}

var пристрійdescriptor TPeripheralcomponentinterconnectПристрійdescriptor
var ipciКонтролерhandler IpciКонтролерhandler

type TMypciКонтролерhandler struct {
}

var консоль TКонсоль = TКонсоль{}
var driverВідлік uint16 = 0

func (поточний TMypciКонтролерhandler) Увімкненоgetdriver(пристрій TPeripheralcomponentinterconnectПристрійdescriptor) {
	if пристрій.ВиробникІДЕНТИФІКАТОР == 0x1022 && пристрій.ПристрійІДЕНТИФІКАТОР == 0x2000 {
		консоль.MДрукxy([]byte("["), 0, 12)
		консоль.MДрук(([]byte)("AMD am79c973"))
		консоль.MДрук([]byte(":"))
		консоль.MUnsignedinteger16Друк(пристрій.ВиробникІДЕНТИФІКАТОР)
		консоль.MДрук([]byte(":"))
		консоль.MUnsignedinteger16Друк(пристрій.ПристрійІДЕНТИФІКАТОР)
		консоль.MДрук([]byte(":"))
		консоль.MUnsignedinteger16Друк(uint16(пристрій.Портbase))
		консоль.MДрук([]byte(":"))
		консоль.MUnsignedinteger32Друк(пристрій.Переривання)

		консоль.MДрук([]byte("]\n"))
		пристрійdescriptor = пристрій
		driverВідлік++
	}
}
func (поточний TMypciКонтролерhandler) Getdriver() TPeripheralcomponentinterconnectПристрійdescriptor {
	return пристрійdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Друкstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	консоль.MДрук(str)
}

func GetФайлРозмір(назвафайлу []byte) uint32 {
	var ата0s = TДодатковоТехнологіяattachment{}
	ата0s.Init(false, 0x1F0)
	ата0s.Identify()

	partition := TmsdospartitionТаблиця{}
	partition.Читанняpartition(&ата0s)

	bios := TПараметри_файлової_системи32{}

	var розмір uint32 = bios.Len(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу)
	ата0s.Flush()

	return розмір
}

func Прочитати_файл(назвафайлу []byte, data []byte) {
	var ата0s = TДодатковоТехнологіяattachment{}
	ата0s.Init(false, 0x1F0)
	ата0s.Identify()

	partition := TmsdospartitionТаблиця{}
	partition.Читанняpartition(&ата0s)

	bios := TПараметри_файлової_системи32{}
	bios.Читання(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу, data)

	ата0s.Flush()
}
func Завантаженняelf() {

	var ата0s = TДодатковоТехнологіяattachment{}
	ата0s.Init(false, 0x1F0)
	ата0s.Identify()

	partition := TmsdospartitionТаблиця{}
	partition.Читанняpartition(&ата0s)

	bios := TПараметри_файлової_системи32{}

	var назвафайлу []byte = ([]byte)("TEST")
	var розмір uint32 = bios.Len(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Читання(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу, data)

	виконуваний_і_компонований_формат := Elf{}

	виконуваний_і_компонований_формат.Parse(data[:розмір], 0x4f00000)

}

var задачаКонсоль TКонсоль = TКонсоль{}

func TФункція1() {
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

		SysДрукunsignedinteger32(esi)

	}
}

func задачаd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func введенняданихПодіяЗадача() {
	for {
		ПроцесиpendingКлавіатураПодії()
		ПроцесиpendingМишаПодії()
		halt()
	}
}

func memorytest(y int) {
	памятьmanager := &TПамятьmanager{}
	allocated := uint32(uintptr(памятьmanager.Виділити_памʼять(1024)))
	консоль.MUnsignedinteger32Друкxy(allocated, 10, uint16(y))
	if y == 11 {
		памятьmanager.Вільно(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Призупинитиloop()
func Перезавантажитиcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Множинаcr3(cr3 uint32)
func Getcr4() uint32
func Дозволитиpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetФункціяНазва(i interface{}) {
	var адреса = reflect.ValueOf(i).Pointer()
	var funcНазва = runtime.FuncForPC(адреса).Name()
	var funcБайт []byte = []byte(funcНазва)

	задачаКонсоль.MДрукxy(funcБайт, 1, 5)
	задачаКонсоль.MДрук(([]byte)(":"))
	задачаКонсоль.MUnsignedinteger32Друк(uint32(uintptr(адреса)))
}

func printreg() {
	cr0 := Getcr0()
	задачаКонсоль.MДрукunsignedinteger32(cr0, 2, 1)
}

var tss *Tssзапис = &Tssзапис{}

func KKernelEntry(СторінкаТеказапис uintptr, stacktop uintptr, stackbottom uintptr) {

	MПослідовнийЖурналinit()
	консоль.MДрук("\n=== UKR BOOT ===\n")

	консоль.MДрукunsignedinteger32(uint32(СторінкаТеказапис), 0, 2)
	консоль.MДрукunsignedinteger32(uint32(СторінкаТеказапис), 10, 2)
	консоль.MДрукunsignedinteger32(uint32(stacktop), 0, 3)
	консоль.MДрукunsignedinteger32(uint32(stackbottom), 10, 3)

	памятьmanager := &TПамятьmanager{}
	памятьmanager.Init(0, МаксимумqueueРозмір)

	paging := &Paging{}
	paging.Init(СторінкаТеказапис, 0x500000, памятьmanager)
	paging.SharedПамятьregion()

	Множинаcr3(uint32(СторінкаТеказапис))
	Дозволитиpaging()

	shareddescriptorТаблиця := &TShareddescriptorТаблиця{}
	shareddescriptorТаблиця.Init()

	консоль.MДрук("esp:")

	esp := getesp()
	консоль.MUnsignedinteger32Друк(uint32(esp))

	tls := gettls()
	консоль.MДрук(([]byte)("tls:"))
	консоль.MUnsignedinteger32Друк(tls)

	tss.Встановити(shareddescriptorТаблиця, 7, Segkerneldata, esp)

	VirtТест()

	cr3 := Перезавантажитиcr3()
	консоль.MДрук(([]byte)(":cr3:"))
	консоль.MUnsignedinteger32Друк(cr3)

	cr0 := Getcr0()
	консоль.MДрук(([]byte)(":cr0:"))
	консоль.MUnsignedinteger32Друк(cr0)

	cr4 := Getcr4()
	консоль.MДрук(([]byte)(":cr4:"))
	консоль.MUnsignedinteger32Друк(cr4)

	задачаmanager_2 := &TЗадачаmanager{}
	задачаmanager_2.Init()

	Перериванняmanager := &TПерериванняmanager{}
	Перериванняmanager.Init(0x20, shareddescriptorТаблиця, задачаmanager_2)

	paging.Сторінкаfault(Перериванняmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(памятьmanager)

	процесиhelper := Процесиhelper{}
	процесиhelper.Init(памятьmanager, СторінкаТеказапис)

	sche := &Scheduler{}
	sche.Init(Перериванняmanager, памятьmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Перериванняmanager)

	процесиhelper.Spawn(задачаa, threadhelper, sche, uint32(СторінкаТеказапис), true)
	процесиhelper.Spawn(задачаb, threadhelper, sche, uint32(СторінкаТеказапис), true)
	процесиhelper.Spawn(задачаc, threadhelper, sche, uint32(СторінкаТеказапис), true)
	процесиhelper.Spawn(задачаd1, threadhelper, sche, uint32(СторінкаТеказапис), true)
	процесиhelper.Spawn(введенняданихПодіяЗадача, threadhelper, sche, uint32(СторінкаТеказапис), true)

	var розмір uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	розмір = GetФайлРозмір(linkerФайл)
	linkerАдреса := памятьmanager.Виділити_памʼять(розмір)
	linkerdata := GetБайтзВказівник(uintptr(linkerАдреса), int(розмір), int(розмір))
	Прочитати_файл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerзапис := elf0.Getзапис(linkerdata)
	elf0.Parse(linkerdata[:], uint32(СторінкаТеказапис))

	посиланняmap := Посиланняmap{}
	посиланняmap.Init(памятьmanager)

	var ліб1Файл []byte = ([]byte)("LIB1")
	розмір = GetФайлРозмір(ліб1Файл)

	ліб1Адреса := памятьmanager.Виділити_памʼять(розмір)
	ліб1data := GetБайтзВказівник(uintptr(ліб1Адреса), int(розмір), int(розмір))
	Прочитати_файл(ліб1Файл, ліб1data)

	ліб1elf := Elf{}
	ліб1elf.Parse(ліб1data[:], uint32(СторінкаТеказапис))
	памятьmanager.Вільно(ліб1Адреса)

	посиланняmap.Додати_в_кінець_списку(uintptr(ліб1elf.Динамічно))

	var ліб2Файл []byte = ([]byte)("LIB2")
	розмір = GetФайлРозмір(ліб2Файл)

	ліб2Адреса := памятьmanager.Виділити_памʼять(розмір)
	ліб2data := GetБайтзВказівник(uintptr(ліб2Адреса), int(розмір), int(розмір))
	Прочитати_файл(ліб2Файл, ліб2data)

	ліб2elf := Elf{}
	ліб2elf.Parse(ліб2data[:], uint32(СторінкаТеказапис))
	памятьmanager.Вільно(ліб2Адреса)

	посиланняmap.Додати_в_кінець_списку(uintptr(ліб2elf.Динамічно))

	лібПосиланняmap := посиланняmap.Clone()
	посиланняmapАдреса := uint32(uintptr(Pointer(лібПосиланняmap.First)))

	ліб1got := Getunsignedinteger32МасивзВказівник(uintptr(ліб1elf.Got), 4, 4)
	ліб1got[1] = посиланняmapАдреса
	ліб1got[2] = 0x4000000

	ліб2got := Getunsignedinteger32МасивзВказівник(uintptr(ліб2elf.Got), 4, 4)
	ліб2got[1] = посиланняmapАдреса
	ліб2got[2] = 0x4000000

	консоль.MДрукxy("lib1: ", 1, 8)
	консоль.MUnsignedinteger32Друк(ліб1elf.Got)
	консоль.MДрук(":")
	консоль.MUnsignedinteger32Друк(ліб1elf.Динамічно)

	консоль.MДрукxy("lib2: ", 1, 9)
	консоль.MUnsignedinteger32Друк(ліб2elf.Got)
	консоль.MДрук(":")
	консоль.MUnsignedinteger32Друк(ліб2elf.Динамічно)

	var користувач1Файл []byte = ([]byte)("USER1")
	розмір = GetФайлРозмір(користувач1Файл)
	користувач1Адреса := памятьmanager.Виділити_памʼять(розмір)
	користувач1data := GetБайтзВказівник(uintptr(користувач1Адреса), int(розмір), int(розмір))
	Прочитати_файл(користувач1Файл, користувач1data)

	elf2 := Elf{}

	користувач1запис := elf2.Getзапис(користувач1data)
	elf2.Parse(користувач1data[:], uint32(СторінкаТеказапис+0x1000))
	глобальніoffsetТаблиця := elf2.Got

	PЗначення1Посиланняmap := посиланняmap.Clone()
	PЗначення1Посиланняmap.Додати_в_кінець_списку(uintptr(elf2.Динамічно))

	памятьmanager.Вільно(користувач1Адреса)

	var code1Вказівник *uintptr
	var func1val func()

	code1Вказівник = (*uintptr)(памятьmanager.Виділити_памʼять(4))
	*code1Вказівник = uintptr(linkerзапис)
	func1val = *(*func())(Pointer(&code1Вказівник))

	proc2 := процесиhelper.Spawn(func1val, threadhelper, sche, uint32(СторінкаТеказапис+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ПроцесорСтан.Ecx = користувач1запис
	thr2.ПроцесорСтан.Edx = глобальніoffsetТаблиця
	thr2.ПроцесорСтан.Esi = uint32(uintptr(Pointer(PЗначення1Посиланняmap.First)))

	консоль.MДрукxy("user1: ", 1, 10)
	консоль.MUnsignedinteger32Друк(elf2.Got)

	var користувач2Файл []byte = ([]byte)("USER2")
	розмір = GetФайлРозмір(користувач2Файл)
	користувач2Адреса := памятьmanager.Виділити_памʼять(розмір)
	користувач2data := GetБайтзВказівник(uintptr(користувач2Адреса), int(розмір), int(розмір))
	Прочитати_файл(користувач2Файл, користувач2data)

	elf3 := Elf{}

	користувач2запис := elf3.Getзапис(користувач2data)
	elf3.Parse(користувач2data[:], uint32(СторінкаТеказапис+0x2000))
	глобальніoffsetТаблиця = elf3.Got

	PЗначення2Посиланняmap := посиланняmap.Clone()
	PЗначення2Посиланняmap.Додати_в_кінець_списку(uintptr(elf3.Динамічно))

	памятьmanager.Вільно(користувач2Адреса)

	var code2Вказівник *uintptr
	var func2val func()

	code2Вказівник = (*uintptr)(памятьmanager.Виділити_памʼять(4))
	*code2Вказівник = uintptr(linkerзапис)
	func2val = *(*func())(Pointer(&code2Вказівник))

	proc3 := процесиhelper.Spawn(func2val, threadhelper, sche, uint32(СторінкаТеказапис+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ПроцесорСтан.Ecx = користувач2запис
	thr3.ПроцесорСтан.Edx = глобальніoffsetТаблиця
	thr3.ПроцесорСтан.Esi = uint32(uintptr(Pointer(PЗначення2Посиланняmap.First)))

	консоль.MДрукxy("user2: ", 1, 11)
	консоль.MUnsignedinteger32Друк(thr3.ПроцесорСтан.Esi)

	лібПосиланняmap.Друк(1, 11)

	var користувач3Файл []byte = ([]byte)("USER3")
	розмір = GetФайлРозмір(користувач3Файл)
	користувач3Адреса := памятьmanager.Виділити_памʼять(розмір)
	користувач3data := GetБайтзВказівник(uintptr(користувач3Адреса), int(розмір), int(розмір))
	Прочитати_файл(користувач3Файл, користувач3data)

	elf4 := Elf{}

	користувач3запис := elf4.Getзапис(користувач3data)
	elf4.Parse(користувач3data[:], uint32(СторінкаТеказапис+0x3000))
	глобальніoffsetТаблиця = elf4.Got

	PЗначення3Посиланняmap := посиланняmap.Clone()
	PЗначення3Посиланняmap.Додати_в_кінець_списку(uintptr(elf4.Динамічно))

	памятьmanager.Вільно(користувач3Адреса)

	var code3Вказівник *uintptr
	var func3val func()

	code3Вказівник = (*uintptr)(памятьmanager.Виділити_памʼять(4))
	*code3Вказівник = uintptr(linkerзапис)
	func3val = *(*func())(Pointer(&code3Вказівник))

	proc4 := процесиhelper.Spawn(func3val, threadhelper, sche, uint32(СторінкаТеказапис+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ПроцесорСтан.Ecx = користувач3запис
	thr4.ПроцесорСтан.Edx = глобальніoffsetТаблиця
	thr4.ПроцесорСтан.Esi = uint32(uintptr(Pointer(PЗначення3Посиланняmap.First)))

	процесиhelper.Spawn(TФункція1, threadhelper, sche, uint32(СторінкаТеказапис+0x4000), true)

	iКлавіатураПодіяhandler = &myКлавіатураПодіяhandler
	клавіатураdriver.Initdriver(Перериванняmanager, iКлавіатураПодіяhandler)

	мишаdriver.Initdriver(Перериванняmanager, nil)

	mypciКонтролерhandler := TMypciКонтролерhandler{}
	pciКонтролер.Init(mypciКонтролерhandler)
	pciКонтролер.Виділитиdriver(&Drivermanager, Перериванняmanager)
	пристрійdescriptor = mypciКонтролерhandler.Getdriver()

	sche.Включено(true)
	Перериванняmanager.Активний()

	for {
		halt()
	}

}
