package pci

import . "port"
import . "sampuk"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Bukagetdriver(peranti TPeripheralcomponentinterconnectPerantidescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TLalaipcicontrollerhandler struct {
}

func (diri TLalaipcicontrollerhandler) Bukagetdriver(peranti TPeripheralcomponentinterconnectPerantidescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectPerantidescriptor struct {
	Portbase	uint32
	Sampuk		uint32

	bus		uint16
	peranti_2	uint16
	fungsi		uint16

	Pembekalid	uint16
	Perantiid	uint16

	kelasid		uint8
	subclassid	uint8
	antaramukaid	uint8

	revision	uint8
}

func (diri *TPeripheralcomponentinterconnectPerantidescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	perintahport		uint16
}

func (diri *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	diri.dataport = 0xCFC
	diri.perintahport = 0xCF8

	diri.ipcicontrollerhandler = TLalaipcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		diri.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (diri *TPeripheralcomponentinterconnectcontroller) Baca(bus uint16, peranti_2 uint16, fungsi uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(peranti_2&0x1f) << 11) | (uint32(fungsi&0x07) << 8) | uint32(registeroffset&0xFC)

	PortTulisdword(diri.perintahport, id)

	result1 := PortBacadword(diri.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (diri *TPeripheralcomponentinterconnectcontroller) Tulis(bus uint16, peranti_2 uint16, fungsi uint16, registeroffset uint32, nilai uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((peranti_2&0x1f)<<11) | uint32((fungsi&0x07)<<8) | uint32(registeroffset&0xFC)
	PortTulisdword(diri.perintahport, id)
	PortTulisdword(diri.dataport, nilai)
}
func (diri *TPeripheralcomponentinterconnectcontroller) Perantihasfunctions(bus uint16, peranti_2 uint16) bool {
	result := diri.Baca(bus, peranti_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (diri *TPeripheralcomponentinterconnectcontroller) Pilihdriver(drivermanager *TDrivermanager, interrupts *TSampukmanager) {
	for bus := 0; bus < 8; bus++ {
		for peranti_2 := 0; peranti_2 < 32; peranti_2++ {

			var nOMBORfunctions int = 1
			if diri.Perantihasfunctions(uint16(bus), uint16(peranti_2)) == true {
				nOMBORfunctions = 8
			} else {
				nOMBORfunctions = 1
			}

			for fungsi := 0; fungsi < nOMBORfunctions; fungsi++ {
				var peranti TPeripheralcomponentinterconnectPerantidescriptor
				peranti = diri.GetPerantidescriptor(uint16(bus), uint16(peranti_2), uint16(fungsi))
				if peranti.Pembekalid == 0x0000 || peranti.Pembekalid == 0xFFFF {
					continue
				}

				for palangNOMBOR := 0; palangNOMBOR < 6; palangNOMBOR++ {
					var palang TBaseaddressregister = diri.Getbaseaddressregister(uint16(bus), uint16(peranti_2), uint16(fungsi), uint16(palangNOMBOR))
					if palang.address_2 != 0 && (palang.regtype == 1) {
						peranti.Portbase = palang.address_2
					}

					diri.Getdriver(peranti, interrupts)

				}

			}

		}
	}
}
func (diri *TPeripheralcomponentinterconnectcontroller) GetPerantidescriptor(bus uint16, peranti_2 uint16, fungsi uint16) TPeripheralcomponentinterconnectPerantidescriptor {
	var result TPeripheralcomponentinterconnectPerantidescriptor
	result = TPeripheralcomponentinterconnectPerantidescriptor{}
	result.bus = bus
	result.peranti_2 = peranti_2
	result.fungsi = fungsi

	result.Pembekalid = uint16(diri.Baca(bus, peranti_2, fungsi, 0x00))
	result.Perantiid = uint16(diri.Baca(bus, peranti_2, fungsi, 0x02))

	result.kelasid = uint8(diri.Baca(bus, peranti_2, fungsi, 0x0b))
	result.subclassid = uint8(diri.Baca(bus, peranti_2, fungsi, 0x0a))
	result.antaramukaid = uint8(diri.Baca(bus, peranti_2, fungsi, 0x09))

	result.revision = uint8(diri.Baca(bus, peranti_2, fungsi, 0x08))
	result.Sampuk = uint32(diri.Baca(bus, peranti_2, fungsi, 0x3C))

	return result
}
func (diri *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, peranti_2 uint16, fungsi uint16, palang uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := diri.Baca(bus, peranti_2, fungsi, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if palang >= uint16(maksbars) {
		return result
	}

	palangNilai := diri.Baca(bus, peranti_2, fungsi, uint32(0x10+4*palang))

	if (palangNilai & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = palangNilai & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (diri *TPeripheralcomponentinterconnectcontroller) Getdriver(peranti TPeripheralcomponentinterconnectPerantidescriptor, interrupts *TSampukmanager) {

	diri.ipcicontrollerhandler.Bukagetdriver(peranti)

}
