package driver

type IDriver interface {
	Virkja()
	Frumstilla() int
	Afvirkja()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (sjálft *TDrivermanager) Init() {
	numberdriver = 0
}

func (sjálft *TDrivermanager) Bætaviðdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (sjálft *TDrivermanager) VirkjaAllt() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Virkja()
	}
}
