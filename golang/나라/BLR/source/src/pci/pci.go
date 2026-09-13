package pci

import . "порт"
import . "перарыванне"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(прылада TPeripheralcomponentinterconnectПрыладаdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TСтандартнаpcicontrollerhandler struct {
}

func (self TСтандартнаpcicontrollerhandler) Ongetdriver(прылада TPeripheralcomponentinterconnectПрыладаdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectПрыладаdescriptor struct {
	Портbase	uint32
	Перарыванне	uint32

	bus		uint16
	прылада_2	uint16
	функцыя		uint16

	ВытворцаІДЭНТЫФІКАТАР	uint16
	ПрыладаІДЭНТЫФІКАТАР	uint16

	класІДЭНТЫФІКАТАР	uint8
	subclassІДЭНТЫФІКАТАР	uint8
	іНТЭРФЭЙСІДЭНТЫФІКАТАР	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectПрыладаdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	загадПорт		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataПорт = 0xCFC
	self.загадПорт = 0xCF8

	self.ipcicontrollerhandler = TСтандартнаpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Чытанне(bus uint16, прылада_2 uint16, функцыя uint16, registeroffset uint32) uint32 {
	var іДЭНТЫФІКАТАР uint32 = 0
	іДЭНТЫФІКАТАР = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(прылада_2&0x1f) << 11) | (uint32(функцыя&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортЗапісdword(self.загадПорт, іДЭНТЫФІКАТАР)

	result1 := ПортЧытаннеdword(self.dataПорт)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Запіс(bus uint16, прылада_2 uint16, функцыя uint16, registeroffset uint32, значэнне uint32) {
	var іДЭНТЫФІКАТАР uint32
	іДЭНТЫФІКАТАР = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((прылада_2&0x1f)<<11) | uint32((функцыя&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортЗапісdword(self.загадПорт, іДЭНТЫФІКАТАР)
	ПортЗапісdword(self.dataПорт, значэнне)
}
func (self *TPeripheralcomponentinterconnectcontroller) ПрыладаХасФункцыі(bus uint16, прылада_2 uint16) bool {
	result := self.Чытанне(bus, прылада_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Вылучыцьdriver(drivermanager *TDrivermanager, interrupts *TПерарываннеmanager) {
	for bus := 0; bus < 8; bus++ {
		for прылада_2 := 0; прылада_2 < 32; прылада_2++ {

			var нУМАРФункцыі int = 1
			if self.ПрыладаХасФункцыі(uint16(bus), uint16(прылада_2)) == true {
				нУМАРФункцыі = 8
			} else {
				нУМАРФункцыі = 1
			}

			for функцыя := 0; функцыя < нУМАРФункцыі; функцыя++ {
				var прылада TPeripheralcomponentinterconnectПрыладаdescriptor
				прылада = self.GetПрыладаdescriptor(uint16(bus), uint16(прылада_2), uint16(функцыя))
				if прылада.ВытворцаІДЭНТЫФІКАТАР == 0x0000 || прылада.ВытворцаІДЭНТЫФІКАТАР == 0xFFFF {
					continue
				}

				for барНУМАР := 0; барНУМАР < 6; барНУМАР++ {
					var бар TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(прылада_2), uint16(функцыя), uint16(барНУМАР))
					if бар.address_2 != 0 && (бар.regtype == 1) {
						прылада.Портbase = бар.address_2
					}

					self.Getdriver(прылада, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetПрыладаdescriptor(bus uint16, прылада_2 uint16, функцыя uint16) TPeripheralcomponentinterconnectПрыладаdescriptor {
	var result TPeripheralcomponentinterconnectПрыладаdescriptor
	result = TPeripheralcomponentinterconnectПрыладаdescriptor{}
	result.bus = bus
	result.прылада_2 = прылада_2
	result.функцыя = функцыя

	result.ВытворцаІДЭНТЫФІКАТАР = uint16(self.Чытанне(bus, прылада_2, функцыя, 0x00))
	result.ПрыладаІДЭНТЫФІКАТАР = uint16(self.Чытанне(bus, прылада_2, функцыя, 0x02))

	result.класІДЭНТЫФІКАТАР = uint8(self.Чытанне(bus, прылада_2, функцыя, 0x0b))
	result.subclassІДЭНТЫФІКАТАР = uint8(self.Чытанне(bus, прылада_2, функцыя, 0x0a))
	result.іНТЭРФЭЙСІДЭНТЫФІКАТАР = uint8(self.Чытанне(bus, прылада_2, функцыя, 0x09))

	result.revision = uint8(self.Чытанне(bus, прылада_2, функцыя, 0x08))
	result.Перарыванне = uint32(self.Чытанне(bus, прылада_2, функцыя, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, прылада_2 uint16, функцыя uint16, бар uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Чытанне(bus, прылада_2, функцыя, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if бар >= uint16(maxbars) {
		return result
	}

	барЗначэнне := self.Чытанне(bus, прылада_2, функцыя, uint32(0x10+4*бар))

	if (барЗначэнне & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = барЗначэнне & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(прылада TPeripheralcomponentinterconnectПрыладаdescriptor, interrupts *TПерарываннеmanager) {

	self.ipcicontrollerhandler.Ongetdriver(прылада)

}
