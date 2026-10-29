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
import . "مداخلت"
import . "multitasking"
import . "tasking/tss"

import . "virtualیادداشت"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/عملکاری"
import . "driver/driver"

import . "driver/کیبورڈ"
import . "driver/ماؤس"

import . "driver/ata"
import . "فائلنظام/msdospartition"
import . "فائلنظام/fat"

import . "فائلنظام/elf"

import . "نظامcall"

import . "یادداشتmanager"
import . "pci"

func halt()

var iکیبورڈواقعہhandler Iکیبورڈواقعہhandler

type TMyکیبورڈواقعہhandler struct {
}

var myکیبورڈواقعہhandler TMyکیبورڈواقعہhandler
var کیبورڈdriver Tکیبورڈdriver
var ماؤسdriver Tماؤسdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var کیبورڈconsole TConsole = TConsole{}

func (self *TMyکیبورڈواقعہhandler) Oچالوkeyنیچے(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	کیبورڈconsole.Mچھاپیںبائٹسxy(foo[:], 1000, 1000)
}

func (self *TMyکیبورڈواقعہhandler) Oچالوkeyاوپر(key byte)	{}

var iماؤسواقعہhandler Iماؤسواقعہhandler

type TMyماؤسواقعہhandler struct {
}

var ماؤسconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMyماؤسواقعہhandler) Oچالوماؤسنیچے(بٹن int8) {
	buffer := []byte("x")
	ماؤسconsole.Mچھاپیںxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyماؤسواقعہhandler) Oچالوماؤساوپر(بٹن int8)	{}
func (self *TMyماؤسواقعہhandler) Oچالوماؤسمنتقلکریں(x int8, y int8) {

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
	ماؤسconsole.Mچھاپیںxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	ماؤسconsole.Mچھاپیںxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var آلہdescriptor TPeripheralcomponentinterconnectآلہdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Oچالوgetdriver(آلہ TPeripheralcomponentinterconnectآلہdescriptor) {
	if آلہ.Vفروشندہآئیڈی == 0x1022 && آلہ.Dآلہآئیڈی == 0x2000 {
		console.Mچھاپیںxy([]byte("["), 0, 12)
		console.Mچھاپیں(([]byte)("AMD am79c973"))
		console.Mچھاپیں([]byte(":"))
		console.MUnsignedinteger16چھاپیں(آلہ.Vفروشندہآئیڈی)
		console.Mچھاپیں([]byte(":"))
		console.MUnsignedinteger16چھاپیں(آلہ.Dآلہآئیڈی)
		console.Mچھاپیں([]byte(":"))
		console.MUnsignedinteger16چھاپیں(uint16(آلہ.Pپورٹbase))
		console.Mچھاپیں([]byte(":"))
		console.MUnsignedinteger32چھاپیں(آلہ.Iمداخلت)

		console.Mچھاپیں([]byte("]\n"))
		آلہdescriptor = آلہ
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectآلہdescriptor {
	return آلہdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pچھاپیںstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.Mچھاپیں(str)
}

func Getفائلحجم(فائلکانام []byte) uint32 {
	var ata0s = Tاعلیٹیکنالوجیattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rپڑھیںpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var حجم uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام)
	ata0s.Flush()

	return حجم
}

func Rپڑھیںفائل(فائلکانام []byte, data []byte) {
	var ata0s = Tاعلیٹیکنالوجیattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rپڑھیںpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Rپڑھیں(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام, data)

	ata0s.Flush()
}
func Lبوجھelf() {

	var ata0s = Tاعلیٹیکنالوجیattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rپڑھیںpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var فائلکانام []byte = ([]byte)("TEST")
	var حجم uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Rپڑھیں(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام, data)

	elf := Elf{}

	elf.Parse(data[:حجم], 0x4f00000)

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

		Sysچھاپیںunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ماداخلواقعہtask() {
	for {
		Pعملکاریpendingکیبورڈevents()
		Pعملکاریpendingماؤسevents()
		halt()
	}
}

func memorytest(y int) {
	یادداشتmanager := &Tیادداشتmanager{}
	allocated := uint32(uintptr(یادداشتmanager.Malloc(1024)))
	console.MUnsignedinteger32چھاپیںxy(allocated, 10, uint16(y))
	if y == 11 {
		یادداشتmanager.Fخالی(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pموقوفloop()
func Rدوبارہلادیںcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sسیٹcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getfunctionنام(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcنام = runtime.FuncForPC(address).Name()
	var funcبائٹس []byte = []byte(funcنام)

	taskconsole.Mچھاپیںxy(funcبائٹس, 1, 5)
	taskconsole.Mچھاپیں(([]byte)(":"))
	taskconsole.MUnsignedinteger32چھاپیں(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.Mچھاپیںunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pصفحہڈائریکٹریentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.Mچھاپیں("\n=== PAK BOOT ===\n")

	console.Mچھاپیںunsignedinteger32(uint32(Pصفحہڈائریکٹریentry), 0, 2)
	console.Mچھاپیںunsignedinteger32(uint32(Pصفحہڈائریکٹریentry), 10, 2)
	console.Mچھاپیںunsignedinteger32(uint32(stacktop), 0, 3)
	console.Mچھاپیںunsignedinteger32(uint32(stackbottom), 10, 3)

	یادداشتmanager := &Tیادداشتmanager{}
	یادداشتmanager.Init(0, Mزیادہqueueحجم)

	paging := &Paging{}
	paging.Init(Pصفحہڈائریکٹریentry, 0x500000, یادداشتmanager)
	paging.Sharedیادداشتregion()

	Sسیٹcr3(uint32(Pصفحہڈائریکٹریentry))
	Enablepaging()

	shareddescriptorجدول := &TShareddescriptorجدول{}
	shareddescriptorجدول.Init()

	console.Mچھاپیں("esp:")

	esp := getesp()
	console.MUnsignedinteger32چھاپیں(uint32(esp))

	tls := gettls()
	console.Mچھاپیں(([]byte)("tls:"))
	console.MUnsignedinteger32چھاپیں(tls)

	tss.Iنصبکریں(shareddescriptorجدول, 7, Segkerneldata, esp)

	Virtٹیسٹ()

	cr3 := Rدوبارہلادیںcr3()
	console.Mچھاپیں(([]byte)(":cr3:"))
	console.MUnsignedinteger32چھاپیں(cr3)

	cr0 := Getcr0()
	console.Mچھاپیں(([]byte)(":cr0:"))
	console.MUnsignedinteger32چھاپیں(cr0)

	cr4 := Getcr4()
	console.Mچھاپیں(([]byte)(":cr4:"))
	console.MUnsignedinteger32چھاپیں(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Iمداخلتmanager := &Tمداخلتmanager{}
	Iمداخلتmanager.Init(0x20, shareddescriptorجدول, taskmanager_2)

	paging.Pصفحہfault(Iمداخلتmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(یادداشتmanager)

	عملکاریhelper := Pعملکاریhelper{}
	عملکاریhelper.Init(یادداشتmanager, Pصفحہڈائریکٹریentry)

	sche := &Scheduler{}
	sche.Init(Iمداخلتmanager, یادداشتmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Iمداخلتmanager)

	عملکاریhelper.Spawn(taska, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry), true)
	عملکاریhelper.Spawn(taskb, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry), true)
	عملکاریhelper.Spawn(taskc, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry), true)
	عملکاریhelper.Spawn(taskd1, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry), true)
	عملکاریhelper.Spawn(ماداخلواقعہtask, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry), true)

	var حجم uint32

	var linkerفائل []byte = ([]byte)("LINKER")
	حجم = Getفائلحجم(linkerفائل)
	linkeraddress := یادداشتmanager.Malloc(حجم)
	linkerdata := Getبائٹسfromپؤائنٹر(uintptr(linkeraddress), int(حجم), int(حجم))
	Rپڑھیںفائل(linkerفائل, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pصفحہڈائریکٹریentry))

	ربطmap := Lربطmap{}
	ربطmap.Init(یادداشتmanager)

	var lib1فائل []byte = ([]byte)("LIB1")
	حجم = Getفائلحجم(lib1فائل)

	lib1address := یادداشتmanager.Malloc(حجم)
	lib1data := Getبائٹسfromپؤائنٹر(uintptr(lib1address), int(حجم), int(حجم))
	Rپڑھیںفائل(lib1فائل, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pصفحہڈائریکٹریentry))
	یادداشتmanager.Fخالی(lib1address)

	ربطmap.Append_to_list(uintptr(lib1elf.Dمحرک))

	var lib2فائل []byte = ([]byte)("LIB2")
	حجم = Getفائلحجم(lib2فائل)

	lib2address := یادداشتmanager.Malloc(حجم)
	lib2data := Getبائٹسfromپؤائنٹر(uintptr(lib2address), int(حجم), int(حجم))
	Rپڑھیںفائل(lib2فائل, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pصفحہڈائریکٹریentry))
	یادداشتmanager.Fخالی(lib2address)

	ربطmap.Append_to_list(uintptr(lib2elf.Dمحرک))

	libربطmap := ربطmap.Clone()
	ربطmapaddress := uint32(uintptr(Pointer(libربطmap.First)))

	lib1got := Getunsignedinteger32لڑیfromپؤائنٹر(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = ربطmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32لڑیfromپؤائنٹر(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = ربطmapaddress
	lib2got[2] = 0x4000000

	console.Mچھاپیںxy("lib1: ", 1, 8)
	console.MUnsignedinteger32چھاپیں(lib1elf.Got)
	console.Mچھاپیں(":")
	console.MUnsignedinteger32چھاپیں(lib1elf.Dمحرک)

	console.Mچھاپیںxy("lib2: ", 1, 9)
	console.MUnsignedinteger32چھاپیں(lib2elf.Got)
	console.Mچھاپیں(":")
	console.MUnsignedinteger32چھاپیں(lib2elf.Dمحرک)

	var صارف1فائل []byte = ([]byte)("USER1")
	حجم = Getفائلحجم(صارف1فائل)
	صارف1address := یادداشتmanager.Malloc(حجم)
	صارف1data := Getبائٹسfromپؤائنٹر(uintptr(صارف1address), int(حجم), int(حجم))
	Rپڑھیںفائل(صارف1فائل, صارف1data)

	elf2 := Elf{}

	صارف1entry := elf2.Getentry(صارف1data)
	elf2.Parse(صارف1data[:], uint32(Pصفحہڈائریکٹریentry+0x1000))
	globaloffsetجدول := elf2.Got

	Pقدر1ربطmap := ربطmap.Clone()
	Pقدر1ربطmap.Append_to_list(uintptr(elf2.Dمحرک))

	یادداشتmanager.Fخالی(صارف1address)

	var code1پؤائنٹر *uintptr
	var func1val func()

	code1پؤائنٹر = (*uintptr)(یادداشتmanager.Malloc(4))
	*code1پؤائنٹر = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1پؤائنٹر))

	proc2 := عملکاریhelper.Spawn(func1val, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cسیپییوحالت.Ecx = صارف1entry
	thr2.Cسیپییوحالت.Edx = globaloffsetجدول
	thr2.Cسیپییوحالت.Esi = uint32(uintptr(Pointer(Pقدر1ربطmap.First)))

	console.Mچھاپیںxy("user1: ", 1, 10)
	console.MUnsignedinteger32چھاپیں(elf2.Got)

	var صارف2فائل []byte = ([]byte)("USER2")
	حجم = Getفائلحجم(صارف2فائل)
	صارف2address := یادداشتmanager.Malloc(حجم)
	صارف2data := Getبائٹسfromپؤائنٹر(uintptr(صارف2address), int(حجم), int(حجم))
	Rپڑھیںفائل(صارف2فائل, صارف2data)

	elf3 := Elf{}

	صارف2entry := elf3.Getentry(صارف2data)
	elf3.Parse(صارف2data[:], uint32(Pصفحہڈائریکٹریentry+0x2000))
	globaloffsetجدول = elf3.Got

	Pقدر2ربطmap := ربطmap.Clone()
	Pقدر2ربطmap.Append_to_list(uintptr(elf3.Dمحرک))

	یادداشتmanager.Fخالی(صارف2address)

	var code2پؤائنٹر *uintptr
	var func2val func()

	code2پؤائنٹر = (*uintptr)(یادداشتmanager.Malloc(4))
	*code2پؤائنٹر = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2پؤائنٹر))

	proc3 := عملکاریhelper.Spawn(func2val, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cسیپییوحالت.Ecx = صارف2entry
	thr3.Cسیپییوحالت.Edx = globaloffsetجدول
	thr3.Cسیپییوحالت.Esi = uint32(uintptr(Pointer(Pقدر2ربطmap.First)))

	console.Mچھاپیںxy("user2: ", 1, 11)
	console.MUnsignedinteger32چھاپیں(thr3.Cسیپییوحالت.Esi)

	libربطmap.Pچھاپیں(1, 11)

	var صارف3فائل []byte = ([]byte)("USER3")
	حجم = Getفائلحجم(صارف3فائل)
	صارف3address := یادداشتmanager.Malloc(حجم)
	صارف3data := Getبائٹسfromپؤائنٹر(uintptr(صارف3address), int(حجم), int(حجم))
	Rپڑھیںفائل(صارف3فائل, صارف3data)

	elf4 := Elf{}

	صارف3entry := elf4.Getentry(صارف3data)
	elf4.Parse(صارف3data[:], uint32(Pصفحہڈائریکٹریentry+0x3000))
	globaloffsetجدول = elf4.Got

	Pقدر3ربطmap := ربطmap.Clone()
	Pقدر3ربطmap.Append_to_list(uintptr(elf4.Dمحرک))

	یادداشتmanager.Fخالی(صارف3address)

	var code3پؤائنٹر *uintptr
	var func3val func()

	code3پؤائنٹر = (*uintptr)(یادداشتmanager.Malloc(4))
	*code3پؤائنٹر = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3پؤائنٹر))

	proc4 := عملکاریhelper.Spawn(func3val, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cسیپییوحالت.Ecx = صارف3entry
	thr4.Cسیپییوحالت.Edx = globaloffsetجدول
	thr4.Cسیپییوحالت.Esi = uint32(uintptr(Pointer(Pقدر3ربطmap.First)))

	عملکاریhelper.Spawn(TFunction1, threadhelper, sche, uint32(Pصفحہڈائریکٹریentry+0x4000), true)

	iکیبورڈواقعہhandler = &myکیبورڈواقعہhandler
	کیبورڈdriver.Initdriver(Iمداخلتmanager, iکیبورڈواقعہhandler)

	ماؤسdriver.Initdriver(Iمداخلتmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Sمنتخبکریںdriver(&Drivermanager, Iمداخلتmanager)
	آلہdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Eفعال(true)
	Iمداخلتmanager.Aفعال()

	for {
		halt()
	}

}
