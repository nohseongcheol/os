package driver

type IDriver interface {
	Aktivovať()
	Reštartovať() int
	Deaktivovať()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var číslodriver int

func (vlastný *TDrivermanager) Init() {
	číslodriver = 0
}

func (vlastný *TDrivermanager) Pridaťdriver(driver_2 IDriver) {
	idriver[číslodriver] = driver_2
	číslodriver++
}
func (vlastný *TDrivermanager) AktivovaťVšetky() {
	for i := 0; i < číslodriver; i++ {
		idriver[i].Aktivovať()
	}
}
