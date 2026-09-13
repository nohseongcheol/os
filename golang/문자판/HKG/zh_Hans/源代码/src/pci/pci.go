package pci

import . "端口"
import . "中断"
import . "控制台"
import . "驱动程序/驱动程序"

type Ipci控制器handler interface {
	O时get驱动程序(设备 TPeripheralcomponentinterconnect设备descriptor)
}

var ipci控制器handler Ipci控制器handler

type T默认pci控制器handler struct {
}

func (self T默认pci控制器handler) O时get驱动程序(设备 TPeripheralcomponentinterconnect设备descriptor) {
}

type TBaseaddress寄存器 struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnect设备descriptor struct {
	P端口base	uint32
	I中断		uint32

	bus	uint16
	设备_2	uint16
	函数	uint16

	V发行商id	uint16
	D设备id	uint16

	类id		uint8
	subclassid	uint8
	接口id		uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnect设备descriptor) Init() {
}

type TPeripheralcomponentinterconnect控制器 struct {
	ipci控制器handler	Ipci控制器handler
	数据端口		uint16
	命令端口		uint16
}

func (self *TPeripheralcomponentinterconnect控制器) Init(ipci控制器handler Ipci控制器handler) {
	self.数据端口 = 0xCFC
	self.命令端口 = 0xCF8

	self.ipci控制器handler = T默认pci控制器handler{}
	if ipci控制器handler != nil {
		self.ipci控制器handler = ipci控制器handler
	}
}

var i计数 int = 0

func (self *TPeripheralcomponentinterconnect控制器) R读取(bus uint16, 设备_2 uint16, 函数 uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(设备_2&0x1f) << 11) | (uint32(函数&0x07) << 8) | uint32(registeroffset&0xFC)

	P端口写入dword(self.命令端口, id)

	结果1 := P端口读取dword(self.数据端口)
	结果2 := (结果1 >> (8 * (registeroffset % 4)))

	return 结果2
}

func (self *TPeripheralcomponentinterconnect控制器) W写入(bus uint16, 设备_2 uint16, 函数 uint16, registeroffset uint32, 值 uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((设备_2&0x1f)<<11) | uint32((函数&0x07)<<8) | uint32(registeroffset&0xFC)
	P端口写入dword(self.命令端口, id)
	P端口写入dword(self.数据端口, 值)
}
func (self *TPeripheralcomponentinterconnect控制器) D设备哈斯区函数(bus uint16, 设备_2 uint16) bool {
	结果 := self.R读取(bus, 设备_2, 0, 0x0E)
	if (结果 & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var 控制台 T控制台 = T控制台{}

func (self *TPeripheralcomponentinterconnect控制器) S选择驱动程序(驱动程序管理器 *T驱动程序管理器, interrupts *T中断管理器) {
	for bus := 0; bus < 8; bus++ {
		for 设备_2 := 0; 设备_2 < 32; 设备_2++ {

			var 数字函数 int = 1
			if self.D设备哈斯区函数(uint16(bus), uint16(设备_2)) == true {
				数字函数 = 8
			} else {
				数字函数 = 1
			}

			for 函数 := 0; 函数 < 数字函数; 函数++ {
				var 设备 TPeripheralcomponentinterconnect设备descriptor
				设备 = self.Get设备descriptor(uint16(bus), uint16(设备_2), uint16(函数))
				if 设备.V发行商id == 0x0000 || 设备.V发行商id == 0xFFFF {
					continue
				}

				for 巴尔数字 := 0; 巴尔数字 < 6; 巴尔数字++ {
					var 巴尔 TBaseaddress寄存器 = self.Getbaseaddress寄存器(uint16(bus), uint16(设备_2), uint16(函数), uint16(巴尔数字))
					if 巴尔.address_2 != 0 && (巴尔.regtype == 1) {
						设备.P端口base = 巴尔.address_2
					}

					self.Get驱动程序(设备, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnect控制器) Get设备descriptor(bus uint16, 设备_2 uint16, 函数 uint16) TPeripheralcomponentinterconnect设备descriptor {
	var 结果 TPeripheralcomponentinterconnect设备descriptor
	结果 = TPeripheralcomponentinterconnect设备descriptor{}
	结果.bus = bus
	结果.设备_2 = 设备_2
	结果.函数 = 函数

	结果.V发行商id = uint16(self.R读取(bus, 设备_2, 函数, 0x00))
	结果.D设备id = uint16(self.R读取(bus, 设备_2, 函数, 0x02))

	结果.类id = uint8(self.R读取(bus, 设备_2, 函数, 0x0b))
	结果.subclassid = uint8(self.R读取(bus, 设备_2, 函数, 0x0a))
	结果.接口id = uint8(self.R读取(bus, 设备_2, 函数, 0x09))

	结果.revision = uint8(self.R读取(bus, 设备_2, 函数, 0x08))
	结果.I中断 = uint32(self.R读取(bus, 设备_2, 函数, 0x3C))

	return 结果
}
func (self *TPeripheralcomponentinterconnect控制器) Getbaseaddress寄存器(bus uint16, 设备_2 uint16, 函数 uint16, 巴尔 uint16) TBaseaddress寄存器 {
	var 结果 TBaseaddress寄存器

	headertype := self.R读取(bus, 设备_2, 函数, 0x0E) & 0x7F
	var 最大值bars int = int(6 - (4 * headertype))
	if 巴尔 >= uint16(最大值bars) {
		return 结果
	}

	巴尔值 := self.R读取(bus, 设备_2, 函数, uint32(0x10+4*巴尔))

	if (巴尔值 & 0x1) != 0 {
		结果.regtype = 1
	} else {
		结果.regtype = 0
	}

	if 结果.regtype == 0 {
	} else {
		结果.address_2 = 巴尔值 & ^uint32(0x3)
		结果.prefetchcapable = false
	}

	return 结果
}
func (self *TPeripheralcomponentinterconnect控制器) Get驱动程序(设备 TPeripheralcomponentinterconnect设备descriptor, interrupts *T中断管理器) {

	self.ipci控制器handler.O时get驱动程序(设备)

}
