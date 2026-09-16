/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "quadro_da_rede_de_meio_partilhado"
import . "utilitário"

var arpconsole TConsole = TConsole{}

type ArpMensagembuffer struct {
	equipamentotipo			[2]byte
	protocol			[2]byte
	equipamentoEndereçoTamanho	byte
	protocolEndereçoTamanho		byte
	comando				[2]byte

	origemmacEndereço	[6]byte
	origemipEndereço	[4]byte
	destinomacEndereço	[6]byte
	destinoipEndereço	[4]byte
}

var arpmesgTamanho uint32 = (64+92+64)/8 + 2

type ArpMensagem struct {
	equipamentotipo			uint16
	protocol			uint16
	equipamentoEndereçoTamanho	uint8
	protocolEndereçoTamanho		uint8
	comando				uint16

	origemmacEndereço	uint64
	origemipEndereço	uint32
	destinomacEndereço	uint64
	destinoipEndereço	uint32
}

func (próprio *ArpMensagem) Init(buffer_2 *ArpMensagembuffer) {

	próprio.equipamentotipo = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.equipamentotipo))
	próprio.protocol = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.protocol))
	próprio.equipamentoEndereçoTamanho = byte(buffer_2.equipamentoEndereçoTamanho)
	próprio.protocolEndereçoTamanho = byte(buffer_2.protocolEndereçoTamanho)
	próprio.comando = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer_2.comando))

	próprio.origemmacEndereço = Unsignedinteger48r(Matrizparaunsignedinteger48(buffer_2.origemmacEndereço))
	próprio.origemipEndereço = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer_2.origemipEndereço))
	próprio.destinomacEndereço = Unsignedinteger48r(Matrizparaunsignedinteger48(buffer_2.destinomacEndereço))
	próprio.destinoipEndereço = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer_2.destinoipEndereço))
}
func (próprio *ArpMensagem) Conjuntobuffer(buffer_2 *ArpMensagembuffer) {
	buffer_2.equipamentotipo = Unsignedinteger16paramatriz(próprio.equipamentotipo)
	buffer_2.protocol = Unsignedinteger16paramatriz(próprio.protocol)
	buffer_2.equipamentoEndereçoTamanho = uint8(próprio.equipamentoEndereçoTamanho)
	buffer_2.protocolEndereçoTamanho = uint8(próprio.protocolEndereçoTamanho)

	buffer_2.comando = Unsignedinteger16paramatriz(próprio.comando)
	buffer_2.origemmacEndereço = Unsignedinteger48paramatriz(próprio.origemmacEndereço)
	buffer_2.origemipEndereço = Unsignedinteger32paramatriz(próprio.origemipEndereço)
	buffer_2.destinomacEndereço = Unsignedinteger48paramatriz(próprio.destinomacEndereço)
	buffer_2.destinoipEndereço = Unsignedinteger32paramatriz(próprio.destinoipEndereço)
}

type Arpethernetquadrohandler struct {
	TEthernetquadrohandler
}

var arpprovider Arpprovider
var fornecedor_de_quadros_de_rede_de_meio_partilhado TFornecedor_de_quadros_de_rede_de_meio_partilhado

func (próprio *Arpethernetquadrohandler) Ethernetquadroreceivewhen(dadosPonteiro uintptr, tamanho int) bool {
	arpconsole.MImprimirxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetquadroreceivewhen(dadosPonteiro, uint32(tamanho))

}
func (próprio *Arpethernetquadrohandler) Enviar(destinomacbe uint64, dadosPonteiro uintptr, tamanho uint32) {
	arpconsole.MImprimirxy([]byte("arp send:"), 0, 24)
	var ethernettipobe = Unsignedinteger16r(0x0806)
	próprio.TEthernetquadrohandler.QuadroEnviar(destinomacbe, ethernettipobe, dadosPonteiro, tamanho)
}

type Arpprovider struct {
	Ipcache				[128]uint32
	Maccache			[128]uint64
	númerocachepontodeentrada	int

	handler	IEthernetquadrohandler
}

var handler IEthernetquadrohandler

func (próprio *Arpprovider) Init(backend TFornecedor_de_quadros_de_rede_de_meio_partilhado, userhandler IEthernetquadrohandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Conjuntohandler(userhandler, 0x0806)
	próprio.númerocachepontodeentrada = 0
	arpprovider = *próprio

}

func (próprio *Arpprovider) Ethernetquadroreceivewhen(dadosPonteiro uintptr, tamanho uint32) bool {

	if tamanho < arpmesgTamanho {
		return false
	}
	var arpbuffer *ArpMensagembuffer = (*ArpMensagembuffer)(Pointer(dadosPonteiro))
	var arp ArpMensagem = ArpMensagem{}
	arp.Init(arpbuffer)

	if arp.equipamentotipo == 0x0100 {

		if arp.protocol == 0x0008 && arp.equipamentoEndereçoTamanho == 6 && arp.protocolEndereçoTamanho == 4 && uint64(arp.destinoipEndereço) == handler.GetipEndereço() {

			arpconsole.MImprimir([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Imprimir(arp.protocol)
			arpconsole.MImprimir([]byte(":"))
			arpconsole.MUnsignedinteger64Imprimir(uint64(arp.destinomacEndereço))
			arpconsole.MImprimir([]byte(":"))
			arpconsole.MUnsignedinteger16Imprimir(arp.comando)
			arpconsole.MImprimir([]byte(":"))
			arpconsole.MUnsignedinteger64Imprimir(handler.GetmacEndereço())

			switch arp.comando {
			case 0x0100:

				if próprio.Getmacdecache(arp.origemipEndereço) == 0xFFFFFFFFFFFF {
					if próprio.númerocachepontodeentrada < 128 {
						próprio.Ipcache[próprio.númerocachepontodeentrada] = arp.origemipEndereço
						próprio.Maccache[próprio.númerocachepontodeentrada] = arp.origemmacEndereço
						próprio.númerocachepontodeentrada++
					}
				}
				arp.comando = 0x0200
				arp.destinoipEndereço = arp.origemipEndereço
				arp.destinomacEndereço = arp.origemmacEndereço
				arp.origemipEndereço = uint32(handler.GetipEndereço())
				arp.origemmacEndereço = handler.GetmacEndereço()
				arp.Conjuntobuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MImprimir(([]byte)("self.numCacheEntries"))

				if próprio.númerocachepontodeentrada < 128 {
					próprio.Ipcache[próprio.númerocachepontodeentrada] = arp.origemipEndereço
					próprio.Maccache[próprio.númerocachepontodeentrada] = arp.origemmacEndereço
					próprio.númerocachepontodeentrada++
				}
				break
			}

		}
	}
	return false

}

func (próprio *Arpprovider) BroadcastmacEndereço(Ipredeoctetoorder uint32) {

	var arp ArpMensagem = ArpMensagem{}
	arp.equipamentotipo = 0x0100
	arp.protocol = 0x0008
	arp.equipamentoEndereçoTamanho = 6
	arp.protocolEndereçoTamanho = 4
	arp.comando = 0x0200

	arp.origemipEndereço = uint32(handler.GetipEndereço())

	arp.destinomacEndereço = próprio.Resolver(Ipredeoctetoorder)
	arp.destinoipEndereço = Ipredeoctetoorder
	arpconsole.MImprimirxy([]byte("broad mac"), 0, 15)

	arp.origemmacEndereço = handler.GetmacEndereço()

	var arpbuffer ArpMensagembuffer = ArpMensagembuffer{}
	arp.Conjuntobuffer(&arpbuffer)

	var referência_de_memória uintptr = uintptr(Pointer(&arpbuffer))
	handler.Enviar(arp.destinomacEndereço, referência_de_memória, arpmesgTamanho)
}
func (próprio *Arpprovider) RequestmacEndereço(Ipredeoctetoorder uint32) {

	var arp ArpMensagem = ArpMensagem{}
	arp.equipamentotipo = 0x0100

	arp.protocol = 0x0008
	arp.equipamentoEndereçoTamanho = 6
	arp.protocolEndereçoTamanho = 4
	arp.comando = 0x0100

	arp.origemmacEndereço = handler.GetmacEndereço()
	arp.origemipEndereço = uint32(handler.GetipEndereço())

	arp.destinomacEndereço = 0xFFFFFFFFFFFF
	arp.destinoipEndereço = Ipredeoctetoorder

	var arpbuffer ArpMensagembuffer = ArpMensagembuffer{}
	arp.Conjuntobuffer(&arpbuffer)

	var referência_de_memória uintptr = uintptr(Pointer(&arpbuffer))
	handler.Enviar(arp.destinomacEndereço, referência_de_memória, arpmesgTamanho)
}
func (próprio *Arpprovider) TestarImprimir(dados *[]byte, tamanho uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(dados))
	arpconsole.MImprimirxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalImprimir(buffer_2[i])
		arpconsole.MImprimir([]byte(":"))
	}
	arpconsole.MImprimir([]byte("]"))
}

func (próprio *Arpprovider) Getmacdecache(Ipredeoctetoorder uint32) uint64 {
	for i := 0; i < próprio.númerocachepontodeentrada; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MImprimir(([]byte)("["))
		arpconsole.MUnsignedinteger32Imprimir(próprio.Ipcache[i])
		arpconsole.MImprimir(([]byte)(":"))
		arpconsole.MUnsignedinteger32Imprimir(Ipredeoctetoorder)
		arpconsole.MImprimir(([]byte)(":"))
		arpconsole.MImprimir(([]byte)(":"))
		arpconsole.MUnsignedinteger64Imprimir(próprio.Maccache[i])
		arpconsole.MImprimir(([]byte)("]\n"))

		if próprio.Ipcache[i] == Ipredeoctetoorder {
			arpconsole.MImprimir([]byte("getmacfromcache"))
			return próprio.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (próprio *Arpprovider) Resolver(Ipredeoctetoorder uint32) uint64 {
	var destino_3 uint64 = próprio.Getmacdecache(Ipredeoctetoorder)
	if destino_3 == 0xFFFFFFFFFFFF {
		próprio.RequestmacEndereço(Ipredeoctetoorder)
	}
	for i := 0; i < 128 && destino_3 == 0xFFFFFFFFFFFF; i++ {
		destino_3 = próprio.Getmacdecache(Ipredeoctetoorder)

	}

	return destino_3
}
