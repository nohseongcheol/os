/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konzola"
import . "prerušenie"
import . "multitasking"
import . "tasking/tss"

import . "virtuálnyPamäť"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/klávesnica"
import . "driver/myš"

import . "driver/ata"
import . "súborSystém/msdospartition"
import . "súborSystém/fat"

import . "súborSystém/elf"

import . "systémcall"

import . "pamäťmanager"
import . "pci"

func halt()

var iKlávesnicaUdalosťhandler IKlávesnicaUdalosťhandler

type TMyKlávesnicaUdalosťhandler struct {
}

var myKlávesnicaUdalosťhandler TMyKlávesnicaUdalosťhandler
var klávesnicadriver TKlávesnicadriver
var myšdriver TMyšdriver
var pciRadič TPeripheralcomponentinterconnectRadič

var klávesnicaKonzola TKonzola = TKonzola{}

func (vlastný *TMyKlávesnicaUdalosťhandler) ZapnutéKľúčDole(kľúč byte) {
	foo := [1]byte{' '}
	foo[0] = kľúč

	klávesnicaKonzola.MTlačiťBajtyxy(foo[:], 1000, 1000)
}

func (vlastný *TMyKlávesnicaUdalosťhandler) ZapnutéKľúčHore(kľúč byte)	{}

var iMyšUdalosťhandler IMyšUdalosťhandler

type TMyMyšUdalosťhandler struct {
}

var myšKonzola TKonzola = TKonzola{}
var previousx int16 = 0
var previousy int16 = 0
var xPozícia int16 = 0
var yPozícia int16 = 0

func (vlastný *TMyMyšUdalosťhandler) ZapnutéMyšDole(tlačidlo int8) {
	buffer := []byte("x")
	myšKonzola.MTlačiťxy(buffer, uint16(previousx), uint16(previousy))
}
func (vlastný *TMyMyšUdalosťhandler) ZapnutéMyšHore(tlačidlo int8)	{}
func (vlastný *TMyMyšUdalosťhandler) ZapnutéMyšPresunúť(x int8, y int8) {

	xPozícia += int16(x)
	if xPozícia < 0 {
		xPozícia = 0
	}
	if xPozícia >= 80 {
		xPozícia = 79
	}

	yPozícia -= int16(y)

	if yPozícia < 0 {
		yPozícia = 0
	}
	if yPozícia >= 25 {
		yPozícia = 24
	}

	buffer := []byte(" ")
	myšKonzola.MTlačiťxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	myšKonzola.MTlačiťxy(buffer, uint16(xPozícia), uint16(yPozícia))

	previousx = xPozícia
	previousy = yPozícia
}

var zariadeniedescriptor TPeripheralcomponentinterconnectZariadeniedescriptor
var ipciRadičhandler IpciRadičhandler

type TMypciRadičhandler struct {
}

var konzola TKonzola = TKonzola{}
var drivercount uint16 = 0

func (vlastný TMypciRadičhandler) Zapnutégetdriver(zariadenie TPeripheralcomponentinterconnectZariadeniedescriptor) {
	if zariadenie.VýrobcaIdentifikátor == 0x1022 && zariadenie.ZariadenieIdentifikátor == 0x2000 {
		konzola.MTlačiťxy([]byte("["), 0, 12)
		konzola.MTlačiť(([]byte)("AMD am79c973"))
		konzola.MTlačiť([]byte(":"))
		konzola.MUnsignedinteger16Tlačiť(zariadenie.VýrobcaIdentifikátor)
		konzola.MTlačiť([]byte(":"))
		konzola.MUnsignedinteger16Tlačiť(zariadenie.ZariadenieIdentifikátor)
		konzola.MTlačiť([]byte(":"))
		konzola.MUnsignedinteger16Tlačiť(uint16(zariadenie.Portbase))
		konzola.MTlačiť([]byte(":"))
		konzola.MUnsignedinteger32Tlačiť(zariadenie.Prerušenie)

		konzola.MTlačiť([]byte("]\n"))
		zariadeniedescriptor = zariadenie
		drivercount++
	}
}
func (vlastný TMypciRadičhandler) Getdriver() TPeripheralcomponentinterconnectZariadeniedescriptor {
	return zariadeniedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Tlačiťstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konzola.MTlačiť(str)
}

func GetSúborVeľkosť(názovsúboru []byte) uint32 {
	var ata0s = TPokročiléTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabuľka{}
	partition.Čítaniepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var veľkosť uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru)
	ata0s.Flush()

	return veľkosť
}

func ČítanieSúbor(názovsúboru []byte, data []byte) {
	var ata0s = TPokročiléTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabuľka{}
	partition.Čítaniepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Čítanie(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru, data)

	ata0s.Flush()
}
func Zaťaženieelf() {

	var ata0s = TPokročiléTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabuľka{}
	partition.Čítaniepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var názovsúboru []byte = ([]byte)("TEST")
	var veľkosť uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Čítanie(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru, data)

	elf := Elf{}

	elf.Parse(data[:veľkosť], 0x4f00000)

}

var ulohaKonzola TKonzola = TKonzola{}

func TFunkcia1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func ulohaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func ulohab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func ulohac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func ulohad()

func ulohad0() {
	esi := getesi()
	for {

		SysTlačiťunsignedinteger32(esi)

	}
}

func ulohad1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func vstupUdalosťUloha() {
	for {
		ProcespendingKlávesnicaUdalosti()
		ProcespendingMyšUdalosti()
		halt()
	}
}

func memorytest(y int) {
	pamäťmanager := &TPamäťmanager{}
	allocated := uint32(uintptr(pamäťmanager.Malloc(1024)))
	konzola.MUnsignedinteger32Tlačiťxy(allocated, 10, uint16(y))
	if y == 11 {
		pamäťmanager.Voľné(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pozastaviťloop()
func Znovunačítaťcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sadacr3(cr3 uint32)
func Getcr4() uint32
func Povoliťpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkciaNázov(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNázov = runtime.FuncForPC(address).Name()
	var funcBajty []byte = []byte(funcNázov)

	ulohaKonzola.MTlačiťxy(funcBajty, 1, 5)
	ulohaKonzola.MTlačiť(([]byte)(":"))
	ulohaKonzola.MUnsignedinteger32Tlačiť(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	ulohaKonzola.MTlačiťunsignedinteger32(cr0, 2, 1)
}

var tss *Tsspoložka = &Tsspoložka{}

func KKernelEntry(STRANAAdresárpoložka uintptr, stacktop uintptr, stackbottom uintptr) {

	MSériovéZaznamenávanieinit()
	konzola.MTlačiť("\n=== SVK BOOT ===\n")

	konzola.MTlačiťunsignedinteger32(uint32(STRANAAdresárpoložka), 0, 2)
	konzola.MTlačiťunsignedinteger32(uint32(STRANAAdresárpoložka), 10, 2)
	konzola.MTlačiťunsignedinteger32(uint32(stacktop), 0, 3)
	konzola.MTlačiťunsignedinteger32(uint32(stackbottom), 10, 3)

	pamäťmanager := &TPamäťmanager{}
	pamäťmanager.Init(0, MaxqueueVeľkosť)

	paging := &Paging{}
	paging.Init(STRANAAdresárpoložka, 0x500000, pamäťmanager)
	paging.SharedPamäťregion()

	Sadacr3(uint32(STRANAAdresárpoložka))
	Povoliťpaging()

	shareddescriptorTabuľka := &TShareddescriptorTabuľka{}
	shareddescriptorTabuľka.Init()

	konzola.MTlačiť("esp:")

	esp := getesp()
	konzola.MUnsignedinteger32Tlačiť(uint32(esp))

	tls := gettls()
	konzola.MTlačiť(([]byte)("tls:"))
	konzola.MUnsignedinteger32Tlačiť(tls)

	tss.Nainštalovať(shareddescriptorTabuľka, 7, Segkerneldata, esp)

	VirtOtestovať()

	cr3 := Znovunačítaťcr3()
	konzola.MTlačiť(([]byte)(":cr3:"))
	konzola.MUnsignedinteger32Tlačiť(cr3)

	cr0 := Getcr0()
	konzola.MTlačiť(([]byte)(":cr0:"))
	konzola.MUnsignedinteger32Tlačiť(cr0)

	cr4 := Getcr4()
	konzola.MTlačiť(([]byte)(":cr4:"))
	konzola.MUnsignedinteger32Tlačiť(cr4)

	ulohamanager_2 := &TUlohamanager{}
	ulohamanager_2.Init()

	Prerušeniemanager := &TPrerušeniemanager{}
	Prerušeniemanager.Init(0x20, shareddescriptorTabuľka, ulohamanager_2)

	paging.STRANAfault(Prerušeniemanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(pamäťmanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(pamäťmanager, STRANAAdresárpoložka)

	sche := &Scheduler{}
	sche.Init(Prerušeniemanager, pamäťmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Prerušeniemanager)

	proceshelper.Spawn(ulohaa, threadhelper, sche, uint32(STRANAAdresárpoložka), true)
	proceshelper.Spawn(ulohab, threadhelper, sche, uint32(STRANAAdresárpoložka), true)
	proceshelper.Spawn(ulohac, threadhelper, sche, uint32(STRANAAdresárpoložka), true)
	proceshelper.Spawn(ulohad1, threadhelper, sche, uint32(STRANAAdresárpoložka), true)
	proceshelper.Spawn(vstupUdalosťUloha, threadhelper, sche, uint32(STRANAAdresárpoložka), true)

	var veľkosť uint32

	var linkerSúbor []byte = ([]byte)("LINKER")
	veľkosť = GetSúborVeľkosť(linkerSúbor)
	linkeraddress := pamäťmanager.Malloc(veľkosť)
	linkerdata := GetBajtyzKurzor(uintptr(linkeraddress), int(veľkosť), int(veľkosť))
	ČítanieSúbor(linkerSúbor, linkerdata)

	elf0 := Elf{}
	linkerpoložka := elf0.Getpoložka(linkerdata)
	elf0.Parse(linkerdata[:], uint32(STRANAAdresárpoložka))

	odkazmap := Odkazmap{}
	odkazmap.Init(pamäťmanager)

	var lib1Súbor []byte = ([]byte)("LIB1")
	veľkosť = GetSúborVeľkosť(lib1Súbor)

	lib1address := pamäťmanager.Malloc(veľkosť)
	lib1data := GetBajtyzKurzor(uintptr(lib1address), int(veľkosť), int(veľkosť))
	ČítanieSúbor(lib1Súbor, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(STRANAAdresárpoložka))
	pamäťmanager.Voľné(lib1address)

	odkazmap.Append_to_list(uintptr(lib1elf.Dynamická))

	var lib2Súbor []byte = ([]byte)("LIB2")
	veľkosť = GetSúborVeľkosť(lib2Súbor)

	lib2address := pamäťmanager.Malloc(veľkosť)
	lib2data := GetBajtyzKurzor(uintptr(lib2address), int(veľkosť), int(veľkosť))
	ČítanieSúbor(lib2Súbor, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(STRANAAdresárpoložka))
	pamäťmanager.Voľné(lib2address)

	odkazmap.Append_to_list(uintptr(lib2elf.Dynamická))

	libOdkazmap := odkazmap.Clone()
	odkazmapaddress := uint32(uintptr(Pointer(libOdkazmap.First)))

	lib1got := Getunsignedinteger32PolezKurzor(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = odkazmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32PolezKurzor(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = odkazmapaddress
	lib2got[2] = 0x4000000

	konzola.MTlačiťxy("lib1: ", 1, 8)
	konzola.MUnsignedinteger32Tlačiť(lib1elf.Got)
	konzola.MTlačiť(":")
	konzola.MUnsignedinteger32Tlačiť(lib1elf.Dynamická)

	konzola.MTlačiťxy("lib2: ", 1, 9)
	konzola.MUnsignedinteger32Tlačiť(lib2elf.Got)
	konzola.MTlačiť(":")
	konzola.MUnsignedinteger32Tlačiť(lib2elf.Dynamická)

	var používateľ1Súbor []byte = ([]byte)("USER1")
	veľkosť = GetSúborVeľkosť(používateľ1Súbor)
	používateľ1address := pamäťmanager.Malloc(veľkosť)
	používateľ1data := GetBajtyzKurzor(uintptr(používateľ1address), int(veľkosť), int(veľkosť))
	ČítanieSúbor(používateľ1Súbor, používateľ1data)

	elf2 := Elf{}

	používateľ1položka := elf2.Getpoložka(používateľ1data)
	elf2.Parse(používateľ1data[:], uint32(STRANAAdresárpoložka+0x1000))
	globálnyPosunutieTabuľka := elf2.Got

	PHodnota1Odkazmap := odkazmap.Clone()
	PHodnota1Odkazmap.Append_to_list(uintptr(elf2.Dynamická))

	pamäťmanager.Voľné(používateľ1address)

	var code1Kurzor *uintptr
	var func1val func()

	code1Kurzor = (*uintptr)(pamäťmanager.Malloc(4))
	*code1Kurzor = uintptr(linkerpoložka)
	func1val = *(*func())(Pointer(&code1Kurzor))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(STRANAAdresárpoložka+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProcesorStav.Ecx = používateľ1položka
	thr2.ProcesorStav.Edx = globálnyPosunutieTabuľka
	thr2.ProcesorStav.Esi = uint32(uintptr(Pointer(PHodnota1Odkazmap.First)))

	konzola.MTlačiťxy("user1: ", 1, 10)
	konzola.MUnsignedinteger32Tlačiť(elf2.Got)

	var používateľ2Súbor []byte = ([]byte)("USER2")
	veľkosť = GetSúborVeľkosť(používateľ2Súbor)
	používateľ2address := pamäťmanager.Malloc(veľkosť)
	používateľ2data := GetBajtyzKurzor(uintptr(používateľ2address), int(veľkosť), int(veľkosť))
	ČítanieSúbor(používateľ2Súbor, používateľ2data)

	elf3 := Elf{}

	používateľ2položka := elf3.Getpoložka(používateľ2data)
	elf3.Parse(používateľ2data[:], uint32(STRANAAdresárpoložka+0x2000))
	globálnyPosunutieTabuľka = elf3.Got

	PHodnota2Odkazmap := odkazmap.Clone()
	PHodnota2Odkazmap.Append_to_list(uintptr(elf3.Dynamická))

	pamäťmanager.Voľné(používateľ2address)

	var code2Kurzor *uintptr
	var func2val func()

	code2Kurzor = (*uintptr)(pamäťmanager.Malloc(4))
	*code2Kurzor = uintptr(linkerpoložka)
	func2val = *(*func())(Pointer(&code2Kurzor))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(STRANAAdresárpoložka+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProcesorStav.Ecx = používateľ2položka
	thr3.ProcesorStav.Edx = globálnyPosunutieTabuľka
	thr3.ProcesorStav.Esi = uint32(uintptr(Pointer(PHodnota2Odkazmap.First)))

	konzola.MTlačiťxy("user2: ", 1, 11)
	konzola.MUnsignedinteger32Tlačiť(thr3.ProcesorStav.Esi)

	libOdkazmap.Tlačiť(1, 11)

	var používateľ3Súbor []byte = ([]byte)("USER3")
	veľkosť = GetSúborVeľkosť(používateľ3Súbor)
	používateľ3address := pamäťmanager.Malloc(veľkosť)
	používateľ3data := GetBajtyzKurzor(uintptr(používateľ3address), int(veľkosť), int(veľkosť))
	ČítanieSúbor(používateľ3Súbor, používateľ3data)

	elf4 := Elf{}

	používateľ3položka := elf4.Getpoložka(používateľ3data)
	elf4.Parse(používateľ3data[:], uint32(STRANAAdresárpoložka+0x3000))
	globálnyPosunutieTabuľka = elf4.Got

	PHodnota3Odkazmap := odkazmap.Clone()
	PHodnota3Odkazmap.Append_to_list(uintptr(elf4.Dynamická))

	pamäťmanager.Voľné(používateľ3address)

	var code3Kurzor *uintptr
	var func3val func()

	code3Kurzor = (*uintptr)(pamäťmanager.Malloc(4))
	*code3Kurzor = uintptr(linkerpoložka)
	func3val = *(*func())(Pointer(&code3Kurzor))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(STRANAAdresárpoložka+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProcesorStav.Ecx = používateľ3položka
	thr4.ProcesorStav.Edx = globálnyPosunutieTabuľka
	thr4.ProcesorStav.Esi = uint32(uintptr(Pointer(PHodnota3Odkazmap.First)))

	proceshelper.Spawn(TFunkcia1, threadhelper, sche, uint32(STRANAAdresárpoložka+0x4000), true)

	iKlávesnicaUdalosťhandler = &myKlávesnicaUdalosťhandler
	klávesnicadriver.Initdriver(Prerušeniemanager, iKlávesnicaUdalosťhandler)

	myšdriver.Initdriver(Prerušeniemanager, nil)

	mypciRadičhandler := TMypciRadičhandler{}
	pciRadič.Init(mypciRadičhandler)
	pciRadič.Vybraťdriver(&Drivermanager, Prerušeniemanager)
	zariadeniedescriptor = mypciRadičhandler.Getdriver()

	sche.Zapnuté(true)
	Prerušeniemanager.Aktívny()

	for {
		halt()
	}

}
