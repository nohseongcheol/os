/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "consola"
import . "util"

import . "driver/ata"

type TPartitionTaulaentrada struct {
	bootable	uint8

	iniciahead	uint8
	iniciasector	uint8
	iniciacylinder	uint16

	PartitionIdentificador	uint8

	finalhead	uint8
	finalsector	uint8
	finalcylinder	uint16

	Inicialba	uint32
	durada		uint32
}

func (unmateix *TPartitionTaulaentrada) Init(data [16]byte) {
	unmateix.bootable = data[0]

	unmateix.iniciahead = data[1]
	unmateix.iniciasector = (data[2] >> 2)
	unmateix.iniciacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	unmateix.PartitionIdentificador = data[4]

	unmateix.finalhead = data[5]
	unmateix.finalsector = (data[6] >> 2)
	unmateix.finalcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	unmateix.Inicialba = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	unmateix.durada = Unsignedinteger32r(Matriutounsignedinteger32(buffer2))
}

type TMestrebootRegistra struct {
	bootloader	[440]byte
	signature	uint32
	senseús		uint16

	Primarypartition	[4]TPartitionTaulaentrada

	magicnumber	uint16
}
type TmsdospartitionTaula struct {
	Mbr TMestrebootRegistra
}

func (unmateix *TmsdospartitionTaula) Lecturapartition(hd *TAvançatTecnologiaattachment) {

	consola_2 := TConsola{}
	consola_2.MImprimeix(([]byte)("Reading MBR"))

	var partitionbytes [512]byte
	var buffer_2 = partitionbytes[:]
	hd.Lectura28(0, &buffer_2, 512)

	unmateix.Mbr = TMestrebootRegistra{}
	var i int = 0
	for ; i < 440; i++ {
		unmateix.Mbr.bootloader[i] = partitionbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbytes[i:i+4])
	unmateix.Mbr.signature = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbytes[i:i+2])
	unmateix.Mbr.senseús = Unsignedinteger16r(Matriutounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionbytes[i:i+16])
	unmateix.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	unmateix.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	unmateix.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	unmateix.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionbytes[i:i+2])
	unmateix.Mbr.magicnumber = Unsignedinteger16r(Matriutounsignedinteger16(buffer6))

	if unmateix.Mbr.magicnumber != 0xAA55 {
		consola_2.MImprimeix(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if unmateix.Mbr.Primarypartition[i].PartitionIdentificador == 0x00 {
			continue
		}

	}
}
