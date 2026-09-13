package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "pertraukimas"
import . "multitasking"
import . "tasking/tss"

import . "virtualiAtmintis"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/procesas"
import . "driver/driver"

import . "driver/klaviatūra"
import . "driver/pelė"

import . "driver/ata"
import . "failasSistema/msdospartition"
import . "failasSistema/fat"

import . "failasSistema/elf"

import . "sistemacall"

import . "atmintismanager"
import . "pci"

func halt()

var iKlaviatūraĮvykishandler IKlaviatūraĮvykishandler

type TMyKlaviatūraĮvykishandler struct {
}

var myKlaviatūraĮvykishandler TMyKlaviatūraĮvykishandler
var klaviatūradriver TKlaviatūradriver
var pelėdriver TPelėdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klaviatūraconsole TConsole = TConsole{}

func (self *TMyKlaviatūraĮvykishandler) ĮjungtaRaktasŽemyn(raktas byte) {
	foo := [1]byte{' '}
	foo[0] = raktas

	klaviatūraconsole.MSpausdintiBaitųxy(foo[:], 1000, 1000)
}

func (self *TMyKlaviatūraĮvykishandler) ĮjungtaRaktasAukštyn(raktas byte)	{}

var iPelėĮvykishandler IPelėĮvykishandler

type TMyPelėĮvykishandler struct {
}

var pelėconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (self *TMyPelėĮvykishandler) ĮjungtaPelėŽemyn(mygtukas int8) {
	buffer := []byte("x")
	pelėconsole.MSpausdintixy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyPelėĮvykishandler) ĮjungtaPelėAukštyn(mygtukas int8)	{}
func (self *TMyPelėĮvykishandler) ĮjungtaPelėPerkelti(x int8, y int8) {

	xPozicija += int16(x)
	if xPozicija < 0 {
		xPozicija = 0
	}
	if xPozicija >= 80 {
		xPozicija = 79
	}

	yPozicija -= int16(y)

	if yPozicija < 0 {
		yPozicija = 0
	}
	if yPozicija >= 25 {
		yPozicija = 24
	}

	buffer := []byte(" ")
	pelėconsole.MSpausdintixy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	pelėconsole.MSpausdintixy(buffer, uint16(xPozicija), uint16(yPozicija))

	previousx = xPozicija
	previousy = yPozicija
}

var įrenginysdescriptor TPeripheralcomponentinterconnectĮrenginysdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Įjungtagetdriver(įrenginys TPeripheralcomponentinterconnectĮrenginysdescriptor) {
	if įrenginys.Gamintojasid == 0x1022 && įrenginys.Įrenginysid == 0x2000 {
		console.MSpausdintixy([]byte("["), 0, 12)
		console.MSpausdinti(([]byte)("AMD am79c973"))
		console.MSpausdinti([]byte(":"))
		console.MUnsignedinteger16Spausdinti(įrenginys.Gamintojasid)
		console.MSpausdinti([]byte(":"))
		console.MUnsignedinteger16Spausdinti(įrenginys.Įrenginysid)
		console.MSpausdinti([]byte(":"))
		console.MUnsignedinteger16Spausdinti(uint16(įrenginys.Prievadasbase))
		console.MSpausdinti([]byte(":"))
		console.MUnsignedinteger32Spausdinti(įrenginys.Pertraukimas)

		console.MSpausdinti([]byte("]\n"))
		įrenginysdescriptor = įrenginys
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectĮrenginysdescriptor {
	return įrenginysdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Spausdintistr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MSpausdinti(str)
}

func GetFailasDydis(failopavadinimas []byte) uint32 {
	var ata0s = TIšsamiauTechnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionLentelė{}
	partition.Skaitymaspartition(&ata0s)

	bios := TBiosparameterBlokas32{}

	var dydis uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas)
	ata0s.Flush()

	return dydis
}

func SkaitymasFailas(failopavadinimas []byte, data []byte) {
	var ata0s = TIšsamiauTechnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionLentelė{}
	partition.Skaitymaspartition(&ata0s)

	bios := TBiosparameterBlokas32{}
	bios.Skaitymas(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas, data)

	ata0s.Flush()
}
func Apkrovaelf() {

	var ata0s = TIšsamiauTechnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionLentelė{}
	partition.Skaitymaspartition(&ata0s)

	bios := TBiosparameterBlokas32{}

	var failopavadinimas []byte = ([]byte)("TEST")
	var dydis uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Skaitymas(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas, data)

	elf := Elf{}

	elf.Parse(data[:dydis], 0x4f00000)

}

var užduotisconsole TConsole = TConsole{}

func TFunkcija1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func užduotisa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func užduotisb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func užduotisc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func užduotisd()

func užduotisd0() {
	esi := getesi()
	for {

		SysSpausdintiunsignedinteger32(esi)

	}
}

func užduotisd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func įvestisĮvykisUžduotis() {
	for {
		ProcesaspendingKlaviatūraĮvykiai()
		ProcesaspendingPelėĮvykiai()
		halt()
	}
}

func memorytest(y int) {
	atmintismanager := &TAtmintismanager{}
	allocated := uint32(uintptr(atmintismanager.Malloc(1024)))
	console.MUnsignedinteger32Spausdintixy(allocated, 10, uint16(y))
	if y == 11 {
		atmintismanager.Laisva(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pristabdytiloop()
func Įkeltiišnaujocr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Nustatytacr3(cr3 uint32)
func Getcr4() uint32
func Įjungtipaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcijaPavadinimas(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcPavadinimas = runtime.FuncForPC(address).Name()
	var funcBaitų []byte = []byte(funcPavadinimas)

	užduotisconsole.MSpausdintixy(funcBaitų, 1, 5)
	užduotisconsole.MSpausdinti(([]byte)(":"))
	užduotisconsole.MUnsignedinteger32Spausdinti(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	užduotisconsole.MSpausdintiunsignedinteger32(cr0, 2, 1)
}

var tss *Tssįrašas = &Tssįrašas{}

func KKernelEntry(Puslapiskatalogasįrašas uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerijinisŽurnalasinit()
	console.MSpausdinti("\n=== LTU BOOT ===\n")

	console.MSpausdintiunsignedinteger32(uint32(Puslapiskatalogasįrašas), 0, 2)
	console.MSpausdintiunsignedinteger32(uint32(Puslapiskatalogasįrašas), 10, 2)
	console.MSpausdintiunsignedinteger32(uint32(stacktop), 0, 3)
	console.MSpausdintiunsignedinteger32(uint32(stackbottom), 10, 3)

	atmintismanager := &TAtmintismanager{}
	atmintismanager.Init(0, MaksqueueDydis)

	paging := &Paging{}
	paging.Init(Puslapiskatalogasįrašas, 0x500000, atmintismanager)
	paging.SharedAtmintisregion()

	Nustatytacr3(uint32(Puslapiskatalogasįrašas))
	Įjungtipaging()

	shareddescriptorLentelė := &TShareddescriptorLentelė{}
	shareddescriptorLentelė.Init()

	console.MSpausdinti("esp:")

	esp := getesp()
	console.MUnsignedinteger32Spausdinti(uint32(esp))

	tls := gettls()
	console.MSpausdinti(([]byte)("tls:"))
	console.MUnsignedinteger32Spausdinti(tls)

	tss.Įdiegti(shareddescriptorLentelė, 7, Segkerneldata, esp)

	VirtTestas()

	cr3 := Įkeltiišnaujocr3()
	console.MSpausdinti(([]byte)(":cr3:"))
	console.MUnsignedinteger32Spausdinti(cr3)

	cr0 := Getcr0()
	console.MSpausdinti(([]byte)(":cr0:"))
	console.MUnsignedinteger32Spausdinti(cr0)

	cr4 := Getcr4()
	console.MSpausdinti(([]byte)(":cr4:"))
	console.MUnsignedinteger32Spausdinti(cr4)

	užduotismanager_2 := &TUžduotismanager{}
	užduotismanager_2.Init()

	Pertraukimasmanager := &TPertraukimasmanager{}
	Pertraukimasmanager.Init(0x20, shareddescriptorLentelė, užduotismanager_2)

	paging.Puslapisfault(Pertraukimasmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(atmintismanager)

	procesashelper := Procesashelper{}
	procesashelper.Init(atmintismanager, Puslapiskatalogasįrašas)

	sche := &Scheduler{}
	sche.Init(Pertraukimasmanager, atmintismanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Pertraukimasmanager)

	procesashelper.Spawn(užduotisa, threadhelper, sche, uint32(Puslapiskatalogasįrašas), true)
	procesashelper.Spawn(užduotisb, threadhelper, sche, uint32(Puslapiskatalogasįrašas), true)
	procesashelper.Spawn(užduotisc, threadhelper, sche, uint32(Puslapiskatalogasįrašas), true)
	procesashelper.Spawn(užduotisd1, threadhelper, sche, uint32(Puslapiskatalogasįrašas), true)
	procesashelper.Spawn(įvestisĮvykisUžduotis, threadhelper, sche, uint32(Puslapiskatalogasįrašas), true)

	var dydis uint32

	var linkerFailas []byte = ([]byte)("LINKER")
	dydis = GetFailasDydis(linkerFailas)
	linkeraddress := atmintismanager.Malloc(dydis)
	linkerdata := GetBaitųfromRodyklė(uintptr(linkeraddress), int(dydis), int(dydis))
	SkaitymasFailas(linkerFailas, linkerdata)

	elf0 := Elf{}
	linkerįrašas := elf0.Getįrašas(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Puslapiskatalogasįrašas))

	nuorodamap := Nuorodamap{}
	nuorodamap.Init(atmintismanager)

	var lib1Failas []byte = ([]byte)("LIB1")
	dydis = GetFailasDydis(lib1Failas)

	lib1address := atmintismanager.Malloc(dydis)
	lib1data := GetBaitųfromRodyklė(uintptr(lib1address), int(dydis), int(dydis))
	SkaitymasFailas(lib1Failas, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Puslapiskatalogasįrašas))
	atmintismanager.Laisva(lib1address)

	nuorodamap.Append_to_list(uintptr(lib1elf.Dinaminis))

	var lib2Failas []byte = ([]byte)("LIB2")
	dydis = GetFailasDydis(lib2Failas)

	lib2address := atmintismanager.Malloc(dydis)
	lib2data := GetBaitųfromRodyklė(uintptr(lib2address), int(dydis), int(dydis))
	SkaitymasFailas(lib2Failas, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Puslapiskatalogasįrašas))
	atmintismanager.Laisva(lib2address)

	nuorodamap.Append_to_list(uintptr(lib2elf.Dinaminis))

	libNuorodamap := nuorodamap.Clone()
	nuorodamapaddress := uint32(uintptr(Pointer(libNuorodamap.First)))

	lib1got := Getunsignedinteger32MasyvasfromRodyklė(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = nuorodamapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32MasyvasfromRodyklė(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = nuorodamapaddress
	lib2got[2] = 0x4000000

	console.MSpausdintixy("lib1: ", 1, 8)
	console.MUnsignedinteger32Spausdinti(lib1elf.Got)
	console.MSpausdinti(":")
	console.MUnsignedinteger32Spausdinti(lib1elf.Dinaminis)

	console.MSpausdintixy("lib2: ", 1, 9)
	console.MUnsignedinteger32Spausdinti(lib2elf.Got)
	console.MSpausdinti(":")
	console.MUnsignedinteger32Spausdinti(lib2elf.Dinaminis)

	var naudotojas1Failas []byte = ([]byte)("USER1")
	dydis = GetFailasDydis(naudotojas1Failas)
	naudotojas1address := atmintismanager.Malloc(dydis)
	naudotojas1data := GetBaitųfromRodyklė(uintptr(naudotojas1address), int(dydis), int(dydis))
	SkaitymasFailas(naudotojas1Failas, naudotojas1data)

	elf2 := Elf{}

	naudotojas1įrašas := elf2.Getįrašas(naudotojas1data)
	elf2.Parse(naudotojas1data[:], uint32(Puslapiskatalogasįrašas+0x1000))
	visuotinėoffsetLentelė := elf2.Got

	PReikšmė1Nuorodamap := nuorodamap.Clone()
	PReikšmė1Nuorodamap.Append_to_list(uintptr(elf2.Dinaminis))

	atmintismanager.Laisva(naudotojas1address)

	var code1Rodyklė *uintptr
	var func1val func()

	code1Rodyklė = (*uintptr)(atmintismanager.Malloc(4))
	*code1Rodyklė = uintptr(linkerįrašas)
	func1val = *(*func())(Pointer(&code1Rodyklė))

	proc2 := procesashelper.Spawn(func1val, threadhelper, sche, uint32(Puslapiskatalogasįrašas+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuBūsena.Ecx = naudotojas1įrašas
	thr2.CpuBūsena.Edx = visuotinėoffsetLentelė
	thr2.CpuBūsena.Esi = uint32(uintptr(Pointer(PReikšmė1Nuorodamap.First)))

	console.MSpausdintixy("user1: ", 1, 10)
	console.MUnsignedinteger32Spausdinti(elf2.Got)

	var naudotojas2Failas []byte = ([]byte)("USER2")
	dydis = GetFailasDydis(naudotojas2Failas)
	naudotojas2address := atmintismanager.Malloc(dydis)
	naudotojas2data := GetBaitųfromRodyklė(uintptr(naudotojas2address), int(dydis), int(dydis))
	SkaitymasFailas(naudotojas2Failas, naudotojas2data)

	elf3 := Elf{}

	naudotojas2įrašas := elf3.Getįrašas(naudotojas2data)
	elf3.Parse(naudotojas2data[:], uint32(Puslapiskatalogasįrašas+0x2000))
	visuotinėoffsetLentelė = elf3.Got

	PReikšmė2Nuorodamap := nuorodamap.Clone()
	PReikšmė2Nuorodamap.Append_to_list(uintptr(elf3.Dinaminis))

	atmintismanager.Laisva(naudotojas2address)

	var code2Rodyklė *uintptr
	var func2val func()

	code2Rodyklė = (*uintptr)(atmintismanager.Malloc(4))
	*code2Rodyklė = uintptr(linkerįrašas)
	func2val = *(*func())(Pointer(&code2Rodyklė))

	proc3 := procesashelper.Spawn(func2val, threadhelper, sche, uint32(Puslapiskatalogasįrašas+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuBūsena.Ecx = naudotojas2įrašas
	thr3.CpuBūsena.Edx = visuotinėoffsetLentelė
	thr3.CpuBūsena.Esi = uint32(uintptr(Pointer(PReikšmė2Nuorodamap.First)))

	console.MSpausdintixy("user2: ", 1, 11)
	console.MUnsignedinteger32Spausdinti(thr3.CpuBūsena.Esi)

	libNuorodamap.Spausdinti(1, 11)

	var naudotojas3Failas []byte = ([]byte)("USER3")
	dydis = GetFailasDydis(naudotojas3Failas)
	naudotojas3address := atmintismanager.Malloc(dydis)
	naudotojas3data := GetBaitųfromRodyklė(uintptr(naudotojas3address), int(dydis), int(dydis))
	SkaitymasFailas(naudotojas3Failas, naudotojas3data)

	elf4 := Elf{}

	naudotojas3įrašas := elf4.Getįrašas(naudotojas3data)
	elf4.Parse(naudotojas3data[:], uint32(Puslapiskatalogasįrašas+0x3000))
	visuotinėoffsetLentelė = elf4.Got

	PReikšmė3Nuorodamap := nuorodamap.Clone()
	PReikšmė3Nuorodamap.Append_to_list(uintptr(elf4.Dinaminis))

	atmintismanager.Laisva(naudotojas3address)

	var code3Rodyklė *uintptr
	var func3val func()

	code3Rodyklė = (*uintptr)(atmintismanager.Malloc(4))
	*code3Rodyklė = uintptr(linkerįrašas)
	func3val = *(*func())(Pointer(&code3Rodyklė))

	proc4 := procesashelper.Spawn(func3val, threadhelper, sche, uint32(Puslapiskatalogasįrašas+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuBūsena.Ecx = naudotojas3įrašas
	thr4.CpuBūsena.Edx = visuotinėoffsetLentelė
	thr4.CpuBūsena.Esi = uint32(uintptr(Pointer(PReikšmė3Nuorodamap.First)))

	procesashelper.Spawn(TFunkcija1, threadhelper, sche, uint32(Puslapiskatalogasįrašas+0x4000), true)

	iKlaviatūraĮvykishandler = &myKlaviatūraĮvykishandler
	klaviatūradriver.Initdriver(Pertraukimasmanager, iKlaviatūraĮvykishandler)

	pelėdriver.Initdriver(Pertraukimasmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Žymėtidriver(&Drivermanager, Pertraukimasmanager)
	įrenginysdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Įjungta(true)
	Pertraukimasmanager.Aktyvus()

	for {
		halt()
	}

}
