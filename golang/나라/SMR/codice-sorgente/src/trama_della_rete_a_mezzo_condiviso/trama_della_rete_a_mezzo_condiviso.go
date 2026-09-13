package trama_della_rete_a_mezzo_condiviso

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRiquadroheaderbuffer struct {
	destinazionemacbe	[6]byte
	originemacbe		[6]byte
	ethernetTipobe		[2]byte
}

var riquadroheaderDimensione int = 14

type TIntestazione_della_trama_di_rete_a_mezzo_condiviso struct {
	destinazionemacbe	uint64
	originemacbe		uint64
	ethernetTipobe		uint16
}

func (séstesso *TIntestazione_della_trama_di_rete_a_mezzo_condiviso) Init(buffer_2 TEthernetRiquadroheaderbuffer) {
	séstesso.destinazionemacbe = (Serietounsignedinteger48(buffer_2.destinazionemacbe))
	séstesso.originemacbe = (Serietounsignedinteger48(buffer_2.originemacbe))
	séstesso.ethernetTipobe = (Serietounsignedinteger16(buffer_2.ethernetTipobe))

}
func (séstesso *TIntestazione_della_trama_di_rete_a_mezzo_condiviso) Impostabuffer(buffer_2 *TEthernetRiquadroheaderbuffer) {
	buffer_2.destinazionemacbe = Unsignedinteger48toSerie(Unsignedinteger48r(séstesso.destinazionemacbe))
	buffer_2.originemacbe = Unsignedinteger48toSerie(Unsignedinteger48r(séstesso.originemacbe))
	buffer_2.ethernetTipobe = Unsignedinteger16toSerie(Unsignedinteger16r(séstesso.ethernetTipobe))
}

type IEthernetRiquadrohandler interface {
	Init(backend TFornitore_di_trame_di_rete_a_mezzo_condiviso)
	Impostahandler(handler IEthernetRiquadrohandler, ethernetTipo uint16)
	EthernetRiquadroreceivewhen(dataPuntatore uintptr, dimensione int) bool
	Spedisci(destinazionemacbe uint64, dataPuntatore uintptr, dimensione uint32)
	RiquadroSpedisci(destinazionemacbe uint64, ethernetTipobe uint16, dataPuntatore uintptr, dimensione uint32)
	Providerget() TFornitore_di_trame_di_rete_a_mezzo_condiviso
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRiquadrohandler struct {
}

var riquadro TIntestazione_della_trama_di_rete_a_mezzo_condiviso
var Backend TFornitore_di_trame_di_rete_a_mezzo_condiviso
var handler_2 [65535]IEthernetRiquadrohandler
var efhandler *TEthernetRiquadrohandler = nil

func (séstesso *TEthernetRiquadrohandler) Init(backend TFornitore_di_trame_di_rete_a_mezzo_condiviso) {
	Backend = backend
}

func (séstesso *TEthernetRiquadrohandler) Impostahandler(handler IEthernetRiquadrohandler, pethernetTipo uint16) {
	handler_2[pethernetTipo] = handler
}
func (séstesso *TEthernetRiquadrohandler) Impostabackend(backend TFornitore_di_trame_di_rete_a_mezzo_condiviso) {
	Backend = backend
}
func (séstesso *TEthernetRiquadrohandler) Getbackend() TFornitore_di_trame_di_rete_a_mezzo_condiviso {
	return Backend
}
func (séstesso *TEthernetRiquadrohandler) EthernetRiquadroreceivewhen(dataPuntatore uintptr, dimensione int) bool {
	ethernetconsole.MStampa(([]byte)("OnEtherFrameReceived"))
	return false
}
func (séstesso *TEthernetRiquadrohandler) Spedisci(destinazionemacbe uint64, dataPuntatore uintptr, dimensione uint32) {
	Backend.RiquadroSpedisci(destinazionemacbe, riquadro.ethernetTipobe, dataPuntatore, dimensione)
}
func (séstesso *TEthernetRiquadrohandler) RiquadroSpedisci(destinazionemacbe uint64, ethernetTipobe uint16, dataPuntatore uintptr, dimensione uint32) {
	Backend.RiquadroSpedisci(destinazionemacbe, ethernetTipobe, dataPuntatore, dimensione)
}
func (séstesso *TEthernetRiquadrohandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (séstesso *TEthernetRiquadrohandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (séstesso *TEthernetRiquadrohandler) Providerget() TFornitore_di_trame_di_rete_a_mezzo_condiviso {
	return Backend
}

type TEthernetRiquadrorawdatahandler struct {
	TRawdatahandler
}

var provider TFornitore_di_trame_di_rete_a_mezzo_condiviso

func (séstesso *TEthernetRiquadrorawdatahandler) Init(pprovider TFornitore_di_trame_di_rete_a_mezzo_condiviso, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (séstesso *TEthernetRiquadrorawdatahandler) Accesorawdatareceive(dataPuntatore uintptr, dimensione int) bool {
	return provider.Accesorawdatareceive(dataPuntatore, dimensione)
}
func (séstesso *TEthernetRiquadrorawdatahandler) Spedisci(dataPuntatore uintptr, dimensione uint32) {
	provider.Spedisci(dataPuntatore, dimensione)
}
func (séstesso *TEthernetRiquadrorawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (séstesso *TEthernetRiquadrorawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (séstesso *TEthernetRiquadrorawdatahandler) Providerget() TFornitore_di_trame_di_rete_a_mezzo_condiviso {
	return provider
}

type TFornitore_di_trame_di_rete_a_mezzo_condiviso struct {
	reteCarte	Tamdam79c973
	handler_2	[65565]IEthernetRiquadrohandler
}

func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) Init(backend Tamdam79c973) {

	séstesso.reteCarte = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		séstesso.handler_2[i] = nil
	}
}

var conteggio uint16 = 0

func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) Accesorawdatareceive(dataPuntatore uintptr, dimensione int) bool {

	var buffer_2 *TEthernetRiquadroheaderbuffer = (*TEthernetRiquadroheaderbuffer)(Pointer(dataPuntatore))
	var riquadro TIntestazione_della_trama_di_rete_a_mezzo_condiviso = TIntestazione_della_trama_di_rete_a_mezzo_condiviso{}
	riquadro.Init(*buffer_2)
	var reply bool = false

	if riquadro.destinazionemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(riquadro.destinazionemacbe) == séstesso.Getmacaddress() {
		if handler_2[riquadro.ethernetTipobe] != nil {
			ethernetconsole.MStampa(([]byte)("provider\n"))

			var riferimento_di_memoria uintptr = uintptr(Pointer(dataPuntatore)) + uintptr(riquadroheaderDimensione)
			reply = handler_2[riquadro.ethernetTipobe].EthernetRiquadroreceivewhen(riferimento_di_memoria, dimensione-riquadroheaderDimensione)

		}
	}

	if reply {
		riquadro.destinazionemacbe = riquadro.originemacbe
		riquadro.originemacbe = Unsignedinteger48r(séstesso.Getmacaddress())
		riquadro.Impostabuffer(buffer_2)

	}

	ethernetconsole.MStampaxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Stampa(riquadro.originemacbe)
	ethernetconsole.MStampa(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Stampa(riquadro.destinazionemacbe)
	ethernetconsole.MStampa(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Stampa(séstesso.Getmacaddress())
	ethernetconsole.MStampa(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Stampa(riquadro.ethernetTipobe)
	ethernetconsole.MStampa(([]byte)("]"))

	return reply

}
func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) Spedisci(dataPuntatore uintptr, dimensione uint32) {
	séstesso.reteCarte.Spedisci(dataPuntatore, dimensione)
}
func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) RiquadroSpedisci(destinazionemacbe uint64, ethernetTipobe uint16, dataPuntatore uintptr, dimensione uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRiquadroheaderbuffer = (*TEthernetRiquadroheaderbuffer)(Pointer(&buffer2_2))

	var riquadro TIntestazione_della_trama_di_rete_a_mezzo_condiviso = TIntestazione_della_trama_di_rete_a_mezzo_condiviso{}
	riquadro.Init(*buffer_2)

	riquadro.destinazionemacbe = Unsignedinteger48r(destinazionemacbe)
	riquadro.originemacbe = Unsignedinteger48r(séstesso.reteCarte.Getmacaddress())
	riquadro.ethernetTipobe = Unsignedinteger16r(ethernetTipobe)

	riquadro.Impostabuffer(buffer_2)
	var origine_2 [4096]byte = *(*([4096]byte))(Pointer(dataPuntatore))

	var i uint32 = 0
	for i = 0; i < dimensione; i++ {
		buffer2_2[uint32(riquadroheaderDimensione)+i] = origine_2[i]

	}

	var riferimento_di_memoria uintptr = uintptr(Pointer(&buffer2_2))

	séstesso.reteCarte.Spedisci(riferimento_di_memoria, dimensione+uint32(riquadroheaderDimensione))

}
func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) Getmacaddress() uint64 {
	return séstesso.reteCarte.Getmacaddress()
}
func (séstesso *TFornitore_di_trame_di_rete_a_mezzo_condiviso) Getipaddress() uint64 {
	return séstesso.reteCarte.Getipaddress()
}
