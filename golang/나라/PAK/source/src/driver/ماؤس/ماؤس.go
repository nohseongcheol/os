package کیبورڈ

import . "unsafe"

import . "پورٹ"
import . "مداخلت"
import . "console"

type Iماؤسواقعہhandler interface {
	Oچالوماؤسنیچے(بٹن int8)
	Oچالوماؤساوپر(بٹن int8)
	Oچالوماؤسمنتقلکریں(x int8, y int8)
}

var iماؤسواقعہhandler Iماؤسواقعہhandler

type Tطےشدہماؤسواقعہhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self Tطےشدہماؤسواقعہhandler) Oچالوماؤسنیچے(بٹن int8) {
	buffer := []byte("+")
	console_2.Mچھاپیںxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tطےشدہماؤسواقعہhandler) Oچالوماؤساوپر(بٹن int8)	{}
func (self Tطےشدہماؤسواقعہhandler) Oچالوماؤسمنتقلکریں(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	console_2.Mچھاپیںxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.Mچھاپیںxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

type Tماؤسdriver struct {
	Tمداخلتhandler
}

var فعالماؤسdriver *Tماؤسdriver
var مداخلتhandler func(uint32) uint32

var dataپورٹ_2 uint16 = 0x60
var کمانڈپورٹ_2 uint16 = 0x64

const ps2waitحد = 100000

func waitps2ماداخلخالی() bool {
	for i := 0; i < ps2waitحد; i++ {
		if (Pپورٹپڑھیںbyte(کمانڈپورٹ_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2ماخارجfull() bool {
	for i := 0; i < ps2waitحد; i++ {
		if (Pپورٹپڑھیںbyte(کمانڈپورٹ_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func لکھیںps2کمانڈ(قدر uint8) bool {
	if !waitps2ماداخلخالی() {
		return false
	}
	Pپورٹلکھیںbyte(کمانڈپورٹ_2, قدر)
	return true
}

func لکھیںps2data(قدر uint8) bool {
	if !waitps2ماداخلخالی() {
		return false
	}
	Pپورٹلکھیںbyte(dataپورٹ_2, قدر)
	return true
}

func پڑھیںps2data() (uint8, bool) {
	if !waitps2ماخارجfull() {
		return 0, false
	}
	return Pپورٹپڑھیںbyte(dataپورٹ_2), true
}

func sendماؤسکمانڈ(قدر uint8) bool {
	if !لکھیںps2کمانڈ(0xD4) || !لکھیںps2data(قدر) {
		return false
	}
	ack, ok := پڑھیںps2data()
	return ok && ack == 0xFA
}

func (self *Tماؤسdriver) Initdriver(manager *Tمداخلتmanager, ماؤسواقعہhandler Iماؤسواقعہhandler) {

	iماؤسواقعہhandler = Tطےشدہماؤسواقعہhandler{}

	if ماؤسواقعہhandler != nil {
		iماؤسواقعہhandler = ماؤسواقعہhandler
	}

	فعالماؤسdriver = self
	مداخلتhandler = handleماؤسمداخلت
	var address uintptr
	address = uintptr(Pointer(&مداخلتhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pپورٹپڑھیںbyte(کمانڈپورٹ_2)&0x01) != 0; i++ {
		Pپورٹپڑھیںbyte(dataپورٹ_2)
	}

	if !لکھیںps2کمانڈ(0xA8) || !لکھیںps2کمانڈ(0x20) {
		return
	}
	حالت, ok := پڑھیںps2data()
	if !ok {
		return
	}
	حالت |= 0x02
	حالت &^= 0x20
	if !لکھیںps2کمانڈ(0x60) || !لکھیںps2data(حالت) {
		return
	}

	if !sendماؤسکمانڈ(0xF6) || !sendماؤسکمانڈ(0xF4) {
		return
	}
	offset = 0

}

func handleماؤسمداخلت(esp uint32) uint32 {
	if فعالماؤسdriver == nil {
		Pپورٹپڑھیںbyte(dataپورٹ_2)
		return esp
	}
	return فعالماؤسdriver.Handleمداخلت(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var بٹن_2 int8
var pendingx int16
var pendingy int16
var pendingبٹن int8
var pendingماؤسواقعہ bool

func (self *Tماؤسdriver) Handleمداخلت(esp uint32) uint32 {
	حالت := Pپورٹپڑھیںbyte(کمانڈپورٹ_2)
	if (حالت&0x01) == 0 || (حالت&0x20) == 0 {
		return esp
	}

	data := Pپورٹپڑھیںbyte(dataپورٹ_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetحالت := uint8(buffer_2[0])

		if (packetحالت & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingبٹن = int8(packetحالت & 0x07)
		pendingماؤسواقعہ = true
	}

	return esp

}

func Pعملکاریpendingماؤسevents() {
	if iماؤسواقعہhandler == nil {
		return
	}

	Iمداخلتdeactive()
	if !pendingماؤسواقعہ {
		Iمداخلتفعال()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	نیابٹن := pendingبٹن
	oldبٹن := بٹن_2

	pendingx = 0
	pendingy = 0
	pendingماؤسواقعہ = false
	Iمداخلتفعال()

	if x != 0 || y != 0 {
		iماؤسواقعہhandler.Oچالوماؤسمنتقلکریں(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (نیابٹن & mask) != (oldبٹن & mask) {
			if (نیابٹن & mask) != 0 {
				iماؤسواقعہhandler.Oچالوماؤسنیچے(int8(i + 1))
			} else {
				iماؤسواقعہhandler.Oچالوماؤساوپر(int8(i + 1))
			}
		}
	}
	بٹن_2 = نیابٹن
}
