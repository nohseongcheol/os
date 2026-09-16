/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktiviraj()
	Vratiizvorno() int
	Deaktiviraj()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var bROJdriver int

func (sam *TDrivermanager) Init() {
	bROJdriver = 0
}

func (sam *TDrivermanager) Dodajdriver(driver_2 IDriver) {
	idriver[bROJdriver] = driver_2
	bROJdriver++
}
func (sam *TDrivermanager) AktivirajSve() {
	for i := 0; i < bROJdriver; i++ {
		idriver[i].Aktiviraj()
	}
}
