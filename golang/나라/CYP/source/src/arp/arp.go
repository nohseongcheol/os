package arp

import . "unsafe"
import . "console"
import . "ethernetΠλαίσιο"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpΜήνυμαbuffer struct {
	υλικόΤύπος		[2]byte
	protocol		[2]byte
	υλικόaddressΜέγεθος	byte
	protocoladdressΜέγεθος	byte
	εντολή			[2]byte

	πηγήmacaddress		[6]byte
	πηγήipaddress		[4]byte
	προορισμόςmacaddress	[6]byte
	προορισμόςipaddress	[4]byte
}

var arpmesgΜέγεθος uint32 = (64+92+64)/8 + 2

type ArpΜήνυμα struct {
	υλικόΤύπος		uint16
	protocol		uint16
	υλικόaddressΜέγεθος	uint8
	protocoladdressΜέγεθος	uint8
	εντολή			uint16

	πηγήmacaddress		uint64
	πηγήipaddress		uint32
	προορισμόςmacaddress	uint64
	προορισμόςipaddress	uint32
}

func (self *ArpΜήνυμα) Init(buffer_2 *ArpΜήνυμαbuffer) {

	self.υλικόΤύπος = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.υλικόΤύπος))
	self.protocol = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.protocol))
	self.υλικόaddressΜέγεθος = byte(buffer_2.υλικόaddressΜέγεθος)
	self.protocoladdressΜέγεθος = byte(buffer_2.protocoladdressΜέγεθος)
	self.εντολή = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.εντολή))

	self.πηγήmacaddress = Unsignedinteger48r(Διάταξηtounsignedinteger48(buffer_2.πηγήmacaddress))
	self.πηγήipaddress = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer_2.πηγήipaddress))
	self.προορισμόςmacaddress = Unsignedinteger48r(Διάταξηtounsignedinteger48(buffer_2.προορισμόςmacaddress))
	self.προορισμόςipaddress = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer_2.προορισμόςipaddress))
}
func (self *ArpΜήνυμα) Σύνολοbuffer(buffer_2 *ArpΜήνυμαbuffer) {
	buffer_2.υλικόΤύπος = Unsignedinteger16toΔιάταξη(self.υλικόΤύπος)
	buffer_2.protocol = Unsignedinteger16toΔιάταξη(self.protocol)
	buffer_2.υλικόaddressΜέγεθος = uint8(self.υλικόaddressΜέγεθος)
	buffer_2.protocoladdressΜέγεθος = uint8(self.protocoladdressΜέγεθος)

	buffer_2.εντολή = Unsignedinteger16toΔιάταξη(self.εντολή)
	buffer_2.πηγήmacaddress = Unsignedinteger48toΔιάταξη(self.πηγήmacaddress)
	buffer_2.πηγήipaddress = Unsignedinteger32toΔιάταξη(self.πηγήipaddress)
	buffer_2.προορισμόςmacaddress = Unsignedinteger48toΔιάταξη(self.προορισμόςmacaddress)
	buffer_2.προορισμόςipaddress = Unsignedinteger32toΔιάταξη(self.προορισμόςipaddress)
}

type ArpethernetΠλαίσιοhandler struct {
	TEthernetΠλαίσιοhandler
}

var arpprovider Arpprovider
var ethernetΠλαίσιοprovider TEthernetΠλαίσιοprovider

func (self *ArpethernetΠλαίσιοhandler) EthernetΠλαίσιοreceivewhen(dataΔείκτης uintptr, μέγεθος int) bool {
	arpconsole.MΕκτύπωσηxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetΠλαίσιοreceivewhen(dataΔείκτης, uint32(μέγεθος))

}
func (self *ArpethernetΠλαίσιοhandler) Αποστολή(προορισμόςmacbe uint64, dataΔείκτης uintptr, μέγεθος uint32) {
	arpconsole.MΕκτύπωσηxy([]byte("arp send:"), 0, 24)
	var ethernetΤύποςbe = Unsignedinteger16r(0x0806)
	self.TEthernetΠλαίσιοhandler.ΠλαίσιοΑποστολή(προορισμόςmacbe, ethernetΤύποςbe, dataΔείκτης, μέγεθος)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	αριθμόςcacheκαταχώρηση	int

	handler	IEthernetΠλαίσιοhandler
}

var handler IEthernetΠλαίσιοhandler

func (self *Arpprovider) Init(backend TEthernetΠλαίσιοprovider, userhandler IEthernetΠλαίσιοhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Σύνολοhandler(userhandler, 0x0806)
	self.αριθμόςcacheκαταχώρηση = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetΠλαίσιοreceivewhen(dataΔείκτης uintptr, μέγεθος uint32) bool {

	if μέγεθος < arpmesgΜέγεθος {
		return false
	}
	var arpbuffer *ArpΜήνυμαbuffer = (*ArpΜήνυμαbuffer)(Pointer(dataΔείκτης))
	var arp ArpΜήνυμα = ArpΜήνυμα{}
	arp.Init(arpbuffer)

	if arp.υλικόΤύπος == 0x0100 {

		if arp.protocol == 0x0008 && arp.υλικόaddressΜέγεθος == 6 && arp.protocoladdressΜέγεθος == 4 && uint64(arp.προορισμόςipaddress) == handler.Getipaddress() {

			arpconsole.MΕκτύπωση([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Εκτύπωση(arp.protocol)
			arpconsole.MΕκτύπωση([]byte(":"))
			arpconsole.MUnsignedinteger64Εκτύπωση(uint64(arp.προορισμόςmacaddress))
			arpconsole.MΕκτύπωση([]byte(":"))
			arpconsole.MUnsignedinteger16Εκτύπωση(arp.εντολή)
			arpconsole.MΕκτύπωση([]byte(":"))
			arpconsole.MUnsignedinteger64Εκτύπωση(handler.Getmacaddress())

			switch arp.εντολή {
			case 0x0100:

				if self.Getmacfromcache(arp.πηγήipaddress) == 0xFFFFFFFFFFFF {
					if self.αριθμόςcacheκαταχώρηση < 128 {
						self.Ipcache[self.αριθμόςcacheκαταχώρηση] = arp.πηγήipaddress
						self.Maccache[self.αριθμόςcacheκαταχώρηση] = arp.πηγήmacaddress
						self.αριθμόςcacheκαταχώρηση++
					}
				}
				arp.εντολή = 0x0200
				arp.προορισμόςipaddress = arp.πηγήipaddress
				arp.προορισμόςmacaddress = arp.πηγήmacaddress
				arp.πηγήipaddress = uint32(handler.Getipaddress())
				arp.πηγήmacaddress = handler.Getmacaddress()
				arp.Σύνολοbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MΕκτύπωση(([]byte)("self.numCacheEntries"))

				if self.αριθμόςcacheκαταχώρηση < 128 {
					self.Ipcache[self.αριθμόςcacheκαταχώρηση] = arp.πηγήipaddress
					self.Maccache[self.αριθμόςcacheκαταχώρηση] = arp.πηγήmacaddress
					self.αριθμόςcacheκαταχώρηση++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpΔίκτυοbyteorder uint32) {

	var arp ArpΜήνυμα = ArpΜήνυμα{}
	arp.υλικόΤύπος = 0x0100
	arp.protocol = 0x0008
	arp.υλικόaddressΜέγεθος = 6
	arp.protocoladdressΜέγεθος = 4
	arp.εντολή = 0x0200

	arp.πηγήipaddress = uint32(handler.Getipaddress())

	arp.προορισμόςmacaddress = self.Resolve(IpΔίκτυοbyteorder)
	arp.προορισμόςipaddress = IpΔίκτυοbyteorder
	arpconsole.MΕκτύπωσηxy([]byte("broad mac"), 0, 15)

	arp.πηγήmacaddress = handler.Getmacaddress()

	var arpbuffer ArpΜήνυμαbuffer = ArpΜήνυμαbuffer{}
	arp.Σύνολοbuffer(&arpbuffer)

	var δείκτης uintptr = uintptr(Pointer(&arpbuffer))
	handler.Αποστολή(arp.προορισμόςmacaddress, δείκτης, arpmesgΜέγεθος)
}
func (self *Arpprovider) Requestmacaddress(IpΔίκτυοbyteorder uint32) {

	var arp ArpΜήνυμα = ArpΜήνυμα{}
	arp.υλικόΤύπος = 0x0100

	arp.protocol = 0x0008
	arp.υλικόaddressΜέγεθος = 6
	arp.protocoladdressΜέγεθος = 4
	arp.εντολή = 0x0100

	arp.πηγήmacaddress = handler.Getmacaddress()
	arp.πηγήipaddress = uint32(handler.Getipaddress())

	arp.προορισμόςmacaddress = 0xFFFFFFFFFFFF
	arp.προορισμόςipaddress = IpΔίκτυοbyteorder

	var arpbuffer ArpΜήνυμαbuffer = ArpΜήνυμαbuffer{}
	arp.Σύνολοbuffer(&arpbuffer)

	var δείκτης uintptr = uintptr(Pointer(&arpbuffer))
	handler.Αποστολή(arp.προορισμόςmacaddress, δείκτης, arpmesgΜέγεθος)
}
func (self *Arpprovider) ΔοκιμήΕκτύπωση(data *[]byte, μέγεθος uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MΕκτύπωσηxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalΕκτύπωση(buffer_2[i])
		arpconsole.MΕκτύπωση([]byte(":"))
	}
	arpconsole.MΕκτύπωση([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpΔίκτυοbyteorder uint32) uint64 {
	for i := 0; i < self.αριθμόςcacheκαταχώρηση; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MΕκτύπωση(([]byte)("["))
		arpconsole.MUnsignedinteger32Εκτύπωση(self.Ipcache[i])
		arpconsole.MΕκτύπωση(([]byte)(":"))
		arpconsole.MUnsignedinteger32Εκτύπωση(IpΔίκτυοbyteorder)
		arpconsole.MΕκτύπωση(([]byte)(":"))
		arpconsole.MΕκτύπωση(([]byte)(":"))
		arpconsole.MUnsignedinteger64Εκτύπωση(self.Maccache[i])
		arpconsole.MΕκτύπωση(([]byte)("]\n"))

		if self.Ipcache[i] == IpΔίκτυοbyteorder {
			arpconsole.MΕκτύπωση([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpΔίκτυοbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpΔίκτυοbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpΔίκτυοbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpΔίκτυοbyteorder)

	}

	return result
}
