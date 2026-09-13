package gate

import ()

type GiánđoạnSỐ uint8

const (
	Dividebyzero	= GiánđoạnSỐ(0)

	Nmi	= GiánđoạnSỐ(2)

	Overflow	= GiánđoạnSỐ(4)

	BoundPhạmviexceeded	= GiánđoạnSỐ(5)

	Khônghợplệopcode	= GiánđoạnSỐ(6)

	ThiếtbịnotSẵnsàng	= GiánđoạnSỐ(7)

	Doublefault	= GiánđoạnSỐ(8)

	Khônghợplệtss	= GiánđoạnSỐ(10)

	SegmentnotCó	= GiánđoạnSỐ(11)

	Stacksegmentfault	= GiánđoạnSỐ(12)

	Gpfexception	= GiánđoạnSỐ(13)

	Trangfaultexception	= GiánđoạnSỐ(14)

	Khôngcốđịnhpointexception	= GiánđoạnSỐ(16)

	Alignmentcheck	= GiánđoạnSỐ(17)

	Machinecheck	= GiánđoạnSỐ(18)

	Simdkhôngcốđịnhpointexception	= GiánđoạnSỐ(19)
)

func Init() {
	càiđặtidt()
}

func HandleGiánđoạn(intSỐ GiánđoạnSỐ, istoffset uint8, handler func(*Registers))

func càiđặtidt()

func dispatchGiánđoạn()

func giánđoạngateentry()
