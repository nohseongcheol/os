package msdospart

import . "console"
import . "util"

import . "drivers/ata"

type TPartitionTableEntry struct {
	bootable	uint8

	start_head	uint8
	start_sector	uint8
	start_cylinder	uint16

	Partition_id	uint8

	end_head		uint8
	end_sector	uint8
	end_cylinder	uint16

	Start_lba	uint32
	length		uint32
}

func (self *TPartitionTableEntry) Vಆರಂಭಿಸು(data [16]byte) {
	self.bootable = data[0]

	self.start_head = data[1]
	self.start_sector = (data[2] >> 2)
	self.start_cylinder = Uint16_R(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partition_id = data[4]

	self.end_head = data[5]
	self.end_sector = (data[6] >> 2)
	self.end_cylinder = Uint16_R(uint16(data[6]&0x03) | uint16(data[7]))

	var buf1 [4]byte
	copy(buf1[:4], data[8:12])
	self.Start_lba = Uint32_R(ArrayToUint32(buf1))

	var buf2 [4]byte
	copy(buf2[:4], data[12:16])
	self.length = Uint32_R(ArrayToUint32(buf2))
}

type TMasterBootRecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	PrimaryPartition	[4]TPartitionTableEntry

	magicnumber	uint16
}
type TMSDOSPartitionTable struct {
	MBR TMasterBootRecord
}

func (self *TMSDOSPartitionTable) ReadPartitions(hd *TAdvancedTechnologyAttachment) {

	콘솔 := T콘솔{}
	콘솔.M출력(([]byte)("Reading MBR"))

	var partitionBytes [512]byte
	var buffer = partitionBytes[:]
	hd.Read28(0, &buffer, 512)

	self.MBR = TMasterBootRecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.MBR.bootloader[i] = partitionBytes[i]
	}

	var buf1 [4]byte
	copy(buf1[:4], partitionBytes[i:i+4])
	self.MBR.signature = Uint32_R(ArrayToUint32(buf1))
	i += 4

	var buf2 [2]byte
	copy(buf2[:2], partitionBytes[i:i+2])
	self.MBR.unused = Uint16_R(ArrayToUint16(buf2))
	i += 2

	var buf3 [16]byte
	copy(buf3[:16], partitionBytes[i:i+16])
	self.MBR.PrimaryPartition[0].Vಆರಂಭಿಸು(buf3)
	i += 16

	copy(buf3[:16], partitionBytes[i:i+16])
	self.MBR.PrimaryPartition[1].Vಆರಂಭಿಸು(buf3)
	i += 16

	copy(buf3[:16], partitionBytes[i:i+16])
	self.MBR.PrimaryPartition[2].Vಆರಂಭಿಸು(buf3)
	i += 16

	copy(buf3[:16], partitionBytes[i:i+16])
	self.MBR.PrimaryPartition[3].Vಆರಂಭಿಸು(buf3)
	i += 16

	var buf6 [2]byte
	copy(buf6[:2], partitionBytes[i:i+2])
	self.MBR.magicnumber = Uint16_R(ArrayToUint16(buf6))

	if self.MBR.magicnumber != 0xAA55 {
		콘솔.M출력(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.MBR.PrimaryPartition[i].Partition_id == 0x00 {
			continue
		}

	}
}
