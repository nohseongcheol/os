package gate

import ()

type KatkestusArv uint8

const (
	Dividebyzero	= KatkestusArv(0)

	Nmi	= KatkestusArv(2)

	Overflow	= KatkestusArv(4)

	BoundVahemikexceeded	= KatkestusArv(5)

	Viganeopcode	= KatkestusArv(6)

	SeadenotSaadaval	= KatkestusArv(7)

	Doublefault	= KatkestusArv(8)

	Viganetss	= KatkestusArv(10)

	SegmentnotOlemas	= KatkestusArv(11)

	Stacksegmentfault	= KatkestusArv(12)

	Gpfexception	= KatkestusArv(13)

	Lehekülgfaultexception	= KatkestusArv(14)

	Ujuvpointexception	= KatkestusArv(16)

	Alignmentcheck	= KatkestusArv(17)

	Machinecheck	= KatkestusArv(18)

	SimdUjuvpointexception	= KatkestusArv(19)
)

func Init() {
	paigaldaidt()
}

func HandleKatkestus(intArv KatkestusArv, istoffset uint8, handler func(*Registers))

func paigaldaidt()

func dispatchKatkestus()

func katkestusgatekirje()
