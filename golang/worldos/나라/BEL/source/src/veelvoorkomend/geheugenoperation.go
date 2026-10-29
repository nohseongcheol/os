/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package veelvoorkomend

type Geheugenoper struct {
}

func (zelf *Geheugenoper) MemInstellen(bufferMuisaanwijzer uintptr, waarde byte, grootte uint32) uintptr {
	return bufferMuisaanwijzer
}
func (zelf *Geheugenoper) MemVerplaatsen(bestemmingMuisaanwijzer_2 uintptr, srcptr uintptr, grootte uint32) uintptr {
	return bestemmingMuisaanwijzer_2
}

func (zelf *Geheugenoper) MemKopiëren(bestemmingMuisaanwijzer_2 uintptr, srcptr uintptr, grootte uint32) uintptr {
	return bestemmingMuisaanwijzer_2
}
func (zelf *Geheugenoper) Memcmp(bestemmingMuisaanwijzer_2 uintptr, srcptr uintptr, grootte uint32) bool {
	return true
}
