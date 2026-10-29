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

import . "virtualeMemoria"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/processi"
import . "driver/driver"

import . "driver/tastiera"
import . "driver/dispositivo_di_puntamento"

import . "driver/ata"
import . "fileSistema/msdospartition"
import . "fileSistema/fat"

import . "fileSistema/formato_eseguibile_e_collegabile"

import . "sistemacall"

import . "memoriamanager"
import . "pci"

func halt()

var iTastieraEventohandler ITastieraEventohandler

type TMyTastieraEventohandler struct {
}

var myTastieraEventohandler TMyTastieraEventohandler
var tastieradriver TTastieradriver
var mousedriver TMousedriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastieraconsole TConsole = TConsole{}

func (séstesso *TMyTastieraEventohandler) AccesoChiaveGiù(chiave byte) {
	foo := [1]byte{' '}
	foo[0] = chiave

	tastieraconsole.MStampaBytexy(foo[:], 1000, 1000)
}

func (séstesso *TMyTastieraEventohandler) AccesoChiaveSu(chiave byte)	{}

var imouseEventohandler IMouseEventohandler

type TMymouseEventohandler struct {
}

var mouseconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosizione int16 = 0
var yPosizione int16 = 0

func (séstesso *TMymouseEventohandler) AccesomouseGiù(pulsante int8) {
	buffer := []byte("x")
	mouseconsole.MStampaxy(buffer, uint16(previousx), uint16(previousy))
}
func (séstesso *TMymouseEventohandler) AccesomouseSu(pulsante int8)	{}
func (séstesso *TMymouseEventohandler) AccesomouseSposta(x int8, y int8) {

	xPosizione += int16(x)
	if xPosizione < 0 {
		xPosizione = 0
	}
	if xPosizione >= 80 {
		xPosizione = 79
	}

	yPosizione -= int16(y)

	if yPosizione < 0 {
		yPosizione = 0
	}
	if yPosizione >= 25 {
		yPosizione = 24
	}

	buffer := []byte(" ")
	mouseconsole.MStampaxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mouseconsole.MStampaxy(buffer, uint16(xPosizione), uint16(yPosizione))

	previousx = xPosizione
	previousy = yPosizione
}

var dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var driverConteggio uint16 = 0

func (séstesso TMypcicontrollerhandler) Accesogetdriver(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
	if dispositivo.Fornitoreid == 0x1022 && dispositivo.Dispositivoid == 0x2000 {
		console.MStampaxy([]byte("["), 0, 12)
		console.MStampa(([]byte)("AMD am79c973"))
		console.MStampa([]byte(":"))
		console.MUnsignedinteger16Stampa(dispositivo.Fornitoreid)
		console.MStampa([]byte(":"))
		console.MUnsignedinteger16Stampa(dispositivo.Dispositivoid)
		console.MStampa([]byte(":"))
		console.MUnsignedinteger16Stampa(uint16(dispositivo.Portabase))
		console.MStampa([]byte(":"))
		console.MUnsignedinteger32Stampa(dispositivo.Interrupt)

		console.MStampa([]byte("]\n"))
		dispositivodescriptor = dispositivo
		driverConteggio++
	}
}
func (séstesso TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectDispositivodescriptor {
	return dispositivodescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Stampastr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MStampa(str)
}

func GetfileDimensione(nomedelfile []byte) uint32 {
	var ata0s = TAvanzateTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabella{}
	partition.Letturapartition(&ata0s)

	bios := TParametri_del_file_system32{}

	var dimensione uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile)
	ata0s.Flush()

	return dimensione
}

func Leggi_file(nomedelfile []byte, data []byte) {
	var ata0s = TAvanzateTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabella{}
	partition.Letturapartition(&ata0s)

	bios := TParametri_del_file_system32{}
	bios.Lettura(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile, data)

	ata0s.Flush()
}
func Caricoelf() {

	var ata0s = TAvanzateTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabella{}
	partition.Letturapartition(&ata0s)

	bios := TParametri_del_file_system32{}

	var nomedelfile []byte = ([]byte)("TEST")
	var dimensione uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lettura(&ata0s, partition.Mbr.Primarypartition[0], nomedelfile, data)

	formato_eseguibile_e_collegabile := Elf{}

	formato_eseguibile_e_collegabile.Parse(data[:dimensione], 0x4f00000)

}

var processoconsole TConsole = TConsole{}

func TFunzione1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func processoa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func processob() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func processoc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func processod()

func processod0() {
	esi := getesi()
	for {

		SysStampaunsignedinteger32(esi)

	}
}

func processod1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ingressoEventoProcesso() {
	for {
		ProcessipendingTastieraEventi()
		ProcessipendingmouseEventi()
		halt()
	}
}

func memorytest(y int) {
	memoriamanager := &TMemoriamanager{}
	allocated := uint32(uintptr(memoriamanager.Alloca_memoria(1024)))
	console.MUnsignedinteger32Stampaxy(allocated, 10, uint16(y))
	if y == 11 {
		memoriamanager.Libero(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pausaloop()
func Ricaricacr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Impostacr3(cr3 uint32)
func Getcr4() uint32
func Abilitapaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunzioneNome(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNome = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcNome)

	processoconsole.MStampaxy(funcByte, 1, 5)
	processoconsole.MStampa(([]byte)(":"))
	processoconsole.MUnsignedinteger32Stampa(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	processoconsole.MStampaunsignedinteger32(cr0, 2, 1)
}

var tss *Tssvoce = &Tssvoce{}

func KKernelEntry(PAGINACartellavoce uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialeRegistroinit()
	console.MStampa("\n=== VAT BOOT ===\n")

	console.MStampaunsignedinteger32(uint32(PAGINACartellavoce), 0, 2)
	console.MStampaunsignedinteger32(uint32(PAGINACartellavoce), 10, 2)
	console.MStampaunsignedinteger32(uint32(stacktop), 0, 3)
	console.MStampaunsignedinteger32(uint32(stackbottom), 10, 3)

	memoriamanager := &TMemoriamanager{}
	memoriamanager.Init(0, MassimaqueueDimensione)

	paging := &Paging{}
	paging.Init(PAGINACartellavoce, 0x500000, memoriamanager)
	paging.SharedMemoriaregion()

	Impostacr3(uint32(PAGINACartellavoce))
	Abilitapaging()

	shareddescriptorTabella := &TShareddescriptorTabella{}
	shareddescriptorTabella.Init()

	console.MStampa("esp:")

	esp := getesp()
	console.MUnsignedinteger32Stampa(uint32(esp))

	tls := gettls()
	console.MStampa(([]byte)("tls:"))
	console.MUnsignedinteger32Stampa(tls)

	tss.Installa(shareddescriptorTabella, 7, Segkerneldata, esp)

	VirtProva()

	cr3 := Ricaricacr3()
	console.MStampa(([]byte)(":cr3:"))
	console.MUnsignedinteger32Stampa(cr3)

	cr0 := Getcr0()
	console.MStampa(([]byte)(":cr0:"))
	console.MUnsignedinteger32Stampa(cr0)

	cr4 := Getcr4()
	console.MStampa(([]byte)(":cr4:"))
	console.MUnsignedinteger32Stampa(cr4)

	processomanager_2 := &TProcessomanager{}
	processomanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptorTabella, processomanager_2)

	paging.PAGINAfault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memoriamanager)

	processihelper := Processihelper{}
	processihelper.Init(memoriamanager, PAGINACartellavoce)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, memoriamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processihelper.Spawn(processoa, threadhelper, sche, uint32(PAGINACartellavoce), true)
	processihelper.Spawn(processob, threadhelper, sche, uint32(PAGINACartellavoce), true)
	processihelper.Spawn(processoc, threadhelper, sche, uint32(PAGINACartellavoce), true)
	processihelper.Spawn(processod1, threadhelper, sche, uint32(PAGINACartellavoce), true)
	processihelper.Spawn(ingressoEventoProcesso, threadhelper, sche, uint32(PAGINACartellavoce), true)

	var dimensione uint32

	var linkerfile []byte = ([]byte)("LINKER")
	dimensione = GetfileDimensione(linkerfile)
	linkeraddress := memoriamanager.Alloca_memoria(dimensione)
	linkerdata := GetBytefromPuntatore(uintptr(linkeraddress), int(dimensione), int(dimensione))
	Leggi_file(linkerfile, linkerdata)

	elf0 := Elf{}
	linkervoce := elf0.Getvoce(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PAGINACartellavoce))

	collegamentomap := Collegamentomap{}
	collegamentomap.Init(memoriamanager)

	var lib1file []byte = ([]byte)("LIB1")
	dimensione = GetfileDimensione(lib1file)

	lib1address := memoriamanager.Alloca_memoria(dimensione)
	lib1data := GetBytefromPuntatore(uintptr(lib1address), int(dimensione), int(dimensione))
	Leggi_file(lib1file, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PAGINACartellavoce))
	memoriamanager.Libero(lib1address)

	collegamentomap.Aggiungi_in_fondo_alla_lista(uintptr(lib1elf.Dinamico))

	var lib2file []byte = ([]byte)("LIB2")
	dimensione = GetfileDimensione(lib2file)

	lib2address := memoriamanager.Alloca_memoria(dimensione)
	lib2data := GetBytefromPuntatore(uintptr(lib2address), int(dimensione), int(dimensione))
	Leggi_file(lib2file, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PAGINACartellavoce))
	memoriamanager.Libero(lib2address)

	collegamentomap.Aggiungi_in_fondo_alla_lista(uintptr(lib2elf.Dinamico))

	libCollegamentomap := collegamentomap.Clone()
	collegamentomapaddress := uint32(uintptr(Pointer(libCollegamentomap.First)))

	lib1got := Getunsignedinteger32SeriefromPuntatore(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = collegamentomapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32SeriefromPuntatore(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = collegamentomapaddress
	lib2got[2] = 0x4000000

	console.MStampaxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Stampa(lib1elf.Got)
	console.MStampa(":")
	console.MUnsignedinteger32Stampa(lib1elf.Dinamico)

	console.MStampaxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Stampa(lib2elf.Got)
	console.MStampa(":")
	console.MUnsignedinteger32Stampa(lib2elf.Dinamico)

	var utente1file []byte = ([]byte)("USER1")
	dimensione = GetfileDimensione(utente1file)
	utente1address := memoriamanager.Alloca_memoria(dimensione)
	utente1data := GetBytefromPuntatore(uintptr(utente1address), int(dimensione), int(dimensione))
	Leggi_file(utente1file, utente1data)

	elf2 := Elf{}

	utente1voce := elf2.Getvoce(utente1data)
	elf2.Parse(utente1data[:], uint32(PAGINACartellavoce+0x1000))
	globaleoffsetTabella := elf2.Got

	PValore1Collegamentomap := collegamentomap.Clone()
	PValore1Collegamentomap.Aggiungi_in_fondo_alla_lista(uintptr(elf2.Dinamico))

	memoriamanager.Libero(utente1address)

	var code1Puntatore *uintptr
	var func1val func()

	code1Puntatore = (*uintptr)(memoriamanager.Alloca_memoria(4))
	*code1Puntatore = uintptr(linkervoce)
	func1val = *(*func())(Pointer(&code1Puntatore))

	proc2 := processihelper.Spawn(func1val, threadhelper, sche, uint32(PAGINACartellavoce+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStato.Ecx = utente1voce
	thr2.CpuStato.Edx = globaleoffsetTabella
	thr2.CpuStato.Esi = uint32(uintptr(Pointer(PValore1Collegamentomap.First)))

	console.MStampaxy("user1: ", 1, 10)
	console.MUnsignedinteger32Stampa(elf2.Got)

	var utente2file []byte = ([]byte)("USER2")
	dimensione = GetfileDimensione(utente2file)
	utente2address := memoriamanager.Alloca_memoria(dimensione)
	utente2data := GetBytefromPuntatore(uintptr(utente2address), int(dimensione), int(dimensione))
	Leggi_file(utente2file, utente2data)

	elf3 := Elf{}

	utente2voce := elf3.Getvoce(utente2data)
	elf3.Parse(utente2data[:], uint32(PAGINACartellavoce+0x2000))
	globaleoffsetTabella = elf3.Got

	PValore2Collegamentomap := collegamentomap.Clone()
	PValore2Collegamentomap.Aggiungi_in_fondo_alla_lista(uintptr(elf3.Dinamico))

	memoriamanager.Libero(utente2address)

	var code2Puntatore *uintptr
	var func2val func()

	code2Puntatore = (*uintptr)(memoriamanager.Alloca_memoria(4))
	*code2Puntatore = uintptr(linkervoce)
	func2val = *(*func())(Pointer(&code2Puntatore))

	proc3 := processihelper.Spawn(func2val, threadhelper, sche, uint32(PAGINACartellavoce+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStato.Ecx = utente2voce
	thr3.CpuStato.Edx = globaleoffsetTabella
	thr3.CpuStato.Esi = uint32(uintptr(Pointer(PValore2Collegamentomap.First)))

	console.MStampaxy("user2: ", 1, 11)
	console.MUnsignedinteger32Stampa(thr3.CpuStato.Esi)

	libCollegamentomap.Stampa(1, 11)

	var utente3file []byte = ([]byte)("USER3")
	dimensione = GetfileDimensione(utente3file)
	utente3address := memoriamanager.Alloca_memoria(dimensione)
	utente3data := GetBytefromPuntatore(uintptr(utente3address), int(dimensione), int(dimensione))
	Leggi_file(utente3file, utente3data)

	elf4 := Elf{}

	utente3voce := elf4.Getvoce(utente3data)
	elf4.Parse(utente3data[:], uint32(PAGINACartellavoce+0x3000))
	globaleoffsetTabella = elf4.Got

	PValore3Collegamentomap := collegamentomap.Clone()
	PValore3Collegamentomap.Aggiungi_in_fondo_alla_lista(uintptr(elf4.Dinamico))

	memoriamanager.Libero(utente3address)

	var code3Puntatore *uintptr
	var func3val func()

	code3Puntatore = (*uintptr)(memoriamanager.Alloca_memoria(4))
	*code3Puntatore = uintptr(linkervoce)
	func3val = *(*func())(Pointer(&code3Puntatore))

	proc4 := processihelper.Spawn(func3val, threadhelper, sche, uint32(PAGINACartellavoce+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStato.Ecx = utente3voce
	thr4.CpuStato.Edx = globaleoffsetTabella
	thr4.CpuStato.Esi = uint32(uintptr(Pointer(PValore3Collegamentomap.First)))

	processihelper.Spawn(TFunzione1, threadhelper, sche, uint32(PAGINACartellavoce+0x4000), true)

	iTastieraEventohandler = &myTastieraEventohandler
	tastieradriver.Initdriver(Interruptmanager, iTastieraEventohandler)

	mousedriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selezionadriver(&Drivermanager, Interruptmanager)
	dispositivodescriptor = mypcicontrollerhandler.Getdriver()

	sche.Abilitato(true)
	Interruptmanager.Attivo()

	for {
		halt()
	}

}
