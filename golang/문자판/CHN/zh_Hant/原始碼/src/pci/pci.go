/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "連接埠"
import . "中斷"
import . "控制台"
import . "驅動程式/驅動程式"

type Ipci控制器handler interface {
	O時get驅動程式(裝置 TPeripheralcomponentinterconnect裝置descriptor)
}

var ipci控制器handler Ipci控制器handler

type T預設pci控制器handler struct {
}

func (self T預設pci控制器handler) O時get驅動程式(裝置 TPeripheralcomponentinterconnect裝置descriptor) {
}

type TBaseaddress暫存器 struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnect裝置descriptor struct {
	P連接埠base	uint32
	I中斷	uint32

	bus	uint16
	裝置_2	uint16
	函式	uint16

	V廠商識別號	uint16
	D裝置識別號	uint16

	類別識別號		uint8
	subclass識別號	uint8
	介面識別號		uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnect裝置descriptor) Init() {
}

type TPeripheralcomponentinterconnect控制器 struct {
	ipci控制器handler	Ipci控制器handler
	資料連接埠		uint16
	指令連接埠		uint16
}

func (self *TPeripheralcomponentinterconnect控制器) Init(ipci控制器handler Ipci控制器handler) {
	self.資料連接埠 = 0xCFC
	self.指令連接埠 = 0xCF8

	self.ipci控制器handler = T預設pci控制器handler{}
	if ipci控制器handler != nil {
		self.ipci控制器handler = ipci控制器handler
	}
}

var i計數 int = 0

func (self *TPeripheralcomponentinterconnect控制器) R讀取(bus uint16, 裝置_2 uint16, 函式 uint16, registeroffset uint32) uint32 {
	var 識別號 uint32 = 0
	識別號 = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(裝置_2&0x1f) << 11) | (uint32(函式&0x07) << 8) | uint32(registeroffset&0xFC)

	P連接埠寫入dword(self.指令連接埠, 識別號)

	結果1 := P連接埠讀取dword(self.資料連接埠)
	結果2 := (結果1 >> (8 * (registeroffset % 4)))

	return 結果2
}

func (self *TPeripheralcomponentinterconnect控制器) W寫入(bus uint16, 裝置_2 uint16, 函式 uint16, registeroffset uint32, 數值 uint32) {
	var 識別號 uint32
	識別號 = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((裝置_2&0x1f)<<11) | uint32((函式&0x07)<<8) | uint32(registeroffset&0xFC)
	P連接埠寫入dword(self.指令連接埠, 識別號)
	P連接埠寫入dword(self.資料連接埠, 數值)
}
func (self *TPeripheralcomponentinterconnect控制器) D裝置has函式(bus uint16, 裝置_2 uint16) bool {
	結果 := self.R讀取(bus, 裝置_2, 0, 0x0E)
	if (結果 & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var 控制台 T控制台 = T控制台{}

func (self *TPeripheralcomponentinterconnect控制器) S選取驅動程式(驅動程式管理器 *T驅動程式管理器, interrupts *T中斷管理器) {
	for bus := 0; bus < 8; bus++ {
		for 裝置_2 := 0; 裝置_2 < 32; 裝置_2++ {

			var 數字函式 int = 1
			if self.D裝置has函式(uint16(bus), uint16(裝置_2)) == true {
				數字函式 = 8
			} else {
				數字函式 = 1
			}

			for 函式 := 0; 函式 < 數字函式; 函式++ {
				var 裝置 TPeripheralcomponentinterconnect裝置descriptor
				裝置 = self.Get裝置descriptor(uint16(bus), uint16(裝置_2), uint16(函式))
				if 裝置.V廠商識別號 == 0x0000 || 裝置.V廠商識別號 == 0xFFFF {
					continue
				}

				for 列數字 := 0; 列數字 < 6; 列數字++ {
					var 列 TBaseaddress暫存器 = self.Getbaseaddress暫存器(uint16(bus), uint16(裝置_2), uint16(函式), uint16(列數字))
					if 列.address_2 != 0 && (列.regtype == 1) {
						裝置.P連接埠base = 列.address_2
					}

					self.Get驅動程式(裝置, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnect控制器) Get裝置descriptor(bus uint16, 裝置_2 uint16, 函式 uint16) TPeripheralcomponentinterconnect裝置descriptor {
	var 結果 TPeripheralcomponentinterconnect裝置descriptor
	結果 = TPeripheralcomponentinterconnect裝置descriptor{}
	結果.bus = bus
	結果.裝置_2 = 裝置_2
	結果.函式 = 函式

	結果.V廠商識別號 = uint16(self.R讀取(bus, 裝置_2, 函式, 0x00))
	結果.D裝置識別號 = uint16(self.R讀取(bus, 裝置_2, 函式, 0x02))

	結果.類別識別號 = uint8(self.R讀取(bus, 裝置_2, 函式, 0x0b))
	結果.subclass識別號 = uint8(self.R讀取(bus, 裝置_2, 函式, 0x0a))
	結果.介面識別號 = uint8(self.R讀取(bus, 裝置_2, 函式, 0x09))

	結果.revision = uint8(self.R讀取(bus, 裝置_2, 函式, 0x08))
	結果.I中斷 = uint32(self.R讀取(bus, 裝置_2, 函式, 0x3C))

	return 結果
}
func (self *TPeripheralcomponentinterconnect控制器) Getbaseaddress暫存器(bus uint16, 裝置_2 uint16, 函式 uint16, 列 uint16) TBaseaddress暫存器 {
	var 結果 TBaseaddress暫存器

	headertype := self.R讀取(bus, 裝置_2, 函式, 0x0E) & 0x7F
	var 最大bars int = int(6 - (4 * headertype))
	if 列 >= uint16(最大bars) {
		return 結果
	}

	列數值 := self.R讀取(bus, 裝置_2, 函式, uint32(0x10+4*列))

	if (列數值 & 0x1) != 0 {
		結果.regtype = 1
	} else {
		結果.regtype = 0
	}

	if 結果.regtype == 0 {
	} else {
		結果.address_2 = 列數值 & ^uint32(0x3)
		結果.prefetchcapable = false
	}

	return 結果
}
func (self *TPeripheralcomponentinterconnect控制器) Get驅動程式(裝置 TPeripheralcomponentinterconnect裝置descriptor, interrupts *T中斷管理器) {

	self.ipci控制器handler.O時get驅動程式(裝置)

}
