/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "прекъсване"
import . "multitasking"
import . "tasking/tss"

import . "virtualПамет"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/процес"
import . "driver/driver"

import . "driver/клавиатура"
import . "driver/мишка"

import . "driver/ata"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"

import . "файлСистема/elf"

import . "системаcall"

import . "паметmanager"
import . "pci"

func halt()

var iКлавиатураСъбитиеhandler IКлавиатураСъбитиеhandler

type TMyКлавиатураСъбитиеhandler struct {
}

var myКлавиатураСъбитиеhandler TMyКлавиатураСъбитиеhandler
var клавиатураdriver TКлавиатураdriver
var мишкаdriver TМишкаdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var клавиатураconsole TConsole = TConsole{}

func (себеси *TMyКлавиатураСъбитиеhandler) ВклКлючНадолу(ключ byte) {
	foo := [1]byte{' '}
	foo[0] = ключ

	клавиатураconsole.MПечатБайтовеxy(foo[:], 1000, 1000)
}

func (себеси *TMyКлавиатураСъбитиеhandler) ВклКлючНагоре(ключ byte)	{}

var iМишкаСъбитиеhandler IМишкаСъбитиеhandler

type TMyМишкаСъбитиеhandler struct {
}

var мишкаconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиция int16 = 0
var yПозиция int16 = 0

func (себеси *TMyМишкаСъбитиеhandler) ВклМишкаНадолу(бутон int8) {
	buffer := []byte("x")
	мишкаconsole.MПечатxy(buffer, uint16(previousx), uint16(previousy))
}
func (себеси *TMyМишкаСъбитиеhandler) ВклМишкаНагоре(бутон int8)	{}
func (себеси *TMyМишкаСъбитиеhandler) ВклМишкаПреместване(x int8, y int8) {

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
	мишкаconsole.MПечатxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мишкаconsole.MПечатxy(buffer, uint16(xПозиция), uint16(yПозиция))

	previousx = xПозиция
	previousy = yПозиция
}

var устройствоdescriptor TPeripheralcomponentinterconnectУстройствоdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (себеси TMypcicontrollerhandler) Вклgetdriver(устройство TPeripheralcomponentinterconnectУстройствоdescriptor) {
	if устройство.ПроизводителИДЕНТИФИКАТОР == 0x1022 && устройство.УстройствоИДЕНТИФИКАТОР == 0x2000 {
		console.MПечатxy([]byte("["), 0, 12)
		console.MПечат(([]byte)("AMD am79c973"))
		console.MПечат([]byte(":"))
		console.MUnsignedinteger16Печат(устройство.ПроизводителИДЕНТИФИКАТОР)
		console.MПечат([]byte(":"))
		console.MUnsignedinteger16Печат(устройство.УстройствоИДЕНТИФИКАТОР)
		console.MПечат([]byte(":"))
		console.MUnsignedinteger16Печат(uint16(устройство.Портbase))
		console.MПечат([]byte(":"))
		console.MUnsignedinteger32Печат(устройство.Прекъсване)

		console.MПечат([]byte("]\n"))
		устройствоdescriptor = устройство
		drivercount++
	}
}
func (себеси TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectУстройствоdescriptor {
	return устройствоdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Печатstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MПечат(str)
}

func GetФайлРазмер(именафайл []byte) uint32 {
	var ata0s = TДопълнителниТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТаблица{}
	partition.Четенеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var размер uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именафайл)
	ata0s.Flush()

	return размер
}

func ЧетенеФайл(именафайл []byte, data []byte) {
	var ata0s = TДопълнителниТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТаблица{}
	partition.Четенеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Четене(&ata0s, partition.Mbr.Primarypartition[0], именафайл, data)

	ata0s.Flush()
}
func Натовареностelf() {

	var ata0s = TДопълнителниТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТаблица{}
	partition.Четенеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var именафайл []byte = ([]byte)("TEST")
	var размер uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именафайл)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Четене(&ata0s, partition.Mbr.Primarypartition[0], именафайл, data)

	elf := Elf{}

	elf.Parse(data[:размер], 0x4f00000)

}

var задачаconsole TConsole = TConsole{}

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

		SysПечатunsignedinteger32(esi)

	}
}

func задачаd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func входСъбитиеЗадача() {
	for {
		ПроцесpendingКлавиатураevents()
		ПроцесpendingМишкаevents()
		halt()
	}
}

func memorytest(y int) {
	паметmanager := &TПаметmanager{}
	allocated := uint32(uintptr(паметmanager.Malloc(1024)))
	console.MUnsignedinteger32Печатxy(allocated, 10, uint16(y))
	if y == 11 {
		паметmanager.Свободно(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Паузаloop()
func Презарежданеcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Задайcr3(cr3 uint32)
func Getcr4() uint32
func Включванеpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetфункцияИме(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcИме = runtime.FuncForPC(address).Name()
	var funcБайтове []byte = []byte(funcИме)

	задачаconsole.MПечатxy(funcБайтове, 1, 5)
	задачаconsole.MПечат(([]byte)(":"))
	задачаconsole.MUnsignedinteger32Печат(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	задачаconsole.MПечатunsignedinteger32(cr0, 2, 1)
}

var tss *Tssзапис = &Tssзапис{}

func KKernelEntry(Страницапапказапис uintptr, stacktop uintptr, stackbottom uintptr) {

	MСериенномерЛогinit()
	console.MПечат("\n=== BGR BOOT ===\n")

	console.MПечатunsignedinteger32(uint32(Страницапапказапис), 0, 2)
	console.MПечатunsignedinteger32(uint32(Страницапапказапис), 10, 2)
	console.MПечатunsignedinteger32(uint32(stacktop), 0, 3)
	console.MПечатunsignedinteger32(uint32(stackbottom), 10, 3)

	паметmanager := &TПаметmanager{}
	паметmanager.Init(0, МаксqueueРазмер)

	paging := &Paging{}
	paging.Init(Страницапапказапис, 0x500000, паметmanager)
	paging.SharedПаметregion()

	Задайcr3(uint32(Страницапапказапис))
	Включванеpaging()

	shareddescriptorТаблица := &TShareddescriptorТаблица{}
	shareddescriptorТаблица.Init()

	console.MПечат("esp:")

	esp := getesp()
	console.MUnsignedinteger32Печат(uint32(esp))

	tls := gettls()
	console.MПечат(([]byte)("tls:"))
	console.MUnsignedinteger32Печат(tls)

	tss.Инсталиране(shareddescriptorТаблица, 7, Segkerneldata, esp)

	VirtТест()

	cr3 := Презарежданеcr3()
	console.MПечат(([]byte)(":cr3:"))
	console.MUnsignedinteger32Печат(cr3)

	cr0 := Getcr0()
	console.MПечат(([]byte)(":cr0:"))
	console.MUnsignedinteger32Печат(cr0)

	cr4 := Getcr4()
	console.MПечат(([]byte)(":cr4:"))
	console.MUnsignedinteger32Печат(cr4)

	задачаmanager_2 := &TЗадачаmanager{}
	задачаmanager_2.Init()

	Прекъсванеmanager := &TПрекъсванеmanager{}
	Прекъсванеmanager.Init(0x20, shareddescriptorТаблица, задачаmanager_2)

	paging.Страницаfault(Прекъсванеmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(паметmanager)

	процесhelper := Процесhelper{}
	процесhelper.Init(паметmanager, Страницапапказапис)

	sche := &Scheduler{}
	sche.Init(Прекъсванеmanager, паметmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Прекъсванеmanager)

	процесhelper.Spawn(задачаa, threadhelper, sche, uint32(Страницапапказапис), true)
	процесhelper.Spawn(задачаb, threadhelper, sche, uint32(Страницапапказапис), true)
	процесhelper.Spawn(задачаc, threadhelper, sche, uint32(Страницапапказапис), true)
	процесhelper.Spawn(задачаd1, threadhelper, sche, uint32(Страницапапказапис), true)
	процесhelper.Spawn(входСъбитиеЗадача, threadhelper, sche, uint32(Страницапапказапис), true)

	var размер uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	размер = GetФайлРазмер(linkerФайл)
	linkeraddress := паметmanager.Malloc(размер)
	linkerdata := GetБайтовеfromПоказалци(uintptr(linkeraddress), int(размер), int(размер))
	ЧетенеФайл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerзапис := elf0.Getзапис(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Страницапапказапис))

	връзкаmap := Връзкаmap{}
	връзкаmap.Init(паметmanager)

	var lib1Файл []byte = ([]byte)("LIB1")
	размер = GetФайлРазмер(lib1Файл)

	lib1address := паметmanager.Malloc(размер)
	lib1data := GetБайтовеfromПоказалци(uintptr(lib1address), int(размер), int(размер))
	ЧетенеФайл(lib1Файл, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Страницапапказапис))
	паметmanager.Свободно(lib1address)

	връзкаmap.Append_to_list(uintptr(lib1elf.Динамично))

	var lib2Файл []byte = ([]byte)("LIB2")
	размер = GetФайлРазмер(lib2Файл)

	lib2address := паметmanager.Malloc(размер)
	lib2data := GetБайтовеfromПоказалци(uintptr(lib2address), int(размер), int(размер))
	ЧетенеФайл(lib2Файл, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Страницапапказапис))
	паметmanager.Свободно(lib2address)

	връзкаmap.Append_to_list(uintptr(lib2elf.Динамично))

	libВръзкаmap := връзкаmap.Clone()
	връзкаmapaddress := uint32(uintptr(Pointer(libВръзкаmap.First)))

	lib1got := Getunsignedinteger32МасивfromПоказалци(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = връзкаmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32МасивfromПоказалци(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = връзкаmapaddress
	lib2got[2] = 0x4000000

	console.MПечатxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Печат(lib1elf.Got)
	console.MПечат(":")
	console.MUnsignedinteger32Печат(lib1elf.Динамично)

	console.MПечатxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Печат(lib2elf.Got)
	console.MПечат(":")
	console.MUnsignedinteger32Печат(lib2elf.Динамично)

	var собственик1Файл []byte = ([]byte)("USER1")
	размер = GetФайлРазмер(собственик1Файл)
	собственик1address := паметmanager.Malloc(размер)
	собственик1data := GetБайтовеfromПоказалци(uintptr(собственик1address), int(размер), int(размер))
	ЧетенеФайл(собственик1Файл, собственик1data)

	elf2 := Elf{}

	собственик1запис := elf2.Getзапис(собственик1data)
	elf2.Parse(собственик1data[:], uint32(Страницапапказапис+0x1000))
	глобалноoffsetТаблица := elf2.Got

	PСтойност1Връзкаmap := връзкаmap.Clone()
	PСтойност1Връзкаmap.Append_to_list(uintptr(elf2.Динамично))

	паметmanager.Свободно(собственик1address)

	var code1Показалци *uintptr
	var func1val func()

	code1Показалци = (*uintptr)(паметmanager.Malloc(4))
	*code1Показалци = uintptr(linkerзапис)
	func1val = *(*func())(Pointer(&code1Показалци))

	proc2 := процесhelper.Spawn(func1val, threadhelper, sche, uint32(Страницапапказапис+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ПроцесорСъстояние.Ecx = собственик1запис
	thr2.ПроцесорСъстояние.Edx = глобалноoffsetТаблица
	thr2.ПроцесорСъстояние.Esi = uint32(uintptr(Pointer(PСтойност1Връзкаmap.First)))

	console.MПечатxy("user1: ", 1, 10)
	console.MUnsignedinteger32Печат(elf2.Got)

	var собственик2Файл []byte = ([]byte)("USER2")
	размер = GetФайлРазмер(собственик2Файл)
	собственик2address := паметmanager.Malloc(размер)
	собственик2data := GetБайтовеfromПоказалци(uintptr(собственик2address), int(размер), int(размер))
	ЧетенеФайл(собственик2Файл, собственик2data)

	elf3 := Elf{}

	собственик2запис := elf3.Getзапис(собственик2data)
	elf3.Parse(собственик2data[:], uint32(Страницапапказапис+0x2000))
	глобалноoffsetТаблица = elf3.Got

	PСтойност2Връзкаmap := връзкаmap.Clone()
	PСтойност2Връзкаmap.Append_to_list(uintptr(elf3.Динамично))

	паметmanager.Свободно(собственик2address)

	var code2Показалци *uintptr
	var func2val func()

	code2Показалци = (*uintptr)(паметmanager.Malloc(4))
	*code2Показалци = uintptr(linkerзапис)
	func2val = *(*func())(Pointer(&code2Показалци))

	proc3 := процесhelper.Spawn(func2val, threadhelper, sche, uint32(Страницапапказапис+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ПроцесорСъстояние.Ecx = собственик2запис
	thr3.ПроцесорСъстояние.Edx = глобалноoffsetТаблица
	thr3.ПроцесорСъстояние.Esi = uint32(uintptr(Pointer(PСтойност2Връзкаmap.First)))

	console.MПечатxy("user2: ", 1, 11)
	console.MUnsignedinteger32Печат(thr3.ПроцесорСъстояние.Esi)

	libВръзкаmap.Печат(1, 11)

	var собственик3Файл []byte = ([]byte)("USER3")
	размер = GetФайлРазмер(собственик3Файл)
	собственик3address := паметmanager.Malloc(размер)
	собственик3data := GetБайтовеfromПоказалци(uintptr(собственик3address), int(размер), int(размер))
	ЧетенеФайл(собственик3Файл, собственик3data)

	elf4 := Elf{}

	собственик3запис := elf4.Getзапис(собственик3data)
	elf4.Parse(собственик3data[:], uint32(Страницапапказапис+0x3000))
	глобалноoffsetТаблица = elf4.Got

	PСтойност3Връзкаmap := връзкаmap.Clone()
	PСтойност3Връзкаmap.Append_to_list(uintptr(elf4.Динамично))

	паметmanager.Свободно(собственик3address)

	var code3Показалци *uintptr
	var func3val func()

	code3Показалци = (*uintptr)(паметmanager.Malloc(4))
	*code3Показалци = uintptr(linkerзапис)
	func3val = *(*func())(Pointer(&code3Показалци))

	proc4 := процесhelper.Spawn(func3val, threadhelper, sche, uint32(Страницапапказапис+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ПроцесорСъстояние.Ecx = собственик3запис
	thr4.ПроцесорСъстояние.Edx = глобалноoffsetТаблица
	thr4.ПроцесорСъстояние.Esi = uint32(uintptr(Pointer(PСтойност3Връзкаmap.First)))

	процесhelper.Spawn(TФункция1, threadhelper, sche, uint32(Страницапапказапис+0x4000), true)

	iКлавиатураСъбитиеhandler = &myКлавиатураСъбитиеhandler
	клавиатураdriver.Initdriver(Прекъсванеmanager, iКлавиатураСъбитиеhandler)

	мишкаdriver.Initdriver(Прекъсванеmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Избиранеdriver(&Drivermanager, Прекъсванеmanager)
	устройствоdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Включена(true)
	Прекъсванеmanager.Активна()

	for {
		halt()
	}

}
