/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package списак

import . "unsafe"
import . "конзола"
import mem "меморијаmanager"

type Чвор struct {
	показивач	uintptr
	previous	*Чвор
	следеће		*Чвор
}

type LinkedСписак struct {
	head		*Чвор
	tail		*Чвор
	Величина_2	int

	mem	*mem.TМеморијаmanager
}

func (исти *LinkedСписак) Init(mem *mem.TМеморијаmanager) {
	исти.head = nil
	исти.tail = nil
	исти.Величина_2 = 0

	исти.mem = mem
}
func (исти *LinkedСписак) Prepend_to_list(показивач uintptr) {
	новаЧвор := (*Чвор)(исти.mem.Malloc(uint32(Sizeof(Чвор{}))))
	if новаЧвор == nil {
		return
	}
	новаЧвор.показивач = показивач
	новаЧвор.previous = nil
	новаЧвор.следеће = исти.head
	if исти.head != nil {
		исти.head.previous = новаЧвор
	}
	исти.head = новаЧвор
	исти.Величина_2++

	if исти.head.следеће == nil {
		исти.tail = исти.head
	}

}
func (исти *LinkedСписак) Append_to_list(показивач uintptr) {
	if исти.Величина_2 == 0 {
		исти.Prepend_to_list(показивач)
	} else {
		новаЧвор := (*Чвор)(исти.mem.Malloc(uint32(Sizeof(Чвор{}))))
		if новаЧвор == nil {
			return
		}
		новаЧвор.показивач = показивач
		новаЧвор.previous = исти.tail
		новаЧвор.следеће = nil
		исти.tail.следеће = новаЧвор
		исти.tail = новаЧвор
		исти.Величина_2++
	}
}
func (исти *LinkedСписак) Insert_at_index(попис int, показивач uintptr) {
	if попис == 0 {
		исти.Prepend_to_list(показивач)
	} else {
		previousЧвор := исти.GetЧворat(попис - 1)
		следећеЧвор := previousЧвор.следеће
		новаЧвор := (*Чвор)(исти.mem.Malloc(uint32(Sizeof(Чвор{}))))
		if новаЧвор == nil {
			return
		}
		новаЧвор.показивач = показивач

		previousЧвор.следеће = новаЧвор
		новаЧвор.previous = previousЧвор
		новаЧвор.следеће = следећеЧвор
		if следећеЧвор != nil {
			следећеЧвор.previous = новаЧвор
		}

		исти.Величина_2++

		if новаЧвор.следеће == nil {
			исти.tail = новаЧвор
		}
	}
}
func (исти *LinkedСписак) GetЧворat(попис int) *Чвор {
	if попис < 0 || попис >= исти.Величина_2 {
		return nil
	}
	var x *Чвор = исти.head
	for i := 0; i < попис; i++ {
		x = x.следеће
	}
	return x
}

func (исти *LinkedСписак) СкупЧворat(попис int, показивач uintptr) {
	var x *Чвор = исти.head
	for i := 0; i < попис; i++ {
		x = x.следеће
	}
	if x != nil {
		x.показивач = показивач
	}
}
func (исти *LinkedСписак) Getat(попис int) Pointer {
	чвор := исти.GetЧворat(попис)
	if чвор == nil {
		return nil
	}
	var показивач uintptr = чвор.показивач
	return Pointer(показивач)
}
func (исти *LinkedСписак) Пописод(показивач uintptr) int {
	var n *Чвор = исти.head
	i := 0
	for ; i < исти.Величина_2; i++ {
		if показивач == n.показивач {
			return i
		}
		n = n.следеће
	}
	return -1
}
func (исти *LinkedСписак) Уклони(показивач uintptr) {
	попис := исти.Пописод(показивач)
	if попис < 0 {
		return
	}
	исти.Уклониat(попис)
}
func (исти *LinkedСписак) Уклониat(попис int) {
	if попис < 0 || попис >= исти.Величина_2 {
		return
	}
	чвор := исти.GetЧворat(попис)
	if чвор == nil {
		return
	}
	if чвор.previous != nil {
		чвор.previous.следеће = чвор.следеће
	} else {
		исти.head = чвор.следеће
	}
	if чвор.следеће != nil {
		чвор.следеће.previous = чвор.previous
	} else {
		исти.tail = чвор.previous
	}
	исти.Величина_2 = исти.Величина_2 - 1

	if исти.mem != nil {
		исти.mem.Слободно(Pointer(чвор))
	}
}

var конзола_2 = TКонзола{}

func (исти *LinkedСписак) Штампај() {
	конзола_2.MШтампајxy("LinkedList:", 1, 1)
	конзола_2.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(исти))))
	for i := 0; i < исти.Величина_2; i++ {
		чвор := (*Чвор)(исти.Getat(i))
		конзола_2.MUnsignedinteger32Штампај(uint32(чвор.показивач))
		конзола_2.MШтампај(":")
	}
}
