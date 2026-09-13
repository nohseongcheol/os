package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionJadualentry struct {
	bootable	uint8

	mulahead	uint8
	mulasector	uint8
	mulacylinder	uint16

	Partitionid	uint8

	tamathead	uint8
	tamatsector	uint8
	tamatcylinder	uint16

	Mulalba	uint32
	jarak	uint32
}

func (diri *TPartitionJadualentry) Init(data [16]byte) {
	diri.bootable = data[0]

	diri.mulahead = data[1]
	diri.mulasector = (data[2] >> 2)
	diri.mulacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	diri.Partitionid = data[4]

	diri.tamathead = data[5]
	diri.tamatsector = (data[6] >> 2)
	diri.tamatcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	diri.Mulalba = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	diri.jarak = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer2))
}

type TRekod_but_utama struct {
	bootloader	[440]byte
	signature	uint32
	tidakdigunakan	uint16

	Primarypartition	[4]TPartitionJadualentry

	magicnumber	uint16
}
type TmsdospartitionJadual struct {
	Mbr TRekod_but_utama
}

func (diri *TmsdospartitionJadual) Bacapartition(hd *TLanjutanTeknologiattachment) {

	console_2 := TConsole{}
	console_2.MCetak(([]byte)("Reading MBR"))

	var partitionBait [512]byte
	var buffer_2 = partitionBait[:]
	hd.Baca28(0, &buffer_2, 512)

	diri.Mbr = TRekod_but_utama{}
	var i int = 0
	for ; i < 440; i++ {
		diri.Mbr.bootloader[i] = partitionBait[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBait[i:i+4])
	diri.Mbr.signature = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBait[i:i+2])
	diri.Mbr.tidakdigunakan = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBait[i:i+16])
	diri.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBait[i:i+16])
	diri.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBait[i:i+16])
	diri.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBait[i:i+16])
	diri.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBait[i:i+2])
	diri.Mbr.magicnumber = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer6))

	if diri.Mbr.magicnumber != 0xAA55 {
		console_2.MCetak(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if diri.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
