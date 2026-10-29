/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package puerta

import ()

type InterrupciónNúmero uint8

const (
	DividirbyCero	= InterrupciónNúmero(0)

	Nmi	= InterrupciónNúmero(2)

	Overflow	= InterrupciónNúmero(4)

	BoundIntervaloexceeded	= InterrupciónNúmero(5)

	Noválidoopcode	= InterrupciónNúmero(6)

	DispositivonotDisponible	= InterrupciónNúmero(7)

	Doblefallo	= InterrupciónNúmero(8)

	Noválidotss	= InterrupciónNúmero(10)

	SegmentnotPresente	= InterrupciónNúmero(11)

	Stacksegmentfallo	= InterrupciónNúmero(12)

	Gpfexception	= InterrupciónNúmero(13)

	Páginafalloexception	= InterrupciónNúmero(14)

	Flotandopointexception	= InterrupciónNúmero(16)

	Alignmentcheck	= InterrupciónNúmero(17)

	Machinecheck	= InterrupciónNúmero(18)

	SimdFlotandopointexception	= InterrupciónNúmero(19)
)

func Init() {
	instalaridt()
}

func Manijainterrupción(enteroNúmero InterrupciónNúmero, istDesplazamiento uint8, handler func(*Registers))

func instalaridt()

func dispatchinterrupción()

func interrupciónpuertaentrada()
