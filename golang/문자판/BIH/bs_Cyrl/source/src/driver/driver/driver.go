/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktiviraj()
	Resetuj() int
	Deaktiviraj()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var brojdriver int

func (self *TDrivermanager) Init() {
	brojdriver = 0
}

func (self *TDrivermanager) Dodajdriver(driver_2 IDriver) {
	idriver[brojdriver] = driver_2
	brojdriver++
}
func (self *TDrivermanager) AktivirajSve() {
	for i := 0; i < brojdriver; i++ {
		idriver[i].Aktiviraj()
	}
}
