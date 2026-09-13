package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "hilfswerkzeug"
import . "gdt"
import . "konsole"
import . "unterbrechung"
import . "mehrfachAufgabenverwaltung"
import . "aufgabenverwaltung/tss"

import . "virtuellSpeicher"
import . "seitenverwaltung"
import . "aufgabenverwaltung/ausführungsfaden"
import . "aufgabenverwaltung/planer"
import . "aufgabenverwaltung/prozess"
import . "treiber/treiber"

import . "treiber/tastatur"
import . "treiber/zeigegerät"

import . "treiber/ata"
import . "dateiSystem/msdosPartition"
import . "dateiSystem/fat"

import . "dateiSystem/ausführbares_und_bindbares_Format"

import . "systemAufruf"

import . "speicherVerwalter"
import . "pci"

func halt()

var iTastaturEreignishandler ITastaturEreignishandler

type TMyTastaturEreignishandler struct {
}

var myTastaturEreignishandler TMyTastaturEreignishandler
var tastaturTreiber TTastaturTreiber
var mausTreiber TMausTreiber
var pciSteuerung TPeripheralcomponentinterconnectSteuerung

var tastaturKonsole TKonsole = TKonsole{}

func (selbst *TMyTastaturEreignishandler) BeiSchlüsselAbwärts(schlüssel byte) {
	foo := [1]byte{' '}
	foo[0] = schlüssel

	tastaturKonsole.MDruckenBytexy(foo[:], 1000, 1000)
}

func (selbst *TMyTastaturEreignishandler) BeiSchlüsselAufwärts(schlüssel byte)	{}

var iMausEreignishandler IMausEreignishandler

type TMyMausEreignishandler struct {
}

var mausKonsole TKonsole = TKonsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (selbst *TMyMausEreignishandler) BeiMausAbwärts(knopf int8) {
	buffer := []byte("x")
	mausKonsole.MDruckenxy(buffer, uint16(previousx), uint16(previousy))
}
func (selbst *TMyMausEreignishandler) BeiMausAufwärts(knopf int8)	{}
func (selbst *TMyMausEreignishandler) BeiMausVerschieben(x int8, y int8) {

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
	mausKonsole.MDruckenxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mausKonsole.MDruckenxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var gerätdescriptor TPeripheralcomponentinterconnectGerätdescriptor
var ipciSteuerunghandler IpciSteuerunghandler

type TMypciSteuerunghandler struct {
}

var konsole TKonsole = TKonsole{}
var treiberAnzahl uint16 = 0

func (selbst TMypciSteuerunghandler) BeigetTreiber(gerät TPeripheralcomponentinterconnectGerätdescriptor) {
	if gerät.HerstellerKennung == 0x1022 && gerät.GerätKennung == 0x2000 {
		konsole.MDruckenxy([]byte("["), 0, 12)
		konsole.MDrucken(([]byte)("AMD am79c973"))
		konsole.MDrucken([]byte(":"))
		konsole.MUnsignedinteger16Drucken(gerät.HerstellerKennung)
		konsole.MDrucken([]byte(":"))
		konsole.MUnsignedinteger16Drucken(gerät.GerätKennung)
		konsole.MDrucken([]byte(":"))
		konsole.MUnsignedinteger16Drucken(uint16(gerät.Anschlussbase))
		konsole.MDrucken([]byte(":"))
		konsole.MUnsignedinteger32Drucken(gerät.Unterbrechung)

		konsole.MDrucken([]byte("]\n"))
		gerätdescriptor = gerät
		treiberAnzahl++
	}
}
func (selbst TMypciSteuerunghandler) GetTreiber() TPeripheralcomponentinterconnectGerätdescriptor {
	return gerätdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Druckenstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsole.MDrucken(str)
}

func GetDateiGröße(dateiname []byte) uint32 {
	var ata0s = TErweitertTechnikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdosPartitionTabelle{}
	partition.LesenPartition(&ata0s)

	bios := TDateisystemparameter32{}

	var größe uint32 = bios.Len(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname)
	ata0s.Flush()

	return größe
}

func Datei_lesen(dateiname []byte, daten []byte) {
	var ata0s = TErweitertTechnikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdosPartitionTabelle{}
	partition.LesenPartition(&ata0s)

	bios := TDateisystemparameter32{}
	bios.Lesen(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname, daten)

	ata0s.Flush()
}
func Ladenelf() {

	var ata0s = TErweitertTechnikattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdosPartitionTabelle{}
	partition.LesenPartition(&ata0s)

	bios := TDateisystemparameter32{}

	var dateiname []byte = ([]byte)("TEST")
	var größe uint32 = bios.Len(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname)
	var datenbuffer [100 * 1024]byte
	var daten []byte = datenbuffer[:]
	bios.Lesen(&ata0s, partition.Mbr.PrimaryPartition[0], dateiname, daten)

	ausführbares_und_bindbares_Format := Elf{}

	ausführbares_und_bindbares_Format.Parse(daten[:größe], 0x4f00000)

}

var aufgabeKonsole TKonsole = TKonsole{}

func TFunktion1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func aufgabea() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func aufgabeb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func aufgabec() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func aufgabed()

func aufgabed0() {
	esi := getesi()
	for {

		SysDruckenunsignedinteger32(esi)

	}
}

func aufgabed1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func eingabeEreignisAufgabe() {
	for {
		ProzessausstehendTastaturEreignisse()
		ProzessausstehendMausEreignisse()
		halt()
	}
}

func memorytest(y int) {
	speicherVerwalter := &TSpeicherVerwalter{}
	allocated := uint32(uintptr(speicherVerwalter.Speicher_reservieren(1024)))
	konsole.MUnsignedinteger32Druckenxy(allocated, 10, uint16(y))
	if y == 11 {
		speicherVerwalter.Frei(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func AnhaltenSchleife()
func Neuladencr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Setzencr3(cr3 uint32)
func Getcr4() uint32
func AktivierenSeitenverwaltung()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunktionElementname(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcElementname = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcElementname)

	aufgabeKonsole.MDruckenxy(funcByte, 1, 5)
	aufgabeKonsole.MDrucken(([]byte)(":"))
	aufgabeKonsole.MUnsignedinteger32Drucken(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	aufgabeKonsole.MDruckenunsignedinteger32(cr0, 2, 1)
}

var tss *TssEintrag = &TssEintrag{}

func KKernelEntry(SeiteOrdnerEintrag uintptr, stacktop uintptr, stackbottom uintptr) {

	MSeriellProtokollinit()
	konsole.MDrucken("\n=== LIE BOOT ===\n")

	konsole.MDruckenunsignedinteger32(uint32(SeiteOrdnerEintrag), 0, 2)
	konsole.MDruckenunsignedinteger32(uint32(SeiteOrdnerEintrag), 10, 2)
	konsole.MDruckenunsignedinteger32(uint32(stacktop), 0, 3)
	konsole.MDruckenunsignedinteger32(uint32(stackbottom), 10, 3)

	speicherVerwalter := &TSpeicherVerwalter{}
	speicherVerwalter.Init(0, MaximumWarteschlangeGröße)

	seitenverwaltung := &Seitenverwaltung{}
	seitenverwaltung.Init(SeiteOrdnerEintrag, 0x500000, speicherVerwalter)
	seitenverwaltung.SharedSpeicherregion()

	Setzencr3(uint32(SeiteOrdnerEintrag))
	AktivierenSeitenverwaltung()

	shareddescriptorTabelle := &TShareddescriptorTabelle{}
	shareddescriptorTabelle.Init()

	konsole.MDrucken("esp:")

	esp := getesp()
	konsole.MUnsignedinteger32Drucken(uint32(esp))

	tls := gettls()
	konsole.MDrucken(([]byte)("tls:"))
	konsole.MUnsignedinteger32Drucken(tls)

	tss.Installieren(shareddescriptorTabelle, 7, SegKernDaten, esp)

	VirtTesten()

	cr3 := Neuladencr3()
	konsole.MDrucken(([]byte)(":cr3:"))
	konsole.MUnsignedinteger32Drucken(cr3)

	cr0 := Getcr0()
	konsole.MDrucken(([]byte)(":cr0:"))
	konsole.MUnsignedinteger32Drucken(cr0)

	cr4 := Getcr4()
	konsole.MDrucken(([]byte)(":cr4:"))
	konsole.MUnsignedinteger32Drucken(cr4)

	aufgabeVerwalter_2 := &TAufgabeVerwalter{}
	aufgabeVerwalter_2.Init()

	UnterbrechungVerwalter := &TUnterbrechungVerwalter{}
	UnterbrechungVerwalter.Init(0x20, shareddescriptorTabelle, aufgabeVerwalter_2)

	seitenverwaltung.SeiteFehler(UnterbrechungVerwalter)

	TreiberVerwalter := TTreiberVerwalter{}
	TreiberVerwalter.Init()

	ausführungsfadenhelper := &TAusführungsfadenhelper{}
	ausführungsfadenhelper.Init(speicherVerwalter)

	prozesshelper := Prozesshelper{}
	prozesshelper.Init(speicherVerwalter, SeiteOrdnerEintrag)

	sche := &Planer{}
	sche.Init(UnterbrechungVerwalter, speicherVerwalter, tss)

	sysAufruf := &TSyscall{}
	sysAufruf.Init(UnterbrechungVerwalter)

	prozesshelper.Spawn(aufgabea, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag), true)
	prozesshelper.Spawn(aufgabeb, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag), true)
	prozesshelper.Spawn(aufgabec, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag), true)
	prozesshelper.Spawn(aufgabed1, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag), true)
	prozesshelper.Spawn(eingabeEreignisAufgabe, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag), true)

	var größe uint32

	var linkerDatei []byte = ([]byte)("LINKER")
	größe = GetDateiGröße(linkerDatei)
	linkeraddress := speicherVerwalter.Speicher_reservieren(größe)
	linkerDaten := GetBytevonZeiger(uintptr(linkeraddress), int(größe), int(größe))
	Datei_lesen(linkerDatei, linkerDaten)

	elf0 := Elf{}
	linkerEintrag := elf0.GetEintrag(linkerDaten)
	elf0.Parse(linkerDaten[:], uint32(SeiteOrdnerEintrag))

	verknüpfungAbbildung := VerknüpfungAbbildung{}
	verknüpfungAbbildung.Init(speicherVerwalter)

	var lib1Datei []byte = ([]byte)("LIB1")
	größe = GetDateiGröße(lib1Datei)

	lib1address := speicherVerwalter.Speicher_reservieren(größe)
	lib1Daten := GetBytevonZeiger(uintptr(lib1address), int(größe), int(größe))
	Datei_lesen(lib1Datei, lib1Daten)

	lib1elf := Elf{}
	lib1elf.Parse(lib1Daten[:], uint32(SeiteOrdnerEintrag))
	speicherVerwalter.Frei(lib1address)

	verknüpfungAbbildung.Am_Listenende_anfügen(uintptr(lib1elf.Dynamisch))

	var lib2Datei []byte = ([]byte)("LIB2")
	größe = GetDateiGröße(lib2Datei)

	lib2address := speicherVerwalter.Speicher_reservieren(größe)
	lib2Daten := GetBytevonZeiger(uintptr(lib2address), int(größe), int(größe))
	Datei_lesen(lib2Datei, lib2Daten)

	lib2elf := Elf{}
	lib2elf.Parse(lib2Daten[:], uint32(SeiteOrdnerEintrag))
	speicherVerwalter.Frei(lib2address)

	verknüpfungAbbildung.Am_Listenende_anfügen(uintptr(lib2elf.Dynamisch))

	libVerknüpfungAbbildung := verknüpfungAbbildung.Clone()
	verknüpfungAbbildungaddress := uint32(uintptr(Pointer(libVerknüpfungAbbildung.First)))

	lib1got := Getunsignedinteger32FeldvonZeiger(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = verknüpfungAbbildungaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32FeldvonZeiger(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = verknüpfungAbbildungaddress
	lib2got[2] = 0x4000000

	konsole.MDruckenxy("lib1: ", 1, 8)
	konsole.MUnsignedinteger32Drucken(lib1elf.Got)
	konsole.MDrucken(":")
	konsole.MUnsignedinteger32Drucken(lib1elf.Dynamisch)

	konsole.MDruckenxy("lib2: ", 1, 9)
	konsole.MUnsignedinteger32Drucken(lib2elf.Got)
	konsole.MDrucken(":")
	konsole.MUnsignedinteger32Drucken(lib2elf.Dynamisch)

	var benutzer1Datei []byte = ([]byte)("USER1")
	größe = GetDateiGröße(benutzer1Datei)
	benutzer1address := speicherVerwalter.Speicher_reservieren(größe)
	benutzer1Daten := GetBytevonZeiger(uintptr(benutzer1address), int(größe), int(größe))
	Datei_lesen(benutzer1Datei, benutzer1Daten)

	elf2 := Elf{}

	benutzer1Eintrag := elf2.GetEintrag(benutzer1Daten)
	elf2.Parse(benutzer1Daten[:], uint32(SeiteOrdnerEintrag+0x1000))
	globalVersatzTabelle := elf2.Got

	PWert1VerknüpfungAbbildung := verknüpfungAbbildung.Clone()
	PWert1VerknüpfungAbbildung.Am_Listenende_anfügen(uintptr(elf2.Dynamisch))

	speicherVerwalter.Frei(benutzer1address)

	var code1Zeiger *uintptr
	var func1val func()

	code1Zeiger = (*uintptr)(speicherVerwalter.Speicher_reservieren(4))
	*code1Zeiger = uintptr(linkerEintrag)
	func1val = *(*func())(Pointer(&code1Zeiger))

	proc2 := prozesshelper.Spawn(func1val, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag+0x1000), false)
	thr2 := (*TAusführungsfaden)(proc2.Threads.Getat(0))
	thr2.CpuStatus.Ecx = benutzer1Eintrag
	thr2.CpuStatus.Edx = globalVersatzTabelle
	thr2.CpuStatus.Esi = uint32(uintptr(Pointer(PWert1VerknüpfungAbbildung.First)))

	konsole.MDruckenxy("user1: ", 1, 10)
	konsole.MUnsignedinteger32Drucken(elf2.Got)

	var benutzer2Datei []byte = ([]byte)("USER2")
	größe = GetDateiGröße(benutzer2Datei)
	benutzer2address := speicherVerwalter.Speicher_reservieren(größe)
	benutzer2Daten := GetBytevonZeiger(uintptr(benutzer2address), int(größe), int(größe))
	Datei_lesen(benutzer2Datei, benutzer2Daten)

	elf3 := Elf{}

	benutzer2Eintrag := elf3.GetEintrag(benutzer2Daten)
	elf3.Parse(benutzer2Daten[:], uint32(SeiteOrdnerEintrag+0x2000))
	globalVersatzTabelle = elf3.Got

	PWert2VerknüpfungAbbildung := verknüpfungAbbildung.Clone()
	PWert2VerknüpfungAbbildung.Am_Listenende_anfügen(uintptr(elf3.Dynamisch))

	speicherVerwalter.Frei(benutzer2address)

	var code2Zeiger *uintptr
	var func2val func()

	code2Zeiger = (*uintptr)(speicherVerwalter.Speicher_reservieren(4))
	*code2Zeiger = uintptr(linkerEintrag)
	func2val = *(*func())(Pointer(&code2Zeiger))

	proc3 := prozesshelper.Spawn(func2val, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag+0x2000), false)
	thr3 := (*TAusführungsfaden)(proc3.Threads.Getat(0))
	thr3.CpuStatus.Ecx = benutzer2Eintrag
	thr3.CpuStatus.Edx = globalVersatzTabelle
	thr3.CpuStatus.Esi = uint32(uintptr(Pointer(PWert2VerknüpfungAbbildung.First)))

	konsole.MDruckenxy("user2: ", 1, 11)
	konsole.MUnsignedinteger32Drucken(thr3.CpuStatus.Esi)

	libVerknüpfungAbbildung.Drucken(1, 11)

	var benutzer3Datei []byte = ([]byte)("USER3")
	größe = GetDateiGröße(benutzer3Datei)
	benutzer3address := speicherVerwalter.Speicher_reservieren(größe)
	benutzer3Daten := GetBytevonZeiger(uintptr(benutzer3address), int(größe), int(größe))
	Datei_lesen(benutzer3Datei, benutzer3Daten)

	elf4 := Elf{}

	benutzer3Eintrag := elf4.GetEintrag(benutzer3Daten)
	elf4.Parse(benutzer3Daten[:], uint32(SeiteOrdnerEintrag+0x3000))
	globalVersatzTabelle = elf4.Got

	PWert3VerknüpfungAbbildung := verknüpfungAbbildung.Clone()
	PWert3VerknüpfungAbbildung.Am_Listenende_anfügen(uintptr(elf4.Dynamisch))

	speicherVerwalter.Frei(benutzer3address)

	var code3Zeiger *uintptr
	var func3val func()

	code3Zeiger = (*uintptr)(speicherVerwalter.Speicher_reservieren(4))
	*code3Zeiger = uintptr(linkerEintrag)
	func3val = *(*func())(Pointer(&code3Zeiger))

	proc4 := prozesshelper.Spawn(func3val, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag+0x3000), false)
	thr4 := (*TAusführungsfaden)(proc4.Threads.Getat(0))
	thr4.CpuStatus.Ecx = benutzer3Eintrag
	thr4.CpuStatus.Edx = globalVersatzTabelle
	thr4.CpuStatus.Esi = uint32(uintptr(Pointer(PWert3VerknüpfungAbbildung.First)))

	prozesshelper.Spawn(TFunktion1, ausführungsfadenhelper, sche, uint32(SeiteOrdnerEintrag+0x4000), true)

	iTastaturEreignishandler = &myTastaturEreignishandler
	tastaturTreiber.InitTreiber(UnterbrechungVerwalter, iTastaturEreignishandler)

	mausTreiber.InitTreiber(UnterbrechungVerwalter, nil)

	mypciSteuerunghandler := TMypciSteuerunghandler{}
	pciSteuerung.Init(mypciSteuerunghandler)
	pciSteuerung.AuswählenTreiber(&TreiberVerwalter, UnterbrechungVerwalter)
	gerätdescriptor = mypciSteuerunghandler.GetTreiber()

	sche.Aktiviert(true)
	UnterbrechungVerwalter.Aktiv()

	for {
		halt()
	}

}
