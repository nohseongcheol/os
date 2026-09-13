package gate

import ()

type PrerušenieČíslo uint8

const (
	DeleniebyNula	= PrerušenieČíslo(0)

	NM	= PrerušenieČíslo(2)

	Overflow	= PrerušenieČíslo(4)

	BoundRozsahexceeded	= PrerušenieČíslo(5)

	Neplatnéopcode	= PrerušenieČíslo(6)

	ZariadenienotDostupné	= PrerušenieČíslo(7)

	Dvojitéfault	= PrerušenieČíslo(8)

	Neplatnétss	= PrerušenieČíslo(10)

	SegmentnotPrítomné	= PrerušenieČíslo(11)

	Stacksegmentfault	= PrerušenieČíslo(12)

	Gpfexception	= PrerušenieČíslo(13)

	STRANAfaultexception	= PrerušenieČíslo(14)

	Pohyblivápointexception	= PrerušenieČíslo(16)

	Alignmentcheck	= PrerušenieČíslo(17)

	Machinecheck	= PrerušenieČíslo(18)

	Simdpohyblivápointexception	= PrerušenieČíslo(19)
)

func Init() {
	nainštalovaťidt()
}

func UškoPrerušenie(intČíslo PrerušenieČíslo, istPosunutie uint8, handler func(*Registers))

func nainštalovaťidt()

func dispatchPrerušenie()

func prerušeniegatepoložka()
