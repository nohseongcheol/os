/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Activează()
	Restabilește() int
	Dezactivează()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var numărdriver int

func (sine *TDrivermanager) Init() {
	numărdriver = 0
}

func (sine *TDrivermanager) Adaugădriver(driver_2 IDriver) {
	idriver[numărdriver] = driver_2
	numărdriver++
}
func (sine *TDrivermanager) ActiveazăToate() {
	for i := 0; i < numărdriver; i++ {
		idriver[i].Activează()
	}
}
