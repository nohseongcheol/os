/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package driver

type IDriver interface {
	Aktifkan()
	AturUlang() int
	Matikan()
}

type TDrivermanager struct {
}

var idriver [256]IDriver
var nomordriver int

func (dirisendiri *TDrivermanager) Init() {
	nomordriver = 0
}

func (dirisendiri *TDrivermanager) Tambahdriver(driver_2 IDriver) {
	idriver[nomordriver] = driver_2
	nomordriver++
}
func (dirisendiri *TDrivermanager) AktifkanSemua() {
	for i := 0; i < nomordriver; i++ {
		idriver[i].Aktifkan()
	}
}
