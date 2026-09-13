package driver

type IDriver interface {
	Pokreni()
	Ponovopostavi() int
	Obustavi()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var бројdriver int

func (isti *TDrivermanager) Init() {
	бројdriver = 0
}

func (isti *TDrivermanager) Додајdriver(driver_2 IDriver) {
	idriver[бројdriver] = driver_2
	бројdriver++
}
func (isti *TDrivermanager) PokreniSve() {
	for i := 0; i < бројdriver; i++ {
		idriver[i].Pokreni()
	}
}
