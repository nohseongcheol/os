package driver

type IDriver interface {
	Activate()
	Reset() int
	Deactivate()
}

type TDriverManager struct {
}

var iDrivers [256]IDriver
var numDrivers int

func (self *TDriverManager) Vప్రారంభించు() {
	numDrivers = 0
}

func (self *TDriverManager) AddDriver(drv IDriver) {
	iDrivers[numDrivers] = drv
	numDrivers++
}
func (self *TDriverManager) ActivateAll() {
	for i := 0; i < numDrivers; i++ {
		iDrivers[i].Activate()
	}
}
