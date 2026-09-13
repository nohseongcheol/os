package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsola"
import . "przerwanie"
import . "multitasking"
import . "tasking/tss"

import . "wirtualnePamięć"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/klawiatura"
import . "driver/urządzenie_wskazujące"

import . "driver/ata"
import . "plikSystemowe/msdospartition"
import . "plikSystemowe/fat"

import . "plikSystemowe/format_wykonywalny_i_konsolidowalny"

import . "systemowecall"

import . "pamięćmanager"
import . "pci"

func halt()

var iKlawiaturaWydarzeniehandler IKlawiaturaWydarzeniehandler

type TMyKlawiaturaWydarzeniehandler struct {
}

var myKlawiaturaWydarzeniehandler TMyKlawiaturaWydarzeniehandler
var klawiaturadriver TKlawiaturadriver
var myszdriver TMyszdriver
var pciKontroler TPeripheralcomponentinterconnectKontroler

var klawiaturaKonsola TKonsola = TKonsola{}

func (bieżący *TMyKlawiaturaWydarzeniehandler) WłączKluczWdół(klucz byte) {
	foo := [1]byte{' '}
	foo[0] = klucz

	klawiaturaKonsola.MWydrukujBajtyxy(foo[:], 1000, 1000)
}

func (bieżący *TMyKlawiaturaWydarzeniehandler) WłączKluczGóra(klucz byte)	{}

var iMyszWydarzeniehandler IMyszWydarzeniehandler

type TMyMyszWydarzeniehandler struct {
}

var myszKonsola TKonsola = TKonsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPozycja int16 = 0
var yPozycja int16 = 0

func (bieżący *TMyMyszWydarzeniehandler) WłączMyszWdół(przycisk int8) {
	buffer := []byte("x")
	myszKonsola.MWydrukujxy(buffer, uint16(previousx), uint16(previousy))
}
func (bieżący *TMyMyszWydarzeniehandler) WłączMyszGóra(przycisk int8)	{}
func (bieżący *TMyMyszWydarzeniehandler) WłączMyszPrzenoszenie(x int8, y int8) {

	xPozycja += int16(x)
	if xPozycja < 0 {
		xPozycja = 0
	}
	if xPozycja >= 80 {
		xPozycja = 79
	}

	yPozycja -= int16(y)

	if yPozycja < 0 {
		yPozycja = 0
	}
	if yPozycja >= 25 {
		yPozycja = 24
	}

	buffer := []byte(" ")
	myszKonsola.MWydrukujxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	myszKonsola.MWydrukujxy(buffer, uint16(xPozycja), uint16(yPozycja))

	previousx = xPozycja
	previousy = yPozycja
}

var urządzeniedescriptor TPeripheralcomponentinterconnectUrządzeniedescriptor
var ipciKontrolerhandler IpciKontrolerhandler

type TMypciKontrolerhandler struct {
}

var konsola TKonsola = TKonsola{}
var driverLiczba uint16 = 0

func (bieżący TMypciKontrolerhandler) Włączgetdriver(urządzenie TPeripheralcomponentinterconnectUrządzeniedescriptor) {
	if urządzenie.DostawcaIdentyfikator == 0x1022 && urządzenie.UrządzenieIdentyfikator == 0x2000 {
		konsola.MWydrukujxy([]byte("["), 0, 12)
		konsola.MWydrukuj(([]byte)("AMD am79c973"))
		konsola.MWydrukuj([]byte(":"))
		konsola.MUnsignedinteger16Wydrukuj(urządzenie.DostawcaIdentyfikator)
		konsola.MWydrukuj([]byte(":"))
		konsola.MUnsignedinteger16Wydrukuj(urządzenie.UrządzenieIdentyfikator)
		konsola.MWydrukuj([]byte(":"))
		konsola.MUnsignedinteger16Wydrukuj(uint16(urządzenie.Portbase))
		konsola.MWydrukuj([]byte(":"))
		konsola.MUnsignedinteger32Wydrukuj(urządzenie.Przerwanie)

		konsola.MWydrukuj([]byte("]\n"))
		urządzeniedescriptor = urządzenie
		driverLiczba++
	}
}
func (bieżący TMypciKontrolerhandler) Getdriver() TPeripheralcomponentinterconnectUrządzeniedescriptor {
	return urządzeniedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Wydrukujstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsola.MWydrukuj(str)
}

func GetPlikRozmiar(nazwapliku []byte) uint32 {
	var ata0s = TZaawansowaneTechnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Odczytpartition(&ata0s)

	bios := TParametry_systemu_plików32{}

	var rozmiar uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku)
	ata0s.Flush()

	return rozmiar
}

func Odczytaj_plik(nazwapliku []byte, data []byte) {
	var ata0s = TZaawansowaneTechnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Odczytpartition(&ata0s)

	bios := TParametry_systemu_plików32{}
	bios.Odczyt(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku, data)

	ata0s.Flush()
}
func Obciążenieelf() {

	var ata0s = TZaawansowaneTechnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Odczytpartition(&ata0s)

	bios := TParametry_systemu_plików32{}

	var nazwapliku []byte = ([]byte)("TEST")
	var rozmiar uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Odczyt(&ata0s, partition.Mbr.Primarypartition[0], nazwapliku, data)

	format_wykonywalny_i_konsolidowalny := Elf{}

	format_wykonywalny_i_konsolidowalny.Parse(data[:rozmiar], 0x4f00000)

}

var zadanieKonsola TKonsola = TKonsola{}

func TFunkcja1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func zadaniea() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func zadanieb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func zadaniec() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func zadanied()

func zadanied0() {
	esi := getesi()
	for {

		SysWydrukujunsignedinteger32(esi)

	}
}

func zadanied1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func wejścieWydarzenieZadanie() {
	for {
		ProcespendingKlawiaturaWydarzenia()
		ProcespendingMyszWydarzenia()
		halt()
	}
}

func memorytest(y int) {
	pamięćmanager := &TPamięćmanager{}
	allocated := uint32(uintptr(pamięćmanager.Przydziel_pamięć(1024)))
	konsola.MUnsignedinteger32Wydrukujxy(allocated, 10, uint16(y))
	if y == 11 {
		pamięćmanager.Wolne(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Wstrzymajloop()
func Wczytajponowniecr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Zbiórcr3(cr3 uint32)
func Getcr4() uint32
func Włączpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcjaNazwa(i interface{}) {
	var adres = reflect.ValueOf(i).Pointer()
	var funcNazwa = runtime.FuncForPC(adres).Name()
	var funcBajty []byte = []byte(funcNazwa)

	zadanieKonsola.MWydrukujxy(funcBajty, 1, 5)
	zadanieKonsola.MWydrukuj(([]byte)(":"))
	zadanieKonsola.MUnsignedinteger32Wydrukuj(uint32(uintptr(adres)))
}

func printreg() {
	cr0 := Getcr0()
	zadanieKonsola.MWydrukujunsignedinteger32(cr0, 2, 1)
}

var tss *Tsswpis = &Tsswpis{}

func KKernelEntry(StronaKatalogwpis uintptr, stacktop uintptr, stackbottom uintptr) {

	MSzeregowoDziennikinit()
	konsola.MWydrukuj("\n=== POL BOOT ===\n")

	konsola.MWydrukujunsignedinteger32(uint32(StronaKatalogwpis), 0, 2)
	konsola.MWydrukujunsignedinteger32(uint32(StronaKatalogwpis), 10, 2)
	konsola.MWydrukujunsignedinteger32(uint32(stacktop), 0, 3)
	konsola.MWydrukujunsignedinteger32(uint32(stackbottom), 10, 3)

	pamięćmanager := &TPamięćmanager{}
	pamięćmanager.Init(0, MaksymalnaqueueRozmiar)

	paging := &Paging{}
	paging.Init(StronaKatalogwpis, 0x500000, pamięćmanager)
	paging.SharedPamięćregion()

	Zbiórcr3(uint32(StronaKatalogwpis))
	Włączpaging()

	shareddescriptorTabela := &TShareddescriptorTabela{}
	shareddescriptorTabela.Init()

	konsola.MWydrukuj("esp:")

	esp := getesp()
	konsola.MUnsignedinteger32Wydrukuj(uint32(esp))

	tls := gettls()
	konsola.MWydrukuj(([]byte)("tls:"))
	konsola.MUnsignedinteger32Wydrukuj(tls)

	tss.Instalacja(shareddescriptorTabela, 7, Segkerneldata, esp)

	VirtPrzetestuj()

	cr3 := Wczytajponowniecr3()
	konsola.MWydrukuj(([]byte)(":cr3:"))
	konsola.MUnsignedinteger32Wydrukuj(cr3)

	cr0 := Getcr0()
	konsola.MWydrukuj(([]byte)(":cr0:"))
	konsola.MUnsignedinteger32Wydrukuj(cr0)

	cr4 := Getcr4()
	konsola.MWydrukuj(([]byte)(":cr4:"))
	konsola.MUnsignedinteger32Wydrukuj(cr4)

	zadaniemanager_2 := &TZadaniemanager{}
	zadaniemanager_2.Init()

	Przerwaniemanager := &TPrzerwaniemanager{}
	Przerwaniemanager.Init(0x20, shareddescriptorTabela, zadaniemanager_2)

	paging.Stronafault(Przerwaniemanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(pamięćmanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(pamięćmanager, StronaKatalogwpis)

	sche := &Scheduler{}
	sche.Init(Przerwaniemanager, pamięćmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Przerwaniemanager)

	proceshelper.Spawn(zadaniea, threadhelper, sche, uint32(StronaKatalogwpis), true)
	proceshelper.Spawn(zadanieb, threadhelper, sche, uint32(StronaKatalogwpis), true)
	proceshelper.Spawn(zadaniec, threadhelper, sche, uint32(StronaKatalogwpis), true)
	proceshelper.Spawn(zadanied1, threadhelper, sche, uint32(StronaKatalogwpis), true)
	proceshelper.Spawn(wejścieWydarzenieZadanie, threadhelper, sche, uint32(StronaKatalogwpis), true)

	var rozmiar uint32

	var linkerPlik []byte = ([]byte)("LINKER")
	rozmiar = GetPlikRozmiar(linkerPlik)
	linkerAdres := pamięćmanager.Przydziel_pamięć(rozmiar)
	linkerdata := GetBajtyzKursor(uintptr(linkerAdres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(linkerPlik, linkerdata)

	elf0 := Elf{}
	linkerwpis := elf0.Getwpis(linkerdata)
	elf0.Parse(linkerdata[:], uint32(StronaKatalogwpis))

	odnośnikmap := Odnośnikmap{}
	odnośnikmap.Init(pamięćmanager)

	var lib1Plik []byte = ([]byte)("LIB1")
	rozmiar = GetPlikRozmiar(lib1Plik)

	lib1Adres := pamięćmanager.Przydziel_pamięć(rozmiar)
	lib1data := GetBajtyzKursor(uintptr(lib1Adres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(lib1Plik, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(StronaKatalogwpis))
	pamięćmanager.Wolne(lib1Adres)

	odnośnikmap.Dodaj_na_końcu_listy(uintptr(lib1elf.Dynamicznie))

	var lib2Plik []byte = ([]byte)("LIB2")
	rozmiar = GetPlikRozmiar(lib2Plik)

	lib2Adres := pamięćmanager.Przydziel_pamięć(rozmiar)
	lib2data := GetBajtyzKursor(uintptr(lib2Adres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(lib2Plik, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(StronaKatalogwpis))
	pamięćmanager.Wolne(lib2Adres)

	odnośnikmap.Dodaj_na_końcu_listy(uintptr(lib2elf.Dynamicznie))

	libOdnośnikmap := odnośnikmap.Clone()
	odnośnikmapAdres := uint32(uintptr(Pointer(libOdnośnikmap.First)))

	lib1got := Getunsignedinteger32TablicazKursor(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = odnośnikmapAdres
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TablicazKursor(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = odnośnikmapAdres
	lib2got[2] = 0x4000000

	konsola.MWydrukujxy("lib1: ", 1, 8)
	konsola.MUnsignedinteger32Wydrukuj(lib1elf.Got)
	konsola.MWydrukuj(":")
	konsola.MUnsignedinteger32Wydrukuj(lib1elf.Dynamicznie)

	konsola.MWydrukujxy("lib2: ", 1, 9)
	konsola.MUnsignedinteger32Wydrukuj(lib2elf.Got)
	konsola.MWydrukuj(":")
	konsola.MUnsignedinteger32Wydrukuj(lib2elf.Dynamicznie)

	var użytkownik1Plik []byte = ([]byte)("USER1")
	rozmiar = GetPlikRozmiar(użytkownik1Plik)
	użytkownik1Adres := pamięćmanager.Przydziel_pamięć(rozmiar)
	użytkownik1data := GetBajtyzKursor(uintptr(użytkownik1Adres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(użytkownik1Plik, użytkownik1data)

	elf2 := Elf{}

	użytkownik1wpis := elf2.Getwpis(użytkownik1data)
	elf2.Parse(użytkownik1data[:], uint32(StronaKatalogwpis+0x1000))
	globalnyPrzesunięcieTabela := elf2.Got

	PWartość1Odnośnikmap := odnośnikmap.Clone()
	PWartość1Odnośnikmap.Dodaj_na_końcu_listy(uintptr(elf2.Dynamicznie))

	pamięćmanager.Wolne(użytkownik1Adres)

	var code1Kursor *uintptr
	var func1val func()

	code1Kursor = (*uintptr)(pamięćmanager.Przydziel_pamięć(4))
	*code1Kursor = uintptr(linkerwpis)
	func1val = *(*func())(Pointer(&code1Kursor))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(StronaKatalogwpis+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProcesorStan.Ecx = użytkownik1wpis
	thr2.ProcesorStan.Edx = globalnyPrzesunięcieTabela
	thr2.ProcesorStan.Esi = uint32(uintptr(Pointer(PWartość1Odnośnikmap.First)))

	konsola.MWydrukujxy("user1: ", 1, 10)
	konsola.MUnsignedinteger32Wydrukuj(elf2.Got)

	var użytkownik2Plik []byte = ([]byte)("USER2")
	rozmiar = GetPlikRozmiar(użytkownik2Plik)
	użytkownik2Adres := pamięćmanager.Przydziel_pamięć(rozmiar)
	użytkownik2data := GetBajtyzKursor(uintptr(użytkownik2Adres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(użytkownik2Plik, użytkownik2data)

	elf3 := Elf{}

	użytkownik2wpis := elf3.Getwpis(użytkownik2data)
	elf3.Parse(użytkownik2data[:], uint32(StronaKatalogwpis+0x2000))
	globalnyPrzesunięcieTabela = elf3.Got

	PWartość2Odnośnikmap := odnośnikmap.Clone()
	PWartość2Odnośnikmap.Dodaj_na_końcu_listy(uintptr(elf3.Dynamicznie))

	pamięćmanager.Wolne(użytkownik2Adres)

	var code2Kursor *uintptr
	var func2val func()

	code2Kursor = (*uintptr)(pamięćmanager.Przydziel_pamięć(4))
	*code2Kursor = uintptr(linkerwpis)
	func2val = *(*func())(Pointer(&code2Kursor))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(StronaKatalogwpis+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProcesorStan.Ecx = użytkownik2wpis
	thr3.ProcesorStan.Edx = globalnyPrzesunięcieTabela
	thr3.ProcesorStan.Esi = uint32(uintptr(Pointer(PWartość2Odnośnikmap.First)))

	konsola.MWydrukujxy("user2: ", 1, 11)
	konsola.MUnsignedinteger32Wydrukuj(thr3.ProcesorStan.Esi)

	libOdnośnikmap.Wydrukuj(1, 11)

	var użytkownik3Plik []byte = ([]byte)("USER3")
	rozmiar = GetPlikRozmiar(użytkownik3Plik)
	użytkownik3Adres := pamięćmanager.Przydziel_pamięć(rozmiar)
	użytkownik3data := GetBajtyzKursor(uintptr(użytkownik3Adres), int(rozmiar), int(rozmiar))
	Odczytaj_plik(użytkownik3Plik, użytkownik3data)

	elf4 := Elf{}

	użytkownik3wpis := elf4.Getwpis(użytkownik3data)
	elf4.Parse(użytkownik3data[:], uint32(StronaKatalogwpis+0x3000))
	globalnyPrzesunięcieTabela = elf4.Got

	PWartość3Odnośnikmap := odnośnikmap.Clone()
	PWartość3Odnośnikmap.Dodaj_na_końcu_listy(uintptr(elf4.Dynamicznie))

	pamięćmanager.Wolne(użytkownik3Adres)

	var code3Kursor *uintptr
	var func3val func()

	code3Kursor = (*uintptr)(pamięćmanager.Przydziel_pamięć(4))
	*code3Kursor = uintptr(linkerwpis)
	func3val = *(*func())(Pointer(&code3Kursor))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(StronaKatalogwpis+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProcesorStan.Ecx = użytkownik3wpis
	thr4.ProcesorStan.Edx = globalnyPrzesunięcieTabela
	thr4.ProcesorStan.Esi = uint32(uintptr(Pointer(PWartość3Odnośnikmap.First)))

	proceshelper.Spawn(TFunkcja1, threadhelper, sche, uint32(StronaKatalogwpis+0x4000), true)

	iKlawiaturaWydarzeniehandler = &myKlawiaturaWydarzeniehandler
	klawiaturadriver.Initdriver(Przerwaniemanager, iKlawiaturaWydarzeniehandler)

	myszdriver.Initdriver(Przerwaniemanager, nil)

	mypciKontrolerhandler := TMypciKontrolerhandler{}
	pciKontroler.Init(mypciKontrolerhandler)
	pciKontroler.Zaznaczdriver(&Drivermanager, Przerwaniemanager)
	urządzeniedescriptor = mypciKontrolerhandler.Getdriver()

	sche.Włączone(true)
	Przerwaniemanager.Aktywne()

	for {
		halt()
	}

}
