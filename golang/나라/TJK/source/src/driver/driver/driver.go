package driver

type IDriver interface {
	Activate()
	Бозсозӣ() int
	Deactivate()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (self *TDrivermanager) Init() {
	numberdriver = 0
}

func (self *TDrivermanager) Adddriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (self *TDrivermanager) ActivateҲама() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Activate()
	}
}
