/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const BytesPerSector int = 512

type TAdvancedTechnologyAttachment struct {
	master		bool
	dataPort	TPort16Bit
	errorPort	TPort8Bit
	sectorCountPort	TPort8Bit
	lbaLowPort	TPort8Bit
	lbaMidPort	TPort8Bit
	lbaHiPort	TPort8Bit
	devicePort	TPort8Bit
	commandPort	TPort8Bit
	controlPort	TPort8Bit
}

func (self *TAdvancedTechnologyAttachment) Vആരംഭിക്കുക(master bool, portBase uint16) {
	self.master = master
	self.dataPort.Vആരംഭിക്കുക(portBase)
	self.errorPort.Vആരംഭിക്കുക(portBase + 0x1)
	self.sectorCountPort.Vആരംഭിക്കുക(portBase + 0x2)
	self.lbaLowPort.Vആരംഭിക്കുക(portBase + 0x3)
	self.lbaMidPort.Vആരംഭിക്കുക(portBase + 0x4)
	self.lbaHiPort.Vആരംഭിക്കുക(portBase + 0x5)
	self.devicePort.Vആരംഭിക്കുക(portBase + 0x6)
	self.commandPort.Vആരംഭിക്കുക(portBase + 0x7)
	self.controlPort.Vആരംഭിക്കുക(portBase + 0x8)

}

func (self *TAdvancedTechnologyAttachment) Identify() {

	var 콘솔 = T콘솔{}

	if self.master {
		self.devicePort.Vഎഴുതുക(0xA0)
	} else {
		self.devicePort.Vഎഴുതുക(0xB0)
	}
	self.controlPort.Vഎഴുതുക(0)
	self.devicePort.Vഎഴുതുക(0xA0)

	var status uint8 = self.commandPort.Vവായിക്കുക()
	if status == 0xFF {
		콘솔.M출력(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.devicePort.Vഎഴുതുക(0xA0)
	} else {
		self.devicePort.Vഎഴുതുക(0xB0)
	}
	self.sectorCountPort.Vഎഴുതുക(0)
	self.lbaLowPort.Vഎഴുതുക(0)
	self.lbaMidPort.Vഎഴുതുക(0)
	self.lbaHiPort.Vഎഴുതുക(0)
	self.commandPort.Vഎഴുതുക(0xEC)

	status = self.commandPort.Vവായിക്കുക()
	if status == 0x00 {
		콘솔.M출력(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = self.commandPort.Vവായിക്കുക()
	}

	if (status & 0x01) != 0 {
		콘솔.M출력(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataPort.Vവായിക്കുക()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	콘솔.M출력XY(([]byte)("ata ok"), 10, 22)

}
func (self *TAdvancedTechnologyAttachment) Read28(sector uint32, data *[]byte, count int) {
	var 콘솔 = T콘솔{}
	if (sector & 0xF0000000) != 0 {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}
	if count > BytesPerSector {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.devicePort.Vഎഴുതുക(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.devicePort.Vഎഴുതുക(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.errorPort.Vഎഴുതുക(0)
	self.sectorCountPort.Vഎഴുതുക(1)

	self.lbaLowPort.Vഎഴുതുക(uint8(sector & 0x000000FF))
	self.lbaMidPort.Vഎഴുതുക(uint8((sector & 0x0000FF00) >> 8))
	self.lbaHiPort.Vഎഴുതുക(uint8((sector & 0x00FF0000) >> 16))
	self.commandPort.Vഎഴുതുക(0x20)

	var status uint8 = self.commandPort.Vവായിക്കുക()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandPort.Vവായിക്കുക()
	}

	if (status & 0x01) != 0 {
		콘솔.M출력(([]byte)("ata read error "))
		return
	}

	콘솔.M출력XY(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataPort.Vവായിക്കുക()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < BytesPerSector; i += 2 {
		self.dataPort.Vവായിക്കുക()
	}
}
func (self *TAdvancedTechnologyAttachment) Write28(sectorNum uint32, data []byte, count uint32) {

	if sectorNum > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.devicePort.Vഎഴുതുക(uint8(0xE0 | uint8((sectorNum&0x0F000000)>>24)))
	} else {
		self.devicePort.Vഎഴുതുക(uint8(0xF0 | uint8((sectorNum&0x0F000000)>>24)))
	}

	self.errorPort.Vഎഴുതുക(0)
	self.sectorCountPort.Vഎഴുതുക(1)
	self.lbaLowPort.Vഎഴുതുക(uint8(sectorNum & 0x000000FF))
	self.lbaMidPort.Vഎഴുതുക(uint8((sectorNum & 0x0000FF00) >> 8))
	self.lbaHiPort.Vഎഴുതുക(uint8((sectorNum & 0x00FF0000) >> 16))
	self.commandPort.Vഎഴുതുക(0x30)

	var 콘솔 = T콘솔{}
	콘솔.M출력(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataPort.Vഎഴുതുക(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		콘솔.M출력(text)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataPort.Vഎഴുതുക(0x0000)
	}

}

func (self *TAdvancedTechnologyAttachment) Flush() {
	if self.master {
		self.devicePort.Vഎഴുതുക(0xE0)
	} else {
		self.devicePort.Vഎഴുതുക(0xF0)
	}
	self.commandPort.Vഎഴുതുക(0xE7)

	var 콘솔 = T콘솔{}

	var status uint8 = self.commandPort.Vവായിക്കുക()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandPort.Vവായിക്കുക()
	}
	if (status & 0x01) != 0 {
		콘솔.M출력(([]byte)(" ata flush error"))
		return
	}

}
