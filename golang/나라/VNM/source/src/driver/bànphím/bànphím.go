package bànphím

import . "unsafe"

import . "cổng"
import . "giánđoạn"

import . "console"
import . "hệthốngcall"

type IBànphímSựkiệnhandler interface {
	Bậtkeydown(key byte)
	BậtkeyLên(key byte)
}

var iBànphímSựkiệnhandler IBànphímSựkiệnhandler
var mặcđịnhBànphímSựkiệnhandler TMặcđịnhBànphímSựkiệnhandler

type TMặcđịnhBànphímSựkiệnhandler struct {
}

func (mình *TMặcđịnhBànphímSựkiệnhandler) Bậtkeydown(key byte) {
	thậplục := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = thậplục[((key >> 4) & 0xF)]
	buffer[18] = thậplục[key&0xF]

	console_2 := TConsole{}
	console_2.MIn(buffer)

}
func (mình *TMặcđịnhBànphímSựkiệnhandler) BậtkeyLên(key byte) {
}

type TBànphímdriver struct {
	TGiánđoạnhandler
}

var hoạtđộngBànphímdriver *TBànphímdriver
var giánđoạnhandler func(uint32) uint32

var dataCổng_2 uint16 = 0x60
var lệnhCổng_2 uint16 = 0x64

const ps2ChờGiớihạn = 100000

func chờps2GõRỗng() bool {
	for i := 0; i < ps2ChờGiớihạn; i++ {
		if (CổngĐọcbyte(lệnhCổng_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func chờps2KếtxuấtĐầy() bool {
	for i := 0; i < ps2ChờGiớihạn; i++ {
		if (CổngĐọcbyte(lệnhCổng_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func ghips2Lệnh(giátrị uint8) bool {
	if !chờps2GõRỗng() {
		return false
	}
	CổngGhibyte(lệnhCổng_2, giátrị)
	return true
}

func ghips2data(giátrị uint8) bool {
	if !chờps2GõRỗng() {
		return false
	}
	CổngGhibyte(dataCổng_2, giátrị)
	return true
}

func đọcps2data() (uint8, bool) {
	if !chờps2KếtxuấtĐầy() {
		return 0, false
	}
	return CổngĐọcbyte(dataCổng_2), true
}

func (mình *TBànphímdriver) Initdriver(manager *TGiánđoạnmanager, bànphímSựkiệnhandler IBànphímSựkiệnhandler) {

	iBànphímSựkiệnhandler = &mặcđịnhBànphímSựkiệnhandler
	if bànphímSựkiệnhandler != nil {
		iBànphímSựkiệnhandler = bànphímSựkiệnhandler
	}

	hoạtđộngBànphímdriver = mình
	giánđoạnhandler = handleBànphímGiánđoạn
	var address uintptr
	address = uintptr(Pointer(&giánđoạnhandler))

	mình.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (CổngĐọcbyte(lệnhCổng_2)&0x01) != 0; i++ {
		CổngĐọcbyte(dataCổng_2)
	}

	if !ghips2Lệnh(0xAE) || !ghips2Lệnh(0x20) {
		return
	}
	trạngthái, đồngý := đọcps2data()
	if !đồngý {
		return
	}
	trạngthái |= 0x01
	trạngthái &^= 0x10
	if !ghips2Lệnh(0x60) || !ghips2data(trạngthái) {
		return
	}

	if !ghips2data(0xF4) {
		return
	}
	ack, đồngý := đọcps2data()
	if !đồngý || ack != 0xFA {
		return
	}

}

func handleBànphímGiánđoạn(esp uint32) uint32 {
	if hoạtđộngBànphímdriver == nil {
		CổngĐọcbyte(dataCổng_2)
		return esp
	}
	return hoạtđộngBànphímdriver.HandleGiánđoạn(esp)
}

const bànphímqueueCỡ = 64

var bànphímqueue [bànphímqueueCỡ]byte
var bànphímqueueĐọc uint8
var bànphímqueueGhi uint8
var tráishift bool
var phảishift bool
var extendedQuétcode bool

func queueBànphímbyte(key byte) {
	kế := (bànphímqueueGhi + 1) % bànphímqueueCỡ
	if kế == bànphímqueueĐọc {
		return
	}
	bànphímqueue[bànphímqueueGhi] = key
	bànphímqueueGhi = kế
}

func TiếntrìnhpendingBànphímevents() {
	for bànphímqueueĐọc != bànphímqueueGhi {
		key := bànphímqueue[bànphímqueueĐọc]
		bànphímqueueĐọc = (bànphímqueueĐọc + 1) % bànphímqueueCỡ
		Stdinputbyte(key)
		if iBànphímSựkiệnhandler != nil {
			iBànphímSựkiệnhandler.Bậtkeydown(key)
		}
	}
}

func quétcodetobyte(quétcode uint8) (byte, bool) {
	shift := tráishift || phảishift

	if quétcode >= 0x02 && quétcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[quétcode-0x02], true
		}
		return "1234567890"[quétcode-0x02], true
	}
	if quétcode >= 0x10 && quétcode <= 0x19 {
		key := "qwertyuiop"[quétcode-0x10]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if quétcode >= 0x1E && quétcode <= 0x26 {
		key := "asdfghjkl"[quétcode-0x1E]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if quétcode >= 0x2C && quétcode <= 0x32 {
		key := "zxcvbnm"[quétcode-0x2C]
		if shift {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch quétcode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (mình *TBànphímdriver) HandleGiánđoạn(esp uint32) uint32 {
	trạngthái := CổngĐọcbyte(lệnhCổng_2)
	if (trạngthái&0x01) == 0 || (trạngthái&0x20) != 0 {
		return esp
	}

	quétcode := CổngĐọcbyte(dataCổng_2)
	if quétcode == 0xE0 {
		extendedQuétcode = true
		return esp
	}
	if extendedQuétcode {
		extendedQuétcode = false
		return esp
	}

	released := (quétcode & 0x80) != 0
	basecode := quétcode & 0x7F
	if basecode == 0x2A {
		tráishift = !released
		return esp
	}
	if basecode == 0x36 {
		phảishift = !released
		return esp
	}
	if released {
		return esp
	}

	if key, đồngý := quétcodetobyte(basecode); đồngý {
		queueBànphímbyte(key)
	}

	return esp
}
