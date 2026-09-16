/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type IntrerupereNumăr uint8

const (
	Impartirebyzero	= IntrerupereNumăr(0)

	Nmi	= IntrerupereNumăr(2)

	Overflow	= IntrerupereNumăr(4)

	BoundIntervalexceeded	= IntrerupereNumăr(5)

	Nevalidopcode	= IntrerupereNumăr(6)

	DispozitivnotDisponibil	= IntrerupereNumăr(7)

	Doublefault	= IntrerupereNumăr(8)

	Nevalidtss	= IntrerupereNumăr(10)

	SegmentnotPrezent	= IntrerupereNumăr(11)

	Stacksegmentfault	= IntrerupereNumăr(12)

	Gpfexception	= IntrerupereNumăr(13)

	PAGINĂfaultexception	= IntrerupereNumăr(14)

	Liberpointexception	= IntrerupereNumăr(16)

	Alignmentcheck	= IntrerupereNumăr(17)

	Machinecheck	= IntrerupereNumăr(18)

	SimdLiberpointexception	= IntrerupereNumăr(19)
)

func Init() {
	instaleazăidt()
}

func MânerIntrerupere(intNumăr IntrerupereNumăr, istoffset uint8, handler func(*Registers))

func instaleazăidt()

func dispatchIntrerupere()

func intreruperegateînregistrare()
