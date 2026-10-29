/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "консол"
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtualСанахой"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/гар"
import . "driver/хулгана"

import . "driver/ata"
import . "файлСистем/msdospartition"
import . "файлСистем/fat"

import . "файлСистем/elf"

import . "системcall"

import . "санахойЗохицуулагч"
import . "pci"

func halt()

var iГарeventhandler IГарeventhandler

type TMyГарeventhandler struct {
}

var myГарeventhandler TMyГарeventhandler
var гарdriver TГарdriver
var хулганаdriver TХулганаdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var гарКонсол TКонсол = TКонсол{}

func (self *TMyГарeventhandler) Onkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	гарКонсол.MХэвлэхБайтxy(foo[:], 1000, 1000)
}

func (self *TMyГарeventhandler) OnkeyДээш(key byte)	{}

var iХулганаeventhandler IХулганаeventhandler

type TMyХулганаeventhandler struct {
}

var хулганаКонсол TКонсол = TКонсол{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMyХулганаeventhandler) OnХулганаdown(button int8) {
	buffer := []byte("x")
	хулганаКонсол.MХэвлэхxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyХулганаeventhandler) OnХулганаДээш(button int8)	{}
func (self *TMyХулганаeventhandler) OnХулганаЗөөх(x int8, y int8) {

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
	хулганаКонсол.MХэвлэхxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	хулганаКонсол.MХэвлэхxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var төхөөрөмжdescriptor TPeripheralcomponentinterconnectТөхөөрөмжdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var консол TКонсол = TКонсол{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(төхөөрөмж TPeripheralcomponentinterconnectТөхөөрөмжdescriptor) {
	if төхөөрөмж.VendorДугаар == 0x1022 && төхөөрөмж.ТөхөөрөмжДугаар == 0x2000 {
		консол.MХэвлэхxy([]byte("["), 0, 12)
		консол.MХэвлэх(([]byte)("AMD am79c973"))
		консол.MХэвлэх([]byte(":"))
		консол.MUnsignedinteger16Хэвлэх(төхөөрөмж.VendorДугаар)
		консол.MХэвлэх([]byte(":"))
		консол.MUnsignedinteger16Хэвлэх(төхөөрөмж.ТөхөөрөмжДугаар)
		консол.MХэвлэх([]byte(":"))
		консол.MUnsignedinteger16Хэвлэх(uint16(төхөөрөмж.Портbase))
		консол.MХэвлэх([]byte(":"))
		консол.MUnsignedinteger32Хэвлэх(төхөөрөмж.Interrupt)

		консол.MХэвлэх([]byte("]\n"))
		төхөөрөмжdescriptor = төхөөрөмж
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectТөхөөрөмжdescriptor {
	return төхөөрөмжdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Хэвлэхstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	консол.MХэвлэх(str)
}

func GetФайлХэмжээ(файлыннэр []byte) uint32 {
	var ata0s = TӨргөтгөсөнtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Уншихpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var хэмжээ uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр)
	ata0s.Flush()

	return хэмжээ
}

func УншихФайл(файлыннэр []byte, data []byte) {
	var ata0s = TӨргөтгөсөнtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Уншихpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Унших(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр, data)

	ata0s.Flush()
}
func Ачаалахelf() {

	var ata0s = TӨргөтгөсөнtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Уншихpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var файлыннэр []byte = ([]byte)("TEST")
	var хэмжээ uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Унших(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр, data)

	elf := Elf{}

	elf.Parse(data[:хэмжээ], 0x4f00000)

}

var taskКонсол TКонсол = TКонсол{}

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

		SysХэвлэхunsignedinteger32(esi)

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
		ProcesspendingГарevents()
		ProcesspendingХулганаevents()
		halt()
	}
}

func memorytest(y int) {
	санахойЗохицуулагч := &TСанахойЗохицуулагч{}
	allocated := uint32(uintptr(санахойЗохицуулагч.Malloc(1024)))
	консол.MUnsignedinteger32Хэвлэхxy(allocated, 10, uint16(y))
	if y == 11 {
		санахойЗохицуулагч.Чөлөөт(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Ахиначаалахcr3() uint32

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

func GetfunctionНэр(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcНэр = runtime.FuncForPC(address).Name()
	var funcБайт []byte = []byte(funcНэр)

	taskКонсол.MХэвлэхxy(funcБайт, 1, 5)
	taskКонсол.MХэвлэх(([]byte)(":"))
	taskКонсол.MUnsignedinteger32Хэвлэх(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskКонсол.MХэвлэхunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(ХУУДАСЛавлахentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	консол.MХэвлэх("\n=== MNG BOOT ===\n")

	консол.MХэвлэхunsignedinteger32(uint32(ХУУДАСЛавлахentry), 0, 2)
	консол.MХэвлэхunsignedinteger32(uint32(ХУУДАСЛавлахentry), 10, 2)
	консол.MХэвлэхunsignedinteger32(uint32(stacktop), 0, 3)
	консол.MХэвлэхunsignedinteger32(uint32(stackbottom), 10, 3)

	санахойЗохицуулагч := &TСанахойЗохицуулагч{}
	санахойЗохицуулагч.Init(0, MaxqueueХэмжээ)

	paging := &Paging{}
	paging.Init(ХУУДАСЛавлахentry, 0x500000, санахойЗохицуулагч)
	paging.SharedСанахойregion()

	Setcr3(uint32(ХУУДАСЛавлахentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	консол.MХэвлэх("esp:")

	esp := getesp()
	консол.MUnsignedinteger32Хэвлэх(uint32(esp))

	tls := gettls()
	консол.MХэвлэх(([]byte)("tls:"))
	консол.MUnsignedinteger32Хэвлэх(tls)

	tss.Суулгах(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Ахиначаалахcr3()
	консол.MХэвлэх(([]byte)(":cr3:"))
	консол.MUnsignedinteger32Хэвлэх(cr3)

	cr0 := Getcr0()
	консол.MХэвлэх(([]byte)(":cr0:"))
	консол.MUnsignedinteger32Хэвлэх(cr0)

	cr4 := Getcr4()
	консол.MХэвлэх(([]byte)(":cr4:"))
	консол.MUnsignedinteger32Хэвлэх(cr4)

	taskЗохицуулагч_2 := &TTaskЗохицуулагч{}
	taskЗохицуулагч_2.Init()

	InterruptЗохицуулагч := &TInterruptЗохицуулагч{}
	InterruptЗохицуулагч.Init(0x20, shareddescriptortable, taskЗохицуулагч_2)

	paging.ХУУДАСfault(InterruptЗохицуулагч)

	DriverЗохицуулагч := TDriverЗохицуулагч{}
	DriverЗохицуулагч.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(санахойЗохицуулагч)

	processhelper := Processhelper{}
	processhelper.Init(санахойЗохицуулагч, ХУУДАСЛавлахentry)

	sche := &Scheduler{}
	sche.Init(InterruptЗохицуулагч, санахойЗохицуулагч, tss)

	syscall := &TSyscall{}
	syscall.Init(InterruptЗохицуулагч)

	processhelper.Spawn(taska, threadhelper, sche, uint32(ХУУДАСЛавлахentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(ХУУДАСЛавлахentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(ХУУДАСЛавлахentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(ХУУДАСЛавлахentry), true)
	processhelper.Spawn(inputeventtask, threadhelper, sche, uint32(ХУУДАСЛавлахentry), true)

	var хэмжээ uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	хэмжээ = GetФайлХэмжээ(linkerФайл)
	linkeraddress := санахойЗохицуулагч.Malloc(хэмжээ)
	linkerdata := GetБайтfrompointer(uintptr(linkeraddress), int(хэмжээ), int(хэмжээ))
	УншихФайл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(ХУУДАСЛавлахentry))

	холбоосmap := Холбоосmap{}
	холбоосmap.Init(санахойЗохицуулагч)

	var lib1Файл []byte = ([]byte)("LIB1")
	хэмжээ = GetФайлХэмжээ(lib1Файл)

	lib1address := санахойЗохицуулагч.Malloc(хэмжээ)
	lib1data := GetБайтfrompointer(uintptr(lib1address), int(хэмжээ), int(хэмжээ))
	УншихФайл(lib1Файл, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(ХУУДАСЛавлахentry))
	санахойЗохицуулагч.Чөлөөт(lib1address)

	холбоосmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Файл []byte = ([]byte)("LIB2")
	хэмжээ = GetФайлХэмжээ(lib2Файл)

	lib2address := санахойЗохицуулагч.Malloc(хэмжээ)
	lib2data := GetБайтfrompointer(uintptr(lib2address), int(хэмжээ), int(хэмжээ))
	УншихФайл(lib2Файл, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(ХУУДАСЛавлахentry))
	санахойЗохицуулагч.Чөлөөт(lib2address)

	холбоосmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libХолбоосmap := холбоосmap.Clone()
	холбоосmapaddress := uint32(uintptr(Pointer(libХолбоосmap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = холбоосmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = холбоосmapaddress
	lib2got[2] = 0x4000000

	консол.MХэвлэхxy("lib1: ", 1, 8)
	консол.MUnsignedinteger32Хэвлэх(lib1elf.Got)
	консол.MХэвлэх(":")
	консол.MUnsignedinteger32Хэвлэх(lib1elf.Dynamic)

	консол.MХэвлэхxy("lib2: ", 1, 9)
	консол.MUnsignedinteger32Хэвлэх(lib2elf.Got)
	консол.MХэвлэх(":")
	консол.MUnsignedinteger32Хэвлэх(lib2elf.Dynamic)

	var хэрэглэгч1Файл []byte = ([]byte)("USER1")
	хэмжээ = GetФайлХэмжээ(хэрэглэгч1Файл)
	хэрэглэгч1address := санахойЗохицуулагч.Malloc(хэмжээ)
	хэрэглэгч1data := GetБайтfrompointer(uintptr(хэрэглэгч1address), int(хэмжээ), int(хэмжээ))
	УншихФайл(хэрэглэгч1Файл, хэрэглэгч1data)

	elf2 := Elf{}

	хэрэглэгч1entry := elf2.Getentry(хэрэглэгч1data)
	elf2.Parse(хэрэглэгч1data[:], uint32(ХУУДАСЛавлахentry+0x1000))
	globaloffsettable := elf2.Got

	PУтга1Холбоосmap := холбоосmap.Clone()
	PУтга1Холбоосmap.Append_to_list(uintptr(elf2.Dynamic))

	санахойЗохицуулагч.Чөлөөт(хэрэглэгч1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(санахойЗохицуулагч.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(ХУУДАСЛавлахentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = хэрэглэгч1entry
	thr2.Cpustate.Edx = globaloffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PУтга1Холбоосmap.First)))

	консол.MХэвлэхxy("user1: ", 1, 10)
	консол.MUnsignedinteger32Хэвлэх(elf2.Got)

	var хэрэглэгч2Файл []byte = ([]byte)("USER2")
	хэмжээ = GetФайлХэмжээ(хэрэглэгч2Файл)
	хэрэглэгч2address := санахойЗохицуулагч.Malloc(хэмжээ)
	хэрэглэгч2data := GetБайтfrompointer(uintptr(хэрэглэгч2address), int(хэмжээ), int(хэмжээ))
	УншихФайл(хэрэглэгч2Файл, хэрэглэгч2data)

	elf3 := Elf{}

	хэрэглэгч2entry := elf3.Getentry(хэрэглэгч2data)
	elf3.Parse(хэрэглэгч2data[:], uint32(ХУУДАСЛавлахentry+0x2000))
	globaloffsettable = elf3.Got

	PУтга2Холбоосmap := холбоосmap.Clone()
	PУтга2Холбоосmap.Append_to_list(uintptr(elf3.Dynamic))

	санахойЗохицуулагч.Чөлөөт(хэрэглэгч2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(санахойЗохицуулагч.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(ХУУДАСЛавлахentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = хэрэглэгч2entry
	thr3.Cpustate.Edx = globaloffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PУтга2Холбоосmap.First)))

	консол.MХэвлэхxy("user2: ", 1, 11)
	консол.MUnsignedinteger32Хэвлэх(thr3.Cpustate.Esi)

	libХолбоосmap.Хэвлэх(1, 11)

	var хэрэглэгч3Файл []byte = ([]byte)("USER3")
	хэмжээ = GetФайлХэмжээ(хэрэглэгч3Файл)
	хэрэглэгч3address := санахойЗохицуулагч.Malloc(хэмжээ)
	хэрэглэгч3data := GetБайтfrompointer(uintptr(хэрэглэгч3address), int(хэмжээ), int(хэмжээ))
	УншихФайл(хэрэглэгч3Файл, хэрэглэгч3data)

	elf4 := Elf{}

	хэрэглэгч3entry := elf4.Getentry(хэрэглэгч3data)
	elf4.Parse(хэрэглэгч3data[:], uint32(ХУУДАСЛавлахentry+0x3000))
	globaloffsettable = elf4.Got

	PУтга3Холбоосmap := холбоосmap.Clone()
	PУтга3Холбоосmap.Append_to_list(uintptr(elf4.Dynamic))

	санахойЗохицуулагч.Чөлөөт(хэрэглэгч3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(санахойЗохицуулагч.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(ХУУДАСЛавлахentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = хэрэглэгч3entry
	thr4.Cpustate.Edx = globaloffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PУтга3Холбоосmap.First)))

	processhelper.Spawn(TFunction1, threadhelper, sche, uint32(ХУУДАСЛавлахentry+0x4000), true)

	iГарeventhandler = &myГарeventhandler
	гарdriver.Initdriver(InterruptЗохицуулагч, iГарeventhandler)

	хулганаdriver.Initdriver(InterruptЗохицуулагч, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&DriverЗохицуулагч, InterruptЗохицуулагч)
	төхөөрөмжdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	InterruptЗохицуулагч.Идэвхтэй()

	for {
		halt()
	}

}
