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

import . "driver/knappaborð"
import . "driver/mús"

import . "driver/ata"
import . "fílasystem/msdospartition"
import . "fílasystem/fat"

import . "fílasystem/elf"

import . "systemcall"

import . "memorymanager"
import . "pci"

func halt()

var iKnappaborðeventhandler IKnappaborðeventhandler

type TMyKnappaborðeventhandler struct {
}

var myKnappaborðeventhandler TMyKnappaborðeventhandler
var knappaborðdriver TKnappaborðdriver
var músdriver TMúsdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var knappaborðconsole TConsole = TConsole{}

func (self *TMyKnappaborðeventhandler) Onkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	knappaborðconsole.MPrintbýtxy(foo[:], 1000, 1000)
}

func (self *TMyKnappaborðeventhandler) Onkeyup(key byte)	{}

var iMúseventhandler IMúseventhandler

type TMyMúseventhandler struct {
}

var músconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMyMúseventhandler) OnMúsdown(knappur int8) {
	buffer := []byte("x")
	músconsole.MPrintxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyMúseventhandler) OnMúsup(knappur int8)	{}
func (self *TMyMúseventhandler) OnMúsmove(x int8, y int8) {

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
	músconsole.MPrintxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	músconsole.MPrintxy(buffer, uint16(xposition), uint16(yposition))

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

func GetFílaStødd(filename []byte) uint32 {
	var ata0s = TFramkomiðtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Lesapartition(&ata0s)

	bios := TBiosparameterBlokkur32{}

	var stødd uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()

	return stødd
}

func LesaFíla(filename []byte, data []byte) {
	var ata0s = TFramkomiðtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Lesapartition(&ata0s)

	bios := TBiosparameterBlokkur32{}
	bios.Lesa(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	ata0s.Flush()
}
func Loadelf() {

	var ata0s = TFramkomiðtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Lesapartition(&ata0s)

	bios := TBiosparameterBlokkur32{}

	var filename []byte = ([]byte)("TEST")
	var stødd uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lesa(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	elf := Elf{}

	elf.Parse(data[:stødd], 0x4f00000)

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
		ProcesspendingKnappaborðevents()
		ProcesspendingMúsevents()
		halt()
	}
}

func memorytest(y int) {
	memorymanager := &TMemorymanager{}
	allocated := uint32(uintptr(memorymanager.Malloc(1024)))
	console.MUnsignedinteger32printxy(allocated, 10, uint16(y))
	if y == 11 {
		memorymanager.Free(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Steðgabráfeingisloop()
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

func GetfunctionNavn(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNavn = runtime.FuncForPC(address).Name()
	var funcbýt []byte = []byte(funcNavn)

	taskconsole.MPrintxy(funcbýt, 1, 5)
	taskconsole.MPrint(([]byte)(":"))
	taskconsole.MUnsignedinteger32print(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MPrintunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(PageFíluskráentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MPrint("\n=== FRO BOOT ===\n")

	console.MPrintunsignedinteger32(uint32(PageFíluskráentry), 0, 2)
	console.MPrintunsignedinteger32(uint32(PageFíluskráentry), 10, 2)
	console.MPrintunsignedinteger32(uint32(stacktop), 0, 3)
	console.MPrintunsignedinteger32(uint32(stackbottom), 10, 3)

	memorymanager := &TMemorymanager{}
	memorymanager.Init(0, MaxqueueStødd)

	paging := &Paging{}
	paging.Init(PageFíluskráentry, 0x500000, memorymanager)
	paging.Sharedmemoryregion()

	Setcr3(uint32(PageFíluskráentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MPrint("esp:")

	esp := getesp()
	console.MUnsignedinteger32print(uint32(esp))

	tls := gettls()
	console.MPrint(([]byte)("tls:"))
	console.MUnsignedinteger32print(tls)

	tss.Legginn(shareddescriptortable, 7, Segkerneldata, esp)

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
	processhelper.Init(memorymanager, PageFíluskráentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, memorymanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(PageFíluskráentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(PageFíluskráentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(PageFíluskráentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(PageFíluskráentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(PageFíluskráentry), true)

	var stødd uint32

	var linkerFíla []byte = ([]byte)("LINKER")
	stødd = GetFílaStødd(linkerFíla)
	linkeraddress := memorymanager.Malloc(stødd)
	linkerdata := Getbýtfrompointer(uintptr(linkeraddress), int(stødd), int(stødd))
	LesaFíla(linkerFíla, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PageFíluskráentry))

	linkmap := Linkmap{}
	linkmap.Init(memorymanager)

	var lib1Fíla []byte = ([]byte)("LIB1")
	stødd = GetFílaStødd(lib1Fíla)

	lib1address := memorymanager.Malloc(stødd)
	lib1data := Getbýtfrompointer(uintptr(lib1address), int(stødd), int(stødd))
	LesaFíla(lib1Fíla, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PageFíluskráentry))
	memorymanager.Free(lib1address)

	linkmap.Append_to_list(uintptr(lib1elf.Rakstrarmáttur))

	var lib2Fíla []byte = ([]byte)("LIB2")
	stødd = GetFílaStødd(lib2Fíla)

	lib2address := memorymanager.Malloc(stødd)
	lib2data := Getbýtfrompointer(uintptr(lib2address), int(stødd), int(stødd))
	LesaFíla(lib2Fíla, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PageFíluskráentry))
	memorymanager.Free(lib2address)

	linkmap.Append_to_list(uintptr(lib2elf.Rakstrarmáttur))

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
	console.MUnsignedinteger32print(lib1elf.Rakstrarmáttur)

	console.MPrintxy("lib2: ", 1, 9)
	console.MUnsignedinteger32print(lib2elf.Got)
	console.MPrint(":")
	console.MUnsignedinteger32print(lib2elf.Rakstrarmáttur)

	var brúkari1Fíla []byte = ([]byte)("USER1")
	stødd = GetFílaStødd(brúkari1Fíla)
	brúkari1address := memorymanager.Malloc(stødd)
	brúkari1data := Getbýtfrompointer(uintptr(brúkari1address), int(stødd), int(stødd))
	LesaFíla(brúkari1Fíla, brúkari1data)

	elf2 := Elf{}

	brúkari1entry := elf2.Getentry(brúkari1data)
	elf2.Parse(brúkari1data[:], uint32(PageFíluskráentry+0x1000))
	globaloffsettable := elf2.Got

	PValue1linkmap := linkmap.Clone()
	PValue1linkmap.Append_to_list(uintptr(elf2.Rakstrarmáttur))

	memorymanager.Free(brúkari1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(memorymanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(PageFíluskráentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStøða.Ecx = brúkari1entry
	thr2.CpuStøða.Edx = globaloffsettable
	thr2.CpuStøða.Esi = uint32(uintptr(Pointer(PValue1linkmap.First)))

	console.MPrintxy("user1: ", 1, 10)
	console.MUnsignedinteger32print(elf2.Got)

	var brúkari2Fíla []byte = ([]byte)("USER2")
	stødd = GetFílaStødd(brúkari2Fíla)
	brúkari2address := memorymanager.Malloc(stødd)
	brúkari2data := Getbýtfrompointer(uintptr(brúkari2address), int(stødd), int(stødd))
	LesaFíla(brúkari2Fíla, brúkari2data)

	elf3 := Elf{}

	brúkari2entry := elf3.Getentry(brúkari2data)
	elf3.Parse(brúkari2data[:], uint32(PageFíluskráentry+0x2000))
	globaloffsettable = elf3.Got

	PValue2linkmap := linkmap.Clone()
	PValue2linkmap.Append_to_list(uintptr(elf3.Rakstrarmáttur))

	memorymanager.Free(brúkari2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(memorymanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(PageFíluskráentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStøða.Ecx = brúkari2entry
	thr3.CpuStøða.Edx = globaloffsettable
	thr3.CpuStøða.Esi = uint32(uintptr(Pointer(PValue2linkmap.First)))

	console.MPrintxy("user2: ", 1, 11)
	console.MUnsignedinteger32print(thr3.CpuStøða.Esi)

	liblinkmap.Print(1, 11)

	var brúkari3Fíla []byte = ([]byte)("USER3")
	stødd = GetFílaStødd(brúkari3Fíla)
	brúkari3address := memorymanager.Malloc(stødd)
	brúkari3data := Getbýtfrompointer(uintptr(brúkari3address), int(stødd), int(stødd))
	LesaFíla(brúkari3Fíla, brúkari3data)

	elf4 := Elf{}

	brúkari3entry := elf4.Getentry(brúkari3data)
	elf4.Parse(brúkari3data[:], uint32(PageFíluskráentry+0x3000))
	globaloffsettable = elf4.Got

	PValue3linkmap := linkmap.Clone()
	PValue3linkmap.Append_to_list(uintptr(elf4.Rakstrarmáttur))

	memorymanager.Free(brúkari3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(memorymanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(PageFíluskráentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStøða.Ecx = brúkari3entry
	thr4.CpuStøða.Edx = globaloffsettable
	thr4.CpuStøða.Esi = uint32(uintptr(Pointer(PValue3linkmap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(PageFíluskráentry+0x4000), true)

	iKnappaborðeventhandler = &myKnappaborðeventhandler
	knappaborðdriver.Initdriver(Interruptmanager, iKnappaborðeventhandler)

	músdriver.Initdriver(Interruptmanager, nil)

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
