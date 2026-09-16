/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type MegszakításSzám uint8

const (
	OsztásbyNulla	= MegszakításSzám(0)

	Nmi	= MegszakításSzám(2)

	Overflow	= MegszakításSzám(4)

	BoundTartományexceeded	= MegszakításSzám(5)

	Érvénytelenopcode	= MegszakításSzám(6)

	EszközNemElérhető	= MegszakításSzám(7)

	Duplafault	= MegszakításSzám(8)

	Érvénytelentss	= MegszakításSzám(10)

	SegmentNemJelenvan	= MegszakításSzám(11)

	Stacksegmentfault	= MegszakításSzám(12)

	Gpfexception	= MegszakításSzám(13)

	Oldalfaultexception	= MegszakításSzám(14)

	Lebegőpointexception	= MegszakításSzám(16)

	Alignmentcheck	= MegszakításSzám(17)

	Machinecheck	= MegszakításSzám(18)

	SimdLebegőpointexception	= MegszakításSzám(19)
)

func Init() {
	telepítésidt()
}

func FogantyúMegszakítás(egészSzám MegszakításSzám, istEltolás uint8, handler func(*Registers))

func telepítésidt()

func dispatchMegszakítás()

func megszakításgatebejegyzés()
