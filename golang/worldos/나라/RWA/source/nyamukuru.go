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
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtualUbubiko"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/mwandikisho"
import . "driver/imbeba"

import . "driver/ata"
import . "idosiyesystem/msdospartition"
import . "idosiyesystem/fat"

import . "idosiyesystem/elf"

import . "systemcall"

import . "ububikomanager"
import . "pci"

func halt()

var iMwandikishoeventhandler IMwandikishoeventhandler

type TMyMwandikishoeventhandler struct {
}

var myMwandikishoeventhandler TMyMwandikishoeventhandler
var mwandikishodriver TMwandikishodriver
var imbebadriver TImbebadriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var mwandikishoconsole TConsole = TConsole{}

func (self *TMyMwandikishoeventhandler) Kurikeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	mwandikishoconsole.MGucapaBayitexy(foo[:], 1000, 1000)
}

func (self *TMyMwandikishoeventhandler) Kurikeyup(key byte)	{}

var iImbebaeventhandler IImbebaeventhandler

type TMyImbebaeventhandler struct {
}

var imbebaconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMyImbebaeventhandler) KuriImbebadown(button int8) {
	buffer := []byte("x")
	imbebaconsole.MGucapaxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyImbebaeventhandler) KuriImbebaup(button int8)	{}
func (self *TMyImbebaeventhandler) KuriImbebamove(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	imbebaconsole.MGucapaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	imbebaconsole.MGucapaxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var ububikodescriptor TPeripheralcomponentinterconnectUbubikodescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Kurigetdriver(ububiko TPeripheralcomponentinterconnectUbubikodescriptor) {
	if ububiko.Vendorid == 0x1022 && ububiko.Ububikoid == 0x2000 {
		console.MGucapaxy([]byte("["), 0, 12)
		console.MGucapa(([]byte)("AMD am79c973"))
		console.MGucapa([]byte(":"))
		console.MUnsignedinteger16Gucapa(ububiko.Vendorid)
		console.MGucapa([]byte(":"))
		console.MUnsignedinteger16Gucapa(ububiko.Ububikoid)
		console.MGucapa([]byte(":"))
		console.MUnsignedinteger16Gucapa(uint16(ububiko.Umuyoborobase))
		console.MGucapa([]byte(":"))
		console.MUnsignedinteger32Gucapa(ububiko.Interrupt)

		console.MGucapa([]byte("]\n"))
		ububikodescriptor = ububiko
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectUbubikodescriptor {
	return ububikodescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Gucapastr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MGucapa(str)
}

func GetIdosiyeIngano(izinaryidosiye []byte) uint32 {
	var ata0s = TUrwegorwohejurutechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionImbonerahamwe{}
	partition.Gusomapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var ingano uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye)
	ata0s.Flush()

	return ingano
}

func GusomaIdosiye(izinaryidosiye []byte, data []byte) {
	var ata0s = TUrwegorwohejurutechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionImbonerahamwe{}
	partition.Gusomapartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Gusoma(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye, data)

	ata0s.Flush()
}
func Ibirimoelf() {

	var ata0s = TUrwegorwohejurutechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionImbonerahamwe{}
	partition.Gusomapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var izinaryidosiye []byte = ([]byte)("TEST")
	var ingano uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Gusoma(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye, data)

	elf := Elf{}

	elf.Parse(data[:ingano], 0x4f00000)

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

		SysGucapaunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func inputeventtask() {
	for {
		ProcesspendingMwandikishoevents()
		ProcesspendingImbebaevents()
		halt()
	}
}

func memorytest(y int) {
	ububikomanager := &TUbubikomanager{}
	allocated := uint32(uintptr(ububikomanager.Malloc(1024)))
	console.MUnsignedinteger32Gucapaxy(allocated, 10, uint16(y))
	if y == 11 {
		ububikomanager.Kigenga(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Reloadcr3() uint32

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

func GetfunctionIzina(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcIzina = runtime.FuncForPC(address).Name()
	var funcBayite []byte = []byte(funcIzina)

	taskconsole.MGucapaxy(funcBayite, 1, 5)
	taskconsole.MGucapa(([]byte)(":"))
	taskconsole.MUnsignedinteger32Gucapa(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MGucapaunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(IpajiUbubikoentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MGucapa("\n=== RWA BOOT ===\n")

	console.MGucapaunsignedinteger32(uint32(IpajiUbubikoentry), 0, 2)
	console.MGucapaunsignedinteger32(uint32(IpajiUbubikoentry), 10, 2)
	console.MGucapaunsignedinteger32(uint32(stacktop), 0, 3)
	console.MGucapaunsignedinteger32(uint32(stackbottom), 10, 3)

	ububikomanager := &TUbubikomanager{}
	ububikomanager.Init(0, MaxqueueIngano)

	paging := &Paging{}
	paging.Init(IpajiUbubikoentry, 0x500000, ububikomanager)
	paging.SharedUbubikoregion()

	Setcr3(uint32(IpajiUbubikoentry))
	Enablepaging()

	shareddescriptorImbonerahamwe := &TShareddescriptorImbonerahamwe{}
	shareddescriptorImbonerahamwe.Init()

	console.MGucapa("esp:")

	esp := getesp()
	console.MUnsignedinteger32Gucapa(uint32(esp))

	tls := gettls()
	console.MGucapa(([]byte)("tls:"))
	console.MUnsignedinteger32Gucapa(tls)

	tss.Install(shareddescriptorImbonerahamwe, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Reloadcr3()
	console.MGucapa(([]byte)(":cr3:"))
	console.MUnsignedinteger32Gucapa(cr3)

	cr0 := Getcr0()
	console.MGucapa(([]byte)(":cr0:"))
	console.MUnsignedinteger32Gucapa(cr0)

	cr4 := Getcr4()
	console.MGucapa(([]byte)(":cr4:"))
	console.MUnsignedinteger32Gucapa(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorImbonerahamwe, taskmanager_2)

	paging.Ipajifault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(ububikomanager)

	processhelper := Processhelper{}
	processhelper.Init(ububikomanager, IpajiUbubikoentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, ububikomanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(IpajiUbubikoentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(IpajiUbubikoentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(IpajiUbubikoentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(IpajiUbubikoentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(IpajiUbubikoentry), true)

	var ingano uint32

	var linkerIdosiye []byte = ([]byte)("LINKER")
	ingano = GetIdosiyeIngano(linkerIdosiye)
	linkeraddress := ububikomanager.Malloc(ingano)
	linkerdata := GetBayitefrompointer(uintptr(linkeraddress), int(ingano), int(ingano))
	GusomaIdosiye(linkerIdosiye, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(IpajiUbubikoentry))

	linkmap := Linkmap{}
	linkmap.Init(ububikomanager)

	var lib1Idosiye []byte = ([]byte)("LIB1")
	ingano = GetIdosiyeIngano(lib1Idosiye)

	lib1address := ububikomanager.Malloc(ingano)
	lib1data := GetBayitefrompointer(uintptr(lib1address), int(ingano), int(ingano))
	GusomaIdosiye(lib1Idosiye, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(IpajiUbubikoentry))
	ububikomanager.Kigenga(lib1address)

	linkmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Idosiye []byte = ([]byte)("LIB2")
	ingano = GetIdosiyeIngano(lib2Idosiye)

	lib2address := ububikomanager.Malloc(ingano)
	lib2data := GetBayitefrompointer(uintptr(lib2address), int(ingano), int(ingano))
	GusomaIdosiye(lib2Idosiye, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(IpajiUbubikoentry))
	ububikomanager.Kigenga(lib2address)

	linkmap.Append_to_list(uintptr(lib2elf.Dynamic))

	liblinkmap := linkmap.Clone()
	linkmapaddress := uint32(uintptr(Pointer(liblinkmap.First)))

	lib1got := Getunsignedinteger32Imbonerahamwefrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = linkmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32Imbonerahamwefrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = linkmapaddress
	lib2got[2] = 0x4000000

	console.MGucapaxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Gucapa(lib1elf.Got)
	console.MGucapa(":")
	console.MUnsignedinteger32Gucapa(lib1elf.Dynamic)

	console.MGucapaxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Gucapa(lib2elf.Got)
	console.MGucapa(":")
	console.MUnsignedinteger32Gucapa(lib2elf.Dynamic)

	var ukoresha1Idosiye []byte = ([]byte)("USER1")
	ingano = GetIdosiyeIngano(ukoresha1Idosiye)
	ukoresha1address := ububikomanager.Malloc(ingano)
	ukoresha1data := GetBayitefrompointer(uintptr(ukoresha1address), int(ingano), int(ingano))
	GusomaIdosiye(ukoresha1Idosiye, ukoresha1data)

	elf2 := Elf{}

	ukoresha1entry := elf2.Getentry(ukoresha1data)
	elf2.Parse(ukoresha1data[:], uint32(IpajiUbubikoentry+0x1000))
	globaloffsetImbonerahamwe := elf2.Got

	PAgaciro1linkmap := linkmap.Clone()
	PAgaciro1linkmap.Append_to_list(uintptr(elf2.Dynamic))

	ububikomanager.Kigenga(ukoresha1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(ububikomanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(IpajiUbubikoentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = ukoresha1entry
	thr2.Cpustate.Edx = globaloffsetImbonerahamwe
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PAgaciro1linkmap.First)))

	console.MGucapaxy("user1: ", 1, 10)
	console.MUnsignedinteger32Gucapa(elf2.Got)

	var ukoresha2Idosiye []byte = ([]byte)("USER2")
	ingano = GetIdosiyeIngano(ukoresha2Idosiye)
	ukoresha2address := ububikomanager.Malloc(ingano)
	ukoresha2data := GetBayitefrompointer(uintptr(ukoresha2address), int(ingano), int(ingano))
	GusomaIdosiye(ukoresha2Idosiye, ukoresha2data)

	elf3 := Elf{}

	ukoresha2entry := elf3.Getentry(ukoresha2data)
	elf3.Parse(ukoresha2data[:], uint32(IpajiUbubikoentry+0x2000))
	globaloffsetImbonerahamwe = elf3.Got

	PAgaciro2linkmap := linkmap.Clone()
	PAgaciro2linkmap.Append_to_list(uintptr(elf3.Dynamic))

	ububikomanager.Kigenga(ukoresha2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(ububikomanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(IpajiUbubikoentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = ukoresha2entry
	thr3.Cpustate.Edx = globaloffsetImbonerahamwe
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PAgaciro2linkmap.First)))

	console.MGucapaxy("user2: ", 1, 11)
	console.MUnsignedinteger32Gucapa(thr3.Cpustate.Esi)

	liblinkmap.Gucapa(1, 11)

	var ukoresha3Idosiye []byte = ([]byte)("USER3")
	ingano = GetIdosiyeIngano(ukoresha3Idosiye)
	ukoresha3address := ububikomanager.Malloc(ingano)
	ukoresha3data := GetBayitefrompointer(uintptr(ukoresha3address), int(ingano), int(ingano))
	GusomaIdosiye(ukoresha3Idosiye, ukoresha3data)

	elf4 := Elf{}

	ukoresha3entry := elf4.Getentry(ukoresha3data)
	elf4.Parse(ukoresha3data[:], uint32(IpajiUbubikoentry+0x3000))
	globaloffsetImbonerahamwe = elf4.Got

	PAgaciro3linkmap := linkmap.Clone()
	PAgaciro3linkmap.Append_to_list(uintptr(elf4.Dynamic))

	ububikomanager.Kigenga(ukoresha3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(ububikomanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(IpajiUbubikoentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = ukoresha3entry
	thr4.Cpustate.Edx = globaloffsetImbonerahamwe
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PAgaciro3linkmap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(IpajiUbubikoentry+0x4000), true)

	iMwandikishoeventhandler = &myMwandikishoeventhandler
	mwandikishodriver.Initdriver(Interruptmanager, iMwandikishoeventhandler)

	imbebadriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	ububikodescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	Interruptmanager.Gikora()

	for {
		halt()
	}

}
