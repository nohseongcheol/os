package amdam79c973

import . "unsafe"
import . "interrupção"
import . "console"
import . "porto"
import . "pci"

var redeCartasconsole TConsole = TConsole{}

type TInitializationBloco struct {
	modo			uint16
	númeroEnviarbuffer	uint8
	númerorecvbuffer	uint8

	físicoEndereço	uint64

	lógicosEndereço			uint64
	recvbufferDescriçãoEndereço	uintptr
	enviarbufferDescriçãoEndereço	uintptr
}
type TBufferdescriptor struct {
	endereço_2	uint32
	parâmetros	uint32
	parâmetros2	uint32
	disponível	uint32
}

type IRawdadoshandler interface {
	Aorawdadosreceive(dadosPonteiro uintptr, tamanho int) bool
	Enviar(dadosPonteiro uintptr, tamanho uint32)
}

var rawdadosbackend Tamdam79c973

type TRawdadoshandler struct {
}

func (próprio *TRawdadoshandler) Conjuntobackend(backend Tamdam79c973) {

	rawdadosbackend = backend
}
func (próprio *TRawdadoshandler) Getbackend() Tamdam79c973 {
	return rawdadosbackend
}
func (próprio *TRawdadoshandler) Aorawdadosreceive(dadosPonteiro uintptr, tamanho int) bool {
	redeCartasconsole.MImprimirxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (próprio *TRawdadoshandler) Enviar(dadosPonteiro uintptr, tamanho uint32) {
	redeCartasconsole.MImprimirxy(([]byte)("TRawDataSend"), 10, 10)
	rawdadosbackend.Enviar(dadosPonteiro, tamanho)
}

var MacEndereço0porto uint16
var MacEndereço2porto uint16
var MacEndereço4porto uint16
var registodadosporto uint16
var registoEndereçoporto uint16
var reporporto uint16
var busControloregistodadosporto uint16

var initBloco TInitializationBloco

var enviarbufferDescrição [8]TBufferdescriptor
var enviarbufferDescriçãomemória [2048 + 15]byte
var enviarbuffer [2*1024 + 15][8]uint8
var atualEnviarbuffer uint8

var recvbufferDescrição [8]TBufferdescriptor
var recvbufferDescriçãomemória [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var atualrecvbuffer uint8
var funcValor func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TInterrupçãohandler
	dispositivodescriptor	TPeripheralcomponentinterconnectDispositivodescriptor
	interrupção		*TInterrupçãogestor
	handler			*TRawdadoshandler
}

var console_2 TConsole = TConsole{}
var irawdadoshandler IRawdadoshandler

func (próprio *Tamdam79c973) Initcontrolador(interrupção *TInterrupçãogestor, dispositivodescriptor TPeripheralcomponentinterconnectDispositivodescriptor, handler IRawdadoshandler) {

	próprio.dispositivodescriptor = dispositivodescriptor

	funcValor = (*Tamdam79c973).Manípulointerrupção
	var endereço uintptr
	endereço = uintptr(Pointer(&funcValor))

	próprio.Init(uint8(0x20+dispositivodescriptor.Interrupção), uintptr(Pointer(interrupção)), endereço)

	MacEndereço0porto = uint16(dispositivodescriptor.Portobase)
	MacEndereço2porto = uint16(dispositivodescriptor.Portobase) + 0x02
	MacEndereço4porto = uint16(dispositivodescriptor.Portobase) + 0x04
	registodadosporto = uint16(dispositivodescriptor.Portobase) + 0x10
	registoEndereçoporto = uint16(dispositivodescriptor.Portobase) + 0x12
	reporporto = uint16(dispositivodescriptor.Portobase) + 0x14
	busControloregistodadosporto = uint16(dispositivodescriptor.Portobase) + 0x16

	irawdadoshandler = &TRawdadoshandler{}
	if handler != nil {
		irawdadoshandler = handler
	}

	atualEnviarbuffer = 0
	atualrecvbuffer = 0

	var Mac0 uint64 = uint64(Portolerpalavra(MacEndereço0porto) % 256)
	var Mac1 uint64 = uint64(Portolerpalavra(MacEndereço0porto) / 256)
	var Mac2 uint64 = uint64(Portolerpalavra(MacEndereço2porto) % 256)
	var Mac3 uint64 = uint64(Portolerpalavra(MacEndereço2porto) / 256)
	var Mac4 uint64 = uint64(Portolerpalavra(MacEndereço4porto) % 256)
	var Mac5 uint64 = uint64(Portolerpalavra(MacEndereço4porto) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macEndereço uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MImprimirxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalImprimir(uint8(dispositivodescriptor.Interrupção))
	console_2.MImprimir(([]byte)("]"))
	console_2.MImprimir(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Imprimir(uint16(macEndereço >> 32))
	console_2.MUnsignedinteger32Imprimir(uint32(macEndereço & 0x00000000FFFFFFFF))
	console_2.MImprimir(([]byte)("]"))

	Portoescreverpalavra(registoEndereçoporto, 20)
	Portoescreverpalavra(busControloregistodadosporto, 0x102)

	Portoescreverpalavra(registoEndereçoporto, 0)
	Portoescreverpalavra(registodadosporto, 0x04)

	initBloco.modo = 0x0000
	initBloco.númeroEnviarbuffer = 3
	initBloco.númerorecvbuffer = 3

	initBloco.físicoEndereço = Mac

	initBloco.lógicosEndereço = 0

	enviarbufferDescrição = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&enviarbufferDescriçãomemória)) + 15) & ^(uintptr)(0xF)))
	initBloco.enviarbufferDescriçãoEndereço = uintptr(Pointer(&enviarbufferDescrição))
	recvbufferDescrição = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferDescriçãomemória)) + 15) & ^(uintptr)(0xF)))
	initBloco.recvbufferDescriçãoEndereço = uintptr(Pointer(&recvbufferDescrição))

	for i := 0; i < 8; i++ {
		enviarbufferDescrição[i].endereço_2 = uint32((uintptr(Pointer(&enviarbuffer[i])) + 15) & ^(uintptr(0xF)))
		enviarbufferDescrição[i].parâmetros = 0x7FF | 0xF000
		enviarbufferDescrição[i].parâmetros2 = 0
		enviarbufferDescrição[i].disponível = 0

		recvbufferDescrição[i].endereço_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferDescrição[i].parâmetros = 0xF7FF | 0x80000000

	}

	Portoescreverpalavra(registoEndereçoporto, 1)
	Portoescreverpalavra(registodadosporto, uint16(uintptr(Pointer(&initBloco))&0xFFFF))

	Portoescreverpalavra(registoEndereçoporto, 2)
	Portoescreverpalavra(registodadosporto, uint16((uintptr(Pointer(&initBloco))>>16)&0xFFFF))

}
func (próprio *Tamdam79c973) Ativar() {
	Portoescreverpalavra(registoEndereçoporto, 0)
	Portoescreverpalavra(registodadosporto, 0x41)

	Portoescreverpalavra(registoEndereçoporto, 4)
	temporary := Portolerpalavra(registodadosporto)
	Portoescreverpalavra(registoEndereçoporto, 4)
	Portoescreverpalavra(registodadosporto, temporary|0xC00)

	Portoescreverpalavra(registoEndereçoporto, 0)
	Portoescreverpalavra(registodadosporto, 0x42)

}
func (próprio *Tamdam79c973) Repor() int {
	Portolerpalavra(reporporto)
	Portoescreverpalavra(reporporto, 0)
	return 10
}

var contar uint16 = 0

func (próprio *Tamdam79c973) Manípulointerrupção(esp uint32) uint32 {

	Portoescreverpalavra(registoEndereçoporto, 0)
	temporary := uint32(Portolerpalavra(registodadosporto))
	console_2.MImprimir(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Imprimir(esp)
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimir(temporary)
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger16Imprimir(contar)
	contar++
	console_2.MImprimir(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MImprimir(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MImprimir(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MImprimir(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MImprimir(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MImprimir(([]byte)("am79c973 data received"))
		próprio.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MImprimir(([]byte)("am79c973 data sent"))
	}

	Portoescreverpalavra(registoEndereçoporto, 0)
	Portoescreverpalavra(registodadosporto, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MImprimir(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (próprio *Tamdam79c973) Enviar(dadosPonteiro uintptr, tamanho uint32) {
	var enviardescriptor uint16 = uint16(atualEnviarbuffer)
	atualEnviarbuffer = 0

	if tamanho > 1518 {
		tamanho = 1518
	}

	var origem_2 [4096]byte = *(*([4096]byte))(Pointer(dadosPonteiro))
	var destino_2 uint32 = enviarbufferDescrição[enviardescriptor].endereço_2 + tamanho - 1

	for i := 0; i < int(tamanho); i++ {

		*(*byte)(Pointer(uintptr(destino_2))) = origem_2[int(tamanho)-i-1]

		destino_2--
	}

	var dados [4096]byte = *(*([4096]byte))(Pointer(dadosPonteiro))
	console_2.MImprimirxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalImprimir(dados[i])
		console_2.MImprimir(([]byte)(":"))
	}
	console_2.MImprimir(([]byte)("\n"))

	enviarbufferDescrição[enviardescriptor].disponível = 0
	enviarbufferDescrição[enviardescriptor].parâmetros2 = 0
	enviarbufferDescrição[enviardescriptor].parâmetros = 0x8300F000 | uint32((-tamanho)&0xFFF)

	Portoescreverpalavra(registoEndereçoporto, 0)
	Portoescreverpalavra(registodadosporto, 0x48)

}
func (próprio *Tamdam79c973) Receive() {
	console_2.MImprimir(([]byte)(":"))
	console_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&enviarbuffer))))
	console_2.MImprimir(([]byte)(":"))
	console_2.MHexadecimalImprimir(enviarbuffer[0][0])
	console_2.MHexadecimalImprimir(enviarbuffer[0][1])
	console_2.MImprimir(([]byte)(":"))
	atualrecvbuffer = 0

	for ; (recvbufferDescrição[atualrecvbuffer].parâmetros & 0x80000000) == 0; atualrecvbuffer = (atualrecvbuffer + 1) % 8 {

		if !(recvbufferDescrição[atualrecvbuffer].parâmetros&0x40000000 != 0) && ((recvbufferDescrição[atualrecvbuffer].parâmetros & 0x03000000) == 0x03000000) {
			var tamanho uint32 = recvbufferDescrição[atualrecvbuffer].parâmetros & 0xFFF
			if tamanho > 64 {
				tamanho -= 4
			}

			console_2.MImprimir([]byte(" size : ["))
			console_2.MUnsignedinteger32Imprimir(tamanho)
			console_2.MImprimir([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferDescrição[atualrecvbuffer].endereço_2)))
			var referência_de_memória uintptr = uintptr(Pointer(&buffer_2))
			if irawdadoshandler != nil {
				if irawdadoshandler.Aorawdadosreceive(referência_de_memória, int(tamanho)) {

					console_2.MImprimirxy(([]byte)("self.Send"), 0, 22)

					próprio.Enviar(referência_de_memória, tamanho)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalImprimir(buffer_2[i])
				console_2.MImprimir([]byte(":"))
			}

		}
		recvbufferDescrição[atualrecvbuffer].parâmetros2 = 0
		recvbufferDescrição[atualrecvbuffer].parâmetros = 0x8000F7FF
	}
}
func (próprio *Tamdam79c973) Conjuntohandler(handler *TRawdadoshandler) {
	próprio.handler = handler
}
func (próprio *Tamdam79c973) GetmacEndereço() uint64 {

	return initBloco.físicoEndereço
}
func (próprio *Tamdam79c973) ConjuntoipEndereço(ip uint64) {
	initBloco.lógicosEndereço = ip
}
func (próprio *Tamdam79c973) GetipEndereço() uint64 {
	return initBloco.lógicosEndereço
}
