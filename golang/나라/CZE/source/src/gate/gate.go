/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type PřerušeníČíslo uint8

const (
	DěleníbyNula	= PřerušeníČíslo(0)

	Nmi	= PřerušeníČíslo(2)

	Overflow	= PřerušeníČíslo(4)

	BoundRozsahexceeded	= PřerušeníČíslo(5)

	Neplatnéopcode	= PřerušeníČíslo(6)

	ZařízenínotKdispozici	= PřerušeníČíslo(7)

	Dvojitéfault	= PřerušeníČíslo(8)

	Neplatnétss	= PřerušeníČíslo(10)

	SegmentnotSoučasný	= PřerušeníČíslo(11)

	Stacksegmentfault	= PřerušeníČíslo(12)

	Gpfexception	= PřerušeníČíslo(13)

	Stránkafaultexception	= PřerušeníČíslo(14)

	Plovoucípointexception	= PřerušeníČíslo(16)

	Alignmentcheck	= PřerušeníČíslo(17)

	Machinecheck	= PřerušeníČíslo(18)

	SimdPlovoucípointexception	= PřerušeníČíslo(19)
)

func Init() {
	instalovatidt()
}

func ÚchytkaPřerušení(intČíslo PřerušeníČíslo, istoffset uint8, handler func(*Registers))

func instalovatidt()

func dispatchPřerušení()

func přerušenígateZáznam()
