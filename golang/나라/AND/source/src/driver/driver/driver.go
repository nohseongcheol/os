package driver

type IDriver interface {
	Activa()
	Restableix() int
	Desactiva()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var nombredriver int

func (unmateix *TDrivermanager) Init() {
	nombredriver = 0
}

func (unmateix *TDrivermanager) Afegeixdriver(driver_2 IDriver) {
	idriver[nombredriver] = driver_2
	nombredriver++
}
func (unmateix *TDrivermanager) ActivaTot() {
	for i := 0; i < nombredriver; i++ {
		idriver[i].Activa()
	}
}
