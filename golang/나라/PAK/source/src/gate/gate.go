package gate

import ()

type Iمداخلتnumber uint8

const (
	Dividebyzero	= Iمداخلتnumber(0)

	Nmi	= Iمداخلتnumber(2)

	Overflow	= Iمداخلتnumber(4)

	Boundrangeexceeded	= Iمداخلتnumber(5)

	Invalidopcode	= Iمداخلتnumber(6)

	Dآلہnotدستیاب	= Iمداخلتnumber(7)

	Doublefault	= Iمداخلتnumber(8)

	Invalidtss	= Iمداخلتnumber(10)

	Segmentnotموجود	= Iمداخلتnumber(11)

	Stacksegmentfault	= Iمداخلتnumber(12)

	Gpfexception	= Iمداخلتnumber(13)

	Pصفحہfaultexception	= Iمداخلتnumber(14)

	Fفلوٹنگpointexception	= Iمداخلتnumber(16)

	Alignmentcheck	= Iمداخلتnumber(17)

	Machinecheck	= Iمداخلتnumber(18)

	Simdفلوٹنگpointexception	= Iمداخلتnumber(19)
)

func Init() {
	نصبکریںidt()
}

func Handleمداخلت(intnumber Iمداخلتnumber, istoffset uint8, handler func(*Registers))

func نصبکریںidt()

func dispatchمداخلت()

func مداخلتgateentry()
