package ստեղնաշար

import . "unsafe"

import . "պորտ"
import . "ընդհատել"

import . "console"
import . "համակարգcall"

type IՍտեղնաշարeventhandler interface {
	ՄիացնելԲանալիՆերքև(բանալի byte)
	ՄիացնելԲանալիՎերև(բանալի byte)
}

var iՍտեղնաշարeventhandler IՍտեղնաշարeventhandler
var հիմնականՍտեղնաշարeventhandler TՀիմնականՍտեղնաշարeventhandler

type TՀիմնականՍտեղնաշարeventhandler struct {
}

func (ինքնուրույն *TՀիմնականՍտեղնաշարeventhandler) ՄիացնելԲանալիՆերքև(բանալի byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((բանալի >> 4) & 0xF)]
	buffer[18] = hex[բանալի&0xF]

	console_2 := TConsole{}
	console_2.MՏպել(buffer)

}
func (ինքնուրույն *TՀիմնականՍտեղնաշարeventhandler) ՄիացնելԲանալիՎերև(բանալի byte) {
}

type TՍտեղնաշարdriver struct {
	TԸնդհատելhandler
}

var ակտիվՍտեղնաշարdriver *TՍտեղնաշարdriver
var ընդհատելhandler func(uint32) uint32

var dataՊորտ_2 uint16 = 0x60
var հրահանգՊորտ_2 uint16 = 0x64

const ps2Սպասելlimit = 100000

func սպասելps2ՀիմաԴատարկ() bool {
	for i := 0; i < ps2Սպասելlimit; i++ {
		if (ՊորտԸնթերցումbyte(հրահանգՊորտ_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func սպասելps2ԵլքԼրիվ() bool {
	for i := 0; i < ps2Սպասելlimit; i++ {
		if (ՊորտԸնթերցումbyte(հրահանգՊորտ_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func գրելps2Հրահանգ(արժեք uint8) bool {
	if !սպասելps2ՀիմաԴատարկ() {
		return false
	}
	ՊորտԳրելbyte(հրահանգՊորտ_2, արժեք)
	return true
}

func գրելps2data(արժեք uint8) bool {
	if !սպասելps2ՀիմաԴատարկ() {
		return false
	}
	ՊորտԳրելbyte(dataՊորտ_2, արժեք)
	return true
}

func ընթերցումps2data() (uint8, bool) {
	if !սպասելps2ԵլքԼրիվ() {
		return 0, false
	}
	return ՊորտԸնթերցումbyte(dataՊորտ_2), true
}

func (ինքնուրույն *TՍտեղնաշարdriver) Initdriver(manager *TԸնդհատելmanager, ստեղնաշարeventhandler IՍտեղնաշարeventhandler) {

	iՍտեղնաշարeventhandler = &հիմնականՍտեղնաշարeventhandler
	if ստեղնաշարeventhandler != nil {
		iՍտեղնաշարeventhandler = ստեղնաշարeventhandler
	}

	ակտիվՍտեղնաշարdriver = ինքնուրույն
	ընդհատելhandler = handleՍտեղնաշարԸնդհատել
	var address uintptr
	address = uintptr(Pointer(&ընդհատելhandler))

	ինքնուրույն.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ՊորտԸնթերցումbyte(հրահանգՊորտ_2)&0x01) != 0; i++ {
		ՊորտԸնթերցումbyte(dataՊորտ_2)
	}

	if !գրելps2Հրահանգ(0xAE) || !գրելps2Հրահանգ(0x20) {
		return
	}
	կարգավիճակ, ok := ընթերցումps2data()
	if !ok {
		return
	}
	կարգավիճակ |= 0x01
	կարգավիճակ &^= 0x10
	if !գրելps2Հրահանգ(0x60) || !գրելps2data(կարգավիճակ) {
		return
	}

	if !գրելps2data(0xF4) {
		return
	}
	ack, ok := ընթերցումps2data()
	if !ok || ack != 0xFA {
		return
	}

}

func handleՍտեղնաշարԸնդհատել(esp uint32) uint32 {
	if ակտիվՍտեղնաշարdriver == nil {
		ՊորտԸնթերցումbyte(dataՊորտ_2)
		return esp
	}
	return ակտիվՍտեղնաշարdriver.HandleԸնդհատել(esp)
}

const ստեղնաշարqueueՉափս = 64

var ստեղնաշարqueue [ստեղնաշարqueueՉափս]byte
var ստեղնաշարqueueԸնթերցում uint8
var ստեղնաշարqueueԳրել uint8
var ձախshiftՌեգիստրիփոփոխում bool
var աջshiftՌեգիստրիփոփոխում bool
var extendedՈրոնելcode bool

func queueՍտեղնաշարbyte(բանալի byte) {
	հաջորդ := (ստեղնաշարqueueԳրել + 1) % ստեղնաշարqueueՉափս
	if հաջորդ == ստեղնաշարqueueԸնթերցում {
		return
	}
	ստեղնաշարqueue[ստեղնաշարqueueԳրել] = բանալի
	ստեղնաշարqueueԳրել = հաջորդ
}

func ԳործընթացpendingՍտեղնաշարevents() {
	for ստեղնաշարqueueԸնթերցում != ստեղնաշարqueueԳրել {
		բանալի := ստեղնաշարqueue[ստեղնաշարqueueԸնթերցում]
		ստեղնաշարqueueԸնթերցում = (ստեղնաշարqueueԸնթերցում + 1) % ստեղնաշարqueueՉափս
		Stdinputbyte(բանալի)
		if iՍտեղնաշարeventhandler != nil {
			iՍտեղնաշարeventhandler.ՄիացնելԲանալիՆերքև(բանալի)
		}
	}
}

func որոնելcodetobyte(որոնելcode uint8) (byte, bool) {
	shiftՌեգիստրիփոփոխում := ձախshiftՌեգիստրիփոփոխում || աջshiftՌեգիստրիփոփոխում

	if որոնելcode >= 0x02 && որոնելcode <= 0x0B {
		if shiftՌեգիստրիփոփոխում {
			return "!@#$%^&*()"[որոնելcode-0x02], true
		}
		return "1234567890"[որոնելcode-0x02], true
	}
	if որոնելcode >= 0x10 && որոնելcode <= 0x19 {
		բանալի := "qwertyuiop"[որոնելcode-0x10]
		if shiftՌեգիստրիփոփոխում {
			բանալի -= 'a' - 'A'
		}
		return բանալի, true
	}
	if որոնելcode >= 0x1E && որոնելcode <= 0x26 {
		բանալի := "asdfghjkl"[որոնելcode-0x1E]
		if shiftՌեգիստրիփոփոխում {
			բանալի -= 'a' - 'A'
		}
		return բանալի, true
	}
	if որոնելcode >= 0x2C && որոնելcode <= 0x32 {
		բանալի := "zxcvbnm"[որոնելcode-0x2C]
		if shiftՌեգիստրիփոփոխում {
			բանալի -= 'a' - 'A'
		}
		return բանալի, true
	}

	switch որոնելcode {
	case 0x0C:
		if shiftՌեգիստրիփոփոխում {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shiftՌեգիստրիփոփոխում {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shiftՌեգիստրիփոփոխում {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shiftՌեգիստրիփոփոխում {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shiftՌեգիստրիփոփոխում {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shiftՌեգիստրիփոփոխում {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shiftՌեգիստրիփոփոխում {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shiftՌեգիստրիփոփոխում {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shiftՌեգիստրիփոփոխում {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shiftՌեգիստրիփոփոխում {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shiftՌեգիստրիփոփոխում {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (ինքնուրույն *TՍտեղնաշարdriver) HandleԸնդհատել(esp uint32) uint32 {
	կարգավիճակ := ՊորտԸնթերցումbyte(հրահանգՊորտ_2)
	if (կարգավիճակ&0x01) == 0 || (կարգավիճակ&0x20) != 0 {
		return esp
	}

	որոնելcode := ՊորտԸնթերցումbyte(dataՊորտ_2)
	if որոնելcode == 0xE0 {
		extendedՈրոնելcode = true
		return esp
	}
	if extendedՈրոնելcode {
		extendedՈրոնելcode = false
		return esp
	}

	released := (որոնելcode & 0x80) != 0
	basecode := որոնելcode & 0x7F
	if basecode == 0x2A {
		ձախshiftՌեգիստրիփոփոխում = !released
		return esp
	}
	if basecode == 0x36 {
		աջshiftՌեգիստրիփոփոխում = !released
		return esp
	}
	if released {
		return esp
	}

	if բանալի, ok := որոնելcodetobyte(basecode); ok {
		queueՍտեղնաշարbyte(բանալի)
	}

	return esp
}
