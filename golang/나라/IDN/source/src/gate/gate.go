package gate

import ()

type InterupsiNomor uint8

const (
	BagibyNol	= InterupsiNomor(0)

	Nmi	= InterupsiNomor(2)

	Overflow	= InterupsiNomor(4)

	BoundCakupanexceeded	= InterupsiNomor(5)

	Salahopcode	= InterupsiNomor(6)

	PerangkatnotTersedia	= InterupsiNomor(7)

	Gandafault	= InterupsiNomor(8)

	Salahtss	= InterupsiNomor(10)

	SegmentnotAda	= InterupsiNomor(11)

	Stacksegmentfault	= InterupsiNomor(12)

	Gpfexception	= InterupsiNomor(13)

	Halamanfaultexception	= InterupsiNomor(14)

	Mengambangpointexception	= InterupsiNomor(16)

	Alignmentcheck	= InterupsiNomor(17)

	Machinecheck	= InterupsiNomor(18)

	Simdmengambangpointexception	= InterupsiNomor(19)
)

func Init() {
	pasangidt()
}

func PenangananInterupsi(intNomor InterupsiNomor, istoffset uint8, handler func(*Registers))

func pasangidt()

func dispatchInterupsi()

func interupsigateentri()
