package driver

type IDriver interface {
	Aktivizēt()
	Pārstatīt() int
	Deaktivizēt()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var skaitlisdriver int

func (pats *TDrivermanager) Init() {
	skaitlisdriver = 0
}

func (pats *TDrivermanager) Pievienotdriver(driver_2 IDriver) {
	idriver[skaitlisdriver] = driver_2
	skaitlisdriver++
}
func (pats *TDrivermanager) AktivizētVisi() {
	for i := 0; i < skaitlisdriver; i++ {
		idriver[i].Aktivizēt()
	}
}
