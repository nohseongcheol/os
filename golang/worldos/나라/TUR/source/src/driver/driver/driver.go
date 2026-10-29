/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
