/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "یادداشتmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tصارفdatagramprotocolheaderbuffer struct {
	مصدرپورٹnumber		[2]byte
	destinationپورٹnumber	[2]byte

	طول		[2]byte
	checksum	[2]byte
}

var udpheaderحجم uint32 = 8

type Tصارفdatagramprotocolheader struct {
	مصدرپورٹnumber		uint16
	destinationپورٹnumber	uint16

	طول		uint16
	checksum	uint16
}

func (self *Tصارفdatagramprotocolheader) Init(buffer_2 *Tصارفdatagramprotocolheaderbuffer) {
	self.مصدرپورٹnumber = Aلڑیtounsignedinteger16(buffer_2.مصدرپورٹnumber)
	self.destinationپورٹnumber = Aلڑیtounsignedinteger16(buffer_2.destinationپورٹnumber)

	self.طول = Aلڑیtounsignedinteger16(buffer_2.طول)
	self.checksum = Aلڑیtounsignedinteger16(buffer_2.checksum)
}
func (self *Tصارفdatagramprotocolheader) Sسیٹbuffer(buffer_2 *Tصارفdatagramprotocolheaderbuffer) {

	buffer_2.مصدرپورٹnumber = Unsignedinteger16toلڑی(self.مصدرپورٹnumber)
	buffer_2.destinationپورٹnumber = Unsignedinteger16toلڑی(self.destinationپورٹnumber)

	buffer_2.طول = Unsignedinteger16toلڑی(self.طول)
	buffer_2.checksum = Unsignedinteger16toلڑی(self.checksum)

}

type Iصارفdatagramprotocolhandler interface {
	Handleصارفdatagramprotocolپیغام(ساکٹ *Tصارفdatagramprotocolساکٹ, data uintptr, حجم uint16)
}

type Tصارفdatagramprotocolhandler struct {
}

func (self *Tصارفdatagramprotocolhandler) Init(backend Tانٹرنیٹprotocolprovider) {
}
func (self *Tصارفdatagramprotocolhandler) Handleصارفdatagramprotocolپیغام(ساکٹ *Tصارفdatagramprotocolساکٹ, data uintptr, حجم uint16) {
}

type Iصارفdatagramprotocolساکٹ interface {
	Handleصارفdatagramprotocolپیغام(data uintptr, حجم uint16)
}
type Tصارفdatagramprotocolساکٹ struct {
	remoteپورٹnumber	uint16
	remoteip		uint32
	مقامیپورٹnumber		uint16
	مقامیip			uint32

	listening	bool
}

var udpprovider Tصارفdatagramprotocolprovider
var udphandler Iصارفdatagramprotocolhandler

func (self *Tصارفdatagramprotocolساکٹ) Tٹیسٹ() {
}
func (self *Tصارفdatagramprotocolساکٹ) Init(pudpprovider Tصارفdatagramprotocolprovider, pudphandler Iصارفdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tصارفdatagramprotocolساکٹ) Handleصارفdatagramprotocolپیغام(data uintptr, حجم uint16) {
	if udphandler != nil {
		udphandler.Handleصارفdatagramprotocolپیغام(self, data, حجم)
	}
}
func (self *Tصارفdatagramprotocolساکٹ) Send(pdata []byte, حجم uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(حجم); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, حجم)
}
func (self *Tصارفdatagramprotocolساکٹ) Dاتصالمنطعکریں() {
	udpprovider.Dاتصالمنطعکریں(self)
}

type Tصارفdatagramprotocolprovider struct {
}

var iphandler Iانٹرنیٹprotocolhandler
var sockets [65535]Tصارفdatagramprotocolساکٹ
var numbersockets int
var خالیپورٹ uint16

func (self *Tصارفdatagramprotocolprovider) Init(pipprovider Tانٹرنیٹprotocolprovider, piphandler Iانٹرنیٹprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numbersockets = 0
	خالیپورٹ = 1024
}
func (self *Tصارفdatagramprotocolprovider) Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder uint32, destinationipaddressنیٹورکbyteorder uint32, انٹرنیٹprotocolpayload uintptr, حجم uint32) bool {
	if حجم < udpheaderحجم {
		return false
	}

	var buffer_2 *Tصارفdatagramprotocolheaderbuffer = (*Tصارفdatagramprotocolheaderbuffer)(Pointer(انٹرنیٹprotocolpayload))
	var msg Tصارفdatagramprotocolheader
	msg.Init(buffer_2)

	var ساکٹ *Tصارفdatagramprotocolساکٹ = nil

	for i := 0; i < numbersockets && ساکٹ == nil; i++ {
		if sockets[i].مقامیپورٹnumber == msg.destinationپورٹnumber && sockets[i].مقامیip == destinationipaddressنیٹورکbyteorder && sockets[i].listening == true {
			ساکٹ = &sockets[i]
			ساکٹ.listening = false
			ساکٹ.remoteپورٹnumber = msg.مصدرپورٹnumber
			ساکٹ.remoteip = مصدرipaddressنیٹورکbyteorder
		} else if sockets[i].مقامیپورٹnumber == msg.destinationپورٹnumber && sockets[i].مقامیip == destinationipaddressنیٹورکbyteorder && sockets[i].remoteپورٹnumber == msg.مصدرپورٹnumber && sockets[i].remoteip == مصدرipaddressنیٹورکbyteorder {
			ساکٹ = &sockets[i]

		}
	}

	msg.Sسیٹbuffer(buffer_2)
	if ساکٹ != nil {
		ساکٹ.Handleصارفdatagramprotocolپیغام(انٹرنیٹprotocolpayload+uintptr(udpheaderحجم), uint16(حجم-udpheaderحجم))
	}

	return false
}

func (self *Tصارفdatagramprotocolprovider) Cمتصلہوں(ip uint32, پورٹ uint16) *Tصارفdatagramprotocolساکٹ {
	var یادداشتmanager = &Tیادداشتmanager{}
	var ساکٹ = (*Tصارفdatagramprotocolساکٹ)(یادداشتmanager.Malloc(50))

	if ساکٹ != nil {

		ساکٹ.Init(*self, nil)
		ساکٹ.remoteپورٹnumber = پورٹ
		ساکٹ.remoteip = ip
		ساکٹ.مقامیپورٹnumber = خالیپورٹ
		خالیپورٹ++
		ساکٹ.مقامیip = uint32((*iphandler.Providerget()).Getipaddress())

		ساکٹ.remoteپورٹnumber = Unsignedinteger16r(ساکٹ.remoteپورٹnumber)
		ساکٹ.مقامیپورٹnumber = Unsignedinteger16r(ساکٹ.مقامیپورٹnumber)

		sockets[numbersockets] = *ساکٹ
		numbersockets++

	}
	return ساکٹ

}
func (self *Tصارفdatagramprotocolprovider) Listen(پورٹ uint16) *Tصارفdatagramprotocolساکٹ {
	var ساکٹ = &Tصارفdatagramprotocolساکٹ{}
	ساکٹ = nil
	if ساکٹ != nil {
		ساکٹ.Init(*self, nil)
		ساکٹ.listening = true
		ساکٹ.مقامیپورٹnumber = پورٹ
		ساکٹ.مقامیip = uint32((*iphandler.Providerget()).Getipaddress())

		ساکٹ.مقامیپورٹnumber = Unsignedinteger16r(ساکٹ.مقامیپورٹnumber)
	}
	return ساکٹ
}
func (self *Tصارفdatagramprotocolprovider) Dاتصالمنطعکریں(ساکٹ *Tصارفdatagramprotocolساکٹ) {
	for i := 0; i < numbersockets && ساکٹ == nil; i++ {
		if sockets[i] == *ساکٹ {
			numbersockets--
			sockets[i] = sockets[numbersockets]
			break
		}
	}
}
func (self *Tصارفdatagramprotocolprovider) Send(ساکٹ *Tصارفdatagramprotocolساکٹ, pdata uintptr, حجم uint16) {
	var میزانطول = uint32(حجم) + udpheaderحجم

	var buffer_2 [4096]byte

	var msgbuffer = (*Tصارفdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tصارفdatagramprotocolheader{}

	msg.مصدرپورٹnumber = ساکٹ.مقامیپورٹnumber
	msg.destinationپورٹnumber = ساکٹ.remoteپورٹnumber
	msg.طول = Unsignedinteger16r(uint16(میزانطول))

	msg.checksum = 0x0
	msg.Sسیٹbuffer(msgbuffer)

	var dataبائٹس [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(حجم); i++ {
		buffer_2[int(udpheaderحجم)+i] = dataبائٹس[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(ساکٹ.remoteip, 0x11, data, میزانطول)

}
func (self *Tصارفdatagramprotocolprovider) Bind(ساکٹ *Tصارفdatagramprotocolساکٹ, handler *Tصارفdatagramprotocolhandler) {
}
