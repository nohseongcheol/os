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

import . "virtualmemory"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/keyboard"
import . "driver/mouse"

import . "driver/ata"
import . "faýlsystem/msdospartition"
import . "faýlsystem/fat"

import . "faýlsystem/elf"

import . "systemcall"

import . "memorymanager"
import . "pci"

func halt()

var ikeyboardeventhandler IKeyboardeventhandler

type TMykeyboardeventhandler struct {
}

var mykeyboardeventhandler TMykeyboardeventhandler
var keyboarddriver TKeyboarddriver
var mousedriver TMousedriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var keyboardconsole TConsole = TConsole{}

func (self *TMykeyboardeventhandler) Onkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	keyboardconsole.MÇapBaýtlarxy(foo[:], 1000, 1000)
}

func (self *TMykeyboardeventhandler) OnkeyÝokary(key byte)	{}

var imouseeventhandler IMouseeventhandler

type TMymouseeventhandler struct {
}

var mouseconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMymouseeventhandler) Onmousedown(button int8) {
	buffer := []byte("x")
	mouseconsole.MÇapxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMymouseeventhandler) OnmouseÝokary(button int8)	{}
func (self *TMymouseeventhandler) OnmouseGöçir(x int8, y int8) {

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
	mouseconsole.MÇapxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mouseconsole.MÇapxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var devicedescriptor TPeripheralcomponentinterconnectdevicedescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(device TPeripheralcomponentinterconnectdevicedescriptor) {
	if device.Vendorid == 0x1022 && device.Deviceid == 0x2000 {
		console.MÇapxy([]byte("["), 0, 12)
		console.MÇap(([]byte)("AMD am79c973"))
		console.MÇap([]byte(":"))
		console.MUnsignedinteger16Çap(device.Vendorid)
		console.MÇap([]byte(":"))
		console.MUnsignedinteger16Çap(device.Deviceid)
		console.MÇap([]byte(":"))
		console.MUnsignedinteger16Çap(uint16(device.Portbase))
		console.MÇap([]byte(":"))
		console.MUnsignedinteger32Çap(device.Interrupt)

		console.MÇap([]byte("]\n"))
		devicedescriptor = device
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectdevicedescriptor {
	return devicedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Çapstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MÇap(str)
}

func GetFaýlUlulyk(faýlady []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Okapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var ululyk uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faýlady)
	ata0s.Flush()

	return ululyk
}

func OkaFaýl(faýlady []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Okapartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Oka(&ata0s, partition.Mbr.Primarypartition[0], faýlady, data)

	ata0s.Flush()
}
func Loadelf() {

	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Okapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var faýlady []byte = ([]byte)("TEST")
	var ululyk uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faýlady)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Oka(&ata0s, partition.Mbr.Primarypartition[0], faýlady, data)

	elf := Elf{}

	elf.Parse(data[:ululyk], 0x4f00000)

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

		SysÇapunsignedinteger32(esi)

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
		Processpendingkeyboardevents()
		Processpendingmouseevents()
		halt()
	}
}

func memorytest(y int) {
	memorymanager := &TMemorymanager{}
	allocated := uint32(uintptr(memorymanager.Malloc(1024)))
	console.MUnsignedinteger32Çapxy(allocated, 10, uint16(y))
	if y == 11 {
		memorymanager.Free(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func ÝeneÝüklecr3() uint32

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

func GetfunctionAd(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcAd = runtime.FuncForPC(address).Name()
	var funcBaýtlar []byte = []byte(funcAd)

	taskconsole.MÇapxy(funcBaýtlar, 1, 5)
	taskconsole.MÇap(([]byte)(":"))
	taskconsole.MUnsignedinteger32Çap(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MÇapunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pagedirectoryentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MÇap("\n=== TKM BOOT ===\n")

	console.MÇapunsignedinteger32(uint32(Pagedirectoryentry), 0, 2)
	console.MÇapunsignedinteger32(uint32(Pagedirectoryentry), 10, 2)
	console.MÇapunsignedinteger32(uint32(stacktop), 0, 3)
	console.MÇapunsignedinteger32(uint32(stackbottom), 10, 3)

	memorymanager := &TMemorymanager{}
	memorymanager.Init(0, MaxqueueUlulyk)

	paging := &Paging{}
	paging.Init(Pagedirectoryentry, 0x500000, memorymanager)
	paging.Sharedmemoryregion()

	Setcr3(uint32(Pagedirectoryentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MÇap("esp:")

	esp := getesp()
	console.MUnsignedinteger32Çap(uint32(esp))

	tls := gettls()
	console.MÇap(([]byte)("tls:"))
	console.MUnsignedinteger32Çap(tls)

	tss.Install(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := ÝeneÝüklecr3()
	console.MÇap(([]byte)(":cr3:"))
	console.MUnsignedinteger32Çap(cr3)

	cr0 := Getcr0()
	console.MÇap(([]byte)(":cr0:"))
	console.MUnsignedinteger32Çap(cr0)

	cr4 := Getcr4()
	console.MÇap(([]byte)(":cr4:"))
	console.MUnsignedinteger32Çap(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptortable, taskmanager_2)

	paging.Pagefault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorymanager)

	processhelper := Processhelper{}
	processhelper.Init(memorymanager, Pagedirectoryentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, memorymanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(Pagedirectoryentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(Pagedirectoryentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(Pagedirectoryentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(Pagedirectoryentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(Pagedirectoryentry), true)

	var ululyk uint32

	var linkerFaýl []byte = ([]byte)("LINKER")
	ululyk = GetFaýlUlulyk(linkerFaýl)
	linkeraddress := memorymanager.Malloc(ululyk)
	linkerdata := GetBaýtlarfrompointer(uintptr(linkeraddress), int(ululyk), int(ululyk))
	OkaFaýl(linkerFaýl, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pagedirectoryentry))

	baglaýyşmap := Baglaýyşmap{}
	baglaýyşmap.Init(memorymanager)

	var lib1Faýl []byte = ([]byte)("LIB1")
	ululyk = GetFaýlUlulyk(lib1Faýl)

	lib1address := memorymanager.Malloc(ululyk)
	lib1data := GetBaýtlarfrompointer(uintptr(lib1address), int(ululyk), int(ululyk))
	OkaFaýl(lib1Faýl, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pagedirectoryentry))
	memorymanager.Free(lib1address)

	baglaýyşmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Faýl []byte = ([]byte)("LIB2")
	ululyk = GetFaýlUlulyk(lib2Faýl)

	lib2address := memorymanager.Malloc(ululyk)
	lib2data := GetBaýtlarfrompointer(uintptr(lib2address), int(ululyk), int(ululyk))
	OkaFaýl(lib2Faýl, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pagedirectoryentry))
	memorymanager.Free(lib2address)

	baglaýyşmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libbaglaýyşmap := baglaýyşmap.Clone()
	baglaýyşmapaddress := uint32(uintptr(Pointer(libbaglaýyşmap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = baglaýyşmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = baglaýyşmapaddress
	lib2got[2] = 0x4000000

	console.MÇapxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Çap(lib1elf.Got)
	console.MÇap(":")
	console.MUnsignedinteger32Çap(lib1elf.Dynamic)

	console.MÇapxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Çap(lib2elf.Got)
	console.MÇap(":")
	console.MUnsignedinteger32Çap(lib2elf.Dynamic)

	var ullançy1Faýl []byte = ([]byte)("USER1")
	ululyk = GetFaýlUlulyk(ullançy1Faýl)
	ullançy1address := memorymanager.Malloc(ululyk)
	ullançy1data := GetBaýtlarfrompointer(uintptr(ullançy1address), int(ululyk), int(ululyk))
	OkaFaýl(ullançy1Faýl, ullançy1data)

	elf2 := Elf{}

	ullançy1entry := elf2.Getentry(ullançy1data)
	elf2.Parse(ullançy1data[:], uint32(Pagedirectoryentry+0x1000))
	globaloffsettable := elf2.Got

	PMykdar1baglaýyşmap := baglaýyşmap.Clone()
	PMykdar1baglaýyşmap.Append_to_list(uintptr(elf2.Dynamic))

	memorymanager.Free(ullançy1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(memorymanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(Pagedirectoryentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = ullançy1entry
	thr2.Cpustate.Edx = globaloffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PMykdar1baglaýyşmap.First)))

	console.MÇapxy("user1: ", 1, 10)
	console.MUnsignedinteger32Çap(elf2.Got)

	var ullançy2Faýl []byte = ([]byte)("USER2")
	ululyk = GetFaýlUlulyk(ullançy2Faýl)
	ullançy2address := memorymanager.Malloc(ululyk)
	ullançy2data := GetBaýtlarfrompointer(uintptr(ullançy2address), int(ululyk), int(ululyk))
	OkaFaýl(ullançy2Faýl, ullançy2data)

	elf3 := Elf{}

	ullançy2entry := elf3.Getentry(ullançy2data)
	elf3.Parse(ullançy2data[:], uint32(Pagedirectoryentry+0x2000))
	globaloffsettable = elf3.Got

	PMykdar2baglaýyşmap := baglaýyşmap.Clone()
	PMykdar2baglaýyşmap.Append_to_list(uintptr(elf3.Dynamic))

	memorymanager.Free(ullançy2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(memorymanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(Pagedirectoryentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = ullançy2entry
	thr3.Cpustate.Edx = globaloffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PMykdar2baglaýyşmap.First)))

	console.MÇapxy("user2: ", 1, 11)
	console.MUnsignedinteger32Çap(thr3.Cpustate.Esi)

	libbaglaýyşmap.Çap(1, 11)

	var ullançy3Faýl []byte = ([]byte)("USER3")
	ululyk = GetFaýlUlulyk(ullançy3Faýl)
	ullançy3address := memorymanager.Malloc(ululyk)
	ullançy3data := GetBaýtlarfrompointer(uintptr(ullançy3address), int(ululyk), int(ululyk))
	OkaFaýl(ullançy3Faýl, ullançy3data)

	elf4 := Elf{}

	ullançy3entry := elf4.Getentry(ullançy3data)
	elf4.Parse(ullançy3data[:], uint32(Pagedirectoryentry+0x3000))
	globaloffsettable = elf4.Got

	PMykdar3baglaýyşmap := baglaýyşmap.Clone()
	PMykdar3baglaýyşmap.Append_to_list(uintptr(elf4.Dynamic))

	memorymanager.Free(ullançy3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(memorymanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(Pagedirectoryentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = ullançy3entry
	thr4.Cpustate.Edx = globaloffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PMykdar3baglaýyşmap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(Pagedirectoryentry+0x4000), true)

	ikeyboardeventhandler = &mykeyboardeventhandler
	keyboarddriver.Initdriver(Interruptmanager, ikeyboardeventhandler)

	mousedriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	devicedescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	Interruptmanager.Active()

	for {
		halt()
	}

}
