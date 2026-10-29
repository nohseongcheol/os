/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package frame_van_het_gedeelde_medium_netwerk

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	bestemmingmacbe	[6]byte
	bronmacbe	[6]byte
	ethernetSoortbe	[2]byte
}

var frameheaderGrootte int = 14

type TFramekop_van_het_gedeelde_medium_netwerk struct {
	bestemmingmacbe	uint64
	bronmacbe	uint64
	ethernetSoortbe	uint16
}

func (zelf *TFramekop_van_het_gedeelde_medium_netwerk) Init(buffer_2 TEthernetframeheaderbuffer) {
	zelf.bestemmingmacbe = (Reeksnaarunsignedinteger48(buffer_2.bestemmingmacbe))
	zelf.bronmacbe = (Reeksnaarunsignedinteger48(buffer_2.bronmacbe))
	zelf.ethernetSoortbe = (Reeksnaarunsignedinteger16(buffer_2.ethernetSoortbe))

}
func (zelf *TFramekop_van_het_gedeelde_medium_netwerk) Instellenbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.bestemmingmacbe = Unsignedinteger48naarReeks(Unsignedinteger48r(zelf.bestemmingmacbe))
	buffer_2.bronmacbe = Unsignedinteger48naarReeks(Unsignedinteger48r(zelf.bronmacbe))
	buffer_2.ethernetSoortbe = Unsignedinteger16naarReeks(Unsignedinteger16r(zelf.ethernetSoortbe))
}

type IEthernetframehandler interface {
	Init(backend TFrameleverancier_van_het_gedeelde_medium_netwerk)
	Instellenhandler(handler IEthernetframehandler, ethernetSoort uint16)
	Ethernetframereceivewhen(dataMuisaanwijzer uintptr, grootte int) bool
	Verzenden(bestemmingmacbe uint64, dataMuisaanwijzer uintptr, grootte uint32)
	FrameVerzenden(bestemmingmacbe uint64, ethernetSoortbe uint16, dataMuisaanwijzer uintptr, grootte uint32)
	Providerget() TFrameleverancier_van_het_gedeelde_medium_netwerk
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetframehandler struct {
}

var frame TFramekop_van_het_gedeelde_medium_netwerk
var Backend TFrameleverancier_van_het_gedeelde_medium_netwerk
var handler_2 [65535]IEthernetframehandler
var efhandler *TEthernetframehandler = nil

func (zelf *TEthernetframehandler) Init(backend TFrameleverancier_van_het_gedeelde_medium_netwerk) {
	Backend = backend
}

func (zelf *TEthernetframehandler) Instellenhandler(handler IEthernetframehandler, pethernetSoort uint16) {
	handler_2[pethernetSoort] = handler
}
func (zelf *TEthernetframehandler) Instellenbackend(backend TFrameleverancier_van_het_gedeelde_medium_netwerk) {
	Backend = backend
}
func (zelf *TEthernetframehandler) Getbackend() TFrameleverancier_van_het_gedeelde_medium_netwerk {
	return Backend
}
func (zelf *TEthernetframehandler) Ethernetframereceivewhen(dataMuisaanwijzer uintptr, grootte int) bool {
	ethernetconsole.MAfdrukken(([]byte)("OnEtherFrameReceived"))
	return false
}
func (zelf *TEthernetframehandler) Verzenden(bestemmingmacbe uint64, dataMuisaanwijzer uintptr, grootte uint32) {
	Backend.FrameVerzenden(bestemmingmacbe, frame.ethernetSoortbe, dataMuisaanwijzer, grootte)
}
func (zelf *TEthernetframehandler) FrameVerzenden(bestemmingmacbe uint64, ethernetSoortbe uint16, dataMuisaanwijzer uintptr, grootte uint32) {
	Backend.FrameVerzenden(bestemmingmacbe, ethernetSoortbe, dataMuisaanwijzer, grootte)
}
func (zelf *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (zelf *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (zelf *TEthernetframehandler) Providerget() TFrameleverancier_van_het_gedeelde_medium_netwerk {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TFrameleverancier_van_het_gedeelde_medium_netwerk

func (zelf *TEthernetframerawdatahandler) Init(pprovider TFrameleverancier_van_het_gedeelde_medium_netwerk, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (zelf *TEthernetframerawdatahandler) Aanrawdatareceive(dataMuisaanwijzer uintptr, grootte int) bool {
	return provider.Aanrawdatareceive(dataMuisaanwijzer, grootte)
}
func (zelf *TEthernetframerawdatahandler) Verzenden(dataMuisaanwijzer uintptr, grootte uint32) {
	provider.Verzenden(dataMuisaanwijzer, grootte)
}
func (zelf *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (zelf *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (zelf *TEthernetframerawdatahandler) Providerget() TFrameleverancier_van_het_gedeelde_medium_netwerk {
	return provider
}

type TFrameleverancier_van_het_gedeelde_medium_netwerk struct {
	netwerkKaart	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) Init(backend Tamdam79c973) {

	zelf.netwerkKaart = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		zelf.handler_2[i] = nil
	}
}

var aantal uint16 = 0

func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) Aanrawdatareceive(dataMuisaanwijzer uintptr, grootte int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(dataMuisaanwijzer))
	var frame TFramekop_van_het_gedeelde_medium_netwerk = TFramekop_van_het_gedeelde_medium_netwerk{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.bestemmingmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.bestemmingmacbe) == zelf.Getmacaddress() {
		if handler_2[frame.ethernetSoortbe] != nil {
			ethernetconsole.MAfdrukken(([]byte)("provider\n"))

			var adresverwijzing uintptr = uintptr(Pointer(dataMuisaanwijzer)) + uintptr(frameheaderGrootte)
			reply = handler_2[frame.ethernetSoortbe].Ethernetframereceivewhen(adresverwijzing, grootte-frameheaderGrootte)

		}
	}

	if reply {
		frame.bestemmingmacbe = frame.bronmacbe
		frame.bronmacbe = Unsignedinteger48r(zelf.Getmacaddress())
		frame.Instellenbuffer(buffer_2)

	}

	ethernetconsole.MAfdrukkenxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Afdrukken(frame.bronmacbe)
	ethernetconsole.MAfdrukken(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Afdrukken(frame.bestemmingmacbe)
	ethernetconsole.MAfdrukken(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Afdrukken(zelf.Getmacaddress())
	ethernetconsole.MAfdrukken(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Afdrukken(frame.ethernetSoortbe)
	ethernetconsole.MAfdrukken(([]byte)("]"))

	return reply

}
func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) Verzenden(dataMuisaanwijzer uintptr, grootte uint32) {
	zelf.netwerkKaart.Verzenden(dataMuisaanwijzer, grootte)
}
func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) FrameVerzenden(bestemmingmacbe uint64, ethernetSoortbe uint16, dataMuisaanwijzer uintptr, grootte uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TFramekop_van_het_gedeelde_medium_netwerk = TFramekop_van_het_gedeelde_medium_netwerk{}
	frame.Init(*buffer_2)

	frame.bestemmingmacbe = Unsignedinteger48r(bestemmingmacbe)
	frame.bronmacbe = Unsignedinteger48r(zelf.netwerkKaart.Getmacaddress())
	frame.ethernetSoortbe = Unsignedinteger16r(ethernetSoortbe)

	frame.Instellenbuffer(buffer_2)
	var bron_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuisaanwijzer))

	var i uint32 = 0
	for i = 0; i < grootte; i++ {
		buffer2_2[uint32(frameheaderGrootte)+i] = bron_2[i]

	}

	var adresverwijzing uintptr = uintptr(Pointer(&buffer2_2))

	zelf.netwerkKaart.Verzenden(adresverwijzing, grootte+uint32(frameheaderGrootte))

}
func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) Getmacaddress() uint64 {
	return zelf.netwerkKaart.Getmacaddress()
}
func (zelf *TFrameleverancier_van_het_gedeelde_medium_netwerk) Getipaddress() uint64 {
	return zelf.netwerkKaart.Getipaddress()
}
