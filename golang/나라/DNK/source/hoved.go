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

import . "virtuelHukommelse"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/tastatur"
import . "driver/mus"

import . "driver/ata"
import . "filsystem/msdospartition"
import . "filsystem/fat"

import . "filsystem/elf"

import . "systemcall"

import . "hukommelsemanager"
import . "pci"

func halt()

var iTastatureventhandler ITastatureventhandler

type TMyTastatureventhandler struct {
}

var myTastatureventhandler TMyTastatureventhandler
var tastaturdriver TTastaturdriver
var musdriver TMusdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastaturconsole TConsole = TConsole{}

func (selv *TMyTastatureventhandler) TændtNøgleNed(nøgle byte) {
	foo := [1]byte{' '}
	foo[0] = nøgle

	tastaturconsole.MUdskrivBytexy(foo[:], 1000, 1000)
}

func (selv *TMyTastatureventhandler) TændtNøgleOp(nøgle byte)	{}

var iMuseventhandler IMuseventhandler

type TMyMuseventhandler struct {
}

var musconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPlacering int16 = 0
var yPlacering int16 = 0

func (selv *TMyMuseventhandler) TændtMusNed(knap int8) {
	buffer := []byte("x")
	musconsole.MUdskrivxy(buffer, uint16(previousx), uint16(previousy))
}
func (selv *TMyMuseventhandler) TændtMusOp(knap int8)	{}
func (selv *TMyMuseventhandler) TændtMusFlyt(x int8, y int8) {

	xPlacering += int16(x)
	if xPlacering < 0 {
		xPlacering = 0
	}
	if xPlacering >= 80 {
		xPlacering = 79
	}

	yPlacering -= int16(y)

	if yPlacering < 0 {
		yPlacering = 0
	}
	if yPlacering >= 25 {
		yPlacering = 24
	}

	buffer := []byte(" ")
	musconsole.MUdskrivxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	musconsole.MUdskrivxy(buffer, uint16(xPlacering), uint16(yPlacering))

	previousx = xPlacering
	previousy = yPlacering
}

var enheddescriptor TPeripheralcomponentinterconnectEnheddescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var driverAntal uint16 = 0

func (selv TMypcicontrollerhandler) Tændtgetdriver(enhed TPeripheralcomponentinterconnectEnheddescriptor) {
	if enhed.Forhandlerid == 0x1022 && enhed.Enhedid == 0x2000 {
		console.MUdskrivxy([]byte("["), 0, 12)
		console.MUdskriv(([]byte)("AMD am79c973"))
		console.MUdskriv([]byte(":"))
		console.MUnsignedinteger16Udskriv(enhed.Forhandlerid)
		console.MUdskriv([]byte(":"))
		console.MUnsignedinteger16Udskriv(enhed.Enhedid)
		console.MUdskriv([]byte(":"))
		console.MUnsignedinteger16Udskriv(uint16(enhed.Portbase))
		console.MUdskriv([]byte(":"))
		console.MUnsignedinteger32Udskriv(enhed.Interrupt)

		console.MUdskriv([]byte("]\n"))
		enheddescriptor = enhed
		driverAntal++
	}
}
func (selv TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectEnheddescriptor {
	return enheddescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Udskrivstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MUdskriv(str)
}

func GetFilStørrelse(filnavn []byte) uint32 {
	var ata0s = TAvanceretTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Læsepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var størrelse uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	ata0s.Flush()

	return størrelse
}

func LæseFil(filnavn []byte, data []byte) {
	var ata0s = TAvanceretTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Læsepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Læse(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)

	ata0s.Flush()
}
func Belastningelf() {

	var ata0s = TAvanceretTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Læsepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var filnavn []byte = ([]byte)("TEST")
	var størrelse uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Læse(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)

	elf := Elf{}

	elf.Parse(data[:størrelse], 0x4f00000)

}

var opgaveconsole TConsole = TConsole{}

func TFunktion1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func opgavea() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func opgaveb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func opgavec() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func opgaved()

func opgaved0() {
	esi := getesi()
	for {

		SysUdskrivunsignedinteger32(esi)

	}
}

func opgaved1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func indgangeventOpgave() {
	for {
		ProcespendingTastaturBegivenheder()
		ProcespendingMusBegivenheder()
		halt()
	}
}

func memorytest(y int) {
	hukommelsemanager := &THukommelsemanager{}
	allocated := uint32(uintptr(hukommelsemanager.Malloc(1024)))
	console.MUnsignedinteger32Udskrivxy(allocated, 10, uint16(y))
	if y == 11 {
		hukommelsemanager.Fri(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func PauseLøkkekolonier()
func Genindlæscr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Satcr3(cr3 uint32)
func Getcr4() uint32
func Aktiverpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunktionNavn(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNavn = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcNavn)

	opgaveconsole.MUdskrivxy(funcByte, 1, 5)
	opgaveconsole.MUdskriv(([]byte)(":"))
	opgaveconsole.MUnsignedinteger32Udskriv(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	opgaveconsole.MUdskrivunsignedinteger32(cr0, 2, 1)
}

var tss *Tssemne = &Tssemne{}

func KKernelEntry(SideMappeemne uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerielloginit()
	console.MUdskriv("\n=== DNK BOOT ===\n")

	console.MUdskrivunsignedinteger32(uint32(SideMappeemne), 0, 2)
	console.MUdskrivunsignedinteger32(uint32(SideMappeemne), 10, 2)
	console.MUdskrivunsignedinteger32(uint32(stacktop), 0, 3)
	console.MUdskrivunsignedinteger32(uint32(stackbottom), 10, 3)

	hukommelsemanager := &THukommelsemanager{}
	hukommelsemanager.Init(0, MaxqueueStørrelse)

	paging := &Paging{}
	paging.Init(SideMappeemne, 0x500000, hukommelsemanager)
	paging.SharedHukommelseregion()

	Satcr3(uint32(SideMappeemne))
	Aktiverpaging()

	shareddescriptorTabel := &TShareddescriptorTabel{}
	shareddescriptorTabel.Init()

	console.MUdskriv("esp:")

	esp := getesp()
	console.MUnsignedinteger32Udskriv(uint32(esp))

	tls := gettls()
	console.MUdskriv(([]byte)("tls:"))
	console.MUnsignedinteger32Udskriv(tls)

	tss.Installér(shareddescriptorTabel, 7, Segkerneldata, esp)

	VirtPrøv()

	cr3 := Genindlæscr3()
	console.MUdskriv(([]byte)(":cr3:"))
	console.MUnsignedinteger32Udskriv(cr3)

	cr0 := Getcr0()
	console.MUdskriv(([]byte)(":cr0:"))
	console.MUnsignedinteger32Udskriv(cr0)

	cr4 := Getcr4()
	console.MUdskriv(([]byte)(":cr4:"))
	console.MUnsignedinteger32Udskriv(cr4)

	opgavemanager_2 := &TOpgavemanager{}
	opgavemanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorTabel, opgavemanager_2)

	paging.Sidefault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(hukommelsemanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(hukommelsemanager, SideMappeemne)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, hukommelsemanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	proceshelper.Spawn(opgavea, threadhelper, sche, uint32(SideMappeemne), true)
	proceshelper.Spawn(opgaveb, threadhelper, sche, uint32(SideMappeemne), true)
	proceshelper.Spawn(opgavec, threadhelper, sche, uint32(SideMappeemne), true)
	proceshelper.Spawn(opgaved1, threadhelper, sche, uint32(SideMappeemne), true)
	proceshelper.Spawn(indgangeventOpgave, threadhelper, sche, uint32(SideMappeemne), true)

	var størrelse uint32

	var linkerFil []byte = ([]byte)("LINKER")
	størrelse = GetFilStørrelse(linkerFil)
	linkeraddress := hukommelsemanager.Malloc(størrelse)
	linkerdata := GetBytefraMarkør(uintptr(linkeraddress), int(størrelse), int(størrelse))
	LæseFil(linkerFil, linkerdata)

	elf0 := Elf{}
	linkeremne := elf0.Getemne(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SideMappeemne))

	henvisningmap := Henvisningmap{}
	henvisningmap.Init(hukommelsemanager)

	var lib1Fil []byte = ([]byte)("LIB1")
	størrelse = GetFilStørrelse(lib1Fil)

	lib1address := hukommelsemanager.Malloc(størrelse)
	lib1data := GetBytefraMarkør(uintptr(lib1address), int(størrelse), int(størrelse))
	LæseFil(lib1Fil, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SideMappeemne))
	hukommelsemanager.Fri(lib1address)

	henvisningmap.Append_to_list(uintptr(lib1elf.Dynamisk))

	var lib2Fil []byte = ([]byte)("LIB2")
	størrelse = GetFilStørrelse(lib2Fil)

	lib2address := hukommelsemanager.Malloc(størrelse)
	lib2data := GetBytefraMarkør(uintptr(lib2address), int(størrelse), int(størrelse))
	LæseFil(lib2Fil, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SideMappeemne))
	hukommelsemanager.Fri(lib2address)

	henvisningmap.Append_to_list(uintptr(lib2elf.Dynamisk))

	libHenvisningmap := henvisningmap.Clone()
	henvisningmapaddress := uint32(uintptr(Pointer(libHenvisningmap.First)))

	lib1got := Getunsignedinteger32TabelfraMarkør(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = henvisningmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TabelfraMarkør(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = henvisningmapaddress
	lib2got[2] = 0x4000000

	console.MUdskrivxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Udskriv(lib1elf.Got)
	console.MUdskriv(":")
	console.MUnsignedinteger32Udskriv(lib1elf.Dynamisk)

	console.MUdskrivxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Udskriv(lib2elf.Got)
	console.MUdskriv(":")
	console.MUnsignedinteger32Udskriv(lib2elf.Dynamisk)

	var bruger1Fil []byte = ([]byte)("USER1")
	størrelse = GetFilStørrelse(bruger1Fil)
	bruger1address := hukommelsemanager.Malloc(størrelse)
	bruger1data := GetBytefraMarkør(uintptr(bruger1address), int(størrelse), int(størrelse))
	LæseFil(bruger1Fil, bruger1data)

	elf2 := Elf{}

	bruger1emne := elf2.Getemne(bruger1data)
	elf2.Parse(bruger1data[:], uint32(SideMappeemne+0x1000))
	globaltForskydningTabel := elf2.Got

	PVærdi1Henvisningmap := henvisningmap.Clone()
	PVærdi1Henvisningmap.Append_to_list(uintptr(elf2.Dynamisk))

	hukommelsemanager.Fri(bruger1address)

	var code1Markør *uintptr
	var func1val func()

	code1Markør = (*uintptr)(hukommelsemanager.Malloc(4))
	*code1Markør = uintptr(linkeremne)
	func1val = *(*func())(Pointer(&code1Markør))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(SideMappeemne+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStatus.Ecx = bruger1emne
	thr2.CpuStatus.Edx = globaltForskydningTabel
	thr2.CpuStatus.Esi = uint32(uintptr(Pointer(PVærdi1Henvisningmap.First)))

	console.MUdskrivxy("user1: ", 1, 10)
	console.MUnsignedinteger32Udskriv(elf2.Got)

	var bruger2Fil []byte = ([]byte)("USER2")
	størrelse = GetFilStørrelse(bruger2Fil)
	bruger2address := hukommelsemanager.Malloc(størrelse)
	bruger2data := GetBytefraMarkør(uintptr(bruger2address), int(størrelse), int(størrelse))
	LæseFil(bruger2Fil, bruger2data)

	elf3 := Elf{}

	bruger2emne := elf3.Getemne(bruger2data)
	elf3.Parse(bruger2data[:], uint32(SideMappeemne+0x2000))
	globaltForskydningTabel = elf3.Got

	PVærdi2Henvisningmap := henvisningmap.Clone()
	PVærdi2Henvisningmap.Append_to_list(uintptr(elf3.Dynamisk))

	hukommelsemanager.Fri(bruger2address)

	var code2Markør *uintptr
	var func2val func()

	code2Markør = (*uintptr)(hukommelsemanager.Malloc(4))
	*code2Markør = uintptr(linkeremne)
	func2val = *(*func())(Pointer(&code2Markør))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(SideMappeemne+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStatus.Ecx = bruger2emne
	thr3.CpuStatus.Edx = globaltForskydningTabel
	thr3.CpuStatus.Esi = uint32(uintptr(Pointer(PVærdi2Henvisningmap.First)))

	console.MUdskrivxy("user2: ", 1, 11)
	console.MUnsignedinteger32Udskriv(thr3.CpuStatus.Esi)

	libHenvisningmap.Udskriv(1, 11)

	var bruger3Fil []byte = ([]byte)("USER3")
	størrelse = GetFilStørrelse(bruger3Fil)
	bruger3address := hukommelsemanager.Malloc(størrelse)
	bruger3data := GetBytefraMarkør(uintptr(bruger3address), int(størrelse), int(størrelse))
	LæseFil(bruger3Fil, bruger3data)

	elf4 := Elf{}

	bruger3emne := elf4.Getemne(bruger3data)
	elf4.Parse(bruger3data[:], uint32(SideMappeemne+0x3000))
	globaltForskydningTabel = elf4.Got

	PVærdi3Henvisningmap := henvisningmap.Clone()
	PVærdi3Henvisningmap.Append_to_list(uintptr(elf4.Dynamisk))

	hukommelsemanager.Fri(bruger3address)

	var code3Markør *uintptr
	var func3val func()

	code3Markør = (*uintptr)(hukommelsemanager.Malloc(4))
	*code3Markør = uintptr(linkeremne)
	func3val = *(*func())(Pointer(&code3Markør))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(SideMappeemne+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStatus.Ecx = bruger3emne
	thr4.CpuStatus.Edx = globaltForskydningTabel
	thr4.CpuStatus.Esi = uint32(uintptr(Pointer(PVærdi3Henvisningmap.First)))

	proceshelper.Spawn(TFunktion1, threadhelper, sche, uint32(SideMappeemne+0x4000), true)

	iTastatureventhandler = &myTastatureventhandler
	tastaturdriver.Initdriver(Interruptmanager, iTastatureventhandler)

	musdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Vælgdriver(&Drivermanager, Interruptmanager)
	enheddescriptor = mypcicontrollerhandler.Getdriver()

	sche.Aktiveret(true)
	Interruptmanager.Aktiv()

	for {
		halt()
	}

}
