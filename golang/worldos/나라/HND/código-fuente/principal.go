/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "utilidad"
import . "gdt"
import . "consola"
import . "interrupción"
import . "múltiplegestiónTareas"
import . "gestiónTareas/tss"

import . "virtualmemoria"
import . "paginación"
import . "gestiónTareas/hilo"
import . "gestiónTareas/planificador"
import . "gestiónTareas/proceso"
import . "controlador/controlador"

import . "controlador/teclado"
import . "controlador/dispositivo_señalador"

import . "controlador/ata"
import . "archivosistema/msdospartición"
import . "archivosistema/fat"

import . "archivosistema/formato_ejecutable_y_enlazable"

import . "sistemallamada"

import . "memoriagestor"
import . "pci"

func halt()

var itecladoeventohandler ITecladoeventohandler

type TMytecladoeventohandler struct {
}

var mytecladoeventohandler TMytecladoeventohandler
var tecladocontrolador TTecladocontrolador
var ratóncontrolador TRatóncontrolador
var pcicontrolador TPeripheralcomponentinterconnectcontrolador

var tecladoconsola TConsola = TConsola{}

func (propio *TMytecladoeventohandler) AlClaveAbajo(clave byte) {
	tururú := [1]byte{' '}
	tururú[0] = clave

	tecladoconsola.MImprimirbytesxy(tururú[:], 1000, 1000)
}

func (propio *TMytecladoeventohandler) AlClaveSubir(clave byte)	{}

var iratóneventohandler IRatóneventohandler

type TMyratóneventohandler struct {
}

var ratónconsola TConsola = TConsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPosición int16 = 0
var yPosición int16 = 0

func (propio *TMyratóneventohandler) AlratónAbajo(botón int8) {
	buffer := []byte("x")
	ratónconsola.MImprimirxy(buffer, uint16(previousx), uint16(previousy))
}
func (propio *TMyratóneventohandler) AlratónSubir(botón int8)	{}
func (propio *TMyratóneventohandler) AlratónMover(x int8, y int8) {

	xPosición += int16(x)
	if xPosición < 0 {
		xPosición = 0
	}
	if xPosición >= 80 {
		xPosición = 79
	}

	yPosición -= int16(y)

	if yPosición < 0 {
		yPosición = 0
	}
	if yPosición >= 25 {
		yPosición = 24
	}

	buffer := []byte(" ")
	ratónconsola.MImprimirxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	ratónconsola.MImprimirxy(buffer, uint16(xPosición), uint16(yPosición))

	previousx = xPosición
	previousy = yPosición
}

var dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor
var ipcicontroladorhandler Ipcicontroladorhandler

type TMypcicontroladorhandler struct {
}

var consola TConsola = TConsola{}
var controladorRecuento uint16 = 0

func (propio TMypcicontroladorhandler) Algetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
	if dispositivo.Fabricanteid == 0x1022 && dispositivo.Dispositivoid == 0x2000 {
		consola.MImprimirxy([]byte("["), 0, 12)
		consola.MImprimir(([]byte)("AMD am79c973"))
		consola.MImprimir([]byte(":"))
		consola.MUnsignedinteger16Imprimir(dispositivo.Fabricanteid)
		consola.MImprimir([]byte(":"))
		consola.MUnsignedinteger16Imprimir(dispositivo.Dispositivoid)
		consola.MImprimir([]byte(":"))
		consola.MUnsignedinteger16Imprimir(uint16(dispositivo.Puertobase))
		consola.MImprimir([]byte(":"))
		consola.MUnsignedinteger32Imprimir(dispositivo.Interrupción)

		consola.MImprimir([]byte("]\n"))
		dispositivodescriptor = dispositivo
		controladorRecuento++
	}
}
func (propio TMypcicontroladorhandler) Getcontrolador() TPeripheralcomponentinterconnectDispositivodescriptor {
	return dispositivodescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Imprimirstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	consola.MImprimir(str)
}

func GetarchivoTamaño(nombredearchivo []byte) uint32 {
	var ata0s = TAvanzadoTecnologíaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partición := TmsdosparticiónTabla{}
	partición.Leerpartición(&ata0s)

	bios := TParámetros_del_sistema_de_archivos32{}

	var tamaño uint32 = bios.Len(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo)
	ata0s.Flush()

	return tamaño
}

func Leer_archivo(nombredearchivo []byte, datos []byte) {
	var ata0s = TAvanzadoTecnologíaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partición := TmsdosparticiónTabla{}
	partición.Leerpartición(&ata0s)

	bios := TParámetros_del_sistema_de_archivos32{}
	bios.Leer(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo, datos)

	ata0s.Flush()
}
func Cargarelf() {

	var ata0s = TAvanzadoTecnologíaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partición := TmsdosparticiónTabla{}
	partición.Leerpartición(&ata0s)

	bios := TParámetros_del_sistema_de_archivos32{}

	var nombredearchivo []byte = ([]byte)("TEST")
	var tamaño uint32 = bios.Len(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo)
	var datosbuffer [100 * 1024]byte
	var datos []byte = datosbuffer[:]
	bios.Leer(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo, datos)

	formato_ejecutable_y_enlazable := Elf{}

	formato_ejecutable_y_enlazable.Parse(datos[:tamaño], 0x4f00000)

}

var tareaconsola TConsola = TConsola{}

func TFunción1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tareaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tareab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tareac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func taread()

func taread0() {
	esi := getesi()
	for {

		SysImprimirunsignedinteger32(esi)

	}
}

func taread1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func entradaeventotarea() {
	for {
		Procesopendientetecladoeventos()
		Procesopendienteratóneventos()
		halt()
	}
}

func memorytest(y int) {
	memoriagestor := &TMemoriagestor{}
	allocated := uint32(uintptr(memoriagestor.Asignar_memoria(1024)))
	consola.MUnsignedinteger32Imprimirxy(allocated, 10, uint16(y))
	if y == 11 {
		memoriagestor.Libre(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func PausaBucle()
func Recargarcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Establecercr3(cr3 uint32)
func Getcr4() uint32
func Activarpaginación()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunciónNombre(i interface{}) {
	var dirección = reflect.ValueOf(i).Pointer()
	var funcNombre = runtime.FuncForPC(dirección).Name()
	var funcbytes []byte = []byte(funcNombre)

	tareaconsola.MImprimirxy(funcbytes, 1, 5)
	tareaconsola.MImprimir(([]byte)(":"))
	tareaconsola.MUnsignedinteger32Imprimir(uint32(uintptr(dirección)))
}

func printreg() {
	cr0 := Getcr0()
	tareaconsola.MImprimirunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentrada = &Tssentrada{}

func KKernelEntry(Páginadirectorioentrada uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerieRegistroinit()
	consola.MImprimir("\n=== HND BOOT ===\n")

	consola.MImprimirunsignedinteger32(uint32(Páginadirectorioentrada), 0, 2)
	consola.MImprimirunsignedinteger32(uint32(Páginadirectorioentrada), 10, 2)
	consola.MImprimirunsignedinteger32(uint32(stacktop), 0, 3)
	consola.MImprimirunsignedinteger32(uint32(stackbottom), 10, 3)

	memoriagestor := &TMemoriagestor{}
	memoriagestor.Init(0, MáxcolaTamaño)

	paginación := &Paginación{}
	paginación.Init(Páginadirectorioentrada, 0x500000, memoriagestor)
	paginación.Sharedmemoriaregion()

	Establecercr3(uint32(Páginadirectorioentrada))
	Activarpaginación()

	shareddescriptorTabla := &TShareddescriptorTabla{}
	shareddescriptorTabla.Init()

	consola.MImprimir("esp:")

	esp := getesp()
	consola.MUnsignedinteger32Imprimir(uint32(esp))

	tls := gettls()
	consola.MImprimir(([]byte)("tls:"))
	consola.MUnsignedinteger32Imprimir(tls)

	tss.Instalar(shareddescriptorTabla, 7, Segnúcleodatos, esp)

	VirtProbar()

	cr3 := Recargarcr3()
	consola.MImprimir(([]byte)(":cr3:"))
	consola.MUnsignedinteger32Imprimir(cr3)

	cr0 := Getcr0()
	consola.MImprimir(([]byte)(":cr0:"))
	consola.MUnsignedinteger32Imprimir(cr0)

	cr4 := Getcr4()
	consola.MImprimir(([]byte)(":cr4:"))
	consola.MUnsignedinteger32Imprimir(cr4)

	tareagestor_2 := &TTareagestor{}
	tareagestor_2.Init()

	Interrupcióngestor := &TInterrupcióngestor{}
	Interrupcióngestor.Init(0x20, shareddescriptorTabla, tareagestor_2)

	paginación.Páginafallo(Interrupcióngestor)

	Controladorgestor := TControladorgestor{}
	Controladorgestor.Init()

	hilohelper := &THilohelper{}
	hilohelper.Init(memoriagestor)

	procesohelper := Procesohelper{}
	procesohelper.Init(memoriagestor, Páginadirectorioentrada)

	sche := &Planificador{}
	sche.Init(Interrupcióngestor, memoriagestor, tss)

	sysllamada := &TSyscall{}
	sysllamada.Init(Interrupcióngestor)

	procesohelper.Spawn(tareaa, hilohelper, sche, uint32(Páginadirectorioentrada), true)
	procesohelper.Spawn(tareab, hilohelper, sche, uint32(Páginadirectorioentrada), true)
	procesohelper.Spawn(tareac, hilohelper, sche, uint32(Páginadirectorioentrada), true)
	procesohelper.Spawn(taread1, hilohelper, sche, uint32(Páginadirectorioentrada), true)
	procesohelper.Spawn(entradaeventotarea, hilohelper, sche, uint32(Páginadirectorioentrada), true)

	var tamaño uint32

	var linkerarchivo []byte = ([]byte)("LINKER")
	tamaño = GetarchivoTamaño(linkerarchivo)
	linkerDirección := memoriagestor.Asignar_memoria(tamaño)
	linkerdatos := GetbytesdesdePuntero(uintptr(linkerDirección), int(tamaño), int(tamaño))
	Leer_archivo(linkerarchivo, linkerdatos)

	elf0 := Elf{}
	linkerentrada := elf0.Getentrada(linkerdatos)
	elf0.Parse(linkerdatos[:], uint32(Páginadirectorioentrada))

	enlacemapa := Enlacemapa{}
	enlacemapa.Init(memoriagestor)

	var lib1archivo []byte = ([]byte)("LIB1")
	tamaño = GetarchivoTamaño(lib1archivo)

	lib1Dirección := memoriagestor.Asignar_memoria(tamaño)
	lib1datos := GetbytesdesdePuntero(uintptr(lib1Dirección), int(tamaño), int(tamaño))
	Leer_archivo(lib1archivo, lib1datos)

	lib1elf := Elf{}
	lib1elf.Parse(lib1datos[:], uint32(Páginadirectorioentrada))
	memoriagestor.Libre(lib1Dirección)

	enlacemapa.Añadir_al_final_de_la_lista(uintptr(lib1elf.Dinámico))

	var lib2archivo []byte = ([]byte)("LIB2")
	tamaño = GetarchivoTamaño(lib2archivo)

	lib2Dirección := memoriagestor.Asignar_memoria(tamaño)
	lib2datos := GetbytesdesdePuntero(uintptr(lib2Dirección), int(tamaño), int(tamaño))
	Leer_archivo(lib2archivo, lib2datos)

	lib2elf := Elf{}
	lib2elf.Parse(lib2datos[:], uint32(Páginadirectorioentrada))
	memoriagestor.Libre(lib2Dirección)

	enlacemapa.Añadir_al_final_de_la_lista(uintptr(lib2elf.Dinámico))

	libenlacemapa := enlacemapa.Clone()
	enlacemapaDirección := uint32(uintptr(Pointer(libenlacemapa.First)))

	lib1got := Getunsignedinteger32matrizdesdePuntero(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = enlacemapaDirección
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32matrizdesdePuntero(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = enlacemapaDirección
	lib2got[2] = 0x4000000

	consola.MImprimirxy("lib1: ", 1, 8)
	consola.MUnsignedinteger32Imprimir(lib1elf.Got)
	consola.MImprimir(":")
	consola.MUnsignedinteger32Imprimir(lib1elf.Dinámico)

	consola.MImprimirxy("lib2: ", 1, 9)
	consola.MUnsignedinteger32Imprimir(lib2elf.Got)
	consola.MImprimir(":")
	consola.MUnsignedinteger32Imprimir(lib2elf.Dinámico)

	var usuario1archivo []byte = ([]byte)("USER1")
	tamaño = GetarchivoTamaño(usuario1archivo)
	usuario1Dirección := memoriagestor.Asignar_memoria(tamaño)
	usuario1datos := GetbytesdesdePuntero(uintptr(usuario1Dirección), int(tamaño), int(tamaño))
	Leer_archivo(usuario1archivo, usuario1datos)

	elf2 := Elf{}

	usuario1entrada := elf2.Getentrada(usuario1datos)
	elf2.Parse(usuario1datos[:], uint32(Páginadirectorioentrada+0x1000))
	globalDesplazamientoTabla := elf2.Got

	PValor1enlacemapa := enlacemapa.Clone()
	PValor1enlacemapa.Añadir_al_final_de_la_lista(uintptr(elf2.Dinámico))

	memoriagestor.Libre(usuario1Dirección)

	var code1Puntero *uintptr
	var func1val func()

	code1Puntero = (*uintptr)(memoriagestor.Asignar_memoria(4))
	*code1Puntero = uintptr(linkerentrada)
	func1val = *(*func())(Pointer(&code1Puntero))

	proc2 := procesohelper.Spawn(func1val, hilohelper, sche, uint32(Páginadirectorioentrada+0x1000), false)
	thr2 := (*THilo)(proc2.Threads.Getat(0))
	thr2.CpuEstado.Ecx = usuario1entrada
	thr2.CpuEstado.Edx = globalDesplazamientoTabla
	thr2.CpuEstado.Esi = uint32(uintptr(Pointer(PValor1enlacemapa.First)))

	consola.MImprimirxy("user1: ", 1, 10)
	consola.MUnsignedinteger32Imprimir(elf2.Got)

	var usuario2archivo []byte = ([]byte)("USER2")
	tamaño = GetarchivoTamaño(usuario2archivo)
	usuario2Dirección := memoriagestor.Asignar_memoria(tamaño)
	usuario2datos := GetbytesdesdePuntero(uintptr(usuario2Dirección), int(tamaño), int(tamaño))
	Leer_archivo(usuario2archivo, usuario2datos)

	elf3 := Elf{}

	usuario2entrada := elf3.Getentrada(usuario2datos)
	elf3.Parse(usuario2datos[:], uint32(Páginadirectorioentrada+0x2000))
	globalDesplazamientoTabla = elf3.Got

	PValor2enlacemapa := enlacemapa.Clone()
	PValor2enlacemapa.Añadir_al_final_de_la_lista(uintptr(elf3.Dinámico))

	memoriagestor.Libre(usuario2Dirección)

	var code2Puntero *uintptr
	var func2val func()

	code2Puntero = (*uintptr)(memoriagestor.Asignar_memoria(4))
	*code2Puntero = uintptr(linkerentrada)
	func2val = *(*func())(Pointer(&code2Puntero))

	proc3 := procesohelper.Spawn(func2val, hilohelper, sche, uint32(Páginadirectorioentrada+0x2000), false)
	thr3 := (*THilo)(proc3.Threads.Getat(0))
	thr3.CpuEstado.Ecx = usuario2entrada
	thr3.CpuEstado.Edx = globalDesplazamientoTabla
	thr3.CpuEstado.Esi = uint32(uintptr(Pointer(PValor2enlacemapa.First)))

	consola.MImprimirxy("user2: ", 1, 11)
	consola.MUnsignedinteger32Imprimir(thr3.CpuEstado.Esi)

	libenlacemapa.Imprimir(1, 11)

	var usuario3archivo []byte = ([]byte)("USER3")
	tamaño = GetarchivoTamaño(usuario3archivo)
	usuario3Dirección := memoriagestor.Asignar_memoria(tamaño)
	usuario3datos := GetbytesdesdePuntero(uintptr(usuario3Dirección), int(tamaño), int(tamaño))
	Leer_archivo(usuario3archivo, usuario3datos)

	elf4 := Elf{}

	usuario3entrada := elf4.Getentrada(usuario3datos)
	elf4.Parse(usuario3datos[:], uint32(Páginadirectorioentrada+0x3000))
	globalDesplazamientoTabla = elf4.Got

	PValor3enlacemapa := enlacemapa.Clone()
	PValor3enlacemapa.Añadir_al_final_de_la_lista(uintptr(elf4.Dinámico))

	memoriagestor.Libre(usuario3Dirección)

	var code3Puntero *uintptr
	var func3val func()

	code3Puntero = (*uintptr)(memoriagestor.Asignar_memoria(4))
	*code3Puntero = uintptr(linkerentrada)
	func3val = *(*func())(Pointer(&code3Puntero))

	proc4 := procesohelper.Spawn(func3val, hilohelper, sche, uint32(Páginadirectorioentrada+0x3000), false)
	thr4 := (*THilo)(proc4.Threads.Getat(0))
	thr4.CpuEstado.Ecx = usuario3entrada
	thr4.CpuEstado.Edx = globalDesplazamientoTabla
	thr4.CpuEstado.Esi = uint32(uintptr(Pointer(PValor3enlacemapa.First)))

	procesohelper.Spawn(TFunción1, hilohelper, sche, uint32(Páginadirectorioentrada+0x4000), true)

	itecladoeventohandler = &mytecladoeventohandler
	tecladocontrolador.Initcontrolador(Interrupcióngestor, itecladoeventohandler)

	ratóncontrolador.Initcontrolador(Interrupcióngestor, nil)

	mypcicontroladorhandler := TMypcicontroladorhandler{}
	pcicontrolador.Init(mypcicontroladorhandler)
	pcicontrolador.Seleccionarcontrolador(&Controladorgestor, Interrupcióngestor)
	dispositivodescriptor = mypcicontroladorhandler.Getcontrolador()

	sche.Activado(true)
	Interrupcióngestor.Activo()

	for {
		halt()
	}

}
