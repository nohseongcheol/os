/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package የፊደልሠሌዳ

import . "unsafe"

import . "port"
import . "ማቋረጫ"
import . "console"

type Iአይጥeventhandler interface {
	Oማብሪያአይጥወደታች(button int8)
	Oማብሪያአይጥወደላይ(button int8)
	Oማብሪያአይጥመንቀሳቅስ(x int8, y int8)
}

var iአይጥeventhandler Iአይጥeventhandler

type Tነባርአይጥeventhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xአካባቢ int16 = 0
var yአካባቢ int16 = 0

func (self Tነባርአይጥeventhandler) Oማብሪያአይጥወደታች(button int8) {
	buffer := []byte("+")
	console_2.Mማተሚያxy(buffer, uint16(previousx), uint16(previousy))
}
func (self Tነባርአይጥeventhandler) Oማብሪያአይጥወደላይ(button int8)	{}
func (self Tነባርአይጥeventhandler) Oማብሪያአይጥመንቀሳቅስ(x int8, y int8) {

	xአካባቢ += int16(x)
	if xአካባቢ < 0 {
		xአካባቢ = 0
	}
	if xአካባቢ >= 80 {
		xአካባቢ = 79
	}

	yአካባቢ -= int16(y)

	if yአካባቢ < 0 {
		yአካባቢ = 0
	}
	if yአካባቢ >= 25 {
		yአካባቢ = 24
	}

	buffer := []byte(" ")
	console_2.Mማተሚያxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.Mማተሚያxy(buffer, uint16(xአካባቢ), uint16(yአካባቢ))

	previousx = xአካባቢ
	previousy = yአካባቢ
}

type Tአይጥdriver struct {
	Tማቋረጫhandler
}

var አሰራአይጥdriver *Tአይጥdriver
var ማቋረጫhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var ትእዛዝport_2 uint16 = 0x64

const ps2ይጠብቁገደብ = 100000

func ይጠብቁps2ማስገቢያባዶ() bool {
	for i := 0; i < ps2ይጠብቁገደብ; i++ {
		if (Portማንበቢያbyte(ትእዛዝport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ይጠብቁps2ውጤትሙሉ() bool {
	for i := 0; i < ps2ይጠብቁገደብ; i++ {
		if (Portማንበቢያbyte(ትእዛዝport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func መጻፊያps2ትእዛዝ(ዋጋ uint8) bool {
	if !ይጠብቁps2ማስገቢያባዶ() {
		return false
	}
	Portመጻፊያbyte(ትእዛዝport_2, ዋጋ)
	return true
}

func መጻፊያps2data(ዋጋ uint8) bool {
	if !ይጠብቁps2ማስገቢያባዶ() {
		return false
	}
	Portመጻፊያbyte(dataport_2, ዋጋ)
	return true
}

func ማንበቢያps2data() (uint8, bool) {
	if !ይጠብቁps2ውጤትሙሉ() {
		return 0, false
	}
	return Portማንበቢያbyte(dataport_2), true
}

func sendአይጥትእዛዝ(ዋጋ uint8) bool {
	if !መጻፊያps2ትእዛዝ(0xD4) || !መጻፊያps2data(ዋጋ) {
		return false
	}
	ack, እሺ := ማንበቢያps2data()
	return እሺ && ack == 0xFA
}

func (self *Tአይጥdriver) Initdriver(manager *Tማቋረጫmanager, አይጥeventhandler Iአይጥeventhandler) {

	iአይጥeventhandler = Tነባርአይጥeventhandler{}

	if አይጥeventhandler != nil {
		iአይጥeventhandler = አይጥeventhandler
	}

	አሰራአይጥdriver = self
	ማቋረጫhandler = handleአይጥማቋረጫ
	var address uintptr
	address = uintptr(Pointer(&ማቋረጫhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portማንበቢያbyte(ትእዛዝport_2)&0x01) != 0; i++ {
		Portማንበቢያbyte(dataport_2)
	}

	if !መጻፊያps2ትእዛዝ(0xA8) || !መጻፊያps2ትእዛዝ(0x20) {
		return
	}
	ሁኔታ, እሺ := ማንበቢያps2data()
	if !እሺ {
		return
	}
	ሁኔታ |= 0x02
	ሁኔታ &^= 0x20
	if !መጻፊያps2ትእዛዝ(0x60) || !መጻፊያps2data(ሁኔታ) {
		return
	}

	if !sendአይጥትእዛዝ(0xF6) || !sendአይጥትእዛዝ(0xF4) {
		return
	}
	offset = 0

}

func handleአይጥማቋረጫ(esp uint32) uint32 {
	if አሰራአይጥdriver == nil {
		Portማንበቢያbyte(dataport_2)
		return esp
	}
	return አሰራአይጥdriver.Handleማቋረጫ(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var button_2 int8
var pendingx int16
var pendingy int16
var pendingbutton int8
var pendingአይጥevent bool

func (self *Tአይጥdriver) Handleማቋረጫ(esp uint32) uint32 {
	ሁኔታ := Portማንበቢያbyte(ትእዛዝport_2)
	if (ሁኔታ&0x01) == 0 || (ሁኔታ&0x20) == 0 {
		return esp
	}

	data := Portማንበቢያbyte(dataport_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetሁኔታ := uint8(buffer_2[0])

		if (packetሁኔታ & 0xC0) == 0 {
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
		pendingbutton = int8(packetሁኔታ & 0x07)
		pendingአይጥevent = true
	}

	return esp

}

func Pሂደቶችpendingአይጥevents() {
	if iአይጥeventhandler == nil {
		return
	}

	Iማቋረጫdeactive()
	if !pendingአይጥevent {
		Iማቋረጫአሰራ()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	አዲስbutton := pendingbutton
	oldbutton := button_2

	pendingx = 0
	pendingy = 0
	pendingአይጥevent = false
	Iማቋረጫአሰራ()

	if x != 0 || y != 0 {
		iአይጥeventhandler.Oማብሪያአይጥመንቀሳቅስ(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		mask := int8(0x1 << i)
		if (አዲስbutton & mask) != (oldbutton & mask) {
			if (አዲስbutton & mask) != 0 {
				iአይጥeventhandler.Oማብሪያአይጥወደታች(int8(i + 1))
			} else {
				iአይጥeventhandler.Oማብሪያአይጥወደላይ(int8(i + 1))
			}
		}
	}
	button_2 = አዲስbutton
}
