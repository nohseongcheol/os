/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "utilitaire"

import . "pilote/ata"

type TPartitionTableauélément struct {
	bootable	uint8

	démarrerhead		uint8
	démarrersector		uint8
	démarrercylinder	uint16

	PartitionIdentifiant	uint8

	finhead		uint8
	finsector	uint8
	fincylinder	uint16

	Démarrerlba	uint32
	durée		uint32
}

func (self *TPartitionTableauélément) Init(données [16]byte) {
	self.bootable = données[0]

	self.démarrerhead = données[1]
	self.démarrersector = (données[2] >> 2)
	self.démarrercylinder = Unsignedinteger16r(uint16(données[2]&0x03) | uint16(données[3]))

	self.PartitionIdentifiant = données[4]

	self.finhead = données[5]
	self.finsector = (données[6] >> 2)
	self.fincylinder = Unsignedinteger16r(uint16(données[6]&0x03) | uint16(données[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], données[8:12])
	self.Démarrerlba = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], données[12:16])
	self.durée = Unsignedinteger32r(Tableautounsignedinteger32(buffer2))
}

type TEnregistrement_principal_de_démarrage struct {
	bootloader	[440]byte
	signature	uint32
	inutilisé	uint16

	Primarypartition	[4]TPartitionTableauélément

	magicnumber	uint16
}
type TmsdospartitionTableau struct {
	Mbr TEnregistrement_principal_de_démarrage
}

func (self *TmsdospartitionTableau) Lirepartition(hd *TAvancéTechnologieattachment) {

	console_2 := TConsole{}
	console_2.MImprimer(([]byte)("Reading MBR"))

	var partitionOctets [512]byte
	var buffer_2 = partitionOctets[:]
	hd.Lire28(0, &buffer_2, 512)

	self.Mbr = TEnregistrement_principal_de_démarrage{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionOctets[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionOctets[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionOctets[i:i+2])
	self.Mbr.inutilisé = Unsignedinteger16r(Tableautounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionOctets[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctets[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctets[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctets[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionOctets[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Tableautounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MImprimer(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionIdentifiant == 0x00 {
			continue
		}

	}
}
