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

import . "virtualYaddaş"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/klaviatura"
import . "driver/siçan"

import . "driver/ata"
import . "faylsystem/msdospartition"
import . "faylsystem/fat"

import . "faylsystem/elf"

import . "systemcall"

import . "yaddaşmanager"
import . "pci"

func halt()

var iKlaviaturaeventhandler IKlaviaturaeventhandler

type TMyKlaviaturaeventhandler struct {
}

var myKlaviaturaeventhandler TMyKlaviaturaeventhandler
var klaviaturadriver TKlaviaturadriver
var siçandriver TSiçandriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klaviaturaconsole TConsole = TConsole{}

func (self *TMyKlaviaturaeventhandler) OnAçardown(açar byte) {
	foo := [1]byte{' '}
	foo[0] = açar

	klaviaturaconsole.MÇapEtBaytxy(foo[:], 1000, 1000)
}

func (self *TMyKlaviaturaeventhandler) OnAçarYuxarı(açar byte)	{}

var iSiçaneventhandler ISiçaneventhandler

type TMySiçaneventhandler struct {
}

var siçanconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMySiçaneventhandler) OnSiçandown(button int8) {
	buffer := []byte("x")
	siçanconsole.MÇapEtxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMySiçaneventhandler) OnSiçanYuxarı(button int8)	{}
func (self *TMySiçaneventhandler) OnSiçanDaşı(x int8, y int8) {

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
	siçanconsole.MÇapEtxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	siçanconsole.MÇapEtxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var avadanlıqdescriptor TPeripheralcomponentinterconnectAvadanlıqdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(avadanlıq TPeripheralcomponentinterconnectAvadanlıqdescriptor) {
	if avadanlıq.Vendorid == 0x1022 && avadanlıq.Avadanlıqid == 0x2000 {
		console.MÇapEtxy([]byte("["), 0, 12)
		console.MÇapEt(([]byte)("AMD am79c973"))
		console.MÇapEt([]byte(":"))
		console.MUnsignedinteger16ÇapEt(avadanlıq.Vendorid)
		console.MÇapEt([]byte(":"))
		console.MUnsignedinteger16ÇapEt(avadanlıq.Avadanlıqid)
		console.MÇapEt([]byte(":"))
		console.MUnsignedinteger16ÇapEt(uint16(avadanlıq.Qapıbase))
		console.MÇapEt([]byte(":"))
		console.MUnsignedinteger32ÇapEt(avadanlıq.Interrupt)

		console.MÇapEt([]byte("]\n"))
		avadanlıqdescriptor = avadanlıq
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectAvadanlıqdescriptor {
	return avadanlıqdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func ÇapEtstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MÇapEt(str)
}

func GetFaylBöyüklük(fayladı []byte) uint32 {
	var ata0s = TƏtraflıtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oxumapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var böyüklük uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], fayladı)
	ata0s.Flush()

	return böyüklük
}

func OxumaFayl(fayladı []byte, data []byte) {
	var ata0s = TƏtraflıtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oxumapartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Oxuma(&ata0s, partition.Mbr.Primarypartition[0], fayladı, data)

	ata0s.Flush()
}
func Yükelf() {

	var ata0s = TƏtraflıtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oxumapartition(&ata0s)

	bios := TBiosparameterblock32{}

	var fayladı []byte = ([]byte)("TEST")
	var böyüklük uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], fayladı)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Oxuma(&ata0s, partition.Mbr.Primarypartition[0], fayladı, data)

	elf := Elf{}

	elf.Parse(data[:böyüklük], 0x4f00000)

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

		SysÇapEtunsignedinteger32(esi)

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
		ProcesspendingKlaviaturaevents()
		ProcesspendingSiçanevents()
		halt()
	}
}

func memorytest(y int) {
	yaddaşmanager := &TYaddaşmanager{}
	allocated := uint32(uintptr(yaddaşmanager.Malloc(1024)))
	console.MUnsignedinteger32ÇapEtxy(allocated, 10, uint16(y))
	if y == 11 {
		yaddaşmanager.Boş(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Yeniləcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Setcr3(cr3 uint32)
func Getcr4() uint32
func Fəallaşdırpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetfunctionAd(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcAd = runtime.FuncForPC(address).Name()
	var funcBayt []byte = []byte(funcAd)

	taskconsole.MÇapEtxy(funcBayt, 1, 5)
	taskconsole.MÇapEt(([]byte)(":"))
	taskconsole.MUnsignedinteger32ÇapEt(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MÇapEtunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(SəhifəCərgəentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MÇapEt("\n=== AZE BOOT ===\n")

	console.MÇapEtunsignedinteger32(uint32(SəhifəCərgəentry), 0, 2)
	console.MÇapEtunsignedinteger32(uint32(SəhifəCərgəentry), 10, 2)
	console.MÇapEtunsignedinteger32(uint32(stacktop), 0, 3)
	console.MÇapEtunsignedinteger32(uint32(stackbottom), 10, 3)

	yaddaşmanager := &TYaddaşmanager{}
	yaddaşmanager.Init(0, MaxqueueBöyüklük)

	paging := &Paging{}
	paging.Init(SəhifəCərgəentry, 0x500000, yaddaşmanager)
	paging.SharedYaddaşregion()

	Setcr3(uint32(SəhifəCərgəentry))
	Fəallaşdırpaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MÇapEt("esp:")

	esp := getesp()
	console.MUnsignedinteger32ÇapEt(uint32(esp))

	tls := gettls()
	console.MÇapEt(([]byte)("tls:"))
	console.MUnsignedinteger32ÇapEt(tls)

	tss.Quraşdır(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Yeniləcr3()
	console.MÇapEt(([]byte)(":cr3:"))
	console.MUnsignedinteger32ÇapEt(cr3)

	cr0 := Getcr0()
	console.MÇapEt(([]byte)(":cr0:"))
	console.MUnsignedinteger32ÇapEt(cr0)

	cr4 := Getcr4()
	console.MÇapEt(([]byte)(":cr4:"))
	console.MUnsignedinteger32ÇapEt(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptortable, taskmanager_2)

	paging.Səhifəfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(yaddaşmanager)

	processhelper := Processhelper{}
	processhelper.Init(yaddaşmanager, SəhifəCərgəentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, yaddaşmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(SəhifəCərgəentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(SəhifəCərgəentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(SəhifəCərgəentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(SəhifəCərgəentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(SəhifəCərgəentry), true)

	var böyüklük uint32

	var linkerFayl []byte = ([]byte)("LINKER")
	böyüklük = GetFaylBöyüklük(linkerFayl)
	linkeraddress := yaddaşmanager.Malloc(böyüklük)
	linkerdata := GetBaytfrompointer(uintptr(linkeraddress), int(böyüklük), int(böyüklük))
	OxumaFayl(linkerFayl, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SəhifəCərgəentry))

	körpümap := Körpümap{}
	körpümap.Init(yaddaşmanager)

	var lib1Fayl []byte = ([]byte)("LIB1")
	böyüklük = GetFaylBöyüklük(lib1Fayl)

	lib1address := yaddaşmanager.Malloc(böyüklük)
	lib1data := GetBaytfrompointer(uintptr(lib1address), int(böyüklük), int(böyüklük))
	OxumaFayl(lib1Fayl, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SəhifəCərgəentry))
	yaddaşmanager.Boş(lib1address)

	körpümap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Fayl []byte = ([]byte)("LIB2")
	böyüklük = GetFaylBöyüklük(lib2Fayl)

	lib2address := yaddaşmanager.Malloc(böyüklük)
	lib2data := GetBaytfrompointer(uintptr(lib2address), int(böyüklük), int(böyüklük))
	OxumaFayl(lib2Fayl, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SəhifəCərgəentry))
	yaddaşmanager.Boş(lib2address)

	körpümap.Append_to_list(uintptr(lib2elf.Dynamic))

	libkörpümap := körpümap.Clone()
	körpümapaddress := uint32(uintptr(Pointer(libkörpümap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = körpümapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = körpümapaddress
	lib2got[2] = 0x4000000

	console.MÇapEtxy("lib1: ", 1, 8)
	console.MUnsignedinteger32ÇapEt(lib1elf.Got)
	console.MÇapEt(":")
	console.MUnsignedinteger32ÇapEt(lib1elf.Dynamic)

	console.MÇapEtxy("lib2: ", 1, 9)
	console.MUnsignedinteger32ÇapEt(lib2elf.Got)
	console.MÇapEt(":")
	console.MUnsignedinteger32ÇapEt(lib2elf.Dynamic)

	var istifadəçi1Fayl []byte = ([]byte)("USER1")
	böyüklük = GetFaylBöyüklük(istifadəçi1Fayl)
	istifadəçi1address := yaddaşmanager.Malloc(böyüklük)
	istifadəçi1data := GetBaytfrompointer(uintptr(istifadəçi1address), int(böyüklük), int(böyüklük))
	OxumaFayl(istifadəçi1Fayl, istifadəçi1data)

	elf2 := Elf{}

	istifadəçi1entry := elf2.Getentry(istifadəçi1data)
	elf2.Parse(istifadəçi1data[:], uint32(SəhifəCərgəentry+0x1000))
	globaloffsettable := elf2.Got

	PQiymət1körpümap := körpümap.Clone()
	PQiymət1körpümap.Append_to_list(uintptr(elf2.Dynamic))

	yaddaşmanager.Boş(istifadəçi1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(yaddaşmanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(SəhifəCərgəentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = istifadəçi1entry
	thr2.Cpustate.Edx = globaloffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PQiymət1körpümap.First)))

	console.MÇapEtxy("user1: ", 1, 10)
	console.MUnsignedinteger32ÇapEt(elf2.Got)

	var istifadəçi2Fayl []byte = ([]byte)("USER2")
	böyüklük = GetFaylBöyüklük(istifadəçi2Fayl)
	istifadəçi2address := yaddaşmanager.Malloc(böyüklük)
	istifadəçi2data := GetBaytfrompointer(uintptr(istifadəçi2address), int(böyüklük), int(böyüklük))
	OxumaFayl(istifadəçi2Fayl, istifadəçi2data)

	elf3 := Elf{}

	istifadəçi2entry := elf3.Getentry(istifadəçi2data)
	elf3.Parse(istifadəçi2data[:], uint32(SəhifəCərgəentry+0x2000))
	globaloffsettable = elf3.Got

	PQiymət2körpümap := körpümap.Clone()
	PQiymət2körpümap.Append_to_list(uintptr(elf3.Dynamic))

	yaddaşmanager.Boş(istifadəçi2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(yaddaşmanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(SəhifəCərgəentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = istifadəçi2entry
	thr3.Cpustate.Edx = globaloffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PQiymət2körpümap.First)))

	console.MÇapEtxy("user2: ", 1, 11)
	console.MUnsignedinteger32ÇapEt(thr3.Cpustate.Esi)

	libkörpümap.ÇapEt(1, 11)

	var istifadəçi3Fayl []byte = ([]byte)("USER3")
	böyüklük = GetFaylBöyüklük(istifadəçi3Fayl)
	istifadəçi3address := yaddaşmanager.Malloc(böyüklük)
	istifadəçi3data := GetBaytfrompointer(uintptr(istifadəçi3address), int(böyüklük), int(böyüklük))
	OxumaFayl(istifadəçi3Fayl, istifadəçi3data)

	elf4 := Elf{}

	istifadəçi3entry := elf4.Getentry(istifadəçi3data)
	elf4.Parse(istifadəçi3data[:], uint32(SəhifəCərgəentry+0x3000))
	globaloffsettable = elf4.Got

	PQiymət3körpümap := körpümap.Clone()
	PQiymət3körpümap.Append_to_list(uintptr(elf4.Dynamic))

	yaddaşmanager.Boş(istifadəçi3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(yaddaşmanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(SəhifəCərgəentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = istifadəçi3entry
	thr4.Cpustate.Edx = globaloffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PQiymət3körpümap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(SəhifəCərgəentry+0x4000), true)

	iKlaviaturaeventhandler = &myKlaviaturaeventhandler
	klaviaturadriver.Initdriver(Interruptmanager, iKlaviaturaeventhandler)

	siçandriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	avadanlıqdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	Interruptmanager.Fəal()

	for {
		halt()
	}

}
