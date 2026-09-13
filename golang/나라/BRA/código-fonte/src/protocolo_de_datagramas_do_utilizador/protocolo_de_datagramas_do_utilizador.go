package protocolo_de_datagramas_do_utilizador

import . "unsafe"
import . "console"
import . "utilitário"
import . "memóriagestor"
import . "protocolo_de_rede_interligada_4"

var udpconsole = TConsole{}

type TUtilizadordatagramprotocolcabeçalhobuffer struct {
	número_da_porta_de_origem	[2]byte
	número_da_porta_de_destino	[2]byte

	duração		[2]byte
	checksum	[2]byte
}

var udpcabeçalhoTamanho uint32 = 8

type TCabeçalho_de_datagramas_do_utilizador struct {
	número_da_porta_de_origem	uint16
	número_da_porta_de_destino	uint16

	duração		uint16
	checksum	uint16
}

func (próprio *TCabeçalho_de_datagramas_do_utilizador) Init(buffer_2 *TUtilizadordatagramprotocolcabeçalhobuffer) {
	próprio.número_da_porta_de_origem = Matrizparaunsignedinteger16(buffer_2.número_da_porta_de_origem)
	próprio.número_da_porta_de_destino = Matrizparaunsignedinteger16(buffer_2.número_da_porta_de_destino)

	próprio.duração = Matrizparaunsignedinteger16(buffer_2.duração)
	próprio.checksum = Matrizparaunsignedinteger16(buffer_2.checksum)
}
func (próprio *TCabeçalho_de_datagramas_do_utilizador) Conjuntobuffer(buffer_2 *TUtilizadordatagramprotocolcabeçalhobuffer) {

	buffer_2.número_da_porta_de_origem = Unsignedinteger16paramatriz(próprio.número_da_porta_de_origem)
	buffer_2.número_da_porta_de_destino = Unsignedinteger16paramatriz(próprio.número_da_porta_de_destino)

	buffer_2.duração = Unsignedinteger16paramatriz(próprio.duração)
	buffer_2.checksum = Unsignedinteger16paramatriz(próprio.checksum)

}

type IUtilizadordatagramprotocolhandler interface {
	ManípuloutilizadordatagramprotocolMensagem(conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador, dados uintptr, tamanho uint16)
}

type TUtilizadordatagramprotocolhandler struct {
}

func (próprio *TUtilizadordatagramprotocolhandler) Init(backend TFornecedor_do_protocolo_de_rede_interligada) {
}
func (próprio *TUtilizadordatagramprotocolhandler) ManípuloutilizadordatagramprotocolMensagem(conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador, dados uintptr, tamanho uint16) {
}

type IUtilizadordatagramprotocolconectorRede interface {
	ManípuloutilizadordatagramprotocolMensagem(dados uintptr, tamanho uint16)
}
type TExtremo_de_comunicação_de_datagramas_do_utilizador struct {
	remotosportoNúmero	uint16
	remotosip		uint32
	localportoNúmero	uint16
	localip			uint32

	listening	bool
}

var udpprovider TUtilizadordatagramprotocolprovider
var udphandler IUtilizadordatagramprotocolhandler

func (próprio *TExtremo_de_comunicação_de_datagramas_do_utilizador) Testar() {
}
func (próprio *TExtremo_de_comunicação_de_datagramas_do_utilizador) Init(pudpprovider TUtilizadordatagramprotocolprovider, pudphandler IUtilizadordatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	próprio.listening = false
}
func (próprio *TExtremo_de_comunicação_de_datagramas_do_utilizador) ManípuloutilizadordatagramprotocolMensagem(dados uintptr, tamanho uint16) {
	if udphandler != nil {
		udphandler.ManípuloutilizadordatagramprotocolMensagem(próprio, dados, tamanho)
	}
}
func (próprio *TExtremo_de_comunicação_de_datagramas_do_utilizador) Enviar(pdados []byte, tamanho uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(tamanho); i++ {
		buffer_2[i] = pdados[i]
	}
	var dados = uintptr(Pointer(&buffer_2))
	udpprovider.Enviar(próprio, dados, tamanho)
}
func (próprio *TExtremo_de_comunicação_de_datagramas_do_utilizador) Desligar() {
	udpprovider.Desligar(próprio)
}

type TUtilizadordatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TExtremo_de_comunicação_de_datagramas_do_utilizador
var númerosockets int
var livreporto uint16

func (próprio *TUtilizadordatagramprotocolprovider) Init(pipprovider TFornecedor_do_protocolo_de_rede_interligada, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	númerosockets = 0
	livreporto = 1024
}
func (próprio *TUtilizadordatagramprotocolprovider) Internetprotocolreceivewhen(origemipEndereçoredeoctetoorder uint32, destinoipEndereçoredeoctetoorder uint32, internetprotocolpayload uintptr, tamanho uint32) bool {
	if tamanho < udpcabeçalhoTamanho {
		return false
	}

	var buffer_2 *TUtilizadordatagramprotocolcabeçalhobuffer = (*TUtilizadordatagramprotocolcabeçalhobuffer)(Pointer(internetprotocolpayload))
	var msg TCabeçalho_de_datagramas_do_utilizador
	msg.Init(buffer_2)

	var conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador = nil

	for i := 0; i < númerosockets && conectorRede == nil; i++ {
		if sockets[i].localportoNúmero == msg.número_da_porta_de_destino && sockets[i].localip == destinoipEndereçoredeoctetoorder && sockets[i].listening == true {
			conectorRede = &sockets[i]
			conectorRede.listening = false
			conectorRede.remotosportoNúmero = msg.número_da_porta_de_origem
			conectorRede.remotosip = origemipEndereçoredeoctetoorder
		} else if sockets[i].localportoNúmero == msg.número_da_porta_de_destino && sockets[i].localip == destinoipEndereçoredeoctetoorder && sockets[i].remotosportoNúmero == msg.número_da_porta_de_origem && sockets[i].remotosip == origemipEndereçoredeoctetoorder {
			conectorRede = &sockets[i]

		}
	}

	msg.Conjuntobuffer(buffer_2)
	if conectorRede != nil {
		conectorRede.ManípuloutilizadordatagramprotocolMensagem(internetprotocolpayload+uintptr(udpcabeçalhoTamanho), uint16(tamanho-udpcabeçalhoTamanho))
	}

	return false
}

func (próprio *TUtilizadordatagramprotocolprovider) Ligar(ip uint32, porto uint16) *TExtremo_de_comunicação_de_datagramas_do_utilizador {
	var memóriagestor = &TMemóriagestor{}
	var conectorRede = (*TExtremo_de_comunicação_de_datagramas_do_utilizador)(memóriagestor.Alocar_memória(50))

	if conectorRede != nil {

		conectorRede.Init(*próprio, nil)
		conectorRede.remotosportoNúmero = porto
		conectorRede.remotosip = ip
		conectorRede.localportoNúmero = livreporto
		livreporto++
		conectorRede.localip = uint32((*iphandler.Providerget()).GetipEndereço())

		conectorRede.remotosportoNúmero = Unsignedinteger16r(conectorRede.remotosportoNúmero)
		conectorRede.localportoNúmero = Unsignedinteger16r(conectorRede.localportoNúmero)

		sockets[númerosockets] = *conectorRede
		númerosockets++

	}
	return conectorRede

}
func (próprio *TUtilizadordatagramprotocolprovider) Listen(porto uint16) *TExtremo_de_comunicação_de_datagramas_do_utilizador {
	var conectorRede = &TExtremo_de_comunicação_de_datagramas_do_utilizador{}
	conectorRede = nil
	if conectorRede != nil {
		conectorRede.Init(*próprio, nil)
		conectorRede.listening = true
		conectorRede.localportoNúmero = porto
		conectorRede.localip = uint32((*iphandler.Providerget()).GetipEndereço())

		conectorRede.localportoNúmero = Unsignedinteger16r(conectorRede.localportoNúmero)
	}
	return conectorRede
}
func (próprio *TUtilizadordatagramprotocolprovider) Desligar(conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador) {
	for i := 0; i < númerosockets && conectorRede == nil; i++ {
		if sockets[i] == *conectorRede {
			númerosockets--
			sockets[i] = sockets[númerosockets]
			break
		}
	}
}
func (próprio *TUtilizadordatagramprotocolprovider) Enviar(conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador, pdados uintptr, tamanho uint16) {
	var totalDuração = uint32(tamanho) + udpcabeçalhoTamanho

	var buffer_2 [4096]byte

	var msgbuffer = (*TUtilizadordatagramprotocolcabeçalhobuffer)(Pointer(&buffer_2))

	var msg = TCabeçalho_de_datagramas_do_utilizador{}

	msg.número_da_porta_de_origem = conectorRede.localportoNúmero
	msg.número_da_porta_de_destino = conectorRede.remotosportoNúmero
	msg.duração = Unsignedinteger16r(uint16(totalDuração))

	msg.checksum = 0x0
	msg.Conjuntobuffer(msgbuffer)

	var dadosbytes [4096]byte = *(*[4096]byte)(Pointer(pdados))
	for i := 0; i < int(tamanho); i++ {
		buffer_2[int(udpcabeçalhoTamanho)+i] = dadosbytes[i]
	}

	var dados uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Enviar(conectorRede.remotosip, 0x11, dados, totalDuração)

}
func (próprio *TUtilizadordatagramprotocolprovider) Vincular(conectorRede *TExtremo_de_comunicação_de_datagramas_do_utilizador, handler *TUtilizadordatagramprotocolhandler) {
}
