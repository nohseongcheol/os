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

import . "sýndarMinni"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/lyklaborð"
import . "driver/mús"

import . "driver/ata"
import . "skráKerfis/msdospartition"
import . "skráKerfis/fat"

import . "skráKerfis/elf"

import . "kerfiscall"

import . "minnimanager"
import . "pci"

func halt()

var iLyklaborðeventhandler ILyklaborðeventhandler

type TMyLyklaborðeventhandler struct {
}

var myLyklaborðeventhandler TMyLyklaborðeventhandler
var lyklaborðdriver TLyklaborðdriver
var músdriver TMúsdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var lyklaborðconsole TConsole = TConsole{}

func (sjálft *TMyLyklaborðeventhandler) NotakeyNiður(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	lyklaborðconsole.MPrentaBætixy(foo[:], 1000, 1000)
}

func (sjálft *TMyLyklaborðeventhandler) NotakeyUpp(key byte)	{}

var iMúseventhandler IMúseventhandler

type TMyMúseventhandler struct {
}

var músconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xStaða int16 = 0
var yStaða int16 = 0

func (sjálft *TMyMúseventhandler) NotaMúsNiður(hnappur int8) {
	buffer := []byte("x")
	músconsole.MPrentaxy(buffer, uint16(previousx), uint16(previousy))
}
func (sjálft *TMyMúseventhandler) NotaMúsUpp(hnappur int8)	{}
func (sjálft *TMyMúseventhandler) NotaMúsFæra(x int8, y int8) {

	xStaða += int16(x)
	if xStaða < 0 {
		xStaða = 0
	}
	if xStaða >= 80 {
		xStaða = 79
	}

	yStaða -= int16(y)

	if yStaða < 0 {
		yStaða = 0
	}
	if yStaða >= 25 {
		yStaða = 24
	}

	buffer := []byte(" ")
	músconsole.MPrentaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	músconsole.MPrentaxy(buffer, uint16(xStaða), uint16(yStaða))

	previousx = xStaða
	previousy = yStaða
}

var tækidescriptor TPeripheralcomponentinterconnectTækidescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (sjálft TMypcicontrollerhandler) Notagetdriver(tæki TPeripheralcomponentinterconnectTækidescriptor) {
	if tæki.FramleiðandiAuðkenni == 0x1022 && tæki.TækiAuðkenni == 0x2000 {
		console.MPrentaxy([]byte("["), 0, 12)
		console.MPrenta(([]byte)("AMD am79c973"))
		console.MPrenta([]byte(":"))
		console.MUnsignedinteger16Prenta(tæki.FramleiðandiAuðkenni)
		console.MPrenta([]byte(":"))
		console.MUnsignedinteger16Prenta(tæki.TækiAuðkenni)
		console.MPrenta([]byte(":"))
		console.MUnsignedinteger16Prenta(uint16(tæki.Portbase))
		console.MPrenta([]byte(":"))
		console.MUnsignedinteger32Prenta(tæki.Interrupt)

		console.MPrenta([]byte("]\n"))
		tækidescriptor = tæki
		drivercount++
	}
}
func (sjálft TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectTækidescriptor {
	return tækidescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Prentastr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MPrenta(str)
}

func GetSkráStærð(skráarheiti []byte) uint32 {
	var ata0s = TNánarTækniattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTafla{}
	partition.Lesturpartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var stærð uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti)
	ata0s.Flush()

	return stærð
}

func LesturSkrá(skráarheiti []byte, data []byte) {
	var ata0s = TNánarTækniattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTafla{}
	partition.Lesturpartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Lestur(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti, data)

	ata0s.Flush()
}
func Álagelf() {

	var ata0s = TNánarTækniattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTafla{}
	partition.Lesturpartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var skráarheiti []byte = ([]byte)("TEST")
	var stærð uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lestur(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti, data)

	elf := Elf{}

	elf.Parse(data[:stærð], 0x4f00000)

}

var verkconsole TConsole = TConsole{}

func TAðgerð1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func verka() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func verkb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func verkc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func verkd()

func verkd0() {
	esi := getesi()
	for {

		SysPrentaunsignedinteger32(esi)

	}
}

func verkd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func inntakeventVerk() {
	for {
		ProcesspendingLyklaborðevents()
		ProcesspendingMúsevents()
		halt()
	}
}

func memorytest(y int) {
	minnimanager := &TMinnimanager{}
	allocated := uint32(uintptr(minnimanager.Malloc(1024)))
	console.MUnsignedinteger32Prentaxy(allocated, 10, uint16(y))
	if y == 11 {
		minnimanager.Laust(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Bíðaloop()
func Endurhlaðacr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Setjacr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetAðgerðHeiti(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcHeiti = runtime.FuncForPC(address).Name()
	var funcBæti []byte = []byte(funcHeiti)

	verkconsole.MPrentaxy(funcBæti, 1, 5)
	verkconsole.MPrenta(([]byte)(":"))
	verkconsole.MUnsignedinteger32Prenta(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	verkconsole.MPrentaunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Síðamappaentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MRaðnúmerloginit()
	console.MPrenta("\n=== ISL BOOT ===\n")

	console.MPrentaunsignedinteger32(uint32(Síðamappaentry), 0, 2)
	console.MPrentaunsignedinteger32(uint32(Síðamappaentry), 10, 2)
	console.MPrentaunsignedinteger32(uint32(stacktop), 0, 3)
	console.MPrentaunsignedinteger32(uint32(stackbottom), 10, 3)

	minnimanager := &TMinnimanager{}
	minnimanager.Init(0, HámarkqueueStærð)

	paging := &Paging{}
	paging.Init(Síðamappaentry, 0x500000, minnimanager)
	paging.SharedMinniregion()

	Setjacr3(uint32(Síðamappaentry))
	Enablepaging()

	shareddescriptorTafla := &TShareddescriptorTafla{}
	shareddescriptorTafla.Init()

	console.MPrenta("esp:")

	esp := getesp()
	console.MUnsignedinteger32Prenta(uint32(esp))

	tls := gettls()
	console.MPrenta(([]byte)("tls:"))
	console.MUnsignedinteger32Prenta(tls)

	tss.Setjaupp(shareddescriptorTafla, 7, Segkerneldata, esp)

	VirtPrófun()

	cr3 := Endurhlaðacr3()
	console.MPrenta(([]byte)(":cr3:"))
	console.MUnsignedinteger32Prenta(cr3)

	cr0 := Getcr0()
	console.MPrenta(([]byte)(":cr0:"))
	console.MUnsignedinteger32Prenta(cr0)

	cr4 := Getcr4()
	console.MPrenta(([]byte)(":cr4:"))
	console.MUnsignedinteger32Prenta(cr4)

	verkmanager_2 := &TVerkmanager{}
	verkmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorTafla, verkmanager_2)

	paging.Síðafault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(minnimanager)

	processhelper := Processhelper{}
	processhelper.Init(minnimanager, Síðamappaentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, minnimanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(verka, threadhelper, sche, uint32(Síðamappaentry), true)
	processhelper.Spawn(verkb, threadhelper, sche, uint32(Síðamappaentry), true)
	processhelper.Spawn(verkc, threadhelper, sche, uint32(Síðamappaentry), true)
	processhelper.Spawn(verkd1, threadhelper, sche, uint32(Síðamappaentry), true)
	processhelper.Spawn(inntakeventVerk, threadhelper, sche, uint32(Síðamappaentry), true)

	var stærð uint32

	var linkerSkrá []byte = ([]byte)("LINKER")
	stærð = GetSkráStærð(linkerSkrá)
	linkeraddress := minnimanager.Malloc(stærð)
	linkerdata := GetBætifromBendill(uintptr(linkeraddress), int(stærð), int(stærð))
	LesturSkrá(linkerSkrá, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Síðamappaentry))

	tengillmap := Tengillmap{}
	tengillmap.Init(minnimanager)

	var lib1Skrá []byte = ([]byte)("LIB1")
	stærð = GetSkráStærð(lib1Skrá)

	lib1address := minnimanager.Malloc(stærð)
	lib1data := GetBætifromBendill(uintptr(lib1address), int(stærð), int(stærð))
	LesturSkrá(lib1Skrá, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Síðamappaentry))
	minnimanager.Laust(lib1address)

	tengillmap.Append_to_list(uintptr(lib1elf.Breytilegt))

	var lib2Skrá []byte = ([]byte)("LIB2")
	stærð = GetSkráStærð(lib2Skrá)

	lib2address := minnimanager.Malloc(stærð)
	lib2data := GetBætifromBendill(uintptr(lib2address), int(stærð), int(stærð))
	LesturSkrá(lib2Skrá, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Síðamappaentry))
	minnimanager.Laust(lib2address)

	tengillmap.Append_to_list(uintptr(lib2elf.Breytilegt))

	libTengillmap := tengillmap.Clone()
	tengillmapaddress := uint32(uintptr(Pointer(libTengillmap.First)))

	lib1got := Getunsignedinteger32FylkifromBendill(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = tengillmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32FylkifromBendill(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = tengillmapaddress
	lib2got[2] = 0x4000000

	console.MPrentaxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Prenta(lib1elf.Got)
	console.MPrenta(":")
	console.MUnsignedinteger32Prenta(lib1elf.Breytilegt)

	console.MPrentaxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Prenta(lib2elf.Got)
	console.MPrenta(":")
	console.MUnsignedinteger32Prenta(lib2elf.Breytilegt)

	var notandi1Skrá []byte = ([]byte)("USER1")
	stærð = GetSkráStærð(notandi1Skrá)
	notandi1address := minnimanager.Malloc(stærð)
	notandi1data := GetBætifromBendill(uintptr(notandi1address), int(stærð), int(stærð))
	LesturSkrá(notandi1Skrá, notandi1data)

	elf2 := Elf{}

	notandi1entry := elf2.Getentry(notandi1data)
	elf2.Parse(notandi1data[:], uint32(Síðamappaentry+0x1000))
	víðværtoffsetTafla := elf2.Got

	PGildi1Tengillmap := tengillmap.Clone()
	PGildi1Tengillmap.Append_to_list(uintptr(elf2.Breytilegt))

	minnimanager.Laust(notandi1address)

	var code1Bendill *uintptr
	var func1val func()

	code1Bendill = (*uintptr)(minnimanager.Malloc(4))
	*code1Bendill = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Bendill))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(Síðamappaentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStaða.Ecx = notandi1entry
	thr2.CpuStaða.Edx = víðværtoffsetTafla
	thr2.CpuStaða.Esi = uint32(uintptr(Pointer(PGildi1Tengillmap.First)))

	console.MPrentaxy("user1: ", 1, 10)
	console.MUnsignedinteger32Prenta(elf2.Got)

	var notandi2Skrá []byte = ([]byte)("USER2")
	stærð = GetSkráStærð(notandi2Skrá)
	notandi2address := minnimanager.Malloc(stærð)
	notandi2data := GetBætifromBendill(uintptr(notandi2address), int(stærð), int(stærð))
	LesturSkrá(notandi2Skrá, notandi2data)

	elf3 := Elf{}

	notandi2entry := elf3.Getentry(notandi2data)
	elf3.Parse(notandi2data[:], uint32(Síðamappaentry+0x2000))
	víðværtoffsetTafla = elf3.Got

	PGildi2Tengillmap := tengillmap.Clone()
	PGildi2Tengillmap.Append_to_list(uintptr(elf3.Breytilegt))

	minnimanager.Laust(notandi2address)

	var code2Bendill *uintptr
	var func2val func()

	code2Bendill = (*uintptr)(minnimanager.Malloc(4))
	*code2Bendill = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Bendill))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(Síðamappaentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStaða.Ecx = notandi2entry
	thr3.CpuStaða.Edx = víðværtoffsetTafla
	thr3.CpuStaða.Esi = uint32(uintptr(Pointer(PGildi2Tengillmap.First)))

	console.MPrentaxy("user2: ", 1, 11)
	console.MUnsignedinteger32Prenta(thr3.CpuStaða.Esi)

	libTengillmap.Prenta(1, 11)

	var notandi3Skrá []byte = ([]byte)("USER3")
	stærð = GetSkráStærð(notandi3Skrá)
	notandi3address := minnimanager.Malloc(stærð)
	notandi3data := GetBætifromBendill(uintptr(notandi3address), int(stærð), int(stærð))
	LesturSkrá(notandi3Skrá, notandi3data)

	elf4 := Elf{}

	notandi3entry := elf4.Getentry(notandi3data)
	elf4.Parse(notandi3data[:], uint32(Síðamappaentry+0x3000))
	víðværtoffsetTafla = elf4.Got

	PGildi3Tengillmap := tengillmap.Clone()
	PGildi3Tengillmap.Append_to_list(uintptr(elf4.Breytilegt))

	minnimanager.Laust(notandi3address)

	var code3Bendill *uintptr
	var func3val func()

	code3Bendill = (*uintptr)(minnimanager.Malloc(4))
	*code3Bendill = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Bendill))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(Síðamappaentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStaða.Ecx = notandi3entry
	thr4.CpuStaða.Edx = víðværtoffsetTafla
	thr4.CpuStaða.Esi = uint32(uintptr(Pointer(PGildi3Tengillmap.First)))

	processhelper.Spawn(TAðgerð1, threadhelper, sche, uint32(Síðamappaentry+0x4000), true)

	iLyklaborðeventhandler = &myLyklaborðeventhandler
	lyklaborðdriver.Initdriver(Interruptmanager, iLyklaborðeventhandler)

	músdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Veljadriver(&Drivermanager, Interruptmanager)
	tækidescriptor = mypcicontrollerhandler.Getdriver()

	sche.Virkjað(true)
	Interruptmanager.Virkt()

	for {
		halt()
	}

}
