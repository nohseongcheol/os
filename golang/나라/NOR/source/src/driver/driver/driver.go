package driver

type IDriver interface {
	Aktiver()
	Nullstill() int
	Deaktiver()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var talldriver int

func (selv *TDrivermanager) Init() {
	talldriver = 0
}

func (selv *TDrivermanager) Leggtildriver(driver_2 IDriver) {
	idriver[talldriver] = driver_2
	talldriver++
}
func (selv *TDrivermanager) AktiverAlle() {
	for i := 0; i < talldriver; i++ {
		idriver[i].Aktiver()
	}
}
