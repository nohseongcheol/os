/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartição

import . "console"
import . "utilitário"

import . "controlador/ata"

type TPartiçãoTabelapontodeentrada struct {
	bootable	uint8

	iniciarhead	uint8
	iniciarsector	uint8
	iniciarcylinder	uint16

	Partiçãoid	uint8

	fimhead		uint8
	fimsector	uint8
	fimcylinder	uint16

	Iniciarlba	uint32
	duração		uint32
}

func (próprio *TPartiçãoTabelapontodeentrada) Init(dados [16]byte) {
	próprio.bootable = dados[0]

	próprio.iniciarhead = dados[1]
	próprio.iniciarsector = (dados[2] >> 2)
	próprio.iniciarcylinder = Unsignedinteger16r(uint16(dados[2]&0x03) | uint16(dados[3]))

	próprio.Partiçãoid = dados[4]

	próprio.fimhead = dados[5]
	próprio.fimsector = (dados[6] >> 2)
	próprio.fimcylinder = Unsignedinteger16r(uint16(dados[6]&0x03) | uint16(dados[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], dados[8:12])
	próprio.Iniciarlba = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], dados[12:16])
	próprio.duração = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer2))
}

type TRegisto_principal_de_arranque struct {
	bootloader	[440]byte
	signature	uint32
	nãoutilizado	uint16

	Primarypartição	[4]TPartiçãoTabelapontodeentrada

	magicnumber	uint16
}
type TmsdospartiçãoTabela struct {
	Mbr TRegisto_principal_de_arranque
}

func (próprio *TmsdospartiçãoTabela) Lerpartição(hd *TAvançadoTecnologiaattachment) {

	console_2 := TConsole{}
	console_2.MImprimir(([]byte)("Reading MBR"))

	var partiçãobytes [512]byte
	var buffer_2 = partiçãobytes[:]
	hd.Ler28(0, &buffer_2, 512)

	próprio.Mbr = TRegisto_principal_de_arranque{}
	var i int = 0
	for ; i < 440; i++ {
		próprio.Mbr.bootloader[i] = partiçãobytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partiçãobytes[i:i+4])
	próprio.Mbr.signature = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partiçãobytes[i:i+2])
	próprio.Mbr.nãoutilizado = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partiçãobytes[i:i+16])
	próprio.Mbr.Primarypartição[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partiçãobytes[i:i+16])
	próprio.Mbr.Primarypartição[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partiçãobytes[i:i+16])
	próprio.Mbr.Primarypartição[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partiçãobytes[i:i+16])
	próprio.Mbr.Primarypartição[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partiçãobytes[i:i+2])
	próprio.Mbr.magicnumber = Unsignedinteger16r(Matrizparaunsignedinteger16(buffer6))

	if próprio.Mbr.magicnumber != 0xAA55 {
		console_2.MImprimir(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if próprio.Mbr.Primarypartição[i].Partiçãoid == 0x00 {
			continue
		}

	}
}
