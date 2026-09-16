/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package quadro_da_rede_de_meio_partilhado

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "utilitário"

var ethernetconsole TConsole = TConsole{}

type TEthernetquadrocabeçalhobuffer struct {
	destinomacbe	[6]byte
	origemmacbe	[6]byte
	ethernettipobe	[2]byte
}

var quadrocabeçalhoTamanho int = 14

type TCabeçalho_de_quadro_de_rede_de_meio_partilhado struct {
	destinomacbe	uint64
	origemmacbe	uint64
	ethernettipobe	uint16
}

func (próprio *TCabeçalho_de_quadro_de_rede_de_meio_partilhado) Init(buffer_2 TEthernetquadrocabeçalhobuffer) {
	próprio.destinomacbe = (Matrizparaunsignedinteger48(buffer_2.destinomacbe))
	próprio.origemmacbe = (Matrizparaunsignedinteger48(buffer_2.origemmacbe))
	próprio.ethernettipobe = (Matrizparaunsignedinteger16(buffer_2.ethernettipobe))

}
func (próprio *TCabeçalho_de_quadro_de_rede_de_meio_partilhado) Conjuntobuffer(buffer_2 *TEthernetquadrocabeçalhobuffer) {
	buffer_2.destinomacbe = Unsignedinteger48paramatriz(Unsignedinteger48r(próprio.destinomacbe))
	buffer_2.origemmacbe = Unsignedinteger48paramatriz(Unsignedinteger48r(próprio.origemmacbe))
	buffer_2.ethernettipobe = Unsignedinteger16paramatriz(Unsignedinteger16r(próprio.ethernettipobe))
}

type IEthernetquadrohandler interface {
	Init(backend TFornecedor_de_quadros_de_rede_de_meio_partilhado)
	Conjuntohandler(handler IEthernetquadrohandler, ethernettipo uint16)
	Ethernetquadroreceivewhen(dadosPonteiro uintptr, tamanho int) bool
	Enviar(destinomacbe uint64, dadosPonteiro uintptr, tamanho uint32)
	QuadroEnviar(destinomacbe uint64, ethernettipobe uint16, dadosPonteiro uintptr, tamanho uint32)
	Providerget() TFornecedor_de_quadros_de_rede_de_meio_partilhado
	GetmacEndereço() uint64
	GetipEndereço() uint64
}

type TEthernetquadrohandler struct {
}

var quadro TCabeçalho_de_quadro_de_rede_de_meio_partilhado
var Backend TFornecedor_de_quadros_de_rede_de_meio_partilhado
var handler_2 [65535]IEthernetquadrohandler
var efhandler *TEthernetquadrohandler = nil

func (próprio *TEthernetquadrohandler) Init(backend TFornecedor_de_quadros_de_rede_de_meio_partilhado) {
	Backend = backend
}

func (próprio *TEthernetquadrohandler) Conjuntohandler(handler IEthernetquadrohandler, pethernettipo uint16) {
	handler_2[pethernettipo] = handler
}
func (próprio *TEthernetquadrohandler) Conjuntobackend(backend TFornecedor_de_quadros_de_rede_de_meio_partilhado) {
	Backend = backend
}
func (próprio *TEthernetquadrohandler) Getbackend() TFornecedor_de_quadros_de_rede_de_meio_partilhado {
	return Backend
}
func (próprio *TEthernetquadrohandler) Ethernetquadroreceivewhen(dadosPonteiro uintptr, tamanho int) bool {
	ethernetconsole.MImprimir(([]byte)("OnEtherFrameReceived"))
	return false
}
func (próprio *TEthernetquadrohandler) Enviar(destinomacbe uint64, dadosPonteiro uintptr, tamanho uint32) {
	Backend.QuadroEnviar(destinomacbe, quadro.ethernettipobe, dadosPonteiro, tamanho)
}
func (próprio *TEthernetquadrohandler) QuadroEnviar(destinomacbe uint64, ethernettipobe uint16, dadosPonteiro uintptr, tamanho uint32) {
	Backend.QuadroEnviar(destinomacbe, ethernettipobe, dadosPonteiro, tamanho)
}
func (próprio *TEthernetquadrohandler) GetmacEndereço() uint64 {
	return Backend.GetmacEndereço()
}
func (próprio *TEthernetquadrohandler) GetipEndereço() uint64 {
	return Backend.GetipEndereço()
}
func (próprio *TEthernetquadrohandler) Providerget() TFornecedor_de_quadros_de_rede_de_meio_partilhado {
	return Backend
}

type TEthernetquadrorawdadoshandler struct {
	TRawdadoshandler
}

var provider TFornecedor_de_quadros_de_rede_de_meio_partilhado

func (próprio *TEthernetquadrorawdadoshandler) Init(pprovider TFornecedor_de_quadros_de_rede_de_meio_partilhado, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (próprio *TEthernetquadrorawdadoshandler) Aorawdadosreceive(dadosPonteiro uintptr, tamanho int) bool {
	return provider.Aorawdadosreceive(dadosPonteiro, tamanho)
}
func (próprio *TEthernetquadrorawdadoshandler) Enviar(dadosPonteiro uintptr, tamanho uint32) {
	provider.Enviar(dadosPonteiro, tamanho)
}
func (próprio *TEthernetquadrorawdadoshandler) GetmacEndereço() uint64 {
	return provider.GetmacEndereço()
}
func (próprio *TEthernetquadrorawdadoshandler) GetipEndereço() uint64 {
	return provider.GetipEndereço()
}
func (próprio *TEthernetquadrorawdadoshandler) Providerget() TFornecedor_de_quadros_de_rede_de_meio_partilhado {
	return provider
}

type TFornecedor_de_quadros_de_rede_de_meio_partilhado struct {
	redeCartas	Tamdam79c973
	handler_2	[65565]IEthernetquadrohandler
}

func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) Init(backend Tamdam79c973) {

	próprio.redeCartas = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		próprio.handler_2[i] = nil
	}
}

var contar uint16 = 0

func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) Aorawdadosreceive(dadosPonteiro uintptr, tamanho int) bool {

	var buffer_2 *TEthernetquadrocabeçalhobuffer = (*TEthernetquadrocabeçalhobuffer)(Pointer(dadosPonteiro))
	var quadro TCabeçalho_de_quadro_de_rede_de_meio_partilhado = TCabeçalho_de_quadro_de_rede_de_meio_partilhado{}
	quadro.Init(*buffer_2)
	var reply bool = false

	if quadro.destinomacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(quadro.destinomacbe) == próprio.GetmacEndereço() {
		if handler_2[quadro.ethernettipobe] != nil {
			ethernetconsole.MImprimir(([]byte)("provider\n"))

			var referência_de_memória uintptr = uintptr(Pointer(dadosPonteiro)) + uintptr(quadrocabeçalhoTamanho)
			reply = handler_2[quadro.ethernettipobe].Ethernetquadroreceivewhen(referência_de_memória, tamanho-quadrocabeçalhoTamanho)

		}
	}

	if reply {
		quadro.destinomacbe = quadro.origemmacbe
		quadro.origemmacbe = Unsignedinteger48r(próprio.GetmacEndereço())
		quadro.Conjuntobuffer(buffer_2)

	}

	ethernetconsole.MImprimirxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Imprimir(quadro.origemmacbe)
	ethernetconsole.MImprimir(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Imprimir(quadro.destinomacbe)
	ethernetconsole.MImprimir(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Imprimir(próprio.GetmacEndereço())
	ethernetconsole.MImprimir(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Imprimir(quadro.ethernettipobe)
	ethernetconsole.MImprimir(([]byte)("]"))

	return reply

}
func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) Enviar(dadosPonteiro uintptr, tamanho uint32) {
	próprio.redeCartas.Enviar(dadosPonteiro, tamanho)
}
func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) QuadroEnviar(destinomacbe uint64, ethernettipobe uint16, dadosPonteiro uintptr, tamanho uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetquadrocabeçalhobuffer = (*TEthernetquadrocabeçalhobuffer)(Pointer(&buffer2_2))

	var quadro TCabeçalho_de_quadro_de_rede_de_meio_partilhado = TCabeçalho_de_quadro_de_rede_de_meio_partilhado{}
	quadro.Init(*buffer_2)

	quadro.destinomacbe = Unsignedinteger48r(destinomacbe)
	quadro.origemmacbe = Unsignedinteger48r(próprio.redeCartas.GetmacEndereço())
	quadro.ethernettipobe = Unsignedinteger16r(ethernettipobe)

	quadro.Conjuntobuffer(buffer_2)
	var origem_2 [4096]byte = *(*([4096]byte))(Pointer(dadosPonteiro))

	var i uint32 = 0
	for i = 0; i < tamanho; i++ {
		buffer2_2[uint32(quadrocabeçalhoTamanho)+i] = origem_2[i]

	}

	var referência_de_memória uintptr = uintptr(Pointer(&buffer2_2))

	próprio.redeCartas.Enviar(referência_de_memória, tamanho+uint32(quadrocabeçalhoTamanho))

}
func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) GetmacEndereço() uint64 {
	return próprio.redeCartas.GetmacEndereço()
}
func (próprio *TFornecedor_de_quadros_de_rede_de_meio_partilhado) GetipEndereço() uint64 {
	return próprio.redeCartas.GetipEndereço()
}
