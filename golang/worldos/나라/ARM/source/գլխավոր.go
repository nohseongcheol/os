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
import . "ընդհատել"
import . "multitasking"
import . "tasking/tss"

import . "virtualՀիշողություն"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/գործընթաց"
import . "driver/driver"

import . "driver/ստեղնաշար"
import . "driver/մկնիկ"

import . "driver/ata"
import . "ֆայլՀամակարգ/msdospartition"
import . "ֆայլՀամակարգ/fat"

import . "ֆայլՀամակարգ/elf"

import . "համակարգcall"

import . "հիշողությունmanager"
import . "pci"

func halt()

var iՍտեղնաշարeventhandler IՍտեղնաշարeventhandler

type TMyՍտեղնաշարeventhandler struct {
}

var myՍտեղնաշարeventhandler TMyՍտեղնաշարeventhandler
var ստեղնաշարdriver TՍտեղնաշարdriver
var մկնիկdriver TՄկնիկdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var ստեղնաշարconsole TConsole = TConsole{}

func (ինքնուրույն *TMyՍտեղնաշարeventhandler) ՄիացնելԲանալիՆերքև(բանալի byte) {
	foo := [1]byte{' '}
	foo[0] = բանալի

	ստեղնաշարconsole.MՏպելԲայթերxy(foo[:], 1000, 1000)
}

func (ինքնուրույն *TMyՍտեղնաշարeventhandler) ՄիացնելԲանալիՎերև(բանալի byte)	{}

var iՄկնիկeventhandler IՄկնիկeventhandler

type TMyՄկնիկeventhandler struct {
}

var մկնիկconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xԴիրք int16 = 0
var yԴիրք int16 = 0

func (ինքնուրույն *TMyՄկնիկeventhandler) ՄիացնելՄկնիկՆերքև(button int8) {
	buffer := []byte("x")
	մկնիկconsole.MՏպելxy(buffer, uint16(previousx), uint16(previousy))
}
func (ինքնուրույն *TMyՄկնիկeventhandler) ՄիացնելՄկնիկՎերև(button int8)	{}
func (ինքնուրույն *TMyՄկնիկeventhandler) ՄիացնելՄկնիկՏեղաշարժել(x int8, y int8) {

	xԴիրք += int16(x)
	if xԴիրք < 0 {
		xԴիրք = 0
	}
	if xԴիրք >= 80 {
		xԴիրք = 79
	}

	yԴիրք -= int16(y)

	if yԴիրք < 0 {
		yԴիրք = 0
	}
	if yԴիրք >= 25 {
		yԴիրք = 24
	}

	buffer := []byte(" ")
	մկնիկconsole.MՏպելxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	մկնիկconsole.MՏպելxy(buffer, uint16(xԴիրք), uint16(yԴիրք))

	previousx = xԴիրք
	previousy = yԴիրք
}

var սարքdescriptor TPeripheralcomponentinterconnectՍարքdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (ինքնուրույն TMypcicontrollerhandler) Միացնելgetdriver(սարք TPeripheralcomponentinterconnectՍարքdescriptor) {
	if սարք.Վաճառողid == 0x1022 && սարք.Սարքid == 0x2000 {
		console.MՏպելxy([]byte("["), 0, 12)
		console.MՏպել(([]byte)("AMD am79c973"))
		console.MՏպել([]byte(":"))
		console.MUnsignedinteger16Տպել(սարք.Վաճառողid)
		console.MՏպել([]byte(":"))
		console.MUnsignedinteger16Տպել(սարք.Սարքid)
		console.MՏպել([]byte(":"))
		console.MUnsignedinteger16Տպել(uint16(սարք.Պորտbase))
		console.MՏպել([]byte(":"))
		console.MUnsignedinteger32Տպել(սարք.Ընդհատել)

		console.MՏպել([]byte("]\n"))
		սարքdescriptor = սարք
		drivercount++
	}
}
func (ինքնուրույն TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectՍարքdescriptor {
	return սարքdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Տպելstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MՏպել(str)
}

func GetՖայլՉափս(ֆայլիանուն []byte) uint32 {
	var ata0s = TԸնդլայնվածՏեխնոլոգիաattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionԱղյուսակ{}
	partition.Ընթերցումpartition(&ata0s)

	bios := TBiosparameterԱրգելափակել32{}

	var չափս uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն)
	ata0s.Flush()

	return չափս
}

func ԸնթերցումՖայլ(ֆայլիանուն []byte, data []byte) {
	var ata0s = TԸնդլայնվածՏեխնոլոգիաattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionԱղյուսակ{}
	partition.Ընթերցումpartition(&ata0s)

	bios := TBiosparameterԱրգելափակել32{}
	bios.Ընթերցում(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն, data)

	ata0s.Flush()
}
func Բեռնումelf() {

	var ata0s = TԸնդլայնվածՏեխնոլոգիաattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionԱղյուսակ{}
	partition.Ընթերցումpartition(&ata0s)

	bios := TBiosparameterԱրգելափակել32{}

	var ֆայլիանուն []byte = ([]byte)("TEST")
	var չափս uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Ընթերցում(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն, data)

	elf := Elf{}

	elf.Parse(data[:չափս], 0x4f00000)

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

		SysՏպելunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func հիմաeventtask() {
	for {
		ԳործընթացpendingՍտեղնաշարevents()
		ԳործընթացpendingՄկնիկevents()
		halt()
	}
}

func memorytest(y int) {
	հիշողությունmanager := &TՀիշողությունmanager{}
	allocated := uint32(uintptr(հիշողությունmanager.Malloc(1024)))
	console.MUnsignedinteger32Տպելxy(allocated, 10, uint16(y))
	if y == 11 {
		հիշողությունmanager.Ազատ(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Վերբեռնելcr3() uint32

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

func GetfunctionԱնուն(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcԱնուն = runtime.FuncForPC(address).Name()
	var funcԲայթեր []byte = []byte(funcԱնուն)

	taskconsole.MՏպելxy(funcԲայթեր, 1, 5)
	taskconsole.MՏպել(([]byte)(":"))
	taskconsole.MUnsignedinteger32Տպել(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MՏպելunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Էջֆայլապանակentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MՏպել("\n=== ARM BOOT ===\n")

	console.MՏպելunsignedinteger32(uint32(Էջֆայլապանակentry), 0, 2)
	console.MՏպելunsignedinteger32(uint32(Էջֆայլապանակentry), 10, 2)
	console.MՏպելunsignedinteger32(uint32(stacktop), 0, 3)
	console.MՏպելunsignedinteger32(uint32(stackbottom), 10, 3)

	հիշողությունmanager := &TՀիշողությունmanager{}
	հիշողությունmanager.Init(0, MaxqueueՉափս)

	paging := &Paging{}
	paging.Init(Էջֆայլապանակentry, 0x500000, հիշողությունmanager)
	paging.SharedՀիշողությունregion()

	Setcr3(uint32(Էջֆայլապանակentry))
	Enablepaging()

	shareddescriptorԱղյուսակ := &TShareddescriptorԱղյուսակ{}
	shareddescriptorԱղյուսակ.Init()

	console.MՏպել("esp:")

	esp := getesp()
	console.MUnsignedinteger32Տպել(uint32(esp))

	tls := gettls()
	console.MՏպել(([]byte)("tls:"))
	console.MUnsignedinteger32Տպել(tls)

	tss.Տեղադրել(shareddescriptorԱղյուսակ, 7, Segkerneldata, esp)

	VirtԹեստ()

	cr3 := Վերբեռնելcr3()
	console.MՏպել(([]byte)(":cr3:"))
	console.MUnsignedinteger32Տպել(cr3)

	cr0 := Getcr0()
	console.MՏպել(([]byte)(":cr0:"))
	console.MUnsignedinteger32Տպել(cr0)

	cr4 := Getcr4()
	console.MՏպել(([]byte)(":cr4:"))
	console.MUnsignedinteger32Տպել(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Ընդհատելmanager := &TԸնդհատելmanager{}
	Ընդհատելmanager.Init(0x20, shareddescriptorԱղյուսակ, taskmanager_2)

	paging.Էջfault(Ընդհատելmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(հիշողությունmanager)

	գործընթացhelper := Գործընթացhelper{}
	գործընթացhelper.Init(հիշողությունmanager, Էջֆայլապանակentry)

	sche := &Scheduler{}
	sche.Init(Ընդհատելmanager, հիշողությունmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Ընդհատելmanager)

	գործընթացhelper.Spawn(taska, threadhelper, sche, uint32(Էջֆայլապանակentry), true)
	գործընթացhelper.Spawn(taskb, threadhelper, sche, uint32(Էջֆայլապանակentry), true)
	գործընթացhelper.Spawn(taskc, threadhelper, sche, uint32(Էջֆայլապանակentry), true)
	գործընթացhelper.Spawn(taskd1, threadhelper, sche, uint32(Էջֆայլապանակentry), true)
	գործընթացhelper.Spawn(հիմաeventtask, threadhelper, sche, uint32(Էջֆայլապանակentry), true)

	var չափս uint32

	var linkerՖայլ []byte = ([]byte)("LINKER")
	չափս = GetՖայլՉափս(linkerՖայլ)
	linkeraddress := հիշողությունmanager.Malloc(չափս)
	linkerdata := GetԲայթերիցՑուցիչ(uintptr(linkeraddress), int(չափս), int(չափս))
	ԸնթերցումՖայլ(linkerՖայլ, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Էջֆայլապանակentry))

	հղումmap := Հղումmap{}
	հղումmap.Init(հիշողությունmanager)

	var lib1Ֆայլ []byte = ([]byte)("LIB1")
	չափս = GetՖայլՉափս(lib1Ֆայլ)

	lib1address := հիշողությունmanager.Malloc(չափս)
	lib1data := GetԲայթերիցՑուցիչ(uintptr(lib1address), int(չափս), int(չափս))
	ԸնթերցումՖայլ(lib1Ֆայլ, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Էջֆայլապանակentry))
	հիշողությունmanager.Ազատ(lib1address)

	հղումmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Ֆայլ []byte = ([]byte)("LIB2")
	չափս = GetՖայլՉափս(lib2Ֆայլ)

	lib2address := հիշողությունmanager.Malloc(չափս)
	lib2data := GetԲայթերիցՑուցիչ(uintptr(lib2address), int(չափս), int(չափս))
	ԸնթերցումՖայլ(lib2Ֆայլ, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Էջֆայլապանակentry))
	հիշողությունmanager.Ազատ(lib2address)

	հղումmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libհղումmap := հղումmap.Clone()
	հղումmapaddress := uint32(uintptr(Pointer(libհղումmap.First)))

	lib1got := Getunsignedinteger32ԶանգվածիցՑուցիչ(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = հղումmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ԶանգվածիցՑուցիչ(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = հղումmapaddress
	lib2got[2] = 0x4000000

	console.MՏպելxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Տպել(lib1elf.Got)
	console.MՏպել(":")
	console.MUnsignedinteger32Տպել(lib1elf.Dynamic)

	console.MՏպելxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Տպել(lib2elf.Got)
	console.MՏպել(":")
	console.MUnsignedinteger32Տպել(lib2elf.Dynamic)

	var օգտագործող1Ֆայլ []byte = ([]byte)("USER1")
	չափս = GetՖայլՉափս(օգտագործող1Ֆայլ)
	օգտագործող1address := հիշողությունmanager.Malloc(չափս)
	օգտագործող1data := GetԲայթերիցՑուցիչ(uintptr(օգտագործող1address), int(չափս), int(չափս))
	ԸնթերցումՖայլ(օգտագործող1Ֆայլ, օգտագործող1data)

	elf2 := Elf{}

	օգտագործող1entry := elf2.Getentry(օգտագործող1data)
	elf2.Parse(օգտագործող1data[:], uint32(Էջֆայլապանակentry+0x1000))
	գլոբալoffsetԱղյուսակ := elf2.Got

	PԱրժեք1հղումmap := հղումmap.Clone()
	PԱրժեք1հղումmap.Append_to_list(uintptr(elf2.Dynamic))

	հիշողությունmanager.Ազատ(օգտագործող1address)

	var code1Ցուցիչ *uintptr
	var func1val func()

	code1Ցուցիչ = (*uintptr)(հիշողությունmanager.Malloc(4))
	*code1Ցուցիչ = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Ցուցիչ))

	proc2 := գործընթացhelper.Spawn(func1val, threadhelper, sche, uint32(Էջֆայլապանակentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ԿՄՀՎիճակ.Ecx = օգտագործող1entry
	thr2.ԿՄՀՎիճակ.Edx = գլոբալoffsetԱղյուսակ
	thr2.ԿՄՀՎիճակ.Esi = uint32(uintptr(Pointer(PԱրժեք1հղումmap.First)))

	console.MՏպելxy("user1: ", 1, 10)
	console.MUnsignedinteger32Տպել(elf2.Got)

	var օգտագործող2Ֆայլ []byte = ([]byte)("USER2")
	չափս = GetՖայլՉափս(օգտագործող2Ֆայլ)
	օգտագործող2address := հիշողությունmanager.Malloc(չափս)
	օգտագործող2data := GetԲայթերիցՑուցիչ(uintptr(օգտագործող2address), int(չափս), int(չափս))
	ԸնթերցումՖայլ(օգտագործող2Ֆայլ, օգտագործող2data)

	elf3 := Elf{}

	օգտագործող2entry := elf3.Getentry(օգտագործող2data)
	elf3.Parse(օգտագործող2data[:], uint32(Էջֆայլապանակentry+0x2000))
	գլոբալoffsetԱղյուսակ = elf3.Got

	PԱրժեք2հղումmap := հղումmap.Clone()
	PԱրժեք2հղումmap.Append_to_list(uintptr(elf3.Dynamic))

	հիշողությունmanager.Ազատ(օգտագործող2address)

	var code2Ցուցիչ *uintptr
	var func2val func()

	code2Ցուցիչ = (*uintptr)(հիշողությունmanager.Malloc(4))
	*code2Ցուցիչ = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Ցուցիչ))

	proc3 := գործընթացhelper.Spawn(func2val, threadhelper, sche, uint32(Էջֆայլապանակentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ԿՄՀՎիճակ.Ecx = օգտագործող2entry
	thr3.ԿՄՀՎիճակ.Edx = գլոբալoffsetԱղյուսակ
	thr3.ԿՄՀՎիճակ.Esi = uint32(uintptr(Pointer(PԱրժեք2հղումmap.First)))

	console.MՏպելxy("user2: ", 1, 11)
	console.MUnsignedinteger32Տպել(thr3.ԿՄՀՎիճակ.Esi)

	libհղումmap.Տպել(1, 11)

	var օգտագործող3Ֆայլ []byte = ([]byte)("USER3")
	չափս = GetՖայլՉափս(օգտագործող3Ֆայլ)
	օգտագործող3address := հիշողությունmanager.Malloc(չափս)
	օգտագործող3data := GetԲայթերիցՑուցիչ(uintptr(օգտագործող3address), int(չափս), int(չափս))
	ԸնթերցումՖայլ(օգտագործող3Ֆայլ, օգտագործող3data)

	elf4 := Elf{}

	օգտագործող3entry := elf4.Getentry(օգտագործող3data)
	elf4.Parse(օգտագործող3data[:], uint32(Էջֆայլապանակentry+0x3000))
	գլոբալoffsetԱղյուսակ = elf4.Got

	PԱրժեք3հղումmap := հղումmap.Clone()
	PԱրժեք3հղումmap.Append_to_list(uintptr(elf4.Dynamic))

	հիշողությունmanager.Ազատ(օգտագործող3address)

	var code3Ցուցիչ *uintptr
	var func3val func()

	code3Ցուցիչ = (*uintptr)(հիշողությունmanager.Malloc(4))
	*code3Ցուցիչ = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Ցուցիչ))

	proc4 := գործընթացhelper.Spawn(func3val, threadhelper, sche, uint32(Էջֆայլապանակentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ԿՄՀՎիճակ.Ecx = օգտագործող3entry
	thr4.ԿՄՀՎիճակ.Edx = գլոբալoffsetԱղյուսակ
	thr4.ԿՄՀՎիճակ.Esi = uint32(uintptr(Pointer(PԱրժեք3հղումmap.First)))

	գործընթացhelper.Spawn(TFunction1, threadhelper, sche, uint32(Էջֆայլապանակentry+0x4000), true)

	iՍտեղնաշարeventhandler = &myՍտեղնաշարeventhandler
	ստեղնաշարdriver.Initdriver(Ընդհատելmanager, iՍտեղնաշարeventhandler)

	մկնիկdriver.Initdriver(Ընդհատելmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Ընդհատելmanager)
	սարքdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Միացված(true)
	Ընդհատելmanager.Ակտիվ()

	for {
		halt()
	}

}
