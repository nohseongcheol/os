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
import . "prekinitev"
import . "multitasking"
import . "tasking/tss"

import . "navideznoPomnilnik"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/opravilo"
import . "driver/driver"

import . "driver/tipkovnica"
import . "driver/miška"

import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "datotekaSistem/fat"

import . "datotekaSistem/elf"

import . "sistemcall"

import . "pomnilnikmanager"
import . "pci"

func halt()

var iTipkovnicaeventhandler ITipkovnicaeventhandler

type TMyTipkovnicaeventhandler struct {
}

var myTipkovnicaeventhandler TMyTipkovnicaeventhandler
var tipkovnicadriver TTipkovnicadriver
var miškadriver TMiškadriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tipkovnicaconsole TConsole = TConsole{}

func (sam *TMyTipkovnicaeventhandler) VključenoKljučDol(ključ byte) {
	foo := [1]byte{' '}
	foo[0] = ključ

	tipkovnicaconsole.MNatisniBajtovxy(foo[:], 1000, 1000)
}

func (sam *TMyTipkovnicaeventhandler) VključenoKljučGor(ključ byte)	{}

var iMiškaeventhandler IMiškaeventhandler

type TMyMiškaeventhandler struct {
}

var miškaconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (sam *TMyMiškaeventhandler) VključenoMiškaDol(gumb int8) {
	buffer := []byte("x")
	miškaconsole.MNatisnixy(buffer, uint16(previousx), uint16(previousy))
}
func (sam *TMyMiškaeventhandler) VključenoMiškaGor(gumb int8)	{}
func (sam *TMyMiškaeventhandler) VključenoMiškaPremakni(x int8, y int8) {

	xPoložaj += int16(x)
	if xPoložaj < 0 {
		xPoložaj = 0
	}
	if xPoložaj >= 80 {
		xPoložaj = 79
	}

	yPoložaj -= int16(y)

	if yPoložaj < 0 {
		yPoložaj = 0
	}
	if yPoložaj >= 25 {
		yPoložaj = 24
	}

	buffer := []byte(" ")
	miškaconsole.MNatisnixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	miškaconsole.MNatisnixy(buffer, uint16(xPoložaj), uint16(yPoložaj))

	previousx = xPoložaj
	previousy = yPoložaj
}

var napravadescriptor TPeripheralcomponentinterconnectNapravadescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (sam TMypcicontrollerhandler) Vključenogetdriver(naprava TPeripheralcomponentinterconnectNapravadescriptor) {
	if naprava.Prodajalecid == 0x1022 && naprava.Napravaid == 0x2000 {
		console.MNatisnixy([]byte("["), 0, 12)
		console.MNatisni(([]byte)("AMD am79c973"))
		console.MNatisni([]byte(":"))
		console.MUnsignedinteger16Natisni(naprava.Prodajalecid)
		console.MNatisni([]byte(":"))
		console.MUnsignedinteger16Natisni(naprava.Napravaid)
		console.MNatisni([]byte(":"))
		console.MUnsignedinteger16Natisni(uint16(naprava.Vratabase))
		console.MNatisni([]byte(":"))
		console.MUnsignedinteger32Natisni(naprava.Prekinitev)

		console.MNatisni([]byte("]\n"))
		napravadescriptor = naprava
		drivercount++
	}
}
func (sam TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectNapravadescriptor {
	return napravadescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Natisnistr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MNatisni(str)
}

func GetDatotekaVelikost(imedatoteke []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionPreglednica{}
	partition.Branjepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var velikost uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	ata0s.Flush()

	return velikost
}

func BranjeDatoteka(imedatoteke []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionPreglednica{}
	partition.Branjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Branje(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	ata0s.Flush()
}
func Obremenjenostelf() {

	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionPreglednica{}
	partition.Branjepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var imedatoteke []byte = ([]byte)("TEST")
	var velikost uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Branje(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	elf := Elf{}

	elf.Parse(data[:velikost], 0x4f00000)

}

var nalogaconsole TConsole = TConsole{}

func TFunkcija1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func nalogaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func nalogab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func nalogac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func nalogad()

func nalogad0() {
	esi := getesi()
	for {

		SysNatisniunsignedinteger32(esi)

	}
}

func nalogad1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func vhodeventNaloga() {
	for {
		OpravilopendingTipkovnicaDogodki()
		OpravilopendingMiškaDogodki()
		halt()
	}
}

func memorytest(y int) {
	pomnilnikmanager := &TPomnilnikmanager{}
	allocated := uint32(uintptr(pomnilnikmanager.Malloc(1024)))
	console.MUnsignedinteger32Natisnixy(allocated, 10, uint16(y))
	if y == 11 {
		pomnilnikmanager.Prosto(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Premorloop()
func Ponovnonaložicr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Množicacr3(cr3 uint32)
func Getcr4() uint32
func Omogočipaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcijaIme(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcIme = runtime.FuncForPC(address).Name()
	var funcBajtov []byte = []byte(funcIme)

	nalogaconsole.MNatisnixy(funcBajtov, 1, 5)
	nalogaconsole.MNatisni(([]byte)(":"))
	nalogaconsole.MUnsignedinteger32Natisni(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	nalogaconsole.MNatisniunsignedinteger32(cr0, 2, 1)
}

var tss *Tssvnos = &Tssvnos{}

func KKernelEntry(StranMapavnos uintptr, stacktop uintptr, stackbottom uintptr) {

	MZaporednaštevilkaloginit()
	console.MNatisni("\n=== SVN BOOT ===\n")

	console.MNatisniunsignedinteger32(uint32(StranMapavnos), 0, 2)
	console.MNatisniunsignedinteger32(uint32(StranMapavnos), 10, 2)
	console.MNatisniunsignedinteger32(uint32(stacktop), 0, 3)
	console.MNatisniunsignedinteger32(uint32(stackbottom), 10, 3)

	pomnilnikmanager := &TPomnilnikmanager{}
	pomnilnikmanager.Init(0, MaxqueueVelikost)

	paging := &Paging{}
	paging.Init(StranMapavnos, 0x500000, pomnilnikmanager)
	paging.SharedPomnilnikregion()

	Množicacr3(uint32(StranMapavnos))
	Omogočipaging()

	shareddescriptorPreglednica := &TShareddescriptorPreglednica{}
	shareddescriptorPreglednica.Init()

	console.MNatisni("esp:")

	esp := getesp()
	console.MUnsignedinteger32Natisni(uint32(esp))

	tls := gettls()
	console.MNatisni(([]byte)("tls:"))
	console.MUnsignedinteger32Natisni(tls)

	tss.Namesti(shareddescriptorPreglednica, 7, Segkerneldata, esp)

	VirtPreizkus()

	cr3 := Ponovnonaložicr3()
	console.MNatisni(([]byte)(":cr3:"))
	console.MUnsignedinteger32Natisni(cr3)

	cr0 := Getcr0()
	console.MNatisni(([]byte)(":cr0:"))
	console.MUnsignedinteger32Natisni(cr0)

	cr4 := Getcr4()
	console.MNatisni(([]byte)(":cr4:"))
	console.MUnsignedinteger32Natisni(cr4)

	nalogamanager_2 := &TNalogamanager{}
	nalogamanager_2.Init()

	Prekinitevmanager := &TPrekinitevmanager{}
	Prekinitevmanager.Init(0x20, shareddescriptorPreglednica, nalogamanager_2)

	paging.Stranfault(Prekinitevmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(pomnilnikmanager)

	opravilohelper := Opravilohelper{}
	opravilohelper.Init(pomnilnikmanager, StranMapavnos)

	sche := &Scheduler{}
	sche.Init(Prekinitevmanager, pomnilnikmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Prekinitevmanager)

	opravilohelper.Spawn(nalogaa, threadhelper, sche, uint32(StranMapavnos), true)
	opravilohelper.Spawn(nalogab, threadhelper, sche, uint32(StranMapavnos), true)
	opravilohelper.Spawn(nalogac, threadhelper, sche, uint32(StranMapavnos), true)
	opravilohelper.Spawn(nalogad1, threadhelper, sche, uint32(StranMapavnos), true)
	opravilohelper.Spawn(vhodeventNaloga, threadhelper, sche, uint32(StranMapavnos), true)

	var velikost uint32

	var linkerDatoteka []byte = ([]byte)("LINKER")
	velikost = GetDatotekaVelikost(linkerDatoteka)
	linkeraddress := pomnilnikmanager.Malloc(velikost)
	linkerdata := GetBajtovfromKazalnik(uintptr(linkeraddress), int(velikost), int(velikost))
	BranjeDatoteka(linkerDatoteka, linkerdata)

	elf0 := Elf{}
	linkervnos := elf0.Getvnos(linkerdata)
	elf0.Parse(linkerdata[:], uint32(StranMapavnos))

	povezavamap := Povezavamap{}
	povezavamap.Init(pomnilnikmanager)

	var lib1Datoteka []byte = ([]byte)("LIB1")
	velikost = GetDatotekaVelikost(lib1Datoteka)

	lib1address := pomnilnikmanager.Malloc(velikost)
	lib1data := GetBajtovfromKazalnik(uintptr(lib1address), int(velikost), int(velikost))
	BranjeDatoteka(lib1Datoteka, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(StranMapavnos))
	pomnilnikmanager.Prosto(lib1address)

	povezavamap.Append_to_list(uintptr(lib1elf.Dinamično))

	var lib2Datoteka []byte = ([]byte)("LIB2")
	velikost = GetDatotekaVelikost(lib2Datoteka)

	lib2address := pomnilnikmanager.Malloc(velikost)
	lib2data := GetBajtovfromKazalnik(uintptr(lib2address), int(velikost), int(velikost))
	BranjeDatoteka(lib2Datoteka, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(StranMapavnos))
	pomnilnikmanager.Prosto(lib2address)

	povezavamap.Append_to_list(uintptr(lib2elf.Dinamično))

	libPovezavamap := povezavamap.Clone()
	povezavamapaddress := uint32(uintptr(Pointer(libPovezavamap.Prvi)))

	lib1got := Getunsignedinteger32PoljefromKazalnik(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = povezavamapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32PoljefromKazalnik(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = povezavamapaddress
	lib2got[2] = 0x4000000

	console.MNatisnixy("lib1: ", 1, 8)
	console.MUnsignedinteger32Natisni(lib1elf.Got)
	console.MNatisni(":")
	console.MUnsignedinteger32Natisni(lib1elf.Dinamično)

	console.MNatisnixy("lib2: ", 1, 9)
	console.MUnsignedinteger32Natisni(lib2elf.Got)
	console.MNatisni(":")
	console.MUnsignedinteger32Natisni(lib2elf.Dinamično)

	var uporabnik1Datoteka []byte = ([]byte)("USER1")
	velikost = GetDatotekaVelikost(uporabnik1Datoteka)
	uporabnik1address := pomnilnikmanager.Malloc(velikost)
	uporabnik1data := GetBajtovfromKazalnik(uintptr(uporabnik1address), int(velikost), int(velikost))
	BranjeDatoteka(uporabnik1Datoteka, uporabnik1data)

	elf2 := Elf{}

	uporabnik1vnos := elf2.Getvnos(uporabnik1data)
	elf2.Parse(uporabnik1data[:], uint32(StranMapavnos+0x1000))
	splošnooffsetPreglednica := elf2.Got

	PVrednost1Povezavamap := povezavamap.Clone()
	PVrednost1Povezavamap.Append_to_list(uintptr(elf2.Dinamično))

	pomnilnikmanager.Prosto(uporabnik1address)

	var code1Kazalnik *uintptr
	var func1val func()

	code1Kazalnik = (*uintptr)(pomnilnikmanager.Malloc(4))
	*code1Kazalnik = uintptr(linkervnos)
	func1val = *(*func())(Pointer(&code1Kazalnik))

	proc2 := opravilohelper.Spawn(func1val, threadhelper, sche, uint32(StranMapavnos+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CPEStanje.Ecx = uporabnik1vnos
	thr2.CPEStanje.Edx = splošnooffsetPreglednica
	thr2.CPEStanje.Esi = uint32(uintptr(Pointer(PVrednost1Povezavamap.Prvi)))

	console.MNatisnixy("user1: ", 1, 10)
	console.MUnsignedinteger32Natisni(elf2.Got)

	var uporabnik2Datoteka []byte = ([]byte)("USER2")
	velikost = GetDatotekaVelikost(uporabnik2Datoteka)
	uporabnik2address := pomnilnikmanager.Malloc(velikost)
	uporabnik2data := GetBajtovfromKazalnik(uintptr(uporabnik2address), int(velikost), int(velikost))
	BranjeDatoteka(uporabnik2Datoteka, uporabnik2data)

	elf3 := Elf{}

	uporabnik2vnos := elf3.Getvnos(uporabnik2data)
	elf3.Parse(uporabnik2data[:], uint32(StranMapavnos+0x2000))
	splošnooffsetPreglednica = elf3.Got

	PVrednost2Povezavamap := povezavamap.Clone()
	PVrednost2Povezavamap.Append_to_list(uintptr(elf3.Dinamično))

	pomnilnikmanager.Prosto(uporabnik2address)

	var code2Kazalnik *uintptr
	var func2val func()

	code2Kazalnik = (*uintptr)(pomnilnikmanager.Malloc(4))
	*code2Kazalnik = uintptr(linkervnos)
	func2val = *(*func())(Pointer(&code2Kazalnik))

	proc3 := opravilohelper.Spawn(func2val, threadhelper, sche, uint32(StranMapavnos+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CPEStanje.Ecx = uporabnik2vnos
	thr3.CPEStanje.Edx = splošnooffsetPreglednica
	thr3.CPEStanje.Esi = uint32(uintptr(Pointer(PVrednost2Povezavamap.Prvi)))

	console.MNatisnixy("user2: ", 1, 11)
	console.MUnsignedinteger32Natisni(thr3.CPEStanje.Esi)

	libPovezavamap.Natisni(1, 11)

	var uporabnik3Datoteka []byte = ([]byte)("USER3")
	velikost = GetDatotekaVelikost(uporabnik3Datoteka)
	uporabnik3address := pomnilnikmanager.Malloc(velikost)
	uporabnik3data := GetBajtovfromKazalnik(uintptr(uporabnik3address), int(velikost), int(velikost))
	BranjeDatoteka(uporabnik3Datoteka, uporabnik3data)

	elf4 := Elf{}

	uporabnik3vnos := elf4.Getvnos(uporabnik3data)
	elf4.Parse(uporabnik3data[:], uint32(StranMapavnos+0x3000))
	splošnooffsetPreglednica = elf4.Got

	PVrednost3Povezavamap := povezavamap.Clone()
	PVrednost3Povezavamap.Append_to_list(uintptr(elf4.Dinamično))

	pomnilnikmanager.Prosto(uporabnik3address)

	var code3Kazalnik *uintptr
	var func3val func()

	code3Kazalnik = (*uintptr)(pomnilnikmanager.Malloc(4))
	*code3Kazalnik = uintptr(linkervnos)
	func3val = *(*func())(Pointer(&code3Kazalnik))

	proc4 := opravilohelper.Spawn(func3val, threadhelper, sche, uint32(StranMapavnos+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CPEStanje.Ecx = uporabnik3vnos
	thr4.CPEStanje.Edx = splošnooffsetPreglednica
	thr4.CPEStanje.Esi = uint32(uintptr(Pointer(PVrednost3Povezavamap.Prvi)))

	opravilohelper.Spawn(TFunkcija1, threadhelper, sche, uint32(StranMapavnos+0x4000), true)

	iTipkovnicaeventhandler = &myTipkovnicaeventhandler
	tipkovnicadriver.Initdriver(Prekinitevmanager, iTipkovnicaeventhandler)

	miškadriver.Initdriver(Prekinitevmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Prekinitevmanager)
	napravadescriptor = mypcicontrollerhandler.Getdriver()

	sche.Omogočeno(true)
	Prekinitevmanager.Dejaven()

	for {
		halt()
	}

}
