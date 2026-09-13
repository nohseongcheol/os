package driver

type IDriver interface {
	Activate()
	Түшүрүү() int
	Deactivate()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var нОМЕРdriver int

func (self *TDrivermanager) Init() {
	нОМЕРdriver = 0
}

func (self *TDrivermanager) Кошууdriver(driver_2 IDriver) {
	idriver[нОМЕРdriver] = driver_2
	нОМЕРdriver++
}
func (self *TDrivermanager) Activateall() {
	for i := 0; i < нОМЕРdriver; i++ {
		idriver[i].Activate()
	}
}
