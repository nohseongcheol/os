/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type PrzerwanieLiczba uint8

const (
	Dzieleniebyzero	= PrzerwanieLiczba(0)

	Nmi	= PrzerwanieLiczba(2)

	Overflow	= PrzerwanieLiczba(4)

	BoundZakresexceeded	= PrzerwanieLiczba(5)

	Niewłaściwyopcode	= PrzerwanieLiczba(6)

	UrządzenienotDostępne	= PrzerwanieLiczba(7)

	Podwójnejprecyzjifault	= PrzerwanieLiczba(8)

	Niewłaściwytss	= PrzerwanieLiczba(10)

	SegmentnotObecny	= PrzerwanieLiczba(11)

	Stacksegmentfault	= PrzerwanieLiczba(12)

	Gpfexception	= PrzerwanieLiczba(13)

	Stronafaultexception	= PrzerwanieLiczba(14)

	Zmiennapointexception	= PrzerwanieLiczba(16)

	Alignmentcheck	= PrzerwanieLiczba(17)

	Machinecheck	= PrzerwanieLiczba(18)

	SimdZmiennapointexception	= PrzerwanieLiczba(19)
)

func Init() {
	instalacjaidt()
}

func UchwytPrzerwanie(całkowityLiczba PrzerwanieLiczba, istPrzesunięcie uint8, handler func(*Registers))

func instalacjaidt()

func dispatchPrzerwanie()

func przerwaniegatewpis()
