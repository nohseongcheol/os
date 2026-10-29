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

import . "virtueelGeheugen"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/toetsenbord"
import . "driver/aanwijsapparaat"

import . "driver/ata"
import . "bestandSysteem/msdospartition"
import . "bestandSysteem/fat"

import . "bestandSysteem/uitvoerbaar_en_koppelbaar_formaat"

import . "systeemcall"

import . "geheugenmanager"
import . "pci"

func halt()

var iToetsenbordGebeurtenishandler IToetsenbordGebeurtenishandler

type TMyToetsenbordGebeurtenishandler struct {
}

var myToetsenbordGebeurtenishandler TMyToetsenbordGebeurtenishandler
var toetsenborddriver TToetsenborddriver
var muisdriver TMuisdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var toetsenbordconsole TConsole = TConsole{}

func (zelf *TMyToetsenbordGebeurtenishandler) AanSleutelOmlaag(sleutel byte) {
	foo := [1]byte{' '}
	foo[0] = sleutel

	toetsenbordconsole.MAfdrukkenbytesxy(foo[:], 1000, 1000)
}

func (zelf *TMyToetsenbordGebeurtenishandler) AanSleutelOmhoog(sleutel byte)	{}

var iMuisGebeurtenishandler IMuisGebeurtenishandler

type TMyMuisGebeurtenishandler struct {
}

var muisconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPositie int16 = 0
var yPositie int16 = 0

func (zelf *TMyMuisGebeurtenishandler) AanMuisOmlaag(knop int8) {
	buffer := []byte("x")
	muisconsole.MAfdrukkenxy(buffer, uint16(previousx), uint16(previousy))
}
func (zelf *TMyMuisGebeurtenishandler) AanMuisOmhoog(knop int8)	{}
func (zelf *TMyMuisGebeurtenishandler) AanMuisVerplaatsen(x int8, y int8) {

	xPositie += int16(x)
	if xPositie < 0 {
		xPositie = 0
	}
	if xPositie >= 80 {
		xPositie = 79
	}

	yPositie -= int16(y)

	if yPositie < 0 {
		yPositie = 0
	}
	if yPositie >= 25 {
		yPositie = 24
	}

	buffer := []byte(" ")
	muisconsole.MAfdrukkenxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	muisconsole.MAfdrukkenxy(buffer, uint16(xPositie), uint16(yPositie))

	previousx = xPositie
	previousy = yPositie
}

var apparaatdescriptor TPeripheralcomponentinterconnectApparaatdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var driverAantal uint16 = 0

func (zelf TMypcicontrollerhandler) Aangetdriver(apparaat TPeripheralcomponentinterconnectApparaatdescriptor) {
	if apparaat.Verkoperid == 0x1022 && apparaat.Apparaatid == 0x2000 {
		console.MAfdrukkenxy([]byte("["), 0, 12)
		console.MAfdrukken(([]byte)("AMD am79c973"))
		console.MAfdrukken([]byte(":"))
		console.MUnsignedinteger16Afdrukken(apparaat.Verkoperid)
		console.MAfdrukken([]byte(":"))
		console.MUnsignedinteger16Afdrukken(apparaat.Apparaatid)
		console.MAfdrukken([]byte(":"))
		console.MUnsignedinteger16Afdrukken(uint16(apparaat.Poortbase))
		console.MAfdrukken([]byte(":"))
		console.MUnsignedinteger32Afdrukken(apparaat.Interrupt)

		console.MAfdrukken([]byte("]\n"))
		apparaatdescriptor = apparaat
		driverAantal++
	}
}
func (zelf TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectApparaatdescriptor {
	return apparaatdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Afdrukkenstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MAfdrukken(str)
}

func GetBestandGrootte(bestandsnaam []byte) uint32 {
	var ata0s = TGeavanceerdTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lezenpartition(&ata0s)

	bios := TBestandssysteemparameters32{}

	var grootte uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam)
	ata0s.Flush()

	return grootte
}

func Bestand_lezen(bestandsnaam []byte, data []byte) {
	var ata0s = TGeavanceerdTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lezenpartition(&ata0s)

	bios := TBestandssysteemparameters32{}
	bios.Lezen(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam, data)

	ata0s.Flush()
}
func Belastingelf() {

	var ata0s = TGeavanceerdTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Lezenpartition(&ata0s)

	bios := TBestandssysteemparameters32{}

	var bestandsnaam []byte = ([]byte)("TEST")
	var grootte uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lezen(&ata0s, partition.Mbr.Primarypartition[0], bestandsnaam, data)

	uitvoerbaar_en_koppelbaar_formaat := Elf{}

	uitvoerbaar_en_koppelbaar_formaat.Parse(data[:grootte], 0x4f00000)

}

var taakconsole TConsole = TConsole{}

func TFunctie1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func taaka() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func taakb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func taakc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func taakd()

func taakd0() {
	esi := getesi()
	for {

		SysAfdrukkenunsignedinteger32(esi)

	}
}

func taakd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func invoerGebeurtenisTaak() {
	for {
		ProcespendingToetsenbordGebeurtenissen()
		ProcespendingMuisGebeurtenissen()
		halt()
	}
}

func memorytest(y int) {
	geheugenmanager := &TGeheugenmanager{}
	allocated := uint32(uintptr(geheugenmanager.Geheugen_toewijzen(1024)))
	console.MUnsignedinteger32Afdrukkenxy(allocated, 10, uint16(y))
	if y == 11 {
		geheugenmanager.Vrij(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzerenloop()
func Herladencr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Instellencr3(cr3 uint32)
func Getcr4() uint32
func Inschakelenpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunctieNaam(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNaam = runtime.FuncForPC(address).Name()
	var funcbytes []byte = []byte(funcNaam)

	taakconsole.MAfdrukkenxy(funcbytes, 1, 5)
	taakconsole.MAfdrukken(([]byte)(":"))
	taakconsole.MUnsignedinteger32Afdrukken(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taakconsole.MAfdrukkenunsignedinteger32(cr0, 2, 1)
}

var tss *TssItem = &TssItem{}

func KKernelEntry(PaginaMapItem uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerienummerLogboekinit()
	console.MAfdrukken("\n=== SUR BOOT ===\n")

	console.MAfdrukkenunsignedinteger32(uint32(PaginaMapItem), 0, 2)
	console.MAfdrukkenunsignedinteger32(uint32(PaginaMapItem), 10, 2)
	console.MAfdrukkenunsignedinteger32(uint32(stacktop), 0, 3)
	console.MAfdrukkenunsignedinteger32(uint32(stackbottom), 10, 3)

	geheugenmanager := &TGeheugenmanager{}
	geheugenmanager.Init(0, MaxqueueGrootte)

	paging := &Paging{}
	paging.Init(PaginaMapItem, 0x500000, geheugenmanager)
	paging.SharedGeheugenregion()

	Instellencr3(uint32(PaginaMapItem))
	Inschakelenpaging()

	shareddescriptorTabel := &TShareddescriptorTabel{}
	shareddescriptorTabel.Init()

	console.MAfdrukken("esp:")

	esp := getesp()
	console.MUnsignedinteger32Afdrukken(uint32(esp))

	tls := gettls()
	console.MAfdrukken(([]byte)("tls:"))
	console.MUnsignedinteger32Afdrukken(tls)

	tss.Installeren(shareddescriptorTabel, 7, Segkerneldata, esp)

	VirtProef()

	cr3 := Herladencr3()
	console.MAfdrukken(([]byte)(":cr3:"))
	console.MUnsignedinteger32Afdrukken(cr3)

	cr0 := Getcr0()
	console.MAfdrukken(([]byte)(":cr0:"))
	console.MUnsignedinteger32Afdrukken(cr0)

	cr4 := Getcr4()
	console.MAfdrukken(([]byte)(":cr4:"))
	console.MUnsignedinteger32Afdrukken(cr4)

	taakmanager_2 := &TTaakmanager{}
	taakmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorTabel, taakmanager_2)

	paging.Paginafault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(geheugenmanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(geheugenmanager, PaginaMapItem)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, geheugenmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	proceshelper.Spawn(taaka, threadhelper, sche, uint32(PaginaMapItem), true)
	proceshelper.Spawn(taakb, threadhelper, sche, uint32(PaginaMapItem), true)
	proceshelper.Spawn(taakc, threadhelper, sche, uint32(PaginaMapItem), true)
	proceshelper.Spawn(taakd1, threadhelper, sche, uint32(PaginaMapItem), true)
	proceshelper.Spawn(invoerGebeurtenisTaak, threadhelper, sche, uint32(PaginaMapItem), true)

	var grootte uint32

	var linkerBestand []byte = ([]byte)("LINKER")
	grootte = GetBestandGrootte(linkerBestand)
	linkeraddress := geheugenmanager.Geheugen_toewijzen(grootte)
	linkerdata := GetbytesvanMuisaanwijzer(uintptr(linkeraddress), int(grootte), int(grootte))
	Bestand_lezen(linkerBestand, linkerdata)

	elf0 := Elf{}
	linkerItem := elf0.GetItem(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PaginaMapItem))

	koppelingmap := Koppelingmap{}
	koppelingmap.Init(geheugenmanager)

	var lib1Bestand []byte = ([]byte)("LIB1")
	grootte = GetBestandGrootte(lib1Bestand)

	lib1address := geheugenmanager.Geheugen_toewijzen(grootte)
	lib1data := GetbytesvanMuisaanwijzer(uintptr(lib1address), int(grootte), int(grootte))
	Bestand_lezen(lib1Bestand, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PaginaMapItem))
	geheugenmanager.Vrij(lib1address)

	koppelingmap.Achteraan_toevoegen(uintptr(lib1elf.Dynamisch))

	var lib2Bestand []byte = ([]byte)("LIB2")
	grootte = GetBestandGrootte(lib2Bestand)

	lib2address := geheugenmanager.Geheugen_toewijzen(grootte)
	lib2data := GetbytesvanMuisaanwijzer(uintptr(lib2address), int(grootte), int(grootte))
	Bestand_lezen(lib2Bestand, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PaginaMapItem))
	geheugenmanager.Vrij(lib2address)

	koppelingmap.Achteraan_toevoegen(uintptr(lib2elf.Dynamisch))

	libKoppelingmap := koppelingmap.Clone()
	koppelingmapaddress := uint32(uintptr(Pointer(libKoppelingmap.First)))

	lib1got := Getunsignedinteger32ReeksvanMuisaanwijzer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = koppelingmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ReeksvanMuisaanwijzer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = koppelingmapaddress
	lib2got[2] = 0x4000000

	console.MAfdrukkenxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Afdrukken(lib1elf.Got)
	console.MAfdrukken(":")
	console.MUnsignedinteger32Afdrukken(lib1elf.Dynamisch)

	console.MAfdrukkenxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Afdrukken(lib2elf.Got)
	console.MAfdrukken(":")
	console.MUnsignedinteger32Afdrukken(lib2elf.Dynamisch)

	var gebruiker1Bestand []byte = ([]byte)("USER1")
	grootte = GetBestandGrootte(gebruiker1Bestand)
	gebruiker1address := geheugenmanager.Geheugen_toewijzen(grootte)
	gebruiker1data := GetbytesvanMuisaanwijzer(uintptr(gebruiker1address), int(grootte), int(grootte))
	Bestand_lezen(gebruiker1Bestand, gebruiker1data)

	elf2 := Elf{}

	gebruiker1Item := elf2.GetItem(gebruiker1data)
	elf2.Parse(gebruiker1data[:], uint32(PaginaMapItem+0x1000))
	algemeenVerschuivingTabel := elf2.Got

	PWaarde1Koppelingmap := koppelingmap.Clone()
	PWaarde1Koppelingmap.Achteraan_toevoegen(uintptr(elf2.Dynamisch))

	geheugenmanager.Vrij(gebruiker1address)

	var code1Muisaanwijzer *uintptr
	var func1val func()

	code1Muisaanwijzer = (*uintptr)(geheugenmanager.Geheugen_toewijzen(4))
	*code1Muisaanwijzer = uintptr(linkerItem)
	func1val = *(*func())(Pointer(&code1Muisaanwijzer))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(PaginaMapItem+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStatus.Ecx = gebruiker1Item
	thr2.CpuStatus.Edx = algemeenVerschuivingTabel
	thr2.CpuStatus.Esi = uint32(uintptr(Pointer(PWaarde1Koppelingmap.First)))

	console.MAfdrukkenxy("user1: ", 1, 10)
	console.MUnsignedinteger32Afdrukken(elf2.Got)

	var gebruiker2Bestand []byte = ([]byte)("USER2")
	grootte = GetBestandGrootte(gebruiker2Bestand)
	gebruiker2address := geheugenmanager.Geheugen_toewijzen(grootte)
	gebruiker2data := GetbytesvanMuisaanwijzer(uintptr(gebruiker2address), int(grootte), int(grootte))
	Bestand_lezen(gebruiker2Bestand, gebruiker2data)

	elf3 := Elf{}

	gebruiker2Item := elf3.GetItem(gebruiker2data)
	elf3.Parse(gebruiker2data[:], uint32(PaginaMapItem+0x2000))
	algemeenVerschuivingTabel = elf3.Got

	PWaarde2Koppelingmap := koppelingmap.Clone()
	PWaarde2Koppelingmap.Achteraan_toevoegen(uintptr(elf3.Dynamisch))

	geheugenmanager.Vrij(gebruiker2address)

	var code2Muisaanwijzer *uintptr
	var func2val func()

	code2Muisaanwijzer = (*uintptr)(geheugenmanager.Geheugen_toewijzen(4))
	*code2Muisaanwijzer = uintptr(linkerItem)
	func2val = *(*func())(Pointer(&code2Muisaanwijzer))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(PaginaMapItem+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStatus.Ecx = gebruiker2Item
	thr3.CpuStatus.Edx = algemeenVerschuivingTabel
	thr3.CpuStatus.Esi = uint32(uintptr(Pointer(PWaarde2Koppelingmap.First)))

	console.MAfdrukkenxy("user2: ", 1, 11)
	console.MUnsignedinteger32Afdrukken(thr3.CpuStatus.Esi)

	libKoppelingmap.Afdrukken(1, 11)

	var gebruiker3Bestand []byte = ([]byte)("USER3")
	grootte = GetBestandGrootte(gebruiker3Bestand)
	gebruiker3address := geheugenmanager.Geheugen_toewijzen(grootte)
	gebruiker3data := GetbytesvanMuisaanwijzer(uintptr(gebruiker3address), int(grootte), int(grootte))
	Bestand_lezen(gebruiker3Bestand, gebruiker3data)

	elf4 := Elf{}

	gebruiker3Item := elf4.GetItem(gebruiker3data)
	elf4.Parse(gebruiker3data[:], uint32(PaginaMapItem+0x3000))
	algemeenVerschuivingTabel = elf4.Got

	PWaarde3Koppelingmap := koppelingmap.Clone()
	PWaarde3Koppelingmap.Achteraan_toevoegen(uintptr(elf4.Dynamisch))

	geheugenmanager.Vrij(gebruiker3address)

	var code3Muisaanwijzer *uintptr
	var func3val func()

	code3Muisaanwijzer = (*uintptr)(geheugenmanager.Geheugen_toewijzen(4))
	*code3Muisaanwijzer = uintptr(linkerItem)
	func3val = *(*func())(Pointer(&code3Muisaanwijzer))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(PaginaMapItem+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStatus.Ecx = gebruiker3Item
	thr4.CpuStatus.Edx = algemeenVerschuivingTabel
	thr4.CpuStatus.Esi = uint32(uintptr(Pointer(PWaarde3Koppelingmap.First)))

	proceshelper.Spawn(TFunctie1, threadhelper, sche, uint32(PaginaMapItem+0x4000), true)

	iToetsenbordGebeurtenishandler = &myToetsenbordGebeurtenishandler
	toetsenborddriver.Initdriver(Interruptmanager, iToetsenbordGebeurtenishandler)

	muisdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selecterendriver(&Drivermanager, Interruptmanager)
	apparaatdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Ingeschakeld(true)
	Interruptmanager.Actief()

	for {
		halt()
	}

}
