package gate

import ()

type PrekidBROJ uint8

const (
	Dividebyzero	= PrekidBROJ(0)

	Nmi	= PrekidBROJ(2)

	Overflow	= PrekidBROJ(4)

	BoundOpsegexceeded	= PrekidBROJ(5)

	Neispravnoopcode	= PrekidBROJ(6)

	UređajnotDostupno	= PrekidBROJ(7)

	Dvostrukofault	= PrekidBROJ(8)

	Neispravnotss	= PrekidBROJ(10)

	SegmentnotPrisutno	= PrekidBROJ(11)

	Stacksegmentfault	= PrekidBROJ(12)

	Gpfexception	= PrekidBROJ(13)

	Stranicafaultexception	= PrekidBROJ(14)

	Plutajućepointexception	= PrekidBROJ(16)

	Alignmentcheck	= PrekidBROJ(17)

	Machinecheck	= PrekidBROJ(18)

	Simdplutajućepointexception	= PrekidBROJ(19)
)

func Init() {
	instalirajidt()
}

func RučkaPrekid(intBROJ PrekidBROJ, istoffset uint8, handler func(*Registers))

func instalirajidt()

func dispatchPrekid()

func prekidgateentry()
