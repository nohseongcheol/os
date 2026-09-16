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
import . "ማቋረጫ"
import . "multitasking"
import . "tasking/tss"

import . "virtualማስታወሻ"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/ሂደቶች"
import . "driver/driver"

import . "driver/የፊደልሠሌዳ"
import . "driver/አይጥ"

import . "driver/ata"
import . "ፋይልስርአት/msdospartition"
import . "ፋይልስርአት/fat"

import . "ፋይልስርአት/elf"

import . "ስርአትcall"

import . "ማስታወሻmanager"
import . "pci"

func halt()

var iየፊደልሠሌዳeventhandler Iየፊደልሠሌዳeventhandler

type TMyየፊደልሠሌዳeventhandler struct {
}

var myየፊደልሠሌዳeventhandler TMyየፊደልሠሌዳeventhandler
var የፊደልሠሌዳdriver Tየፊደልሠሌዳdriver
var አይጥdriver Tአይጥdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var የፊደልሠሌዳconsole TConsole = TConsole{}

func (self *TMyየፊደልሠሌዳeventhandler) Oማብሪያቁልፍወደታች(ቁልፍ byte) {
	foo := [1]byte{' '}
	foo[0] = ቁልፍ

	የፊደልሠሌዳconsole.Mማተሚያባይትስxy(foo[:], 1000, 1000)
}

func (self *TMyየፊደልሠሌዳeventhandler) Oማብሪያቁልፍወደላይ(ቁልፍ byte)	{}

var iአይጥeventhandler Iአይጥeventhandler

type TMyአይጥeventhandler struct {
}

var አይጥconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xአካባቢ int16 = 0
var yአካባቢ int16 = 0

func (self *TMyአይጥeventhandler) Oማብሪያአይጥወደታች(button int8) {
	buffer := []byte("x")
	አይጥconsole.Mማተሚያxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyአይጥeventhandler) Oማብሪያአይጥወደላይ(button int8)	{}
func (self *TMyአይጥeventhandler) Oማብሪያአይጥመንቀሳቅስ(x int8, y int8) {

	xአካባቢ += int16(x)
	if xአካባቢ < 0 {
		xአካባቢ = 0
	}
	if xአካባቢ >= 80 {
		xአካባቢ = 79
	}

	yአካባቢ -= int16(y)

	if yአካባቢ < 0 {
		yአካባቢ = 0
	}
	if yአካባቢ >= 25 {
		yአካባቢ = 24
	}

	buffer := []byte(" ")
	አይጥconsole.Mማተሚያxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	አይጥconsole.Mማተሚያxy(buffer, uint16(xአካባቢ), uint16(yአካባቢ))

	previousx = xአካባቢ
	previousy = yአካባቢ
}

var ዲቫይስdescriptor TPeripheralcomponentinterconnectዲቫይስdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Oማብሪያgetdriver(ዲቫይስ TPeripheralcomponentinterconnectዲቫይስdescriptor) {
	if ዲቫይስ.Vሻጭመለያ == 0x1022 && ዲቫይስ.Dዲቫይስመለያ == 0x2000 {
		console.Mማተሚያxy([]byte("["), 0, 12)
		console.Mማተሚያ(([]byte)("AMD am79c973"))
		console.Mማተሚያ([]byte(":"))
		console.MUnsignedinteger16ማተሚያ(ዲቫይስ.Vሻጭመለያ)
		console.Mማተሚያ([]byte(":"))
		console.MUnsignedinteger16ማተሚያ(ዲቫይስ.Dዲቫይስመለያ)
		console.Mማተሚያ([]byte(":"))
		console.MUnsignedinteger16ማተሚያ(uint16(ዲቫይስ.Portbase))
		console.Mማተሚያ([]byte(":"))
		console.MUnsignedinteger32ማተሚያ(ዲቫይስ.Iማቋረጫ)

		console.Mማተሚያ([]byte("]\n"))
		ዲቫይስdescriptor = ዲቫይስ
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectዲቫይስdescriptor {
	return ዲቫይስdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pማተሚያstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.Mማተሚያ(str)
}

func Getፋይልመጠን(የፋይልስም []byte) uint32 {
	var ata0s = Tጠለቅቴክኖሎጂattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionሰንጠረዥ{}
	partition.Rማንበቢያpartition(&ata0s)

	bios := TBiosparameterመከልከያ32{}

	var መጠን uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም)
	ata0s.Flush()

	return መጠን
}

func Rማንበቢያፋይል(የፋይልስም []byte, data []byte) {
	var ata0s = Tጠለቅቴክኖሎጂattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionሰንጠረዥ{}
	partition.Rማንበቢያpartition(&ata0s)

	bios := TBiosparameterመከልከያ32{}
	bios.Rማንበቢያ(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም, data)

	ata0s.Flush()
}
func Lመጫኛelf() {

	var ata0s = Tጠለቅቴክኖሎጂattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionሰንጠረዥ{}
	partition.Rማንበቢያpartition(&ata0s)

	bios := TBiosparameterመከልከያ32{}

	var የፋይልስም []byte = ([]byte)("TEST")
	var መጠን uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Rማንበቢያ(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም, data)

	elf := Elf{}

	elf.Parse(data[:መጠን], 0x4f00000)

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

		Sysማተሚያunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ማስገቢያeventtask() {
	for {
		Pሂደቶችpendingየፊደልሠሌዳevents()
		Pሂደቶችpendingአይጥevents()
		halt()
	}
}

func memorytest(y int) {
	ማስታወሻmanager := &Tማስታወሻmanager{}
	allocated := uint32(uintptr(ማስታወሻmanager.Malloc(1024)))
	console.MUnsignedinteger32ማተሚያxy(allocated, 10, uint16(y))
	if y == 11 {
		ማስታወሻmanager.Fነፃ(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Rእንደገናመጫኛcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Setcr3(cr3 uint32)
func Getcr4() uint32
func Eአስቻለpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getfunctionስም(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcስም = runtime.FuncForPC(address).Name()
	var funcባይትስ []byte = []byte(funcስም)

	taskconsole.Mማተሚያxy(funcባይትስ, 1, 5)
	taskconsole.Mማተሚያ(([]byte)(":"))
	taskconsole.MUnsignedinteger32ማተሚያ(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.Mማተሚያunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pገጽዳይሬክቶሪentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.Mማተሚያ("\n=== ETH BOOT ===\n")

	console.Mማተሚያunsignedinteger32(uint32(Pገጽዳይሬክቶሪentry), 0, 2)
	console.Mማተሚያunsignedinteger32(uint32(Pገጽዳይሬክቶሪentry), 10, 2)
	console.Mማተሚያunsignedinteger32(uint32(stacktop), 0, 3)
	console.Mማተሚያunsignedinteger32(uint32(stackbottom), 10, 3)

	ማስታወሻmanager := &Tማስታወሻmanager{}
	ማስታወሻmanager.Init(0, Maxqueueመጠን)

	paging := &Paging{}
	paging.Init(Pገጽዳይሬክቶሪentry, 0x500000, ማስታወሻmanager)
	paging.Sharedማስታወሻregion()

	Setcr3(uint32(Pገጽዳይሬክቶሪentry))
	Eአስቻለpaging()

	shareddescriptorሰንጠረዥ := &TShareddescriptorሰንጠረዥ{}
	shareddescriptorሰንጠረዥ.Init()

	console.Mማተሚያ("esp:")

	esp := getesp()
	console.MUnsignedinteger32ማተሚያ(uint32(esp))

	tls := gettls()
	console.Mማተሚያ(([]byte)("tls:"))
	console.MUnsignedinteger32ማተሚያ(tls)

	tss.Iመግጠም(shareddescriptorሰንጠረዥ, 7, Segkerneldata, esp)

	Virtመሞከሪያ()

	cr3 := Rእንደገናመጫኛcr3()
	console.Mማተሚያ(([]byte)(":cr3:"))
	console.MUnsignedinteger32ማተሚያ(cr3)

	cr0 := Getcr0()
	console.Mማተሚያ(([]byte)(":cr0:"))
	console.MUnsignedinteger32ማተሚያ(cr0)

	cr4 := Getcr4()
	console.Mማተሚያ(([]byte)(":cr4:"))
	console.MUnsignedinteger32ማተሚያ(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Iማቋረጫmanager := &Tማቋረጫmanager{}
	Iማቋረጫmanager.Init(0x20, shareddescriptorሰንጠረዥ, taskmanager_2)

	paging.Pገጽfault(Iማቋረጫmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(ማስታወሻmanager)

	ሂደቶችhelper := Pሂደቶችhelper{}
	ሂደቶችhelper.Init(ማስታወሻmanager, Pገጽዳይሬክቶሪentry)

	sche := &Scheduler{}
	sche.Init(Iማቋረጫmanager, ማስታወሻmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Iማቋረጫmanager)

	ሂደቶችhelper.Spawn(taska, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry), true)
	ሂደቶችhelper.Spawn(taskb, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry), true)
	ሂደቶችhelper.Spawn(taskc, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry), true)
	ሂደቶችhelper.Spawn(taskd1, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry), true)
	ሂደቶችhelper.Spawn(ማስገቢያeventtask, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry), true)

	var መጠን uint32

	var linkerፋይል []byte = ([]byte)("LINKER")
	መጠን = Getፋይልመጠን(linkerፋይል)
	linkeraddress := ማስታወሻmanager.Malloc(መጠን)
	linkerdata := Getባይትስfromጠቋሚ(uintptr(linkeraddress), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(linkerፋይል, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Pገጽዳይሬክቶሪentry))

	አገናኝmap := Lአገናኝmap{}
	አገናኝmap.Init(ማስታወሻmanager)

	var lib1ፋይል []byte = ([]byte)("LIB1")
	መጠን = Getፋይልመጠን(lib1ፋይል)

	lib1address := ማስታወሻmanager.Malloc(መጠን)
	lib1data := Getባይትስfromጠቋሚ(uintptr(lib1address), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(lib1ፋይል, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Pገጽዳይሬክቶሪentry))
	ማስታወሻmanager.Fነፃ(lib1address)

	አገናኝmap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2ፋይል []byte = ([]byte)("LIB2")
	መጠን = Getፋይልመጠን(lib2ፋይል)

	lib2address := ማስታወሻmanager.Malloc(መጠን)
	lib2data := Getባይትስfromጠቋሚ(uintptr(lib2address), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(lib2ፋይል, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Pገጽዳይሬክቶሪentry))
	ማስታወሻmanager.Fነፃ(lib2address)

	አገናኝmap.Append_to_list(uintptr(lib2elf.Dynamic))

	libአገናኝmap := አገናኝmap.Clone()
	አገናኝmapaddress := uint32(uintptr(Pointer(libአገናኝmap.First)))

	lib1got := Getunsignedinteger32ማዘጋጃfromጠቋሚ(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = አገናኝmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ማዘጋጃfromጠቋሚ(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = አገናኝmapaddress
	lib2got[2] = 0x4000000

	console.Mማተሚያxy("lib1: ", 1, 8)
	console.MUnsignedinteger32ማተሚያ(lib1elf.Got)
	console.Mማተሚያ(":")
	console.MUnsignedinteger32ማተሚያ(lib1elf.Dynamic)

	console.Mማተሚያxy("lib2: ", 1, 9)
	console.MUnsignedinteger32ማተሚያ(lib2elf.Got)
	console.Mማተሚያ(":")
	console.MUnsignedinteger32ማተሚያ(lib2elf.Dynamic)

	var ተጠቃሚ1ፋይል []byte = ([]byte)("USER1")
	መጠን = Getፋይልመጠን(ተጠቃሚ1ፋይል)
	ተጠቃሚ1address := ማስታወሻmanager.Malloc(መጠን)
	ተጠቃሚ1data := Getባይትስfromጠቋሚ(uintptr(ተጠቃሚ1address), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(ተጠቃሚ1ፋይል, ተጠቃሚ1data)

	elf2 := Elf{}

	ተጠቃሚ1entry := elf2.Getentry(ተጠቃሚ1data)
	elf2.Parse(ተጠቃሚ1data[:], uint32(Pገጽዳይሬክቶሪentry+0x1000))
	አለምአቀፍoffsetሰንጠረዥ := elf2.Got

	Pዋጋ1አገናኝmap := አገናኝmap.Clone()
	Pዋጋ1አገናኝmap.Append_to_list(uintptr(elf2.Dynamic))

	ማስታወሻmanager.Fነፃ(ተጠቃሚ1address)

	var code1ጠቋሚ *uintptr
	var func1val func()

	code1ጠቋሚ = (*uintptr)(ማስታወሻmanager.Malloc(4))
	*code1ጠቋሚ = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1ጠቋሚ))

	proc2 := ሂደቶችhelper.Spawn(func1val, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpuሁኔታ.Ecx = ተጠቃሚ1entry
	thr2.Cpuሁኔታ.Edx = አለምአቀፍoffsetሰንጠረዥ
	thr2.Cpuሁኔታ.Esi = uint32(uintptr(Pointer(Pዋጋ1አገናኝmap.First)))

	console.Mማተሚያxy("user1: ", 1, 10)
	console.MUnsignedinteger32ማተሚያ(elf2.Got)

	var ተጠቃሚ2ፋይል []byte = ([]byte)("USER2")
	መጠን = Getፋይልመጠን(ተጠቃሚ2ፋይል)
	ተጠቃሚ2address := ማስታወሻmanager.Malloc(መጠን)
	ተጠቃሚ2data := Getባይትስfromጠቋሚ(uintptr(ተጠቃሚ2address), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(ተጠቃሚ2ፋይል, ተጠቃሚ2data)

	elf3 := Elf{}

	ተጠቃሚ2entry := elf3.Getentry(ተጠቃሚ2data)
	elf3.Parse(ተጠቃሚ2data[:], uint32(Pገጽዳይሬክቶሪentry+0x2000))
	አለምአቀፍoffsetሰንጠረዥ = elf3.Got

	Pዋጋ2አገናኝmap := አገናኝmap.Clone()
	Pዋጋ2አገናኝmap.Append_to_list(uintptr(elf3.Dynamic))

	ማስታወሻmanager.Fነፃ(ተጠቃሚ2address)

	var code2ጠቋሚ *uintptr
	var func2val func()

	code2ጠቋሚ = (*uintptr)(ማስታወሻmanager.Malloc(4))
	*code2ጠቋሚ = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2ጠቋሚ))

	proc3 := ሂደቶችhelper.Spawn(func2val, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpuሁኔታ.Ecx = ተጠቃሚ2entry
	thr3.Cpuሁኔታ.Edx = አለምአቀፍoffsetሰንጠረዥ
	thr3.Cpuሁኔታ.Esi = uint32(uintptr(Pointer(Pዋጋ2አገናኝmap.First)))

	console.Mማተሚያxy("user2: ", 1, 11)
	console.MUnsignedinteger32ማተሚያ(thr3.Cpuሁኔታ.Esi)

	libአገናኝmap.Pማተሚያ(1, 11)

	var ተጠቃሚ3ፋይል []byte = ([]byte)("USER3")
	መጠን = Getፋይልመጠን(ተጠቃሚ3ፋይል)
	ተጠቃሚ3address := ማስታወሻmanager.Malloc(መጠን)
	ተጠቃሚ3data := Getባይትስfromጠቋሚ(uintptr(ተጠቃሚ3address), int(መጠን), int(መጠን))
	Rማንበቢያፋይል(ተጠቃሚ3ፋይል, ተጠቃሚ3data)

	elf4 := Elf{}

	ተጠቃሚ3entry := elf4.Getentry(ተጠቃሚ3data)
	elf4.Parse(ተጠቃሚ3data[:], uint32(Pገጽዳይሬክቶሪentry+0x3000))
	አለምአቀፍoffsetሰንጠረዥ = elf4.Got

	Pዋጋ3አገናኝmap := አገናኝmap.Clone()
	Pዋጋ3አገናኝmap.Append_to_list(uintptr(elf4.Dynamic))

	ማስታወሻmanager.Fነፃ(ተጠቃሚ3address)

	var code3ጠቋሚ *uintptr
	var func3val func()

	code3ጠቋሚ = (*uintptr)(ማስታወሻmanager.Malloc(4))
	*code3ጠቋሚ = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3ጠቋሚ))

	proc4 := ሂደቶችhelper.Spawn(func3val, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpuሁኔታ.Ecx = ተጠቃሚ3entry
	thr4.Cpuሁኔታ.Edx = አለምአቀፍoffsetሰንጠረዥ
	thr4.Cpuሁኔታ.Esi = uint32(uintptr(Pointer(Pዋጋ3አገናኝmap.First)))

	ሂደቶችhelper.Spawn(TFunction1, threadhelper, sche, uint32(Pገጽዳይሬክቶሪentry+0x4000), true)

	iየፊደልሠሌዳeventhandler = &myየፊደልሠሌዳeventhandler
	የፊደልሠሌዳdriver.Initdriver(Iማቋረጫmanager, iየፊደልሠሌዳeventhandler)

	አይጥdriver.Initdriver(Iማቋረጫmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Sይምረጡdriver(&Drivermanager, Iማቋረጫmanager)
	ዲቫይስdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Eያስችላል(true)
	Iማቋረጫmanager.Aአሰራ()

	for {
		halt()
	}

}
