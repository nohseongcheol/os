package driver

type IDriver interface {
	Aktifkan()
	TetapSemula() int
	Nyahaktifkan()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var nOMBORdriver int

func (diri *TDrivermanager) Init() {
	nOMBORdriver = 0
}

func (diri *TDrivermanager) Tambahdriver(driver_2 IDriver) {
	idriver[nOMBORdriver] = driver_2
	nOMBORdriver++
}
func (diri *TDrivermanager) AktifkanSemua() {
	for i := 0; i < nOMBORdriver; i++ {
		idriver[i].Aktifkan()
	}
}
