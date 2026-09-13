package gate

import (
	"ввідвивід"
)

type ПерериванняЧисло uint8

const (
	ПоділитиbyНуль	= ПерериванняЧисло(0)

	Морськамиля	= ПерериванняЧисло(2)

	Overflow	= ПерериванняЧисло(4)

	BoundДіяпазонexceeded	= ПерериванняЧисло(5)

	Помилковийopcode	= ПерериванняЧисло(6)

	ПристрійnotДоступно	= ПерериванняЧисло(7)

	Подвійнийfault	= ПерериванняЧисло(8)

	Помилковийtss	= ПерериванняЧисло(10)

	SegmentnotПрисутній	= ПерериванняЧисло(11)

	Stacksegmentfault	= ПерериванняЧисло(12)

	Gpfexception	= ПерериванняЧисло(13)

	Сторінкаfaultexception	= ПерериванняЧисло(14)

	Плаваючеpointexception	= ПерериванняЧисло(16)

	Alignmentcheck	= ПерериванняЧисло(17)

	Machinecheck	= ПерериванняЧисло(18)

	Simdплаваючеpointexception	= ПерериванняЧисло(19)
)

func Init() {
	встановитиidt()
}

func ЕлементкеруванняПереривання(intЧисло ПерериванняЧисло, istoffset uint8, handler func(*Registers))

func встановитиidt()

func dispatchПереривання()

func перериванняgateзапис()
