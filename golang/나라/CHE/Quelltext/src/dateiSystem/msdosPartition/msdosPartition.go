package msdosPartition

import . "konsole"
import . "hilfswerkzeug"

import . "treiber/ata"

type TPartitionTabelleEintrag struct {
	bootable	uint8

	startenhead	uint8
	startensector	uint8
	startencylinder	uint16

	PartitionKennung	uint8

	endehead	uint8
	endesector	uint8
	endecylinder	uint16

	Startenlba	uint32
	länge		uint32
}

func (selbst *TPartitionTabelleEintrag) Init(daten [16]byte) {
	selbst.bootable = daten[0]

	selbst.startenhead = daten[1]
	selbst.startensector = (daten[2] >> 2)
	selbst.startencylinder = Unsignedinteger16r(uint16(daten[2]&0x03) | uint16(daten[3]))

	selbst.PartitionKennung = daten[4]

	selbst.endehead = daten[5]
	selbst.endesector = (daten[6] >> 2)
	selbst.endecylinder = Unsignedinteger16r(uint16(daten[6]&0x03) | uint16(daten[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], daten[8:12])
	selbst.Startenlba = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], daten[12:16])
	selbst.länge = Unsignedinteger32r(Feldtounsignedinteger32(buffer2))
}

type THauptstartdatensatz struct {
	bootloader	[440]byte
	signature	uint32
	unbenutzt	uint16

	PrimaryPartition	[4]TPartitionTabelleEintrag

	magicnumber	uint16
}
type TmsdosPartitionTabelle struct {
	Mbr THauptstartdatensatz
}

func (selbst *TmsdosPartitionTabelle) LesenPartition(hd *TErweitertTechnikattachment) {

	konsole_2 := TKonsole{}
	konsole_2.MDrucken(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Lesen28(0, &buffer_2, 512)

	selbst.Mbr = THauptstartdatensatz{}
	var i int = 0
	for ; i < 440; i++ {
		selbst.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	selbst.Mbr.signature = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	selbst.Mbr.unbenutzt = Unsignedinteger16r(Feldtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	selbst.Mbr.PrimaryPartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selbst.Mbr.PrimaryPartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selbst.Mbr.PrimaryPartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selbst.Mbr.PrimaryPartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	selbst.Mbr.magicnumber = Unsignedinteger16r(Feldtounsignedinteger16(buffer6))

	if selbst.Mbr.magicnumber != 0xAA55 {
		konsole_2.MDrucken(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if selbst.Mbr.PrimaryPartition[i].PartitionKennung == 0x00 {
			continue
		}

	}
}
