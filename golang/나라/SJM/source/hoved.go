package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "avbrudd"
import . "multitasking"
import . "tasking/tss"

import . "virtuellMinne"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/prosess"
import . "driver/driver"

import . "driver/tastatur"
import . "driver/mus"

import . "driver/ata"
import . "filsystem/msdospartition"
import . "filsystem/fat"

import . "filsystem/elf"

import . "systemcall"

import . "minnemanager"
import . "pci"

func halt()

var iTastaturHendelsehandler ITastaturHendelsehandler

type TMyTastaturHendelsehandler struct {
}

var myTastaturHendelsehandler TMyTastaturHendelsehandler
var tastaturdriver TTastaturdriver
var musdriver TMusdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastaturconsole TConsole = TConsole{}

func (selv *TMyTastaturHendelsehandler) PåNøkkelNed(nøkkel byte) {
	foo := [1]byte{' '}
	foo[0] = nøkkel

	tastaturconsole.MSkrivutBytexy(foo[:], 1000, 1000)
}

func (selv *TMyTastaturHendelsehandler) PåNøkkelOpp(nøkkel byte)	{}

var iMusHendelsehandler IMusHendelsehandler

type TMyMusHendelsehandler struct {
}

var musconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosisjon int16 = 0
var yPosisjon int16 = 0

func (selv *TMyMusHendelsehandler) PåMusNed(knapp int8) {
	buffer := []byte("x")
	musconsole.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))
}
func (selv *TMyMusHendelsehandler) PåMusOpp(knapp int8)	{}
func (selv *TMyMusHendelsehandler) PåMusFlytt(x int8, y int8) {

	xPosisjon += int16(x)
	if xPosisjon < 0 {
		xPosisjon = 0
	}
	if xPosisjon >= 80 {
		xPosisjon = 79
	}

	yPosisjon -= int16(y)

	if yPosisjon < 0 {
		yPosisjon = 0
	}
	if yPosisjon >= 25 {
		yPosisjon = 24
	}

	buffer := []byte(" ")
	musconsole.MSkrivutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	musconsole.MSkrivutxy(buffer, uint16(xPosisjon), uint16(yPosisjon))

	previousx = xPosisjon
	previousy = yPosisjon
}

var enhetdescriptor TPeripheralcomponentinterconnectEnhetdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var driverAntall uint16 = 0

func (selv TMypcicontrollerhandler) Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor) {
	if enhet.Leverandørid == 0x1022 && enhet.Enhetid == 0x2000 {
		console.MSkrivutxy([]byte("["), 0, 12)
		console.MSkrivut(([]byte)("AMD am79c973"))
		console.MSkrivut([]byte(":"))
		console.MUnsignedinteger16Skrivut(enhet.Leverandørid)
		console.MSkrivut([]byte(":"))
		console.MUnsignedinteger16Skrivut(enhet.Enhetid)
		console.MSkrivut([]byte(":"))
		console.MUnsignedinteger16Skrivut(uint16(enhet.Portbase))
		console.MSkrivut([]byte(":"))
		console.MUnsignedinteger32Skrivut(enhet.Avbrudd)

		console.MSkrivut([]byte("]\n"))
		enhetdescriptor = enhet
		driverAntall++
	}
}
func (selv TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectEnhetdescriptor {
	return enhetdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Skrivutstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MSkrivut(str)
}

func GetFilStørrelse(filnavn []byte) uint32 {
	var ata0s = TAvansertTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Lespartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var størrelse uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	ata0s.Flush()

	return størrelse
}

func LesFil(filnavn []byte, data []byte) {
	var ata0s = TAvansertTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Lespartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Les(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)

	ata0s.Flush()
}
func Belastningelf() {

	var ata0s = TAvansertTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Lespartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var filnavn []byte = ([]byte)("TEST")
	var størrelse uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Les(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)

	elf := Elf{}

	elf.Parse(data[:størrelse], 0x4f00000)

}

var oppgaveconsole TConsole = TConsole{}

func TFunksjon1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func oppgavea() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func oppgaveb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func oppgavec() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func oppgaved()

func oppgaved0() {
	esi := getesi()
	for {

		SysSkrivutunsignedinteger32(esi)

	}
}

func oppgaved1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func inndataHendelseOppgave() {
	for {
		ProsesspendingTastaturevents()
		ProsesspendingMusevents()
		halt()
	}
}

func memorytest(y int) {
	minnemanager := &TMinnemanager{}
	allocated := uint32(uintptr(minnemanager.Malloc(1024)))
	console.MUnsignedinteger32Skrivutxy(allocated, 10, uint16(y))
	if y == 11 {
		minnemanager.Ledig(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func PauseLøkke()
func Lastpånyttcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Settcr3(cr3 uint32)
func Getcr4() uint32
func Slåpåpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunksjonNavn(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNavn = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcNavn)

	oppgaveconsole.MSkrivutxy(funcByte, 1, 5)
	oppgaveconsole.MSkrivut(([]byte)(":"))
	oppgaveconsole.MUnsignedinteger32Skrivut(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	oppgaveconsole.MSkrivutunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(SideKatalogentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerienummerLogginit()
	console.MSkrivut("\n=== SJM BOOT ===\n")

	console.MSkrivutunsignedinteger32(uint32(SideKatalogentry), 0, 2)
	console.MSkrivutunsignedinteger32(uint32(SideKatalogentry), 10, 2)
	console.MSkrivutunsignedinteger32(uint32(stacktop), 0, 3)
	console.MSkrivutunsignedinteger32(uint32(stackbottom), 10, 3)

	minnemanager := &TMinnemanager{}
	minnemanager.Init(0, MaksqueueStørrelse)

	paging := &Paging{}
	paging.Init(SideKatalogentry, 0x500000, minnemanager)
	paging.SharedMinneregion()

	Settcr3(uint32(SideKatalogentry))
	Slåpåpaging()

	shareddescriptorTabell := &TShareddescriptorTabell{}
	shareddescriptorTabell.Init()

	console.MSkrivut("esp:")

	esp := getesp()
	console.MUnsignedinteger32Skrivut(uint32(esp))

	tls := gettls()
	console.MSkrivut(([]byte)("tls:"))
	console.MUnsignedinteger32Skrivut(tls)

	tss.Installer(shareddescriptorTabell, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Lastpånyttcr3()
	console.MSkrivut(([]byte)(":cr3:"))
	console.MUnsignedinteger32Skrivut(cr3)

	cr0 := Getcr0()
	console.MSkrivut(([]byte)(":cr0:"))
	console.MUnsignedinteger32Skrivut(cr0)

	cr4 := Getcr4()
	console.MSkrivut(([]byte)(":cr4:"))
	console.MUnsignedinteger32Skrivut(cr4)

	oppgavemanager_2 := &TOppgavemanager{}
	oppgavemanager_2.Init()

	Avbruddmanager := &TAvbruddmanager{}
	Avbruddmanager.Init(0x20, shareddescriptorTabell, oppgavemanager_2)

	paging.Sidefault(Avbruddmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(minnemanager)

	prosesshelper := Prosesshelper{}
	prosesshelper.Init(minnemanager, SideKatalogentry)

	sche := &Scheduler{}
	sche.Init(Avbruddmanager, minnemanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Avbruddmanager)

	prosesshelper.Spawn(oppgavea, threadhelper, sche, uint32(SideKatalogentry), true)
	prosesshelper.Spawn(oppgaveb, threadhelper, sche, uint32(SideKatalogentry), true)
	prosesshelper.Spawn(oppgavec, threadhelper, sche, uint32(SideKatalogentry), true)
	prosesshelper.Spawn(oppgaved1, threadhelper, sche, uint32(SideKatalogentry), true)
	prosesshelper.Spawn(inndataHendelseOppgave, threadhelper, sche, uint32(SideKatalogentry), true)

	var størrelse uint32

	var linkerFil []byte = ([]byte)("LINKER")
	størrelse = GetFilStørrelse(linkerFil)
	linkeraddress := minnemanager.Malloc(størrelse)
	linkerdata := GetBytefromPeker(uintptr(linkeraddress), int(størrelse), int(størrelse))
	LesFil(linkerFil, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SideKatalogentry))

	lenkemap := Lenkemap{}
	lenkemap.Init(minnemanager)

	var lib1Fil []byte = ([]byte)("LIB1")
	størrelse = GetFilStørrelse(lib1Fil)

	lib1address := minnemanager.Malloc(størrelse)
	lib1data := GetBytefromPeker(uintptr(lib1address), int(størrelse), int(størrelse))
	LesFil(lib1Fil, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SideKatalogentry))
	minnemanager.Ledig(lib1address)

	lenkemap.Append_to_list(uintptr(lib1elf.Dynamisk))

	var lib2Fil []byte = ([]byte)("LIB2")
	størrelse = GetFilStørrelse(lib2Fil)

	lib2address := minnemanager.Malloc(størrelse)
	lib2data := GetBytefromPeker(uintptr(lib2address), int(størrelse), int(størrelse))
	LesFil(lib2Fil, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SideKatalogentry))
	minnemanager.Ledig(lib2address)

	lenkemap.Append_to_list(uintptr(lib2elf.Dynamisk))

	libLenkemap := lenkemap.Clone()
	lenkemapaddress := uint32(uintptr(Pointer(libLenkemap.First)))

	lib1got := Getunsignedinteger32TabellfromPeker(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = lenkemapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TabellfromPeker(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = lenkemapaddress
	lib2got[2] = 0x4000000

	console.MSkrivutxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Skrivut(lib1elf.Got)
	console.MSkrivut(":")
	console.MUnsignedinteger32Skrivut(lib1elf.Dynamisk)

	console.MSkrivutxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Skrivut(lib2elf.Got)
	console.MSkrivut(":")
	console.MUnsignedinteger32Skrivut(lib2elf.Dynamisk)

	var bruker1Fil []byte = ([]byte)("USER1")
	størrelse = GetFilStørrelse(bruker1Fil)
	bruker1address := minnemanager.Malloc(størrelse)
	bruker1data := GetBytefromPeker(uintptr(bruker1address), int(størrelse), int(størrelse))
	LesFil(bruker1Fil, bruker1data)

	elf2 := Elf{}

	bruker1entry := elf2.Getentry(bruker1data)
	elf2.Parse(bruker1data[:], uint32(SideKatalogentry+0x1000))
	globalAvstandTabell := elf2.Got

	PVerdi1Lenkemap := lenkemap.Clone()
	PVerdi1Lenkemap.Append_to_list(uintptr(elf2.Dynamisk))

	minnemanager.Ledig(bruker1address)

	var code1Peker *uintptr
	var func1val func()

	code1Peker = (*uintptr)(minnemanager.Malloc(4))
	*code1Peker = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Peker))

	proc2 := prosesshelper.Spawn(func1val, threadhelper, sche, uint32(SideKatalogentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStatus.Ecx = bruker1entry
	thr2.CpuStatus.Edx = globalAvstandTabell
	thr2.CpuStatus.Esi = uint32(uintptr(Pointer(PVerdi1Lenkemap.First)))

	console.MSkrivutxy("user1: ", 1, 10)
	console.MUnsignedinteger32Skrivut(elf2.Got)

	var bruker2Fil []byte = ([]byte)("USER2")
	størrelse = GetFilStørrelse(bruker2Fil)
	bruker2address := minnemanager.Malloc(størrelse)
	bruker2data := GetBytefromPeker(uintptr(bruker2address), int(størrelse), int(størrelse))
	LesFil(bruker2Fil, bruker2data)

	elf3 := Elf{}

	bruker2entry := elf3.Getentry(bruker2data)
	elf3.Parse(bruker2data[:], uint32(SideKatalogentry+0x2000))
	globalAvstandTabell = elf3.Got

	PVerdi2Lenkemap := lenkemap.Clone()
	PVerdi2Lenkemap.Append_to_list(uintptr(elf3.Dynamisk))

	minnemanager.Ledig(bruker2address)

	var code2Peker *uintptr
	var func2val func()

	code2Peker = (*uintptr)(minnemanager.Malloc(4))
	*code2Peker = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Peker))

	proc3 := prosesshelper.Spawn(func2val, threadhelper, sche, uint32(SideKatalogentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStatus.Ecx = bruker2entry
	thr3.CpuStatus.Edx = globalAvstandTabell
	thr3.CpuStatus.Esi = uint32(uintptr(Pointer(PVerdi2Lenkemap.First)))

	console.MSkrivutxy("user2: ", 1, 11)
	console.MUnsignedinteger32Skrivut(thr3.CpuStatus.Esi)

	libLenkemap.Skrivut(1, 11)

	var bruker3Fil []byte = ([]byte)("USER3")
	størrelse = GetFilStørrelse(bruker3Fil)
	bruker3address := minnemanager.Malloc(størrelse)
	bruker3data := GetBytefromPeker(uintptr(bruker3address), int(størrelse), int(størrelse))
	LesFil(bruker3Fil, bruker3data)

	elf4 := Elf{}

	bruker3entry := elf4.Getentry(bruker3data)
	elf4.Parse(bruker3data[:], uint32(SideKatalogentry+0x3000))
	globalAvstandTabell = elf4.Got

	PVerdi3Lenkemap := lenkemap.Clone()
	PVerdi3Lenkemap.Append_to_list(uintptr(elf4.Dynamisk))

	minnemanager.Ledig(bruker3address)

	var code3Peker *uintptr
	var func3val func()

	code3Peker = (*uintptr)(minnemanager.Malloc(4))
	*code3Peker = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Peker))

	proc4 := prosesshelper.Spawn(func3val, threadhelper, sche, uint32(SideKatalogentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStatus.Ecx = bruker3entry
	thr4.CpuStatus.Edx = globalAvstandTabell
	thr4.CpuStatus.Esi = uint32(uintptr(Pointer(PVerdi3Lenkemap.First)))

	prosesshelper.Spawn(TFunksjon1, threadhelper, sche, uint32(SideKatalogentry+0x4000), true)

	iTastaturHendelsehandler = &myTastaturHendelsehandler
	tastaturdriver.Initdriver(Avbruddmanager, iTastaturHendelsehandler)

	musdriver.Initdriver(Avbruddmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Velgdriver(&Drivermanager, Avbruddmanager)
	enhetdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Aktivert(true)
	Avbruddmanager.Aktiv()

	for {
		halt()
	}

}
