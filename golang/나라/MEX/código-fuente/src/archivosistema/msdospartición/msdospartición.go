package msdospartición

import . "consola"
import . "utilidad"

import . "controlador/ata"

type TParticiónTablaentrada struct {
	bootable	uint8

	iniciarhead	uint8
	iniciarsector	uint8
	iniciarcylinder	uint16

	Particiónid	uint8

	finhead		uint8
	finsector	uint8
	fincylinder	uint16

	Iniciarlba	uint32
	duración	uint32
}

func (propio *TParticiónTablaentrada) Init(datos [16]byte) {
	propio.bootable = datos[0]

	propio.iniciarhead = datos[1]
	propio.iniciarsector = (datos[2] >> 2)
	propio.iniciarcylinder = Unsignedinteger16r(uint16(datos[2]&0x03) | uint16(datos[3]))

	propio.Particiónid = datos[4]

	propio.finhead = datos[5]
	propio.finsector = (datos[6] >> 2)
	propio.fincylinder = Unsignedinteger16r(uint16(datos[6]&0x03) | uint16(datos[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], datos[8:12])
	propio.Iniciarlba = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], datos[12:16])
	propio.duración = Unsignedinteger32r(Matriztounsignedinteger32(buffer2))
}

type TRegistro_principal_de_arranque struct {
	bootloader	[440]byte
	signature	uint32
	sinusar		uint16

	Primarypartición	[4]TParticiónTablaentrada

	magicnumber	uint16
}
type TmsdosparticiónTabla struct {
	Mbr TRegistro_principal_de_arranque
}

func (propio *TmsdosparticiónTabla) Leerpartición(hd *TAvanzadoTecnologíaattachment) {

	consola_2 := TConsola{}
	consola_2.MImprimir(([]byte)("Reading MBR"))

	var particiónbytes [512]byte
	var buffer_2 = particiónbytes[:]
	hd.Leer28(0, &buffer_2, 512)

	propio.Mbr = TRegistro_principal_de_arranque{}
	var i int = 0
	for ; i < 440; i++ {
		propio.Mbr.bootloader[i] = particiónbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], particiónbytes[i:i+4])
	propio.Mbr.signature = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], particiónbytes[i:i+2])
	propio.Mbr.sinusar = Unsignedinteger16r(Matriztounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], particiónbytes[i:i+16])
	propio.Mbr.Primarypartición[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], particiónbytes[i:i+16])
	propio.Mbr.Primarypartición[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], particiónbytes[i:i+16])
	propio.Mbr.Primarypartición[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], particiónbytes[i:i+16])
	propio.Mbr.Primarypartición[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], particiónbytes[i:i+2])
	propio.Mbr.magicnumber = Unsignedinteger16r(Matriztounsignedinteger16(buffer6))

	if propio.Mbr.magicnumber != 0xAA55 {
		consola_2.MImprimir(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if propio.Mbr.Primarypartición[i].Particiónid == 0x00 {
			continue
		}

	}
}
