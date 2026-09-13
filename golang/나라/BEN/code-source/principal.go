package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "utilitaire"
import . "gdt"
import . "console"
import . "interruption"
import . "multiplegestionTâches"
import . "gestionTâches/tss"

import . "virtuelmémoire"
import . "pagination"
import . "gestionTâches/filExécution"
import . "gestionTâches/ordonnanceur"
import . "gestionTâches/processus"
import . "pilote/pilote"

import . "pilote/clavier"
import . "pilote/dispositif_de_pointage"

import . "pilote/ata"
import . "fichiersystème/msdospartition"
import . "fichiersystème/fat"

import . "fichiersystème/format_exécutable_et_liable"

import . "systèmeappel"

import . "mémoiregestionnaire"
import . "pci"

func halt()

var iclavierévénementhandler IClavierévénementhandler

type TMyclavierévénementhandler struct {
}

var myclavierévénementhandler TMyclavierévénementhandler
var clavierpilote TClavierpilote
var sourispilote TSourispilote
var pcicontrôleur TPeripheralcomponentinterconnectcontrôleur

var clavierconsole TConsole = TConsole{}

func (self *TMyclavierévénementhandler) SurCléVerslebas(clé byte) {
	foo := [1]byte{' '}
	foo[0] = clé

	clavierconsole.MImprimerOctetsxy(foo[:], 1000, 1000)
}

func (self *TMyclavierévénementhandler) SurCléHaut(clé byte)	{}

var isourisévénementhandler ISourisévénementhandler

type TMysourisévénementhandler struct {
}

var sourisconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xposition int16 = 0
var yposition int16 = 0

func (self *TMysourisévénementhandler) SursourisVerslebas(bouton int8) {
	buffer := []byte("x")
	sourisconsole.MImprimerxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMysourisévénementhandler) SursourisHaut(bouton int8)	{}
func (self *TMysourisévénementhandler) SursourisDéplacer(x int8, y int8) {

	xposition += int16(x)
	if xposition < 0 {
		xposition = 0
	}
	if xposition >= 80 {
		xposition = 79
	}

	yposition -= int16(y)

	if yposition < 0 {
		yposition = 0
	}
	if yposition >= 25 {
		yposition = 24
	}

	buffer := []byte(" ")
	sourisconsole.MImprimerxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	sourisconsole.MImprimerxy(buffer, uint16(xposition), uint16(yposition))

	previousx = xposition
	previousy = yposition
}

var périphériquedescriptor TPeripheralcomponentinterconnectPériphériquedescriptor
var ipcicontrôleurhandler Ipcicontrôleurhandler

type TMypcicontrôleurhandler struct {
}

var console TConsole = TConsole{}
var piloteNombre uint16 = 0

func (self TMypcicontrôleurhandler) Surgetpilote(périphérique TPeripheralcomponentinterconnectPériphériquedescriptor) {
	if périphérique.MarqueIdentifiant == 0x1022 && périphérique.PériphériqueIdentifiant == 0x2000 {
		console.MImprimerxy([]byte("["), 0, 12)
		console.MImprimer(([]byte)("AMD am79c973"))
		console.MImprimer([]byte(":"))
		console.MUnsignedinteger16Imprimer(périphérique.MarqueIdentifiant)
		console.MImprimer([]byte(":"))
		console.MUnsignedinteger16Imprimer(périphérique.PériphériqueIdentifiant)
		console.MImprimer([]byte(":"))
		console.MUnsignedinteger16Imprimer(uint16(périphérique.Portbase))
		console.MImprimer([]byte(":"))
		console.MUnsignedinteger32Imprimer(périphérique.Interruption)

		console.MImprimer([]byte("]\n"))
		périphériquedescriptor = périphérique
		piloteNombre++
	}
}
func (self TMypcicontrôleurhandler) Getpilote() TPeripheralcomponentinterconnectPériphériquedescriptor {
	return périphériquedescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Imprimerstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MImprimer(str)
}

func GetfichierTaille(nomdefichier []byte) uint32 {
	var ata0s = TAvancéTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTableau{}
	partition.Lirepartition(&ata0s)

	bios := TParamètres_du_système_de_fichiers32{}

	var taille uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier)
	ata0s.Flush()

	return taille
}

func Lire_le_fichier(nomdefichier []byte, données []byte) {
	var ata0s = TAvancéTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTableau{}
	partition.Lirepartition(&ata0s)

	bios := TParamètres_du_système_de_fichiers32{}
	bios.Lire(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier, données)

	ata0s.Flush()
}
func Chargerelf() {

	var ata0s = TAvancéTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTableau{}
	partition.Lirepartition(&ata0s)

	bios := TParamètres_du_système_de_fichiers32{}

	var nomdefichier []byte = ([]byte)("TEST")
	var taille uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier)
	var donnéesbuffer [100 * 1024]byte
	var données []byte = donnéesbuffer[:]
	bios.Lire(&ata0s, partition.Mbr.Primarypartition[0], nomdefichier, données)

	format_exécutable_et_liable := Elf{}

	format_exécutable_et_liable.Parse(données[:taille], 0x4f00000)

}

var tâcheconsole TConsole = TConsole{}

func TFonction1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tâchea() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tâcheb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tâchec() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tâched()

func tâched0() {
	esi := getesi()
	for {

		SysImprimerunsignedinteger32(esi)

	}
}

func tâched1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func entréeévénementtâche() {
	for {
		Processusattenteclavierévénements()
		Processusattentesourisévénements()
		halt()
	}
}

func memorytest(y int) {
	mémoiregestionnaire := &TMémoiregestionnaire{}
	allocated := uint32(uintptr(mémoiregestionnaire.Allouer_la_mémoire(1024)))
	console.MUnsignedinteger32Imprimerxy(allocated, 10, uint16(y))
	if y == 11 {
		mémoiregestionnaire.Libre(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func SuspendreBoucles()
func Rechargercr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Ensemblecr3(cr3 uint32)
func Getcr4() uint32
func Activerpagination()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFonctionNom(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNom = runtime.FuncForPC(address).Name()
	var funcOctets []byte = []byte(funcNom)

	tâcheconsole.MImprimerxy(funcOctets, 1, 5)
	tâcheconsole.MImprimer(([]byte)(":"))
	tâcheconsole.MUnsignedinteger32Imprimer(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	tâcheconsole.MImprimerunsignedinteger32(cr0, 2, 1)
}

var tss *Tssélément = &Tssélément{}

func KKernelEntry(Pagerépertoireélément uintptr, stacktop uintptr, stackbottom uintptr) {

	MSérieJournalinit()
	console.MImprimer("\n=== BEN BOOT ===\n")

	console.MImprimerunsignedinteger32(uint32(Pagerépertoireélément), 0, 2)
	console.MImprimerunsignedinteger32(uint32(Pagerépertoireélément), 10, 2)
	console.MImprimerunsignedinteger32(uint32(stacktop), 0, 3)
	console.MImprimerunsignedinteger32(uint32(stackbottom), 10, 3)

	mémoiregestionnaire := &TMémoiregestionnaire{}
	mémoiregestionnaire.Init(0, MaxfileAttenteTaille)

	pagination := &Pagination{}
	pagination.Init(Pagerépertoireélément, 0x500000, mémoiregestionnaire)
	pagination.Sharedmémoireregion()

	Ensemblecr3(uint32(Pagerépertoireélément))
	Activerpagination()

	shareddescriptorTableau := &TShareddescriptorTableau{}
	shareddescriptorTableau.Init()

	console.MImprimer("esp:")

	esp := getesp()
	console.MUnsignedinteger32Imprimer(uint32(esp))

	tls := gettls()
	console.MImprimer(([]byte)("tls:"))
	console.MUnsignedinteger32Imprimer(tls)

	tss.Installer(shareddescriptorTableau, 7, Segnoyaudonnées, esp)

	VirtTester()

	cr3 := Rechargercr3()
	console.MImprimer(([]byte)(":cr3:"))
	console.MUnsignedinteger32Imprimer(cr3)

	cr0 := Getcr0()
	console.MImprimer(([]byte)(":cr0:"))
	console.MUnsignedinteger32Imprimer(cr0)

	cr4 := Getcr4()
	console.MImprimer(([]byte)(":cr4:"))
	console.MUnsignedinteger32Imprimer(cr4)

	tâchegestionnaire_2 := &TTâchegestionnaire{}
	tâchegestionnaire_2.Init()

	Interruptiongestionnaire := &TInterruptiongestionnaire{}
	Interruptiongestionnaire.Init(0x20, shareddescriptorTableau, tâchegestionnaire_2)

	pagination.Pagedéfaut(Interruptiongestionnaire)

	Pilotegestionnaire := TPilotegestionnaire{}
	Pilotegestionnaire.Init()

	filExécutionhelper := &TFilExécutionhelper{}
	filExécutionhelper.Init(mémoiregestionnaire)

	processushelper := Processushelper{}
	processushelper.Init(mémoiregestionnaire, Pagerépertoireélément)

	sche := &Ordonnanceur{}
	sche.Init(Interruptiongestionnaire, mémoiregestionnaire, tss)

	sysappel := &TSyscall{}
	sysappel.Init(Interruptiongestionnaire)

	processushelper.Spawn(tâchea, filExécutionhelper, sche, uint32(Pagerépertoireélément), true)
	processushelper.Spawn(tâcheb, filExécutionhelper, sche, uint32(Pagerépertoireélément), true)
	processushelper.Spawn(tâchec, filExécutionhelper, sche, uint32(Pagerépertoireélément), true)
	processushelper.Spawn(tâched1, filExécutionhelper, sche, uint32(Pagerépertoireélément), true)
	processushelper.Spawn(entréeévénementtâche, filExécutionhelper, sche, uint32(Pagerépertoireélément), true)

	var taille uint32

	var linkerfichier []byte = ([]byte)("LINKER")
	taille = GetfichierTaille(linkerfichier)
	linkeraddress := mémoiregestionnaire.Allouer_la_mémoire(taille)
	linkerdonnées := GetOctetsdePointeur(uintptr(linkeraddress), int(taille), int(taille))
	Lire_le_fichier(linkerfichier, linkerdonnées)

	elf0 := Elf{}
	linkerélément := elf0.Getélément(linkerdonnées)
	elf0.Parse(linkerdonnées[:], uint32(Pagerépertoireélément))

	liencarte := Liencarte{}
	liencarte.Init(mémoiregestionnaire)

	var lib1fichier []byte = ([]byte)("LIB1")
	taille = GetfichierTaille(lib1fichier)

	lib1address := mémoiregestionnaire.Allouer_la_mémoire(taille)
	lib1données := GetOctetsdePointeur(uintptr(lib1address), int(taille), int(taille))
	Lire_le_fichier(lib1fichier, lib1données)

	lib1elf := Elf{}
	lib1elf.Parse(lib1données[:], uint32(Pagerépertoireélément))
	mémoiregestionnaire.Libre(lib1address)

	liencarte.Ajouter_en_fin_de_liste(uintptr(lib1elf.Dynamique))

	var lib2fichier []byte = ([]byte)("LIB2")
	taille = GetfichierTaille(lib2fichier)

	lib2address := mémoiregestionnaire.Allouer_la_mémoire(taille)
	lib2données := GetOctetsdePointeur(uintptr(lib2address), int(taille), int(taille))
	Lire_le_fichier(lib2fichier, lib2données)

	lib2elf := Elf{}
	lib2elf.Parse(lib2données[:], uint32(Pagerépertoireélément))
	mémoiregestionnaire.Libre(lib2address)

	liencarte.Ajouter_en_fin_de_liste(uintptr(lib2elf.Dynamique))

	libliencarte := liencarte.Clone()
	liencarteaddress := uint32(uintptr(Pointer(libliencarte.First)))

	lib1got := Getunsignedinteger32tableaudePointeur(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = liencarteaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32tableaudePointeur(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = liencarteaddress
	lib2got[2] = 0x4000000

	console.MImprimerxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Imprimer(lib1elf.Got)
	console.MImprimer(":")
	console.MUnsignedinteger32Imprimer(lib1elf.Dynamique)

	console.MImprimerxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Imprimer(lib2elf.Got)
	console.MImprimer(":")
	console.MUnsignedinteger32Imprimer(lib2elf.Dynamique)

	var utilisateur1fichier []byte = ([]byte)("USER1")
	taille = GetfichierTaille(utilisateur1fichier)
	utilisateur1address := mémoiregestionnaire.Allouer_la_mémoire(taille)
	utilisateur1données := GetOctetsdePointeur(uintptr(utilisateur1address), int(taille), int(taille))
	Lire_le_fichier(utilisateur1fichier, utilisateur1données)

	elf2 := Elf{}

	utilisateur1élément := elf2.Getélément(utilisateur1données)
	elf2.Parse(utilisateur1données[:], uint32(Pagerépertoireélément+0x1000))
	globalDécalageTableau := elf2.Got

	PValeur1liencarte := liencarte.Clone()
	PValeur1liencarte.Ajouter_en_fin_de_liste(uintptr(elf2.Dynamique))

	mémoiregestionnaire.Libre(utilisateur1address)

	var code1Pointeur *uintptr
	var func1val func()

	code1Pointeur = (*uintptr)(mémoiregestionnaire.Allouer_la_mémoire(4))
	*code1Pointeur = uintptr(linkerélément)
	func1val = *(*func())(Pointer(&code1Pointeur))

	proc2 := processushelper.Spawn(func1val, filExécutionhelper, sche, uint32(Pagerépertoireélément+0x1000), false)
	thr2 := (*TFilExécution)(proc2.Threads.Getat(0))
	thr2.ProcesseurÉtat.Ecx = utilisateur1élément
	thr2.ProcesseurÉtat.Edx = globalDécalageTableau
	thr2.ProcesseurÉtat.Esi = uint32(uintptr(Pointer(PValeur1liencarte.First)))

	console.MImprimerxy("user1: ", 1, 10)
	console.MUnsignedinteger32Imprimer(elf2.Got)

	var utilisateur2fichier []byte = ([]byte)("USER2")
	taille = GetfichierTaille(utilisateur2fichier)
	utilisateur2address := mémoiregestionnaire.Allouer_la_mémoire(taille)
	utilisateur2données := GetOctetsdePointeur(uintptr(utilisateur2address), int(taille), int(taille))
	Lire_le_fichier(utilisateur2fichier, utilisateur2données)

	elf3 := Elf{}

	utilisateur2élément := elf3.Getélément(utilisateur2données)
	elf3.Parse(utilisateur2données[:], uint32(Pagerépertoireélément+0x2000))
	globalDécalageTableau = elf3.Got

	PValeur2liencarte := liencarte.Clone()
	PValeur2liencarte.Ajouter_en_fin_de_liste(uintptr(elf3.Dynamique))

	mémoiregestionnaire.Libre(utilisateur2address)

	var code2Pointeur *uintptr
	var func2val func()

	code2Pointeur = (*uintptr)(mémoiregestionnaire.Allouer_la_mémoire(4))
	*code2Pointeur = uintptr(linkerélément)
	func2val = *(*func())(Pointer(&code2Pointeur))

	proc3 := processushelper.Spawn(func2val, filExécutionhelper, sche, uint32(Pagerépertoireélément+0x2000), false)
	thr3 := (*TFilExécution)(proc3.Threads.Getat(0))
	thr3.ProcesseurÉtat.Ecx = utilisateur2élément
	thr3.ProcesseurÉtat.Edx = globalDécalageTableau
	thr3.ProcesseurÉtat.Esi = uint32(uintptr(Pointer(PValeur2liencarte.First)))

	console.MImprimerxy("user2: ", 1, 11)
	console.MUnsignedinteger32Imprimer(thr3.ProcesseurÉtat.Esi)

	libliencarte.Imprimer(1, 11)

	var utilisateur3fichier []byte = ([]byte)("USER3")
	taille = GetfichierTaille(utilisateur3fichier)
	utilisateur3address := mémoiregestionnaire.Allouer_la_mémoire(taille)
	utilisateur3données := GetOctetsdePointeur(uintptr(utilisateur3address), int(taille), int(taille))
	Lire_le_fichier(utilisateur3fichier, utilisateur3données)

	elf4 := Elf{}

	utilisateur3élément := elf4.Getélément(utilisateur3données)
	elf4.Parse(utilisateur3données[:], uint32(Pagerépertoireélément+0x3000))
	globalDécalageTableau = elf4.Got

	PValeur3liencarte := liencarte.Clone()
	PValeur3liencarte.Ajouter_en_fin_de_liste(uintptr(elf4.Dynamique))

	mémoiregestionnaire.Libre(utilisateur3address)

	var code3Pointeur *uintptr
	var func3val func()

	code3Pointeur = (*uintptr)(mémoiregestionnaire.Allouer_la_mémoire(4))
	*code3Pointeur = uintptr(linkerélément)
	func3val = *(*func())(Pointer(&code3Pointeur))

	proc4 := processushelper.Spawn(func3val, filExécutionhelper, sche, uint32(Pagerépertoireélément+0x3000), false)
	thr4 := (*TFilExécution)(proc4.Threads.Getat(0))
	thr4.ProcesseurÉtat.Ecx = utilisateur3élément
	thr4.ProcesseurÉtat.Edx = globalDécalageTableau
	thr4.ProcesseurÉtat.Esi = uint32(uintptr(Pointer(PValeur3liencarte.First)))

	processushelper.Spawn(TFonction1, filExécutionhelper, sche, uint32(Pagerépertoireélément+0x4000), true)

	iclavierévénementhandler = &myclavierévénementhandler
	clavierpilote.Initpilote(Interruptiongestionnaire, iclavierévénementhandler)

	sourispilote.Initpilote(Interruptiongestionnaire, nil)

	mypcicontrôleurhandler := TMypcicontrôleurhandler{}
	pcicontrôleur.Init(mypcicontrôleurhandler)
	pcicontrôleur.Sélectionnerpilote(&Pilotegestionnaire, Interruptiongestionnaire)
	périphériquedescriptor = mypcicontrôleurhandler.Getpilote()

	sche.Activé(true)
	Interruptiongestionnaire.Actif()

	for {
		halt()
	}

}
