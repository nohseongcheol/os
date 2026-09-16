/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type SampukNOMBOR uint8

const (
	Dividebyzero	= SampukNOMBOR(0)

	Nmi	= SampukNOMBOR(2)

	Overflow	= SampukNOMBOR(4)

	BoundJulatexceeded	= SampukNOMBOR(5)

	Taksahopcode	= SampukNOMBOR(6)

	PerantinotTersedia	= SampukNOMBOR(7)

	Dwifault	= SampukNOMBOR(8)

	Taksahtss	= SampukNOMBOR(10)

	SegmentnotHadir	= SampukNOMBOR(11)

	Stacksegmentfault	= SampukNOMBOR(12)

	Gpfexception	= SampukNOMBOR(13)

	Halamanfaultexception	= SampukNOMBOR(14)

	Terapungpointexception	= SampukNOMBOR(16)

	Alignmentcheck	= SampukNOMBOR(17)

	Machinecheck	= SampukNOMBOR(18)

	Simdterapungpointexception	= SampukNOMBOR(19)
)

func Init() {
	pasangidt()
}

func KendaliSampuk(intNOMBOR SampukNOMBOR, istoffset uint8, handler func(*Registers))

func pasangidt()

func dispatchSampuk()

func sampukgateentry()
