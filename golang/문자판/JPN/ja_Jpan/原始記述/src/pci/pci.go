/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "ポート"
import . "割込み"
import . "コンソール"
import . "ドライバー/ドライバー"

type Ipci制御器handler interface {
	O時getドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor)
}

var ipci制御器handler Ipci制御器handler

type Tデフォルトpci制御器handler struct {
}

func (self Tデフォルトpci制御器handler) O時getドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor) {
}

type TBaseaddressレジスタ struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectデバイスdescriptor struct {
	Pポートbase	uint32
	I割込み		uint32

	bus	uint16
	デバイス_2	uint16
	関数	uint16

	V製造元id	uint16
	Dデバイスid	uint16

	クラスid		uint8
	subclassid	uint8
	インターフェースid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectデバイスdescriptor) Init() {
}

type TPeripheralcomponentinterconnect制御器 struct {
	ipci制御器handler	Ipci制御器handler
	データポート		uint16
	コマンドポート		uint16
}

func (self *TPeripheralcomponentinterconnect制御器) Init(ipci制御器handler Ipci制御器handler) {
	self.データポート = 0xCFC
	self.コマンドポート = 0xCF8

	self.ipci制御器handler = Tデフォルトpci制御器handler{}
	if ipci制御器handler != nil {
		self.ipci制御器handler = ipci制御器handler
	}
}

var iカウント int = 0

func (self *TPeripheralcomponentinterconnect制御器) R読込み(bus uint16, デバイス_2 uint16, 関数 uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(デバイス_2&0x1f) << 11) | (uint32(関数&0x07) << 8) | uint32(registeroffset&0xFC)

	Pポート書込みdword(self.コマンドポート, id)

	生成先1 := Pポート読込みdword(self.データポート)
	生成先2 := (生成先1 >> (8 * (registeroffset % 4)))

	return 生成先2
}

func (self *TPeripheralcomponentinterconnect制御器) W書込み(bus uint16, デバイス_2 uint16, 関数 uint16, registeroffset uint32, 値 uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((デバイス_2&0x1f)<<11) | uint32((関数&0x07)<<8) | uint32(registeroffset&0xFC)
	Pポート書込みdword(self.コマンドポート, id)
	Pポート書込みdword(self.データポート, 値)
}
func (self *TPeripheralcomponentinterconnect制御器) Dデバイスhas関数(bus uint16, デバイス_2 uint16) bool {
	生成先 := self.R読込み(bus, デバイス_2, 0, 0x0E)
	if (生成先 & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var コンソール Tコンソール = Tコンソール{}

func (self *TPeripheralcomponentinterconnect制御器) S選択ドライバー(ドライバー管理者 *Tドライバー管理者, interrupts *T割込み管理者) {
	for bus := 0; bus < 8; bus++ {
		for デバイス_2 := 0; デバイス_2 < 32; デバイス_2++ {

			var number関数 int = 1
			if self.Dデバイスhas関数(uint16(bus), uint16(デバイス_2)) == true {
				number関数 = 8
			} else {
				number関数 = 1
			}

			for 関数 := 0; 関数 < number関数; 関数++ {
				var デバイス TPeripheralcomponentinterconnectデバイスdescriptor
				デバイス = self.Getデバイスdescriptor(uint16(bus), uint16(デバイス_2), uint16(関数))
				if デバイス.V製造元id == 0x0000 || デバイス.V製造元id == 0xFFFF {
					continue
				}

				for バーnumber := 0; バーnumber < 6; バーnumber++ {
					var バー TBaseaddressレジスタ = self.Getbaseaddressレジスタ(uint16(bus), uint16(デバイス_2), uint16(関数), uint16(バーnumber))
					if バー.address_2 != 0 && (バー.regtype == 1) {
						デバイス.Pポートbase = バー.address_2
					}

					self.Getドライバー(デバイス, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnect制御器) Getデバイスdescriptor(bus uint16, デバイス_2 uint16, 関数 uint16) TPeripheralcomponentinterconnectデバイスdescriptor {
	var 生成先 TPeripheralcomponentinterconnectデバイスdescriptor
	生成先 = TPeripheralcomponentinterconnectデバイスdescriptor{}
	生成先.bus = bus
	生成先.デバイス_2 = デバイス_2
	生成先.関数 = 関数

	生成先.V製造元id = uint16(self.R読込み(bus, デバイス_2, 関数, 0x00))
	生成先.Dデバイスid = uint16(self.R読込み(bus, デバイス_2, 関数, 0x02))

	生成先.クラスid = uint8(self.R読込み(bus, デバイス_2, 関数, 0x0b))
	生成先.subclassid = uint8(self.R読込み(bus, デバイス_2, 関数, 0x0a))
	生成先.インターフェースid = uint8(self.R読込み(bus, デバイス_2, 関数, 0x09))

	生成先.revision = uint8(self.R読込み(bus, デバイス_2, 関数, 0x08))
	生成先.I割込み = uint32(self.R読込み(bus, デバイス_2, 関数, 0x3C))

	return 生成先
}
func (self *TPeripheralcomponentinterconnect制御器) Getbaseaddressレジスタ(bus uint16, デバイス_2 uint16, 関数 uint16, バー uint16) TBaseaddressレジスタ {
	var 生成先 TBaseaddressレジスタ

	headertype := self.R読込み(bus, デバイス_2, 関数, 0x0E) & 0x7F
	var 最大bars int = int(6 - (4 * headertype))
	if バー >= uint16(最大bars) {
		return 生成先
	}

	バー値 := self.R読込み(bus, デバイス_2, 関数, uint32(0x10+4*バー))

	if (バー値 & 0x1) != 0 {
		生成先.regtype = 1
	} else {
		生成先.regtype = 0
	}

	if 生成先.regtype == 0 {
	} else {
		生成先.address_2 = バー値 & ^uint32(0x3)
		生成先.prefetchcapable = false
	}

	return 生成先
}
func (self *TPeripheralcomponentinterconnect制御器) Getドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor, interrupts *T割込み管理者) {

	self.ipci制御器handler.O時getドライバー(デバイス)

}
