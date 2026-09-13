package gate

import (
	"io"
)

type Iפסקמספר uint8

const (
	Dividebyzero	= Iפסקמספר(0)

	Nננומטר	= Iפסקמספר(2)

	Overflow	= Iפסקמספר(4)

	Boundrangeexceeded	= Iפסקמספר(5)

	Iלאתקניopcode	= Iפסקמספר(6)

	Dהתקןnotפנוי	= Iפסקמספר(7)

	Dכפולfault	= Iפסקמספר(8)

	Iלאתקניtss	= Iפסקמספר(10)

	Segmentnotנוכח	= Iפסקמספר(11)

	Stacksegmentfault	= Iפסקמספר(12)

	Gpfexception	= Iפסקמספר(13)

	Pעמודfaultexception	= Iפסקמספר(14)

	Fצףpointexception	= Iפסקמספר(16)

	Alignmentcheck	= Iפסקמספר(17)

	Machinecheck	= Iפסקמספר(18)

	Simdצףpointexception	= Iפסקמספר(19)
)

func Init() {
	התקנהidt()
}

func Hידיתפסק(intמספר Iפסקמספר, istoffset uint8, handler func(*Registers))

func התקנהidt()

func dispatchפסק()

func פסקgateentry()
