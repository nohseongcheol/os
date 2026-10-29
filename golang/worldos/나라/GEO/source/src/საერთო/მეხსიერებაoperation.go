/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package საერთო

type Mმეხსიერებაoper struct {
}

func (self *Mმეხსიერებაoper) Memset(bufferკურსორი uintptr, მნიშვნელობა byte, ზომა uint32) uintptr {
	return bufferკურსორი
}
func (self *Mმეხსიერებაoper) Memგადაადგილება(destinationკურსორი_2 uintptr, srcptr uintptr, ზომა uint32) uintptr {
	return destinationკურსორი_2
}

func (self *Mმეხსიერებაoper) Memდააკოპირე(destinationკურსორი_2 uintptr, srcptr uintptr, ზომა uint32) uintptr {
	return destinationკურსორი_2
}
func (self *Mმეხსიერებაoper) Memcmp(destinationკურსორი_2 uintptr, srcptr uintptr, ზომა uint32) bool {
	return true
}
