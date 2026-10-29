/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsoli"
import . "keskeytys"
import . "multitasking"
import . "tasking/tss"

import . "virtuaalinenMuisti"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/prosessi"
import . "driver/driver"

import . "driver/näppäimistö"
import . "driver/osoitinlaite"

import . "driver/ata"
import . "tiedostoJärjestelmä/msdospartition"
import . "tiedostoJärjestelmä/fat"

import . "tiedostoJärjestelmä/suoritettava_ja_linkitettävä_muoto"

import . "järjestelmäcall"

import . "muistimanager"
import . "pci"

func halt()

var iNäppäimistöTapahtumahandler INäppäimistöTapahtumahandler

type TMyNäppäimistöTapahtumahandler struct {
}

var myNäppäimistöTapahtumahandler TMyNäppäimistöTapahtumahandler
var näppäimistödriver TNäppäimistödriver
var hiiridriver THiiridriver
var pciOhjain TPeripheralcomponentinterconnectOhjain

var näppäimistöKonsoli TKonsoli = TKonsoli{}

func (itse *TMyNäppäimistöTapahtumahandler) PäälläAvainAlas(avain byte) {
	foo := [1]byte{' '}
	foo[0] = avain

	näppäimistöKonsoli.MTulostatavuaxy(foo[:], 1000, 1000)
}

func (itse *TMyNäppäimistöTapahtumahandler) PäälläAvainYlös(avain byte)	{}

var iHiiriTapahtumahandler IHiiriTapahtumahandler

type TMyHiiriTapahtumahandler struct {
}

var hiiriKonsoli TKonsoli = TKonsoli{}
var previousx int16 = 0
var previousy int16 = 0
var xSijainti int16 = 0
var ySijainti int16 = 0

func (itse *TMyHiiriTapahtumahandler) PäälläHiiriAlas(painike int8) {
	buffer := []byte("x")
	hiiriKonsoli.MTulostaxy(buffer, uint16(previousx), uint16(previousy))
}
func (itse *TMyHiiriTapahtumahandler) PäälläHiiriYlös(painike int8)	{}
func (itse *TMyHiiriTapahtumahandler) PäälläHiiriSiirrä(x int8, y int8) {

	xSijainti += int16(x)
	if xSijainti < 0 {
		xSijainti = 0
	}
	if xSijainti >= 80 {
		xSijainti = 79
	}

	ySijainti -= int16(y)

	if ySijainti < 0 {
		ySijainti = 0
	}
	if ySijainti >= 25 {
		ySijainti = 24
	}

	buffer := []byte(" ")
	hiiriKonsoli.MTulostaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	hiiriKonsoli.MTulostaxy(buffer, uint16(xSijainti), uint16(ySijainti))

	previousx = xSijainti
	previousy = ySijainti
}

var laitedescriptor TPeripheralcomponentinterconnectLaitedescriptor
var ipciOhjainhandler IpciOhjainhandler

type TMypciOhjainhandler struct {
}

var konsoli TKonsoli = TKonsoli{}
var drivercount uint16 = 0

func (itse TMypciOhjainhandler) Päällägetdriver(laite TPeripheralcomponentinterconnectLaitedescriptor) {
	if laite.ValmistajaTUNNISTE == 0x1022 && laite.LaiteTUNNISTE == 0x2000 {
		konsoli.MTulostaxy([]byte("["), 0, 12)
		konsoli.MTulosta(([]byte)("AMD am79c973"))
		konsoli.MTulosta([]byte(":"))
		konsoli.MUnsignedinteger16Tulosta(laite.ValmistajaTUNNISTE)
		konsoli.MTulosta([]byte(":"))
		konsoli.MUnsignedinteger16Tulosta(laite.LaiteTUNNISTE)
		konsoli.MTulosta([]byte(":"))
		konsoli.MUnsignedinteger16Tulosta(uint16(laite.Porttibase))
		konsoli.MTulosta([]byte(":"))
		konsoli.MUnsignedinteger32Tulosta(laite.Keskeytys)

		konsoli.MTulosta([]byte("]\n"))
		laitedescriptor = laite
		drivercount++
	}
}
func (itse TMypciOhjainhandler) Getdriver() TPeripheralcomponentinterconnectLaitedescriptor {
	return laitedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Tulostastr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsoli.MTulosta(str)
}

func GetTiedostoKoko(tiedostonimi []byte) uint32 {
	var ata0s = TLisäasetuksetTekniikkaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaulukko{}
	partition.Lukupartition(&ata0s)

	bios := TTiedostojärjestelmän_parametrit32{}

	var koko uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi)
	ata0s.Flush()

	return koko
}

func Lue_tiedosto(tiedostonimi []byte, data []byte) {
	var ata0s = TLisäasetuksetTekniikkaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaulukko{}
	partition.Lukupartition(&ata0s)

	bios := TTiedostojärjestelmän_parametrit32{}
	bios.Luku(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi, data)

	ata0s.Flush()
}
func Kuormaelf() {

	var ata0s = TLisäasetuksetTekniikkaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaulukko{}
	partition.Lukupartition(&ata0s)

	bios := TTiedostojärjestelmän_parametrit32{}

	var tiedostonimi []byte = ([]byte)("TEST")
	var koko uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Luku(&ata0s, partition.Mbr.Primarypartition[0], tiedostonimi, data)

	suoritettava_ja_linkitettävä_muoto := Elf{}

	suoritettava_ja_linkitettävä_muoto.Parse(data[:koko], 0x4f00000)

}

var tehtäväKonsoli TKonsoli = TKonsoli{}

func TFunktio1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tehtäväa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tehtäväb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tehtäväc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tehtäväd()

func tehtäväd0() {
	esi := getesi()
	for {

		SysTulostaunsignedinteger32(esi)

	}
}

func tehtäväd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func syöteTapahtumaTehtävä() {
	for {
		ProsessipendingNäppäimistöTapahtumat()
		ProsessipendingHiiriTapahtumat()
		halt()
	}
}

func memorytest(y int) {
	muistimanager := &TMuistimanager{}
	allocated := uint32(uintptr(muistimanager.Varaa_muistia(1024)))
	konsoli.MUnsignedinteger32Tulostaxy(allocated, 10, uint16(y))
	if y == 11 {
		muistimanager.Vapaana(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Keskeytäloop()
func Lataauudelleencr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Asetacr3(cr3 uint32)
func Getcr4() uint32
func Otakäyttöönpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunktioNimi(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNimi = runtime.FuncForPC(address).Name()
	var functavua []byte = []byte(funcNimi)

	tehtäväKonsoli.MTulostaxy(functavua, 1, 5)
	tehtäväKonsoli.MTulosta(([]byte)(":"))
	tehtäväKonsoli.MUnsignedinteger32Tulosta(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	tehtäväKonsoli.MTulostaunsignedinteger32(cr0, 2, 1)
}

var tss *Tsshakusana = &Tsshakusana{}

func KKernelEntry(SivuKansiohakusana uintptr, stacktop uintptr, stackbottom uintptr) {

	MSarjaKäytälokiainit()
	konsoli.MTulosta("\n=== FIN BOOT ===\n")

	konsoli.MTulostaunsignedinteger32(uint32(SivuKansiohakusana), 0, 2)
	konsoli.MTulostaunsignedinteger32(uint32(SivuKansiohakusana), 10, 2)
	konsoli.MTulostaunsignedinteger32(uint32(stacktop), 0, 3)
	konsoli.MTulostaunsignedinteger32(uint32(stackbottom), 10, 3)

	muistimanager := &TMuistimanager{}
	muistimanager.Init(0, MaksimiqueueKoko)

	paging := &Paging{}
	paging.Init(SivuKansiohakusana, 0x500000, muistimanager)
	paging.SharedMuistiregion()

	Asetacr3(uint32(SivuKansiohakusana))
	Otakäyttöönpaging()

	shareddescriptorTaulukko := &TShareddescriptorTaulukko{}
	shareddescriptorTaulukko.Init()

	konsoli.MTulosta("esp:")

	esp := getesp()
	konsoli.MUnsignedinteger32Tulosta(uint32(esp))

	tls := gettls()
	konsoli.MTulosta(([]byte)("tls:"))
	konsoli.MUnsignedinteger32Tulosta(tls)

	tss.Asenna(shareddescriptorTaulukko, 7, Segkerneldata, esp)

	VirtKokeile()

	cr3 := Lataauudelleencr3()
	konsoli.MTulosta(([]byte)(":cr3:"))
	konsoli.MUnsignedinteger32Tulosta(cr3)

	cr0 := Getcr0()
	konsoli.MTulosta(([]byte)(":cr0:"))
	konsoli.MUnsignedinteger32Tulosta(cr0)

	cr4 := Getcr4()
	konsoli.MTulosta(([]byte)(":cr4:"))
	konsoli.MUnsignedinteger32Tulosta(cr4)

	tehtävämanager_2 := &TTehtävämanager{}
	tehtävämanager_2.Init()

	Keskeytysmanager := &TKeskeytysmanager{}
	Keskeytysmanager.Init(0x20, shareddescriptorTaulukko, tehtävämanager_2)

	paging.Sivufault(Keskeytysmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(muistimanager)

	prosessihelper := Prosessihelper{}
	prosessihelper.Init(muistimanager, SivuKansiohakusana)

	sche := &Scheduler{}
	sche.Init(Keskeytysmanager, muistimanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Keskeytysmanager)

	prosessihelper.Spawn(tehtäväa, threadhelper, sche, uint32(SivuKansiohakusana), true)
	prosessihelper.Spawn(tehtäväb, threadhelper, sche, uint32(SivuKansiohakusana), true)
	prosessihelper.Spawn(tehtäväc, threadhelper, sche, uint32(SivuKansiohakusana), true)
	prosessihelper.Spawn(tehtäväd1, threadhelper, sche, uint32(SivuKansiohakusana), true)
	prosessihelper.Spawn(syöteTapahtumaTehtävä, threadhelper, sche, uint32(SivuKansiohakusana), true)

	var koko uint32

	var linkerTiedosto []byte = ([]byte)("LINKER")
	koko = GetTiedostoKoko(linkerTiedosto)
	linkeraddress := muistimanager.Varaa_muistia(koko)
	linkerdata := GettavualähteestäOsoitin(uintptr(linkeraddress), int(koko), int(koko))
	Lue_tiedosto(linkerTiedosto, linkerdata)

	elf0 := Elf{}
	linkerhakusana := elf0.Gethakusana(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SivuKansiohakusana))

	linkkimap := Linkkimap{}
	linkkimap.Init(muistimanager)

	var lib1Tiedosto []byte = ([]byte)("LIB1")
	koko = GetTiedostoKoko(lib1Tiedosto)

	lib1address := muistimanager.Varaa_muistia(koko)
	lib1data := GettavualähteestäOsoitin(uintptr(lib1address), int(koko), int(koko))
	Lue_tiedosto(lib1Tiedosto, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SivuKansiohakusana))
	muistimanager.Vapaana(lib1address)

	linkkimap.Lisää_listan_loppuun(uintptr(lib1elf.Dynaaminen))

	var lib2Tiedosto []byte = ([]byte)("LIB2")
	koko = GetTiedostoKoko(lib2Tiedosto)

	lib2address := muistimanager.Varaa_muistia(koko)
	lib2data := GettavualähteestäOsoitin(uintptr(lib2address), int(koko), int(koko))
	Lue_tiedosto(lib2Tiedosto, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SivuKansiohakusana))
	muistimanager.Vapaana(lib2address)

	linkkimap.Lisää_listan_loppuun(uintptr(lib2elf.Dynaaminen))

	libLinkkimap := linkkimap.Clone()
	linkkimapaddress := uint32(uintptr(Pointer(libLinkkimap.First)))

	lib1got := Getunsignedinteger32TaulukkolähteestäOsoitin(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = linkkimapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TaulukkolähteestäOsoitin(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = linkkimapaddress
	lib2got[2] = 0x4000000

	konsoli.MTulostaxy("lib1: ", 1, 8)
	konsoli.MUnsignedinteger32Tulosta(lib1elf.Got)
	konsoli.MTulosta(":")
	konsoli.MUnsignedinteger32Tulosta(lib1elf.Dynaaminen)

	konsoli.MTulostaxy("lib2: ", 1, 9)
	konsoli.MUnsignedinteger32Tulosta(lib2elf.Got)
	konsoli.MTulosta(":")
	konsoli.MUnsignedinteger32Tulosta(lib2elf.Dynaaminen)

	var käyttäjä1Tiedosto []byte = ([]byte)("USER1")
	koko = GetTiedostoKoko(käyttäjä1Tiedosto)
	käyttäjä1address := muistimanager.Varaa_muistia(koko)
	käyttäjä1data := GettavualähteestäOsoitin(uintptr(käyttäjä1address), int(koko), int(koko))
	Lue_tiedosto(käyttäjä1Tiedosto, käyttäjä1data)

	elf2 := Elf{}

	käyttäjä1hakusana := elf2.Gethakusana(käyttäjä1data)
	elf2.Parse(käyttäjä1data[:], uint32(SivuKansiohakusana+0x1000))
	globaalissaoffsetTaulukko := elf2.Got

	PArvo1Linkkimap := linkkimap.Clone()
	PArvo1Linkkimap.Lisää_listan_loppuun(uintptr(elf2.Dynaaminen))

	muistimanager.Vapaana(käyttäjä1address)

	var code1Osoitin *uintptr
	var func1val func()

	code1Osoitin = (*uintptr)(muistimanager.Varaa_muistia(4))
	*code1Osoitin = uintptr(linkerhakusana)
	func1val = *(*func())(Pointer(&code1Osoitin))

	proc2 := prosessihelper.Spawn(func1val, threadhelper, sche, uint32(SivuKansiohakusana+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuTila.Ecx = käyttäjä1hakusana
	thr2.CpuTila.Edx = globaalissaoffsetTaulukko
	thr2.CpuTila.Esi = uint32(uintptr(Pointer(PArvo1Linkkimap.First)))

	konsoli.MTulostaxy("user1: ", 1, 10)
	konsoli.MUnsignedinteger32Tulosta(elf2.Got)

	var käyttäjä2Tiedosto []byte = ([]byte)("USER2")
	koko = GetTiedostoKoko(käyttäjä2Tiedosto)
	käyttäjä2address := muistimanager.Varaa_muistia(koko)
	käyttäjä2data := GettavualähteestäOsoitin(uintptr(käyttäjä2address), int(koko), int(koko))
	Lue_tiedosto(käyttäjä2Tiedosto, käyttäjä2data)

	elf3 := Elf{}

	käyttäjä2hakusana := elf3.Gethakusana(käyttäjä2data)
	elf3.Parse(käyttäjä2data[:], uint32(SivuKansiohakusana+0x2000))
	globaalissaoffsetTaulukko = elf3.Got

	PArvo2Linkkimap := linkkimap.Clone()
	PArvo2Linkkimap.Lisää_listan_loppuun(uintptr(elf3.Dynaaminen))

	muistimanager.Vapaana(käyttäjä2address)

	var code2Osoitin *uintptr
	var func2val func()

	code2Osoitin = (*uintptr)(muistimanager.Varaa_muistia(4))
	*code2Osoitin = uintptr(linkerhakusana)
	func2val = *(*func())(Pointer(&code2Osoitin))

	proc3 := prosessihelper.Spawn(func2val, threadhelper, sche, uint32(SivuKansiohakusana+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuTila.Ecx = käyttäjä2hakusana
	thr3.CpuTila.Edx = globaalissaoffsetTaulukko
	thr3.CpuTila.Esi = uint32(uintptr(Pointer(PArvo2Linkkimap.First)))

	konsoli.MTulostaxy("user2: ", 1, 11)
	konsoli.MUnsignedinteger32Tulosta(thr3.CpuTila.Esi)

	libLinkkimap.Tulosta(1, 11)

	var käyttäjä3Tiedosto []byte = ([]byte)("USER3")
	koko = GetTiedostoKoko(käyttäjä3Tiedosto)
	käyttäjä3address := muistimanager.Varaa_muistia(koko)
	käyttäjä3data := GettavualähteestäOsoitin(uintptr(käyttäjä3address), int(koko), int(koko))
	Lue_tiedosto(käyttäjä3Tiedosto, käyttäjä3data)

	elf4 := Elf{}

	käyttäjä3hakusana := elf4.Gethakusana(käyttäjä3data)
	elf4.Parse(käyttäjä3data[:], uint32(SivuKansiohakusana+0x3000))
	globaalissaoffsetTaulukko = elf4.Got

	PArvo3Linkkimap := linkkimap.Clone()
	PArvo3Linkkimap.Lisää_listan_loppuun(uintptr(elf4.Dynaaminen))

	muistimanager.Vapaana(käyttäjä3address)

	var code3Osoitin *uintptr
	var func3val func()

	code3Osoitin = (*uintptr)(muistimanager.Varaa_muistia(4))
	*code3Osoitin = uintptr(linkerhakusana)
	func3val = *(*func())(Pointer(&code3Osoitin))

	proc4 := prosessihelper.Spawn(func3val, threadhelper, sche, uint32(SivuKansiohakusana+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuTila.Ecx = käyttäjä3hakusana
	thr4.CpuTila.Edx = globaalissaoffsetTaulukko
	thr4.CpuTila.Esi = uint32(uintptr(Pointer(PArvo3Linkkimap.First)))

	prosessihelper.Spawn(TFunktio1, threadhelper, sche, uint32(SivuKansiohakusana+0x4000), true)

	iNäppäimistöTapahtumahandler = &myNäppäimistöTapahtumahandler
	näppäimistödriver.Initdriver(Keskeytysmanager, iNäppäimistöTapahtumahandler)

	hiiridriver.Initdriver(Keskeytysmanager, nil)

	mypciOhjainhandler := TMypciOhjainhandler{}
	pciOhjain.Init(mypciOhjainhandler)
	pciOhjain.Valitsedriver(&Drivermanager, Keskeytysmanager)
	laitedescriptor = mypciOhjainhandler.Getdriver()

	sche.Käytössä(true)
	Keskeytysmanager.Aktiivinen()

	for {
		halt()
	}

}
