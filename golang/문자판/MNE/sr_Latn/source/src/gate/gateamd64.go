package gate

import (
	"уИ"
)

type Ometanjebroj uint8

const (
	Dividebyzero	= Ometanjebroj(0)

	Nmi	= Ometanjebroj(2)

	Overflow	= Ometanjebroj(4)

	BoundOpsegexceeded	= Ometanjebroj(5)

	Neispravnoopcode	= Ometanjebroj(6)

	UređajnotRaspoloživo	= Ometanjebroj(7)

	Dvostrukofault	= Ometanjebroj(8)

	Neispravnotss	= Ometanjebroj(10)

	SegmentnotPrisutna	= Ometanjebroj(11)

	Stacksegmentfault	= Ometanjebroj(12)

	Gpfexception	= Ometanjebroj(13)

	STRANAfaultexception	= Ometanjebroj(14)

	Lebdećipointexception	= Ometanjebroj(16)

	Alignmentcheck	= Ometanjebroj(17)

	Machinecheck	= Ometanjebroj(18)

	SimdLebdećipointexception	= Ometanjebroj(19)
)

func Init() {
	instalirajidt()
}

func RučkaOmetanje(celibrojbroj Ometanjebroj, istoffset uint8, handler func(*Registers))

func instalirajidt()

func dispatchOmetanje()

func ometanjegateunos()
