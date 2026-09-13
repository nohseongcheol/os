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

import . "virtualmemory"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/keyboard"
import . "driver/mouse"

import . "driver/ata"
import . "файлsystem/msdospartition"
import . "файлsystem/fat"

import . "файлsystem/elf"

import . "systemcall"

import . "memorymanager"
import . "pci"

func halt()

var ikeyboardeventhandler IKeyboardeventhandler

type TMykeyboardeventhandler struct {
}

var mykeyboardeventhandler TMykeyboardeventhandler
var keyboarddriver TKeyboarddriver
var mousedriver TMousedriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var keyboardconsole TConsole = TConsole{}

func (self *TMykeyboardeventhandler) OnkeyПоён(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	keyboardconsole.MЧопкарданbytesxy(foo[:], 1000, 1000)
}

func (self *TMykeyboardeventhandler) OnkeyБоло(key byte)	{}

var imouseeventhandler IMouseeventhandler

type TMymouseeventhandler struct {
}

var mouseconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMymouseeventhandler) OnmouseПоён(button int8) {
	buffer := []byte("x")
	mouseconsole.MЧопкарданxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMymouseeventhandler) OnmouseБоло(button int8)	{}
func (self *TMymouseeventhandler) OnmouseТаҳвил(x int8, y int8) {

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
	mouseconsole.MЧопкарданxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mouseconsole.MЧопкарданxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var дастгоҳdescriptor TPeripheralcomponentinterconnectДастгоҳdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(дастгоҳ TPeripheralcomponentinterconnectДастгоҳdescriptor) {
	if дастгоҳ.Vendorid == 0x1022 && дастгоҳ.Дастгоҳid == 0x2000 {
		console.MЧопкарданxy([]byte("["), 0, 12)
		console.MЧопкардан(([]byte)("AMD am79c973"))
		console.MЧопкардан([]byte(":"))
		console.MUnsignedinteger16Чопкардан(дастгоҳ.Vendorid)
		console.MЧопкардан([]byte(":"))
		console.MUnsignedinteger16Чопкардан(дастгоҳ.Дастгоҳid)
		console.MЧопкардан([]byte(":"))
		console.MUnsignedinteger16Чопкардан(uint16(дастгоҳ.Portbase))
		console.MЧопкардан([]byte(":"))
		console.MUnsignedinteger32Чопкардан(дастгоҳ.Interrupt)

		console.MЧопкардан([]byte("]\n"))
		дастгоҳdescriptor = дастгоҳ
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectДастгоҳdescriptor {
	return дастгоҳdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Чопкарданstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MЧопкардан(str)
}

func GetФайлsize(filename []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Хонданpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var size uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()

	return size
}

func ХонданФайл(filename []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Хонданpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Хондан(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	ata0s.Flush()
}
func Loadelf() {

	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Хонданpartition(&ata0s)

	bios := TBiosparameterblock32{}

	var filename []byte = ([]byte)("TEST")
	var size uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Хондан(&ata0s, partition.Mbr.Primarypartition[0], filename, data)

	elf := Elf{}

	elf.Parse(data[:size], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TФунксия1() {
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

		SysЧопкарданunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func вурудeventtask() {
	for {
		Processpendingkeyboardevents()
		Processpendingmouseevents()
		halt()
	}
}

func memorytest(y int) {
	memorymanager := &TMemorymanager{}
	allocated := uint32(uintptr(memorymanager.Malloc(1024)))
	console.MUnsignedinteger32Чопкарданxy(allocated, 10, uint16(y))
	if y == 11 {
		memorymanager.Free(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Reloadcr3() uint32

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

func GetФунксияНом(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcНом = runtime.FuncForPC(address).Name()
	var funcbytes []byte = []byte(funcНом)

	taskconsole.MЧопкарданxy(funcbytes, 1, 5)
	taskconsole.MЧопкардан(([]byte)(":"))
	taskconsole.MUnsignedinteger32Чопкардан(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MЧопкарданunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(PageФеҳрастentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MЧопкардан("\n=== TJK BOOT ===\n")

	console.MЧопкарданunsignedinteger32(uint32(PageФеҳрастentry), 0, 2)
	console.MЧопкарданunsignedinteger32(uint32(PageФеҳрастentry), 10, 2)
	console.MЧопкарданunsignedinteger32(uint32(stacktop), 0, 3)
	console.MЧопкарданunsignedinteger32(uint32(stackbottom), 10, 3)

	memorymanager := &TMemorymanager{}
	memorymanager.Init(0, Maxqueuesize)

	paging := &Paging{}
	paging.Init(PageФеҳрастentry, 0x500000, memorymanager)
	paging.Sharedmemoryregion()

	Setcr3(uint32(PageФеҳрастentry))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MЧопкардан("esp:")

	esp := getesp()
	console.MUnsignedinteger32Чопкардан(uint32(esp))

	tls := gettls()
	console.MЧопкардан(([]byte)("tls:"))
	console.MUnsignedinteger32Чопкардан(tls)

	tss.Сабткунед(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Reloadcr3()
	console.MЧопкардан(([]byte)(":cr3:"))
	console.MUnsignedinteger32Чопкардан(cr3)

	cr0 := Getcr0()
	console.MЧопкардан(([]byte)(":cr0:"))
	console.MUnsignedinteger32Чопкардан(cr0)

	cr4 := Getcr4()
	console.MЧопкардан(([]byte)(":cr4:"))
	console.MUnsignedinteger32Чопкардан(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptortable, taskmanager_2)

	paging.Pagefault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorymanager)

	processhelper := Processhelper{}
	processhelper.Init(memorymanager, PageФеҳрастentry)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, memorymanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(PageФеҳрастentry), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(PageФеҳрастentry), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(PageФеҳрастentry), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(PageФеҳрастentry), true)
	processhelper.Spawn(вурудeventtask, threadhelper, sche, uint32(PageФеҳрастentry), true)

	var size uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	size = GetФайлsize(linkerФайл)
	linkeraddress := memorymanager.Malloc(size)
	linkerdata := Getbytesfrompointer(uintptr(linkeraddress), int(size), int(size))
	ХонданФайл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PageФеҳрастentry))

	алоқаmap := Алоқаmap{}
	алоқаmap.Init(memorymanager)

	var lib1Файл []byte = ([]byte)("LIB1")
	size = GetФайлsize(lib1Файл)

	lib1address := memorymanager.Malloc(size)
	lib1data := Getbytesfrompointer(uintptr(lib1address), int(size), int(size))
	ХонданФайл(lib1Файл, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PageФеҳрастentry))
	memorymanager.Free(lib1address)

	алоқаmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Файл []byte = ([]byte)("LIB2")
	size = GetФайлsize(lib2Файл)

	lib2address := memorymanager.Malloc(size)
	lib2data := Getbytesfrompointer(uintptr(lib2address), int(size), int(size))
	ХонданФайл(lib2Файл, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PageФеҳрастentry))
	memorymanager.Free(lib2address)

	алоқаmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libАлоқаmap := алоқаmap.Clone()
	алоқаmapaddress := uint32(uintptr(Pointer(libАлоқаmap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = алоқаmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = алоқаmapaddress
	lib2got[2] = 0x4000000

	console.MЧопкарданxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Чопкардан(lib1elf.Got)
	console.MЧопкардан(":")
	console.MUnsignedinteger32Чопкардан(lib1elf.Dynamic)

	console.MЧопкарданxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Чопкардан(lib2elf.Got)
	console.MЧопкардан(":")
	console.MUnsignedinteger32Чопкардан(lib2elf.Dynamic)

	var истифодакунанда1Файл []byte = ([]byte)("USER1")
	size = GetФайлsize(истифодакунанда1Файл)
	истифодакунанда1address := memorymanager.Malloc(size)
	истифодакунанда1data := Getbytesfrompointer(uintptr(истифодакунанда1address), int(size), int(size))
	ХонданФайл(истифодакунанда1Файл, истифодакунанда1data)

	elf2 := Elf{}

	истифодакунанда1entry := elf2.Getentry(истифодакунанда1data)
	elf2.Parse(истифодакунанда1data[:], uint32(PageФеҳрастentry+0x1000))
	умумӣoffsettable := elf2.Got

	PValue1Алоқаmap := алоқаmap.Clone()
	PValue1Алоқаmap.Append_to_list(uintptr(elf2.Dynamic))

	memorymanager.Free(истифодакунанда1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(memorymanager.Malloc(4))
	*code1pointer = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(PageФеҳрастentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = истифодакунанда1entry
	thr2.Cpustate.Edx = умумӣoffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PValue1Алоқаmap.First)))

	console.MЧопкарданxy("user1: ", 1, 10)
	console.MUnsignedinteger32Чопкардан(elf2.Got)

	var истифодакунанда2Файл []byte = ([]byte)("USER2")
	size = GetФайлsize(истифодакунанда2Файл)
	истифодакунанда2address := memorymanager.Malloc(size)
	истифодакунанда2data := Getbytesfrompointer(uintptr(истифодакунанда2address), int(size), int(size))
	ХонданФайл(истифодакунанда2Файл, истифодакунанда2data)

	elf3 := Elf{}

	истифодакунанда2entry := elf3.Getentry(истифодакунанда2data)
	elf3.Parse(истифодакунанда2data[:], uint32(PageФеҳрастentry+0x2000))
	умумӣoffsettable = elf3.Got

	PValue2Алоқаmap := алоқаmap.Clone()
	PValue2Алоқаmap.Append_to_list(uintptr(elf3.Dynamic))

	memorymanager.Free(истифодакунанда2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(memorymanager.Malloc(4))
	*code2pointer = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(PageФеҳрастentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = истифодакунанда2entry
	thr3.Cpustate.Edx = умумӣoffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PValue2Алоқаmap.First)))

	console.MЧопкарданxy("user2: ", 1, 11)
	console.MUnsignedinteger32Чопкардан(thr3.Cpustate.Esi)

	libАлоқаmap.Чопкардан(1, 11)

	var истифодакунанда3Файл []byte = ([]byte)("USER3")
	size = GetФайлsize(истифодакунанда3Файл)
	истифодакунанда3address := memorymanager.Malloc(size)
	истифодакунанда3data := Getbytesfrompointer(uintptr(истифодакунанда3address), int(size), int(size))
	ХонданФайл(истифодакунанда3Файл, истифодакунанда3data)

	elf4 := Elf{}

	истифодакунанда3entry := elf4.Getentry(истифодакунанда3data)
	elf4.Parse(истифодакунанда3data[:], uint32(PageФеҳрастentry+0x3000))
	умумӣoffsettable = elf4.Got

	PValue3Алоқаmap := алоқаmap.Clone()
	PValue3Алоқаmap.Append_to_list(uintptr(elf4.Dynamic))

	memorymanager.Free(истифодакунанда3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(memorymanager.Malloc(4))
	*code3pointer = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(PageФеҳрастentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = истифодакунанда3entry
	thr4.Cpustate.Edx = умумӣoffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PValue3Алоқаmap.First)))

	processhelper.Spawn(TФунксия1, threadhelper, sche, uint32(PageФеҳрастentry+0x4000), true)

	ikeyboardeventhandler = &mykeyboardeventhandler
	keyboarddriver.Initdriver(Interruptmanager, ikeyboardeventhandler)

	mousedriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	дастгоҳdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	Interruptmanager.Active()

	for {
		halt()
	}

}
