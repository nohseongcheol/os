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

import . "виртуелноМеморија"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/процес"
import . "driver/driver"

import . "driver/тастатура"
import . "driver/глушец"

import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "датотекаСистем/fat"

import . "датотекаСистем/elf"

import . "системcall"

import . "меморијаmanager"
import . "pci"

func halt()

var iТастатураeventhandler IТастатураeventhandler

type TMyТастатураeventhandler struct {
}

var myТастатураeventhandler TMyТастатураeventhandler
var тастатураdriver TТастатураdriver
var глушецdriver TГлушецdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var тастатураconsole TConsole = TConsole{}

func (само *TMyТастатураeventhandler) ВклученоkeyДолу(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	тастатураconsole.MПечатибајтиxy(foo[:], 1000, 1000)
}

func (само *TMyТастатураeventhandler) ВклученоkeyГоре(key byte)	{}

var iГлушецeventhandler IГлушецeventhandler

type TMyГлушецeventhandler struct {
}

var глушецconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПозиција int16 = 0
var yПозиција int16 = 0

func (само *TMyГлушецeventhandler) ВклученоГлушецДолу(button int8) {
	buffer := []byte("x")
	глушецconsole.MПечатиxy(buffer, uint16(previousx), uint16(previousy))
}
func (само *TMyГлушецeventhandler) ВклученоГлушецГоре(button int8)	{}
func (само *TMyГлушецeventhandler) ВклученоГлушецПомести(x int8, y int8) {

	xПозиција += int16(x)
	if xПозиција < 0 {
		xПозиција = 0
	}
	if xПозиција >= 80 {
		xПозиција = 79
	}

	yПозиција -= int16(y)

	if yПозиција < 0 {
		yПозиција = 0
	}
	if yПозиција >= 25 {
		yПозиција = 24
	}

	buffer := []byte(" ")
	глушецconsole.MПечатиxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	глушецconsole.MПечатиxy(buffer, uint16(xПозиција), uint16(yПозиција))

	previousx = xПозиција
	previousy = yПозиција
}

var уредdescriptor TPeripheralcomponentinterconnectУредdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (само TMypcicontrollerhandler) Вклученоgetdriver(уред TPeripheralcomponentinterconnectУредdescriptor) {
	if уред.VendorИд == 0x1022 && уред.УредИд == 0x2000 {
		console.MПечатиxy([]byte("["), 0, 12)
		console.MПечати(([]byte)("AMD am79c973"))
		console.MПечати([]byte(":"))
		console.MUnsignedinteger16Печати(уред.VendorИд)
		console.MПечати([]byte(":"))
		console.MUnsignedinteger16Печати(уред.УредИд)
		console.MПечати([]byte(":"))
		console.MUnsignedinteger16Печати(uint16(уред.Портаbase))
		console.MПечати([]byte(":"))
		console.MUnsignedinteger32Печати(уред.Interrupt)

		console.MПечати([]byte("]\n"))
		уредdescriptor = уред
		drivercount++
	}
}
func (само TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectУредdescriptor {
	return уредdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Печатиstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MПечати(str)
}

func GetДатотекаГолемина(именадатотека []byte) uint32 {
	var ata0s = TНапредноtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читајpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var големина uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именадатотека)
	ata0s.Flush()

	return големина
}

func ЧитајДатотека(именадатотека []byte, data []byte) {
	var ata0s = TНапредноtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читајpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Читај(&ata0s, partition.Mbr.Primarypartition[0], именадатотека, data)

	ata0s.Flush()
}
func Искористеностelf() {

	var ata0s = TНапредноtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читајpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var именадатотека []byte = ([]byte)("TEST")
	var големина uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именадатотека)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Читај(&ata0s, partition.Mbr.Primarypartition[0], именадатотека, data)

	elf := Elf{}

	elf.Parse(data[:големина], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TФункција1() {
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

		SysПечатиunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func внесeventtask() {
	for {
		ПроцесpendingТастатураevents()
		ПроцесpendingГлушецevents()
		halt()
	}
}

func memorytest(y int) {
	меморијаmanager := &TМеморијаmanager{}
	allocated := uint32(uintptr(меморијаmanager.Malloc(1024)))
	console.MUnsignedinteger32Печатиxy(allocated, 10, uint16(y))
	if y == 11 {
		меморијаmanager.Слободни(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Освежиcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Поставиcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetФункцијаИме(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcИме = runtime.FuncForPC(address).Name()
	var funcбајти []byte = []byte(funcИме)

	taskconsole.MПечатиxy(funcбајти, 1, 5)
	taskconsole.MПечати(([]byte)(":"))
	taskconsole.MUnsignedinteger32Печати(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MПечатиunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(СтраницаДиректориумentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MПечати("\n=== MKD BOOT ===\n")

	console.MПечатиunsignedinteger32(uint32(СтраницаДиректориумentry), 0, 2)
	console.MПечатиunsignedinteger32(uint32(СтраницаДиректориумentry), 10, 2)
	console.MПечатиunsignedinteger32(uint32(stacktop), 0, 3)
	console.MПечатиunsignedinteger32(uint32(stackbottom), 10, 3)

	меморијаmanager := &TМеморијаmanager{}
	меморијаmanager.Init(0, MaxqueueГолемина)

	paging := &Paging{}
	paging.Init(СтраницаДиректориумentry, 0x500000, меморијаmanager)
	paging.SharedМеморијаregion()

	Поставиcr3(uint32(СтраницаДиректориумentry))
	Enablepaging()

	shareddescriptorТабела := &TShareddescriptorТабела{}
	shareddescriptorТабела.Init()

	console.MПечати("esp:")

	esp := getesp()
	console.MUnsignedinteger32Печати(uint32(esp))

	tls := gettls()
	console.MПечати(([]byte)("tls:"))
	console.MUnsignedinteger32Печати(tls)

	tss.Инсталирај(shareddescriptorТабела, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Освежиcr3()
	console.MПечати(([]byte)(":cr3:"))
	console.MUnsignedinteger32Печати(cr3)

	cr0 := Getcr0()
	console.MПечати(([]byte)(":cr0:"))
	console.MUnsignedinteger32Печати(cr0)

	cr4 := Getcr4()
	console.MПечати(([]byte)(":cr4:"))
	console.MUnsignedinteger32Печати(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorТабела, taskmanager_2)

	paging.Страницаfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(меморијаmanager)

	процесhelper := Процесhelper{}
	процесhelper.Init(меморијаmanager, СтраницаДиректориумentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, меморијаmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	процесhelper.Spawn(taska, threadhelper, sche, uint32(СтраницаДиректориумentry), true)
	процесhelper.Spawn(taskb, threadhelper, sche, uint32(СтраницаДиректориумentry), true)
	процесhelper.Spawn(taskc, threadhelper, sche, uint32(СтраницаДиректориумentry), true)
	процесhelper.Spawn(taskd1, threadhelper, sche, uint32(СтраницаДиректориумentry), true)
	процесhelper.Spawn(внесeventtask, threadhelper, sche, uint32(СтраницаДиректориумentry), true)

	var големина uint32

	var linkerДатотека []byte = ([]byte)("LINKER")
	големина = GetДатотекаГолемина(linkerДатотека)
	linkeraddress := меморијаmanager.Malloc(големина)
	linkerdata := GetбајтиfromСтрелка(uintptr(linkeraddress), int(големина), int(големина))
	ЧитајДатотека(linkerДатотека, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(СтраницаДиректориумentry))

	врскаmap := Врскаmap{}
	врскаmap.Init(меморијаmanager)

	var lib1Датотека []byte = ([]byte)("LIB1")
	големина = GetДатотекаГолемина(lib1Датотека)

	lib1address := меморијаmanager.Malloc(големина)
	lib1data := GetбајтиfromСтрелка(uintptr(lib1address), int(големина), int(големина))
	ЧитајДатотека(lib1Датотека, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(СтраницаДиректориумentry))
	меморијаmanager.Слободни(lib1address)

	врскаmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Датотека []byte = ([]byte)("LIB2")
	големина = GetДатотекаГолемина(lib2Датотека)

	lib2address := меморијаmanager.Malloc(големина)
	lib2data := GetбајтиfromСтрелка(uintptr(lib2address), int(големина), int(големина))
	ЧитајДатотека(lib2Датотека, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(СтраницаДиректориумentry))
	меморијаmanager.Слободни(lib2address)

	врскаmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libВрскаmap := врскаmap.Clone()
	врскаmapaddress := uint32(uintptr(Pointer(libВрскаmap.First)))

	lib1got := Getunsignedinteger32ПостроиfromСтрелка(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = врскаmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ПостроиfromСтрелка(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = врскаmapaddress
	lib2got[2] = 0x4000000

	console.MПечатиxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Печати(lib1elf.Got)
	console.MПечати(":")
	console.MUnsignedinteger32Печати(lib1elf.Dynamic)

	console.MПечатиxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Печати(lib2elf.Got)
	console.MПечати(":")
	console.MUnsignedinteger32Печати(lib2elf.Dynamic)

	var корисник1Датотека []byte = ([]byte)("USER1")
	големина = GetДатотекаГолемина(корисник1Датотека)
	корисник1address := меморијаmanager.Malloc(големина)
	корисник1data := GetбајтиfromСтрелка(uintptr(корисник1address), int(големина), int(големина))
	ЧитајДатотека(корисник1Датотека, корисник1data)

	elf2 := Elf{}

	корисник1entry := elf2.Getentry(корисник1data)
	elf2.Parse(корисник1data[:], uint32(СтраницаДиректориумentry+0x1000))
	глобалнаoffsetТабела := elf2.Got

	PВредност1Врскаmap := врскаmap.Clone()
	PВредност1Врскаmap.Append_to_list(uintptr(elf2.Dynamic))

	меморијаmanager.Слободни(корисник1address)

	var code1Стрелка *uintptr
	var func1val func()

	code1Стрелка = (*uintptr)(меморијаmanager.Malloc(4))
	*code1Стрелка = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Стрелка))

	proc2 := процесhelper.Spawn(func1val, threadhelper, sche, uint32(СтраницаДиректориумentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = корисник1entry
	thr2.Cpustate.Edx = глобалнаoffsetТабела
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PВредност1Врскаmap.First)))

	console.MПечатиxy("user1: ", 1, 10)
	console.MUnsignedinteger32Печати(elf2.Got)

	var корисник2Датотека []byte = ([]byte)("USER2")
	големина = GetДатотекаГолемина(корисник2Датотека)
	корисник2address := меморијаmanager.Malloc(големина)
	корисник2data := GetбајтиfromСтрелка(uintptr(корисник2address), int(големина), int(големина))
	ЧитајДатотека(корисник2Датотека, корисник2data)

	elf3 := Elf{}

	корисник2entry := elf3.Getentry(корисник2data)
	elf3.Parse(корисник2data[:], uint32(СтраницаДиректориумentry+0x2000))
	глобалнаoffsetТабела = elf3.Got

	PВредност2Врскаmap := врскаmap.Clone()
	PВредност2Врскаmap.Append_to_list(uintptr(elf3.Dynamic))

	меморијаmanager.Слободни(корисник2address)

	var code2Стрелка *uintptr
	var func2val func()

	code2Стрелка = (*uintptr)(меморијаmanager.Malloc(4))
	*code2Стрелка = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Стрелка))

	proc3 := процесhelper.Spawn(func2val, threadhelper, sche, uint32(СтраницаДиректориумentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = корисник2entry
	thr3.Cpustate.Edx = глобалнаoffsetТабела
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PВредност2Врскаmap.First)))

	console.MПечатиxy("user2: ", 1, 11)
	console.MUnsignedinteger32Печати(thr3.Cpustate.Esi)

	libВрскаmap.Печати(1, 11)

	var корисник3Датотека []byte = ([]byte)("USER3")
	големина = GetДатотекаГолемина(корисник3Датотека)
	корисник3address := меморијаmanager.Malloc(големина)
	корисник3data := GetбајтиfromСтрелка(uintptr(корисник3address), int(големина), int(големина))
	ЧитајДатотека(корисник3Датотека, корисник3data)

	elf4 := Elf{}

	корисник3entry := elf4.Getentry(корисник3data)
	elf4.Parse(корисник3data[:], uint32(СтраницаДиректориумentry+0x3000))
	глобалнаoffsetТабела = elf4.Got

	PВредност3Врскаmap := врскаmap.Clone()
	PВредност3Врскаmap.Append_to_list(uintptr(elf4.Dynamic))

	меморијаmanager.Слободни(корисник3address)

	var code3Стрелка *uintptr
	var func3val func()

	code3Стрелка = (*uintptr)(меморијаmanager.Malloc(4))
	*code3Стрелка = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Стрелка))

	proc4 := процесhelper.Spawn(func3val, threadhelper, sche, uint32(СтраницаДиректориумentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = корисник3entry
	thr4.Cpustate.Edx = глобалнаoffsetТабела
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PВредност3Врскаmap.First)))

	процесhelper.Spawn(TФункција1, threadhelper, sche, uint32(СтраницаДиректориумentry+0x4000), true)

	iТастатураeventhandler = &myТастатураeventhandler
	тастатураdriver.Initdriver(Interruptmanager, iТастатураeventhandler)

	глушецdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	уредdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Овозможено(true)
	Interruptmanager.Активно()

	for {
		halt()
	}

}
