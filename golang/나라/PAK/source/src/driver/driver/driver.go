package driver

type IDriver interface {
	Aفعالکریں()
	Rازسرنوتعینکریں() int
	Dغیرفعالکریں()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numberdriver int

func (self *TDrivermanager) Init() {
	numberdriver = 0
}

func (self *TDrivermanager) Aشاملکریںdriver(driver_2 IDriver) {
	idriver[numberdriver] = driver_2
	numberdriver++
}
func (self *TDrivermanager) Aفعالکریںتمام() {
	for i := 0; i < numberdriver; i++ {
		idriver[i].Aفعالکریں()
	}
}
