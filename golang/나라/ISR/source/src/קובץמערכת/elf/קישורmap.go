/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "זיכרוןmanager"

type Lקישור struct {
	Dדינמי		uintptr
	Previous	*Lקישור
	Nהבא		*Lקישור
}
type Lקישורmap struct {
	First	*Lקישור
	Lאחרון	*Lקישור

	Sגודל_2	int

	mem	*mem.Tזיכרוןmanager
}

func (self *Lקישורmap) Init(mem *mem.Tזיכרוןmanager) {
	self.mem = mem
}
func (self *Lקישורmap) Clone() Lקישורmap {
	var קישורmap Lקישורmap

	קישורmap.Init(self.mem)

	Lקישור := self.First

	for ; Lקישור != nil; Lקישור = Lקישור.Nהבא {
		קישורmap.Append_to_list(Lקישור.Dדינמי)
	}
	return קישורmap
}
func (self *Lקישורmap) Prepend_to_list(Dדינמי uintptr) {
	חדשקישור := (*Lקישור)(self.mem.Malloc(uint32(Sizeof(Lקישור{}))))
	חדשקישור.Dדינמי = Dדינמי
	חדשקישור.Nהבא = self.First
	self.First = חדשקישור
	self.Sגודל_2++

	if self.First.Nהבא == nil {
		self.Lאחרון = self.First
	}
}
func (self *Lקישורmap) Append_to_list(Dדינמי uintptr) {
	if Dדינמי == 0 {
		return
	}

	if self.Sגודל_2 == 0 {
		self.Prepend_to_list(Dדינמי)
	} else {
		חדשקישור := (*Lקישור)(self.mem.Malloc(uint32(Sizeof(Lקישור{}))))
		חדשקישור.Dדינמי = Dדינמי
		חדשקישור.Nהבא = nil
		self.Lאחרון.Nהבא = חדשקישור
		self.Lאחרון = חדשקישור
		self.Sגודל_2++
	}
}
func (self *Lקישורmap) Pהדפסה(x uint16, y uint16) {
	Lקישור := self.First
	console_2 := TConsole{}
	console_2.Mהדפסהxy("linkmap : ", x, y)
	for ; Lקישור != nil; Lקישור = Lקישור.Nהבא {
		console_2.MUnsignedinteger32הדפסה(uint32(Lקישור.Dדינמי))
		console_2.Mהדפסה("+")

	}
}
