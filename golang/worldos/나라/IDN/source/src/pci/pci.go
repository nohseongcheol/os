/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interupsi"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Hidupgetdriver(perangkat TPeripheralcomponentinterconnectPerangkatdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TBakupcicontrollerhandler struct {
}

func (dirisendiri TBakupcicontrollerhandler) Hidupgetdriver(perangkat TPeripheralcomponentinterconnectPerangkatdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectPerangkatdescriptor struct {
	Portbase	uint32
	Interupsi	uint32

	bus		uint16
	perangkat_2	uint16
	fungsi		uint16

	Vendorid	uint16
	Perangkatid	uint16

	kelasid		uint8
	subclassid	uint8
	antarmukaid	uint8

	revision	uint8
}

func (dirisendiri *TPeripheralcomponentinterconnectPerangkatdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	perintahport		uint16
}

func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	dirisendiri.dataport = 0xCFC
	dirisendiri.perintahport = 0xCF8

	dirisendiri.ipcicontrollerhandler = TBakupcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		dirisendiri.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Baca(bus uint16, perangkat_2 uint16, fungsi uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(perangkat_2&0x1f) << 11) | (uint32(fungsi&0x07) << 8) | uint32(registeroffset&0xFC)

	PortTulisdword(dirisendiri.perintahport, id)

	hASIL1 := PortBacadword(dirisendiri.dataport)
	hASIL2 := (hASIL1 >> (8 * (registeroffset % 4)))

	return hASIL2
}

func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Tulis(bus uint16, perangkat_2 uint16, fungsi uint16, registeroffset uint32, nilai uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((perangkat_2&0x1f)<<11) | uint32((fungsi&0x07)<<8) | uint32(registeroffset&0xFC)
	PortTulisdword(dirisendiri.perintahport, id)
	PortTulisdword(dirisendiri.dataport, nilai)
}
func (dirisendiri *TPeripheralcomponentinterconnectcontroller) PerangkathasFungsi(bus uint16, perangkat_2 uint16) bool {
	hASIL := dirisendiri.Baca(bus, perangkat_2, 0, 0x0E)
	if (hASIL & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Pilihdriver(drivermanager *TDrivermanager, interrupts *TInterupsimanager) {
	for bus := 0; bus < 8; bus++ {
		for perangkat_2 := 0; perangkat_2 < 32; perangkat_2++ {

			var nomorFungsi int = 1
			if dirisendiri.PerangkathasFungsi(uint16(bus), uint16(perangkat_2)) == true {
				nomorFungsi = 8
			} else {
				nomorFungsi = 1
			}

			for fungsi := 0; fungsi < nomorFungsi; fungsi++ {
				var perangkat TPeripheralcomponentinterconnectPerangkatdescriptor
				perangkat = dirisendiri.GetPerangkatdescriptor(uint16(bus), uint16(perangkat_2), uint16(fungsi))
				if perangkat.Vendorid == 0x0000 || perangkat.Vendorid == 0xFFFF {
					continue
				}

				for batangNomor := 0; batangNomor < 6; batangNomor++ {
					var batang TBaseaddressregister = dirisendiri.Getbaseaddressregister(uint16(bus), uint16(perangkat_2), uint16(fungsi), uint16(batangNomor))
					if batang.address_2 != 0 && (batang.regtype == 1) {
						perangkat.Portbase = batang.address_2
					}

					dirisendiri.Getdriver(perangkat, interrupts)

				}

			}

		}
	}
}
func (dirisendiri *TPeripheralcomponentinterconnectcontroller) GetPerangkatdescriptor(bus uint16, perangkat_2 uint16, fungsi uint16) TPeripheralcomponentinterconnectPerangkatdescriptor {
	var hASIL TPeripheralcomponentinterconnectPerangkatdescriptor
	hASIL = TPeripheralcomponentinterconnectPerangkatdescriptor{}
	hASIL.bus = bus
	hASIL.perangkat_2 = perangkat_2
	hASIL.fungsi = fungsi

	hASIL.Vendorid = uint16(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x00))
	hASIL.Perangkatid = uint16(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x02))

	hASIL.kelasid = uint8(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x0b))
	hASIL.subclassid = uint8(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x0a))
	hASIL.antarmukaid = uint8(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x09))

	hASIL.revision = uint8(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x08))
	hASIL.Interupsi = uint32(dirisendiri.Baca(bus, perangkat_2, fungsi, 0x3C))

	return hASIL
}
func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, perangkat_2 uint16, fungsi uint16, batang uint16) TBaseaddressregister {
	var hASIL TBaseaddressregister

	headertype := dirisendiri.Baca(bus, perangkat_2, fungsi, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if batang >= uint16(maksbars) {
		return hASIL
	}

	batangNilai := dirisendiri.Baca(bus, perangkat_2, fungsi, uint32(0x10+4*batang))

	if (batangNilai & 0x1) != 0 {
		hASIL.regtype = 1
	} else {
		hASIL.regtype = 0
	}

	if hASIL.regtype == 0 {
	} else {
		hASIL.address_2 = batangNilai & ^uint32(0x3)
		hASIL.prefetchcapable = false
	}

	return hASIL
}
func (dirisendiri *TPeripheralcomponentinterconnectcontroller) Getdriver(perangkat TPeripheralcomponentinterconnectPerangkatdescriptor, interrupts *TInterupsimanager) {

	dirisendiri.ipcicontrollerhandler.Hidupgetdriver(perangkat)

}
