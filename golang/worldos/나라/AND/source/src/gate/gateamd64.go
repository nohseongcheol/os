/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"eS"
)

type InterrupcióNombre uint8

const (
	Dividebyzero	= InterrupcióNombre(0)

	Nmi	= InterrupcióNombre(2)

	Overflow	= InterrupcióNombre(4)

	BoundIntervalexceeded	= InterrupcióNombre(5)

	Invàlidopcode	= InterrupcióNombre(6)

	DispositiunotDisponible	= InterrupcióNombre(7)

	Doblefault	= InterrupcióNombre(8)

	Invàlidtss	= InterrupcióNombre(10)

	Segmentnotpresent	= InterrupcióNombre(11)

	Stacksegmentfault	= InterrupcióNombre(12)

	Gpfexception	= InterrupcióNombre(13)

	Pàginafaultexception	= InterrupcióNombre(14)

	Flotantpointexception	= InterrupcióNombre(16)

	Alignmentcheck	= InterrupcióNombre(17)

	Machinecheck	= InterrupcióNombre(18)

	SimdFlotantpointexception	= InterrupcióNombre(19)
)

func Init() {
	installidt()
}

func GestorInterrupció(enterNombre InterrupcióNombre, istoffset uint8, handler func(*Registers))

func installidt()

func dispatchInterrupció()

func interrupciógateentrada()
