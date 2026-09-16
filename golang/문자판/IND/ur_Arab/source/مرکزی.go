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

import . "virtmem"
import . "paging"
import . "tasking/عملی_دھارا"
import . "tasking/scheduler"
import . "tasking/عمل"
import . "drivers/driver"

import . "drivers/keyboard"
import . "drivers/mouse"

import . "drivers/ata"
import . "filesystem/msdospart"
import . "filesystem/fat"

import . "filesystem/elf"

import . "نظامی_طلب"

import . "حافظہ"
import . "pci"

func 멈추기()

var iKeyboardEventHandler IKeyboardEventHandler

type TMyKeyboardEventHandler struct {
}

var myKeyboardEventHandler TMyKeyboardEventHandler
var keyboardDriver TKeyboardDriver
var mouseDriver TMouseDriver
var pciController TPeripheralComponentInterconnectController

var 키보드콘솔 T콘솔 = T콘솔{}

func (self *TMyKeyboardEventHandler) OnKeyDown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	키보드콘솔.M출력BytesXY(foo[:], 1000, 1000)
}

func (self *TMyKeyboardEventHandler) OnKeyUp(key byte)	{}

var iMouseEventHandler IMouseEventHandler

type TMyMouseEventHandler struct {
}

var 마우스콘솔 T콘솔 = T콘솔{}
var prevX int16 = 0
var prevY int16 = 0
var xPos int16 = 0
var yPos int16 = 0

func (self *TMyMouseEventHandler) OnMouseDown(button int8) {
	buf := []byte("x")
	마우스콘솔.M출력XY(buf, uint16(prevX), uint16(prevY))
}
func (self *TMyMouseEventHandler) OnMouseUp(button int8)	{}
func (self *TMyMouseEventHandler) OnMouseMove(x int8, y int8) {

	xPos += int16(x)
	if xPos < 0 {
		xPos = 0
	}
	if xPos >= 80 {
		xPos = 79
	}

	yPos -= int16(y)

	if yPos < 0 {
		yPos = 0
	}
	if yPos >= 25 {
		yPos = 24
	}

	buf := []byte(" ")
	마우스콘솔.M출력XY(buf, uint16(prevX), uint16(prevY))

	buf = []byte("+")
	마우스콘솔.M출력XY(buf, uint16(xPos), uint16(yPos))

	prevX = xPos
	prevY = yPos
}

var deviceDescriptor TPeripheralComponentInterconnectDeviceDescriptor
var iPCIControllerHandler IPCIControllerHandler

type TMyPCIControllerHandler struct {
}

var console T콘솔 = T콘솔{}
var drivercount uint16 = 0

func (self TMyPCIControllerHandler) OnGetDriver(dev TPeripheralComponentInterconnectDeviceDescriptor) {
	if dev.Vendor_id == 0x1022 && dev.Device_id == 0x2000 {
		console.M출력XY([]byte("["), 0, 12)
		console.M출력(([]byte)("AMD am79c973"))
		console.M출력([]byte(":"))
		console.MUint16출력(dev.Vendor_id)
		console.M출력([]byte(":"))
		console.MUint16출력(dev.Device_id)
		console.M출력([]byte(":"))
		console.MUint16출력(uint16(dev.PortBase))
		console.M출력([]byte(":"))
		console.MUint32출력(dev.Interrupt)

		console.M출력([]byte("]\n"))
		deviceDescriptor = dev
		drivercount++
	}
}
func (self TMyPCIControllerHandler) GetDriver() TPeripheralComponentInterconnectDeviceDescriptor {
	return deviceDescriptor
}

var str []byte = ([]byte)("GetStr")

func GetStr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func PrintStr(p_str uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(p_str)))
	console.M출력(str)
}

func GetFileSize(filename []byte) uint32 {
	var ata0s = TAdvancedTechnologyAttachment{}
	ata0s.Vآغاز_کرنا(false, 0x1F0)
	ata0s.Identify()

	partition := TMSDOSPartitionTable{}
	partition.ReadPartitions(&ata0s)

	bios := TBiosParameterBlock32{}

	var حجم uint32 = bios.Len(&ata0s, partition.MBR.PrimaryPartition[0], filename)
	ata0s.Flush()

	return حجم
}

func Vفائل_پڑھنا(filename []byte, data []byte) {
	var ata0s = TAdvancedTechnologyAttachment{}
	ata0s.Vآغاز_کرنا(false, 0x1F0)
	ata0s.Identify()

	partition := TMSDOSPartitionTable{}
	partition.ReadPartitions(&ata0s)

	bios := TBiosParameterBlock32{}
	bios.Vپڑھنا(&ata0s, partition.MBR.PrimaryPartition[0], filename, data)

	ata0s.Flush()
}
func LoadElf() {

	var ata0s = TAdvancedTechnologyAttachment{}
	ata0s.Vآغاز_کرنا(false, 0x1F0)
	ata0s.Identify()

	partition := TMSDOSPartitionTable{}
	partition.ReadPartitions(&ata0s)

	bios := TBiosParameterBlock32{}

	var filename []byte = ([]byte)("TEST")
	var حجم uint32 = bios.Len(&ata0s, partition.MBR.PrimaryPartition[0], filename)
	var dataBuf [100 * 1024]byte
	var data []byte = dataBuf[:]
	bios.Vپڑھنا(&ata0s, partition.MBR.PrimaryPartition[0], filename, data)

	elf := Elf{}

	elf.Parse(data[:حجم], 0x4f00000)

}

var 작업콘솔 T콘솔 = T콘솔{}

func T함수1() {
	buf := []byte("--TFunc1--")
	for {
		Sys_printf(buf)
	}
}
func taskA() {
	buf := []byte("A")
	for {
		Sys_printf(buf)

	}
}
func taskB() {
	buf := []byte("B")
	for {
		Sys_printf(buf)
	}
}

func taskC() {
	buf := []byte("C")
	for {
		Sys_printf(buf)
	}
}
func taskD()

func taskD0() {
	esi := getESI()
	for {

		Sys_printUint32(esi)

	}
}

func taskD1() {
	buf := ([]byte)("taskD1")
	for {
		Sys_printf(buf)
	}
}

func inputEventTask() {
	for {
		ProcessPendingKeyboardEvents()
		ProcessPendingMouseEvents()
		멈추기()
	}
}

func memorytest(y int) {
	memoryManager := &TMemoryManager{}
	allocated := uint32(uintptr(memoryManager.Vحافظہ_مختص_کرنا(1024)))
	console.MUint32출력XY(allocated, 10, uint16(y))
	if y == 11 {
		memoryManager.Vحافظہ_آزاد_کرنا(Pointer(uintptr(allocated)))
	}
}

func getESP() uint32
func getESI() uint32
func getGS() uint32
func getTLS() uint32
func PAUSE_LOOP()
func ReloadCR3() uint32

func GetCR0() uint32
func GetCR2() uint32
func GetCR3() uint32
func SetCR3(cr3 uint32)
func GetCR4() uint32
func EnablePaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		멈추기()
	}
}

func GetFunctionName(i interface{}) {
	var addr = reflect.ValueOf(i).Pointer()
	var func_name = runtime.FuncForPC(addr).Name()
	var func_bytes []byte = []byte(func_name)

	작업콘솔.M출력XY(func_bytes, 1, 5)
	작업콘솔.M출력(([]byte)(":"))
	작업콘솔.MUint32출력(uint32(uintptr(addr)))
}

func printreg() {
	cr0 := GetCR0()
	작업콘솔.M출력Uint32(cr0, 2, 1)
}

var tss *TSSEntry = &TSSEntry{}

func KKernelEntry(PageDirEntry uintptr, stacktop uintptr, stackbottom uintptr) {

	M직렬로그초기화()
	console.M출력("\n=== IND BOOT ===\n")

	console.M출력Uint32(uint32(PageDirEntry), 0, 2)
	console.M출력Uint32(uint32(PageDirEntry), 10, 2)
	console.M출력Uint32(uint32(stacktop), 0, 3)
	console.M출력Uint32(uint32(stackbottom), 10, 3)

	memoryManager := &TMemoryManager{}
	memoryManager.Vآغاز_کرنا(0, MAX_QUEUE_SIZE)

	paging := &Paging{}
	paging.Vآغاز_کرنا(PageDirEntry, 0x500000, memoryManager)
	paging.SharedMemoryRegion()

	SetCR3(uint32(PageDirEntry))
	EnablePaging()

	공용서술자테이블 := &T공용서술자테이블{}
	공용서술자테이블.Vآغاز_کرنا()

	console.M출력("esp:")

	esp := getESP()
	console.MUint32출력(uint32(esp))

	tls := getTLS()
	console.M출력(([]byte)("tls:"))
	console.MUint32출력(tls)

	tss.Install(공용서술자테이블, 7, SEG_KERNEL_DATA, esp)

	VirtTest()

	cr3 := ReloadCR3()
	console.M출력(([]byte)(":cr3:"))
	console.MUint32출력(cr3)

	cr0 := GetCR0()
	console.M출력(([]byte)(":cr0:"))
	console.MUint32출력(cr0)

	cr4 := GetCR4()
	console.M출력(([]byte)(":cr4:"))
	console.MUint32출력(cr4)

	작업관리자 := &T작업관리자{}
	작업관리자.Vآغاز_کرنا()

	InterruptManager := &TInterruptManager{}
	InterruptManager.Vآغاز_کرنا(0x20, 공용서술자테이블, 작업관리자)

	paging.PageFault(InterruptManager)

	DriverManager := TDriverManager{}
	DriverManager.Vآغاز_کرنا()

	threadHelper := &TThreadHelper{}
	threadHelper.Vآغاز_کرنا(memoryManager)

	processHelper := ProcessHelper{}
	processHelper.Vآغاز_کرنا(memoryManager, PageDirEntry)

	sche := &Scheduler{}
	sche.Vآغاز_کرنا(InterruptManager, memoryManager, tss)

	sysCall := &TSyscall{}
	sysCall.Vآغاز_کرنا(InterruptManager)

	processHelper.Spawn(taskA, threadHelper, sche, uint32(PageDirEntry), true)
	processHelper.Spawn(taskB, threadHelper, sche, uint32(PageDirEntry), true)
	processHelper.Spawn(taskC, threadHelper, sche, uint32(PageDirEntry), true)
	processHelper.Spawn(taskD1, threadHelper, sche, uint32(PageDirEntry), true)
	processHelper.Spawn(inputEventTask, threadHelper, sche, uint32(PageDirEntry), true)

	var حجم uint32

	var linkerFile []byte = ([]byte)("LINKER")
	حجم = GetFileSize(linkerFile)
	linkerAddr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	linkerData := GetBytesFromPtr(uintptr(linkerAddr), int(حجم), int(حجم))
	Vفائل_پڑھنا(linkerFile, linkerData)

	elf0 := Elf{}
	linkerEntry := elf0.GetEntry(linkerData)
	elf0.Parse(linkerData[:], uint32(PageDirEntry))

	linkMap := LinkMap{}
	linkMap.Vآغاز_کرنا(memoryManager)

	var lib1File []byte = ([]byte)("LIB1")
	حجم = GetFileSize(lib1File)

	lib1Addr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	lib1Data := GetBytesFromPtr(uintptr(lib1Addr), int(حجم), int(حجم))
	Vفائل_پڑھنا(lib1File, lib1Data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1Data[:], uint32(PageDirEntry))
	memoryManager.Vحافظہ_آزاد_کرنا(lib1Addr)

	linkMap.Vفہرست_کے_آخر_میں_شامل_کرنا(uintptr(lib1elf.Dynamic))

	var lib2File []byte = ([]byte)("LIB2")
	حجم = GetFileSize(lib2File)

	lib2Addr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	lib2Data := GetBytesFromPtr(uintptr(lib2Addr), int(حجم), int(حجم))
	Vفائل_پڑھنا(lib2File, lib2Data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2Data[:], uint32(PageDirEntry))
	memoryManager.Vحافظہ_آزاد_کرنا(lib2Addr)

	linkMap.Vفہرست_کے_آخر_میں_شامل_کرنا(uintptr(lib2elf.Dynamic))

	libLinkMap := linkMap.Clone()
	linkMapAddr := uint32(uintptr(Pointer(libLinkMap.First)))

	lib1GOT := GetUint32ArrayFromPtr(uintptr(lib1elf.GOT), 4, 4)
	lib1GOT[1] = linkMapAddr
	lib1GOT[2] = 0x4000000

	lib2GOT := GetUint32ArrayFromPtr(uintptr(lib2elf.GOT), 4, 4)
	lib2GOT[1] = linkMapAddr
	lib2GOT[2] = 0x4000000

	console.M출력XY("lib1: ", 1, 8)
	console.MUint32출력(lib1elf.GOT)
	console.M출력(":")
	console.MUint32출력(lib1elf.Dynamic)

	console.M출력XY("lib2: ", 1, 9)
	console.MUint32출력(lib2elf.GOT)
	console.M출력(":")
	console.MUint32출력(lib2elf.Dynamic)

	var user1file []byte = ([]byte)("USER1")
	حجم = GetFileSize(user1file)
	user1addr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	user1data := GetBytesFromPtr(uintptr(user1addr), int(حجم), int(حجم))
	Vفائل_پڑھنا(user1file, user1data)

	elf2 := Elf{}

	user1entry := elf2.GetEntry(user1data)
	elf2.Parse(user1data[:], uint32(PageDirEntry+0x1000))
	globalOffsetTable := elf2.GOT

	P1LinkMap := linkMap.Clone()
	P1LinkMap.Vفہرست_کے_آخر_میں_شامل_کرنا(uintptr(elf2.Dynamic))

	memoryManager.Vحافظہ_آزاد_کرنا(user1addr)

	var code1Ptr *uintptr
	var func1Val func()

	code1Ptr = (*uintptr)(memoryManager.Vحافظہ_مختص_کرنا(4))
	*code1Ptr = uintptr(linkerEntry)
	func1Val = *(*func())(Pointer(&code1Ptr))

	proc2 := processHelper.Spawn(func1Val, threadHelper, sche, uint32(PageDirEntry+0x1000), false)
	thr2 := (*Tعملی_دھارا)(proc2.Threads.GetAt(0))
	thr2.CpuState.Ecx = user1entry
	thr2.CpuState.Edx = globalOffsetTable
	thr2.CpuState.Esi = uint32(uintptr(Pointer(P1LinkMap.First)))

	console.M출력XY("user1: ", 1, 10)
	console.MUint32출력(elf2.GOT)

	var user2file []byte = ([]byte)("USER2")
	حجم = GetFileSize(user2file)
	user2addr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	user2data := GetBytesFromPtr(uintptr(user2addr), int(حجم), int(حجم))
	Vفائل_پڑھنا(user2file, user2data)

	elf3 := Elf{}

	user2entry := elf3.GetEntry(user2data)
	elf3.Parse(user2data[:], uint32(PageDirEntry+0x2000))
	globalOffsetTable = elf3.GOT

	P2LinkMap := linkMap.Clone()
	P2LinkMap.Vفہرست_کے_آخر_میں_شامل_کرنا(uintptr(elf3.Dynamic))

	memoryManager.Vحافظہ_آزاد_کرنا(user2addr)

	var code2Ptr *uintptr
	var func2Val func()

	code2Ptr = (*uintptr)(memoryManager.Vحافظہ_مختص_کرنا(4))
	*code2Ptr = uintptr(linkerEntry)
	func2Val = *(*func())(Pointer(&code2Ptr))

	proc3 := processHelper.Spawn(func2Val, threadHelper, sche, uint32(PageDirEntry+0x2000), false)
	thr3 := (*Tعملی_دھارا)(proc3.Threads.GetAt(0))
	thr3.CpuState.Ecx = user2entry
	thr3.CpuState.Edx = globalOffsetTable
	thr3.CpuState.Esi = uint32(uintptr(Pointer(P2LinkMap.First)))

	console.M출력XY("user2: ", 1, 11)
	console.MUint32출력(thr3.CpuState.Esi)

	libLinkMap.Print(1, 11)

	var user3file []byte = ([]byte)("USER3")
	حجم = GetFileSize(user3file)
	user3addr := memoryManager.Vحافظہ_مختص_کرنا(حجم)
	user3data := GetBytesFromPtr(uintptr(user3addr), int(حجم), int(حجم))
	Vفائل_پڑھنا(user3file, user3data)

	elf4 := Elf{}

	user3entry := elf4.GetEntry(user3data)
	elf4.Parse(user3data[:], uint32(PageDirEntry+0x3000))
	globalOffsetTable = elf4.GOT

	P3LinkMap := linkMap.Clone()
	P3LinkMap.Vفہرست_کے_آخر_میں_شامل_کرنا(uintptr(elf4.Dynamic))

	memoryManager.Vحافظہ_آزاد_کرنا(user3addr)

	var code3Ptr *uintptr
	var func3Val func()

	code3Ptr = (*uintptr)(memoryManager.Vحافظہ_مختص_کرنا(4))
	*code3Ptr = uintptr(linkerEntry)
	func3Val = *(*func())(Pointer(&code3Ptr))

	proc4 := processHelper.Spawn(func3Val, threadHelper, sche, uint32(PageDirEntry+0x3000), false)
	thr4 := (*Tعملی_دھارا)(proc4.Threads.GetAt(0))
	thr4.CpuState.Ecx = user3entry
	thr4.CpuState.Edx = globalOffsetTable
	thr4.CpuState.Esi = uint32(uintptr(Pointer(P3LinkMap.First)))

	processHelper.Spawn(T함수1, threadHelper, sche, uint32(PageDirEntry+0x4000), true)

	iKeyboardEventHandler = &myKeyboardEventHandler
	keyboardDriver.InitDriver(InterruptManager, iKeyboardEventHandler)

	mouseDriver.InitDriver(InterruptManager, nil)

	myPCIControllerHandler := TMyPCIControllerHandler{}
	pciController.Vآغاز_کرنا(myPCIControllerHandler)
	pciController.SelectDrivers(&DriverManager, InterruptManager)
	deviceDescriptor = myPCIControllerHandler.GetDriver()

	sche.Enabled(true)
	InterruptManager.Active()

	for {
		멈추기()
	}

}
