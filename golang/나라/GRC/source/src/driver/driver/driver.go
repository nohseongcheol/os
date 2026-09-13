package driver

type IDriver interface {
	Ενεργοποίηση()
	Επαναφορά() int
	Απενεργοποίηση()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var αριθμόςdriver int

func (self *TDrivermanager) Init() {
	αριθμόςdriver = 0
}

func (self *TDrivermanager) Προσθήκηdriver(driver_2 IDriver) {
	idriver[αριθμόςdriver] = driver_2
	αριθμόςdriver++
}
func (self *TDrivermanager) ΕνεργοποίησηΌλα() {
	for i := 0; i < αριθμόςdriver; i++ {
		idriver[i].Ενεργοποίηση()
	}
}
