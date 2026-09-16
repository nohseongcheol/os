/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocolo_de_rede_interligada_4

import . "unsafe"
import . "utilitário"
import . "console"
import . "quadro_da_rede_de_meio_partilhado"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Mensagembuffer struct {
	lenver		byte
	tos		byte
	totalDuração	[2]byte

	ident			[2]byte
	parâmetroseDeslocamento	[2]byte

	horaparalive	byte
	protocol	byte
	checksum	[2]byte

	origemipEndereço	[4]byte
	destinoipEndereço	[4]byte
}

var ipTamanho uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Mensagem struct {
	cabeçalhoDuração	uint8
	versão			uint8
	tos			uint8
	totalDuração		uint16

	ident			uint16
	parâmetroseDeslocamento	uint16

	horaparalive	uint8
	protocol	uint8
	checksum	uint16

	origemipEndereço	uint32
	destinoipEndereço	uint32
}

func (próprio *TInternetprotocolv4Mensagem) Init(buffer_2 TInternetprotocolv4Mensagembuffer) {

	próprio.versão = ((buffer_2.lenver & 0xF0) >> 4)
	próprio.cabeçalhoDuração = buffer_2.lenver & 0x0F
	próprio.tos = buffer_2.tos
	próprio.totalDuração = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.totalDuração))

	próprio.ident = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.ident))
	próprio.parâmetroseDeslocamento = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.parâmetroseDeslocamento))

	próprio.horaparalive = buffer_2.horaparalive
	próprio.protocol = buffer_2.protocol
	próprio.checksum = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.checksum))

	próprio.origemipEndereço = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer_2.origemipEndereço))
	próprio.destinoipEndereço = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer_2.destinoipEndereço))

}
func (próprio *TInternetprotocolv4Mensagem) Conjuntobuffer(buffer_2 *TInternetprotocolv4Mensagembuffer) {

	buffer_2.lenver = byte(((próprio.versão & 0x0F) << 4) | (próprio.cabeçalhoDuração & 0x0F))
	buffer_2.tos = próprio.tos
	buffer_2.totalDuração = Unsignedinteger16paramatriz(próprio.totalDuração)

	buffer_2.ident = Unsignedinteger16paramatriz(próprio.ident)
	buffer_2.parâmetroseDeslocamento = Unsignedinteger16paramatriz(próprio.parâmetroseDeslocamento)

	buffer_2.horaparalive = próprio.horaparalive
	buffer_2.protocol = próprio.protocol
	buffer_2.checksum = Unsignedinteger16paramatriz(próprio.checksum)

	buffer_2.origemipEndereço = Unsignedinteger32paramatriz(próprio.origemipEndereço)
	buffer_2.destinoipEndereço = Unsignedinteger32paramatriz(próprio.destinoipEndereço)

}

type IInternetprotocolhandler interface {
	Init(backend TFornecedor_do_protocolo_de_rede_interligada, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder uint32, destinoipEndereçoredeoctetoorder uint32, dadosPonteiro uintptr, tamanho uint32) bool
	Enviar(destinoipEndereçoredeoctetoorder uint32, pprotocol uint8, dadosPonteiro uintptr, tamanho uint32)
	Providerget() *TFornecedor_do_protocolo_de_rede_interligada
}

type TInternetprotocolhandler struct {
}

var ipethernetquadrohandler Ipethernetquadrohandler = Ipethernetquadrohandler{}
var protocol uint8

func (próprio *TInternetprotocolhandler) Init(backend TFornecedor_do_protocolo_de_rede_interligada, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (próprio *TInternetprotocolhandler) Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder uint32, destinoipEndereçoredeoctetoorder uint32, dadosPonteiro uintptr, tamanho uint32) bool {
	ipconsole.MImprimir(([]byte)("ipHandler:OnInternet"))
	return false
}
func (próprio *TInternetprotocolhandler) Enviar(destinoipEndereçoredeoctetoorder uint32, pprotocol uint8, dadosPonteiro uintptr, tamanho uint32) {

	fornecedor_do_protocolo_de_rede_interligada.Enviar(destinoipEndereçoredeoctetoorder, pprotocol, dadosPonteiro, tamanho)
}
func (próprio *TInternetprotocolhandler) Providerget() *TFornecedor_do_protocolo_de_rede_interligada {
	return &fornecedor_do_protocolo_de_rede_interligada
}

type Ipethernetquadrohandler struct {
	TEthernetquadrohandler
}

var fornecedor_do_protocolo_de_rede_interligada TFornecedor_do_protocolo_de_rede_interligada

func (próprio *Ipethernetquadrohandler) Ethernetquadroreceivewhen(dadosPonteiro uintptr, tamanho int) bool {
	ipconsole.MImprimir(([]byte)("iphandler:onEtherfameRecv\n"))
	return fornecedor_do_protocolo_de_rede_interligada.Ethernetquadroreceivewhen(dadosPonteiro, uint32(tamanho))

}

func (próprio *Ipethernetquadrohandler) Enviar(destinoipEndereçoredeoctetoorder uint64, dadosPonteiro uintptr, tamanho uint32) {
	ipconsole.MImprimir(([]byte)("ipefhandler:send\n"))
	var ethernettipobe = Unsignedinteger16r(0x0800)
	próprio.TEthernetquadrohandler.QuadroEnviar(destinoipEndereçoredeoctetoorder, ethernettipobe, dadosPonteiro, tamanho)

}

var handler_2 [255]IInternetprotocolhandler

type TFornecedor_do_protocolo_de_rede_interligada struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMáscara	uint32
}

var efhandler IEthernetquadrohandler

func (próprio *TFornecedor_do_protocolo_de_rede_interligada) Init(pefprovider TFornecedor_de_quadros_de_rede_de_meio_partilhado, pefhandler IEthernetquadrohandler, arp Arpprovider, gatewayip uint32, subnetMáscara uint32) {

	efhandler = pefhandler
	efhandler.Conjuntohandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	próprio.arpprovider = arp
	próprio.Gatewayip = gatewayip
	próprio.SubnetMáscara = subnetMáscara
	fornecedor_do_protocolo_de_rede_interligada = *próprio
}
func (próprio *TFornecedor_do_protocolo_de_rede_interligada) Ethernetquadroreceivewhen(ethernetquadropayload uintptr, tamanho uint32) bool {
	if tamanho < uint32(ipTamanho) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Mensagembuffer = (*TInternetprotocolv4Mensagembuffer)(Pointer(ethernetquadropayload))
	var internetprotocolMensagem TInternetprotocolv4Mensagem
	internetprotocolMensagem.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMensagem.destinoipEndereço == uint32(efhandler.GetipEndereço()) {

		var duração uint32 = uint32(internetprotocolMensagem.totalDuração)
		if duração > tamanho {
			duração = tamanho
		}
		if handler_2[internetprotocolMensagem.protocol] != nil {
			reply = handler_2[internetprotocolMensagem.protocol].Internetprotocolreceivewhen(internetprotocolMensagem.origemipEndereço, internetprotocolMensagem.destinoipEndereço, ethernetquadropayload+uintptr(4*internetprotocolMensagem.cabeçalhoDuração), uint32(duração-uint32(4*internetprotocolMensagem.cabeçalhoDuração)))

		}
	}

	if reply {

		var temporary = internetprotocolMensagem.destinoipEndereço
		internetprotocolMensagem.destinoipEndereço = internetprotocolMensagem.origemipEndereço
		internetprotocolMensagem.origemipEndereço = temporary

		internetprotocolMensagem.horaparalive = 0x40
		internetprotocolMensagem.checksum = 0

		internetprotocolMensagem.Conjuntobuffer(buffer_2)
		internetprotocolMensagem.checksum = próprio.Checksum((*([4096]uint16))(Pointer(ethernetquadropayload)), uint32(4*internetprotocolMensagem.cabeçalhoDuração))

		internetprotocolMensagem.Conjuntobuffer(buffer_2)

	}

	ipconsole.MImprimir(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Imprimir(internetprotocolMensagem.origemipEndereço)
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MUnsignedinteger32Imprimir(internetprotocolMensagem.destinoipEndereço)
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimir(uint16(internetprotocolMensagem.cabeçalhoDuração))
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimir(uint16(internetprotocolMensagem.versão))
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimir(internetprotocolMensagem.totalDuração)
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MUnsignedinteger32Imprimir(uint32(efhandler.GetipEndereço()))
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MImprimir(([]byte)("\n"))

	return reply

}
func (próprio *TFornecedor_do_protocolo_de_rede_interligada) Enviar(destinoipEndereçoredeoctetoorder uint32, protocol uint8, dadosPonteiro uintptr, tamanho uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Mensagembuffer = (*TInternetprotocolv4Mensagembuffer)(Pointer(&buffer1_2))
	var mensagem TInternetprotocolv4Mensagem = TInternetprotocolv4Mensagem{}
	mensagem.versão = 4
	mensagem.cabeçalhoDuração = ipTamanho / 4
	mensagem.tos = 0
	mensagem.totalDuração = Unsignedinteger16r(uint16(tamanho + uint32(ipTamanho)))

	mensagem.ident = 0x0100
	mensagem.parâmetroseDeslocamento = 0x0040
	mensagem.horaparalive = 0x40
	mensagem.protocol = protocol

	mensagem.destinoipEndereço = destinoipEndereçoredeoctetoorder

	mensagem.origemipEndereço = uint32(efhandler.GetipEndereço())

	mensagem.checksum = 0

	mensagem.Conjuntobuffer(buffer_2)
	mensagem.checksum = próprio.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipTamanho))
	mensagem.Conjuntobuffer(buffer_2)

	var dadosbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dadosPonteiro))

	for i := 0; i < int(tamanho); i++ {

		buffer1_2[i+int(ipTamanho)] = dadosbuffer_2[i]
	}

	ipconsole.MImprimirxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(tamanho)+int(ipTamanho); i++ {
		ipconsole.MHexadecimalImprimir(buffer1_2[i])
	}
	ipconsole.MImprimir(([]byte)(":"))
	ipconsole.MImprimir(([]byte)("]\n"))

	var seguintehopipEndereçoredeoctetoorder uint32 = destinoipEndereçoredeoctetoorder
	if (destinoipEndereçoredeoctetoorder & próprio.SubnetMáscara) != (mensagem.origemipEndereço & próprio.SubnetMáscara) {
		seguintehopipEndereçoredeoctetoorder = próprio.Gatewayip
	}

	var enviardadosPonteiro = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Imprimir(seguintehopipEndereçoredeoctetoorder)

	var ethernettipobe = Unsignedinteger16r(0x0800)
	efhandler.QuadroEnviar(próprio.arpprovider.Resolver(seguintehopipEndereçoredeoctetoorder), ethernettipobe, enviardadosPonteiro, uint32(ipTamanho)+uint32(tamanho))

}
func (próprio *TFornecedor_do_protocolo_de_rede_interligada) Checksum(pdados *[4096]uint16, duraçãoEntradabytes uint32) uint16 {
	var dados [4096]uint16 = *pdados
	var temporary uint32 = 0
	var dadosbytes [4096]byte = *(*([4096]byte))(Pointer(&dados))
	if (duraçãoEntradabytes % 2) != 0 {
		temporary += uint32(uint16(dadosbytes[duraçãoEntradabytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (próprio *TFornecedor_do_protocolo_de_rede_interligada) GetipEndereço() uint64 {
	return efhandler.GetipEndereço()
}
