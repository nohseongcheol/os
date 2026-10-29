/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsolë"
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtualMemoria"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proçes"
import . "driver/driver"

import . "driver/tastiera"
import . "driver/miu"

import . "driver/ata"
import . "kartelëSistemi/msdospartition"
import . "kartelëSistemi/fat"

import . "kartelëSistemi/elf"

import . "sistemicall"

import . "memoriaManazhuesi"
import . "pci"

func halt()

var iTastieraNgjarjehandler ITastieraNgjarjehandler

type TMyTastieraNgjarjehandler struct {
}

var myTastieraNgjarjehandler TMyTastieraNgjarjehandler
var tastieradriver TTastieradriver
var miudriver TMiudriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastieraKonsolë TKonsolë = TKonsolë{}

func (vetvetja *TMyTastieraNgjarjehandler) OnÇelesPoshtë(çeles byte) {
	foo := [1]byte{' '}
	foo[0] = çeles

	tastieraKonsolë.MPrintobytesxy(foo[:], 1000, 1000)
}

func (vetvetja *TMyTastieraNgjarjehandler) OnÇelesSipër(çeles byte)	{}

var iMiuNgjarjehandler IMiuNgjarjehandler

type TMyMiuNgjarjehandler struct {
}

var miuKonsolë TKonsolë = TKonsolë{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicion int16 = 0
var yPozicion int16 = 0

func (vetvetja *TMyMiuNgjarjehandler) OnMiuPoshtë(buton int8) {
	buffer := []byte("x")
	miuKonsolë.MPrintoxy(buffer, uint16(previousx), uint16(previousy))
}
func (vetvetja *TMyMiuNgjarjehandler) OnMiuSipër(buton int8)	{}
func (vetvetja *TMyMiuNgjarjehandler) OnMiuLëviz(x int8, y int8) {

	xPozicion += int16(x)
	if xPozicion < 0 {
		xPozicion = 0
	}
	if xPozicion >= 80 {
		xPozicion = 79
	}

	yPozicion -= int16(y)

	if yPozicion < 0 {
		yPozicion = 0
	}
	if yPozicion >= 25 {
		yPozicion = 24
	}

	buffer := []byte(" ")
	miuKonsolë.MPrintoxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	miuKonsolë.MPrintoxy(buffer, uint16(xPozicion), uint16(yPozicion))

	previousx = xPozicion
	previousy = yPozicion
}

var dispozitividescriptor TPeripheralcomponentinterconnectDispozitividescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var konsolë TKonsolë = TKonsolë{}
var drivercount uint16 = 0

func (vetvetja TMypcicontrollerhandler) Ongetdriver(dispozitivi TPeripheralcomponentinterconnectDispozitividescriptor) {
	if dispozitivi.Vendorid == 0x1022 && dispozitivi.Dispozitiviid == 0x2000 {
		konsolë.MPrintoxy([]byte("["), 0, 12)
		konsolë.MPrinto(([]byte)("AMD am79c973"))
		konsolë.MPrinto([]byte(":"))
		konsolë.MUnsignedinteger16Printo(dispozitivi.Vendorid)
		konsolë.MPrinto([]byte(":"))
		konsolë.MUnsignedinteger16Printo(dispozitivi.Dispozitiviid)
		konsolë.MPrinto([]byte(":"))
		konsolë.MUnsignedinteger16Printo(uint16(dispozitivi.Portabase))
		konsolë.MPrinto([]byte(":"))
		konsolë.MUnsignedinteger32Printo(dispozitivi.Interrupt)

		konsolë.MPrinto([]byte("]\n"))
		dispozitividescriptor = dispozitivi
		drivercount++
	}
}
func (vetvetja TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectDispozitividescriptor {
	return dispozitividescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Printostr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsolë.MPrinto(str)
}

func GetKartelëMadhësia(emriifile []byte) uint32 {
	var ata0s = TTëmëtejshmetechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Leximipartition(&ata0s)

	bios := TBiosparameterblock32{}

	var madhësia uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], emriifile)
	ata0s.Flush()

	return madhësia
}

func LeximiKartelë(emriifile []byte, data []byte) {
	var ata0s = TTëmëtejshmetechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Leximipartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Leximi(&ata0s, partition.Mbr.Primarypartition[0], emriifile, data)

	ata0s.Flush()
}
func Ngarkoelf() {

	var ata0s = TTëmëtejshmetechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Leximipartition(&ata0s)

	bios := TBiosparameterblock32{}

	var emriifile []byte = ([]byte)("TEST")
	var madhësia uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], emriifile)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Leximi(&ata0s, partition.Mbr.Primarypartition[0], emriifile, data)

	elf := Elf{}

	elf.Parse(data[:madhësia], 0x4f00000)

}

var procesKonsolë TKonsolë = TKonsolë{}

func TFunksion1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func procesa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func procesb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func procesc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func procesd()

func procesd0() {
	esi := getesi()
	for {

		SysPrintounsignedinteger32(esi)

	}
}

func procesd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func hyrjaNgjarjeProces() {
	for {
		ProçespendingTastieraevents()
		ProçespendingMiuevents()
		halt()
	}
}

func memorytest(y int) {
	memoriaManazhuesi := &TMemoriaManazhuesi{}
	allocated := uint32(uintptr(memoriaManazhuesi.Malloc(1024)))
	konsolë.MUnsignedinteger32Printoxy(allocated, 10, uint16(y))
	if y == 11 {
		memoriaManazhuesi.Elirë(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauseloop()
func Ringarkocr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Caktonicr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunksionEmri(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcEmri = runtime.FuncForPC(address).Name()
	var funcbytes []byte = []byte(funcEmri)

	procesKonsolë.MPrintoxy(funcbytes, 1, 5)
	procesKonsolë.MPrinto(([]byte)(":"))
	procesKonsolë.MUnsignedinteger32Printo(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	procesKonsolë.MPrintounsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(FaqeDosjeentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialRegjistërinit()
	konsolë.MPrinto("\n=== ALB BOOT ===\n")

	konsolë.MPrintounsignedinteger32(uint32(FaqeDosjeentry), 0, 2)
	konsolë.MPrintounsignedinteger32(uint32(FaqeDosjeentry), 10, 2)
	konsolë.MPrintounsignedinteger32(uint32(stacktop), 0, 3)
	konsolë.MPrintounsignedinteger32(uint32(stackbottom), 10, 3)

	memoriaManazhuesi := &TMemoriaManazhuesi{}
	memoriaManazhuesi.Init(0, MaxqueueMadhësia)

	paging := &Paging{}
	paging.Init(FaqeDosjeentry, 0x500000, memoriaManazhuesi)
	paging.SharedMemoriaregion()

	Caktonicr3(uint32(FaqeDosjeentry))
	Enablepaging()

	shareddescriptorTabela := &TShareddescriptorTabela{}
	shareddescriptorTabela.Init()

	konsolë.MPrinto("esp:")

	esp := getesp()
	konsolë.MUnsignedinteger32Printo(uint32(esp))

	tls := gettls()
	konsolë.MPrinto(([]byte)("tls:"))
	konsolë.MUnsignedinteger32Printo(tls)

	tss.Instalo(shareddescriptorTabela, 7, Segkerneldata, esp)

	VirtProvo()

	cr3 := Ringarkocr3()
	konsolë.MPrinto(([]byte)(":cr3:"))
	konsolë.MUnsignedinteger32Printo(cr3)

	cr0 := Getcr0()
	konsolë.MPrinto(([]byte)(":cr0:"))
	konsolë.MUnsignedinteger32Printo(cr0)

	cr4 := Getcr4()
	konsolë.MPrinto(([]byte)(":cr4:"))
	konsolë.MUnsignedinteger32Printo(cr4)

	procesManazhuesi_2 := &TProcesManazhuesi{}
	procesManazhuesi_2.Init()

	InterruptManazhuesi := &TInterruptManazhuesi{}
	InterruptManazhuesi.Init(0x20, shareddescriptorTabela, procesManazhuesi_2)

	paging.Faqefault(InterruptManazhuesi)

	DriverManazhuesi := TDriverManazhuesi{}
	DriverManazhuesi.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memoriaManazhuesi)

	proçeshelper := Proçeshelper{}
	proçeshelper.Init(memoriaManazhuesi, FaqeDosjeentry)

	sche := &Scheduler{}
	sche.Init(InterruptManazhuesi, memoriaManazhuesi, tss)

	syscall := &TSyscall{}
	syscall.Init(InterruptManazhuesi)

	proçeshelper.Spawn(procesa, threadhelper, sche, uint32(FaqeDosjeentry), true)
	proçeshelper.Spawn(procesb, threadhelper, sche, uint32(FaqeDosjeentry), true)
	proçeshelper.Spawn(procesc, threadhelper, sche, uint32(FaqeDosjeentry), true)
	proçeshelper.Spawn(procesd1, threadhelper, sche, uint32(FaqeDosjeentry), true)
	proçeshelper.Spawn(hyrjaNgjarjeProces, threadhelper, sche, uint32(FaqeDosjeentry), true)

	var madhësia uint32

	var linkerKartelë []byte = ([]byte)("LINKER")
	madhësia = GetKartelëMadhësia(linkerKartelë)
	linkeraddress := memoriaManazhuesi.Malloc(madhësia)
	linkerdata := GetbytesfromKursori(uintptr(linkeraddress), int(madhësia), int(madhësia))
	LeximiKartelë(linkerKartelë, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(FaqeDosjeentry))

	lidhjemap := Lidhjemap{}
	lidhjemap.Init(memoriaManazhuesi)

	var lib1Kartelë []byte = ([]byte)("LIB1")
	madhësia = GetKartelëMadhësia(lib1Kartelë)

	lib1address := memoriaManazhuesi.Malloc(madhësia)
	lib1data := GetbytesfromKursori(uintptr(lib1address), int(madhësia), int(madhësia))
	LeximiKartelë(lib1Kartelë, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(FaqeDosjeentry))
	memoriaManazhuesi.Elirë(lib1address)

	lidhjemap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Kartelë []byte = ([]byte)("LIB2")
	madhësia = GetKartelëMadhësia(lib2Kartelë)

	lib2address := memoriaManazhuesi.Malloc(madhësia)
	lib2data := GetbytesfromKursori(uintptr(lib2address), int(madhësia), int(madhësia))
	LeximiKartelë(lib2Kartelë, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(FaqeDosjeentry))
	memoriaManazhuesi.Elirë(lib2address)

	lidhjemap.Append_to_list(uintptr(lib2elf.Dynamic))

	libLidhjemap := lidhjemap.Clone()
	lidhjemapaddress := uint32(uintptr(Pointer(libLidhjemap.First)))

	lib1got := Getunsignedinteger32RreshtimifromKursori(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = lidhjemapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32RreshtimifromKursori(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = lidhjemapaddress
	lib2got[2] = 0x4000000

	konsolë.MPrintoxy("lib1: ", 1, 8)
	konsolë.MUnsignedinteger32Printo(lib1elf.Got)
	konsolë.MPrinto(":")
	konsolë.MUnsignedinteger32Printo(lib1elf.Dynamic)

	konsolë.MPrintoxy("lib2: ", 1, 9)
	konsolë.MUnsignedinteger32Printo(lib2elf.Got)
	konsolë.MPrinto(":")
	konsolë.MUnsignedinteger32Printo(lib2elf.Dynamic)

	var përdoruesi1Kartelë []byte = ([]byte)("USER1")
	madhësia = GetKartelëMadhësia(përdoruesi1Kartelë)
	përdoruesi1address := memoriaManazhuesi.Malloc(madhësia)
	përdoruesi1data := GetbytesfromKursori(uintptr(përdoruesi1address), int(madhësia), int(madhësia))
	LeximiKartelë(përdoruesi1Kartelë, përdoruesi1data)

	elf2 := Elf{}

	përdoruesi1entry := elf2.Getentry(përdoruesi1data)
	elf2.Parse(përdoruesi1data[:], uint32(FaqeDosjeentry+0x1000))
	globaloffsetTabela := elf2.Got

	PVlera1Lidhjemap := lidhjemap.Clone()
	PVlera1Lidhjemap.Append_to_list(uintptr(elf2.Dynamic))

	memoriaManazhuesi.Elirë(përdoruesi1address)

	var code1Kursori *uintptr
	var func1val func()

	code1Kursori = (*uintptr)(memoriaManazhuesi.Malloc(4))
	*code1Kursori = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Kursori))

	proc2 := proçeshelper.Spawn(func1val, threadhelper, sche, uint32(FaqeDosjeentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuGjendje.Ecx = përdoruesi1entry
	thr2.CpuGjendje.Edx = globaloffsetTabela
	thr2.CpuGjendje.Esi = uint32(uintptr(Pointer(PVlera1Lidhjemap.First)))

	konsolë.MPrintoxy("user1: ", 1, 10)
	konsolë.MUnsignedinteger32Printo(elf2.Got)

	var përdoruesi2Kartelë []byte = ([]byte)("USER2")
	madhësia = GetKartelëMadhësia(përdoruesi2Kartelë)
	përdoruesi2address := memoriaManazhuesi.Malloc(madhësia)
	përdoruesi2data := GetbytesfromKursori(uintptr(përdoruesi2address), int(madhësia), int(madhësia))
	LeximiKartelë(përdoruesi2Kartelë, përdoruesi2data)

	elf3 := Elf{}

	përdoruesi2entry := elf3.Getentry(përdoruesi2data)
	elf3.Parse(përdoruesi2data[:], uint32(FaqeDosjeentry+0x2000))
	globaloffsetTabela = elf3.Got

	PVlera2Lidhjemap := lidhjemap.Clone()
	PVlera2Lidhjemap.Append_to_list(uintptr(elf3.Dynamic))

	memoriaManazhuesi.Elirë(përdoruesi2address)

	var code2Kursori *uintptr
	var func2val func()

	code2Kursori = (*uintptr)(memoriaManazhuesi.Malloc(4))
	*code2Kursori = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Kursori))

	proc3 := proçeshelper.Spawn(func2val, threadhelper, sche, uint32(FaqeDosjeentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuGjendje.Ecx = përdoruesi2entry
	thr3.CpuGjendje.Edx = globaloffsetTabela
	thr3.CpuGjendje.Esi = uint32(uintptr(Pointer(PVlera2Lidhjemap.First)))

	konsolë.MPrintoxy("user2: ", 1, 11)
	konsolë.MUnsignedinteger32Printo(thr3.CpuGjendje.Esi)

	libLidhjemap.Printo(1, 11)

	var përdoruesi3Kartelë []byte = ([]byte)("USER3")
	madhësia = GetKartelëMadhësia(përdoruesi3Kartelë)
	përdoruesi3address := memoriaManazhuesi.Malloc(madhësia)
	përdoruesi3data := GetbytesfromKursori(uintptr(përdoruesi3address), int(madhësia), int(madhësia))
	LeximiKartelë(përdoruesi3Kartelë, përdoruesi3data)

	elf4 := Elf{}

	përdoruesi3entry := elf4.Getentry(përdoruesi3data)
	elf4.Parse(përdoruesi3data[:], uint32(FaqeDosjeentry+0x3000))
	globaloffsetTabela = elf4.Got

	PVlera3Lidhjemap := lidhjemap.Clone()
	PVlera3Lidhjemap.Append_to_list(uintptr(elf4.Dynamic))

	memoriaManazhuesi.Elirë(përdoruesi3address)

	var code3Kursori *uintptr
	var func3val func()

	code3Kursori = (*uintptr)(memoriaManazhuesi.Malloc(4))
	*code3Kursori = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Kursori))

	proc4 := proçeshelper.Spawn(func3val, threadhelper, sche, uint32(FaqeDosjeentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuGjendje.Ecx = përdoruesi3entry
	thr4.CpuGjendje.Edx = globaloffsetTabela
	thr4.CpuGjendje.Esi = uint32(uintptr(Pointer(PVlera3Lidhjemap.First)))

	proçeshelper.Spawn(TFunksion1, threadhelper, sche, uint32(FaqeDosjeentry+0x4000), true)

	iTastieraNgjarjehandler = &myTastieraNgjarjehandler
	tastieradriver.Initdriver(InterruptManazhuesi, iTastieraNgjarjehandler)

	miudriver.Initdriver(InterruptManazhuesi, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Përzgjidhnidriver(&DriverManazhuesi, InterruptManazhuesi)
	dispozitividescriptor = mypcicontrollerhandler.Getdriver()

	sche.Aktivuar(true)
	InterruptManazhuesi.Aktiv()

	for {
		halt()
	}

}
