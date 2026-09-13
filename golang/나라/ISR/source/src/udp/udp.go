package udp

import . "unsafe"
import . "console"
import . "util"
import . "זיכרוןmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tמשתמשdatagramprotocolheaderbuffer struct {
	מקורשערמספר	[2]byte
	יעדשערמספר	[2]byte

	אורך		[2]byte
	checksum	[2]byte
}

var udpheaderגודל uint32 = 8

type Tמשתמשdatagramprotocolheader struct {
	מקורשערמספר	uint16
	יעדשערמספר	uint16

	אורך		uint16
	checksum	uint16
}

func (self *Tמשתמשdatagramprotocolheader) Init(buffer_2 *Tמשתמשdatagramprotocolheaderbuffer) {
	self.מקורשערמספר = Aמערךtounsignedinteger16(buffer_2.מקורשערמספר)
	self.יעדשערמספר = Aמערךtounsignedinteger16(buffer_2.יעדשערמספר)

	self.אורך = Aמערךtounsignedinteger16(buffer_2.אורך)
	self.checksum = Aמערךtounsignedinteger16(buffer_2.checksum)
}
func (self *Tמשתמשdatagramprotocolheader) Sקבעbuffer(buffer_2 *Tמשתמשdatagramprotocolheaderbuffer) {

	buffer_2.מקורשערמספר = Unsignedinteger16toמערך(self.מקורשערמספר)
	buffer_2.יעדשערמספר = Unsignedinteger16toמערך(self.יעדשערמספר)

	buffer_2.אורך = Unsignedinteger16toמערך(self.אורך)
	buffer_2.checksum = Unsignedinteger16toמערך(self.checksum)

}

type Iמשתמשdatagramprotocolhandler interface {
	Hידיתמשתמשdatagramprotocolהודעה(שקע *Tמשתמשdatagramprotocolשקע, data uintptr, גודל uint16)
}

type Tמשתמשdatagramprotocolhandler struct {
}

func (self *Tמשתמשdatagramprotocolhandler) Init(backend Tאינטרנטprotocolprovider) {
}
func (self *Tמשתמשdatagramprotocolhandler) Hידיתמשתמשdatagramprotocolהודעה(שקע *Tמשתמשdatagramprotocolשקע, data uintptr, גודל uint16) {
}

type Iמשתמשdatagramprotocolשקע interface {
	Hידיתמשתמשdatagramprotocolהודעה(data uintptr, גודל uint16)
}
type Tמשתמשdatagramprotocolשקע struct {
	מרוחקשערמספר	uint16
	מרוחקip		uint32
	מקומישערמספר	uint16
	מקומיip		uint32

	listening	bool
}

var udpprovider Tמשתמשdatagramprotocolprovider
var udphandler Iמשתמשdatagramprotocolhandler

func (self *Tמשתמשdatagramprotocolשקע) Tבדיקה() {
}
func (self *Tמשתמשdatagramprotocolשקע) Init(pudpprovider Tמשתמשdatagramprotocolprovider, pudphandler Iמשתמשdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tמשתמשdatagramprotocolשקע) Hידיתמשתמשdatagramprotocolהודעה(data uintptr, גודל uint16) {
	if udphandler != nil {
		udphandler.Hידיתמשתמשdatagramprotocolהודעה(self, data, גודל)
	}
}
func (self *Tמשתמשdatagramprotocolשקע) Sשלח(pdata []byte, גודל uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(גודל); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Sשלח(self, data, גודל)
}
func (self *Tמשתמשdatagramprotocolשקע) Dניתוק() {
	udpprovider.Dניתוק(self)
}

type Tמשתמשdatagramprotocolprovider struct {
}

var iphandler Iאינטרנטprotocolhandler
var sockets [65535]Tמשתמשdatagramprotocolשקע
var מספרsockets int
var פנוישער uint16

func (self *Tמשתמשdatagramprotocolprovider) Init(pipprovider Tאינטרנטprotocolprovider, piphandler Iאינטרנטprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	מספרsockets = 0
	פנוישער = 1024
}
func (self *Tמשתמשdatagramprotocolprovider) Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder uint32, יעדipaddressרשתbyteorder uint32, אינטרנטprotocolpayload uintptr, גודל uint32) bool {
	if גודל < udpheaderגודל {
		return false
	}

	var buffer_2 *Tמשתמשdatagramprotocolheaderbuffer = (*Tמשתמשdatagramprotocolheaderbuffer)(Pointer(אינטרנטprotocolpayload))
	var msg Tמשתמשdatagramprotocolheader
	msg.Init(buffer_2)

	var שקע *Tמשתמשdatagramprotocolשקע = nil

	for i := 0; i < מספרsockets && שקע == nil; i++ {
		if sockets[i].מקומישערמספר == msg.יעדשערמספר && sockets[i].מקומיip == יעדipaddressרשתbyteorder && sockets[i].listening == true {
			שקע = &sockets[i]
			שקע.listening = false
			שקע.מרוחקשערמספר = msg.מקורשערמספר
			שקע.מרוחקip = מקורipaddressרשתbyteorder
		} else if sockets[i].מקומישערמספר == msg.יעדשערמספר && sockets[i].מקומיip == יעדipaddressרשתbyteorder && sockets[i].מרוחקשערמספר == msg.מקורשערמספר && sockets[i].מרוחקip == מקורipaddressרשתbyteorder {
			שקע = &sockets[i]

		}
	}

	msg.Sקבעbuffer(buffer_2)
	if שקע != nil {
		שקע.Hידיתמשתמשdatagramprotocolהודעה(אינטרנטprotocolpayload+uintptr(udpheaderגודל), uint16(גודל-udpheaderגודל))
	}

	return false
}

func (self *Tמשתמשdatagramprotocolprovider) Cחיבור(ip uint32, שער uint16) *Tמשתמשdatagramprotocolשקע {
	var זיכרוןmanager = &Tזיכרוןmanager{}
	var שקע = (*Tמשתמשdatagramprotocolשקע)(זיכרוןmanager.Malloc(50))

	if שקע != nil {

		שקע.Init(*self, nil)
		שקע.מרוחקשערמספר = שער
		שקע.מרוחקip = ip
		שקע.מקומישערמספר = פנוישער
		פנוישער++
		שקע.מקומיip = uint32((*iphandler.Providerget()).Getipaddress())

		שקע.מרוחקשערמספר = Unsignedinteger16r(שקע.מרוחקשערמספר)
		שקע.מקומישערמספר = Unsignedinteger16r(שקע.מקומישערמספר)

		sockets[מספרsockets] = *שקע
		מספרsockets++

	}
	return שקע

}
func (self *Tמשתמשdatagramprotocolprovider) Listen(שער uint16) *Tמשתמשdatagramprotocolשקע {
	var שקע = &Tמשתמשdatagramprotocolשקע{}
	שקע = nil
	if שקע != nil {
		שקע.Init(*self, nil)
		שקע.listening = true
		שקע.מקומישערמספר = שער
		שקע.מקומיip = uint32((*iphandler.Providerget()).Getipaddress())

		שקע.מקומישערמספר = Unsignedinteger16r(שקע.מקומישערמספר)
	}
	return שקע
}
func (self *Tמשתמשdatagramprotocolprovider) Dניתוק(שקע *Tמשתמשdatagramprotocolשקע) {
	for i := 0; i < מספרsockets && שקע == nil; i++ {
		if sockets[i] == *שקע {
			מספרsockets--
			sockets[i] = sockets[מספרsockets]
			break
		}
	}
}
func (self *Tמשתמשdatagramprotocolprovider) Sשלח(שקע *Tמשתמשdatagramprotocolשקע, pdata uintptr, גודל uint16) {
	var totalאורך = uint32(גודל) + udpheaderגודל

	var buffer_2 [4096]byte

	var msgbuffer = (*Tמשתמשdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tמשתמשdatagramprotocolheader{}

	msg.מקורשערמספר = שקע.מקומישערמספר
	msg.יעדשערמספר = שקע.מרוחקשערמספר
	msg.אורך = Unsignedinteger16r(uint16(totalאורך))

	msg.checksum = 0x0
	msg.Sקבעbuffer(msgbuffer)

	var dataבתים [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(גודל); i++ {
		buffer_2[int(udpheaderגודל)+i] = dataבתים[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Sשלח(שקע.מרוחקip, 0x11, data, totalאורך)

}
func (self *Tמשתמשdatagramprotocolprovider) Bind(שקע *Tמשתמשdatagramprotocolשקע, handler *Tמשתמשdatagramprotocolhandler) {
}
