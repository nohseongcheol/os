/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package elf

import . "unsafe"
import . "console"

import mem "حافظهmanager"

type Lپیوند struct {
	Dپویا		uintptr
	Previous	*Lپیوند
	Nبعدی		*Lپیوند
}
type Lپیوندmap struct {
	First	*Lپیوند
	Lآخرین	*Lپیوند

	Sاندازه_2	int

	mem	*mem.Tحافظهmanager
}

func (خود *Lپیوندmap) Init(mem *mem.Tحافظهmanager) {
	خود.mem = mem
}
func (خود *Lپیوندmap) Clone() Lپیوندmap {
	var پیوندmap Lپیوندmap

	پیوندmap.Init(خود.mem)

	Lپیوند := خود.First

	for ; Lپیوند != nil; Lپیوند = Lپیوند.Nبعدی {
		پیوندmap.Append_to_list(Lپیوند.Dپویا)
	}
	return پیوندmap
}
func (خود *Lپیوندmap) Prepend_to_list(Dپویا uintptr) {
	جدیدپیوند := (*Lپیوند)(خود.mem.Malloc(uint32(Sizeof(Lپیوند{}))))
	جدیدپیوند.Dپویا = Dپویا
	جدیدپیوند.Nبعدی = خود.First
	خود.First = جدیدپیوند
	خود.Sاندازه_2++

	if خود.First.Nبعدی == nil {
		خود.Lآخرین = خود.First
	}
}
func (خود *Lپیوندmap) Append_to_list(Dپویا uintptr) {
	if Dپویا == 0 {
		return
	}

	if خود.Sاندازه_2 == 0 {
		خود.Prepend_to_list(Dپویا)
	} else {
		جدیدپیوند := (*Lپیوند)(خود.mem.Malloc(uint32(Sizeof(Lپیوند{}))))
		جدیدپیوند.Dپویا = Dپویا
		جدیدپیوند.Nبعدی = nil
		خود.Lآخرین.Nبعدی = جدیدپیوند
		خود.Lآخرین = جدیدپیوند
		خود.Sاندازه_2++
	}
}
func (خود *Lپیوندmap) Pچاپ(x uint16, y uint16) {
	Lپیوند := خود.First
	console_2 := TConsole{}
	console_2.Mچاپxy("linkmap : ", x, y)
	for ; Lپیوند != nil; Lپیوند = Lپیوند.Nبعدی {
		console_2.MUnsignedinteger32چاپ(uint32(Lپیوند.Dپویا))
		console_2.Mچاپ("+")

	}
}
