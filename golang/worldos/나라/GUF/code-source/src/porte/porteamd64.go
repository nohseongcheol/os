/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package porte

import (
	"eS"
)

type InterruptionNombre uint8

const (
	DivisionbyZéro	= InterruptionNombre(0)

	Nmi	= InterruptionNombre(2)

	Overflow	= InterruptionNombre(4)

	BoundIntervalleexceeded	= InterruptionNombre(5)

	Nonvalideopcode	= InterruptionNombre(6)

	PériphériqueNonDisponible	= InterruptionNombre(7)

	Doubledéfaut	= InterruptionNombre(8)

	Nonvalidetss	= InterruptionNombre(10)

	SegmentNonPrésente	= InterruptionNombre(11)

	Stacksegmentdéfaut	= InterruptionNombre(12)

	Gpfexception	= InterruptionNombre(13)

	Pagedéfautexception	= InterruptionNombre(14)

	Flottantepointexception	= InterruptionNombre(16)

	Alignmentcheck	= InterruptionNombre(17)

	Machinecheck	= InterruptionNombre(18)

	SimdFlottantepointexception	= InterruptionNombre(19)
)

func Init() {
	installeridt()
}

func Poignéeinterruption(intNombre InterruptionNombre, istDécalage uint8, handler func(*Registers))

func installeridt()

func dispatchinterruption()

func interruptionporteélément()
