package gate

import ()

type PertraukimasSkaičius uint8

const (
	DalybabyNulis	= PertraukimasSkaičius(0)

	Nmi	= PertraukimasSkaičius(2)

	Overflow	= PertraukimasSkaičius(4)

	BoundSritisexceeded	= PertraukimasSkaičius(5)

	Klaidingaopcode	= PertraukimasSkaičius(6)

	ĮrenginysnotPrieinama	= PertraukimasSkaičius(7)

	Dvigubafault	= PertraukimasSkaičius(8)

	Klaidingatss	= PertraukimasSkaičius(10)

	SegmentnotYra	= PertraukimasSkaičius(11)

	Stacksegmentfault	= PertraukimasSkaičius(12)

	Gpfexception	= PertraukimasSkaičius(13)

	Puslapisfaultexception	= PertraukimasSkaičius(14)

	Slankuspointexception	= PertraukimasSkaičius(16)

	Alignmentcheck	= PertraukimasSkaičius(17)

	Machinecheck	= PertraukimasSkaičius(18)

	SimdSlankuspointexception	= PertraukimasSkaičius(19)
)

func Init() {
	įdiegtiidt()
}

func PozicijaPertraukimas(intSkaičius PertraukimasSkaičius, istoffset uint8, handler func(*Registers))

func įdiegtiidt()

func dispatchPertraukimas()

func pertraukimasgateįrašas()
