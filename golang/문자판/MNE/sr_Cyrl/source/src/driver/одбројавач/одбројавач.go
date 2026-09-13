package одбројавач

import . "unsafe"

import . "ометање"
import . "конзола"

type IОдбројавачДогађајhandler interface {
	Наtick()
}

var iОдбројавачДогађајhandler IОдбројавачДогађајhandler

type TПодразумеваноОдбројавачДогађајhandler struct {
}

func (исти *TПодразумеваноОдбројавачДогађајhandler) Наtick() {
}

type TОдбројавачdriver struct {
	TОметањеhandler
}

var ометањеhandler func(*TОдбројавачdriver, uint32) uint32

func (исти *TОдбројавачdriver) Init(manager *TОметањеmanager, тастатураДогађајhandler IОдбројавачДогађајhandler) {
	iОдбројавачДогађајhandler = &TПодразумеваноОдбројавачДогађајhandler{}
	if тастатураДогађајhandler != nil {
		iОдбројавачДогађајhandler = тастатураДогађајhandler
	}

	ометањеhandler = (*TОдбројавачdriver).РучкаОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))

	исти.TОметањеhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (исти *TОдбројавачdriver) РучкаОметање(esp uint32) uint32 {
	конзола_2 := TКонзола{}
	конзола_2.MUnsignedinteger32Штампајxy(tickcount, 3, 1)
	tickcount++

	return esp
}
