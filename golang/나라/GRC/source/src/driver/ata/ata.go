/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "θύρα"
import . "console"

const Bytespersector int = 512

type TΓιαπροχωρημένουςΤεχνολογίαattachment struct {
	κύριαέξοδος	bool
	dataΘύρα	TΘύρα16bit
	σφάλμαΘύρα	TΘύρα8bit
	sectorcountΘύρα	TΘύρα8bit
	lbaΧαμηλήΘύρα	TΘύρα8bit
	lbamidΘύρα	TΘύρα8bit
	lbahiΘύρα	TΘύρα8bit
	συσκευήΘύρα	TΘύρα8bit
	εντολήΘύρα	TΘύρα8bit
	έλεγχοςΘύρα	TΘύρα8bit
}

func (self *TΓιαπροχωρημένουςΤεχνολογίαattachment) Init(κύριαέξοδος bool, θύραbase uint16) {
	self.κύριαέξοδος = κύριαέξοδος
	self.dataΘύρα.Init(θύραbase)
	self.σφάλμαΘύρα.Init(θύραbase + 0x1)
	self.sectorcountΘύρα.Init(θύραbase + 0x2)
	self.lbaΧαμηλήΘύρα.Init(θύραbase + 0x3)
	self.lbamidΘύρα.Init(θύραbase + 0x4)
	self.lbahiΘύρα.Init(θύραbase + 0x5)
	self.συσκευήΘύρα.Init(θύραbase + 0x6)
	self.εντολήΘύρα.Init(θύραbase + 0x7)
	self.έλεγχοςΘύρα.Init(θύραbase + 0x8)

}

func (self *TΓιαπροχωρημένουςΤεχνολογίαattachment) Identify() {

	var console_2 = TConsole{}

	if self.κύριαέξοδος {
		self.συσκευήΘύρα.Εγγραφή(0xA0)
	} else {
		self.συσκευήΘύρα.Εγγραφή(0xB0)
	}
	self.έλεγχοςΘύρα.Εγγραφή(0)
	self.συσκευήΘύρα.Εγγραφή(0xA0)

	var κατάσταση uint8 = self.εντολήΘύρα.Ανάγνωση()
	if κατάσταση == 0xFF {
		console_2.MΕκτύπωση(([]byte)("Invalid Status"))
		return
	}

	if self.κύριαέξοδος {
		self.συσκευήΘύρα.Εγγραφή(0xA0)
	} else {
		self.συσκευήΘύρα.Εγγραφή(0xB0)
	}
	self.sectorcountΘύρα.Εγγραφή(0)
	self.lbaΧαμηλήΘύρα.Εγγραφή(0)
	self.lbamidΘύρα.Εγγραφή(0)
	self.lbahiΘύρα.Εγγραφή(0)
	self.εντολήΘύρα.Εγγραφή(0xEC)

	κατάσταση = self.εντολήΘύρα.Ανάγνωση()
	if κατάσταση == 0x00 {
		console_2.MΕκτύπωση(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (κατάσταση&0x80) == 0x80 && (κατάσταση&0x01) != 0x01 {
		κατάσταση = self.εντολήΘύρα.Ανάγνωση()
	}

	if (κατάσταση & 0x01) != 0 {
		console_2.MΕκτύπωση(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataΘύρα.Ανάγνωση()
		κείμενο := []byte("  ")
		κείμενο[0] = uint8((data >> 8) & 0xFF)
		κείμενο[1] = uint8(data & 0xFF)

	}
	console_2.MΕκτύπωσηxy(([]byte)("ata ok"), 10, 22)

}
func (self *TΓιαπροχωρημένουςΤεχνολογίαattachment) Ανάγνωση28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MΕκτύπωση(([]byte)("ata read error "))
		return
	}
	if count > Bytespersector {
		console_2.MΕκτύπωση(([]byte)("ata read error "))
		return
	}

	if self.κύριαέξοδος {
		self.συσκευήΘύρα.Εγγραφή(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.συσκευήΘύρα.Εγγραφή(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.σφάλμαΘύρα.Εγγραφή(0)
	self.sectorcountΘύρα.Εγγραφή(1)

	self.lbaΧαμηλήΘύρα.Εγγραφή(uint8(sector & 0x000000FF))
	self.lbamidΘύρα.Εγγραφή(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiΘύρα.Εγγραφή(uint8((sector & 0x00FF0000) >> 16))
	self.εντολήΘύρα.Εγγραφή(0x20)

	var κατάσταση uint8 = self.εντολήΘύρα.Ανάγνωση()
	for ((κατάσταση & 0x80) == 0x80) && ((κατάσταση & 0x01) != 0x01) {
		κατάσταση = self.εντολήΘύρα.Ανάγνωση()
	}

	if (κατάσταση & 0x01) != 0 {
		console_2.MΕκτύπωση(([]byte)("ata read error "))
		return
	}

	console_2.MΕκτύπωσηxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataΘύρα.Ανάγνωση()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bytespersector; i += 2 {
		self.dataΘύρα.Ανάγνωση()
	}
}
func (self *TΓιαπροχωρημένουςΤεχνολογίαattachment) Εγγραφή28(sectorΑριθμός uint32, data []byte, count uint32) {

	if sectorΑριθμός > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.κύριαέξοδος {
		self.συσκευήΘύρα.Εγγραφή(uint8(0xE0 | uint8((sectorΑριθμός&0x0F000000)>>24)))
	} else {
		self.συσκευήΘύρα.Εγγραφή(uint8(0xF0 | uint8((sectorΑριθμός&0x0F000000)>>24)))
	}

	self.σφάλμαΘύρα.Εγγραφή(0)
	self.sectorcountΘύρα.Εγγραφή(1)
	self.lbaΧαμηλήΘύρα.Εγγραφή(uint8(sectorΑριθμός & 0x000000FF))
	self.lbamidΘύρα.Εγγραφή(uint8((sectorΑριθμός & 0x0000FF00) >> 8))
	self.lbahiΘύρα.Εγγραφή(uint8((sectorΑριθμός & 0x00FF0000) >> 16))
	self.εντολήΘύρα.Εγγραφή(0x30)

	var console_2 = TConsole{}
	console_2.MΕκτύπωση(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataΘύρα.Εγγραφή(wdata)

		κείμενο := []byte("  ")
		κείμενο[0] = uint8((wdata >> 8) & 0xFF)
		κείμενο[1] = uint8(wdata & 0xFF)

		console_2.MΕκτύπωση(κείμενο)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataΘύρα.Εγγραφή(0x0000)
	}

}

func (self *TΓιαπροχωρημένουςΤεχνολογίαattachment) Flush() {
	if self.κύριαέξοδος {
		self.συσκευήΘύρα.Εγγραφή(0xE0)
	} else {
		self.συσκευήΘύρα.Εγγραφή(0xF0)
	}
	self.εντολήΘύρα.Εγγραφή(0xE7)

	var console_2 = TConsole{}

	var κατάσταση uint8 = self.εντολήΘύρα.Ανάγνωση()
	if κατάσταση == 0x00 {
		return
	}

	for ((κατάσταση & 0x80) == 0x80) && ((κατάσταση & 0x01) != 0x01) {
		κατάσταση = self.εντολήΘύρα.Ανάγνωση()
	}
	if (κατάσταση & 0x01) != 0 {
		console_2.MΕκτύπωση(([]byte)(" ata flush error"))
		return
	}

}
