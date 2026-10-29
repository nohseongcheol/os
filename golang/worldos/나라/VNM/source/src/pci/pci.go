/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "cổng"
import . "giánđoạn"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Bậtgetdriver(thiếtbị TPeripheralcomponentinterconnectThiếtbịdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TMặcđịnhpcicontrollerhandler struct {
}

func (mình TMặcđịnhpcicontrollerhandler) Bậtgetdriver(thiếtbị TPeripheralcomponentinterconnectThiếtbịdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectThiếtbịdescriptor struct {
	Cổngbase	uint32
	Giánđoạn	uint32

	bus		uint16
	thiếtbị_2	uint16
	hàm		uint16

	NhàsảnxuấtMãsố	uint16
	ThiếtbịMãsố	uint16

	hạngMãsố	uint8
	subclassMãsố	uint8
	gIAODIỆNMãsố	uint8

	revision	uint8
}

func (mình *TPeripheralcomponentinterconnectThiếtbịdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataCổng		uint16
	lệnhCổng		uint16
}

func (mình *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	mình.dataCổng = 0xCFC
	mình.lệnhCổng = 0xCF8

	mình.ipcicontrollerhandler = TMặcđịnhpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		mình.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var iSốlượng int = 0

func (mình *TPeripheralcomponentinterconnectcontroller) Đọc(bus uint16, thiếtbị_2 uint16, hàm uint16, registeroffset uint32) uint32 {
	var mãsố uint32 = 0
	mãsố = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(thiếtbị_2&0x1f) << 11) | (uint32(hàm&0x07) << 8) | uint32(registeroffset&0xFC)

	CổngGhidword(mình.lệnhCổng, mãsố)

	result1 := CổngĐọcdword(mình.dataCổng)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (mình *TPeripheralcomponentinterconnectcontroller) Ghi(bus uint16, thiếtbị_2 uint16, hàm uint16, registeroffset uint32, giátrị uint32) {
	var mãsố uint32
	mãsố = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((thiếtbị_2&0x1f)<<11) | uint32((hàm&0x07)<<8) | uint32(registeroffset&0xFC)
	CổngGhidword(mình.lệnhCổng, mãsố)
	CổngGhidword(mình.dataCổng, giátrị)
}
func (mình *TPeripheralcomponentinterconnectcontroller) ThiếtbịhasHàm(bus uint16, thiếtbị_2 uint16) bool {
	result := mình.Đọc(bus, thiếtbị_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (mình *TPeripheralcomponentinterconnectcontroller) Chọndriver(drivermanager *TDrivermanager, interrupts *TGiánđoạnmanager) {
	for bus := 0; bus < 8; bus++ {
		for thiếtbị_2 := 0; thiếtbị_2 < 32; thiếtbị_2++ {

			var sỐHàm int = 1
			if mình.ThiếtbịhasHàm(uint16(bus), uint16(thiếtbị_2)) == true {
				sỐHàm = 8
			} else {
				sỐHàm = 1
			}

			for hàm := 0; hàm < sỐHàm; hàm++ {
				var thiếtbị TPeripheralcomponentinterconnectThiếtbịdescriptor
				thiếtbị = mình.GetThiếtbịdescriptor(uint16(bus), uint16(thiếtbị_2), uint16(hàm))
				if thiếtbị.NhàsảnxuấtMãsố == 0x0000 || thiếtbị.NhàsảnxuấtMãsố == 0xFFFF {
					continue
				}

				for thanhSỐ := 0; thanhSỐ < 6; thanhSỐ++ {
					var thanh TBaseaddressregister = mình.Getbaseaddressregister(uint16(bus), uint16(thiếtbị_2), uint16(hàm), uint16(thanhSỐ))
					if thanh.address_2 != 0 && (thanh.regtype == 1) {
						thiếtbị.Cổngbase = thanh.address_2
					}

					mình.Getdriver(thiếtbị, interrupts)

				}

			}

		}
	}
}
func (mình *TPeripheralcomponentinterconnectcontroller) GetThiếtbịdescriptor(bus uint16, thiếtbị_2 uint16, hàm uint16) TPeripheralcomponentinterconnectThiếtbịdescriptor {
	var result TPeripheralcomponentinterconnectThiếtbịdescriptor
	result = TPeripheralcomponentinterconnectThiếtbịdescriptor{}
	result.bus = bus
	result.thiếtbị_2 = thiếtbị_2
	result.hàm = hàm

	result.NhàsảnxuấtMãsố = uint16(mình.Đọc(bus, thiếtbị_2, hàm, 0x00))
	result.ThiếtbịMãsố = uint16(mình.Đọc(bus, thiếtbị_2, hàm, 0x02))

	result.hạngMãsố = uint8(mình.Đọc(bus, thiếtbị_2, hàm, 0x0b))
	result.subclassMãsố = uint8(mình.Đọc(bus, thiếtbị_2, hàm, 0x0a))
	result.gIAODIỆNMãsố = uint8(mình.Đọc(bus, thiếtbị_2, hàm, 0x09))

	result.revision = uint8(mình.Đọc(bus, thiếtbị_2, hàm, 0x08))
	result.Giánđoạn = uint32(mình.Đọc(bus, thiếtbị_2, hàm, 0x3C))

	return result
}
func (mình *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, thiếtbị_2 uint16, hàm uint16, thanh uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := mình.Đọc(bus, thiếtbị_2, hàm, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if thanh >= uint16(maxbars) {
		return result
	}

	thanhGiátrị := mình.Đọc(bus, thiếtbị_2, hàm, uint32(0x10+4*thanh))

	if (thanhGiátrị & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = thanhGiátrị & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (mình *TPeripheralcomponentinterconnectcontroller) Getdriver(thiếtbị TPeripheralcomponentinterconnectThiếtbịdescriptor, interrupts *TGiánđoạnmanager) {

	mình.ipcicontrollerhandler.Bậtgetdriver(thiếtbị)

}
