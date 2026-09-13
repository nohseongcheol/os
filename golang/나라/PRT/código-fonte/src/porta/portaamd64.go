package porta

import (
	"eS"
)

type InterrupçãoNúmero uint8

const (
	Dividirbyzero	= InterrupçãoNúmero(0)

	Mln	= InterrupçãoNúmero(2)

	Overflow	= InterrupçãoNúmero(4)

	BoundIntervaloexceeded	= InterrupçãoNúmero(5)

	Inválidoopcode	= InterrupçãoNúmero(6)

	DispositivonotDisponível	= InterrupçãoNúmero(7)

	Duplofalha	= InterrupçãoNúmero(8)

	Inválidotss	= InterrupçãoNúmero(10)

	SegmentnotPresente	= InterrupçãoNúmero(11)

	Stacksegmentfalha	= InterrupçãoNúmero(12)

	Gpfexception	= InterrupçãoNúmero(13)

	Páginafalhaexception	= InterrupçãoNúmero(14)

	Flutuarpointexception	= InterrupçãoNúmero(16)

	Alignmentcheck	= InterrupçãoNúmero(17)

	Machinecheck	= InterrupçãoNúmero(18)

	Simdflutuarpointexception	= InterrupçãoNúmero(19)
)

func Init() {
	instalaridt()
}

func Manípulointerrupção(intNúmero InterrupçãoNúmero, istDeslocamento uint8, handler func(*Registers))

func instalaridt()

func dispatchinterrupção()

func interrupçãoportapontodeentrada()
