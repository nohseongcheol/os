package gate

import (
	"io"
)

type ΔιακοπήΑριθμός uint8

const (
	ΔιαίρεσηbyΜηδέν	= ΔιακοπήΑριθμός(0)

	Nmi	= ΔιακοπήΑριθμός(2)

	Overflow	= ΔιακοπήΑριθμός(4)

	BoundΕύροςexceeded	= ΔιακοπήΑριθμός(5)

	Μηέγκυροopcode	= ΔιακοπήΑριθμός(6)

	ΣυσκευήnotΔιαθέσιμα	= ΔιακοπήΑριθμός(7)

	Διπλόςfault	= ΔιακοπήΑριθμός(8)

	Μηέγκυροtss	= ΔιακοπήΑριθμός(10)

	SegmentnotΠαρούσα	= ΔιακοπήΑριθμός(11)

	Stacksegmentfault	= ΔιακοπήΑριθμός(12)

	Gpfexception	= ΔιακοπήΑριθμός(13)

	Σελίδαfaultexception	= ΔιακοπήΑριθμός(14)

	Πλωτόpointexception	= ΔιακοπήΑριθμός(16)

	Alignmentcheck	= ΔιακοπήΑριθμός(17)

	Machinecheck	= ΔιακοπήΑριθμός(18)

	SimdΠλωτόpointexception	= ΔιακοπήΑριθμός(19)
)

func Init() {
	εγκατάστασηidt()
}

func ΧειρολαβήΔιακοπή(ακέραιοςΑριθμός ΔιακοπήΑριθμός, istoffset uint8, handler func(*Registers))

func εγκατάστασηidt()

func dispatchΔιακοπή()

func διακοπήgateκαταχώρηση()
