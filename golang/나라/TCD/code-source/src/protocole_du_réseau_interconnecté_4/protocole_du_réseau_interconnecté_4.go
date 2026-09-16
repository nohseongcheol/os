/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocole_du_réseau_interconnecté_4

import . "unsafe"
import . "utilitaire"
import . "console"
import . "trame_du_réseau_à_support_partagé"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4messagebuffer struct {
	lenver		byte
	tos		byte
	totalDurée	[2]byte

	ident			[2]byte
	attributsetDécalage	[2]byte

	heuretolive	byte
	protocol	byte
	checksum	[2]byte

	sourceipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipTaille uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4message struct {
	enTêteDurée	uint8
	version		uint8
	tos		uint8
	totalDurée	uint16

	ident			uint16
	attributsetDécalage	uint16

	heuretolive	uint8
	protocol	uint8
	checksum	uint16

	sourceipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4message) Init(buffer_2 TInternetprotocolv4messagebuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.enTêteDurée = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.totalDurée = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.totalDurée))

	self.ident = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.ident))
	self.attributsetDécalage = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.attributsetDécalage))

	self.heuretolive = buffer_2.heuretolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.checksum))

	self.sourceipaddress = Unsignedinteger32r(Tableautounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationipaddress = Unsignedinteger32r(Tableautounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4message) Ensemblebuffer(buffer_2 *TInternetprotocolv4messagebuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.enTêteDurée & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.totalDurée = Unsignedinteger16totableau(self.totalDurée)

	buffer_2.ident = Unsignedinteger16totableau(self.ident)
	buffer_2.attributsetDécalage = Unsignedinteger16totableau(self.attributsetDécalage)

	buffer_2.heuretolive = self.heuretolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16totableau(self.checksum)

	buffer_2.sourceipaddress = Unsignedinteger32totableau(self.sourceipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32totableau(self.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TFournisseur_du_protocole_du_réseau_interconnecté, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sourceipaddressréseauoctetorder uint32, destinationipaddressréseauoctetorder uint32, donnéesPointeur uintptr, taille uint32) bool
	Envoyer(destinationipaddressréseauoctetorder uint32, pprotocol uint8, donnéesPointeur uintptr, taille uint32)
	Providerget() *TFournisseur_du_protocole_du_réseau_interconnecté
}

type TInternetprotocolhandler struct {
}

var ipethernettramehandler Ipethernettramehandler = Ipethernettramehandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TFournisseur_du_protocole_du_réseau_interconnecté, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(sourceipaddressréseauoctetorder uint32, destinationipaddressréseauoctetorder uint32, donnéesPointeur uintptr, taille uint32) bool {
	ipconsole.MImprimer(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Envoyer(destinationipaddressréseauoctetorder uint32, pprotocol uint8, donnéesPointeur uintptr, taille uint32) {

	fournisseur_du_protocole_du_réseau_interconnecté.Envoyer(destinationipaddressréseauoctetorder, pprotocol, donnéesPointeur, taille)
}
func (self *TInternetprotocolhandler) Providerget() *TFournisseur_du_protocole_du_réseau_interconnecté {
	return &fournisseur_du_protocole_du_réseau_interconnecté
}

type Ipethernettramehandler struct {
	TEthernettramehandler
}

var fournisseur_du_protocole_du_réseau_interconnecté TFournisseur_du_protocole_du_réseau_interconnecté

func (self *Ipethernettramehandler) Ethernettramereceivewhen(donnéesPointeur uintptr, taille int) bool {
	ipconsole.MImprimer(([]byte)("iphandler:onEtherfameRecv\n"))
	return fournisseur_du_protocole_du_réseau_interconnecté.Ethernettramereceivewhen(donnéesPointeur, uint32(taille))

}

func (self *Ipethernettramehandler) Envoyer(destinationipaddressréseauoctetorder uint64, donnéesPointeur uintptr, taille uint32) {
	ipconsole.MImprimer(([]byte)("ipefhandler:send\n"))
	var ethernettypebe = Unsignedinteger16r(0x0800)
	self.TEthernettramehandler.TrameEnvoyer(destinationipaddressréseauoctetorder, ethernettypebe, donnéesPointeur, taille)

}

var handler_2 [255]IInternetprotocolhandler

type TFournisseur_du_protocole_du_réseau_interconnecté struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMasque	uint32
}

var efhandler IEthernettramehandler

func (self *TFournisseur_du_protocole_du_réseau_interconnecté) Init(pefprovider TFournisseur_de_trames_du_réseau_à_support_partagé, pefhandler IEthernettramehandler, arp Arpprovider, gatewayip uint32, subnetMasque uint32) {

	efhandler = pefhandler
	efhandler.Ensemblehandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetMasque = subnetMasque
	fournisseur_du_protocole_du_réseau_interconnecté = *self
}
func (self *TFournisseur_du_protocole_du_réseau_interconnecté) Ethernettramereceivewhen(ethernettramepayload uintptr, taille uint32) bool {
	if taille < uint32(ipTaille) {
		return false
	}

	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(ethernettramepayload))
	var internetprotocolmessage TInternetprotocolv4message
	internetprotocolmessage.Init(*buffer_2)

	var reply bool = false

	if internetprotocolmessage.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var durée uint32 = uint32(internetprotocolmessage.totalDurée)
		if durée > taille {
			durée = taille
		}
		if handler_2[internetprotocolmessage.protocol] != nil {
			reply = handler_2[internetprotocolmessage.protocol].Internetprotocolreceivewhen(internetprotocolmessage.sourceipaddress, internetprotocolmessage.destinationipaddress, ethernettramepayload+uintptr(4*internetprotocolmessage.enTêteDurée), uint32(durée-uint32(4*internetprotocolmessage.enTêteDurée)))

		}
	}

	if reply {

		var temporary = internetprotocolmessage.destinationipaddress
		internetprotocolmessage.destinationipaddress = internetprotocolmessage.sourceipaddress
		internetprotocolmessage.sourceipaddress = temporary

		internetprotocolmessage.heuretolive = 0x40
		internetprotocolmessage.checksum = 0

		internetprotocolmessage.Ensemblebuffer(buffer_2)
		internetprotocolmessage.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernettramepayload)), uint32(4*internetprotocolmessage.enTêteDurée))

		internetprotocolmessage.Ensemblebuffer(buffer_2)

	}

	ipconsole.MImprimer(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Imprimer(internetprotocolmessage.sourceipaddress)
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MUnsignedinteger32Imprimer(internetprotocolmessage.destinationipaddress)
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimer(uint16(internetprotocolmessage.enTêteDurée))
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimer(uint16(internetprotocolmessage.version))
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MUnsignedinteger16Imprimer(internetprotocolmessage.totalDurée)
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MUnsignedinteger32Imprimer(uint32(efhandler.Getipaddress()))
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MImprimer(([]byte)("\n"))

	return reply

}
func (self *TFournisseur_du_protocole_du_réseau_interconnecté) Envoyer(destinationipaddressréseauoctetorder uint32, protocol uint8, donnéesPointeur uintptr, taille uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(&buffer1_2))
	var message TInternetprotocolv4message = TInternetprotocolv4message{}
	message.version = 4
	message.enTêteDurée = ipTaille / 4
	message.tos = 0
	message.totalDurée = Unsignedinteger16r(uint16(taille + uint32(ipTaille)))

	message.ident = 0x0100
	message.attributsetDécalage = 0x0040
	message.heuretolive = 0x40
	message.protocol = protocol

	message.destinationipaddress = destinationipaddressréseauoctetorder

	message.sourceipaddress = uint32(efhandler.Getipaddress())

	message.checksum = 0

	message.Ensemblebuffer(buffer_2)
	message.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipTaille))
	message.Ensemblebuffer(buffer_2)

	var donnéesbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(donnéesPointeur))

	for i := 0; i < int(taille); i++ {

		buffer1_2[i+int(ipTaille)] = donnéesbuffer_2[i]
	}

	ipconsole.MImprimerxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(taille)+int(ipTaille); i++ {
		ipconsole.MHexadecimalImprimer(buffer1_2[i])
	}
	ipconsole.MImprimer(([]byte)(":"))
	ipconsole.MImprimer(([]byte)("]\n"))

	var suivanthopipaddressréseauoctetorder uint32 = destinationipaddressréseauoctetorder
	if (destinationipaddressréseauoctetorder & self.SubnetMasque) != (message.sourceipaddress & self.SubnetMasque) {
		suivanthopipaddressréseauoctetorder = self.Gatewayip
	}

	var envoyerdonnéesPointeur = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Imprimer(suivanthopipaddressréseauoctetorder)

	var ethernettypebe = Unsignedinteger16r(0x0800)
	efhandler.TrameEnvoyer(self.arpprovider.Résoudre(suivanthopipaddressréseauoctetorder), ethernettypebe, envoyerdonnéesPointeur, uint32(ipTaille)+uint32(taille))

}
func (self *TFournisseur_du_protocole_du_réseau_interconnecté) Checksum(pdonnées *[4096]uint16, duréeEntranteOctets uint32) uint16 {
	var données [4096]uint16 = *pdonnées
	var temporary uint32 = 0
	var donnéesOctets [4096]byte = *(*([4096]byte))(Pointer(&données))
	if (duréeEntranteOctets % 2) != 0 {
		temporary += uint32(uint16(donnéesOctets[duréeEntranteOctets-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TFournisseur_du_protocole_du_réseau_interconnecté) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
