/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktiver()
	Nulstil() int
	Deaktiver()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var taldriver int

func (selv *TDrivermanager) Init() {
	taldriver = 0
}

func (selv *TDrivermanager) Tilføjdriver(driver_2 IDriver) {
	idriver[taldriver] = driver_2
	taldriver++
}
func (selv *TDrivermanager) AktiverAlle() {
	for i := 0; i < taldriver; i++ {
		idriver[i].Aktiver()
	}
}
