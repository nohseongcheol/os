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
import . "katkestus"
import . "multitasking"
import . "tasking/tss"

import . "virtuaalMälu"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/protsess"
import . "driver/driver"

import . "driver/klaviatuur"
import . "driver/hiir"

import . "driver/ata"
import . "failSüsteem/msdospartition"
import . "failSüsteem/fat"

import . "failSüsteem/elf"

import . "süsteemcall"

import . "mälumanager"
import . "pci"

func halt()

var iKlaviatuurSündmushandler IKlaviatuurSündmushandler

type TMyKlaviatuurSündmushandler struct {
}

var myKlaviatuurSündmushandler TMyKlaviatuurSündmushandler
var klaviatuurdriver TKlaviatuurdriver
var hiirdriver THiirdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klaviatuurconsole TConsole = TConsole{}

func (ise *TMyKlaviatuurSündmushandler) SeesVõtiNoolalla(võti byte) {
	foo := [1]byte{' '}
	foo[0] = võti

	klaviatuurconsole.MPrindibaitixy(foo[:], 1000, 1000)
}

func (ise *TMyKlaviatuurSündmushandler) SeesVõtiÜles(võti byte)	{}

var iHiirSündmushandler IHiirSündmushandler

type TMyHiirSündmushandler struct {
}

var hiirconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xAsukoht int16 = 0
var yAsukoht int16 = 0

func (ise *TMyHiirSündmushandler) SeesHiirNoolalla(nupp int8) {
	buffer := []byte("x")
	hiirconsole.MPrindixy(buffer, uint16(previousx), uint16(previousy))
}
func (ise *TMyHiirSündmushandler) SeesHiirÜles(nupp int8)	{}
func (ise *TMyHiirSündmushandler) SeesHiirLiiguta(x int8, y int8) {

	xAsukoht += int16(x)
	if xAsukoht < 0 {
		xAsukoht = 0
	}
	if xAsukoht >= 80 {
		xAsukoht = 79
	}

	yAsukoht -= int16(y)

	if yAsukoht < 0 {
		yAsukoht = 0
	}
	if yAsukoht >= 25 {
		yAsukoht = 24
	}

	buffer := []byte(" ")
	hiirconsole.MPrindixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	hiirconsole.MPrindixy(buffer, uint16(xAsukoht), uint16(yAsukoht))

	previousx = xAsukoht
	previousy = yAsukoht
}

var seadedescriptor TPeripheralcomponentinterconnectSeadedescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (ise TMypcicontrollerhandler) Seesgetdriver(seade TPeripheralcomponentinterconnectSeadedescriptor) {
	if seade.Tootjaid == 0x1022 && seade.Seadeid == 0x2000 {
		console.MPrindixy([]byte("["), 0, 12)
		console.MPrindi(([]byte)("AMD am79c973"))
		console.MPrindi([]byte(":"))
		console.MUnsignedinteger16Prindi(seade.Tootjaid)
		console.MPrindi([]byte(":"))
		console.MUnsignedinteger16Prindi(seade.Seadeid)
		console.MPrindi([]byte(":"))
		console.MUnsignedinteger16Prindi(uint16(seade.Portbase))
		console.MPrindi([]byte(":"))
		console.MUnsignedinteger32Prindi(seade.Katkestus)

		console.MPrindi([]byte("]\n"))
		seadedescriptor = seade
		drivercount++
	}
}
func (ise TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectSeadedescriptor {
	return seadedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Prindistr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MPrindi(str)
}

func GetFailSuurus(failinimi []byte) uint32 {
	var ata0s = TLaiendatudTehnoloogiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lugeminepartition(&ata0s)

	bios := TBiosparameterKast32{}

	var suurus uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failinimi)
	ata0s.Flush()

	return suurus
}

func LugemineFail(failinimi []byte, data []byte) {
	var ata0s = TLaiendatudTehnoloogiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lugeminepartition(&ata0s)

	bios := TBiosparameterKast32{}
	bios.Lugemine(&ata0s, partition.Mbr.Primarypartition[0], failinimi, data)

	ata0s.Flush()
}
func Koormuself() {

	var ata0s = TLaiendatudTehnoloogiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lugeminepartition(&ata0s)

	bios := TBiosparameterKast32{}

	var failinimi []byte = ([]byte)("TEST")
	var suurus uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failinimi)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lugemine(&ata0s, partition.Mbr.Primarypartition[0], failinimi, data)

	elf := Elf{}

	elf.Parse(data[:suurus], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TFunktsioon1() {
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

		SysPrindiunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func sisendSündmustask() {
	for {
		ProtsesspendingKlaviatuurSündmused()
		ProtsesspendingHiirSündmused()
		halt()
	}
}

func memorytest(y int) {
	mälumanager := &TMälumanager{}
	allocated := uint32(uintptr(mälumanager.Malloc(1024)))
	console.MUnsignedinteger32Prindixy(allocated, 10, uint16(y))
	if y == 11 {
		mälumanager.Vaba(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pausloop()
func Laadiuuesticr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Määracr3(cr3 uint32)
func Getcr4() uint32
func Lubatudpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunktsioonNimi(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNimi = runtime.FuncForPC(address).Name()
	var funcbaiti []byte = []byte(funcNimi)

	taskconsole.MPrindixy(funcbaiti, 1, 5)
	taskconsole.MPrindi(([]byte)(":"))
	taskconsole.MUnsignedinteger32Prindi(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MPrindiunsignedinteger32(cr0, 2, 1)
}

var tss *Tsskirje = &Tsskirje{}

func KKernelEntry(LehekülgKataloogkirje uintptr, stacktop uintptr, stackbottom uintptr) {

	MJärjenumberloginit()
	console.MPrindi("\n=== EST BOOT ===\n")

	console.MPrindiunsignedinteger32(uint32(LehekülgKataloogkirje), 0, 2)
	console.MPrindiunsignedinteger32(uint32(LehekülgKataloogkirje), 10, 2)
	console.MPrindiunsignedinteger32(uint32(stacktop), 0, 3)
	console.MPrindiunsignedinteger32(uint32(stackbottom), 10, 3)

	mälumanager := &TMälumanager{}
	mälumanager.Init(0, SuurimqueueSuurus)

	paging := &Paging{}
	paging.Init(LehekülgKataloogkirje, 0x500000, mälumanager)
	paging.SharedMäluregion()

	Määracr3(uint32(LehekülgKataloogkirje))
	Lubatudpaging()

	shareddescriptorTabel := &TShareddescriptorTabel{}
	shareddescriptorTabel.Init()

	console.MPrindi("esp:")

	esp := getesp()
	console.MUnsignedinteger32Prindi(uint32(esp))

	tls := gettls()
	console.MPrindi(([]byte)("tls:"))
	console.MUnsignedinteger32Prindi(tls)

	tss.Paigalda(shareddescriptorTabel, 7, Segkerneldata, esp)

	VirtTesti()

	cr3 := Laadiuuesticr3()
	console.MPrindi(([]byte)(":cr3:"))
	console.MUnsignedinteger32Prindi(cr3)

	cr0 := Getcr0()
	console.MPrindi(([]byte)(":cr0:"))
	console.MUnsignedinteger32Prindi(cr0)

	cr4 := Getcr4()
	console.MPrindi(([]byte)(":cr4:"))
	console.MUnsignedinteger32Prindi(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Katkestusmanager := &TKatkestusmanager{}
	Katkestusmanager.Init(0x20, shareddescriptorTabel, taskmanager_2)

	paging.Lehekülgfault(Katkestusmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(mälumanager)

	protsesshelper := Protsesshelper{}
	protsesshelper.Init(mälumanager, LehekülgKataloogkirje)

	sche := &Scheduler{}
	sche.Init(Katkestusmanager, mälumanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Katkestusmanager)

	protsesshelper.Spawn(taska, threadhelper, sche, uint32(LehekülgKataloogkirje), true)
	protsesshelper.Spawn(taskb, threadhelper, sche, uint32(LehekülgKataloogkirje), true)
	protsesshelper.Spawn(taskc, threadhelper, sche, uint32(LehekülgKataloogkirje), true)
	protsesshelper.Spawn(taskd1, threadhelper, sche, uint32(LehekülgKataloogkirje), true)
	protsesshelper.Spawn(sisendSündmustask, threadhelper, sche, uint32(LehekülgKataloogkirje), true)

	var suurus uint32

	var linkerFail []byte = ([]byte)("LINKER")
	suurus = GetFailSuurus(linkerFail)
	linkeraddress := mälumanager.Malloc(suurus)
	linkerdata := GetbaitifromKursor(uintptr(linkeraddress), int(suurus), int(suurus))
	LugemineFail(linkerFail, linkerdata)

	elf0 := Elf{}
	linkerkirje := elf0.Getkirje(linkerdata)
	elf0.Parse(linkerdata[:], uint32(LehekülgKataloogkirje))

	viitmap := Viitmap{}
	viitmap.Init(mälumanager)

	var lib1Fail []byte = ([]byte)("LIB1")
	suurus = GetFailSuurus(lib1Fail)

	lib1address := mälumanager.Malloc(suurus)
	lib1data := GetbaitifromKursor(uintptr(lib1address), int(suurus), int(suurus))
	LugemineFail(lib1Fail, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(LehekülgKataloogkirje))
	mälumanager.Vaba(lib1address)

	viitmap.Append_to_list(uintptr(lib1elf.Dünaamiline))

	var lib2Fail []byte = ([]byte)("LIB2")
	suurus = GetFailSuurus(lib2Fail)

	lib2address := mälumanager.Malloc(suurus)
	lib2data := GetbaitifromKursor(uintptr(lib2address), int(suurus), int(suurus))
	LugemineFail(lib2Fail, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(LehekülgKataloogkirje))
	mälumanager.Vaba(lib2address)

	viitmap.Append_to_list(uintptr(lib2elf.Dünaamiline))

	libViitmap := viitmap.Clone()
	viitmapaddress := uint32(uintptr(Pointer(libViitmap.First)))

	lib1got := Getunsignedinteger32MassiivfromKursor(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = viitmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32MassiivfromKursor(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = viitmapaddress
	lib2got[2] = 0x4000000

	console.MPrindixy("lib1: ", 1, 8)
	console.MUnsignedinteger32Prindi(lib1elf.Got)
	console.MPrindi(":")
	console.MUnsignedinteger32Prindi(lib1elf.Dünaamiline)

	console.MPrindixy("lib2: ", 1, 9)
	console.MUnsignedinteger32Prindi(lib2elf.Got)
	console.MPrindi(":")
	console.MUnsignedinteger32Prindi(lib2elf.Dünaamiline)

	var kasutaja1Fail []byte = ([]byte)("USER1")
	suurus = GetFailSuurus(kasutaja1Fail)
	kasutaja1address := mälumanager.Malloc(suurus)
	kasutaja1data := GetbaitifromKursor(uintptr(kasutaja1address), int(suurus), int(suurus))
	LugemineFail(kasutaja1Fail, kasutaja1data)

	elf2 := Elf{}

	kasutaja1kirje := elf2.Getkirje(kasutaja1data)
	elf2.Parse(kasutaja1data[:], uint32(LehekülgKataloogkirje+0x1000))
	globaalneoffsetTabel := elf2.Got

	PVäärtus1Viitmap := viitmap.Clone()
	PVäärtus1Viitmap.Append_to_list(uintptr(elf2.Dünaamiline))

	mälumanager.Vaba(kasutaja1address)

	var code1Kursor *uintptr
	var func1val func()

	code1Kursor = (*uintptr)(mälumanager.Malloc(4))
	*code1Kursor = uintptr(linkerkirje)
	func1val = *(*func())(Pointer(&code1Kursor))

	proc2 := protsesshelper.Spawn(func1val, threadhelper, sche, uint32(LehekülgKataloogkirje+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProtsessorOlek.Ecx = kasutaja1kirje
	thr2.ProtsessorOlek.Edx = globaalneoffsetTabel
	thr2.ProtsessorOlek.Esi = uint32(uintptr(Pointer(PVäärtus1Viitmap.First)))

	console.MPrindixy("user1: ", 1, 10)
	console.MUnsignedinteger32Prindi(elf2.Got)

	var kasutaja2Fail []byte = ([]byte)("USER2")
	suurus = GetFailSuurus(kasutaja2Fail)
	kasutaja2address := mälumanager.Malloc(suurus)
	kasutaja2data := GetbaitifromKursor(uintptr(kasutaja2address), int(suurus), int(suurus))
	LugemineFail(kasutaja2Fail, kasutaja2data)

	elf3 := Elf{}

	kasutaja2kirje := elf3.Getkirje(kasutaja2data)
	elf3.Parse(kasutaja2data[:], uint32(LehekülgKataloogkirje+0x2000))
	globaalneoffsetTabel = elf3.Got

	PVäärtus2Viitmap := viitmap.Clone()
	PVäärtus2Viitmap.Append_to_list(uintptr(elf3.Dünaamiline))

	mälumanager.Vaba(kasutaja2address)

	var code2Kursor *uintptr
	var func2val func()

	code2Kursor = (*uintptr)(mälumanager.Malloc(4))
	*code2Kursor = uintptr(linkerkirje)
	func2val = *(*func())(Pointer(&code2Kursor))

	proc3 := protsesshelper.Spawn(func2val, threadhelper, sche, uint32(LehekülgKataloogkirje+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProtsessorOlek.Ecx = kasutaja2kirje
	thr3.ProtsessorOlek.Edx = globaalneoffsetTabel
	thr3.ProtsessorOlek.Esi = uint32(uintptr(Pointer(PVäärtus2Viitmap.First)))

	console.MPrindixy("user2: ", 1, 11)
	console.MUnsignedinteger32Prindi(thr3.ProtsessorOlek.Esi)

	libViitmap.Prindi(1, 11)

	var kasutaja3Fail []byte = ([]byte)("USER3")
	suurus = GetFailSuurus(kasutaja3Fail)
	kasutaja3address := mälumanager.Malloc(suurus)
	kasutaja3data := GetbaitifromKursor(uintptr(kasutaja3address), int(suurus), int(suurus))
	LugemineFail(kasutaja3Fail, kasutaja3data)

	elf4 := Elf{}

	kasutaja3kirje := elf4.Getkirje(kasutaja3data)
	elf4.Parse(kasutaja3data[:], uint32(LehekülgKataloogkirje+0x3000))
	globaalneoffsetTabel = elf4.Got

	PVäärtus3Viitmap := viitmap.Clone()
	PVäärtus3Viitmap.Append_to_list(uintptr(elf4.Dünaamiline))

	mälumanager.Vaba(kasutaja3address)

	var code3Kursor *uintptr
	var func3val func()

	code3Kursor = (*uintptr)(mälumanager.Malloc(4))
	*code3Kursor = uintptr(linkerkirje)
	func3val = *(*func())(Pointer(&code3Kursor))

	proc4 := protsesshelper.Spawn(func3val, threadhelper, sche, uint32(LehekülgKataloogkirje+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProtsessorOlek.Ecx = kasutaja3kirje
	thr4.ProtsessorOlek.Edx = globaalneoffsetTabel
	thr4.ProtsessorOlek.Esi = uint32(uintptr(Pointer(PVäärtus3Viitmap.First)))

	protsesshelper.Spawn(TFunktsioon1, threadhelper, sche, uint32(LehekülgKataloogkirje+0x4000), true)

	iKlaviatuurSündmushandler = &myKlaviatuurSündmushandler
	klaviatuurdriver.Initdriver(Katkestusmanager, iKlaviatuurSündmushandler)

	hiirdriver.Initdriver(Katkestusmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Validriver(&Drivermanager, Katkestusmanager)
	seadedescriptor = mypcicontrollerhandler.Getdriver()

	sche.Lubatud(true)
	Katkestusmanager.Aktiivne()

	for {
		halt()
	}

}
