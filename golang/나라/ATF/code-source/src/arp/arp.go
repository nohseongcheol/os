package arp

import . "unsafe"
import . "console"
import . "trame_du_réseau_à_support_partagé"
import . "utilitaire"

var arpconsole TConsole = TConsole{}

type Arpmessagebuffer struct {
	matérieltype		[2]byte
	protocol		[2]byte
	matérieladdressTaille	byte
	protocoladdressTaille	byte
	commande		[2]byte

	sourcemacaddress	[6]byte
	sourceipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgTaille uint32 = (64+92+64)/8 + 2

type Arpmessage struct {
	matérieltype		uint16
	protocol		uint16
	matérieladdressTaille	uint8
	protocoladdressTaille	uint8
	commande		uint16

	sourcemacaddress	uint64
	sourceipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpmessage) Init(buffer_2 *Arpmessagebuffer) {

	self.matérieltype = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.matérieltype))
	self.protocol = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.protocol))
	self.matérieladdressTaille = byte(buffer_2.matérieladdressTaille)
	self.protocoladdressTaille = byte(buffer_2.protocoladdressTaille)
	self.commande = Unsignedinteger16r(Tableautounsignedinteger16(buffer_2.commande))

	self.sourcemacaddress = Unsignedinteger48r(Tableautounsignedinteger48(buffer_2.sourcemacaddress))
	self.sourceipaddress = Unsignedinteger32r(Tableautounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Tableautounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Tableautounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpmessage) Ensemblebuffer(buffer_2 *Arpmessagebuffer) {
	buffer_2.matérieltype = Unsignedinteger16totableau(self.matérieltype)
	buffer_2.protocol = Unsignedinteger16totableau(self.protocol)
	buffer_2.matérieladdressTaille = uint8(self.matérieladdressTaille)
	buffer_2.protocoladdressTaille = uint8(self.protocoladdressTaille)

	buffer_2.commande = Unsignedinteger16totableau(self.commande)
	buffer_2.sourcemacaddress = Unsignedinteger48totableau(self.sourcemacaddress)
	buffer_2.sourceipaddress = Unsignedinteger32totableau(self.sourceipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48totableau(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32totableau(self.destinationipaddress)
}

type Arpethernettramehandler struct {
	TEthernettramehandler
}

var arpprovider Arpprovider
var fournisseur_de_trames_du_réseau_à_support_partagé TFournisseur_de_trames_du_réseau_à_support_partagé

func (self *Arpethernettramehandler) Ethernettramereceivewhen(donnéesPointeur uintptr, taille int) bool {
	arpconsole.MImprimerxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernettramereceivewhen(donnéesPointeur, uint32(taille))

}
func (self *Arpethernettramehandler) Envoyer(destinationmacbe uint64, donnéesPointeur uintptr, taille uint32) {
	arpconsole.MImprimerxy([]byte("arp send:"), 0, 24)
	var ethernettypebe = Unsignedinteger16r(0x0806)
	self.TEthernettramehandler.TrameEnvoyer(destinationmacbe, ethernettypebe, donnéesPointeur, taille)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	nombrecacheélément	int

	handler	IEthernettramehandler
}

var handler IEthernettramehandler

func (self *Arpprovider) Init(backend TFournisseur_de_trames_du_réseau_à_support_partagé, userhandler IEthernettramehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Ensemblehandler(userhandler, 0x0806)
	self.nombrecacheélément = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernettramereceivewhen(donnéesPointeur uintptr, taille uint32) bool {

	if taille < arpmesgTaille {
		return false
	}
	var arpbuffer *Arpmessagebuffer = (*Arpmessagebuffer)(Pointer(donnéesPointeur))
	var arp Arpmessage = Arpmessage{}
	arp.Init(arpbuffer)

	if arp.matérieltype == 0x0100 {

		if arp.protocol == 0x0008 && arp.matérieladdressTaille == 6 && arp.protocoladdressTaille == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MImprimer([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Imprimer(arp.protocol)
			arpconsole.MImprimer([]byte(":"))
			arpconsole.MUnsignedinteger64Imprimer(uint64(arp.destinationmacaddress))
			arpconsole.MImprimer([]byte(":"))
			arpconsole.MUnsignedinteger16Imprimer(arp.commande)
			arpconsole.MImprimer([]byte(":"))
			arpconsole.MUnsignedinteger64Imprimer(handler.Getmacaddress())

			switch arp.commande {
			case 0x0100:

				if self.Getmacdecache(arp.sourceipaddress) == 0xFFFFFFFFFFFF {
					if self.nombrecacheélément < 128 {
						self.Ipcache[self.nombrecacheélément] = arp.sourceipaddress
						self.Maccache[self.nombrecacheélément] = arp.sourcemacaddress
						self.nombrecacheélément++
					}
				}
				arp.commande = 0x0200
				arp.destinationipaddress = arp.sourceipaddress
				arp.destinationmacaddress = arp.sourcemacaddress
				arp.sourceipaddress = uint32(handler.Getipaddress())
				arp.sourcemacaddress = handler.Getmacaddress()
				arp.Ensemblebuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MImprimer(([]byte)("self.numCacheEntries"))

				if self.nombrecacheélément < 128 {
					self.Ipcache[self.nombrecacheélément] = arp.sourceipaddress
					self.Maccache[self.nombrecacheélément] = arp.sourcemacaddress
					self.nombrecacheélément++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipréseauoctetorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.matérieltype = 0x0100
	arp.protocol = 0x0008
	arp.matérieladdressTaille = 6
	arp.protocoladdressTaille = 4
	arp.commande = 0x0200

	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Résoudre(Ipréseauoctetorder)
	arp.destinationipaddress = Ipréseauoctetorder
	arpconsole.MImprimerxy([]byte("broad mac"), 0, 15)

	arp.sourcemacaddress = handler.Getmacaddress()

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Ensemblebuffer(&arpbuffer)

	var référence_mémoire uintptr = uintptr(Pointer(&arpbuffer))
	handler.Envoyer(arp.destinationmacaddress, référence_mémoire, arpmesgTaille)
}
func (self *Arpprovider) Requestmacaddress(Ipréseauoctetorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.matérieltype = 0x0100

	arp.protocol = 0x0008
	arp.matérieladdressTaille = 6
	arp.protocoladdressTaille = 4
	arp.commande = 0x0100

	arp.sourcemacaddress = handler.Getmacaddress()
	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipréseauoctetorder

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Ensemblebuffer(&arpbuffer)

	var référence_mémoire uintptr = uintptr(Pointer(&arpbuffer))
	handler.Envoyer(arp.destinationmacaddress, référence_mémoire, arpmesgTaille)
}
func (self *Arpprovider) TesterImprimer(données *[]byte, taille uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(données))
	arpconsole.MImprimerxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalImprimer(buffer_2[i])
		arpconsole.MImprimer([]byte(":"))
	}
	arpconsole.MImprimer([]byte("]"))
}

func (self *Arpprovider) Getmacdecache(Ipréseauoctetorder uint32) uint64 {
	for i := 0; i < self.nombrecacheélément; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MImprimer(([]byte)("["))
		arpconsole.MUnsignedinteger32Imprimer(self.Ipcache[i])
		arpconsole.MImprimer(([]byte)(":"))
		arpconsole.MUnsignedinteger32Imprimer(Ipréseauoctetorder)
		arpconsole.MImprimer(([]byte)(":"))
		arpconsole.MImprimer(([]byte)(":"))
		arpconsole.MUnsignedinteger64Imprimer(self.Maccache[i])
		arpconsole.MImprimer(([]byte)("]\n"))

		if self.Ipcache[i] == Ipréseauoctetorder {
			arpconsole.MImprimer([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Résoudre(Ipréseauoctetorder uint32) uint64 {
	var rÉSULTAT uint64 = self.Getmacdecache(Ipréseauoctetorder)
	if rÉSULTAT == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipréseauoctetorder)
	}
	for i := 0; i < 128 && rÉSULTAT == 0xFFFFFFFFFFFF; i++ {
		rÉSULTAT = self.Getmacdecache(Ipréseauoctetorder)

	}

	return rÉSULTAT
}
