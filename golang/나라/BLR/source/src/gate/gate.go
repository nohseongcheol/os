package gate

import ()

type ПерарываннеНУМАР uint8

const (
	Dividebyzero	= ПерарываннеНУМАР(0)

	Nmi	= ПерарываннеНУМАР(2)

	Overflow	= ПерарываннеНУМАР(4)

	BoundДыяпазонexceeded	= ПерарываннеНУМАР(5)

	Няправільныopcode	= ПерарываннеНУМАР(6)

	ПрыладаnotДаступна	= ПерарываннеНУМАР(7)

	Падвойнаяfault	= ПерарываннеНУМАР(8)

	Няправільныtss	= ПерарываннеНУМАР(10)

	SegmentnotПрысутнічае	= ПерарываннеНУМАР(11)

	Stacksegmentfault	= ПерарываннеНУМАР(12)

	Gpfexception	= ПерарываннеНУМАР(13)

	Старонкаfaultexception	= ПерарываннеНУМАР(14)

	Зменныpointexception	= ПерарываннеНУМАР(16)

	Alignmentcheck	= ПерарываннеНУМАР(17)

	Machinecheck	= ПерарываннеНУМАР(18)

	Simdзменныpointexception	= ПерарываннеНУМАР(19)
)

func Init() {
	устанавіцьidt()
}

func HandleПерарыванне(цэлыНУМАР ПерарываннеНУМАР, istoffset uint8, handler func(*Registers))

func устанавіцьidt()

func dispatchПерарыванне()

func перарываннеgateentry()
