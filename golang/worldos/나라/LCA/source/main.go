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
import . "driver/pointing_device"

import . "driver/ata"
import . "filesystem/msdospartition"
import . "filesystem/fat"

import . "filesystem/executable_and_linkable_format"

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

	keyboardconsole.MPrintbytesxy(foo[:], 1000, 1000)
}

func (self *TMykeyboardeventhandler) Onkeyup(key byte)	{}

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
	mouseconsole.MPrintxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMymouseeventhandler) Onmouseup(button int8)	{}
func (self *TMymouseeventhandler) Onmousemove(x int8, y int8) {

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
	mouseconsole.MPrintxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mouseconsole.MPrintxy(buffer, uint16(xposition), uint16(yposition))

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
		console.MPrintxy([]byte("["), 0, 12)
		console.MPrint(([]byte)("AMD am79c973"))
		console.MPrint([]byte(":"))
		console.MUnsignedinteger16print(device.Vendorid)
		console.MPrint([]byte(":"))
		console.MUnsignedinteger16print(device.Deviceid)
		console.MPrint([]byte(":"))
		console.MUnsignedinteger16print(uint16(device.Portbase))
		console.MPrint([]byte(":"))
		console.MUnsignedinteger32print(device.Interrupt)

		console.MPrint([]byte("]\n"))
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
func Printstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MPrint(str)
}

func Getfilesize(filename []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Readpartition(&ata0s)

	bios := TFile_system_parameters32{}

	var size uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()

	return size
}

func Read_file(filename []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Readpartition(&ata0s)

	bios := TFile_system_parameters32{}
	bios.Read(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	ata0s.Flush()
}
func Loadelf() {

	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Readpartition(&ata0s)

	bios := TFile_system_parameters32{}

	var filename []byte = ([]byte)("TEST")
	var size uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Read(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	executable_and_linkable_format := Elf{}

	executable_and_linkable_format.Parse(data[:size], 0x4f00000)

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

		Sysprintunsignedinteger32(esi)

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
	allocated := uint32(uintptr(memorymanager.Allocate_memory(1024)))
	console.MUnsignedinteger32printxy(allocated, 10, uint16(y))
	if y == 11 {
		memorymanager.Free(Pointer(uintptr(allocated)))
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

func Getfunctionname(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcname = runtime.FuncForPC(address).Name()
	var funcbytes []byte = []byte(funcname)

	taskconsole.MPrintxy(funcbytes, 1, 5)
	taskconsole.MPrint(([]byte)(":"))
	taskconsole.MUnsignedinteger32print(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MPrintunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pagedirectoryentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MPrint("\n=== LCA BOOT ===\n")

	console.MPrintunsignedinteger32(uint32(Pagedirectoryentry), 0, 2)
	console.MPrintunsignedinteger32(uint32(Pagedirectoryentry), 10, 2)
	console.MPrintunsignedinteger32(uint32(stacktop), 0, 3)
	console.MPrintunsignedinteger32(uint32(stackbottom), 10, 3)

	memorymanager := &TMemorymanager{}
	memorymanager.Init(0, Maxqueuesize)

	paging := &Paging{}
	paging.Init(Pagedirectoryentry, 0x500000, memorymanager)
	paging.Sharedmemoryregion()

	Setcr3(uint32(Pagedirectoryentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MPrint("esp:")

	esp := getesp()
	console.MUnsignedinteger32print(uint32(esp))

	tls := gettls()
	console.MPrint(([]byte)("tls:"))
	console.MUnsignedinteger32print(tls)

	tss.Install(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Reloadcr3()
	console.MPrint(([]byte)(":cr3:"))
	console.MUnsignedinteger32print(cr3)

	cr0 := Getcr0()
	console.MPrint(([]byte)(":cr0:"))
	console.MUnsignedinteger32print(cr0)

	cr4 := Getcr4()
	console.MPrint(([]byte)(":cr4:"))
	console.MUnsignedinteger32print(cr4)

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

	var size uint32

	var linkerfile []byte = ([]byte)("LINKER")
	size = Getfilesize(linkerfile)
	linkeraddress := memorymanager.Allocate_memory(size)
	linkerdata := Getbytesfrompointer(uintptr(linkeraddress), int(size), int(size))
	Read_file(linkerfile, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pagedirectoryentry))

	linkmap := Linkmap{}
	linkmap.Init(memorymanager)

	var lib1file []byte = ([]byte)("LIB1")
	size = Getfilesize(lib1file)

	lib1address := memorymanager.Allocate_memory(size)
	lib1data := Getbytesfrompointer(uintptr(lib1address), int(size), int(size))
	Read_file(lib1file, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pagedirectoryentry))
	memorymanager.Free(lib1address)

	linkmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2file []byte = ([]byte)("LIB2")
	size = Getfilesize(lib2file)

	lib2address := memorymanager.Allocate_memory(size)
	lib2data := Getbytesfrompointer(uintptr(lib2address), int(size), int(size))
	Read_file(lib2file, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pagedirectoryentry))
	memorymanager.Free(lib2address)

	linkmap.Append_to_list(uintptr(lib2elf.Dynamic))

	liblinkmap := linkmap.Clone()
	linkmapaddress := uint32(uintptr(Pointer(liblinkmap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = linkmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = linkmapaddress
	lib2got[2] = 0x4000000

	console.MPrintxy("lib1: ", 1, 8)
	console.MUnsignedinteger32print(lib1elf.Got)
	console.MPrint(":")
	console.MUnsignedinteger32print(lib1elf.Dynamic)

	console.MPrintxy("lib2: ", 1, 9)
	console.MUnsignedinteger32print(lib2elf.Got)
	console.MPrint(":")
	console.MUnsignedinteger32print(lib2elf.Dynamic)

	var user1file []byte = ([]byte)("USER1")
	size = Getfilesize(user1file)
	user1address := memorymanager.Allocate_memory(size)
	user1data := Getbytesfrompointer(uintptr(user1address), int(size), int(size))
	Read_file(user1file, user1data)

	elf2 := Elf{}

	user1entry := elf2.Getentry(user1data)
	elf2.Parse(user1data[:], uint32(Pagedirectoryentry+0x1000))
	globaloffsettable := elf2.Got

	PValue1linkmap := linkmap.Clone()
	PValue1linkmap.Append_to_list(uintptr(elf2.Dynamic))

	memorymanager.Free(user1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(memorymanager.Allocate_memory(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(Pagedirectoryentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = user1entry
	thr2.Cpustate.Edx = globaloffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PValue1linkmap.First)))

	console.MPrintxy("user1: ", 1, 10)
	console.MUnsignedinteger32print(elf2.Got)

	var user2file []byte = ([]byte)("USER2")
	size = Getfilesize(user2file)
	user2address := memorymanager.Allocate_memory(size)
	user2data := Getbytesfrompointer(uintptr(user2address), int(size), int(size))
	Read_file(user2file, user2data)

	elf3 := Elf{}

	user2entry := elf3.Getentry(user2data)
	elf3.Parse(user2data[:], uint32(Pagedirectoryentry+0x2000))
	globaloffsettable = elf3.Got

	PValue2linkmap := linkmap.Clone()
	PValue2linkmap.Append_to_list(uintptr(elf3.Dynamic))

	memorymanager.Free(user2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(memorymanager.Allocate_memory(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(Pagedirectoryentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = user2entry
	thr3.Cpustate.Edx = globaloffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PValue2linkmap.First)))

	console.MPrintxy("user2: ", 1, 11)
	console.MUnsignedinteger32print(thr3.Cpustate.Esi)

	liblinkmap.Print(1, 11)

	var user3file []byte = ([]byte)("USER3")
	size = Getfilesize(user3file)
	user3address := memorymanager.Allocate_memory(size)
	user3data := Getbytesfrompointer(uintptr(user3address), int(size), int(size))
	Read_file(user3file, user3data)

	elf4 := Elf{}

	user3entry := elf4.Getentry(user3data)
	elf4.Parse(user3data[:], uint32(Pagedirectoryentry+0x3000))
	globaloffsettable = elf4.Got

	PValue3linkmap := linkmap.Clone()
	PValue3linkmap.Append_to_list(uintptr(elf4.Dynamic))

	memorymanager.Free(user3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(memorymanager.Allocate_memory(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(Pagedirectoryentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = user3entry
	thr4.Cpustate.Edx = globaloffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PValue3linkmap.First)))

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
