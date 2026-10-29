/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocolo_de_mensagens_de_controlo_de_rede_interligada

import . "unsafe"
import . "console"
import . "memóriagestor"
import . "quadro_da_rede_de_meio_partilhado"
import . "protocolo_de_rede_interligada_4"
import . "utilitário"

var icmpconsole = TConsole{}

type TInternetControloMensagemprotocolMensagembuffer struct {
	Tipo	byte
	code	byte

	checksum	[2]byte
	dados		[4]byte
}

var icmpTamanho int = 64

type TInternetControloMensagemprotocolMensagem struct {
	Tipo	uint8
	code	uint8

	checksum	uint16
	dados		uint32
}

func (próprio *TInternetControloMensagemprotocolMensagem) Init(buffer_2 TInternetControloMensagemprotocolMensagembuffer) {
	próprio.Tipo = buffer_2.Tipo
	próprio.code = buffer_2.code

	próprio.checksum = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.checksum))
	próprio.dados = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer_2.dados))
}

func (próprio *TInternetControloMensagemprotocolMensagem) Conjuntobuffer(buffer_2 *TInternetControloMensagemprotocolMensagembuffer) {
	buffer_2.Tipo = próprio.Tipo
	buffer_2.code = próprio.code

	buffer_2.checksum = Unsignedinteger16paramatriz(próprio.checksum)
	buffer_2.dados = Unsignedinteger32paramatriz(próprio.dados)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protocolo_de_mensagens_de_controlo_de_rede_interligada *TProtocolo_de_mensagens_de_controlo_de_rede_interligada

func (próprio *Icmphandler) Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder uint32, destinoipEndereçoredeoctetoorder uint32, dadosPonteiro uintptr, tamanho uint32) bool {
	return protocolo_de_mensagens_de_controlo_de_rede_interligada.Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder, destinoipEndereçoredeoctetoorder, dadosPonteiro, tamanho)
}

var iphandler IInternetprotocolhandler

type TProtocolo_de_mensagens_de_controlo_de_rede_interligada struct {
}

func (próprio *TProtocolo_de_mensagens_de_controlo_de_rede_interligada) Init(backend TFornecedor_do_protocolo_de_rede_interligada, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protocolo_de_mensagens_de_controlo_de_rede_interligada = próprio
}
func (próprio *TProtocolo_de_mensagens_de_controlo_de_rede_interligada) Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder uint32, destinoipEndereçoredeoctetoorder uint32, dadosPonteiro uintptr, tamanho uint32) bool {
	if tamanho < uint32(icmpTamanho) {
		return false
	}

	var buffer_2 *TInternetControloMensagemprotocolMensagembuffer = (*TInternetControloMensagemprotocolMensagembuffer)(Pointer(dadosPonteiro))
	var msg TInternetControloMensagemprotocolMensagem = TInternetControloMensagemprotocolMensagem{}
	msg.Init(*buffer_2)

	icmpconsole.MImprimir(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Imprimir(uint16(msg.Tipo))
	icmpconsole.MImprimir(([]byte)(":"))

	switch msg.Tipo {
	case 0:
		icmpconsole.MImprimir(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MImprimir(([]byte)("ping send "))
		msg.Tipo = 0

		msg.checksum = 0
		msg.Conjuntobuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dadosPonteiro)), uint32(icmpTamanho))

		msg.Conjuntobuffer(buffer_2)

		return true
		break
	}
	return false
}

func (próprio *TProtocolo_de_mensagens_de_controlo_de_rede_interligada) EchorequestEnviar(ipredeoctetoorder uint32) bool {
	var protocolo_de_mensagens_de_controlo_de_rede_interligada TInternetControloMensagemprotocolMensagem = TInternetControloMensagemprotocolMensagem{}

	var memóriagestor = &TMemóriagestor{}
	var buffer_2 = (*TInternetControloMensagemprotocolMensagembuffer)(memóriagestor.Alocar_memória(1024))

	protocolo_de_mensagens_de_controlo_de_rede_interligada.Tipo = 8
	protocolo_de_mensagens_de_controlo_de_rede_interligada.code = 0
	protocolo_de_mensagens_de_controlo_de_rede_interligada.dados = 0x3713
	protocolo_de_mensagens_de_controlo_de_rede_interligada.checksum = 0
	protocolo_de_mensagens_de_controlo_de_rede_interligada.Conjuntobuffer(buffer_2)
	protocolo_de_mensagens_de_controlo_de_rede_interligada.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpTamanho))
	protocolo_de_mensagens_de_controlo_de_rede_interligada.Conjuntobuffer(buffer_2)

	var dadosPonteiro uintptr = uintptr(Pointer(buffer_2))
	iphandler.Enviar(ipredeoctetoorder, 0x01, dadosPonteiro, uint32(icmpTamanho))

	return false

}
