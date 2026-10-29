/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "ぽーと"
import . "わりこみ"
import . "こんそーる"
import . "どらいばー/どらいばー"

type Ipciせいぎょきhandler interface {
	Oときgetどらいばー(でばいす TPeripheralcomponentinterconnectでばいすdescriptor)
}

var ipciせいぎょきhandler Ipciせいぎょきhandler

type Tでふぉるとpciせいぎょきhandler struct {
}

func (self Tでふぉるとpciせいぎょきhandler) Oときgetどらいばー(でばいす TPeripheralcomponentinterconnectでばいすdescriptor) {
}

type TBaseaddressれじすた struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectでばいすdescriptor struct {
	Pぽーとbase	uint32
	Iわりこみ		uint32

	bus	uint16
	でばいす_2	uint16
	かんすう	uint16

	Vせいぞうもとid	uint16
	Dでばいすid	uint16

	くらすid		uint8
	subclassid	uint8
	いんたーふぇーすid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectでばいすdescriptor) Init() {
}

type TPeripheralcomponentinterconnectせいぎょき struct {
	ipciせいぎょきhandler	Ipciせいぎょきhandler
	でーたぽーと		uint16
	こまんどぽーと		uint16
}

func (self *TPeripheralcomponentinterconnectせいぎょき) Init(ipciせいぎょきhandler Ipciせいぎょきhandler) {
	self.でーたぽーと = 0xCFC
	self.こまんどぽーと = 0xCF8

	self.ipciせいぎょきhandler = Tでふぉるとpciせいぎょきhandler{}
	if ipciせいぎょきhandler != nil {
		self.ipciせいぎょきhandler = ipciせいぎょきhandler
	}
}

var iかうんと int = 0

func (self *TPeripheralcomponentinterconnectせいぎょき) Rよみこみ(bus uint16, でばいす_2 uint16, かんすう uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(でばいす_2&0x1f) << 11) | (uint32(かんすう&0x07) << 8) | uint32(registeroffset&0xFC)

	Pぽーとかきこみdword(self.こまんどぽーと, id)

	せいせいさき1 := Pぽーとよみこみdword(self.でーたぽーと)
	せいせいさき2 := (せいせいさき1 >> (8 * (registeroffset % 4)))

	return せいせいさき2
}

func (self *TPeripheralcomponentinterconnectせいぎょき) Wかきこみ(bus uint16, でばいす_2 uint16, かんすう uint16, registeroffset uint32, あたい uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((でばいす_2&0x1f)<<11) | uint32((かんすう&0x07)<<8) | uint32(registeroffset&0xFC)
	Pぽーとかきこみdword(self.こまんどぽーと, id)
	Pぽーとかきこみdword(self.でーたぽーと, あたい)
}
func (self *TPeripheralcomponentinterconnectせいぎょき) Dでばいすhasかんすう(bus uint16, でばいす_2 uint16) bool {
	せいせいさき := self.Rよみこみ(bus, でばいす_2, 0, 0x0E)
	if (せいせいさき & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var こんそーる Tこんそーる = Tこんそーる{}

func (self *TPeripheralcomponentinterconnectせいぎょき) Sせんたくどらいばー(どらいばーかんりしゃ *Tどらいばーかんりしゃ, interrupts *Tわりこみかんりしゃ) {
	for bus := 0; bus < 8; bus++ {
		for でばいす_2 := 0; でばいす_2 < 32; でばいす_2++ {

			var numberかんすう int = 1
			if self.Dでばいすhasかんすう(uint16(bus), uint16(でばいす_2)) == true {
				numberかんすう = 8
			} else {
				numberかんすう = 1
			}

			for かんすう := 0; かんすう < numberかんすう; かんすう++ {
				var でばいす TPeripheralcomponentinterconnectでばいすdescriptor
				でばいす = self.Getでばいすdescriptor(uint16(bus), uint16(でばいす_2), uint16(かんすう))
				if でばいす.Vせいぞうもとid == 0x0000 || でばいす.Vせいぞうもとid == 0xFFFF {
					continue
				}

				for ばーnumber := 0; ばーnumber < 6; ばーnumber++ {
					var ばー TBaseaddressれじすた = self.Getbaseaddressれじすた(uint16(bus), uint16(でばいす_2), uint16(かんすう), uint16(ばーnumber))
					if ばー.address_2 != 0 && (ばー.regtype == 1) {
						でばいす.Pぽーとbase = ばー.address_2
					}

					self.Getどらいばー(でばいす, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectせいぎょき) Getでばいすdescriptor(bus uint16, でばいす_2 uint16, かんすう uint16) TPeripheralcomponentinterconnectでばいすdescriptor {
	var せいせいさき TPeripheralcomponentinterconnectでばいすdescriptor
	せいせいさき = TPeripheralcomponentinterconnectでばいすdescriptor{}
	せいせいさき.bus = bus
	せいせいさき.でばいす_2 = でばいす_2
	せいせいさき.かんすう = かんすう

	せいせいさき.Vせいぞうもとid = uint16(self.Rよみこみ(bus, でばいす_2, かんすう, 0x00))
	せいせいさき.Dでばいすid = uint16(self.Rよみこみ(bus, でばいす_2, かんすう, 0x02))

	せいせいさき.くらすid = uint8(self.Rよみこみ(bus, でばいす_2, かんすう, 0x0b))
	せいせいさき.subclassid = uint8(self.Rよみこみ(bus, でばいす_2, かんすう, 0x0a))
	せいせいさき.いんたーふぇーすid = uint8(self.Rよみこみ(bus, でばいす_2, かんすう, 0x09))

	せいせいさき.revision = uint8(self.Rよみこみ(bus, でばいす_2, かんすう, 0x08))
	せいせいさき.Iわりこみ = uint32(self.Rよみこみ(bus, でばいす_2, かんすう, 0x3C))

	return せいせいさき
}
func (self *TPeripheralcomponentinterconnectせいぎょき) Getbaseaddressれじすた(bus uint16, でばいす_2 uint16, かんすう uint16, ばー uint16) TBaseaddressれじすた {
	var せいせいさき TBaseaddressれじすた

	headertype := self.Rよみこみ(bus, でばいす_2, かんすう, 0x0E) & 0x7F
	var さいだいbars int = int(6 - (4 * headertype))
	if ばー >= uint16(さいだいbars) {
		return せいせいさき
	}

	ばーあたい := self.Rよみこみ(bus, でばいす_2, かんすう, uint32(0x10+4*ばー))

	if (ばーあたい & 0x1) != 0 {
		せいせいさき.regtype = 1
	} else {
		せいせいさき.regtype = 0
	}

	if せいせいさき.regtype == 0 {
	} else {
		せいせいさき.address_2 = ばーあたい & ^uint32(0x3)
		せいせいさき.prefetchcapable = false
	}

	return せいせいさき
}
func (self *TPeripheralcomponentinterconnectせいぎょき) Getどらいばー(でばいす TPeripheralcomponentinterconnectでばいすdescriptor, interrupts *Tわりこみかんりしゃ) {

	self.ipciせいぎょきhandler.Oときgetどらいばー(でばいす)

}
