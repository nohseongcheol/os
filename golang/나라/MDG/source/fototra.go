package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsoly"
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtualArika"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/fafanteny"
import . "driver/totozy"

import . "driver/ata"
import . "rakitraRafitra/msdospartition"
import . "rakitraRafitra/fat"

import . "rakitraRafitra/elf"

import . "rafitracall"

import . "arikaMpandrindra"
import . "pci"

func halt()

var iFafantenyeventhandler IFafantenyeventhandler

type TMyFafantenyeventhandler struct {
}

var myFafantenyeventhandler TMyFafantenyeventhandler
var fafantenydriver TFafantenydriver
var totozydriver TTotozydriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var fafantenyKonsoly TKonsoly = TKonsoly{}

func (nytena *TMyFafantenyeventhandler) Onkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	fafantenyKonsoly.MAtontayOctetxy(foo[:], 1000, 1000)
}

func (nytena *TMyFafantenyeventhandler) OnkeyAmbony(key byte)	{}

var iTotozyeventhandler ITotozyeventhandler

type TMyTotozyeventhandler struct {
}

var totozyKonsoly TKonsoly = TKonsoly{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (nytena *TMyTotozyeventhandler) OnTotozydown(button int8) {
	buffer := []byte("x")
	totozyKonsoly.MAtontayxy(buffer, uint16(previousx), uint16(previousy))
}
func (nytena *TMyTotozyeventhandler) OnTotozyAmbony(button int8)	{}
func (nytena *TMyTotozyeventhandler) OnTotozyAfindrao(x int8, y int8) {

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
	totozyKonsoly.MAtontayxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	totozyKonsoly.MAtontayxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var periferikadescriptor TPeripheralcomponentinterconnectPeriferikadescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var konsoly TKonsoly = TKonsoly{}
var drivercount uint16 = 0

func (nytena TMypcicontrollerhandler) Ongetdriver(periferika TPeripheralcomponentinterconnectPeriferikadescriptor) {
	if periferika.Vendorid == 0x1022 && periferika.Periferikaid == 0x2000 {
		konsoly.MAtontayxy([]byte("["), 0, 12)
		konsoly.MAtontay(([]byte)("AMD am79c973"))
		konsoly.MAtontay([]byte(":"))
		konsoly.MUnsignedinteger16Atontay(periferika.Vendorid)
		konsoly.MAtontay([]byte(":"))
		konsoly.MUnsignedinteger16Atontay(periferika.Periferikaid)
		konsoly.MAtontay([]byte(":"))
		konsoly.MUnsignedinteger16Atontay(uint16(periferika.Irikabase))
		konsoly.MAtontay([]byte(":"))
		konsoly.MUnsignedinteger32Atontay(periferika.Interrupt)

		konsoly.MAtontay([]byte("]\n"))
		periferikadescriptor = periferika
		drivercount++
	}
}
func (nytena TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectPeriferikadescriptor {
	return periferikadescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Atontaystr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsoly.MAtontay(str)
}

func GetRakitraHabe(anarandrakitra []byte) uint32 {
	var ata0s = TAvolentatechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionFafana{}
	partition.Mamakypartition(&ata0s)

	bios := TBiosparameterblock32{}

	var habe uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra)
	ata0s.Flush()

	return habe
}

func MamakyRakitra(anarandrakitra []byte, data []byte) {
	var ata0s = TAvolentatechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionFafana{}
	partition.Mamakypartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Mamaky(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra, data)

	ata0s.Flush()
}
func Vesatraelf() {

	var ata0s = TAvolentatechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionFafana{}
	partition.Mamakypartition(&ata0s)

	bios := TBiosparameterblock32{}

	var anarandrakitra []byte = ([]byte)("TEST")
	var habe uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Mamaky(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra, data)

	elf := Elf{}

	elf.Parse(data[:habe], 0x4f00000)

}

var taskKonsoly TKonsoly = TKonsoly{}

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

		SysAtontayunsignedinteger32(esi)

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
		ProcesspendingFafantenyevents()
		ProcesspendingTotozyevents()
		halt()
	}
}

func memorytest(y int) {
	arikaMpandrindra := &TArikaMpandrindra{}
	allocated := uint32(uintptr(arikaMpandrindra.Malloc(1024)))
	konsoly.MUnsignedinteger32Atontayxy(allocated, 10, uint16(y))
	if y == 11 {
		arikaMpandrindra.Malalaka(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Averenoasehocr3() uint32

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

func GetfunctionAnarana(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcAnarana = runtime.FuncForPC(address).Name()
	var funcOctet []byte = []byte(funcAnarana)

	taskKonsoly.MAtontayxy(funcOctet, 1, 5)
	taskKonsoly.MAtontay(([]byte)(":"))
	taskKonsoly.MUnsignedinteger32Atontay(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskKonsoly.MAtontayunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(PEJYLahatahiryentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	konsoly.MAtontay("\n=== MDG BOOT ===\n")

	konsoly.MAtontayunsignedinteger32(uint32(PEJYLahatahiryentry), 0, 2)
	konsoly.MAtontayunsignedinteger32(uint32(PEJYLahatahiryentry), 10, 2)
	konsoly.MAtontayunsignedinteger32(uint32(stacktop), 0, 3)
	konsoly.MAtontayunsignedinteger32(uint32(stackbottom), 10, 3)

	arikaMpandrindra := &TArikaMpandrindra{}
	arikaMpandrindra.Init(0, MaxqueueHabe)

	paging := &Paging{}
	paging.Init(PEJYLahatahiryentry, 0x500000, arikaMpandrindra)
	paging.SharedArikaregion()

	Setcr3(uint32(PEJYLahatahiryentry))
	Enablepaging()

	shareddescriptorFafana := &TShareddescriptorFafana{}
	shareddescriptorFafana.Init()

	konsoly.MAtontay("esp:")

	esp := getesp()
	konsoly.MUnsignedinteger32Atontay(uint32(esp))

	tls := gettls()
	konsoly.MAtontay(([]byte)("tls:"))
	konsoly.MUnsignedinteger32Atontay(tls)

	tss.Hametraka(shareddescriptorFafana, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Averenoasehocr3()
	konsoly.MAtontay(([]byte)(":cr3:"))
	konsoly.MUnsignedinteger32Atontay(cr3)

	cr0 := Getcr0()
	konsoly.MAtontay(([]byte)(":cr0:"))
	konsoly.MUnsignedinteger32Atontay(cr0)

	cr4 := Getcr4()
	konsoly.MAtontay(([]byte)(":cr4:"))
	konsoly.MUnsignedinteger32Atontay(cr4)

	taskMpandrindra_2 := &TTaskMpandrindra{}
	taskMpandrindra_2.Init()

	InterruptMpandrindra := &TInterruptMpandrindra{}
	InterruptMpandrindra.Init(0x20, shareddescriptorFafana, taskMpandrindra_2)

	paging.PEJYfault(InterruptMpandrindra)

	DriverMpandrindra := TDriverMpandrindra{}
	DriverMpandrindra.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(arikaMpandrindra)

	processhelper := Processhelper{}
	processhelper.Init(arikaMpandrindra, PEJYLahatahiryentry)

	sche := &Scheduler{}
	sche.Init(InterruptMpandrindra, arikaMpandrindra, tss)

	syscall := &TSyscall{}
	syscall.Init(InterruptMpandrindra)

	processhelper.Spawn(taska, threadhelper, sche, uint32(PEJYLahatahiryentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(PEJYLahatahiryentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(PEJYLahatahiryentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(PEJYLahatahiryentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(PEJYLahatahiryentry), true)

	var habe uint32

	var linkerRakitra []byte = ([]byte)("LINKER")
	habe = GetRakitraHabe(linkerRakitra)
	linkeraddress := arikaMpandrindra.Malloc(habe)
	linkerdata := GetOctetfrompointer(uintptr(linkeraddress), int(habe), int(habe))
	MamakyRakitra(linkerRakitra, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PEJYLahatahiryentry))

	rohymap := Rohymap{}
	rohymap.Init(arikaMpandrindra)

	var lib1Rakitra []byte = ([]byte)("LIB1")
	habe = GetRakitraHabe(lib1Rakitra)

	lib1address := arikaMpandrindra.Malloc(habe)
	lib1data := GetOctetfrompointer(uintptr(lib1address), int(habe), int(habe))
	MamakyRakitra(lib1Rakitra, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PEJYLahatahiryentry))
	arikaMpandrindra.Malalaka(lib1address)

	rohymap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Rakitra []byte = ([]byte)("LIB2")
	habe = GetRakitraHabe(lib2Rakitra)

	lib2address := arikaMpandrindra.Malloc(habe)
	lib2data := GetOctetfrompointer(uintptr(lib2address), int(habe), int(habe))
	MamakyRakitra(lib2Rakitra, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PEJYLahatahiryentry))
	arikaMpandrindra.Malalaka(lib2address)

	rohymap.Append_to_list(uintptr(lib2elf.Dynamic))

	librohymap := rohymap.Clone()
	rohymapaddress := uint32(uintptr(Pointer(librohymap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = rohymapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = rohymapaddress
	lib2got[2] = 0x4000000

	konsoly.MAtontayxy("lib1: ", 1, 8)
	konsoly.MUnsignedinteger32Atontay(lib1elf.Got)
	konsoly.MAtontay(":")
	konsoly.MUnsignedinteger32Atontay(lib1elf.Dynamic)

	konsoly.MAtontayxy("lib2: ", 1, 9)
	konsoly.MUnsignedinteger32Atontay(lib2elf.Got)
	konsoly.MAtontay(":")
	konsoly.MUnsignedinteger32Atontay(lib2elf.Dynamic)

	var mpampiasa1Rakitra []byte = ([]byte)("USER1")
	habe = GetRakitraHabe(mpampiasa1Rakitra)
	mpampiasa1address := arikaMpandrindra.Malloc(habe)
	mpampiasa1data := GetOctetfrompointer(uintptr(mpampiasa1address), int(habe), int(habe))
	MamakyRakitra(mpampiasa1Rakitra, mpampiasa1data)

	elf2 := Elf{}

	mpampiasa1entry := elf2.Getentry(mpampiasa1data)
	elf2.Parse(mpampiasa1data[:], uint32(PEJYLahatahiryentry+0x1000))
	globaloffsetFafana := elf2.Got

	PSanda1rohymap := rohymap.Clone()
	PSanda1rohymap.Append_to_list(uintptr(elf2.Dynamic))

	arikaMpandrindra.Malalaka(mpampiasa1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(arikaMpandrindra.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(PEJYLahatahiryentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = mpampiasa1entry
	thr2.Cpustate.Edx = globaloffsetFafana
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PSanda1rohymap.First)))

	konsoly.MAtontayxy("user1: ", 1, 10)
	konsoly.MUnsignedinteger32Atontay(elf2.Got)

	var mpampiasa2Rakitra []byte = ([]byte)("USER2")
	habe = GetRakitraHabe(mpampiasa2Rakitra)
	mpampiasa2address := arikaMpandrindra.Malloc(habe)
	mpampiasa2data := GetOctetfrompointer(uintptr(mpampiasa2address), int(habe), int(habe))
	MamakyRakitra(mpampiasa2Rakitra, mpampiasa2data)

	elf3 := Elf{}

	mpampiasa2entry := elf3.Getentry(mpampiasa2data)
	elf3.Parse(mpampiasa2data[:], uint32(PEJYLahatahiryentry+0x2000))
	globaloffsetFafana = elf3.Got

	PSanda2rohymap := rohymap.Clone()
	PSanda2rohymap.Append_to_list(uintptr(elf3.Dynamic))

	arikaMpandrindra.Malalaka(mpampiasa2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(arikaMpandrindra.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(PEJYLahatahiryentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = mpampiasa2entry
	thr3.Cpustate.Edx = globaloffsetFafana
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PSanda2rohymap.First)))

	konsoly.MAtontayxy("user2: ", 1, 11)
	konsoly.MUnsignedinteger32Atontay(thr3.Cpustate.Esi)

	librohymap.Atontay(1, 11)

	var mpampiasa3Rakitra []byte = ([]byte)("USER3")
	habe = GetRakitraHabe(mpampiasa3Rakitra)
	mpampiasa3address := arikaMpandrindra.Malloc(habe)
	mpampiasa3data := GetOctetfrompointer(uintptr(mpampiasa3address), int(habe), int(habe))
	MamakyRakitra(mpampiasa3Rakitra, mpampiasa3data)

	elf4 := Elf{}

	mpampiasa3entry := elf4.Getentry(mpampiasa3data)
	elf4.Parse(mpampiasa3data[:], uint32(PEJYLahatahiryentry+0x3000))
	globaloffsetFafana = elf4.Got

	PSanda3rohymap := rohymap.Clone()
	PSanda3rohymap.Append_to_list(uintptr(elf4.Dynamic))

	arikaMpandrindra.Malalaka(mpampiasa3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(arikaMpandrindra.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(PEJYLahatahiryentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = mpampiasa3entry
	thr4.Cpustate.Edx = globaloffsetFafana
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PSanda3rohymap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(PEJYLahatahiryentry+0x4000), true)

	iFafantenyeventhandler = &myFafantenyeventhandler
	fafantenydriver.Initdriver(InterruptMpandrindra, iFafantenyeventhandler)

	totozydriver.Initdriver(InterruptMpandrindra, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&DriverMpandrindra, InterruptMpandrindra)
	periferikadescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	InterruptMpandrindra.Miasa()

	for {
		halt()
	}

}
