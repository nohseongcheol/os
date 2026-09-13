package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsol"
import . "avbrott"
import . "multitasking"
import . "tasking/tss"

import . "virtuellMinne"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/tangentbord"
import . "driver/pekdon"

import . "driver/ata"
import . "arkivsystem/msdospartition"
import . "arkivsystem/fat"

import . "arkivsystem/körbart_och_länkbart_format"

import . "systemcall"

import . "minnemanager"
import . "pci"

func halt()

var iTangentbordHändelsehandler ITangentbordHändelsehandler

type TMyTangentbordHändelsehandler struct {
}

var myTangentbordHändelsehandler TMyTangentbordHändelsehandler
var tangentborddriver TTangentborddriver
var musdriver TMusdriver
var pciStyrenhet TPeripheralcomponentinterconnectStyrenhet

var tangentbordKonsol TKonsol = TKonsol{}

func (själv *TMyTangentbordHändelsehandler) PåNyckelNer(nyckel byte) {
	apa := [1]byte{' '}
	apa[0] = nyckel

	tangentbordKonsol.MSkrivutBytexy(apa[:], 1000, 1000)
}

func (själv *TMyTangentbordHändelsehandler) PåNyckelUpp(nyckel byte)	{}

var iMusHändelsehandler IMusHändelsehandler

type TMyMusHändelsehandler struct {
}

var musKonsol TKonsol = TKonsol{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (själv *TMyMusHändelsehandler) PåMusNer(knapp int8) {
	buffer := []byte("x")
	musKonsol.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))
}
func (själv *TMyMusHändelsehandler) PåMusUpp(knapp int8)	{}
func (själv *TMyMusHändelsehandler) PåMusFlytta(x int8, y int8) {

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
	musKonsol.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	musKonsol.MSkrivutxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var enhetdescriptor TPeripheralcomponentinterconnectEnhetdescriptor
var ipciStyrenhethandler IpciStyrenhethandler

type TMypciStyrenhethandler struct {
}

var konsol TKonsol = TKonsol{}
var driverAntal uint16 = 0

func (själv TMypciStyrenhethandler) Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor) {
	if enhet.Tillverkareid == 0x1022 && enhet.Enhetid == 0x2000 {
		konsol.MSkrivutxy([]byte("["), 0, 12)
		konsol.MSkrivut(([]byte)("AMD am79c973"))
		konsol.MSkrivut([]byte(":"))
		konsol.MUnsignedinteger16Skrivut(enhet.Tillverkareid)
		konsol.MSkrivut([]byte(":"))
		konsol.MUnsignedinteger16Skrivut(enhet.Enhetid)
		konsol.MSkrivut([]byte(":"))
		konsol.MUnsignedinteger16Skrivut(uint16(enhet.Portbase))
		konsol.MSkrivut([]byte(":"))
		konsol.MUnsignedinteger32Skrivut(enhet.Avbrott)

		konsol.MSkrivut([]byte("]\n"))
		enhetdescriptor = enhet
		driverAntal++
	}
}
func (själv TMypciStyrenhethandler) Getdriver() TPeripheralcomponentinterconnectEnhetdescriptor {
	return enhetdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Skrivutstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsol.MSkrivut(str)
}

func GetArkivStorlek(filnamn []byte) uint32 {
	var ata0s = TAvanceratTeknikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Läspartition(&ata0s)

	bios := TFilsystemsparametrar32{}

	var storlek uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnamn)
	ata0s.Flush()

	return storlek
}

func Läs_fil(filnamn []byte, data []byte) {
	var ata0s = TAvanceratTeknikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Läspartition(&ata0s)

	bios := TFilsystemsparametrar32{}
	bios.Läs(&ata0s, partition.Mbr.Primarypartition[0], filnamn, data)

	ata0s.Flush()
}
func Belastningelf() {

	var ata0s = TAvanceratTeknikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Läspartition(&ata0s)

	bios := TFilsystemsparametrar32{}

	var filnamn []byte = ([]byte)("TEST")
	var storlek uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnamn)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Läs(&ata0s, partition.Mbr.Primarypartition[0], filnamn, data)

	körbart_och_länkbart_format := Elf{}

	körbart_och_länkbart_format.Parse(data[:storlek], 0x4f00000)

}

var aktivitetKonsol TKonsol = TKonsol{}

func TFunktion1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func aktiviteta() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func aktivitetb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func aktivitetc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func aktivitetd()

func aktivitetd0() {
	esi := getesi()
	for {

		SysSkrivutunsignedinteger32(esi)

	}
}

func aktivitetd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func inmatningHändelseAktivitet() {
	for {
		ProcesspendingTangentbordHändelser()
		ProcesspendingMusHändelser()
		halt()
	}
}

func memorytest(y int) {
	minnemanager := &TMinnemanager{}
	allocated := uint32(uintptr(minnemanager.Tilldela_minne(1024)))
	konsol.MUnsignedinteger32Skrivutxy(allocated, 10, uint16(y))
	if y == 11 {
		minnemanager.Ledigt(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func PausaSlinga()
func Uppdateracr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Mängdcr3(cr3 uint32)
func Getcr4() uint32
func Aktiverapaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunktionNamn(i interface{}) {
	var adress = reflect.ValueOf(i).Pointer()
	var funcNamn = runtime.FuncForPC(adress).Name()
	var funcByte []byte = []byte(funcNamn)

	aktivitetKonsol.MSkrivutxy(funcByte, 1, 5)
	aktivitetKonsol.MSkrivut(([]byte)(":"))
	aktivitetKonsol.MUnsignedinteger32Skrivut(uint32(uintptr(adress)))
}

func printreg() {
	cr0 := Getcr0()
	aktivitetKonsol.MSkrivutunsignedinteger32(cr0, 2, 1)
}

var tss *Tsspost = &Tsspost{}

func KKernelEntry(SidaKatalogpost uintptr, stacktop uintptr, stackbottom uintptr) {

	MSeriellLogginit()
	konsol.MSkrivut("\n=== ALA BOOT ===\n")

	konsol.MSkrivutunsignedinteger32(uint32(SidaKatalogpost), 0, 2)
	konsol.MSkrivutunsignedinteger32(uint32(SidaKatalogpost), 10, 2)
	konsol.MSkrivutunsignedinteger32(uint32(stacktop), 0, 3)
	konsol.MSkrivutunsignedinteger32(uint32(stackbottom), 10, 3)

	minnemanager := &TMinnemanager{}
	minnemanager.Init(0, MaximalqueueStorlek)

	paging := &Paging{}
	paging.Init(SidaKatalogpost, 0x500000, minnemanager)
	paging.SharedMinneregion()

	Mängdcr3(uint32(SidaKatalogpost))
	Aktiverapaging()

	shareddescriptorTabell := &TShareddescriptorTabell{}
	shareddescriptorTabell.Init()

	konsol.MSkrivut("esp:")

	esp := getesp()
	konsol.MUnsignedinteger32Skrivut(uint32(esp))

	tls := gettls()
	konsol.MSkrivut(([]byte)("tls:"))
	konsol.MUnsignedinteger32Skrivut(tls)

	tss.Installera(shareddescriptorTabell, 7, Segkerneldata, esp)

	VirtTesta()

	cr3 := Uppdateracr3()
	konsol.MSkrivut(([]byte)(":cr3:"))
	konsol.MUnsignedinteger32Skrivut(cr3)

	cr0 := Getcr0()
	konsol.MSkrivut(([]byte)(":cr0:"))
	konsol.MUnsignedinteger32Skrivut(cr0)

	cr4 := Getcr4()
	konsol.MSkrivut(([]byte)(":cr4:"))
	konsol.MUnsignedinteger32Skrivut(cr4)

	aktivitetmanager_2 := &TAktivitetmanager{}
	aktivitetmanager_2.Init()

	Avbrottmanager := &TAvbrottmanager{}
	Avbrottmanager.Init(0x20, shareddescriptorTabell, aktivitetmanager_2)

	paging.Sidafault(Avbrottmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(minnemanager)

	processhelper := Processhelper{}
	processhelper.Init(minnemanager, SidaKatalogpost)

	sche := &Scheduler{}
	sche.Init(Avbrottmanager, minnemanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Avbrottmanager)

	processhelper.Spawn(aktiviteta, threadhelper, sche, uint32(SidaKatalogpost), true)
	processhelper.Spawn(aktivitetb, threadhelper, sche, uint32(SidaKatalogpost), true)
	processhelper.Spawn(aktivitetc, threadhelper, sche, uint32(SidaKatalogpost), true)
	processhelper.Spawn(aktivitetd1, threadhelper, sche, uint32(SidaKatalogpost), true)
	processhelper.Spawn(inmatningHändelseAktivitet, threadhelper, sche, uint32(SidaKatalogpost), true)

	var storlek uint32

	var linkerArkiv []byte = ([]byte)("LINKER")
	storlek = GetArkivStorlek(linkerArkiv)
	linkerAdress := minnemanager.Tilldela_minne(storlek)
	linkerdata := GetBytefromMuspekare(uintptr(linkerAdress), int(storlek), int(storlek))
	Läs_fil(linkerArkiv, linkerdata)

	elf0 := Elf{}
	linkerpost := elf0.Getpost(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SidaKatalogpost))

	länkmap := Länkmap{}
	länkmap.Init(minnemanager)

	var lib1Arkiv []byte = ([]byte)("LIB1")
	storlek = GetArkivStorlek(lib1Arkiv)

	lib1Adress := minnemanager.Tilldela_minne(storlek)
	lib1data := GetBytefromMuspekare(uintptr(lib1Adress), int(storlek), int(storlek))
	Läs_fil(lib1Arkiv, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SidaKatalogpost))
	minnemanager.Ledigt(lib1Adress)

	länkmap.Lägg_till_sist_i_listan(uintptr(lib1elf.Dynamisk))

	var lib2Arkiv []byte = ([]byte)("LIB2")
	storlek = GetArkivStorlek(lib2Arkiv)

	lib2Adress := minnemanager.Tilldela_minne(storlek)
	lib2data := GetBytefromMuspekare(uintptr(lib2Adress), int(storlek), int(storlek))
	Läs_fil(lib2Arkiv, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SidaKatalogpost))
	minnemanager.Ledigt(lib2Adress)

	länkmap.Lägg_till_sist_i_listan(uintptr(lib2elf.Dynamisk))

	libLänkmap := länkmap.Clone()
	länkmapAdress := uint32(uintptr(Pointer(libLänkmap.First)))

	lib1got := Getunsignedinteger32VektorfromMuspekare(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = länkmapAdress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32VektorfromMuspekare(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = länkmapAdress
	lib2got[2] = 0x4000000

	konsol.MSkrivutxy("lib1: ", 1, 8)
	konsol.MUnsignedinteger32Skrivut(lib1elf.Got)
	konsol.MSkrivut(":")
	konsol.MUnsignedinteger32Skrivut(lib1elf.Dynamisk)

	konsol.MSkrivutxy("lib2: ", 1, 9)
	konsol.MUnsignedinteger32Skrivut(lib2elf.Got)
	konsol.MSkrivut(":")
	konsol.MUnsignedinteger32Skrivut(lib2elf.Dynamisk)

	var användare1Arkiv []byte = ([]byte)("USER1")
	storlek = GetArkivStorlek(användare1Arkiv)
	användare1Adress := minnemanager.Tilldela_minne(storlek)
	användare1data := GetBytefromMuspekare(uintptr(användare1Adress), int(storlek), int(storlek))
	Läs_fil(användare1Arkiv, användare1data)

	elf2 := Elf{}

	användare1post := elf2.Getpost(användare1data)
	elf2.Parse(användare1data[:], uint32(SidaKatalogpost+0x1000))
	globalFörskjutningTabell := elf2.Got

	PVärde1Länkmap := länkmap.Clone()
	PVärde1Länkmap.Lägg_till_sist_i_listan(uintptr(elf2.Dynamisk))

	minnemanager.Ledigt(användare1Adress)

	var code1Muspekare *uintptr
	var func1val func()

	code1Muspekare = (*uintptr)(minnemanager.Tilldela_minne(4))
	*code1Muspekare = uintptr(linkerpost)
	func1val = *(*func())(Pointer(&code1Muspekare))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(SidaKatalogpost+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProcessorTillstånd.Ecx = användare1post
	thr2.ProcessorTillstånd.Edx = globalFörskjutningTabell
	thr2.ProcessorTillstånd.Esi = uint32(uintptr(Pointer(PVärde1Länkmap.First)))

	konsol.MSkrivutxy("user1: ", 1, 10)
	konsol.MUnsignedinteger32Skrivut(elf2.Got)

	var användare2Arkiv []byte = ([]byte)("USER2")
	storlek = GetArkivStorlek(användare2Arkiv)
	användare2Adress := minnemanager.Tilldela_minne(storlek)
	användare2data := GetBytefromMuspekare(uintptr(användare2Adress), int(storlek), int(storlek))
	Läs_fil(användare2Arkiv, användare2data)

	elf3 := Elf{}

	användare2post := elf3.Getpost(användare2data)
	elf3.Parse(användare2data[:], uint32(SidaKatalogpost+0x2000))
	globalFörskjutningTabell = elf3.Got

	PVärde2Länkmap := länkmap.Clone()
	PVärde2Länkmap.Lägg_till_sist_i_listan(uintptr(elf3.Dynamisk))

	minnemanager.Ledigt(användare2Adress)

	var code2Muspekare *uintptr
	var func2val func()

	code2Muspekare = (*uintptr)(minnemanager.Tilldela_minne(4))
	*code2Muspekare = uintptr(linkerpost)
	func2val = *(*func())(Pointer(&code2Muspekare))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(SidaKatalogpost+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProcessorTillstånd.Ecx = användare2post
	thr3.ProcessorTillstånd.Edx = globalFörskjutningTabell
	thr3.ProcessorTillstånd.Esi = uint32(uintptr(Pointer(PVärde2Länkmap.First)))

	konsol.MSkrivutxy("user2: ", 1, 11)
	konsol.MUnsignedinteger32Skrivut(thr3.ProcessorTillstånd.Esi)

	libLänkmap.Skrivut(1, 11)

	var användare3Arkiv []byte = ([]byte)("USER3")
	storlek = GetArkivStorlek(användare3Arkiv)
	användare3Adress := minnemanager.Tilldela_minne(storlek)
	användare3data := GetBytefromMuspekare(uintptr(användare3Adress), int(storlek), int(storlek))
	Läs_fil(användare3Arkiv, användare3data)

	elf4 := Elf{}

	användare3post := elf4.Getpost(användare3data)
	elf4.Parse(användare3data[:], uint32(SidaKatalogpost+0x3000))
	globalFörskjutningTabell = elf4.Got

	PVärde3Länkmap := länkmap.Clone()
	PVärde3Länkmap.Lägg_till_sist_i_listan(uintptr(elf4.Dynamisk))

	minnemanager.Ledigt(användare3Adress)

	var code3Muspekare *uintptr
	var func3val func()

	code3Muspekare = (*uintptr)(minnemanager.Tilldela_minne(4))
	*code3Muspekare = uintptr(linkerpost)
	func3val = *(*func())(Pointer(&code3Muspekare))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(SidaKatalogpost+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProcessorTillstånd.Ecx = användare3post
	thr4.ProcessorTillstånd.Edx = globalFörskjutningTabell
	thr4.ProcessorTillstånd.Esi = uint32(uintptr(Pointer(PVärde3Länkmap.First)))

	processhelper.Spawn(TFunktion1, threadhelper, sche, uint32(SidaKatalogpost+0x4000), true)

	iTangentbordHändelsehandler = &myTangentbordHändelsehandler
	tangentborddriver.Initdriver(Avbrottmanager, iTangentbordHändelsehandler)

	musdriver.Initdriver(Avbrottmanager, nil)

	mypciStyrenhethandler := TMypciStyrenhethandler{}
	pciStyrenhet.Init(mypciStyrenhethandler)
	pciStyrenhet.Väljdriver(&Drivermanager, Avbrottmanager)
	enhetdescriptor = mypciStyrenhethandler.Getdriver()

	sche.Aktiverad(true)
	Avbrottmanager.Aktiv()

	for {
		halt()
	}

}
