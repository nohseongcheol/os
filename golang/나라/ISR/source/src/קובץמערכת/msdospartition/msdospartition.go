/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitiontableentry struct {
	bootable	uint8

	התחלהhead	uint8
	התחלהsector	uint8
	התחלהcylinder	uint16

	Partitionמזהה	uint8

	סיוםhead	uint8
	סיוםsector	uint8
	סיוםcylinder	uint16

	Sהתחלהlba	uint32
	אורך		uint32
}

func (self *TPartitiontableentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.התחלהhead = data[1]
	self.התחלהsector = (data[2] >> 2)
	self.התחלהcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionמזהה = data[4]

	self.סיוםhead = data[5]
	self.סיוםsector = (data[6] >> 2)
	self.סיוםcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Sהתחלהlba = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.אורך = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	לאבשימוש	uint16

	Primarypartition	[4]TPartitiontableentry

	magicnumber	uint16
}
type Tmsdospartitiontable struct {
	Mbr TMasterbootrecord
}

func (self *Tmsdospartitiontable) Rקריאהpartition(hd *Tמתקדםטכנולוגיהattachment) {

	console_2 := TConsole{}
	console_2.Mהדפסה(([]byte)("Reading MBR"))

	var partitionבתים [512]byte
	var buffer_2 = partitionבתים[:]
	hd.Rקריאה28(0, &buffer_2, 512)

	self.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionבתים[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionבתים[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionבתים[i:i+2])
	self.Mbr.לאבשימוש = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionבתים[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionבתים[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionבתים[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionבתים[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionבתים[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.Mהדפסה(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionמזהה == 0x00 {
			continue
		}

	}
}
