/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "ポート"
import . "ワリコミ"
import . "コンソール"
import . "ドライバー/ドライバー"

type Ipciセイギョキhandler interface {
	Oトキgetドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor)
}

var ipciセイギョキhandler Ipciセイギョキhandler

type Tデフォルトpciセイギョキhandler struct {
}

func (self Tデフォルトpciセイギョキhandler) Oトキgetドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor) {
}

type TBaseaddressレジスタ struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectデバイスdescriptor struct {
	Pポートbase	uint32
	Iワリコミ		uint32

	bus	uint16
	デバイス_2	uint16
	カンスウ	uint16

	Vセイゾウモトid	uint16
	Dデバイスid	uint16

	クラスid		uint8
	subclassid	uint8
	インターフェースid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectデバイスdescriptor) Init() {
}

type TPeripheralcomponentinterconnectセイギョキ struct {
	ipciセイギョキhandler	Ipciセイギョキhandler
	データポート		uint16
	コマンドポート		uint16
}

func (self *TPeripheralcomponentinterconnectセイギョキ) Init(ipciセイギョキhandler Ipciセイギョキhandler) {
	self.データポート = 0xCFC
	self.コマンドポート = 0xCF8

	self.ipciセイギョキhandler = Tデフォルトpciセイギョキhandler{}
	if ipciセイギョキhandler != nil {
		self.ipciセイギョキhandler = ipciセイギョキhandler
	}
}

var iカウント int = 0

func (self *TPeripheralcomponentinterconnectセイギョキ) Rヨミコミ(bus uint16, デバイス_2 uint16, カンスウ uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(デバイス_2&0x1f) << 11) | (uint32(カンスウ&0x07) << 8) | uint32(registeroffset&0xFC)

	Pポートカキコミdword(self.コマンドポート, id)

	セイセイサキ1 := Pポートヨミコミdword(self.データポート)
	セイセイサキ2 := (セイセイサキ1 >> (8 * (registeroffset % 4)))

	return セイセイサキ2
}

func (self *TPeripheralcomponentinterconnectセイギョキ) Wカキコミ(bus uint16, デバイス_2 uint16, カンスウ uint16, registeroffset uint32, アタイ uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((デバイス_2&0x1f)<<11) | uint32((カンスウ&0x07)<<8) | uint32(registeroffset&0xFC)
	Pポートカキコミdword(self.コマンドポート, id)
	Pポートカキコミdword(self.データポート, アタイ)
}
func (self *TPeripheralcomponentinterconnectセイギョキ) Dデバイスhasカンスウ(bus uint16, デバイス_2 uint16) bool {
	セイセイサキ := self.Rヨミコミ(bus, デバイス_2, 0, 0x0E)
	if (セイセイサキ & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var コンソール Tコンソール = Tコンソール{}

func (self *TPeripheralcomponentinterconnectセイギョキ) Sセンタクドライバー(ドライバーカンリシャ *Tドライバーカンリシャ, interrupts *Tワリコミカンリシャ) {
	for bus := 0; bus < 8; bus++ {
		for デバイス_2 := 0; デバイス_2 < 32; デバイス_2++ {

			var numberカンスウ int = 1
			if self.Dデバイスhasカンスウ(uint16(bus), uint16(デバイス_2)) == true {
				numberカンスウ = 8
			} else {
				numberカンスウ = 1
			}

			for カンスウ := 0; カンスウ < numberカンスウ; カンスウ++ {
				var デバイス TPeripheralcomponentinterconnectデバイスdescriptor
				デバイス = self.Getデバイスdescriptor(uint16(bus), uint16(デバイス_2), uint16(カンスウ))
				if デバイス.Vセイゾウモトid == 0x0000 || デバイス.Vセイゾウモトid == 0xFFFF {
					continue
				}

				for バーnumber := 0; バーnumber < 6; バーnumber++ {
					var バー TBaseaddressレジスタ = self.Getbaseaddressレジスタ(uint16(bus), uint16(デバイス_2), uint16(カンスウ), uint16(バーnumber))
					if バー.address_2 != 0 && (バー.regtype == 1) {
						デバイス.Pポートbase = バー.address_2
					}

					self.Getドライバー(デバイス, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectセイギョキ) Getデバイスdescriptor(bus uint16, デバイス_2 uint16, カンスウ uint16) TPeripheralcomponentinterconnectデバイスdescriptor {
	var セイセイサキ TPeripheralcomponentinterconnectデバイスdescriptor
	セイセイサキ = TPeripheralcomponentinterconnectデバイスdescriptor{}
	セイセイサキ.bus = bus
	セイセイサキ.デバイス_2 = デバイス_2
	セイセイサキ.カンスウ = カンスウ

	セイセイサキ.Vセイゾウモトid = uint16(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x00))
	セイセイサキ.Dデバイスid = uint16(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x02))

	セイセイサキ.クラスid = uint8(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x0b))
	セイセイサキ.subclassid = uint8(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x0a))
	セイセイサキ.インターフェースid = uint8(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x09))

	セイセイサキ.revision = uint8(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x08))
	セイセイサキ.Iワリコミ = uint32(self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x3C))

	return セイセイサキ
}
func (self *TPeripheralcomponentinterconnectセイギョキ) Getbaseaddressレジスタ(bus uint16, デバイス_2 uint16, カンスウ uint16, バー uint16) TBaseaddressレジスタ {
	var セイセイサキ TBaseaddressレジスタ

	headertype := self.Rヨミコミ(bus, デバイス_2, カンスウ, 0x0E) & 0x7F
	var サイダイbars int = int(6 - (4 * headertype))
	if バー >= uint16(サイダイbars) {
		return セイセイサキ
	}

	バーアタイ := self.Rヨミコミ(bus, デバイス_2, カンスウ, uint32(0x10+4*バー))

	if (バーアタイ & 0x1) != 0 {
		セイセイサキ.regtype = 1
	} else {
		セイセイサキ.regtype = 0
	}

	if セイセイサキ.regtype == 0 {
	} else {
		セイセイサキ.address_2 = バーアタイ & ^uint32(0x3)
		セイセイサキ.prefetchcapable = false
	}

	return セイセイサキ
}
func (self *TPeripheralcomponentinterconnectセイギョキ) Getドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor, interrupts *Tワリコミカンリシャ) {

	self.ipciセイギョキhandler.Oトキgetドライバー(デバイス)

}
