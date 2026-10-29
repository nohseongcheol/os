/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package trame_du_réseau_à_support_partagé

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "utilitaire"

var ethernetconsole TConsole = TConsole{}

type TEthernettrameenTêtebuffer struct {
	destinationmacbe	[6]byte
	sourcemacbe		[6]byte
	ethernettypebe		[2]byte
}

var trameenTêteTaille int = 14

type TEntête_de_trame_du_réseau_à_support_partagé struct {
	destinationmacbe	uint64
	sourcemacbe		uint64
	ethernettypebe		uint16
}

func (self *TEntête_de_trame_du_réseau_à_support_partagé) Init(buffer_2 TEthernettrameenTêtebuffer) {
	self.destinationmacbe = (Tableautounsignedinteger48(buffer_2.destinationmacbe))
	self.sourcemacbe = (Tableautounsignedinteger48(buffer_2.sourcemacbe))
	self.ethernettypebe = (Tableautounsignedinteger16(buffer_2.ethernettypebe))

}
func (self *TEntête_de_trame_du_réseau_à_support_partagé) Ensemblebuffer(buffer_2 *TEthernettrameenTêtebuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48totableau(Unsignedinteger48r(self.destinationmacbe))
	buffer_2.sourcemacbe = Unsignedinteger48totableau(Unsignedinteger48r(self.sourcemacbe))
	buffer_2.ethernettypebe = Unsignedinteger16totableau(Unsignedinteger16r(self.ethernettypebe))
}

type IEthernettramehandler interface {
	Init(backend TFournisseur_de_trames_du_réseau_à_support_partagé)
	Ensemblehandler(handler IEthernettramehandler, ethernettype uint16)
	Ethernettramereceivewhen(donnéesPointeur uintptr, taille int) bool
	Envoyer(destinationmacbe uint64, donnéesPointeur uintptr, taille uint32)
	TrameEnvoyer(destinationmacbe uint64, ethernettypebe uint16, donnéesPointeur uintptr, taille uint32)
	Providerget() TFournisseur_de_trames_du_réseau_à_support_partagé
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernettramehandler struct {
}

var trame TEntête_de_trame_du_réseau_à_support_partagé
var Backend TFournisseur_de_trames_du_réseau_à_support_partagé
var handler_2 [65535]IEthernettramehandler
var efhandler *TEthernettramehandler = nil

func (self *TEthernettramehandler) Init(backend TFournisseur_de_trames_du_réseau_à_support_partagé) {
	Backend = backend
}

func (self *TEthernettramehandler) Ensemblehandler(handler IEthernettramehandler, pethernettype uint16) {
	handler_2[pethernettype] = handler
}
func (self *TEthernettramehandler) Ensemblebackend(backend TFournisseur_de_trames_du_réseau_à_support_partagé) {
	Backend = backend
}
func (self *TEthernettramehandler) Getbackend() TFournisseur_de_trames_du_réseau_à_support_partagé {
	return Backend
}
func (self *TEthernettramehandler) Ethernettramereceivewhen(donnéesPointeur uintptr, taille int) bool {
	ethernetconsole.MImprimer(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernettramehandler) Envoyer(destinationmacbe uint64, donnéesPointeur uintptr, taille uint32) {
	Backend.TrameEnvoyer(destinationmacbe, trame.ethernettypebe, donnéesPointeur, taille)
}
func (self *TEthernettramehandler) TrameEnvoyer(destinationmacbe uint64, ethernettypebe uint16, donnéesPointeur uintptr, taille uint32) {
	Backend.TrameEnvoyer(destinationmacbe, ethernettypebe, donnéesPointeur, taille)
}
func (self *TEthernettramehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernettramehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernettramehandler) Providerget() TFournisseur_de_trames_du_réseau_à_support_partagé {
	return Backend
}

type TEthernettramerawdonnéeshandler struct {
	TRawdonnéeshandler
}

var provider TFournisseur_de_trames_du_réseau_à_support_partagé

func (self *TEthernettramerawdonnéeshandler) Init(pprovider TFournisseur_de_trames_du_réseau_à_support_partagé, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernettramerawdonnéeshandler) Surrawdonnéesreceive(donnéesPointeur uintptr, taille int) bool {
	return provider.Surrawdonnéesreceive(donnéesPointeur, taille)
}
func (self *TEthernettramerawdonnéeshandler) Envoyer(donnéesPointeur uintptr, taille uint32) {
	provider.Envoyer(donnéesPointeur, taille)
}
func (self *TEthernettramerawdonnéeshandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernettramerawdonnéeshandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernettramerawdonnéeshandler) Providerget() TFournisseur_de_trames_du_réseau_à_support_partagé {
	return provider
}

type TFournisseur_de_trames_du_réseau_à_support_partagé struct {
	réseauCartes	Tamdam79c973
	handler_2	[65565]IEthernettramehandler
}

func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) Init(backend Tamdam79c973) {

	self.réseauCartes = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var nombre uint16 = 0

func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) Surrawdonnéesreceive(donnéesPointeur uintptr, taille int) bool {

	var buffer_2 *TEthernettrameenTêtebuffer = (*TEthernettrameenTêtebuffer)(Pointer(donnéesPointeur))
	var trame TEntête_de_trame_du_réseau_à_support_partagé = TEntête_de_trame_du_réseau_à_support_partagé{}
	trame.Init(*buffer_2)
	var reply bool = false

	if trame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(trame.destinationmacbe) == self.Getmacaddress() {
		if handler_2[trame.ethernettypebe] != nil {
			ethernetconsole.MImprimer(([]byte)("provider\n"))

			var référence_mémoire uintptr = uintptr(Pointer(donnéesPointeur)) + uintptr(trameenTêteTaille)
			reply = handler_2[trame.ethernettypebe].Ethernettramereceivewhen(référence_mémoire, taille-trameenTêteTaille)

		}
	}

	if reply {
		trame.destinationmacbe = trame.sourcemacbe
		trame.sourcemacbe = Unsignedinteger48r(self.Getmacaddress())
		trame.Ensemblebuffer(buffer_2)

	}

	ethernetconsole.MImprimerxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Imprimer(trame.sourcemacbe)
	ethernetconsole.MImprimer(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Imprimer(trame.destinationmacbe)
	ethernetconsole.MImprimer(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Imprimer(self.Getmacaddress())
	ethernetconsole.MImprimer(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Imprimer(trame.ethernettypebe)
	ethernetconsole.MImprimer(([]byte)("]"))

	return reply

}
func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) Envoyer(donnéesPointeur uintptr, taille uint32) {
	self.réseauCartes.Envoyer(donnéesPointeur, taille)
}
func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) TrameEnvoyer(destinationmacbe uint64, ethernettypebe uint16, donnéesPointeur uintptr, taille uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernettrameenTêtebuffer = (*TEthernettrameenTêtebuffer)(Pointer(&buffer2_2))

	var trame TEntête_de_trame_du_réseau_à_support_partagé = TEntête_de_trame_du_réseau_à_support_partagé{}
	trame.Init(*buffer_2)

	trame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	trame.sourcemacbe = Unsignedinteger48r(self.réseauCartes.Getmacaddress())
	trame.ethernettypebe = Unsignedinteger16r(ethernettypebe)

	trame.Ensemblebuffer(buffer_2)
	var source_2 [4096]byte = *(*([4096]byte))(Pointer(donnéesPointeur))

	var i uint32 = 0
	for i = 0; i < taille; i++ {
		buffer2_2[uint32(trameenTêteTaille)+i] = source_2[i]

	}

	var référence_mémoire uintptr = uintptr(Pointer(&buffer2_2))

	self.réseauCartes.Envoyer(référence_mémoire, taille+uint32(trameenTêteTaille))

}
func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) Getmacaddress() uint64 {
	return self.réseauCartes.Getmacaddress()
}
func (self *TFournisseur_de_trames_du_réseau_à_support_partagé) Getipaddress() uint64 {
	return self.réseauCartes.Getipaddress()
}
