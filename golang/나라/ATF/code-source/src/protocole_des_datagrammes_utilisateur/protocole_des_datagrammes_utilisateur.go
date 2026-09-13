package protocole_des_datagrammes_utilisateur

import . "unsafe"
import . "console"
import . "utilitaire"
import . "mémoiregestionnaire"
import . "protocole_du_réseau_interconnecté_4"

var udpconsole = TConsole{}

type TUtilisateurdatagramprotocolenTêtebuffer struct {
	numéro_du_port_source	[2]byte
	numéro_du_port_destination	[2]byte

	durée		[2]byte
	checksum	[2]byte
}

var udpenTêteTaille uint32 = 8

type TEntête_des_datagrammes_utilisateur struct {
	numéro_du_port_source	uint16
	numéro_du_port_destination	uint16

	durée		uint16
	checksum	uint16
}

func (self *TEntête_des_datagrammes_utilisateur) Init(buffer_2 *TUtilisateurdatagramprotocolenTêtebuffer) {
	self.numéro_du_port_source = Tableautounsignedinteger16(buffer_2.numéro_du_port_source)
	self.numéro_du_port_destination = Tableautounsignedinteger16(buffer_2.numéro_du_port_destination)

	self.durée = Tableautounsignedinteger16(buffer_2.durée)
	self.checksum = Tableautounsignedinteger16(buffer_2.checksum)
}
func (self *TEntête_des_datagrammes_utilisateur) Ensemblebuffer(buffer_2 *TUtilisateurdatagramprotocolenTêtebuffer) {

	buffer_2.numéro_du_port_source = Unsignedinteger16totableau(self.numéro_du_port_source)
	buffer_2.numéro_du_port_destination = Unsignedinteger16totableau(self.numéro_du_port_destination)

	buffer_2.durée = Unsignedinteger16totableau(self.durée)
	buffer_2.checksum = Unsignedinteger16totableau(self.checksum)

}

type IUtilisateurdatagramprotocolhandler interface {
	Poignéeutilisateurdatagramprotocolmessage(priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur, données uintptr, taille uint16)
}

type TUtilisateurdatagramprotocolhandler struct {
}

func (self *TUtilisateurdatagramprotocolhandler) Init(backend TFournisseur_du_protocole_du_réseau_interconnecté) {
}
func (self *TUtilisateurdatagramprotocolhandler) Poignéeutilisateurdatagramprotocolmessage(priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur, données uintptr, taille uint16) {
}

type IUtilisateurdatagramprotocolpriseRéseau interface {
	Poignéeutilisateurdatagramprotocolmessage(données uintptr, taille uint16)
}
type TPoint_de_communication_des_datagrammes_utilisateur struct {
	distantportNombre	uint16
	distantip		uint32
	localeportNombre	uint16
	localeip		uint32

	listening	bool
}

var udpprovider TUtilisateurdatagramprotocolprovider
var udphandler IUtilisateurdatagramprotocolhandler

func (self *TPoint_de_communication_des_datagrammes_utilisateur) Tester() {
}
func (self *TPoint_de_communication_des_datagrammes_utilisateur) Init(pudpprovider TUtilisateurdatagramprotocolprovider, pudphandler IUtilisateurdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TPoint_de_communication_des_datagrammes_utilisateur) Poignéeutilisateurdatagramprotocolmessage(données uintptr, taille uint16) {
	if udphandler != nil {
		udphandler.Poignéeutilisateurdatagramprotocolmessage(self, données, taille)
	}
}
func (self *TPoint_de_communication_des_datagrammes_utilisateur) Envoyer(pdonnées []byte, taille uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(taille); i++ {
		buffer_2[i] = pdonnées[i]
	}
	var données = uintptr(Pointer(&buffer_2))
	udpprovider.Envoyer(self, données, taille)
}
func (self *TPoint_de_communication_des_datagrammes_utilisateur) Déconnecter() {
	udpprovider.Déconnecter(self)
}

type TUtilisateurdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TPoint_de_communication_des_datagrammes_utilisateur
var nombresockets int
var libreport uint16

func (self *TUtilisateurdatagramprotocolprovider) Init(pipprovider TFournisseur_du_protocole_du_réseau_interconnecté, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nombresockets = 0
	libreport = 1024
}
func (self *TUtilisateurdatagramprotocolprovider) Internetprotocolreceivewhen(sourceipaddressréseauoctetorder uint32, destinationipaddressréseauoctetorder uint32, internetprotocolpayload uintptr, taille uint32) bool {
	if taille < udpenTêteTaille {
		return false
	}

	var buffer_2 *TUtilisateurdatagramprotocolenTêtebuffer = (*TUtilisateurdatagramprotocolenTêtebuffer)(Pointer(internetprotocolpayload))
	var msg TEntête_des_datagrammes_utilisateur
	msg.Init(buffer_2)

	var priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur = nil

	for i := 0; i < nombresockets && priseRéseau == nil; i++ {
		if sockets[i].localeportNombre == msg.numéro_du_port_destination && sockets[i].localeip == destinationipaddressréseauoctetorder && sockets[i].listening == true {
			priseRéseau = &sockets[i]
			priseRéseau.listening = false
			priseRéseau.distantportNombre = msg.numéro_du_port_source
			priseRéseau.distantip = sourceipaddressréseauoctetorder
		} else if sockets[i].localeportNombre == msg.numéro_du_port_destination && sockets[i].localeip == destinationipaddressréseauoctetorder && sockets[i].distantportNombre == msg.numéro_du_port_source && sockets[i].distantip == sourceipaddressréseauoctetorder {
			priseRéseau = &sockets[i]

		}
	}

	msg.Ensemblebuffer(buffer_2)
	if priseRéseau != nil {
		priseRéseau.Poignéeutilisateurdatagramprotocolmessage(internetprotocolpayload+uintptr(udpenTêteTaille), uint16(taille-udpenTêteTaille))
	}

	return false
}

func (self *TUtilisateurdatagramprotocolprovider) Connecter(ip uint32, port uint16) *TPoint_de_communication_des_datagrammes_utilisateur {
	var mémoiregestionnaire = &TMémoiregestionnaire{}
	var priseRéseau = (*TPoint_de_communication_des_datagrammes_utilisateur)(mémoiregestionnaire.Allouer_la_mémoire(50))

	if priseRéseau != nil {

		priseRéseau.Init(*self, nil)
		priseRéseau.distantportNombre = port
		priseRéseau.distantip = ip
		priseRéseau.localeportNombre = libreport
		libreport++
		priseRéseau.localeip = uint32((*iphandler.Providerget()).Getipaddress())

		priseRéseau.distantportNombre = Unsignedinteger16r(priseRéseau.distantportNombre)
		priseRéseau.localeportNombre = Unsignedinteger16r(priseRéseau.localeportNombre)

		sockets[nombresockets] = *priseRéseau
		nombresockets++

	}
	return priseRéseau

}
func (self *TUtilisateurdatagramprotocolprovider) Listen(port uint16) *TPoint_de_communication_des_datagrammes_utilisateur {
	var priseRéseau = &TPoint_de_communication_des_datagrammes_utilisateur{}
	priseRéseau = nil
	if priseRéseau != nil {
		priseRéseau.Init(*self, nil)
		priseRéseau.listening = true
		priseRéseau.localeportNombre = port
		priseRéseau.localeip = uint32((*iphandler.Providerget()).Getipaddress())

		priseRéseau.localeportNombre = Unsignedinteger16r(priseRéseau.localeportNombre)
	}
	return priseRéseau
}
func (self *TUtilisateurdatagramprotocolprovider) Déconnecter(priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur) {
	for i := 0; i < nombresockets && priseRéseau == nil; i++ {
		if sockets[i] == *priseRéseau {
			nombresockets--
			sockets[i] = sockets[nombresockets]
			break
		}
	}
}
func (self *TUtilisateurdatagramprotocolprovider) Envoyer(priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur, pdonnées uintptr, taille uint16) {
	var totalDurée = uint32(taille) + udpenTêteTaille

	var buffer_2 [4096]byte

	var msgbuffer = (*TUtilisateurdatagramprotocolenTêtebuffer)(Pointer(&buffer_2))

	var msg = TEntête_des_datagrammes_utilisateur{}

	msg.numéro_du_port_source = priseRéseau.localeportNombre
	msg.numéro_du_port_destination = priseRéseau.distantportNombre
	msg.durée = Unsignedinteger16r(uint16(totalDurée))

	msg.checksum = 0x0
	msg.Ensemblebuffer(msgbuffer)

	var donnéesOctets [4096]byte = *(*[4096]byte)(Pointer(pdonnées))
	for i := 0; i < int(taille); i++ {
		buffer_2[int(udpenTêteTaille)+i] = donnéesOctets[i]
	}

	var données uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Envoyer(priseRéseau.distantip, 0x11, données, totalDurée)

}
func (self *TUtilisateurdatagramprotocolprovider) Relier(priseRéseau *TPoint_de_communication_des_datagrammes_utilisateur, handler *TUtilisateurdatagramprotocolhandler,) {
}
