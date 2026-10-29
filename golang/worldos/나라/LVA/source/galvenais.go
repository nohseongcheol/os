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
import . "pārtraukums"
import . "multitasking"
import . "tasking/tss"

import . "virtuālaAtmiņa"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/klaviatūra"
import . "driver/pele"

import . "driver/ata"
import . "failsSistēma/msdospartition"
import . "failsSistēma/fat"

import . "failsSistēma/elf"

import . "sistēmacall"

import . "atmiņamanager"
import . "pci"

func halt()

var iKlaviatūraNotikumshandler IKlaviatūraNotikumshandler

type TMyKlaviatūraNotikumshandler struct {
}

var myKlaviatūraNotikumshandler TMyKlaviatūraNotikumshandler
var klaviatūradriver TKlaviatūradriver
var peledriver TPeledriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klaviatūraconsole TConsole = TConsole{}

func (pats *TMyKlaviatūraNotikumshandler) IeslēgtsAtslēgaLejup(atslēga byte) {
	foo := [1]byte{' '}
	foo[0] = atslēga

	klaviatūraconsole.MDrukātBaitixy(foo[:], 1000, 1000)
}

func (pats *TMyKlaviatūraNotikumshandler) IeslēgtsAtslēgaAugšup(atslēga byte)	{}

var iPeleNotikumshandler IPeleNotikumshandler

type TMyPeleNotikumshandler struct {
}

var peleconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xNovietojums int16 = 0
var yNovietojums int16 = 0

func (pats *TMyPeleNotikumshandler) IeslēgtsPeleLejup(pogas int8) {
	buffer := []byte("x")
	peleconsole.MDrukātxy(buffer, uint16(previousx), uint16(previousy))
}
func (pats *TMyPeleNotikumshandler) IeslēgtsPeleAugšup(pogas int8)	{}
func (pats *TMyPeleNotikumshandler) IeslēgtsPelePārvietot(x int8, y int8) {

	xNovietojums += int16(x)
	if xNovietojums < 0 {
		xNovietojums = 0
	}
	if xNovietojums >= 80 {
		xNovietojums = 79
	}

	yNovietojums -= int16(y)

	if yNovietojums < 0 {
		yNovietojums = 0
	}
	if yNovietojums >= 25 {
		yNovietojums = 24
	}

	buffer := []byte(" ")
	peleconsole.MDrukātxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	peleconsole.MDrukātxy(buffer, uint16(xNovietojums), uint16(yNovietojums))

	previousx = xNovietojums
	previousy = yNovietojums
}

var ierīcedescriptor TPeripheralcomponentinterconnectIerīcedescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (pats TMypcicontrollerhandler) Ieslēgtsgetdriver(ierīce TPeripheralcomponentinterconnectIerīcedescriptor) {
	if ierīce.Ražotājsid == 0x1022 && ierīce.Ierīceid == 0x2000 {
		console.MDrukātxy([]byte("["), 0, 12)
		console.MDrukāt(([]byte)("AMD am79c973"))
		console.MDrukāt([]byte(":"))
		console.MUnsignedinteger16Drukāt(ierīce.Ražotājsid)
		console.MDrukāt([]byte(":"))
		console.MUnsignedinteger16Drukāt(ierīce.Ierīceid)
		console.MDrukāt([]byte(":"))
		console.MUnsignedinteger16Drukāt(uint16(ierīce.Portsbase))
		console.MDrukāt([]byte(":"))
		console.MUnsignedinteger32Drukāt(ierīce.Pārtraukums)

		console.MDrukāt([]byte("]\n"))
		ierīcedescriptor = ierīce
		drivercount++
	}
}
func (pats TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectIerīcedescriptor {
	return ierīcedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Drukātstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MDrukāt(str)
}

func GetFailsIzmērs(failanosaukums []byte) uint32 {
	var ata0s = TPaplašinātiTehnoloģijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabula{}
	partition.Lasītpartition(&ata0s)

	bios := TBiosparameterBloks32{}

	var izmērs uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums)
	ata0s.Flush()

	return izmērs
}

func LasītFails(failanosaukums []byte, data []byte) {
	var ata0s = TPaplašinātiTehnoloģijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabula{}
	partition.Lasītpartition(&ata0s)

	bios := TBiosparameterBloks32{}
	bios.Lasīt(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums, data)

	ata0s.Flush()
}
func Noslodzeelf() {

	var ata0s = TPaplašinātiTehnoloģijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabula{}
	partition.Lasītpartition(&ata0s)

	bios := TBiosparameterBloks32{}

	var failanosaukums []byte = ([]byte)("TEST")
	var izmērs uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lasīt(&ata0s, partition.Mbr.Primarypartition[0], failanosaukums, data)

	elf := Elf{}

	elf.Parse(data[:izmērs], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TFunkcija1() {
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

		SysDrukātunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ievadeNotikumstask() {
	for {
		ProcesspendingKlaviatūraevents()
		ProcesspendingPeleevents()
		halt()
	}
}

func memorytest(y int) {
	atmiņamanager := &TAtmiņamanager{}
	allocated := uint32(uintptr(atmiņamanager.Malloc(1024)))
	console.MUnsignedinteger32Drukātxy(allocated, 10, uint16(y))
	if y == 11 {
		atmiņamanager.Brīvs(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Pārlādētcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Kopacr3(cr3 uint32)
func Getcr4() uint32
func Ieslēgtpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcijaNosaukums(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNosaukums = runtime.FuncForPC(address).Name()
	var funcBaiti []byte = []byte(funcNosaukums)

	taskconsole.MDrukātxy(funcBaiti, 1, 5)
	taskconsole.MDrukāt(([]byte)(":"))
	taskconsole.MUnsignedinteger32Drukāt(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MDrukātunsignedinteger32(cr0, 2, 1)
}

var tss *Tssieraksts = &Tssieraksts{}

func KKernelEntry(LapaMapeieraksts uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MDrukāt("\n=== LVA BOOT ===\n")

	console.MDrukātunsignedinteger32(uint32(LapaMapeieraksts), 0, 2)
	console.MDrukātunsignedinteger32(uint32(LapaMapeieraksts), 10, 2)
	console.MDrukātunsignedinteger32(uint32(stacktop), 0, 3)
	console.MDrukātunsignedinteger32(uint32(stackbottom), 10, 3)

	atmiņamanager := &TAtmiņamanager{}
	atmiņamanager.Init(0, MaksqueueIzmērs)

	paging := &Paging{}
	paging.Init(LapaMapeieraksts, 0x500000, atmiņamanager)
	paging.SharedAtmiņaregion()

	Kopacr3(uint32(LapaMapeieraksts))
	Ieslēgtpaging()

	shareddescriptorTabula := &TShareddescriptorTabula{}
	shareddescriptorTabula.Init()

	console.MDrukāt("esp:")

	esp := getesp()
	console.MUnsignedinteger32Drukāt(uint32(esp))

	tls := gettls()
	console.MDrukāt(([]byte)("tls:"))
	console.MUnsignedinteger32Drukāt(tls)

	tss.Instalēt(shareddescriptorTabula, 7, Segkerneldata, esp)

	VirtPārbaudīt()

	cr3 := Pārlādētcr3()
	console.MDrukāt(([]byte)(":cr3:"))
	console.MUnsignedinteger32Drukāt(cr3)

	cr0 := Getcr0()
	console.MDrukāt(([]byte)(":cr0:"))
	console.MUnsignedinteger32Drukāt(cr0)

	cr4 := Getcr4()
	console.MDrukāt(([]byte)(":cr4:"))
	console.MUnsignedinteger32Drukāt(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Pārtraukumsmanager := &TPārtraukumsmanager{}
	Pārtraukumsmanager.Init(0x20, shareddescriptorTabula, taskmanager_2)

	paging.Lapafault(Pārtraukumsmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(atmiņamanager)

	processhelper := Processhelper{}
	processhelper.Init(atmiņamanager, LapaMapeieraksts)

	sche := &Scheduler{}
	sche.Init(Pārtraukumsmanager, atmiņamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Pārtraukumsmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(LapaMapeieraksts), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(LapaMapeieraksts), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(LapaMapeieraksts), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(LapaMapeieraksts), true)
	processhelper.Spawn(ievadeNotikumstask, threadhelper, sche, uint32(LapaMapeieraksts), true)

	var izmērs uint32

	var linkerFails []byte = ([]byte)("LINKER")
	izmērs = GetFailsIzmērs(linkerFails)
	linkeraddress := atmiņamanager.Malloc(izmērs)
	linkerdata := GetBaitifromKursors(uintptr(linkeraddress), int(izmērs), int(izmērs))
	LasītFails(linkerFails, linkerdata)

	elf0 := Elf{}
	linkerieraksts := elf0.Getieraksts(linkerdata)
	elf0.Parse(linkerdata[:], uint32(LapaMapeieraksts))

	saitemap := Saitemap{}
	saitemap.Init(atmiņamanager)

	var lib1Fails []byte = ([]byte)("LIB1")
	izmērs = GetFailsIzmērs(lib1Fails)

	lib1address := atmiņamanager.Malloc(izmērs)
	lib1data := GetBaitifromKursors(uintptr(lib1address), int(izmērs), int(izmērs))
	LasītFails(lib1Fails, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(LapaMapeieraksts))
	atmiņamanager.Brīvs(lib1address)

	saitemap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Fails []byte = ([]byte)("LIB2")
	izmērs = GetFailsIzmērs(lib2Fails)

	lib2address := atmiņamanager.Malloc(izmērs)
	lib2data := GetBaitifromKursors(uintptr(lib2address), int(izmērs), int(izmērs))
	LasītFails(lib2Fails, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(LapaMapeieraksts))
	atmiņamanager.Brīvs(lib2address)

	saitemap.Append_to_list(uintptr(lib2elf.Dynamic))

	libSaitemap := saitemap.Clone()
	saitemapaddress := uint32(uintptr(Pointer(libSaitemap.Pirmais)))

	lib1got := Getunsignedinteger32MasīvsfromKursors(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = saitemapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32MasīvsfromKursors(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = saitemapaddress
	lib2got[2] = 0x4000000

	console.MDrukātxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Drukāt(lib1elf.Got)
	console.MDrukāt(":")
	console.MUnsignedinteger32Drukāt(lib1elf.Dynamic)

	console.MDrukātxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Drukāt(lib2elf.Got)
	console.MDrukāt(":")
	console.MUnsignedinteger32Drukāt(lib2elf.Dynamic)

	var lietotājs1Fails []byte = ([]byte)("USER1")
	izmērs = GetFailsIzmērs(lietotājs1Fails)
	lietotājs1address := atmiņamanager.Malloc(izmērs)
	lietotājs1data := GetBaitifromKursors(uintptr(lietotājs1address), int(izmērs), int(izmērs))
	LasītFails(lietotājs1Fails, lietotājs1data)

	elf2 := Elf{}

	lietotājs1ieraksts := elf2.Getieraksts(lietotājs1data)
	elf2.Parse(lietotājs1data[:], uint32(LapaMapeieraksts+0x1000))
	globālaisoffsetTabula := elf2.Got

	PVērtība1Saitemap := saitemap.Clone()
	PVērtība1Saitemap.Append_to_list(uintptr(elf2.Dynamic))

	atmiņamanager.Brīvs(lietotājs1address)

	var code1Kursors *uintptr
	var func1val func()

	code1Kursors = (*uintptr)(atmiņamanager.Malloc(4))
	*code1Kursors = uintptr(linkerieraksts)
	func1val = *(*func())(Pointer(&code1Kursors))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(LapaMapeieraksts+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStāvoklis.Ecx = lietotājs1ieraksts
	thr2.CpuStāvoklis.Edx = globālaisoffsetTabula
	thr2.CpuStāvoklis.Esi = uint32(uintptr(Pointer(PVērtība1Saitemap.Pirmais)))

	console.MDrukātxy("user1: ", 1, 10)
	console.MUnsignedinteger32Drukāt(elf2.Got)

	var lietotājs2Fails []byte = ([]byte)("USER2")
	izmērs = GetFailsIzmērs(lietotājs2Fails)
	lietotājs2address := atmiņamanager.Malloc(izmērs)
	lietotājs2data := GetBaitifromKursors(uintptr(lietotājs2address), int(izmērs), int(izmērs))
	LasītFails(lietotājs2Fails, lietotājs2data)

	elf3 := Elf{}

	lietotājs2ieraksts := elf3.Getieraksts(lietotājs2data)
	elf3.Parse(lietotājs2data[:], uint32(LapaMapeieraksts+0x2000))
	globālaisoffsetTabula = elf3.Got

	PVērtība2Saitemap := saitemap.Clone()
	PVērtība2Saitemap.Append_to_list(uintptr(elf3.Dynamic))

	atmiņamanager.Brīvs(lietotājs2address)

	var code2Kursors *uintptr
	var func2val func()

	code2Kursors = (*uintptr)(atmiņamanager.Malloc(4))
	*code2Kursors = uintptr(linkerieraksts)
	func2val = *(*func())(Pointer(&code2Kursors))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(LapaMapeieraksts+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStāvoklis.Ecx = lietotājs2ieraksts
	thr3.CpuStāvoklis.Edx = globālaisoffsetTabula
	thr3.CpuStāvoklis.Esi = uint32(uintptr(Pointer(PVērtība2Saitemap.Pirmais)))

	console.MDrukātxy("user2: ", 1, 11)
	console.MUnsignedinteger32Drukāt(thr3.CpuStāvoklis.Esi)

	libSaitemap.Drukāt(1, 11)

	var lietotājs3Fails []byte = ([]byte)("USER3")
	izmērs = GetFailsIzmērs(lietotājs3Fails)
	lietotājs3address := atmiņamanager.Malloc(izmērs)
	lietotājs3data := GetBaitifromKursors(uintptr(lietotājs3address), int(izmērs), int(izmērs))
	LasītFails(lietotājs3Fails, lietotājs3data)

	elf4 := Elf{}

	lietotājs3ieraksts := elf4.Getieraksts(lietotājs3data)
	elf4.Parse(lietotājs3data[:], uint32(LapaMapeieraksts+0x3000))
	globālaisoffsetTabula = elf4.Got

	PVērtība3Saitemap := saitemap.Clone()
	PVērtība3Saitemap.Append_to_list(uintptr(elf4.Dynamic))

	atmiņamanager.Brīvs(lietotājs3address)

	var code3Kursors *uintptr
	var func3val func()

	code3Kursors = (*uintptr)(atmiņamanager.Malloc(4))
	*code3Kursors = uintptr(linkerieraksts)
	func3val = *(*func())(Pointer(&code3Kursors))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(LapaMapeieraksts+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStāvoklis.Ecx = lietotājs3ieraksts
	thr4.CpuStāvoklis.Edx = globālaisoffsetTabula
	thr4.CpuStāvoklis.Esi = uint32(uintptr(Pointer(PVērtība3Saitemap.Pirmais)))

	processhelper.Spawn(TFunkcija1, threadhelper, sche, uint32(LapaMapeieraksts+0x4000), true)

	iKlaviatūraNotikumshandler = &myKlaviatūraNotikumshandler
	klaviatūradriver.Initdriver(Pārtraukumsmanager, iKlaviatūraNotikumshandler)

	peledriver.Initdriver(Pārtraukumsmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Atlasītdriver(&Drivermanager, Pārtraukumsmanager)
	ierīcedescriptor = mypcicontrollerhandler.Getdriver()

	sche.Ieslēgt(true)
	Pārtraukumsmanager.Aktīvs()

	for {
		halt()
	}

}
