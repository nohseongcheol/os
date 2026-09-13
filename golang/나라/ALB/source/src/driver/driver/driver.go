package driver

type IDriver interface {
	Aktivo()
	Ngafillimi() int
	Çaktivo()
}

type TDriverManazhuesi struct {
}

var idriver [256]IDriver
var numberdriver int

func (vetvetja *TDriverManazhuesi) Init() {
	numberdriver = 0
}

func (vetvetja *TDriverManazhuesi) Shtodriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (vetvetja *TDriverManazhuesi) Aktivokrejt() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Aktivo()
	}
}
