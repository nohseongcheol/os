/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konzole"
import . "přerušení"
import . "multitasking"
import . "tasking/tss"

import . "virtuálníPaměť"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/klávesnice"
import . "driver/polohovací_zařízení"

import . "driver/ata"
import . "souborSystém/msdospartition"
import . "souborSystém/fat"

import . "souborSystém/spustitelný_a_spojitelný_formát"

import . "systémcall"

import . "paměťmanager"
import . "pci"

func halt()

var iKlávesniceUdálostihandler IKlávesniceUdálostihandler

type TMyKlávesniceUdálostihandler struct {
}

var myKlávesniceUdálostihandler TMyKlávesniceUdálostihandler
var klávesnicedriver TKlávesnicedriver
var myšdriver TMyšdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var klávesniceKonzole TKonzole = TKonzole{}

func (self *TMyKlávesniceUdálostihandler) ZapnutoKlíčDolů(klíč byte) {
	foo := [1]byte{' '}
	foo[0] = klíč

	klávesniceKonzole.MTisknoutBytůxy(foo[:], 1000, 1000)
}

func (self *TMyKlávesniceUdálostihandler) ZapnutoKlíčNahoru(klíč byte)	{}

var iMyšUdálostihandler IMyšUdálostihandler

type TMyMyšUdálostihandler struct {
}

var myšKonzole TKonzole = TKonzole{}
var previousx int16 = 0
var previousy int16 = 0
var xUmístění int16 = 0
var yUmístění int16 = 0

func (self *TMyMyšUdálostihandler) ZapnutoMyšDolů(tlačítko int8) {
	buffer := []byte("x")
	myšKonzole.MTisknoutxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyMyšUdálostihandler) ZapnutoMyšNahoru(tlačítko int8)	{}
func (self *TMyMyšUdálostihandler) ZapnutoMyšPřesunout(x int8, y int8) {

	xUmístění += int16(x)
	if xUmístění < 0 {
		xUmístění = 0
	}
	if xUmístění >= 80 {
		xUmístění = 79
	}

	yUmístění -= int16(y)

	if yUmístění < 0 {
		yUmístění = 0
	}
	if yUmístění >= 25 {
		yUmístění = 24
	}

	buffer := []byte(" ")
	myšKonzole.MTisknoutxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	myšKonzole.MTisknoutxy(buffer, uint16(xUmístění), uint16(yUmístění))

	previousx = xUmístění
	previousy = yUmístění
}

var zařízenídescriptor TPeripheralcomponentinterconnectZařízenídescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var konzole TKonzole = TKonzole{}
var driverPočet uint16 = 0

func (self TMypcicontrollerhandler) Zapnutogetdriver(zařízení TPeripheralcomponentinterconnectZařízenídescriptor) {
	if zařízení.Výrobceid == 0x1022 && zařízení.Zařízeníid == 0x2000 {
		konzole.MTisknoutxy([]byte("["), 0, 12)
		konzole.MTisknout(([]byte)("AMD am79c973"))
		konzole.MTisknout([]byte(":"))
		konzole.MUnsignedinteger16Tisknout(zařízení.Výrobceid)
		konzole.MTisknout([]byte(":"))
		konzole.MUnsignedinteger16Tisknout(zařízení.Zařízeníid)
		konzole.MTisknout([]byte(":"))
		konzole.MUnsignedinteger16Tisknout(uint16(zařízení.Portbase))
		konzole.MTisknout([]byte(":"))
		konzole.MUnsignedinteger32Tisknout(zařízení.Přerušení)

		konzole.MTisknout([]byte("]\n"))
		zařízenídescriptor = zařízení
		driverPočet++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectZařízenídescriptor {
	return zařízenídescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Tisknoutstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konzole.MTisknout(str)
}

func GetSouborVelikost(názevsouboru []byte) uint32 {
	var ata0s = TPokročiléTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabulka{}
	partition.Čtenípartition(&ata0s)

	bios := TParametry_souborového_systému32{}

	var velikost uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru)
	ata0s.Flush()

	return velikost
}

func Číst_soubor(názevsouboru []byte, data []byte) {
	var ata0s = TPokročiléTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabulka{}
	partition.Čtenípartition(&ata0s)

	bios := TParametry_souborového_systému32{}
	bios.Čtení(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru, data)

	ata0s.Flush()
}
func Zátěželf() {

	var ata0s = TPokročiléTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabulka{}
	partition.Čtenípartition(&ata0s)

	bios := TParametry_souborového_systému32{}

	var názevsouboru []byte = ([]byte)("TEST")
	var velikost uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Čtení(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru, data)

	spustitelný_a_spojitelný_formát := Elf{}

	spustitelný_a_spojitelný_formát.Parse(data[:velikost], 0x4f00000)

}

var úlohaKonzole TKonzole = TKonzole{}

func TFunkce1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func úlohaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func úlohab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func úlohac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func úlohad()

func úlohad0() {
	esi := getesi()
	for {

		SysTisknoutunsignedinteger32(esi)

	}
}

func úlohad1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func vstupUdálostiÚloha() {
	for {
		ProcespendingKlávesniceUdálosti()
		ProcespendingMyšUdálosti()
		halt()
	}
}

func memorytest(y int) {
	paměťmanager := &TPaměťmanager{}
	allocated := uint32(uintptr(paměťmanager.Přidělit_paměť(1024)))
	konzole.MUnsignedinteger32Tisknoutxy(allocated, 10, uint16(y))
	if y == 11 {
		paměťmanager.Volné(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Uspatloop()
func Znovunačístcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Nastavitcr3(cr3 uint32)
func Getcr4() uint32
func Povolitpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkceNázev(i interface{}) {
	var adresa = reflect.ValueOf(i).Pointer()
	var funcNázev = runtime.FuncForPC(adresa).Name()
	var funcBytů []byte = []byte(funcNázev)

	úlohaKonzole.MTisknoutxy(funcBytů, 1, 5)
	úlohaKonzole.MTisknout(([]byte)(":"))
	úlohaKonzole.MUnsignedinteger32Tisknout(uint32(uintptr(adresa)))
}

func printreg() {
	cr0 := Getcr0()
	úlohaKonzole.MTisknoutunsignedinteger32(cr0, 2, 1)
}

var tss *TssZáznam = &TssZáznam{}

func KKernelEntry(StránkaadresářZáznam uintptr, stacktop uintptr, stackbottom uintptr) {

	MSériovýProtokolinit()
	konzole.MTisknout("\n=== CZE BOOT ===\n")

	konzole.MTisknoutunsignedinteger32(uint32(StránkaadresářZáznam), 0, 2)
	konzole.MTisknoutunsignedinteger32(uint32(StránkaadresářZáznam), 10, 2)
	konzole.MTisknoutunsignedinteger32(uint32(stacktop), 0, 3)
	konzole.MTisknoutunsignedinteger32(uint32(stackbottom), 10, 3)

	paměťmanager := &TPaměťmanager{}
	paměťmanager.Init(0, MaxqueueVelikost)

	paging := &Paging{}
	paging.Init(StránkaadresářZáznam, 0x500000, paměťmanager)
	paging.SharedPaměťregion()

	Nastavitcr3(uint32(StránkaadresářZáznam))
	Povolitpaging()

	shareddescriptorTabulka := &TShareddescriptorTabulka{}
	shareddescriptorTabulka.Init()

	konzole.MTisknout("esp:")

	esp := getesp()
	konzole.MUnsignedinteger32Tisknout(uint32(esp))

	tls := gettls()
	konzole.MTisknout(([]byte)("tls:"))
	konzole.MUnsignedinteger32Tisknout(tls)

	tss.Instalovat(shareddescriptorTabulka, 7, Segkerneldata, esp)

	VirtOtestovat()

	cr3 := Znovunačístcr3()
	konzole.MTisknout(([]byte)(":cr3:"))
	konzole.MUnsignedinteger32Tisknout(cr3)

	cr0 := Getcr0()
	konzole.MTisknout(([]byte)(":cr0:"))
	konzole.MUnsignedinteger32Tisknout(cr0)

	cr4 := Getcr4()
	konzole.MTisknout(([]byte)(":cr4:"))
	konzole.MUnsignedinteger32Tisknout(cr4)

	úlohamanager_2 := &TÚlohamanager{}
	úlohamanager_2.Init()

	Přerušenímanager := &TPřerušenímanager{}
	Přerušenímanager.Init(0x20, shareddescriptorTabulka, úlohamanager_2)

	paging.Stránkafault(Přerušenímanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(paměťmanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(paměťmanager, StránkaadresářZáznam)

	sche := &Scheduler{}
	sche.Init(Přerušenímanager, paměťmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Přerušenímanager)

	proceshelper.Spawn(úlohaa, threadhelper, sche, uint32(StránkaadresářZáznam), true)
	proceshelper.Spawn(úlohab, threadhelper, sche, uint32(StránkaadresářZáznam), true)
	proceshelper.Spawn(úlohac, threadhelper, sche, uint32(StránkaadresářZáznam), true)
	proceshelper.Spawn(úlohad1, threadhelper, sche, uint32(StránkaadresářZáznam), true)
	proceshelper.Spawn(vstupUdálostiÚloha, threadhelper, sche, uint32(StránkaadresářZáznam), true)

	var velikost uint32

	var linkerSoubor []byte = ([]byte)("LINKER")
	velikost = GetSouborVelikost(linkerSoubor)
	linkerAdresa := paměťmanager.Přidělit_paměť(velikost)
	linkerdata := GetBytůzKurzor(uintptr(linkerAdresa), int(velikost), int(velikost))
	Číst_soubor(linkerSoubor, linkerdata)

	elf0 := Elf{}
	linkerZáznam := elf0.GetZáznam(linkerdata)
	elf0.Parse(linkerdata[:], uint32(StránkaadresářZáznam))

	odkazmap := Odkazmap{}
	odkazmap.Init(paměťmanager)

	var lib1Soubor []byte = ([]byte)("LIB1")
	velikost = GetSouborVelikost(lib1Soubor)

	lib1Adresa := paměťmanager.Přidělit_paměť(velikost)
	lib1data := GetBytůzKurzor(uintptr(lib1Adresa), int(velikost), int(velikost))
	Číst_soubor(lib1Soubor, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(StránkaadresářZáznam))
	paměťmanager.Volné(lib1Adresa)

	odkazmap.Přidat_na_konec_seznamu(uintptr(lib1elf.Dynamické))

	var lib2Soubor []byte = ([]byte)("LIB2")
	velikost = GetSouborVelikost(lib2Soubor)

	lib2Adresa := paměťmanager.Přidělit_paměť(velikost)
	lib2data := GetBytůzKurzor(uintptr(lib2Adresa), int(velikost), int(velikost))
	Číst_soubor(lib2Soubor, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(StránkaadresářZáznam))
	paměťmanager.Volné(lib2Adresa)

	odkazmap.Přidat_na_konec_seznamu(uintptr(lib2elf.Dynamické))

	libOdkazmap := odkazmap.Clone()
	odkazmapAdresa := uint32(uintptr(Pointer(libOdkazmap.First)))

	lib1got := Getunsignedinteger32PolezKurzor(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = odkazmapAdresa
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32PolezKurzor(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = odkazmapAdresa
	lib2got[2] = 0x4000000

	konzole.MTisknoutxy("lib1: ", 1, 8)
	konzole.MUnsignedinteger32Tisknout(lib1elf.Got)
	konzole.MTisknout(":")
	konzole.MUnsignedinteger32Tisknout(lib1elf.Dynamické)

	konzole.MTisknoutxy("lib2: ", 1, 9)
	konzole.MUnsignedinteger32Tisknout(lib2elf.Got)
	konzole.MTisknout(":")
	konzole.MUnsignedinteger32Tisknout(lib2elf.Dynamické)

	var uživatel1Soubor []byte = ([]byte)("USER1")
	velikost = GetSouborVelikost(uživatel1Soubor)
	uživatel1Adresa := paměťmanager.Přidělit_paměť(velikost)
	uživatel1data := GetBytůzKurzor(uintptr(uživatel1Adresa), int(velikost), int(velikost))
	Číst_soubor(uživatel1Soubor, uživatel1data)

	elf2 := Elf{}

	uživatel1Záznam := elf2.GetZáznam(uživatel1data)
	elf2.Parse(uživatel1data[:], uint32(StránkaadresářZáznam+0x1000))
	globálníoffsetTabulka := elf2.Got

	PHodnota1Odkazmap := odkazmap.Clone()
	PHodnota1Odkazmap.Přidat_na_konec_seznamu(uintptr(elf2.Dynamické))

	paměťmanager.Volné(uživatel1Adresa)

	var code1Kurzor *uintptr
	var func1val func()

	code1Kurzor = (*uintptr)(paměťmanager.Přidělit_paměť(4))
	*code1Kurzor = uintptr(linkerZáznam)
	func1val = *(*func())(Pointer(&code1Kurzor))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(StránkaadresářZáznam+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStav.Ecx = uživatel1Záznam
	thr2.CpuStav.Edx = globálníoffsetTabulka
	thr2.CpuStav.Esi = uint32(uintptr(Pointer(PHodnota1Odkazmap.First)))

	konzole.MTisknoutxy("user1: ", 1, 10)
	konzole.MUnsignedinteger32Tisknout(elf2.Got)

	var uživatel2Soubor []byte = ([]byte)("USER2")
	velikost = GetSouborVelikost(uživatel2Soubor)
	uživatel2Adresa := paměťmanager.Přidělit_paměť(velikost)
	uživatel2data := GetBytůzKurzor(uintptr(uživatel2Adresa), int(velikost), int(velikost))
	Číst_soubor(uživatel2Soubor, uživatel2data)

	elf3 := Elf{}

	uživatel2Záznam := elf3.GetZáznam(uživatel2data)
	elf3.Parse(uživatel2data[:], uint32(StránkaadresářZáznam+0x2000))
	globálníoffsetTabulka = elf3.Got

	PHodnota2Odkazmap := odkazmap.Clone()
	PHodnota2Odkazmap.Přidat_na_konec_seznamu(uintptr(elf3.Dynamické))

	paměťmanager.Volné(uživatel2Adresa)

	var code2Kurzor *uintptr
	var func2val func()

	code2Kurzor = (*uintptr)(paměťmanager.Přidělit_paměť(4))
	*code2Kurzor = uintptr(linkerZáznam)
	func2val = *(*func())(Pointer(&code2Kurzor))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(StránkaadresářZáznam+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStav.Ecx = uživatel2Záznam
	thr3.CpuStav.Edx = globálníoffsetTabulka
	thr3.CpuStav.Esi = uint32(uintptr(Pointer(PHodnota2Odkazmap.First)))

	konzole.MTisknoutxy("user2: ", 1, 11)
	konzole.MUnsignedinteger32Tisknout(thr3.CpuStav.Esi)

	libOdkazmap.Tisknout(1, 11)

	var uživatel3Soubor []byte = ([]byte)("USER3")
	velikost = GetSouborVelikost(uživatel3Soubor)
	uživatel3Adresa := paměťmanager.Přidělit_paměť(velikost)
	uživatel3data := GetBytůzKurzor(uintptr(uživatel3Adresa), int(velikost), int(velikost))
	Číst_soubor(uživatel3Soubor, uživatel3data)

	elf4 := Elf{}

	uživatel3Záznam := elf4.GetZáznam(uživatel3data)
	elf4.Parse(uživatel3data[:], uint32(StránkaadresářZáznam+0x3000))
	globálníoffsetTabulka = elf4.Got

	PHodnota3Odkazmap := odkazmap.Clone()
	PHodnota3Odkazmap.Přidat_na_konec_seznamu(uintptr(elf4.Dynamické))

	paměťmanager.Volné(uživatel3Adresa)

	var code3Kurzor *uintptr
	var func3val func()

	code3Kurzor = (*uintptr)(paměťmanager.Přidělit_paměť(4))
	*code3Kurzor = uintptr(linkerZáznam)
	func3val = *(*func())(Pointer(&code3Kurzor))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(StránkaadresářZáznam+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStav.Ecx = uživatel3Záznam
	thr4.CpuStav.Edx = globálníoffsetTabulka
	thr4.CpuStav.Esi = uint32(uintptr(Pointer(PHodnota3Odkazmap.First)))

	proceshelper.Spawn(TFunkce1, threadhelper, sche, uint32(StránkaadresářZáznam+0x4000), true)

	iKlávesniceUdálostihandler = &myKlávesniceUdálostihandler
	klávesnicedriver.Initdriver(Přerušenímanager, iKlávesniceUdálostihandler)

	myšdriver.Initdriver(Přerušenímanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Vybratdriver(&Drivermanager, Přerušenímanager)
	zařízenídescriptor = mypcicontrollerhandler.Getdriver()

	sche.Povoleno(true)
	Přerušenímanager.Aktivní()

	for {
		halt()
	}

}
