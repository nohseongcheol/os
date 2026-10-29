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

import . "مجازیحافظه"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/صفحهکلید"
import . "driver/موشی"

import . "driver/ata"
import . "پروندهسیستم/msdospartition"
import . "پروندهسیستم/fat"

import . "پروندهسیستم/elf"

import . "سیستمcall"

import . "حافظهmanager"
import . "pci"

func halt()

var iصفحهکلیدeventhandler Iصفحهکلیدeventhandler

type TMyصفحهکلیدeventhandler struct {
}

var myصفحهکلیدeventhandler TMyصفحهکلیدeventhandler
var صفحهکلیدdriver Tصفحهکلیدdriver
var موشیdriver Tموشیdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var صفحهکلیدconsole TConsole = TConsole{}

func (خود *TMyصفحهکلیدeventhandler) Oروشنkeyپایین(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	صفحهکلیدconsole.Mچاپبایتxy(foo[:], 1000, 1000)
}

func (خود *TMyصفحهکلیدeventhandler) Oروشنkeyبالا(key byte)	{}

var iموشیeventhandler Iموشیeventhandler

type TMyموشیeventhandler struct {
}

var موشیconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (خود *TMyموشیeventhandler) Oروشنموشیپایین(دکمه int8) {
	buffer := []byte("x")
	موشیconsole.Mچاپxy(buffer, uint16(previousx), uint16(previousy))
}
func (خود *TMyموشیeventhandler) Oروشنموشیبالا(دکمه int8)	{}
func (خود *TMyموشیeventhandler) Oروشنموشیانتقال(x int8, y int8) {

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
	موشیconsole.Mچاپxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	موشیconsole.Mچاپxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var دستگاهdescriptor TPeripheralcomponentinterconnectدستگاهdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (خود TMypcicontrollerhandler) Oروشنgetdriver(دستگاه TPeripheralcomponentinterconnectدستگاهdescriptor) {
	if دستگاه.Vendorشناسه == 0x1022 && دستگاه.Dدستگاهشناسه == 0x2000 {
		console.Mچاپxy([]byte("["), 0, 12)
		console.Mچاپ(([]byte)("AMD am79c973"))
		console.Mچاپ([]byte(":"))
		console.MUnsignedinteger16چاپ(دستگاه.Vendorشناسه)
		console.Mچاپ([]byte(":"))
		console.MUnsignedinteger16چاپ(دستگاه.Dدستگاهشناسه)
		console.Mچاپ([]byte(":"))
		console.MUnsignedinteger16چاپ(uint16(دستگاه.Pدرگاهbase))
		console.Mچاپ([]byte(":"))
		console.MUnsignedinteger32چاپ(دستگاه.Interrupt)

		console.Mچاپ([]byte("]\n"))
		دستگاهdescriptor = دستگاه
		drivercount++
	}
}
func (خود TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectدستگاهdescriptor {
	return دستگاهdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pچاپstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.Mچاپ(str)
}

func Getپروندهاندازه(نامپرونده []byte) uint32 {
	var ata0s = Tپیشرفتهtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rخواندنpartition(&ata0s)

	bios := TBiosparameterقطعه32{}

	var اندازه uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], نامپرونده)
	ata0s.Flush()

	return اندازه
}

func Rخواندنپرونده(نامپرونده []byte, data []byte) {
	var ata0s = Tپیشرفتهtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rخواندنpartition(&ata0s)

	bios := TBiosparameterقطعه32{}
	bios.Rخواندن(&ata0s, partition.Mbr.Primarypartition[0], نامپرونده, data)

	ata0s.Flush()
}
func Lبارelf() {

	var ata0s = Tپیشرفتهtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rخواندنpartition(&ata0s)

	bios := TBiosparameterقطعه32{}

	var نامپرونده []byte = ([]byte)("TEST")
	var اندازه uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], نامپرونده)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Rخواندن(&ata0s, partition.Mbr.Primarypartition[0], نامپرونده, data)

	elf := Elf{}

	elf.Parse(data[:اندازه], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func Tتابع1() {
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

		Sysچاپunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ورودیeventtask() {
	for {
		Processpendingصفحهکلیدevents()
		Processpendingموشیevents()
		halt()
	}
}

func memorytest(y int) {
	حافظهmanager := &Tحافظهmanager{}
	allocated := uint32(uintptr(حافظهmanager.Malloc(1024)))
	console.MUnsignedinteger32چاپxy(allocated, 10, uint16(y))
	if y == 11 {
		حافظهmanager.Fآزاد(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pمکثloop()
func Rبازخوانیcr3() uint32

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

func Getتابعنام(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcنام = runtime.FuncForPC(address).Name()
	var funcبایت []byte = []byte(funcنام)

	taskconsole.Mچاپxy(funcبایت, 1, 5)
	taskconsole.Mچاپ(([]byte)(":"))
	taskconsole.MUnsignedinteger32چاپ(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.Mچاپunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pصفحهشاخهentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.Mچاپ("\n=== AFG BOOT ===\n")

	console.Mچاپunsignedinteger32(uint32(Pصفحهشاخهentry), 0, 2)
	console.Mچاپunsignedinteger32(uint32(Pصفحهشاخهentry), 10, 2)
	console.Mچاپunsignedinteger32(uint32(stacktop), 0, 3)
	console.Mچاپunsignedinteger32(uint32(stackbottom), 10, 3)

	حافظهmanager := &Tحافظهmanager{}
	حافظهmanager.Init(0, Maxqueueاندازه)

	paging := &Paging{}
	paging.Init(Pصفحهشاخهentry, 0x500000, حافظهmanager)
	paging.Sharedحافظهregion()

	Setcr3(uint32(Pصفحهشاخهentry))
	Enablepaging()

	shareddescriptorجدول := &TShareddescriptorجدول{}
	shareddescriptorجدول.Init()

	console.Mچاپ("esp:")

	esp := getesp()
	console.MUnsignedinteger32چاپ(uint32(esp))

	tls := gettls()
	console.Mچاپ(([]byte)("tls:"))
	console.MUnsignedinteger32چاپ(tls)

	tss.Iنصب(shareddescriptorجدول, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Rبازخوانیcr3()
	console.Mچاپ(([]byte)(":cr3:"))
	console.MUnsignedinteger32چاپ(cr3)

	cr0 := Getcr0()
	console.Mچاپ(([]byte)(":cr0:"))
	console.MUnsignedinteger32چاپ(cr0)

	cr4 := Getcr4()
	console.Mچاپ(([]byte)(":cr4:"))
	console.MUnsignedinteger32چاپ(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorجدول, taskmanager_2)

	paging.Pصفحهfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(حافظهmanager)

	processhelper := Processhelper{}
	processhelper.Init(حافظهmanager, Pصفحهشاخهentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, حافظهmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(Pصفحهشاخهentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(Pصفحهشاخهentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(Pصفحهشاخهentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(Pصفحهشاخهentry), true)
	processhelper.Spawn(ورودیeventtask, threadhelper, sche, uint32(Pصفحهشاخهentry), true)

	var اندازه uint32

	var linkerپرونده []byte = ([]byte)("LINKER")
	اندازه = Getپروندهاندازه(linkerپرونده)
	linkeraddress := حافظهmanager.Malloc(اندازه)
	linkerdata := Getبایتfrompointer(uintptr(linkeraddress), int(اندازه), int(اندازه))
	Rخواندنپرونده(linkerپرونده, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pصفحهشاخهentry))

	پیوندmap := Lپیوندmap{}
	پیوندmap.Init(حافظهmanager)

	var lib1پرونده []byte = ([]byte)("LIB1")
	اندازه = Getپروندهاندازه(lib1پرونده)

	lib1address := حافظهmanager.Malloc(اندازه)
	lib1data := Getبایتfrompointer(uintptr(lib1address), int(اندازه), int(اندازه))
	Rخواندنپرونده(lib1پرونده, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pصفحهشاخهentry))
	حافظهmanager.Fآزاد(lib1address)

	پیوندmap.Append_to_list(uintptr(lib1elf.Dپویا))

	var lib2پرونده []byte = ([]byte)("LIB2")
	اندازه = Getپروندهاندازه(lib2پرونده)

	lib2address := حافظهmanager.Malloc(اندازه)
	lib2data := Getبایتfrompointer(uintptr(lib2address), int(اندازه), int(اندازه))
	Rخواندنپرونده(lib2پرونده, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pصفحهشاخهentry))
	حافظهmanager.Fآزاد(lib2address)

	پیوندmap.Append_to_list(uintptr(lib2elf.Dپویا))

	libپیوندmap := پیوندmap.Clone()
	پیوندmapaddress := uint32(uintptr(Pointer(libپیوندmap.First)))

	lib1got := Getunsignedinteger32آرایهfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = پیوندmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32آرایهfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = پیوندmapaddress
	lib2got[2] = 0x4000000

	console.Mچاپxy("lib1: ", 1, 8)
	console.MUnsignedinteger32چاپ(lib1elf.Got)
	console.Mچاپ(":")
	console.MUnsignedinteger32چاپ(lib1elf.Dپویا)

	console.Mچاپxy("lib2: ", 1, 9)
	console.MUnsignedinteger32چاپ(lib2elf.Got)
	console.Mچاپ(":")
	console.MUnsignedinteger32چاپ(lib2elf.Dپویا)

	var کاربر1پرونده []byte = ([]byte)("USER1")
	اندازه = Getپروندهاندازه(کاربر1پرونده)
	کاربر1address := حافظهmanager.Malloc(اندازه)
	کاربر1data := Getبایتfrompointer(uintptr(کاربر1address), int(اندازه), int(اندازه))
	Rخواندنپرونده(کاربر1پرونده, کاربر1data)

	elf2 := Elf{}

	کاربر1entry := elf2.Getentry(کاربر1data)
	elf2.Parse(کاربر1data[:], uint32(Pصفحهشاخهentry+0x1000))
	سراسریoffsetجدول := elf2.Got

	Pمقدار1پیوندmap := پیوندmap.Clone()
	Pمقدار1پیوندmap.Append_to_list(uintptr(elf2.Dپویا))

	حافظهmanager.Fآزاد(کاربر1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(حافظهmanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(Pصفحهشاخهentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpuحالت.Ecx = کاربر1entry
	thr2.Cpuحالت.Edx = سراسریoffsetجدول
	thr2.Cpuحالت.Esi = uint32(uintptr(Pointer(Pمقدار1پیوندmap.First)))

	console.Mچاپxy("user1: ", 1, 10)
	console.MUnsignedinteger32چاپ(elf2.Got)

	var کاربر2پرونده []byte = ([]byte)("USER2")
	اندازه = Getپروندهاندازه(کاربر2پرونده)
	کاربر2address := حافظهmanager.Malloc(اندازه)
	کاربر2data := Getبایتfrompointer(uintptr(کاربر2address), int(اندازه), int(اندازه))
	Rخواندنپرونده(کاربر2پرونده, کاربر2data)

	elf3 := Elf{}

	کاربر2entry := elf3.Getentry(کاربر2data)
	elf3.Parse(کاربر2data[:], uint32(Pصفحهشاخهentry+0x2000))
	سراسریoffsetجدول = elf3.Got

	Pمقدار2پیوندmap := پیوندmap.Clone()
	Pمقدار2پیوندmap.Append_to_list(uintptr(elf3.Dپویا))

	حافظهmanager.Fآزاد(کاربر2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(حافظهmanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(Pصفحهشاخهentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpuحالت.Ecx = کاربر2entry
	thr3.Cpuحالت.Edx = سراسریoffsetجدول
	thr3.Cpuحالت.Esi = uint32(uintptr(Pointer(Pمقدار2پیوندmap.First)))

	console.Mچاپxy("user2: ", 1, 11)
	console.MUnsignedinteger32چاپ(thr3.Cpuحالت.Esi)

	libپیوندmap.Pچاپ(1, 11)

	var کاربر3پرونده []byte = ([]byte)("USER3")
	اندازه = Getپروندهاندازه(کاربر3پرونده)
	کاربر3address := حافظهmanager.Malloc(اندازه)
	کاربر3data := Getبایتfrompointer(uintptr(کاربر3address), int(اندازه), int(اندازه))
	Rخواندنپرونده(کاربر3پرونده, کاربر3data)

	elf4 := Elf{}

	کاربر3entry := elf4.Getentry(کاربر3data)
	elf4.Parse(کاربر3data[:], uint32(Pصفحهشاخهentry+0x3000))
	سراسریoffsetجدول = elf4.Got

	Pمقدار3پیوندmap := پیوندmap.Clone()
	Pمقدار3پیوندmap.Append_to_list(uintptr(elf4.Dپویا))

	حافظهmanager.Fآزاد(کاربر3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(حافظهmanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(Pصفحهشاخهentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpuحالت.Ecx = کاربر3entry
	thr4.Cpuحالت.Edx = سراسریoffsetجدول
	thr4.Cpuحالت.Esi = uint32(uintptr(Pointer(Pمقدار3پیوندmap.First)))

	processhelper.Spawn(Tتابع1, threadhelper, sche, uint32(Pصفحهشاخهentry+0x4000), true)

	iصفحهکلیدeventhandler = &myصفحهکلیدeventhandler
	صفحهکلیدdriver.Initdriver(Interruptmanager, iصفحهکلیدeventhandler)

	موشیdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	دستگاهdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Eفعالشده(true)
	Interruptmanager.Aفعال()

	for {
		halt()
	}

}
