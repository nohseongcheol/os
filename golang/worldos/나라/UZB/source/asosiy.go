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

import . "virtualXotira"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/jarayon"
import . "driver/driver"

import . "driver/klaviatura"
import . "driver/sichqoncha"

import . "driver/ata"
import . "faylTizim/msdospartition"
import . "faylTizim/fat"

import . "faylTizim/elf"

import . "tizimcall"

import . "xotiramanager"
import . "pci"

func halt()

var iKlaviaturaeventhandler IKlaviaturaeventhandler

type TMyKlaviaturaeventhandler struct {
}

var myKlaviaturaeventhandler TMyKlaviaturaeventhandler
var klaviaturadriver TKlaviaturadriver
var sichqonchadriver TSichqonchadriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klaviaturaconsole TConsole = TConsole{}

func (self *TMyKlaviaturaeventhandler) YoqishKalitPastga(kalit byte) {
	foo := [1]byte{' '}
	foo[0] = kalit

	klaviaturaconsole.MChopetishBaytlarxy(foo[:], 1000, 1000)
}

func (self *TMyKlaviaturaeventhandler) YoqishKalitYuqoriga(kalit byte)	{}

var iSichqonchaeventhandler ISichqonchaeventhandler

type TMySichqonchaeventhandler struct {
}

var sichqonchaconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xHolati int16 = 0
var yHolati int16 = 0

func (self *TMySichqonchaeventhandler) YoqishSichqonchaPastga(tugma int8) {
	buffer := []byte("x")
	sichqonchaconsole.MChopetishxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMySichqonchaeventhandler) YoqishSichqonchaYuqoriga(tugma int8)	{}
func (self *TMySichqonchaeventhandler) YoqishSichqonchaKoʻchirish(x int8, y int8) {

	xHolati += int16(x)
	if xHolati < 0 {
		xHolati = 0
	}
	if xHolati >= 80 {
		xHolati = 79
	}

	yHolati -= int16(y)

	if yHolati < 0 {
		yHolati = 0
	}
	if yHolati >= 25 {
		yHolati = 24
	}

	buffer := []byte(" ")
	sichqonchaconsole.MChopetishxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	sichqonchaconsole.MChopetishxy(buffer, uint16(xHolati), uint16(yHolati))

	previousx = xHolati
	previousy = yHolati
}

var uskunadescriptor TPeripheralcomponentinterconnectUskunadescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Yoqishgetdriver(uskuna TPeripheralcomponentinterconnectUskunadescriptor) {
	if uskuna.Ishlabchiqaruvchiid == 0x1022 && uskuna.Uskunaid == 0x2000 {
		console.MChopetishxy([]byte("["), 0, 12)
		console.MChopetish(([]byte)("AMD am79c973"))
		console.MChopetish([]byte(":"))
		console.MUnsignedinteger16Chopetish(uskuna.Ishlabchiqaruvchiid)
		console.MChopetish([]byte(":"))
		console.MUnsignedinteger16Chopetish(uskuna.Uskunaid)
		console.MChopetish([]byte(":"))
		console.MUnsignedinteger16Chopetish(uint16(uskuna.Portbase))
		console.MChopetish([]byte(":"))
		console.MUnsignedinteger32Chopetish(uskuna.Interrupt)

		console.MChopetish([]byte("]\n"))
		uskunadescriptor = uskuna
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectUskunadescriptor {
	return uskunadescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Chopetishstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MChopetish(str)
}

func GetFaylHajmi(faylnomi []byte) uint32 {
	var ata0s = TMurakkabTexnologiyaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oʻqishpartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var hajmi uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faylnomi)
	ata0s.Flush()

	return hajmi
}

func OʻqishFayl(faylnomi []byte, data []byte) {
	var ata0s = TMurakkabTexnologiyaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oʻqishpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Oʻqish(&ata0s, partition.Mbr.Primarypartition[0], faylnomi, data)

	ata0s.Flush()
}
func Yuklashelf() {

	var ata0s = TMurakkabTexnologiyaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oʻqishpartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var faylnomi []byte = ([]byte)("TEST")
	var hajmi uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faylnomi)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Oʻqish(&ata0s, partition.Mbr.Primarypartition[0], faylnomi, data)

	elf := Elf{}

	elf.Parse(data[:hajmi], 0x4f00000)

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

		SysChopetishunsignedinteger32(esi)

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
		JarayonpendingKlaviaturaevents()
		JarayonpendingSichqonchaevents()
		halt()
	}
}

func memorytest(y int) {
	xotiramanager := &TXotiramanager{}
	allocated := uint32(uintptr(xotiramanager.Malloc(1024)))
	console.MUnsignedinteger32Chopetishxy(allocated, 10, uint16(y))
	if y == 11 {
		xotiramanager.Bosh(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Qaytayuklashcr3() uint32

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

func GetfunctionNomi(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNomi = runtime.FuncForPC(address).Name()
	var funcBaytlar []byte = []byte(funcNomi)

	taskconsole.MChopetishxy(funcBaytlar, 1, 5)
	taskconsole.MChopetish(([]byte)(":"))
	taskconsole.MUnsignedinteger32Chopetish(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MChopetishunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(SAHIFAJildentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MChopetish("\n=== UZB BOOT ===\n")

	console.MChopetishunsignedinteger32(uint32(SAHIFAJildentry), 0, 2)
	console.MChopetishunsignedinteger32(uint32(SAHIFAJildentry), 10, 2)
	console.MChopetishunsignedinteger32(uint32(stacktop), 0, 3)
	console.MChopetishunsignedinteger32(uint32(stackbottom), 10, 3)

	xotiramanager := &TXotiramanager{}
	xotiramanager.Init(0, MaxqueueHajmi)

	paging := &Paging{}
	paging.Init(SAHIFAJildentry, 0x500000, xotiramanager)
	paging.SharedXotiraregion()

	Setcr3(uint32(SAHIFAJildentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MChopetish("esp:")

	esp := getesp()
	console.MUnsignedinteger32Chopetish(uint32(esp))

	tls := gettls()
	console.MChopetish(([]byte)("tls:"))
	console.MUnsignedinteger32Chopetish(tls)

	tss.Oʻrnatish(shareddescriptortable, 7, Segkerneldata, esp)

	VirtSinash()

	cr3 := Qaytayuklashcr3()
	console.MChopetish(([]byte)(":cr3:"))
	console.MUnsignedinteger32Chopetish(cr3)

	cr0 := Getcr0()
	console.MChopetish(([]byte)(":cr0:"))
	console.MUnsignedinteger32Chopetish(cr0)

	cr4 := Getcr4()
	console.MChopetish(([]byte)(":cr4:"))
	console.MUnsignedinteger32Chopetish(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptortable, taskmanager_2)

	paging.SAHIFAfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(xotiramanager)

	jarayonhelper := Jarayonhelper{}
	jarayonhelper.Init(xotiramanager, SAHIFAJildentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, xotiramanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	jarayonhelper.Spawn(taska, threadhelper, sche, uint32(SAHIFAJildentry), true)
	jarayonhelper.Spawn(taskb, threadhelper, sche, uint32(SAHIFAJildentry), true)
	jarayonhelper.Spawn(taskc, threadhelper, sche, uint32(SAHIFAJildentry), true)
	jarayonhelper.Spawn(taskd1, threadhelper, sche, uint32(SAHIFAJildentry), true)
	jarayonhelper.Spawn(inputeventtask, threadhelper, sche, uint32(SAHIFAJildentry), true)

	var hajmi uint32

	var linkerFayl []byte = ([]byte)("LINKER")
	hajmi = GetFaylHajmi(linkerFayl)
	linkeraddress := xotiramanager.Malloc(hajmi)
	linkerdata := GetBaytlarfromKorsatgich(uintptr(linkeraddress), int(hajmi), int(hajmi))
	OʻqishFayl(linkerFayl, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SAHIFAJildentry))

	bogʻmap := Bogʻmap{}
	bogʻmap.Init(xotiramanager)

	var lib1Fayl []byte = ([]byte)("LIB1")
	hajmi = GetFaylHajmi(lib1Fayl)

	lib1address := xotiramanager.Malloc(hajmi)
	lib1data := GetBaytlarfromKorsatgich(uintptr(lib1address), int(hajmi), int(hajmi))
	OʻqishFayl(lib1Fayl, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SAHIFAJildentry))
	xotiramanager.Bosh(lib1address)

	bogʻmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Fayl []byte = ([]byte)("LIB2")
	hajmi = GetFaylHajmi(lib2Fayl)

	lib2address := xotiramanager.Malloc(hajmi)
	lib2data := GetBaytlarfromKorsatgich(uintptr(lib2address), int(hajmi), int(hajmi))
	OʻqishFayl(lib2Fayl, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SAHIFAJildentry))
	xotiramanager.Bosh(lib2address)

	bogʻmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libBogʻmap := bogʻmap.Clone()
	bogʻmapaddress := uint32(uintptr(Pointer(libBogʻmap.First)))

	lib1got := Getunsignedinteger32arrayfromKorsatgich(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = bogʻmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfromKorsatgich(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = bogʻmapaddress
	lib2got[2] = 0x4000000

	console.MChopetishxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Chopetish(lib1elf.Got)
	console.MChopetish(":")
	console.MUnsignedinteger32Chopetish(lib1elf.Dynamic)

	console.MChopetishxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Chopetish(lib2elf.Got)
	console.MChopetish(":")
	console.MUnsignedinteger32Chopetish(lib2elf.Dynamic)

	var foydalanuvchi1Fayl []byte = ([]byte)("USER1")
	hajmi = GetFaylHajmi(foydalanuvchi1Fayl)
	foydalanuvchi1address := xotiramanager.Malloc(hajmi)
	foydalanuvchi1data := GetBaytlarfromKorsatgich(uintptr(foydalanuvchi1address), int(hajmi), int(hajmi))
	OʻqishFayl(foydalanuvchi1Fayl, foydalanuvchi1data)

	elf2 := Elf{}

	foydalanuvchi1entry := elf2.Getentry(foydalanuvchi1data)
	elf2.Parse(foydalanuvchi1data[:], uint32(SAHIFAJildentry+0x1000))
	globaloffsettable := elf2.Got

	PQiymat1Bogʻmap := bogʻmap.Clone()
	PQiymat1Bogʻmap.Append_to_list(uintptr(elf2.Dynamic))

	xotiramanager.Bosh(foydalanuvchi1address)

	var code1Korsatgich *uintptr
	var func1val func()

	code1Korsatgich = (*uintptr)(xotiramanager.Malloc(4))
	*code1Korsatgich = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Korsatgich))

	proc2 := jarayonhelper.Spawn(func1val, threadhelper, sche, uint32(SAHIFAJildentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = foydalanuvchi1entry
	thr2.Cpustate.Edx = globaloffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PQiymat1Bogʻmap.First)))

	console.MChopetishxy("user1: ", 1, 10)
	console.MUnsignedinteger32Chopetish(elf2.Got)

	var foydalanuvchi2Fayl []byte = ([]byte)("USER2")
	hajmi = GetFaylHajmi(foydalanuvchi2Fayl)
	foydalanuvchi2address := xotiramanager.Malloc(hajmi)
	foydalanuvchi2data := GetBaytlarfromKorsatgich(uintptr(foydalanuvchi2address), int(hajmi), int(hajmi))
	OʻqishFayl(foydalanuvchi2Fayl, foydalanuvchi2data)

	elf3 := Elf{}

	foydalanuvchi2entry := elf3.Getentry(foydalanuvchi2data)
	elf3.Parse(foydalanuvchi2data[:], uint32(SAHIFAJildentry+0x2000))
	globaloffsettable = elf3.Got

	PQiymat2Bogʻmap := bogʻmap.Clone()
	PQiymat2Bogʻmap.Append_to_list(uintptr(elf3.Dynamic))

	xotiramanager.Bosh(foydalanuvchi2address)

	var code2Korsatgich *uintptr
	var func2val func()

	code2Korsatgich = (*uintptr)(xotiramanager.Malloc(4))
	*code2Korsatgich = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Korsatgich))

	proc3 := jarayonhelper.Spawn(func2val, threadhelper, sche, uint32(SAHIFAJildentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = foydalanuvchi2entry
	thr3.Cpustate.Edx = globaloffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PQiymat2Bogʻmap.First)))

	console.MChopetishxy("user2: ", 1, 11)
	console.MUnsignedinteger32Chopetish(thr3.Cpustate.Esi)

	libBogʻmap.Chopetish(1, 11)

	var foydalanuvchi3Fayl []byte = ([]byte)("USER3")
	hajmi = GetFaylHajmi(foydalanuvchi3Fayl)
	foydalanuvchi3address := xotiramanager.Malloc(hajmi)
	foydalanuvchi3data := GetBaytlarfromKorsatgich(uintptr(foydalanuvchi3address), int(hajmi), int(hajmi))
	OʻqishFayl(foydalanuvchi3Fayl, foydalanuvchi3data)

	elf4 := Elf{}

	foydalanuvchi3entry := elf4.Getentry(foydalanuvchi3data)
	elf4.Parse(foydalanuvchi3data[:], uint32(SAHIFAJildentry+0x3000))
	globaloffsettable = elf4.Got

	PQiymat3Bogʻmap := bogʻmap.Clone()
	PQiymat3Bogʻmap.Append_to_list(uintptr(elf4.Dynamic))

	xotiramanager.Bosh(foydalanuvchi3address)

	var code3Korsatgich *uintptr
	var func3val func()

	code3Korsatgich = (*uintptr)(xotiramanager.Malloc(4))
	*code3Korsatgich = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Korsatgich))

	proc4 := jarayonhelper.Spawn(func3val, threadhelper, sche, uint32(SAHIFAJildentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = foydalanuvchi3entry
	thr4.Cpustate.Edx = globaloffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PQiymat3Bogʻmap.First)))

	jarayonhelper.Spawn(TFunction1, threadhelper, sche, uint32(SAHIFAJildentry+0x4000), true)

	iKlaviaturaeventhandler = &myKlaviaturaeventhandler
	klaviaturadriver.Initdriver(Interruptmanager, iKlaviaturaeventhandler)

	sichqonchadriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	uskunadescriptor = mypcicontrollerhandler.Getdriver()

	sche.Yoqilgan(true)
	Interruptmanager.Faol()

	for {
		halt()
	}

}
