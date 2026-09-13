package arp

import . "unsafe"
import . "consola"
import . "trama_de_la_red_de_medio_compartido"
import . "utilidad"

var arpconsola TConsola = TConsola{}

type ArpMensajebuffer struct {
	hardwaretipo		[2]byte
	protocol		[2]byte
	hardwareDirecciónTamaño	byte
	protocolDirecciónTamaño	byte
	orden			[2]byte

	origenmacDirección	[6]byte
	origenipDirección	[4]byte
	destinomacDirección	[6]byte
	destinoipDirección	[4]byte
}

var arpmesgTamaño uint32 = (64+92+64)/8 + 2

type ArpMensaje struct {
	hardwaretipo		uint16
	protocol		uint16
	hardwareDirecciónTamaño	uint8
	protocolDirecciónTamaño	uint8
	orden			uint16

	origenmacDirección	uint64
	origenipDirección	uint32
	destinomacDirección	uint64
	destinoipDirección	uint32
}

func (propio *ArpMensaje) Init(buffer_2 *ArpMensajebuffer) {

	propio.hardwaretipo = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.hardwaretipo))
	propio.protocol = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.protocol))
	propio.hardwareDirecciónTamaño = byte(buffer_2.hardwareDirecciónTamaño)
	propio.protocolDirecciónTamaño = byte(buffer_2.protocolDirecciónTamaño)
	propio.orden = Unsignedinteger16r(Matriztounsignedinteger16(buffer_2.orden))

	propio.origenmacDirección = Unsignedinteger48r(Matriztounsignedinteger48(buffer_2.origenmacDirección))
	propio.origenipDirección = Unsignedinteger32r(Matriztounsignedinteger32(buffer_2.origenipDirección))
	propio.destinomacDirección = Unsignedinteger48r(Matriztounsignedinteger48(buffer_2.destinomacDirección))
	propio.destinoipDirección = Unsignedinteger32r(Matriztounsignedinteger32(buffer_2.destinoipDirección))
}
func (propio *ArpMensaje) Establecerbuffer(buffer_2 *ArpMensajebuffer) {
	buffer_2.hardwaretipo = Unsignedinteger16tomatriz(propio.hardwaretipo)
	buffer_2.protocol = Unsignedinteger16tomatriz(propio.protocol)
	buffer_2.hardwareDirecciónTamaño = uint8(propio.hardwareDirecciónTamaño)
	buffer_2.protocolDirecciónTamaño = uint8(propio.protocolDirecciónTamaño)

	buffer_2.orden = Unsignedinteger16tomatriz(propio.orden)
	buffer_2.origenmacDirección = Unsignedinteger48tomatriz(propio.origenmacDirección)
	buffer_2.origenipDirección = Unsignedinteger32tomatriz(propio.origenipDirección)
	buffer_2.destinomacDirección = Unsignedinteger48tomatriz(propio.destinomacDirección)
	buffer_2.destinoipDirección = Unsignedinteger32tomatriz(propio.destinoipDirección)
}

type Arpethernettramahandler struct {
	TEthernettramahandler
}

var arpprovider Arpprovider
var proveedor_de_tramas_de_red_de_medio_compartido TProveedor_de_tramas_de_red_de_medio_compartido

func (propio *Arpethernettramahandler) Ethernettramareceivewhen(datosPuntero uintptr, tamaño int) bool {
	arpconsola.MImprimirxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernettramareceivewhen(datosPuntero, uint32(tamaño))

}
func (propio *Arpethernettramahandler) Enviar(destinomacbe uint64, datosPuntero uintptr, tamaño uint32) {
	arpconsola.MImprimirxy([]byte("arp send:"), 0, 24)
	var ethernettipobe = Unsignedinteger16r(0x0806)
	propio.TEthernettramahandler.TramaEnviar(destinomacbe, ethernettipobe, datosPuntero, tamaño)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	númerocacheentrada	int

	handler	IEthernettramahandler
}

var handler IEthernettramahandler

func (propio *Arpprovider) Init(backend TProveedor_de_tramas_de_red_de_medio_compartido, userhandler IEthernettramahandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Establecerhandler(userhandler, 0x0806)
	propio.númerocacheentrada = 0
	arpprovider = *propio

}

func (propio *Arpprovider) Ethernettramareceivewhen(datosPuntero uintptr, tamaño uint32) bool {

	if tamaño < arpmesgTamaño {
		return false
	}
	var arpbuffer *ArpMensajebuffer = (*ArpMensajebuffer)(Pointer(datosPuntero))
	var arp ArpMensaje = ArpMensaje{}
	arp.Init(arpbuffer)

	if arp.hardwaretipo == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareDirecciónTamaño == 6 && arp.protocolDirecciónTamaño == 4 && uint64(arp.destinoipDirección) == handler.GetipDirección() {

			arpconsola.MImprimir([]byte("arp onetherframe"))
			arpconsola.MUnsignedinteger16Imprimir(arp.protocol)
			arpconsola.MImprimir([]byte(":"))
			arpconsola.MUnsignedinteger64Imprimir(uint64(arp.destinomacDirección))
			arpconsola.MImprimir([]byte(":"))
			arpconsola.MUnsignedinteger16Imprimir(arp.orden)
			arpconsola.MImprimir([]byte(":"))
			arpconsola.MUnsignedinteger64Imprimir(handler.GetmacDirección())

			switch arp.orden {
			case 0x0100:

				if propio.Getmacdesdecache(arp.origenipDirección) == 0xFFFFFFFFFFFF {
					if propio.númerocacheentrada < 128 {
						propio.Ipcache[propio.númerocacheentrada] = arp.origenipDirección
						propio.Maccache[propio.númerocacheentrada] = arp.origenmacDirección
						propio.númerocacheentrada++
					}
				}
				arp.orden = 0x0200
				arp.destinoipDirección = arp.origenipDirección
				arp.destinomacDirección = arp.origenmacDirección
				arp.origenipDirección = uint32(handler.GetipDirección())
				arp.origenmacDirección = handler.GetmacDirección()
				arp.Establecerbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsola.MImprimir(([]byte)("self.numCacheEntries"))

				if propio.númerocacheentrada < 128 {
					propio.Ipcache[propio.númerocacheentrada] = arp.origenipDirección
					propio.Maccache[propio.númerocacheentrada] = arp.origenmacDirección
					propio.númerocacheentrada++
				}
				break
			}

		}
	}
	return false

}

func (propio *Arpprovider) BroadcastmacDirección(Ipredoctetoorder uint32) {

	var arp ArpMensaje = ArpMensaje{}
	arp.hardwaretipo = 0x0100
	arp.protocol = 0x0008
	arp.hardwareDirecciónTamaño = 6
	arp.protocolDirecciónTamaño = 4
	arp.orden = 0x0200

	arp.origenipDirección = uint32(handler.GetipDirección())

	arp.destinomacDirección = propio.Resolver(Ipredoctetoorder)
	arp.destinoipDirección = Ipredoctetoorder
	arpconsola.MImprimirxy([]byte("broad mac"), 0, 15)

	arp.origenmacDirección = handler.GetmacDirección()

	var arpbuffer ArpMensajebuffer = ArpMensajebuffer{}
	arp.Establecerbuffer(&arpbuffer)

	var referencia_de_memoria uintptr = uintptr(Pointer(&arpbuffer))
	handler.Enviar(arp.destinomacDirección, referencia_de_memoria, arpmesgTamaño)
}
func (propio *Arpprovider) RequestmacDirección(Ipredoctetoorder uint32) {

	var arp ArpMensaje = ArpMensaje{}
	arp.hardwaretipo = 0x0100

	arp.protocol = 0x0008
	arp.hardwareDirecciónTamaño = 6
	arp.protocolDirecciónTamaño = 4
	arp.orden = 0x0100

	arp.origenmacDirección = handler.GetmacDirección()
	arp.origenipDirección = uint32(handler.GetipDirección())

	arp.destinomacDirección = 0xFFFFFFFFFFFF
	arp.destinoipDirección = Ipredoctetoorder

	var arpbuffer ArpMensajebuffer = ArpMensajebuffer{}
	arp.Establecerbuffer(&arpbuffer)

	var referencia_de_memoria uintptr = uintptr(Pointer(&arpbuffer))
	handler.Enviar(arp.destinomacDirección, referencia_de_memoria, arpmesgTamaño)
}
func (propio *Arpprovider) ProbarImprimir(datos *[]byte, tamaño uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(datos))
	arpconsola.MImprimirxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsola.MHexadecimalImprimir(buffer_2[i])
		arpconsola.MImprimir([]byte(":"))
	}
	arpconsola.MImprimir([]byte("]"))
}

func (propio *Arpprovider) Getmacdesdecache(Ipredoctetoorder uint32) uint64 {
	for i := 0; i < propio.númerocacheentrada; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsola.MImprimir(([]byte)("["))
		arpconsola.MUnsignedinteger32Imprimir(propio.Ipcache[i])
		arpconsola.MImprimir(([]byte)(":"))
		arpconsola.MUnsignedinteger32Imprimir(Ipredoctetoorder)
		arpconsola.MImprimir(([]byte)(":"))
		arpconsola.MImprimir(([]byte)(":"))
		arpconsola.MUnsignedinteger64Imprimir(propio.Maccache[i])
		arpconsola.MImprimir(([]byte)("]\n"))

		if propio.Ipcache[i] == Ipredoctetoorder {
			arpconsola.MImprimir([]byte("getmacfromcache"))
			return propio.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (propio *Arpprovider) Resolver(Ipredoctetoorder uint32) uint64 {
	var rESULTADO uint64 = propio.Getmacdesdecache(Ipredoctetoorder)
	if rESULTADO == 0xFFFFFFFFFFFF {
		propio.RequestmacDirección(Ipredoctetoorder)
	}
	for i := 0; i < 128 && rESULTADO == 0xFFFFFFFFFFFF; i++ {
		rESULTADO = propio.Getmacdesdecache(Ipredoctetoorder)

	}

	return rESULTADO
}
