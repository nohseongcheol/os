package driver

type IDriver interface {
	Alefaso()
	Avereno() int
	Atsaharo()
}

type TDriverMpandrindra struct {
}

var idriver [256]IDriver
var numberdriver int

func (nytena *TDriverMpandrindra) Init() {
	numberdriver = 0
}

func (nytena *TDriverMpandrindra) Ampidirodriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (nytena *TDriverMpandrindra) Alefasoall() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Alefaso()
	}
}
