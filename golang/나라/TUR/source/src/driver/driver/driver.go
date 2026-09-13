package driver

type IDriver interface {
	Etkinleştir()
	Sıfırla() int
	Etkisizleştir()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var sayıdriver int

func (self *TDrivermanager) Init() {
	sayıdriver = 0
}

func (self *TDrivermanager) Ekledriver(driver_2 IDriver) {
	idriver[sayıdriver] = driver_2
	sayıdriver++
}
func (self *TDrivermanager) EtkinleştirHepsi() {
	for i := 0; i < sayıdriver; i++ {
		idriver[i].Etkinleştir()
	}
}
