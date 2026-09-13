package driver

type IDriver interface {
	Activeren()
	Terugzetten() int
	Deactiveren()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var getaldriver int

func (zelf *TDrivermanager) Init() {
	getaldriver = 0
}

func (zelf *TDrivermanager) Toevoegendriver(driver_2 IDriver) {
	idriver[getaldriver] = driver_2
	getaldriver++
}
func (zelf *TDrivermanager) ActiverenAlle() {
	for i := 0; i < getaldriver; i++ {
		idriver[i].Activeren()
	}
}
