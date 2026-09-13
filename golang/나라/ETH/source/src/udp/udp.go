package udp

import . "unsafe"
import . "console"
import . "util"
import . "ማስታወሻmanager"
import . "ipv4"

var udpconsole = TConsole{}

type Tተጠቃሚdatagramprotocolheaderbuffer struct {
	ምንጩportቁጥር		[2]byte
	destinationportቁጥር	[2]byte

	እርዝመት_2		[2]byte
	checksum	[2]byte
}

var udpheaderመጠን uint32 = 8

type Tተጠቃሚdatagramprotocolheader struct {
	ምንጩportቁጥር		uint16
	destinationportቁጥር	uint16

	እርዝመት_2		uint16
	checksum	uint16
}

func (self *Tተጠቃሚdatagramprotocolheader) Init(buffer_2 *Tተጠቃሚdatagramprotocolheaderbuffer) {
	self.ምንጩportቁጥር = Aማዘጋጃtounsignedinteger16(buffer_2.ምንጩportቁጥር)
	self.destinationportቁጥር = Aማዘጋጃtounsignedinteger16(buffer_2.destinationportቁጥር)

	self.እርዝመት_2 = Aማዘጋጃtounsignedinteger16(buffer_2.እርዝመት_2)
	self.checksum = Aማዘጋጃtounsignedinteger16(buffer_2.checksum)
}
func (self *Tተጠቃሚdatagramprotocolheader) Setbuffer(buffer_2 *Tተጠቃሚdatagramprotocolheaderbuffer) {

	buffer_2.ምንጩportቁጥር = Unsignedinteger16toማዘጋጃ(self.ምንጩportቁጥር)
	buffer_2.destinationportቁጥር = Unsignedinteger16toማዘጋጃ(self.destinationportቁጥር)

	buffer_2.እርዝመት_2 = Unsignedinteger16toማዘጋጃ(self.እርዝመት_2)
	buffer_2.checksum = Unsignedinteger16toማዘጋጃ(self.checksum)

}

type Iተጠቃሚdatagramprotocolhandler interface {
	Handleተጠቃሚdatagramprotocolመልእክት(ሶኬት *Tተጠቃሚdatagramprotocolሶኬት, data uintptr, መጠን uint16)
}

type Tተጠቃሚdatagramprotocolhandler struct {
}

func (self *Tተጠቃሚdatagramprotocolhandler) Init(backend Tኢንተርኔትprotocolprovider) {
}
func (self *Tተጠቃሚdatagramprotocolhandler) Handleተጠቃሚdatagramprotocolመልእክት(ሶኬት *Tተጠቃሚdatagramprotocolሶኬት, data uintptr, መጠን uint16) {
}

type Iተጠቃሚdatagramprotocolሶኬት interface {
	Handleተጠቃሚdatagramprotocolመልእክት(data uintptr, መጠን uint16)
}
type Tተጠቃሚdatagramprotocolሶኬት struct {
	remoteportቁጥር	uint16
	remoteip	uint32
	አካባቢportቁጥር	uint16
	አካባቢip		uint32

	listening	bool
}

var udpprovider Tተጠቃሚdatagramprotocolprovider
var udphandler Iተጠቃሚdatagramprotocolhandler

func (self *Tተጠቃሚdatagramprotocolሶኬት) Tመሞከሪያ() {
}
func (self *Tተጠቃሚdatagramprotocolሶኬት) Init(pudpprovider Tተጠቃሚdatagramprotocolprovider, pudphandler Iተጠቃሚdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *Tተጠቃሚdatagramprotocolሶኬት) Handleተጠቃሚdatagramprotocolመልእክት(data uintptr, መጠን uint16) {
	if udphandler != nil {
		udphandler.Handleተጠቃሚdatagramprotocolመልእክት(self, data, መጠን)
	}
}
func (self *Tተጠቃሚdatagramprotocolሶኬት) Send(pdata []byte, መጠን uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(መጠን); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Send(self, data, መጠን)
}
func (self *Tተጠቃሚdatagramprotocolሶኬት) Dመለያያ() {
	udpprovider.Dመለያያ(self)
}

type Tተጠቃሚdatagramprotocolprovider struct {
}

var iphandler Iኢንተርኔትprotocolhandler
var sockets [65535]Tተጠቃሚdatagramprotocolሶኬት
var ቁጥርsockets int
var ነፃport uint16

func (self *Tተጠቃሚdatagramprotocolprovider) Init(pipprovider Tኢንተርኔትprotocolprovider, piphandler Iኢንተርኔትprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	ቁጥርsockets = 0
	ነፃport = 1024
}
func (self *Tተጠቃሚdatagramprotocolprovider) Oኢንተርኔትprotocolreceivewhen(ምንጩipaddressኔትዎርክbyteorder uint32, destinationipaddressኔትዎርክbyteorder uint32, ኢንተርኔትprotocolpayload uintptr, መጠን uint32) bool {
	if መጠን < udpheaderመጠን {
		return false
	}

	var buffer_2 *Tተጠቃሚdatagramprotocolheaderbuffer = (*Tተጠቃሚdatagramprotocolheaderbuffer)(Pointer(ኢንተርኔትprotocolpayload))
	var msg Tተጠቃሚdatagramprotocolheader
	msg.Init(buffer_2)

	var ሶኬት *Tተጠቃሚdatagramprotocolሶኬት = nil

	for i := 0; i < ቁጥርsockets && ሶኬት == nil; i++ {
		if sockets[i].አካባቢportቁጥር == msg.destinationportቁጥር && sockets[i].አካባቢip == destinationipaddressኔትዎርክbyteorder && sockets[i].listening == true {
			ሶኬት = &sockets[i]
			ሶኬት.listening = false
			ሶኬት.remoteportቁጥር = msg.ምንጩportቁጥር
			ሶኬት.remoteip = ምንጩipaddressኔትዎርክbyteorder
		} else if sockets[i].አካባቢportቁጥር == msg.destinationportቁጥር && sockets[i].አካባቢip == destinationipaddressኔትዎርክbyteorder && sockets[i].remoteportቁጥር == msg.ምንጩportቁጥር && sockets[i].remoteip == ምንጩipaddressኔትዎርክbyteorder {
			ሶኬት = &sockets[i]

		}
	}

	msg.Setbuffer(buffer_2)
	if ሶኬት != nil {
		ሶኬት.Handleተጠቃሚdatagramprotocolመልእክት(ኢንተርኔትprotocolpayload+uintptr(udpheaderመጠን), uint16(መጠን-udpheaderመጠን))
	}

	return false
}

func (self *Tተጠቃሚdatagramprotocolprovider) Cመገናኛ(ip uint32, port uint16) *Tተጠቃሚdatagramprotocolሶኬት {
	var ማስታወሻmanager = &Tማስታወሻmanager{}
	var ሶኬት = (*Tተጠቃሚdatagramprotocolሶኬት)(ማስታወሻmanager.Malloc(50))

	if ሶኬት != nil {

		ሶኬት.Init(*self, nil)
		ሶኬት.remoteportቁጥር = port
		ሶኬት.remoteip = ip
		ሶኬት.አካባቢportቁጥር = ነፃport
		ነፃport++
		ሶኬት.አካባቢip = uint32((*iphandler.Providerget()).Getipaddress())

		ሶኬት.remoteportቁጥር = Unsignedinteger16r(ሶኬት.remoteportቁጥር)
		ሶኬት.አካባቢportቁጥር = Unsignedinteger16r(ሶኬት.አካባቢportቁጥር)

		sockets[ቁጥርsockets] = *ሶኬት
		ቁጥርsockets++

	}
	return ሶኬት

}
func (self *Tተጠቃሚdatagramprotocolprovider) Listen(port uint16) *Tተጠቃሚdatagramprotocolሶኬት {
	var ሶኬት = &Tተጠቃሚdatagramprotocolሶኬት{}
	ሶኬት = nil
	if ሶኬት != nil {
		ሶኬት.Init(*self, nil)
		ሶኬት.listening = true
		ሶኬት.አካባቢportቁጥር = port
		ሶኬት.አካባቢip = uint32((*iphandler.Providerget()).Getipaddress())

		ሶኬት.አካባቢportቁጥር = Unsignedinteger16r(ሶኬት.አካባቢportቁጥር)
	}
	return ሶኬት
}
func (self *Tተጠቃሚdatagramprotocolprovider) Dመለያያ(ሶኬት *Tተጠቃሚdatagramprotocolሶኬት) {
	for i := 0; i < ቁጥርsockets && ሶኬት == nil; i++ {
		if sockets[i] == *ሶኬት {
			ቁጥርsockets--
			sockets[i] = sockets[ቁጥርsockets]
			break
		}
	}
}
func (self *Tተጠቃሚdatagramprotocolprovider) Send(ሶኬት *Tተጠቃሚdatagramprotocolሶኬት, pdata uintptr, መጠን uint16) {
	var ጠቅላላእርዝመት = uint32(መጠን) + udpheaderመጠን

	var buffer_2 [4096]byte

	var msgbuffer = (*Tተጠቃሚdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = Tተጠቃሚdatagramprotocolheader{}

	msg.ምንጩportቁጥር = ሶኬት.አካባቢportቁጥር
	msg.destinationportቁጥር = ሶኬት.remoteportቁጥር
	msg.እርዝመት_2 = Unsignedinteger16r(uint16(ጠቅላላእርዝመት))

	msg.checksum = 0x0
	msg.Setbuffer(msgbuffer)

	var dataባይትስ [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(መጠን); i++ {
		buffer_2[int(udpheaderመጠን)+i] = dataባይትስ[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Send(ሶኬት.remoteip, 0x11, data, ጠቅላላእርዝመት)

}
func (self *Tተጠቃሚdatagramprotocolprovider) Bind(ሶኬት *Tተጠቃሚdatagramprotocolሶኬት, handler *Tተጠቃሚdatagramprotocolhandler,) {
}
