package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "utilitário"
import . "gdt"
import . "console"
import . "interrupção"
import . "múltiplogestãoTarefas"
import . "gestãoTarefas/tss"

import . "virtualmemória"
import . "paginação"
import . "gestãoTarefas/fluxoExecução"
import . "gestãoTarefas/escalonador"
import . "gestãoTarefas/processo"
import . "controlador/controlador"

import . "controlador/teclado"
import . "controlador/dispositivo_apontador"

import . "controlador/ata"
import . "ficheirosistema/msdospartição"
import . "ficheirosistema/fat"

import . "ficheirosistema/formato_executável_e_ligável"

import . "sistemachamada"

import . "memóriagestor"
import . "pci"

func halt()

var itecladoeventohandler ITecladoeventohandler

type TMytecladoeventohandler struct {
}

var mytecladoeventohandler TMytecladoeventohandler
var tecladocontrolador TTecladocontrolador
var ratocontrolador TRatocontrolador
var pcicontrolador TPeripheralcomponentinterconnectcontrolador

var tecladoconsole TConsole = TConsole{}

func (próprio *TMytecladoeventohandler) AoChaveAbaixo(chave byte) {
	foo := [1]byte{' '}
	foo[0] = chave

	tecladoconsole.MImprimirbytesxy(foo[:], 1000, 1000)
}

func (próprio *TMytecladoeventohandler) AoChaveParacima(chave byte)	{}

var iratoeventohandler IRatoeventohandler

type TMyratoeventohandler struct {
}

var ratoconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosição int16 = 0
var yPosição int16 = 0

func (próprio *TMyratoeventohandler) AoratoAbaixo(botão int8) {
	buffer := []byte("x")
	ratoconsole.MImprimirxy(buffer, uint16(previousx), uint16(previousy))
}
func (próprio *TMyratoeventohandler) AoratoParacima(botão int8)	{}
func (próprio *TMyratoeventohandler) AoratoMover(x int8, y int8) {

	xPosição += int16(x)
	if xPosição < 0 {
		xPosição = 0
	}
	if xPosição >= 80 {
		xPosição = 79
	}

	yPosição -= int16(y)

	if yPosição < 0 {
		yPosição = 0
	}
	if yPosição >= 25 {
		yPosição = 24
	}

	buffer := []byte(" ")
	ratoconsole.MImprimirxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	ratoconsole.MImprimirxy(buffer, uint16(xPosição), uint16(yPosição))

	previousx = xPosição
	previousy = yPosição
}

var dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor
var ipcicontroladorhandler Ipcicontroladorhandler

type TMypcicontroladorhandler struct {
}

var console TConsole = TConsole{}
var controladorContar uint16 = 0

func (próprio TMypcicontroladorhandler) Aogetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
	if dispositivo.Fabricanteid == 0x1022 && dispositivo.Dispositivoid == 0x2000 {
		console.MImprimirxy([]byte("["), 0, 12)
		console.MImprimir(([]byte)("AMD am79c973"))
		console.MImprimir([]byte(":"))
		console.MUnsignedinteger16Imprimir(dispositivo.Fabricanteid)
		console.MImprimir([]byte(":"))
		console.MUnsignedinteger16Imprimir(dispositivo.Dispositivoid)
		console.MImprimir([]byte(":"))
		console.MUnsignedinteger16Imprimir(uint16(dispositivo.Portobase))
		console.MImprimir([]byte(":"))
		console.MUnsignedinteger32Imprimir(dispositivo.Interrupção)

		console.MImprimir([]byte("]\n"))
		dispositivodescriptor = dispositivo
		controladorContar++
	}
}
func (próprio TMypcicontroladorhandler) Getcontrolador() TPeripheralcomponentinterconnectDispositivodescriptor {
	return dispositivodescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Imprimirstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MImprimir(str)
}

func GetficheiroTamanho(nomedoficheiro []byte) uint32 {
	var ata0s = TAvançadoTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partição := TmsdospartiçãoTabela{}
	partição.Lerpartição(&ata0s)

	bios := TParâmetros_do_sistema_de_ficheiros32{}

	var tamanho uint32 = bios.Len(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro)
	ata0s.Flush()

	return tamanho
}

func Ler_ficheiro(nomedoficheiro []byte, dados []byte) {
	var ata0s = TAvançadoTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partição := TmsdospartiçãoTabela{}
	partição.Lerpartição(&ata0s)

	bios := TParâmetros_do_sistema_de_ficheiros32{}
	bios.Ler(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro, dados)

	ata0s.Flush()
}
func Carregarelf() {

	var ata0s = TAvançadoTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partição := TmsdospartiçãoTabela{}
	partição.Lerpartição(&ata0s)

	bios := TParâmetros_do_sistema_de_ficheiros32{}

	var nomedoficheiro []byte = ([]byte)("TEST")
	var tamanho uint32 = bios.Len(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro)
	var dadosbuffer [100 * 1024]byte
	var dados []byte = dadosbuffer[:]
	bios.Ler(&ata0s, partição.Mbr.Primarypartição[0], nomedoficheiro, dados)

	formato_executável_e_ligável := Elf{}

	formato_executável_e_ligável.Parse(dados[:tamanho], 0x4f00000)

}

var tarefaconsole TConsole = TConsole{}

func TFunção1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tarefaa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tarefab() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tarefac() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tarefad()

func tarefad0() {
	esi := getesi()
	for {

		SysImprimirunsignedinteger32(esi)

	}
}

func tarefad1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func entradaeventotarefa() {
	for {
		Processopendentetecladoeventos()
		Processopendenteratoeventos()
		halt()
	}
}

func memorytest(y int) {
	memóriagestor := &TMemóriagestor{}
	allocated := uint32(uintptr(memóriagestor.Alocar_memória(1024)))
	console.MUnsignedinteger32Imprimirxy(allocated, 10, uint16(y))
	if y == 11 {
		memóriagestor.Livre(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pausaloop()
func Recarregarcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Conjuntocr3(cr3 uint32)
func Getcr4() uint32
func Activarpaginação()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunçãoNome(i interface{}) {
	var endereço = reflect.ValueOf(i).Pointer()
	var funcNome = runtime.FuncForPC(endereço).Name()
	var funcbytes []byte = []byte(funcNome)

	tarefaconsole.MImprimirxy(funcbytes, 1, 5)
	tarefaconsole.MImprimir(([]byte)(":"))
	tarefaconsole.MUnsignedinteger32Imprimir(uint32(uintptr(endereço)))
}

func printreg() {
	cr0 := Getcr0()
	tarefaconsole.MImprimirunsignedinteger32(cr0, 2, 1)
}

var tss *Tsspontodeentrada = &Tsspontodeentrada{}

func KKernelEntry(Páginadiretóriopontodeentrada uintptr, stacktop uintptr, stackbottom uintptr) {

	MSérieRegistoinit()
	console.MImprimir("\n=== CPV BOOT ===\n")

	console.MImprimirunsignedinteger32(uint32(Páginadiretóriopontodeentrada), 0, 2)
	console.MImprimirunsignedinteger32(uint32(Páginadiretóriopontodeentrada), 10, 2)
	console.MImprimirunsignedinteger32(uint32(stacktop), 0, 3)
	console.MImprimirunsignedinteger32(uint32(stackbottom), 10, 3)

	memóriagestor := &TMemóriagestor{}
	memóriagestor.Init(0, MaxfilaTamanho)

	paginação := &Paginação{}
	paginação.Init(Páginadiretóriopontodeentrada, 0x500000, memóriagestor)
	paginação.Sharedmemóriaregion()

	Conjuntocr3(uint32(Páginadiretóriopontodeentrada))
	Activarpaginação()

	shareddescriptorTabela := &TShareddescriptorTabela{}
	shareddescriptorTabela.Init()

	console.MImprimir("esp:")

	esp := getesp()
	console.MUnsignedinteger32Imprimir(uint32(esp))

	tls := gettls()
	console.MImprimir(([]byte)("tls:"))
	console.MUnsignedinteger32Imprimir(tls)

	tss.Instalar(shareddescriptorTabela, 7, Segnúcleodados, esp)

	VirtTestar()

	cr3 := Recarregarcr3()
	console.MImprimir(([]byte)(":cr3:"))
	console.MUnsignedinteger32Imprimir(cr3)

	cr0 := Getcr0()
	console.MImprimir(([]byte)(":cr0:"))
	console.MUnsignedinteger32Imprimir(cr0)

	cr4 := Getcr4()
	console.MImprimir(([]byte)(":cr4:"))
	console.MUnsignedinteger32Imprimir(cr4)

	tarefagestor_2 := &TTarefagestor{}
	tarefagestor_2.Init()

	Interrupçãogestor := &TInterrupçãogestor{}
	Interrupçãogestor.Init(0x20, shareddescriptorTabela, tarefagestor_2)

	paginação.Páginafalha(Interrupçãogestor)

	Controladorgestor := TControladorgestor{}
	Controladorgestor.Init()

	fluxoExecuçãohelper := &TFluxoExecuçãohelper{}
	fluxoExecuçãohelper.Init(memóriagestor)

	processohelper := Processohelper{}
	processohelper.Init(memóriagestor, Páginadiretóriopontodeentrada)

	sche := &Escalonador{}
	sche.Init(Interrupçãogestor, memóriagestor, tss)

	syschamada := &TSyscall{}
	syschamada.Init(Interrupçãogestor)

	processohelper.Spawn(tarefaa, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada), true)
	processohelper.Spawn(tarefab, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada), true)
	processohelper.Spawn(tarefac, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada), true)
	processohelper.Spawn(tarefad1, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada), true)
	processohelper.Spawn(entradaeventotarefa, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada), true)

	var tamanho uint32

	var linkerficheiro []byte = ([]byte)("LINKER")
	tamanho = GetficheiroTamanho(linkerficheiro)
	linkerEndereço := memóriagestor.Alocar_memória(tamanho)
	linkerdados := GetbytesdePonteiro(uintptr(linkerEndereço), int(tamanho), int(tamanho))
	Ler_ficheiro(linkerficheiro, linkerdados)

	elf0 := Elf{}
	linkerpontodeentrada := elf0.Getpontodeentrada(linkerdados)
	elf0.Parse(linkerdados[:], uint32(Páginadiretóriopontodeentrada))

	ligaçãomapa := Ligaçãomapa{}
	ligaçãomapa.Init(memóriagestor)

	var lib1ficheiro []byte = ([]byte)("LIB1")
	tamanho = GetficheiroTamanho(lib1ficheiro)

	lib1Endereço := memóriagestor.Alocar_memória(tamanho)
	lib1dados := GetbytesdePonteiro(uintptr(lib1Endereço), int(tamanho), int(tamanho))
	Ler_ficheiro(lib1ficheiro, lib1dados)

	lib1elf := Elf{}
	lib1elf.Parse(lib1dados[:], uint32(Páginadiretóriopontodeentrada))
	memóriagestor.Livre(lib1Endereço)

	ligaçãomapa.Adicionar_ao_fim_da_lista(uintptr(lib1elf.Dinâmico))

	var lib2ficheiro []byte = ([]byte)("LIB2")
	tamanho = GetficheiroTamanho(lib2ficheiro)

	lib2Endereço := memóriagestor.Alocar_memória(tamanho)
	lib2dados := GetbytesdePonteiro(uintptr(lib2Endereço), int(tamanho), int(tamanho))
	Ler_ficheiro(lib2ficheiro, lib2dados)

	lib2elf := Elf{}
	lib2elf.Parse(lib2dados[:], uint32(Páginadiretóriopontodeentrada))
	memóriagestor.Livre(lib2Endereço)

	ligaçãomapa.Adicionar_ao_fim_da_lista(uintptr(lib2elf.Dinâmico))

	libligaçãomapa := ligaçãomapa.Clone()
	ligaçãomapaEndereço := uint32(uintptr(Pointer(libligaçãomapa.First)))

	lib1got := Getunsignedinteger32matrizdePonteiro(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = ligaçãomapaEndereço
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32matrizdePonteiro(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = ligaçãomapaEndereço
	lib2got[2] = 0x4000000

	console.MImprimirxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Imprimir(lib1elf.Got)
	console.MImprimir(":")
	console.MUnsignedinteger32Imprimir(lib1elf.Dinâmico)

	console.MImprimirxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Imprimir(lib2elf.Got)
	console.MImprimir(":")
	console.MUnsignedinteger32Imprimir(lib2elf.Dinâmico)

	var utilizador1ficheiro []byte = ([]byte)("USER1")
	tamanho = GetficheiroTamanho(utilizador1ficheiro)
	utilizador1Endereço := memóriagestor.Alocar_memória(tamanho)
	utilizador1dados := GetbytesdePonteiro(uintptr(utilizador1Endereço), int(tamanho), int(tamanho))
	Ler_ficheiro(utilizador1ficheiro, utilizador1dados)

	elf2 := Elf{}

	utilizador1pontodeentrada := elf2.Getpontodeentrada(utilizador1dados)
	elf2.Parse(utilizador1dados[:], uint32(Páginadiretóriopontodeentrada+0x1000))
	globalDeslocamentoTabela := elf2.Got

	PValor1ligaçãomapa := ligaçãomapa.Clone()
	PValor1ligaçãomapa.Adicionar_ao_fim_da_lista(uintptr(elf2.Dinâmico))

	memóriagestor.Livre(utilizador1Endereço)

	var code1Ponteiro *uintptr
	var func1val func()

	code1Ponteiro = (*uintptr)(memóriagestor.Alocar_memória(4))
	*code1Ponteiro = uintptr(linkerpontodeentrada)
	func1val = *(*func())(Pointer(&code1Ponteiro))

	proc2 := processohelper.Spawn(func1val, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada+0x1000), false)
	thr2 := (*TFluxoExecução)(proc2.Threads.Getat(0))
	thr2.CpuEstado.Ecx = utilizador1pontodeentrada
	thr2.CpuEstado.Edx = globalDeslocamentoTabela
	thr2.CpuEstado.Esi = uint32(uintptr(Pointer(PValor1ligaçãomapa.First)))

	console.MImprimirxy("user1: ", 1, 10)
	console.MUnsignedinteger32Imprimir(elf2.Got)

	var utilizador2ficheiro []byte = ([]byte)("USER2")
	tamanho = GetficheiroTamanho(utilizador2ficheiro)
	utilizador2Endereço := memóriagestor.Alocar_memória(tamanho)
	utilizador2dados := GetbytesdePonteiro(uintptr(utilizador2Endereço), int(tamanho), int(tamanho))
	Ler_ficheiro(utilizador2ficheiro, utilizador2dados)

	elf3 := Elf{}

	utilizador2pontodeentrada := elf3.Getpontodeentrada(utilizador2dados)
	elf3.Parse(utilizador2dados[:], uint32(Páginadiretóriopontodeentrada+0x2000))
	globalDeslocamentoTabela = elf3.Got

	PValor2ligaçãomapa := ligaçãomapa.Clone()
	PValor2ligaçãomapa.Adicionar_ao_fim_da_lista(uintptr(elf3.Dinâmico))

	memóriagestor.Livre(utilizador2Endereço)

	var code2Ponteiro *uintptr
	var func2val func()

	code2Ponteiro = (*uintptr)(memóriagestor.Alocar_memória(4))
	*code2Ponteiro = uintptr(linkerpontodeentrada)
	func2val = *(*func())(Pointer(&code2Ponteiro))

	proc3 := processohelper.Spawn(func2val, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada+0x2000), false)
	thr3 := (*TFluxoExecução)(proc3.Threads.Getat(0))
	thr3.CpuEstado.Ecx = utilizador2pontodeentrada
	thr3.CpuEstado.Edx = globalDeslocamentoTabela
	thr3.CpuEstado.Esi = uint32(uintptr(Pointer(PValor2ligaçãomapa.First)))

	console.MImprimirxy("user2: ", 1, 11)
	console.MUnsignedinteger32Imprimir(thr3.CpuEstado.Esi)

	libligaçãomapa.Imprimir(1, 11)

	var utilizador3ficheiro []byte = ([]byte)("USER3")
	tamanho = GetficheiroTamanho(utilizador3ficheiro)
	utilizador3Endereço := memóriagestor.Alocar_memória(tamanho)
	utilizador3dados := GetbytesdePonteiro(uintptr(utilizador3Endereço), int(tamanho), int(tamanho))
	Ler_ficheiro(utilizador3ficheiro, utilizador3dados)

	elf4 := Elf{}

	utilizador3pontodeentrada := elf4.Getpontodeentrada(utilizador3dados)
	elf4.Parse(utilizador3dados[:], uint32(Páginadiretóriopontodeentrada+0x3000))
	globalDeslocamentoTabela = elf4.Got

	PValor3ligaçãomapa := ligaçãomapa.Clone()
	PValor3ligaçãomapa.Adicionar_ao_fim_da_lista(uintptr(elf4.Dinâmico))

	memóriagestor.Livre(utilizador3Endereço)

	var code3Ponteiro *uintptr
	var func3val func()

	code3Ponteiro = (*uintptr)(memóriagestor.Alocar_memória(4))
	*code3Ponteiro = uintptr(linkerpontodeentrada)
	func3val = *(*func())(Pointer(&code3Ponteiro))

	proc4 := processohelper.Spawn(func3val, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada+0x3000), false)
	thr4 := (*TFluxoExecução)(proc4.Threads.Getat(0))
	thr4.CpuEstado.Ecx = utilizador3pontodeentrada
	thr4.CpuEstado.Edx = globalDeslocamentoTabela
	thr4.CpuEstado.Esi = uint32(uintptr(Pointer(PValor3ligaçãomapa.First)))

	processohelper.Spawn(TFunção1, fluxoExecuçãohelper, sche, uint32(Páginadiretóriopontodeentrada+0x4000), true)

	itecladoeventohandler = &mytecladoeventohandler
	tecladocontrolador.Initcontrolador(Interrupçãogestor, itecladoeventohandler)

	ratocontrolador.Initcontrolador(Interrupçãogestor, nil)

	mypcicontroladorhandler := TMypcicontroladorhandler{}
	pcicontrolador.Init(mypcicontroladorhandler)
	pcicontrolador.Selecionarcontrolador(&Controladorgestor, Interrupçãogestor)
	dispositivodescriptor = mypcicontroladorhandler.Getcontrolador()

	sche.Ativado(true)
	Interrupçãogestor.Ativo()

	for {
		halt()
	}

}
