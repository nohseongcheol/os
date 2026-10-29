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
import . "intrerupere"
import . "multitasking"
import . "tasking/tss"

import . "virtualăMemorie"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/tastatură"
import . "driver/maus"

import . "driver/ata"
import . "fișierSistem/msdospartition"
import . "fișierSistem/fat"

import . "fișierSistem/elf"

import . "sistemcall"

import . "memoriemanager"
import . "pci"

func halt()

var iTastaturăEvenimenthandler ITastaturăEvenimenthandler

type TMyTastaturăEvenimenthandler struct {
}

var myTastaturăEvenimenthandler TMyTastaturăEvenimenthandler
var tastaturădriver TTastaturădriver
var mausdriver TMausdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastaturăconsole TConsole = TConsole{}

func (sine *TMyTastaturăEvenimenthandler) PornitCheieÎnjos(cheie byte) {
	foo := [1]byte{' '}
	foo[0] = cheie

	tastaturăconsole.MTipăreșteOctețixy(foo[:], 1000, 1000)
}

func (sine *TMyTastaturăEvenimenthandler) PornitCheieSus(cheie byte)	{}

var iMausEvenimenthandler IMausEvenimenthandler

type TMyMausEvenimenthandler struct {
}

var mausconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPoziție int16 = 0
var yPoziție int16 = 0

func (sine *TMyMausEvenimenthandler) PornitMausÎnjos(buton int8) {
	buffer := []byte("x")
	mausconsole.MTipăreștexy(buffer, uint16(previousx), uint16(previousy))
}
func (sine *TMyMausEvenimenthandler) PornitMausSus(buton int8)	{}
func (sine *TMyMausEvenimenthandler) PornitMausMutare(x int8, y int8) {

	xPoziție += int16(x)
	if xPoziție < 0 {
		xPoziție = 0
	}
	if xPoziție >= 80 {
		xPoziție = 79
	}

	yPoziție -= int16(y)

	if yPoziție < 0 {
		yPoziție = 0
	}
	if yPoziție >= 25 {
		yPoziție = 24
	}

	buffer := []byte(" ")
	mausconsole.MTipăreștexy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mausconsole.MTipăreștexy(buffer, uint16(xPoziție), uint16(yPoziție))

	previousx = xPoziție
	previousy = yPoziție
}

var dispozitivdescriptor TPeripheralcomponentinterconnectDispozitivdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (sine TMypcicontrollerhandler) Pornitgetdriver(dispozitiv TPeripheralcomponentinterconnectDispozitivdescriptor) {
	if dispozitiv.Comerciantid == 0x1022 && dispozitiv.Dispozitivid == 0x2000 {
		console.MTipăreștexy([]byte("["), 0, 12)
		console.MTipărește(([]byte)("AMD am79c973"))
		console.MTipărește([]byte(":"))
		console.MUnsignedinteger16Tipărește(dispozitiv.Comerciantid)
		console.MTipărește([]byte(":"))
		console.MUnsignedinteger16Tipărește(dispozitiv.Dispozitivid)
		console.MTipărește([]byte(":"))
		console.MUnsignedinteger16Tipărește(uint16(dispozitiv.Portbase))
		console.MTipărește([]byte(":"))
		console.MUnsignedinteger32Tipărește(dispozitiv.Intrerupere)

		console.MTipărește([]byte("]\n"))
		dispozitivdescriptor = dispozitiv
		drivercount++
	}
}
func (sine TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectDispozitivdescriptor {
	return dispozitivdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Tipăreștestr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MTipărește(str)
}

func GetFișierMărime(numefișier []byte) uint32 {
	var ata0s = TAvansateTehnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Citirepartition(&ata0s)

	bios := TBiosparameterBloc32{}

	var mărime uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], numefișier)
	ata0s.Flush()

	return mărime
}

func CitireFișier(numefișier []byte, data []byte) {
	var ata0s = TAvansateTehnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Citirepartition(&ata0s)

	bios := TBiosparameterBloc32{}
	bios.Citire(&ata0s, partition.Mbr.Primarypartition[0], numefișier, data)

	ata0s.Flush()
}
func Încărcareelf() {

	var ata0s = TAvansateTehnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Citirepartition(&ata0s)

	bios := TBiosparameterBloc32{}

	var numefișier []byte = ([]byte)("TEST")
	var mărime uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], numefișier)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Citire(&ata0s, partition.Mbr.Primarypartition[0], numefișier, data)

	elf := Elf{}

	elf.Parse(data[:mărime], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TFuncție1() {
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

		SysTipăreșteunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func introducețiEvenimenttask() {
	for {
		ProcespendingTastaturăevents()
		ProcespendingMausevents()
		halt()
	}
}

func memorytest(y int) {
	memoriemanager := &TMemoriemanager{}
	allocated := uint32(uintptr(memoriemanager.Malloc(1024)))
	console.MUnsignedinteger32Tipăreștexy(allocated, 10, uint16(y))
	if y == 11 {
		memoriemanager.Liber(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzăloop()
func Reîncarcăcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Definitcr3(cr3 uint32)
func Getcr4() uint32
func Activeazăpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFuncțieNume(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNume = runtime.FuncForPC(address).Name()
	var funcOcteți []byte = []byte(funcNume)

	taskconsole.MTipăreștexy(funcOcteți, 1, 5)
	taskconsole.MTipărește(([]byte)(":"))
	taskconsole.MUnsignedinteger32Tipărește(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MTipăreșteunsignedinteger32(cr0, 2, 1)
}

var tss *Tssînregistrare = &Tssînregistrare{}

func KKernelEntry(PAGINĂDirectorînregistrare uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerieloginit()
	console.MTipărește("\n=== MDA BOOT ===\n")

	console.MTipăreșteunsignedinteger32(uint32(PAGINĂDirectorînregistrare), 0, 2)
	console.MTipăreșteunsignedinteger32(uint32(PAGINĂDirectorînregistrare), 10, 2)
	console.MTipăreșteunsignedinteger32(uint32(stacktop), 0, 3)
	console.MTipăreșteunsignedinteger32(uint32(stackbottom), 10, 3)

	memoriemanager := &TMemoriemanager{}
	memoriemanager.Init(0, MaxqueueMărime)

	paging := &Paging{}
	paging.Init(PAGINĂDirectorînregistrare, 0x500000, memoriemanager)
	paging.SharedMemorieregion()

	Definitcr3(uint32(PAGINĂDirectorînregistrare))
	Activeazăpaging()

	shareddescriptorTabel := &TShareddescriptorTabel{}
	shareddescriptorTabel.Init()

	console.MTipărește("esp:")

	esp := getesp()
	console.MUnsignedinteger32Tipărește(uint32(esp))

	tls := gettls()
	console.MTipărește(([]byte)("tls:"))
	console.MUnsignedinteger32Tipărește(tls)

	tss.Instalează(shareddescriptorTabel, 7, Segkerneldata, esp)

	VirtTestează()

	cr3 := Reîncarcăcr3()
	console.MTipărește(([]byte)(":cr3:"))
	console.MUnsignedinteger32Tipărește(cr3)

	cr0 := Getcr0()
	console.MTipărește(([]byte)(":cr0:"))
	console.MUnsignedinteger32Tipărește(cr0)

	cr4 := Getcr4()
	console.MTipărește(([]byte)(":cr4:"))
	console.MUnsignedinteger32Tipărește(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Intreruperemanager := &TIntreruperemanager{}
	Intreruperemanager.Init(0x20, shareddescriptorTabel, taskmanager_2)

	paging.PAGINĂfault(Intreruperemanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memoriemanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(memoriemanager, PAGINĂDirectorînregistrare)

	sche := &Scheduler{}
	sche.Init(Intreruperemanager, memoriemanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Intreruperemanager)

	proceshelper.Spawn(taska, threadhelper, sche, uint32(PAGINĂDirectorînregistrare), true)
	proceshelper.Spawn(taskb, threadhelper, sche, uint32(PAGINĂDirectorînregistrare), true)
	proceshelper.Spawn(taskc, threadhelper, sche, uint32(PAGINĂDirectorînregistrare), true)
	proceshelper.Spawn(taskd1, threadhelper, sche, uint32(PAGINĂDirectorînregistrare), true)
	proceshelper.Spawn(introducețiEvenimenttask, threadhelper, sche, uint32(PAGINĂDirectorînregistrare), true)

	var mărime uint32

	var linkerFișier []byte = ([]byte)("LINKER")
	mărime = GetFișierMărime(linkerFișier)
	linkeraddress := memoriemanager.Malloc(mărime)
	linkerdata := GetOctețifromIndicator(uintptr(linkeraddress), int(mărime), int(mărime))
	CitireFișier(linkerFișier, linkerdata)

	elf0 := Elf{}
	linkerînregistrare := elf0.Getînregistrare(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PAGINĂDirectorînregistrare))

	legăturămap := Legăturămap{}
	legăturămap.Init(memoriemanager)

	var lib1Fișier []byte = ([]byte)("LIB1")
	mărime = GetFișierMărime(lib1Fișier)

	lib1address := memoriemanager.Malloc(mărime)
	lib1data := GetOctețifromIndicator(uintptr(lib1address), int(mărime), int(mărime))
	CitireFișier(lib1Fișier, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PAGINĂDirectorînregistrare))
	memoriemanager.Liber(lib1address)

	legăturămap.Append_to_list(uintptr(lib1elf.Dinamică))

	var lib2Fișier []byte = ([]byte)("LIB2")
	mărime = GetFișierMărime(lib2Fișier)

	lib2address := memoriemanager.Malloc(mărime)
	lib2data := GetOctețifromIndicator(uintptr(lib2address), int(mărime), int(mărime))
	CitireFișier(lib2Fișier, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PAGINĂDirectorînregistrare))
	memoriemanager.Liber(lib2address)

	legăturămap.Append_to_list(uintptr(lib2elf.Dinamică))

	libLegăturămap := legăturămap.Clone()
	legăturămapaddress := uint32(uintptr(Pointer(libLegăturămap.First)))

	lib1got := Getunsignedinteger32VectorfromIndicator(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = legăturămapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32VectorfromIndicator(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = legăturămapaddress
	lib2got[2] = 0x4000000

	console.MTipăreștexy("lib1: ", 1, 8)
	console.MUnsignedinteger32Tipărește(lib1elf.Got)
	console.MTipărește(":")
	console.MUnsignedinteger32Tipărește(lib1elf.Dinamică)

	console.MTipăreștexy("lib2: ", 1, 9)
	console.MUnsignedinteger32Tipărește(lib2elf.Got)
	console.MTipărește(":")
	console.MUnsignedinteger32Tipărește(lib2elf.Dinamică)

	var utilizator1Fișier []byte = ([]byte)("USER1")
	mărime = GetFișierMărime(utilizator1Fișier)
	utilizator1address := memoriemanager.Malloc(mărime)
	utilizator1data := GetOctețifromIndicator(uintptr(utilizator1address), int(mărime), int(mărime))
	CitireFișier(utilizator1Fișier, utilizator1data)

	elf2 := Elf{}

	utilizator1înregistrare := elf2.Getînregistrare(utilizator1data)
	elf2.Parse(utilizator1data[:], uint32(PAGINĂDirectorînregistrare+0x1000))
	globaloffsetTabel := elf2.Got

	PValoare1Legăturămap := legăturămap.Clone()
	PValoare1Legăturămap.Append_to_list(uintptr(elf2.Dinamică))

	memoriemanager.Liber(utilizator1address)

	var code1Indicator *uintptr
	var func1val func()

	code1Indicator = (*uintptr)(memoriemanager.Malloc(4))
	*code1Indicator = uintptr(linkerînregistrare)
	func1val = *(*func())(Pointer(&code1Indicator))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(PAGINĂDirectorînregistrare+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStare.Ecx = utilizator1înregistrare
	thr2.CpuStare.Edx = globaloffsetTabel
	thr2.CpuStare.Esi = uint32(uintptr(Pointer(PValoare1Legăturămap.First)))

	console.MTipăreștexy("user1: ", 1, 10)
	console.MUnsignedinteger32Tipărește(elf2.Got)

	var utilizator2Fișier []byte = ([]byte)("USER2")
	mărime = GetFișierMărime(utilizator2Fișier)
	utilizator2address := memoriemanager.Malloc(mărime)
	utilizator2data := GetOctețifromIndicator(uintptr(utilizator2address), int(mărime), int(mărime))
	CitireFișier(utilizator2Fișier, utilizator2data)

	elf3 := Elf{}

	utilizator2înregistrare := elf3.Getînregistrare(utilizator2data)
	elf3.Parse(utilizator2data[:], uint32(PAGINĂDirectorînregistrare+0x2000))
	globaloffsetTabel = elf3.Got

	PValoare2Legăturămap := legăturămap.Clone()
	PValoare2Legăturămap.Append_to_list(uintptr(elf3.Dinamică))

	memoriemanager.Liber(utilizator2address)

	var code2Indicator *uintptr
	var func2val func()

	code2Indicator = (*uintptr)(memoriemanager.Malloc(4))
	*code2Indicator = uintptr(linkerînregistrare)
	func2val = *(*func())(Pointer(&code2Indicator))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(PAGINĂDirectorînregistrare+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStare.Ecx = utilizator2înregistrare
	thr3.CpuStare.Edx = globaloffsetTabel
	thr3.CpuStare.Esi = uint32(uintptr(Pointer(PValoare2Legăturămap.First)))

	console.MTipăreștexy("user2: ", 1, 11)
	console.MUnsignedinteger32Tipărește(thr3.CpuStare.Esi)

	libLegăturămap.Tipărește(1, 11)

	var utilizator3Fișier []byte = ([]byte)("USER3")
	mărime = GetFișierMărime(utilizator3Fișier)
	utilizator3address := memoriemanager.Malloc(mărime)
	utilizator3data := GetOctețifromIndicator(uintptr(utilizator3address), int(mărime), int(mărime))
	CitireFișier(utilizator3Fișier, utilizator3data)

	elf4 := Elf{}

	utilizator3înregistrare := elf4.Getînregistrare(utilizator3data)
	elf4.Parse(utilizator3data[:], uint32(PAGINĂDirectorînregistrare+0x3000))
	globaloffsetTabel = elf4.Got

	PValoare3Legăturămap := legăturămap.Clone()
	PValoare3Legăturămap.Append_to_list(uintptr(elf4.Dinamică))

	memoriemanager.Liber(utilizator3address)

	var code3Indicator *uintptr
	var func3val func()

	code3Indicator = (*uintptr)(memoriemanager.Malloc(4))
	*code3Indicator = uintptr(linkerînregistrare)
	func3val = *(*func())(Pointer(&code3Indicator))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(PAGINĂDirectorînregistrare+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStare.Ecx = utilizator3înregistrare
	thr4.CpuStare.Edx = globaloffsetTabel
	thr4.CpuStare.Esi = uint32(uintptr(Pointer(PValoare3Legăturămap.First)))

	proceshelper.Spawn(TFuncție1, threadhelper, sche, uint32(PAGINĂDirectorînregistrare+0x4000), true)

	iTastaturăEvenimenthandler = &myTastaturăEvenimenthandler
	tastaturădriver.Initdriver(Intreruperemanager, iTastaturăEvenimenthandler)

	mausdriver.Initdriver(Intreruperemanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selecteazădriver(&Drivermanager, Intreruperemanager)
	dispozitivdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Activat(true)
	Intreruperemanager.Activ()

	for {
		halt()
	}

}
