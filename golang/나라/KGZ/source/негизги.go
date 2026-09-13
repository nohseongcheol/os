package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtualЭси"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/процесси"
import . "driver/driver"

import . "driver/клавиатура"
import . "driver/чычкан"

import . "driver/ata"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"

import . "файлСистема/elf"

import . "системаcall"

import . "эсиmanager"
import . "pci"

func halt()

var iКлавиатураeventhandler IКлавиатураeventhandler

type TMyКлавиатураeventhandler struct {
}

var myКлавиатураeventhandler TMyКлавиатураeventhandler
var клавиатураdriver TКлавиатураdriver
var чычканdriver TЧычканdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var клавиатураconsole TConsole = TConsole{}

func (self *TMyКлавиатураeventhandler) OnАчкычdown(ачкыч byte) {
	foo := [1]byte{' '}
	foo[0] = ачкыч

	клавиатураconsole.MБасмаБайтxy(foo[:], 1000, 1000)
}

func (self *TMyКлавиатураeventhandler) OnАчкычӨйдө(ачкыч byte)	{}

var iЧычканeventhandler IЧычканeventhandler

type TMyЧычканeventhandler struct {
}

var чычканconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xТурганжери int16 = 0
var yТурганжери int16 = 0

func (self *TMyЧычканeventhandler) OnЧычканdown(button int8) {
	buffer := []byte("x")
	чычканconsole.MБасмаxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyЧычканeventhandler) OnЧычканӨйдө(button int8)	{}
func (self *TMyЧычканeventhandler) OnЧычканТашуу(x int8, y int8) {

	xТурганжери += int16(x)
	if xТурганжери < 0 {
		xТурганжери = 0
	}
	if xТурганжери >= 80 {
		xТурганжери = 79
	}

	yТурганжери -= int16(y)

	if yТурганжери < 0 {
		yТурганжери = 0
	}
	if yТурганжери >= 25 {
		yТурганжери = 24
	}

	buffer := []byte(" ")
	чычканconsole.MБасмаxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	чычканconsole.MБасмаxy(buffer, uint16(xТурганжери), uint16(yТурганжери))

	previousx = xТурганжери
	previousy = yТурганжери
}

var түзүлүшүdescriptor TPeripheralcomponentinterconnectТүзүлүшүdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(түзүлүшү TPeripheralcomponentinterconnectТүзүлүшүdescriptor) {
	if түзүлүшү.ИштепчыгаруучуИДЕНТИФИКАТОР == 0x1022 && түзүлүшү.ТүзүлүшүИДЕНТИФИКАТОР == 0x2000 {
		console.MБасмаxy([]byte("["), 0, 12)
		console.MБасма(([]byte)("AMD am79c973"))
		console.MБасма([]byte(":"))
		console.MUnsignedinteger16Басма(түзүлүшү.ИштепчыгаруучуИДЕНТИФИКАТОР)
		console.MБасма([]byte(":"))
		console.MUnsignedinteger16Басма(түзүлүшү.ТүзүлүшүИДЕНТИФИКАТОР)
		console.MБасма([]byte(":"))
		console.MUnsignedinteger16Басма(uint16(түзүлүшү.Портbase))
		console.MБасма([]byte(":"))
		console.MUnsignedinteger32Басма(түзүлүшү.Interrupt)

		console.MБасма([]byte("]\n"))
		түзүлүшүdescriptor = түзүлүшү
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectТүзүлүшүdescriptor {
	return түзүлүшүdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Басмаstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MБасма(str)
}

func GetФайлӨлчөм(файлаты []byte) uint32 {
	var ata0s = TКеңейтилгенТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionЖадыбал{}
	partition.Окууpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var өлчөм uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлаты)
	ata0s.Flush()

	return өлчөм
}

func ОкууФайл(файлаты []byte, data []byte) {
	var ata0s = TКеңейтилгенТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionЖадыбал{}
	partition.Окууpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Окуу(&ata0s, partition.Mbr.Primarypartition[0], файлаты, data)

	ata0s.Flush()
}
func Жүктөөelf() {

	var ata0s = TКеңейтилгенТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionЖадыбал{}
	partition.Окууpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var файлаты []byte = ([]byte)("TEST")
	var өлчөм uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлаты)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Окуу(&ata0s, partition.Mbr.Primarypartition[0], файлаты, data)

	elf := Elf{}

	elf.Parse(data[:өлчөм], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TFunction1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func taska() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func taskb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func taskc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func taskd()

func taskd0() {
	esi := getesi()
	for {

		SysБасмаunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func киришeventtask() {
	for {
		ПроцессиpendingКлавиатураevents()
		ПроцессиpendingЧычканevents()
		halt()
	}
}

func memorytest(y int) {
	эсиmanager := &TЭсиmanager{}
	allocated := uint32(uintptr(эсиmanager.Malloc(1024)))
	console.MUnsignedinteger32Басмаxy(allocated, 10, uint16(y))
	if y == 11 {
		эсиmanager.Бош(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Кайтаданжүктөөcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Setcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetfunctionАты(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcАты = runtime.FuncForPC(address).Name()
	var funcБайт []byte = []byte(funcАты)

	taskconsole.MБасмаxy(funcБайт, 1, 5)
	taskconsole.MБасма(([]byte)(":"))
	taskconsole.MUnsignedinteger32Басма(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MБасмаunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(БАРАКкаталогentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MБасма("\n=== KGZ BOOT ===\n")

	console.MБасмаunsignedinteger32(uint32(БАРАКкаталогentry), 0, 2)
	console.MБасмаunsignedinteger32(uint32(БАРАКкаталогentry), 10, 2)
	console.MБасмаunsignedinteger32(uint32(stacktop), 0, 3)
	console.MБасмаunsignedinteger32(uint32(stackbottom), 10, 3)

	эсиmanager := &TЭсиmanager{}
	эсиmanager.Init(0, MaxqueueӨлчөм)

	paging := &Paging{}
	paging.Init(БАРАКкаталогentry, 0x500000, эсиmanager)
	paging.SharedЭсиregion()

	Setcr3(uint32(БАРАКкаталогentry))
	Enablepaging()

	shareddescriptorЖадыбал := &TShareddescriptorЖадыбал{}
	shareddescriptorЖадыбал.Init()

	console.MБасма("esp:")

	esp := getesp()
	console.MUnsignedinteger32Басма(uint32(esp))

	tls := gettls()
	console.MБасма(([]byte)("tls:"))
	console.MUnsignedinteger32Басма(tls)

	tss.Орнотуу(shareddescriptorЖадыбал, 7, Segkerneldata, esp)

	VirtТекшерүү()

	cr3 := Кайтаданжүктөөcr3()
	console.MБасма(([]byte)(":cr3:"))
	console.MUnsignedinteger32Басма(cr3)

	cr0 := Getcr0()
	console.MБасма(([]byte)(":cr0:"))
	console.MUnsignedinteger32Басма(cr0)

	cr4 := Getcr4()
	console.MБасма(([]byte)(":cr4:"))
	console.MUnsignedinteger32Басма(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorЖадыбал, taskmanager_2)

	paging.БАРАКfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(эсиmanager)

	процессиhelper := Процессиhelper{}
	процессиhelper.Init(эсиmanager, БАРАКкаталогentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, эсиmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	процессиhelper.Spawn(taska, threadhelper, sche, uint32(БАРАКкаталогentry), true)
	процессиhelper.Spawn(taskb, threadhelper, sche, uint32(БАРАКкаталогentry), true)
	процессиhelper.Spawn(taskc, threadhelper, sche, uint32(БАРАКкаталогentry), true)
	процессиhelper.Spawn(taskd1, threadhelper, sche, uint32(БАРАКкаталогentry), true)
	процессиhelper.Spawn(киришeventtask, threadhelper, sche, uint32(БАРАКкаталогentry), true)

	var өлчөм uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	өлчөм = GetФайлӨлчөм(linkerФайл)
	linkeraddress := эсиmanager.Malloc(өлчөм)
	linkerdata := GetБайтfromКөрсөткүч(uintptr(linkeraddress), int(өлчөм), int(өлчөм))
	ОкууФайл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(БАРАКкаталогentry))

	шилтемеmap := Шилтемеmap{}
	шилтемеmap.Init(эсиmanager)

	var lib1Файл []byte = ([]byte)("LIB1")
	өлчөм = GetФайлӨлчөм(lib1Файл)

	lib1address := эсиmanager.Malloc(өлчөм)
	lib1data := GetБайтfromКөрсөткүч(uintptr(lib1address), int(өлчөм), int(өлчөм))
	ОкууФайл(lib1Файл, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(БАРАКкаталогentry))
	эсиmanager.Бош(lib1address)

	шилтемеmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Файл []byte = ([]byte)("LIB2")
	өлчөм = GetФайлӨлчөм(lib2Файл)

	lib2address := эсиmanager.Malloc(өлчөм)
	lib2data := GetБайтfromКөрсөткүч(uintptr(lib2address), int(өлчөм), int(өлчөм))
	ОкууФайл(lib2Файл, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(БАРАКкаталогentry))
	эсиmanager.Бош(lib2address)

	шилтемеmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libшилтемеmap := шилтемеmap.Clone()
	шилтемеmapaddress := uint32(uintptr(Pointer(libшилтемеmap.First)))

	lib1got := Getunsignedinteger32МассивfromКөрсөткүч(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = шилтемеmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32МассивfromКөрсөткүч(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = шилтемеmapaddress
	lib2got[2] = 0x4000000

	console.MБасмаxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Басма(lib1elf.Got)
	console.MБасма(":")
	console.MUnsignedinteger32Басма(lib1elf.Dynamic)

	console.MБасмаxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Басма(lib2elf.Got)
	console.MБасма(":")
	console.MUnsignedinteger32Басма(lib2elf.Dynamic)

	var колдонуучу1Файл []byte = ([]byte)("USER1")
	өлчөм = GetФайлӨлчөм(колдонуучу1Файл)
	колдонуучу1address := эсиmanager.Malloc(өлчөм)
	колдонуучу1data := GetБайтfromКөрсөткүч(uintptr(колдонуучу1address), int(өлчөм), int(өлчөм))
	ОкууФайл(колдонуучу1Файл, колдонуучу1data)

	elf2 := Elf{}

	колдонуучу1entry := elf2.Getentry(колдонуучу1data)
	elf2.Parse(колдонуучу1data[:], uint32(БАРАКкаталогentry+0x1000))
	globaloffsetЖадыбал := elf2.Got

	PМааниси1шилтемеmap := шилтемеmap.Clone()
	PМааниси1шилтемеmap.Append_to_list(uintptr(elf2.Dynamic))

	эсиmanager.Бош(колдонуучу1address)

	var code1Көрсөткүч *uintptr
	var func1val func()

	code1Көрсөткүч = (*uintptr)(эсиmanager.Malloc(4))
	*code1Көрсөткүч = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Көрсөткүч))

	proc2 := процессиhelper.Spawn(func1val, threadhelper, sche, uint32(БАРАКкаталогentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.БПАбал.Ecx = колдонуучу1entry
	thr2.БПАбал.Edx = globaloffsetЖадыбал
	thr2.БПАбал.Esi = uint32(uintptr(Pointer(PМааниси1шилтемеmap.First)))

	console.MБасмаxy("user1: ", 1, 10)
	console.MUnsignedinteger32Басма(elf2.Got)

	var колдонуучу2Файл []byte = ([]byte)("USER2")
	өлчөм = GetФайлӨлчөм(колдонуучу2Файл)
	колдонуучу2address := эсиmanager.Malloc(өлчөм)
	колдонуучу2data := GetБайтfromКөрсөткүч(uintptr(колдонуучу2address), int(өлчөм), int(өлчөм))
	ОкууФайл(колдонуучу2Файл, колдонуучу2data)

	elf3 := Elf{}

	колдонуучу2entry := elf3.Getentry(колдонуучу2data)
	elf3.Parse(колдонуучу2data[:], uint32(БАРАКкаталогentry+0x2000))
	globaloffsetЖадыбал = elf3.Got

	PМааниси2шилтемеmap := шилтемеmap.Clone()
	PМааниси2шилтемеmap.Append_to_list(uintptr(elf3.Dynamic))

	эсиmanager.Бош(колдонуучу2address)

	var code2Көрсөткүч *uintptr
	var func2val func()

	code2Көрсөткүч = (*uintptr)(эсиmanager.Malloc(4))
	*code2Көрсөткүч = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Көрсөткүч))

	proc3 := процессиhelper.Spawn(func2val, threadhelper, sche, uint32(БАРАКкаталогentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.БПАбал.Ecx = колдонуучу2entry
	thr3.БПАбал.Edx = globaloffsetЖадыбал
	thr3.БПАбал.Esi = uint32(uintptr(Pointer(PМааниси2шилтемеmap.First)))

	console.MБасмаxy("user2: ", 1, 11)
	console.MUnsignedinteger32Басма(thr3.БПАбал.Esi)

	libшилтемеmap.Басма(1, 11)

	var колдонуучу3Файл []byte = ([]byte)("USER3")
	өлчөм = GetФайлӨлчөм(колдонуучу3Файл)
	колдонуучу3address := эсиmanager.Malloc(өлчөм)
	колдонуучу3data := GetБайтfromКөрсөткүч(uintptr(колдонуучу3address), int(өлчөм), int(өлчөм))
	ОкууФайл(колдонуучу3Файл, колдонуучу3data)

	elf4 := Elf{}

	колдонуучу3entry := elf4.Getentry(колдонуучу3data)
	elf4.Parse(колдонуучу3data[:], uint32(БАРАКкаталогentry+0x3000))
	globaloffsetЖадыбал = elf4.Got

	PМааниси3шилтемеmap := шилтемеmap.Clone()
	PМааниси3шилтемеmap.Append_to_list(uintptr(elf4.Dynamic))

	эсиmanager.Бош(колдонуучу3address)

	var code3Көрсөткүч *uintptr
	var func3val func()

	code3Көрсөткүч = (*uintptr)(эсиmanager.Malloc(4))
	*code3Көрсөткүч = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Көрсөткүч))

	proc4 := процессиhelper.Spawn(func3val, threadhelper, sche, uint32(БАРАКкаталогentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.БПАбал.Ecx = колдонуучу3entry
	thr4.БПАбал.Edx = globaloffsetЖадыбал
	thr4.БПАбал.Esi = uint32(uintptr(Pointer(PМааниси3шилтемеmap.First)))

	процессиhelper.Spawn(TFunction1, threadhelper, sche, uint32(БАРАКкаталогentry+0x4000), true)

	iКлавиатураeventhandler = &myКлавиатураeventhandler
	клавиатураdriver.Initdriver(Interruptmanager, iКлавиатураeventhandler)

	чычканdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	түзүлүшүdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Күйүк(true)
	Interruptmanager.Активдүү()

	for {
		halt()
	}

}
