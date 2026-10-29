/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "consola"
import . "interrupció"
import . "multitasking"
import . "tasking/tss"

import . "virtualMemòria"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/procés"
import . "driver/driver"

import . "driver/teclat"
import . "driver/ratolí"

import . "driver/ata"
import . "fitxerSistema/msdospartition"
import . "fitxerSistema/fat"

import . "fitxerSistema/elf"

import . "sistemacall"

import . "memòriamanager"
import . "pci"

func halt()

var iTeclatEsdevenimenthandler ITeclatEsdevenimenthandler

type TMyTeclatEsdevenimenthandler struct {
}

var myTeclatEsdevenimenthandler TMyTeclatEsdevenimenthandler
var teclatdriver TTeclatdriver
var ratolídriver TRatolídriver
var pciControlador TPeripheralcomponentinterconnectControlador

var teclatConsola TConsola = TConsola{}

func (unmateix *TMyTeclatEsdevenimenthandler) EngegatClauAvall(clau byte) {
	foo := [1]byte{' '}
	foo[0] = clau

	teclatConsola.MImprimeixbytesxy(foo[:], 1000, 1000)
}

func (unmateix *TMyTeclatEsdevenimenthandler) EngegatClauAmunt(clau byte)	{}

var iRatolíEsdevenimenthandler IRatolíEsdevenimenthandler

type TMyRatolíEsdevenimenthandler struct {
}

var ratolíConsola TConsola = TConsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPosició int16 = 0
var yPosició int16 = 0

func (unmateix *TMyRatolíEsdevenimenthandler) EngegatRatolíAvall(botó int8) {
	buffer := []byte("x")
	ratolíConsola.MImprimeixxy(buffer, uint16(previousx), uint16(previousy))
}
func (unmateix *TMyRatolíEsdevenimenthandler) EngegatRatolíAmunt(botó int8)	{}
func (unmateix *TMyRatolíEsdevenimenthandler) EngegatRatolíMou(x int8, y int8) {

	xPosició += int16(x)
	if xPosició < 0 {
		xPosició = 0
	}
	if xPosició >= 80 {
		xPosició = 79
	}

	yPosició -= int16(y)

	if yPosició < 0 {
		yPosició = 0
	}
	if yPosició >= 25 {
		yPosició = 24
	}

	buffer := []byte(" ")
	ratolíConsola.MImprimeixxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	ratolíConsola.MImprimeixxy(buffer, uint16(xPosició), uint16(yPosició))

	previousx = xPosició
	previousy = yPosició
}

var dispositiudescriptor TPeripheralcomponentinterconnectDispositiudescriptor
var ipciControladorhandler IpciControladorhandler

type TMypciControladorhandler struct {
}

var consola TConsola = TConsola{}
var driverRecompte uint16 = 0

func (unmateix TMypciControladorhandler) Engegatgetdriver(dispositiu TPeripheralcomponentinterconnectDispositiudescriptor) {
	if dispositiu.FabricantIdentificador == 0x1022 && dispositiu.DispositiuIdentificador == 0x2000 {
		consola.MImprimeixxy([]byte("["), 0, 12)
		consola.MImprimeix(([]byte)("AMD am79c973"))
		consola.MImprimeix([]byte(":"))
		consola.MUnsignedinteger16Imprimeix(dispositiu.FabricantIdentificador)
		consola.MImprimeix([]byte(":"))
		consola.MUnsignedinteger16Imprimeix(dispositiu.DispositiuIdentificador)
		consola.MImprimeix([]byte(":"))
		consola.MUnsignedinteger16Imprimeix(uint16(dispositiu.Portbase))
		consola.MImprimeix([]byte(":"))
		consola.MUnsignedinteger32Imprimeix(dispositiu.Interrupció)

		consola.MImprimeix([]byte("]\n"))
		dispositiudescriptor = dispositiu
		driverRecompte++
	}
}
func (unmateix TMypciControladorhandler) Getdriver() TPeripheralcomponentinterconnectDispositiudescriptor {
	return dispositiudescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Imprimeixstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	consola.MImprimeix(str)
}

func GetFitxerMida(nomdelfitxer []byte) uint32 {
	var ata0s = TAvançatTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaula{}
	partition.Lecturapartition(&ata0s)

	bios := TBiosparameterBloc32{}

	var mida uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer)
	ata0s.Flush()

	return mida
}

func LecturaFitxer(nomdelfitxer []byte, data []byte) {
	var ata0s = TAvançatTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaula{}
	partition.Lecturapartition(&ata0s)

	bios := TBiosparameterBloc32{}
	bios.Lectura(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer, data)

	ata0s.Flush()
}
func Càrregaelf() {

	var ata0s = TAvançatTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaula{}
	partition.Lecturapartition(&ata0s)

	bios := TBiosparameterBloc32{}

	var nomdelfitxer []byte = ([]byte)("TEST")
	var mida uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Lectura(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer, data)

	elf := Elf{}

	elf.Parse(data[:mida], 0x4f00000)

}

var tascaConsola TConsola = TConsola{}

func TFunció1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tascaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tascab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tascac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tascad()

func tascad0() {
	esi := getesi()
	for {

		SysImprimeixunsignedinteger32(esi)

	}
}

func tascad1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func entradaEsdevenimentTasca() {
	for {
		ProcéspendingTeclatEsdeveniments()
		ProcéspendingRatolíEsdeveniments()
		halt()
	}
}

func memorytest(y int) {
	memòriamanager := &TMemòriamanager{}
	allocated := uint32(uintptr(memòriamanager.Malloc(1024)))
	consola.MUnsignedinteger32Imprimeixxy(allocated, 10, uint16(y))
	if y == 11 {
		memòriamanager.Lliure(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Posaenpausaloop()
func Tornaacarregarcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Estableixcr3(cr3 uint32)
func Getcr4() uint32
func Activapaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFuncióNom(i interface{}) {
	var adreça = reflect.ValueOf(i).Pointer()
	var funcNom = runtime.FuncForPC(adreça).Name()
	var funcbytes []byte = []byte(funcNom)

	tascaConsola.MImprimeixxy(funcbytes, 1, 5)
	tascaConsola.MImprimeix(([]byte)(":"))
	tascaConsola.MUnsignedinteger32Imprimeix(uint32(uintptr(adreça)))
}

func printreg() {
	cr0 := Getcr0()
	tascaConsola.MImprimeixunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentrada = &Tssentrada{}

func KKernelEntry(PàginaDirectorientrada uintptr, stacktop uintptr, stackbottom uintptr) {

	MSèrieRegistreinit()
	consola.MImprimeix("\n=== AND BOOT ===\n")

	consola.MImprimeixunsignedinteger32(uint32(PàginaDirectorientrada), 0, 2)
	consola.MImprimeixunsignedinteger32(uint32(PàginaDirectorientrada), 10, 2)
	consola.MImprimeixunsignedinteger32(uint32(stacktop), 0, 3)
	consola.MImprimeixunsignedinteger32(uint32(stackbottom), 10, 3)

	memòriamanager := &TMemòriamanager{}
	memòriamanager.Init(0, MàxqueueMida)

	paging := &Paging{}
	paging.Init(PàginaDirectorientrada, 0x500000, memòriamanager)
	paging.SharedMemòriaregion()

	Estableixcr3(uint32(PàginaDirectorientrada))
	Activapaging()

	shareddescriptorTaula := &TShareddescriptorTaula{}
	shareddescriptorTaula.Init()

	consola.MImprimeix("esp:")

	esp := getesp()
	consola.MUnsignedinteger32Imprimeix(uint32(esp))

	tls := gettls()
	consola.MImprimeix(([]byte)("tls:"))
	consola.MUnsignedinteger32Imprimeix(tls)

	tss.Install(shareddescriptorTaula, 7, Segkerneldata, esp)

	VirtProva()

	cr3 := Tornaacarregarcr3()
	consola.MImprimeix(([]byte)(":cr3:"))
	consola.MUnsignedinteger32Imprimeix(cr3)

	cr0 := Getcr0()
	consola.MImprimeix(([]byte)(":cr0:"))
	consola.MUnsignedinteger32Imprimeix(cr0)

	cr4 := Getcr4()
	consola.MImprimeix(([]byte)(":cr4:"))
	consola.MUnsignedinteger32Imprimeix(cr4)

	tascamanager_2 := &TTascamanager{}
	tascamanager_2.Init()

	Interrupciómanager := &TInterrupciómanager{}
	Interrupciómanager.Init(0x20, shareddescriptorTaula, tascamanager_2)

	paging.Pàginafault(Interrupciómanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memòriamanager)

	procéshelper := Procéshelper{}
	procéshelper.Init(memòriamanager, PàginaDirectorientrada)

	sche := &Scheduler{}
	sche.Init(Interrupciómanager, memòriamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interrupciómanager)

	procéshelper.Spawn(tascaa, threadhelper, sche, uint32(PàginaDirectorientrada), true)
	procéshelper.Spawn(tascab, threadhelper, sche, uint32(PàginaDirectorientrada), true)
	procéshelper.Spawn(tascac, threadhelper, sche, uint32(PàginaDirectorientrada), true)
	procéshelper.Spawn(tascad1, threadhelper, sche, uint32(PàginaDirectorientrada), true)
	procéshelper.Spawn(entradaEsdevenimentTasca, threadhelper, sche, uint32(PàginaDirectorientrada), true)

	var mida uint32

	var linkerFitxer []byte = ([]byte)("LINKER")
	mida = GetFitxerMida(linkerFitxer)
	linkerAdreça := memòriamanager.Malloc(mida)
	linkerdata := GetbytesdesdePunter(uintptr(linkerAdreça), int(mida), int(mida))
	LecturaFitxer(linkerFitxer, linkerdata)

	elf0 := Elf{}
	linkerentrada := elf0.Getentrada(linkerdata)
	elf0.Parse(linkerdata[:], uint32(PàginaDirectorientrada))

	enllaçmap := Enllaçmap{}
	enllaçmap.Init(memòriamanager)

	var lib1Fitxer []byte = ([]byte)("LIB1")
	mida = GetFitxerMida(lib1Fitxer)

	lib1Adreça := memòriamanager.Malloc(mida)
	lib1data := GetbytesdesdePunter(uintptr(lib1Adreça), int(mida), int(mida))
	LecturaFitxer(lib1Fitxer, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(PàginaDirectorientrada))
	memòriamanager.Lliure(lib1Adreça)

	enllaçmap.Append_to_list(uintptr(lib1elf.Dinàmic))

	var lib2Fitxer []byte = ([]byte)("LIB2")
	mida = GetFitxerMida(lib2Fitxer)

	lib2Adreça := memòriamanager.Malloc(mida)
	lib2data := GetbytesdesdePunter(uintptr(lib2Adreça), int(mida), int(mida))
	LecturaFitxer(lib2Fitxer, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(PàginaDirectorientrada))
	memòriamanager.Lliure(lib2Adreça)

	enllaçmap.Append_to_list(uintptr(lib2elf.Dinàmic))

	libEnllaçmap := enllaçmap.Clone()
	enllaçmapAdreça := uint32(uintptr(Pointer(libEnllaçmap.First)))

	lib1got := Getunsignedinteger32MatriudesdePunter(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = enllaçmapAdreça
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32MatriudesdePunter(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = enllaçmapAdreça
	lib2got[2] = 0x4000000

	consola.MImprimeixxy("lib1: ", 1, 8)
	consola.MUnsignedinteger32Imprimeix(lib1elf.Got)
	consola.MImprimeix(":")
	consola.MUnsignedinteger32Imprimeix(lib1elf.Dinàmic)

	consola.MImprimeixxy("lib2: ", 1, 9)
	consola.MUnsignedinteger32Imprimeix(lib2elf.Got)
	consola.MImprimeix(":")
	consola.MUnsignedinteger32Imprimeix(lib2elf.Dinàmic)

	var usuari1Fitxer []byte = ([]byte)("USER1")
	mida = GetFitxerMida(usuari1Fitxer)
	usuari1Adreça := memòriamanager.Malloc(mida)
	usuari1data := GetbytesdesdePunter(uintptr(usuari1Adreça), int(mida), int(mida))
	LecturaFitxer(usuari1Fitxer, usuari1data)

	elf2 := Elf{}

	usuari1entrada := elf2.Getentrada(usuari1data)
	elf2.Parse(usuari1data[:], uint32(PàginaDirectorientrada+0x1000))
	globaloffsetTaula := elf2.Got

	PValor1Enllaçmap := enllaçmap.Clone()
	PValor1Enllaçmap.Append_to_list(uintptr(elf2.Dinàmic))

	memòriamanager.Lliure(usuari1Adreça)

	var code1Punter *uintptr
	var func1val func()

	code1Punter = (*uintptr)(memòriamanager.Malloc(4))
	*code1Punter = uintptr(linkerentrada)
	func1val = *(*func())(Pointer(&code1Punter))

	proc2 := procéshelper.Spawn(func1val, threadhelper, sche, uint32(PàginaDirectorientrada+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuEstat.Ecx = usuari1entrada
	thr2.CpuEstat.Edx = globaloffsetTaula
	thr2.CpuEstat.Esi = uint32(uintptr(Pointer(PValor1Enllaçmap.First)))

	consola.MImprimeixxy("user1: ", 1, 10)
	consola.MUnsignedinteger32Imprimeix(elf2.Got)

	var usuari2Fitxer []byte = ([]byte)("USER2")
	mida = GetFitxerMida(usuari2Fitxer)
	usuari2Adreça := memòriamanager.Malloc(mida)
	usuari2data := GetbytesdesdePunter(uintptr(usuari2Adreça), int(mida), int(mida))
	LecturaFitxer(usuari2Fitxer, usuari2data)

	elf3 := Elf{}

	usuari2entrada := elf3.Getentrada(usuari2data)
	elf3.Parse(usuari2data[:], uint32(PàginaDirectorientrada+0x2000))
	globaloffsetTaula = elf3.Got

	PValor2Enllaçmap := enllaçmap.Clone()
	PValor2Enllaçmap.Append_to_list(uintptr(elf3.Dinàmic))

	memòriamanager.Lliure(usuari2Adreça)

	var code2Punter *uintptr
	var func2val func()

	code2Punter = (*uintptr)(memòriamanager.Malloc(4))
	*code2Punter = uintptr(linkerentrada)
	func2val = *(*func())(Pointer(&code2Punter))

	proc3 := procéshelper.Spawn(func2val, threadhelper, sche, uint32(PàginaDirectorientrada+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuEstat.Ecx = usuari2entrada
	thr3.CpuEstat.Edx = globaloffsetTaula
	thr3.CpuEstat.Esi = uint32(uintptr(Pointer(PValor2Enllaçmap.First)))

	consola.MImprimeixxy("user2: ", 1, 11)
	consola.MUnsignedinteger32Imprimeix(thr3.CpuEstat.Esi)

	libEnllaçmap.Imprimeix(1, 11)

	var usuari3Fitxer []byte = ([]byte)("USER3")
	mida = GetFitxerMida(usuari3Fitxer)
	usuari3Adreça := memòriamanager.Malloc(mida)
	usuari3data := GetbytesdesdePunter(uintptr(usuari3Adreça), int(mida), int(mida))
	LecturaFitxer(usuari3Fitxer, usuari3data)

	elf4 := Elf{}

	usuari3entrada := elf4.Getentrada(usuari3data)
	elf4.Parse(usuari3data[:], uint32(PàginaDirectorientrada+0x3000))
	globaloffsetTaula = elf4.Got

	PValor3Enllaçmap := enllaçmap.Clone()
	PValor3Enllaçmap.Append_to_list(uintptr(elf4.Dinàmic))

	memòriamanager.Lliure(usuari3Adreça)

	var code3Punter *uintptr
	var func3val func()

	code3Punter = (*uintptr)(memòriamanager.Malloc(4))
	*code3Punter = uintptr(linkerentrada)
	func3val = *(*func())(Pointer(&code3Punter))

	proc4 := procéshelper.Spawn(func3val, threadhelper, sche, uint32(PàginaDirectorientrada+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuEstat.Ecx = usuari3entrada
	thr4.CpuEstat.Edx = globaloffsetTaula
	thr4.CpuEstat.Esi = uint32(uintptr(Pointer(PValor3Enllaçmap.First)))

	procéshelper.Spawn(TFunció1, threadhelper, sche, uint32(PàginaDirectorientrada+0x4000), true)

	iTeclatEsdevenimenthandler = &myTeclatEsdevenimenthandler
	teclatdriver.Initdriver(Interrupciómanager, iTeclatEsdevenimenthandler)

	ratolídriver.Initdriver(Interrupciómanager, nil)

	mypciControladorhandler := TMypciControladorhandler{}
	pciControlador.Init(mypciControladorhandler)
	pciControlador.Seleccionadriver(&Drivermanager, Interrupciómanager)
	dispositiudescriptor = mypciControladorhandler.Getdriver()

	sche.Habilitat(true)
	Interrupciómanager.Actiu()

	for {
		halt()
	}

}
