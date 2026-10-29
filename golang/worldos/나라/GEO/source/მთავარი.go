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

import . "virtualმეხსიერება"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/პროცესი"
import . "driver/driver"

import . "driver/კლავიატურა"
import . "driver/თაგვი"

import . "driver/ata"
import . "ფაილისისტემა/msdospartition"
import . "ფაილისისტემა/fat"

import . "ფაილისისტემა/elf"

import . "სისტემაcall"

import . "მეხსიერებაmanager"
import . "pci"

func halt()

var iკლავიატურაeventhandler Iკლავიატურაeventhandler

type TMyკლავიატურაeventhandler struct {
}

var myკლავიატურაeventhandler TMyკლავიატურაeventhandler
var კლავიატურაdriver Tკლავიატურაdriver
var თაგვიdriver Tთაგვიdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var კლავიატურაconsole TConsole = TConsole{}

func (self *TMyკლავიატურაeventhandler) Onkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	კლავიატურაconsole.Mბეჭდვაბაიტიxy(foo[:], 1000, 1000)
}

func (self *TMyკლავიატურაeventhandler) Onkeyზემოთ(key byte)	{}

var iთაგვიeventhandler Iთაგვიeventhandler

type TMyთაგვიeventhandler struct {
}

var თაგვიconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMyთაგვიeventhandler) Onთაგვიdown(button int8) {
	buffer := []byte("x")
	თაგვიconsole.Mბეჭდვაxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyთაგვიeventhandler) Onთაგვიზემოთ(button int8)	{}
func (self *TMyთაგვიeventhandler) Onთაგვიგადაადგილება(x int8, y int8) {

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
	თაგვიconsole.Mბეჭდვაxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	თაგვიconsole.Mბეჭდვაxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var მოწყობილობაdescriptor TPeripheralcomponentinterconnectმოწყობილობაdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(მოწყობილობა TPeripheralcomponentinterconnectმოწყობილობაdescriptor) {
	if მოწყობილობა.Vendorid == 0x1022 && მოწყობილობა.Dმოწყობილობაid == 0x2000 {
		console.Mბეჭდვაxy([]byte("["), 0, 12)
		console.Mბეჭდვა(([]byte)("AMD am79c973"))
		console.Mბეჭდვა([]byte(":"))
		console.MUnsignedinteger16ბეჭდვა(მოწყობილობა.Vendorid)
		console.Mბეჭდვა([]byte(":"))
		console.MUnsignedinteger16ბეჭდვა(მოწყობილობა.Dმოწყობილობაid)
		console.Mბეჭდვა([]byte(":"))
		console.MUnsignedinteger16ბეჭდვა(uint16(მოწყობილობა.Pპორტიbase))
		console.Mბეჭდვა([]byte(":"))
		console.MUnsignedinteger32ბეჭდვა(მოწყობილობა.Interrupt)

		console.Mბეჭდვა([]byte("]\n"))
		მოწყობილობაdescriptor = მოწყობილობა
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectმოწყობილობაdescriptor {
	return მოწყობილობაdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pბეჭდვაstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.Mბეჭდვა(str)
}

func Getფაილიზომა(ფაილისსახელი []byte) uint32 {
	var ata0s = Tდეტალურიtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionცხრილი{}
	partition.Rკითხვაpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var ზომა uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი)
	ata0s.Flush()

	return ზომა
}

func Rკითხვაფაილი(ფაილისსახელი []byte, data []byte) {
	var ata0s = Tდეტალურიtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionცხრილი{}
	partition.Rკითხვაpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Rკითხვა(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი, data)

	ata0s.Flush()
}
func Lჩატვირთვაelf() {

	var ata0s = Tდეტალურიtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionცხრილი{}
	partition.Rკითხვაpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var ფაილისსახელი []byte = ([]byte)("TEST")
	var ზომა uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Rკითხვა(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი, data)

	elf := Elf{}

	elf.Parse(data[:ზომა], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func Tფუნქცია1() {
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

		Sysბეჭდვაunsignedinteger32(esi)

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
		Pპროცესიpendingკლავიატურაevents()
		Pპროცესიpendingთაგვიevents()
		halt()
	}
}

func memorytest(y int) {
	მეხსიერებაmanager := &Tმეხსიერებაmanager{}
	allocated := uint32(uintptr(მეხსიერებაmanager.Malloc(1024)))
	console.MUnsignedinteger32ბეჭდვაxy(allocated, 10, uint16(y))
	if y == 11 {
		მეხსიერებაmanager.Fთავისუფალი(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Rგადატვირთვაcr3() uint32

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

func Getფუნქციასახელი(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcსახელი = runtime.FuncForPC(address).Name()
	var funcბაიტი []byte = []byte(funcსახელი)

	taskconsole.Mბეჭდვაxy(funcბაიტი, 1, 5)
	taskconsole.Mბეჭდვა(([]byte)(":"))
	taskconsole.MUnsignedinteger32ბეჭდვა(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.Mბეჭდვაunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pგვერდიდასტაentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.Mბეჭდვა("\n=== GEO BOOT ===\n")

	console.Mბეჭდვაunsignedinteger32(uint32(Pგვერდიდასტაentry), 0, 2)
	console.Mბეჭდვაunsignedinteger32(uint32(Pგვერდიდასტაentry), 10, 2)
	console.Mბეჭდვაunsignedinteger32(uint32(stacktop), 0, 3)
	console.Mბეჭდვაunsignedinteger32(uint32(stackbottom), 10, 3)

	მეხსიერებაmanager := &Tმეხსიერებაmanager{}
	მეხსიერებაmanager.Init(0, Maxqueueზომა)

	paging := &Paging{}
	paging.Init(Pგვერდიდასტაentry, 0x500000, მეხსიერებაmanager)
	paging.Sharedმეხსიერებაregion()

	Setcr3(uint32(Pგვერდიდასტაentry))
	Enablepaging()

	shareddescriptorცხრილი := &TShareddescriptorცხრილი{}
	shareddescriptorცხრილი.Init()

	console.Mბეჭდვა("esp:")

	esp := getesp()
	console.MUnsignedinteger32ბეჭდვა(uint32(esp))

	tls := gettls()
	console.Mბეჭდვა(([]byte)("tls:"))
	console.MUnsignedinteger32ბეჭდვა(tls)

	tss.Iდაყენება(shareddescriptorცხრილი, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Rგადატვირთვაcr3()
	console.Mბეჭდვა(([]byte)(":cr3:"))
	console.MUnsignedinteger32ბეჭდვა(cr3)

	cr0 := Getcr0()
	console.Mბეჭდვა(([]byte)(":cr0:"))
	console.MUnsignedinteger32ბეჭდვა(cr0)

	cr4 := Getcr4()
	console.Mბეჭდვა(([]byte)(":cr4:"))
	console.MUnsignedinteger32ბეჭდვა(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorცხრილი, taskmanager_2)

	paging.Pგვერდიfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(მეხსიერებაmanager)

	პროცესიhelper := Pპროცესიhelper{}
	პროცესიhelper.Init(მეხსიერებაmanager, Pგვერდიდასტაentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, მეხსიერებაmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	პროცესიhelper.Spawn(taska, threadhelper, sche, uint32(Pგვერდიდასტაentry), true)
	პროცესიhelper.Spawn(taskb, threadhelper, sche, uint32(Pგვერდიდასტაentry), true)
	პროცესიhelper.Spawn(taskc, threadhelper, sche, uint32(Pგვერდიდასტაentry), true)
	პროცესიhelper.Spawn(taskd1, threadhelper, sche, uint32(Pგვერდიდასტაentry), true)
	პროცესიhelper.Spawn(inputeventtask, threadhelper, sche, uint32(Pგვერდიდასტაentry), true)

	var ზომა uint32

	var linkerფაილი []byte = ([]byte)("LINKER")
	ზომა = Getფაილიზომა(linkerფაილი)
	linkeraddress := მეხსიერებაmanager.Malloc(ზომა)
	linkerdata := Getბაიტიfromკურსორი(uintptr(linkeraddress), int(ზომა), int(ზომა))
	Rკითხვაფაილი(linkerფაილი, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pგვერდიდასტაentry))

	ბმულიmap := Lბმულიmap{}
	ბმულიmap.Init(მეხსიერებაmanager)

	var lib1ფაილი []byte = ([]byte)("LIB1")
	ზომა = Getფაილიზომა(lib1ფაილი)

	lib1address := მეხსიერებაmanager.Malloc(ზომა)
	lib1data := Getბაიტიfromკურსორი(uintptr(lib1address), int(ზომა), int(ზომა))
	Rკითხვაფაილი(lib1ფაილი, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pგვერდიდასტაentry))
	მეხსიერებაmanager.Fთავისუფალი(lib1address)

	ბმულიmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2ფაილი []byte = ([]byte)("LIB2")
	ზომა = Getფაილიზომა(lib2ფაილი)

	lib2address := მეხსიერებაmanager.Malloc(ზომა)
	lib2data := Getბაიტიfromკურსორი(uintptr(lib2address), int(ზომა), int(ზომა))
	Rკითხვაფაილი(lib2ფაილი, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pგვერდიდასტაentry))
	მეხსიერებაmanager.Fთავისუფალი(lib2address)

	ბმულიmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libბმულიmap := ბმულიmap.Clone()
	ბმულიmapaddress := uint32(uintptr(Pointer(libბმულიmap.First)))

	lib1got := Getunsignedinteger32მასივიfromკურსორი(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = ბმულიmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32მასივიfromკურსორი(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = ბმულიmapaddress
	lib2got[2] = 0x4000000

	console.Mბეჭდვაxy("lib1: ", 1, 8)
	console.MUnsignedinteger32ბეჭდვა(lib1elf.Got)
	console.Mბეჭდვა(":")
	console.MUnsignedinteger32ბეჭდვა(lib1elf.Dynamic)

	console.Mბეჭდვაxy("lib2: ", 1, 9)
	console.MUnsignedinteger32ბეჭდვა(lib2elf.Got)
	console.Mბეჭდვა(":")
	console.MUnsignedinteger32ბეჭდვა(lib2elf.Dynamic)

	var მომხმარებელი1ფაილი []byte = ([]byte)("USER1")
	ზომა = Getფაილიზომა(მომხმარებელი1ფაილი)
	მომხმარებელი1address := მეხსიერებაmanager.Malloc(ზომა)
	მომხმარებელი1data := Getბაიტიfromკურსორი(uintptr(მომხმარებელი1address), int(ზომა), int(ზომა))
	Rკითხვაფაილი(მომხმარებელი1ფაილი, მომხმარებელი1data)

	elf2 := Elf{}

	მომხმარებელი1entry := elf2.Getentry(მომხმარებელი1data)
	elf2.Parse(მომხმარებელი1data[:], uint32(Pგვერდიდასტაentry+0x1000))
	globaloffsetცხრილი := elf2.Got

	Pმნიშვნელობა1ბმულიmap := ბმულიmap.Clone()
	Pმნიშვნელობა1ბმულიmap.Append_to_list(uintptr(elf2.Dynamic))

	მეხსიერებაmanager.Fთავისუფალი(მომხმარებელი1address)

	var code1კურსორი *uintptr
	var func1val func()

	code1კურსორი = (*uintptr)(მეხსიერებაmanager.Malloc(4))
	*code1კურსორი = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1კურსორი))

	proc2 := პროცესიhelper.Spawn(func1val, threadhelper, sche, uint32(Pგვერდიდასტაentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = მომხმარებელი1entry
	thr2.Cpustate.Edx = globaloffsetცხრილი
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(Pმნიშვნელობა1ბმულიmap.First)))

	console.Mბეჭდვაxy("user1: ", 1, 10)
	console.MUnsignedinteger32ბეჭდვა(elf2.Got)

	var მომხმარებელი2ფაილი []byte = ([]byte)("USER2")
	ზომა = Getფაილიზომა(მომხმარებელი2ფაილი)
	მომხმარებელი2address := მეხსიერებაmanager.Malloc(ზომა)
	მომხმარებელი2data := Getბაიტიfromკურსორი(uintptr(მომხმარებელი2address), int(ზომა), int(ზომა))
	Rკითხვაფაილი(მომხმარებელი2ფაილი, მომხმარებელი2data)

	elf3 := Elf{}

	მომხმარებელი2entry := elf3.Getentry(მომხმარებელი2data)
	elf3.Parse(მომხმარებელი2data[:], uint32(Pგვერდიდასტაentry+0x2000))
	globaloffsetცხრილი = elf3.Got

	Pმნიშვნელობა2ბმულიmap := ბმულიmap.Clone()
	Pმნიშვნელობა2ბმულიmap.Append_to_list(uintptr(elf3.Dynamic))

	მეხსიერებაmanager.Fთავისუფალი(მომხმარებელი2address)

	var code2კურსორი *uintptr
	var func2val func()

	code2კურსორი = (*uintptr)(მეხსიერებაmanager.Malloc(4))
	*code2კურსორი = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2კურსორი))

	proc3 := პროცესიhelper.Spawn(func2val, threadhelper, sche, uint32(Pგვერდიდასტაentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = მომხმარებელი2entry
	thr3.Cpustate.Edx = globaloffsetცხრილი
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(Pმნიშვნელობა2ბმულიmap.First)))

	console.Mბეჭდვაxy("user2: ", 1, 11)
	console.MUnsignedinteger32ბეჭდვა(thr3.Cpustate.Esi)

	libბმულიmap.Pბეჭდვა(1, 11)

	var მომხმარებელი3ფაილი []byte = ([]byte)("USER3")
	ზომა = Getფაილიზომა(მომხმარებელი3ფაილი)
	მომხმარებელი3address := მეხსიერებაmanager.Malloc(ზომა)
	მომხმარებელი3data := Getბაიტიfromკურსორი(uintptr(მომხმარებელი3address), int(ზომა), int(ზომა))
	Rკითხვაფაილი(მომხმარებელი3ფაილი, მომხმარებელი3data)

	elf4 := Elf{}

	მომხმარებელი3entry := elf4.Getentry(მომხმარებელი3data)
	elf4.Parse(მომხმარებელი3data[:], uint32(Pგვერდიდასტაentry+0x3000))
	globaloffsetცხრილი = elf4.Got

	Pმნიშვნელობა3ბმულიmap := ბმულიmap.Clone()
	Pმნიშვნელობა3ბმულიmap.Append_to_list(uintptr(elf4.Dynamic))

	მეხსიერებაmanager.Fთავისუფალი(მომხმარებელი3address)

	var code3კურსორი *uintptr
	var func3val func()

	code3კურსორი = (*uintptr)(მეხსიერებაmanager.Malloc(4))
	*code3კურსორი = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3კურსორი))

	proc4 := პროცესიhelper.Spawn(func3val, threadhelper, sche, uint32(Pგვერდიდასტაentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = მომხმარებელი3entry
	thr4.Cpustate.Edx = globaloffsetცხრილი
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(Pმნიშვნელობა3ბმულიmap.First)))

	პროცესიhelper.Spawn(Tფუნქცია1, threadhelper, sche, uint32(Pგვერდიდასტაentry+0x4000), true)

	iკლავიატურაeventhandler = &myკლავიატურაeventhandler
	კლავიატურაdriver.Initdriver(Interruptmanager, iკლავიატურაeventhandler)

	თაგვიdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	მოწყობილობაdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Eჩართულია(true)
	Interruptmanager.Aაქტიური()

	for {
		halt()
	}

}
