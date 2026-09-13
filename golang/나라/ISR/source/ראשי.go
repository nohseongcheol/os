package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "פסק"
import . "multitasking"
import . "tasking/tss"

import . "וירטואליזיכרון"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/תהליך"
import . "driver/driver"

import . "driver/מקלדת"
import . "driver/עכבר"

import . "driver/ata"
import . "קובץמערכת/msdospartition"
import . "קובץמערכת/fat"

import . "קובץמערכת/elf"

import . "מערכתcall"

import . "זיכרוןmanager"
import . "pci"

func halt()

var iמקלדתeventhandler Iמקלדתeventhandler

type TMyמקלדתeventhandler struct {
}

var myמקלדתeventhandler TMyמקלדתeventhandler
var מקלדתdriver Tמקלדתdriver
var עכברdriver Tעכברdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var מקלדתconsole TConsole = TConsole{}

func (self *TMyמקלדתeventhandler) Oפעילמפתחלמטה(מפתח_2 byte) {
	foo := [1]byte{' '}
	foo[0] = מפתח_2

	מקלדתconsole.Mהדפסהבתיםxy(foo[:], 1000, 1000)
}

func (self *TMyמקלדתeventhandler) Oפעילמפתחמעלה(מפתח_2 byte)	{}

var iעכברeventhandler Iעכברeventhandler

type TMyעכברeventhandler struct {
}

var עכברconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xמיקום int16 = 0
var yמיקום int16 = 0

func (self *TMyעכברeventhandler) Oפעילעכברלמטה(לחצן int8) {
	buffer := []byte("x")
	עכברconsole.Mהדפסהxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyעכברeventhandler) Oפעילעכברמעלה(לחצן int8)	{}
func (self *TMyעכברeventhandler) Oפעילעכברהזז(x int8, y int8) {

	xמיקום += int16(x)
	if xמיקום < 0 {
		xמיקום = 0
	}
	if xמיקום >= 80 {
		xמיקום = 79
	}

	yמיקום -= int16(y)

	if yמיקום < 0 {
		yמיקום = 0
	}
	if yמיקום >= 25 {
		yמיקום = 24
	}

	buffer := []byte(" ")
	עכברconsole.Mהדפסהxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	עכברconsole.Mהדפסהxy(buffer, uint16(xמיקום), uint16(yמיקום))

	previousx = xמיקום
	previousy = yמיקום
}

var התקןdescriptor TPeripheralcomponentinterconnectהתקןdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Oפעילgetdriver(התקן TPeripheralcomponentinterconnectהתקןdescriptor) {
	if התקן.Vיצרןמזהה == 0x1022 && התקן.Dהתקןמזהה == 0x2000 {
		console.Mהדפסהxy([]byte("["), 0, 12)
		console.Mהדפסה(([]byte)("AMD am79c973"))
		console.Mהדפסה([]byte(":"))
		console.MUnsignedinteger16הדפסה(התקן.Vיצרןמזהה)
		console.Mהדפסה([]byte(":"))
		console.MUnsignedinteger16הדפסה(התקן.Dהתקןמזהה)
		console.Mהדפסה([]byte(":"))
		console.MUnsignedinteger16הדפסה(uint16(התקן.Pשערbase))
		console.Mהדפסה([]byte(":"))
		console.MUnsignedinteger32הדפסה(התקן.Iפסק)

		console.Mהדפסה([]byte("]\n"))
		התקןdescriptor = התקן
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectהתקןdescriptor {
	return התקןdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pהדפסהstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.Mהדפסה(str)
}

func Getקובץגודל(שםהקובץ []byte) uint32 {
	var ata0s = Tמתקדםטכנולוגיהattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Rקריאהpartition(&ata0s)

	bios := TBiosparameterבלוק32{}

	var גודל uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ)
	ata0s.Flush()

	return גודל
}

func Rקריאהקובץ(שםהקובץ []byte, data []byte) {
	var ata0s = Tמתקדםטכנולוגיהattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Rקריאהpartition(&ata0s)

	bios := TBiosparameterבלוק32{}
	bios.Rקריאה(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ, data)

	ata0s.Flush()
}
func Lעומסelf() {

	var ata0s = Tמתקדםטכנולוגיהattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Rקריאהpartition(&ata0s)

	bios := TBiosparameterבלוק32{}

	var שםהקובץ []byte = ([]byte)("TEST")
	var גודל uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Rקריאה(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ, data)

	elf := Elf{}

	elf.Parse(data[:גודל], 0x4f00000)

}

var משימהconsole TConsole = TConsole{}

func Tפונקציה1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func משימהa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func משימהb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func משימהc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func משימהd()

func משימהd0() {
	esi := getesi()
	for {

		Sysהדפסהunsignedinteger32(esi)

	}
}

func משימהd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func קלטeventמשימה() {
	for {
		Pתהליךpendingמקלדתאירועים()
		Pתהליךpendingעכבראירועים()
		halt()
	}
}

func memorytest(y int) {
	זיכרוןmanager := &Tזיכרוןmanager{}
	allocated := uint32(uintptr(זיכרוןmanager.Malloc(1024)))
	console.MUnsignedinteger32הדפסהxy(allocated, 10, uint16(y))
	if y == 11 {
		זיכרוןmanager.Fפנוי(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pהשהייהloop()
func Rטעןמחדשcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sקבעcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getפונקציהשם(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcשם = runtime.FuncForPC(address).Name()
	var funcבתים []byte = []byte(funcשם)

	משימהconsole.Mהדפסהxy(funcבתים, 1, 5)
	משימהconsole.Mהדפסה(([]byte)(":"))
	משימהconsole.MUnsignedinteger32הדפסה(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	משימהconsole.Mהדפסהunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pעמודספרייהentry uintptr, stacktop uintptr, stackbottom uintptr) {

	Mסידורייומןinit()
	console.Mהדפסה("\n=== ISR BOOT ===\n")

	console.Mהדפסהunsignedinteger32(uint32(Pעמודספרייהentry), 0, 2)
	console.Mהדפסהunsignedinteger32(uint32(Pעמודספרייהentry), 10, 2)
	console.Mהדפסהunsignedinteger32(uint32(stacktop), 0, 3)
	console.Mהדפסהunsignedinteger32(uint32(stackbottom), 10, 3)

	זיכרוןmanager := &Tזיכרוןmanager{}
	זיכרוןmanager.Init(0, Mמקסימוםqueueגודל)

	paging := &Paging{}
	paging.Init(Pעמודספרייהentry, 0x500000, זיכרוןmanager)
	paging.Sharedזיכרוןregion()

	Sקבעcr3(uint32(Pעמודספרייהentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.Mהדפסה("esp:")

	esp := getesp()
	console.MUnsignedinteger32הדפסה(uint32(esp))

	tls := gettls()
	console.Mהדפסה(([]byte)("tls:"))
	console.MUnsignedinteger32הדפסה(tls)

	tss.Iהתקנה(shareddescriptortable, 7, Segkerneldata, esp)

	Virtבדיקה()

	cr3 := Rטעןמחדשcr3()
	console.Mהדפסה(([]byte)(":cr3:"))
	console.MUnsignedinteger32הדפסה(cr3)

	cr0 := Getcr0()
	console.Mהדפסה(([]byte)(":cr0:"))
	console.MUnsignedinteger32הדפסה(cr0)

	cr4 := Getcr4()
	console.Mהדפסה(([]byte)(":cr4:"))
	console.MUnsignedinteger32הדפסה(cr4)

	משימהmanager_2 := &Tמשימהmanager{}
	משימהmanager_2.Init()

	Iפסקmanager := &Tפסקmanager{}
	Iפסקmanager.Init(0x20, shareddescriptortable, משימהmanager_2)

	paging.Pעמודfault(Iפסקmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(זיכרוןmanager)

	תהליךhelper := Pתהליךhelper{}
	תהליךhelper.Init(זיכרוןmanager, Pעמודספרייהentry)

	sche := &Scheduler{}
	sche.Init(Iפסקmanager, זיכרוןmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Iפסקmanager)

	תהליךhelper.Spawn(משימהa, threadhelper, sche, uint32(Pעמודספרייהentry), true)
	תהליךhelper.Spawn(משימהb, threadhelper, sche, uint32(Pעמודספרייהentry), true)
	תהליךhelper.Spawn(משימהc, threadhelper, sche, uint32(Pעמודספרייהentry), true)
	תהליךhelper.Spawn(משימהd1, threadhelper, sche, uint32(Pעמודספרייהentry), true)
	תהליךhelper.Spawn(קלטeventמשימה, threadhelper, sche, uint32(Pעמודספרייהentry), true)

	var גודל uint32

	var linkerקובץ []byte = ([]byte)("LINKER")
	גודל = Getקובץגודל(linkerקובץ)
	linkeraddress := זיכרוןmanager.Malloc(גודל)
	linkerdata := Getבתיםfromסמן(uintptr(linkeraddress), int(גודל), int(גודל))
	Rקריאהקובץ(linkerקובץ, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pעמודספרייהentry))

	קישורmap := Lקישורmap{}
	קישורmap.Init(זיכרוןmanager)

	var lib1קובץ []byte = ([]byte)("LIB1")
	גודל = Getקובץגודל(lib1קובץ)

	lib1address := זיכרוןmanager.Malloc(גודל)
	lib1data := Getבתיםfromסמן(uintptr(lib1address), int(גודל), int(גודל))
	Rקריאהקובץ(lib1קובץ, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pעמודספרייהentry))
	זיכרוןmanager.Fפנוי(lib1address)

	קישורmap.Append_to_list(uintptr(lib1elf.Dדינמי))

	var lib2קובץ []byte = ([]byte)("LIB2")
	גודל = Getקובץגודל(lib2קובץ)

	lib2address := זיכרוןmanager.Malloc(גודל)
	lib2data := Getבתיםfromסמן(uintptr(lib2address), int(גודל), int(גודל))
	Rקריאהקובץ(lib2קובץ, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pעמודספרייהentry))
	זיכרוןmanager.Fפנוי(lib2address)

	קישורmap.Append_to_list(uintptr(lib2elf.Dדינמי))

	libקישורmap := קישורmap.Clone()
	קישורmapaddress := uint32(uintptr(Pointer(libקישורmap.First)))

	lib1got := Getunsignedinteger32מערךfromסמן(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = קישורmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32מערךfromסמן(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = קישורmapaddress
	lib2got[2] = 0x4000000

	console.Mהדפסהxy("lib1: ", 1, 8)
	console.MUnsignedinteger32הדפסה(lib1elf.Got)
	console.Mהדפסה(":")
	console.MUnsignedinteger32הדפסה(lib1elf.Dדינמי)

	console.Mהדפסהxy("lib2: ", 1, 9)
	console.MUnsignedinteger32הדפסה(lib2elf.Got)
	console.Mהדפסה(":")
	console.MUnsignedinteger32הדפסה(lib2elf.Dדינמי)

	var משתמש1קובץ []byte = ([]byte)("USER1")
	גודל = Getקובץגודל(משתמש1קובץ)
	משתמש1address := זיכרוןmanager.Malloc(גודל)
	משתמש1data := Getבתיםfromסמן(uintptr(משתמש1address), int(גודל), int(גודל))
	Rקריאהקובץ(משתמש1קובץ, משתמש1data)

	elf2 := Elf{}

	משתמש1entry := elf2.Getentry(משתמש1data)
	elf2.Parse(משתמש1data[:], uint32(Pעמודספרייהentry+0x1000))
	גלובליoffsettable := elf2.Got

	Pערך1קישורmap := קישורmap.Clone()
	Pערך1קישורmap.Append_to_list(uintptr(elf2.Dדינמי))

	זיכרוןmanager.Fפנוי(משתמש1address)

	var code1סמן *uintptr
	var func1val func()

	code1סמן = (*uintptr)(זיכרוןmanager.Malloc(4))
	*code1סמן = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1סמן))

	proc2 := תהליךhelper.Spawn(func1val, threadhelper, sche, uint32(Pעמודספרייהentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cמעבדמצב.Ecx = משתמש1entry
	thr2.Cמעבדמצב.Edx = גלובליoffsettable
	thr2.Cמעבדמצב.Esi = uint32(uintptr(Pointer(Pערך1קישורmap.First)))

	console.Mהדפסהxy("user1: ", 1, 10)
	console.MUnsignedinteger32הדפסה(elf2.Got)

	var משתמש2קובץ []byte = ([]byte)("USER2")
	גודל = Getקובץגודל(משתמש2קובץ)
	משתמש2address := זיכרוןmanager.Malloc(גודל)
	משתמש2data := Getבתיםfromסמן(uintptr(משתמש2address), int(גודל), int(גודל))
	Rקריאהקובץ(משתמש2קובץ, משתמש2data)

	elf3 := Elf{}

	משתמש2entry := elf3.Getentry(משתמש2data)
	elf3.Parse(משתמש2data[:], uint32(Pעמודספרייהentry+0x2000))
	גלובליoffsettable = elf3.Got

	Pערך2קישורmap := קישורmap.Clone()
	Pערך2קישורmap.Append_to_list(uintptr(elf3.Dדינמי))

	זיכרוןmanager.Fפנוי(משתמש2address)

	var code2סמן *uintptr
	var func2val func()

	code2סמן = (*uintptr)(זיכרוןmanager.Malloc(4))
	*code2סמן = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2סמן))

	proc3 := תהליךhelper.Spawn(func2val, threadhelper, sche, uint32(Pעמודספרייהentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cמעבדמצב.Ecx = משתמש2entry
	thr3.Cמעבדמצב.Edx = גלובליoffsettable
	thr3.Cמעבדמצב.Esi = uint32(uintptr(Pointer(Pערך2קישורmap.First)))

	console.Mהדפסהxy("user2: ", 1, 11)
	console.MUnsignedinteger32הדפסה(thr3.Cמעבדמצב.Esi)

	libקישורmap.Pהדפסה(1, 11)

	var משתמש3קובץ []byte = ([]byte)("USER3")
	גודל = Getקובץגודל(משתמש3קובץ)
	משתמש3address := זיכרוןmanager.Malloc(גודל)
	משתמש3data := Getבתיםfromסמן(uintptr(משתמש3address), int(גודל), int(גודל))
	Rקריאהקובץ(משתמש3קובץ, משתמש3data)

	elf4 := Elf{}

	משתמש3entry := elf4.Getentry(משתמש3data)
	elf4.Parse(משתמש3data[:], uint32(Pעמודספרייהentry+0x3000))
	גלובליoffsettable = elf4.Got

	Pערך3קישורmap := קישורmap.Clone()
	Pערך3קישורmap.Append_to_list(uintptr(elf4.Dדינמי))

	זיכרוןmanager.Fפנוי(משתמש3address)

	var code3סמן *uintptr
	var func3val func()

	code3סמן = (*uintptr)(זיכרוןmanager.Malloc(4))
	*code3סמן = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3סמן))

	proc4 := תהליךhelper.Spawn(func3val, threadhelper, sche, uint32(Pעמודספרייהentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cמעבדמצב.Ecx = משתמש3entry
	thr4.Cמעבדמצב.Edx = גלובליoffsettable
	thr4.Cמעבדמצב.Esi = uint32(uintptr(Pointer(Pערך3קישורmap.First)))

	תהליךhelper.Spawn(Tפונקציה1, threadhelper, sche, uint32(Pעמודספרייהentry+0x4000), true)

	iמקלדתeventhandler = &myמקלדתeventhandler
	מקלדתdriver.Initdriver(Iפסקmanager, iמקלדתeventhandler)

	עכברdriver.Initdriver(Iפסקmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Sבחרdriver(&Drivermanager, Iפסקmanager)
	התקןdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Eמופעל(true)
	Iפסקmanager.Aפעיל()

	for {
		halt()
	}

}
