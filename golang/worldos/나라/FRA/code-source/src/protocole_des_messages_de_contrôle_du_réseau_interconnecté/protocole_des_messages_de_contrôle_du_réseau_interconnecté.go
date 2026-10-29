/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocole_des_messages_de_contrôle_du_réseau_interconnecté

import . "unsafe"
import . "console"
import . "mémoiregestionnaire"
import . "trame_du_réseau_à_support_partagé"
import . "protocole_du_réseau_interconnecté_4"
import . "utilitaire"

var icmpconsole = TConsole{}

type TInternetCtrlmessageprotocolmessagebuffer struct {
	TypeValeur	byte
	code		byte

	checksum	[2]byte
	données		[4]byte
}

var icmpTaille int = 64

type TInternetCtrlmessageprotocolmessage struct {
	TypeValeur	uint8
	code		uint8

	checksum	uint16
	données		uint32
}

func (self *TInternetCtrlmessageprotocolmessage) Init(buffer_2 TInternetCtrlmessageprotocolmessagebuffer) {
	self.TypeValeur = buffer_2.TypeValeur
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.checksum))
	self.données = Unsignedinteger32r(Tableautounsignedinteger32(buffer_2.données))
}

func (self *TInternetCtrlmessageprotocolmessage) Ensemblebuffer(buffer_2 *TInternetCtrlmessageprotocolmessagebuffer) {
	buffer_2.TypeValeur = self.TypeValeur
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16totableau(self.checksum)
	buffer_2.données = Unsignedinteger32totableau(self.données)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protocole_des_messages_de_contrôle_du_réseau_interconnecté *TProtocole_des_messages_de_contrôle_du_réseau_interconnecté

func (self *Icmphandler) Internetprotocolreceivewhen(sourceipaddressréseauoctetorder uint32, destinationipaddressréseauoctetorder uint32, donnéesPointeur uintptr, taille uint32) bool {
	return protocole_des_messages_de_contrôle_du_réseau_interconnecté.Internetprotocolreceivewhen(sourceipaddressréseauoctetorder, destinationipaddressréseauoctetorder, donnéesPointeur, taille)
}

var iphandler IInternetprotocolhandler

type TProtocole_des_messages_de_contrôle_du_réseau_interconnecté struct {
}

func (self *TProtocole_des_messages_de_contrôle_du_réseau_interconnecté) Init(backend TFournisseur_du_protocole_du_réseau_interconnecté, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protocole_des_messages_de_contrôle_du_réseau_interconnecté = self
}
func (self *TProtocole_des_messages_de_contrôle_du_réseau_interconnecté) Internetprotocolreceivewhen(sourceipaddressréseauoctetorder uint32, destinationipaddressréseauoctetorder uint32, donnéesPointeur uintptr, taille uint32) bool {
	if taille < uint32(icmpTaille) {
		return false
	}

	var buffer_2 *TInternetCtrlmessageprotocolmessagebuffer = (*TInternetCtrlmessageprotocolmessagebuffer)(Pointer(donnéesPointeur))
	var msg TInternetCtrlmessageprotocolmessage = TInternetCtrlmessageprotocolmessage{}
	msg.Init(*buffer_2)

	icmpconsole.MImprimer(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Imprimer(uint16(msg.TypeValeur))
	icmpconsole.MImprimer(([]byte)(":"))

	switch msg.TypeValeur {
	case 0:
		icmpconsole.MImprimer(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MImprimer(([]byte)("ping send "))
		msg.TypeValeur = 0

		msg.checksum = 0
		msg.Ensemblebuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(donnéesPointeur)), uint32(icmpTaille))

		msg.Ensemblebuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TProtocole_des_messages_de_contrôle_du_réseau_interconnecté) EchorequestEnvoyer(ipréseauoctetorder uint32) bool {
	var protocole_des_messages_de_contrôle_du_réseau_interconnecté TInternetCtrlmessageprotocolmessage = TInternetCtrlmessageprotocolmessage{}

	var mémoiregestionnaire = &TMémoiregestionnaire{}
	var buffer_2 = (*TInternetCtrlmessageprotocolmessagebuffer)(mémoiregestionnaire.Allouer_la_mémoire(1024))

	protocole_des_messages_de_contrôle_du_réseau_interconnecté.TypeValeur = 8
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.code = 0
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.données = 0x3713
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.checksum = 0
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.Ensemblebuffer(buffer_2)
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpTaille))
	protocole_des_messages_de_contrôle_du_réseau_interconnecté.Ensemblebuffer(buffer_2)

	var donnéesPointeur uintptr = uintptr(Pointer(buffer_2))
	iphandler.Envoyer(ipréseauoctetorder, 0x01, donnéesPointeur, uint32(icmpTaille))

	return false

}
