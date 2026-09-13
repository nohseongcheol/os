package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "διακοπή"
import . "multitasking"
import . "tasking/tss"

import . "εικονικήΜνήμη"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/διεργασία"
import . "driver/driver"

import . "driver/πληκτρολόγιο"
import . "driver/ποντίκι"

import . "driver/ata"
import . "αρχείοΣύστημα/msdospartition"
import . "αρχείοΣύστημα/fat"

import . "αρχείοΣύστημα/elf"

import . "σύστημαcall"

import . "μνήμηmanager"
import . "pci"

func halt()

var iΠληκτρολόγιοΣυμβάνhandler IΠληκτρολόγιοΣυμβάνhandler

type TMyΠληκτρολόγιοΣυμβάνhandler struct {
}

var myΠληκτρολόγιοΣυμβάνhandler TMyΠληκτρολόγιοΣυμβάνhandler
var πληκτρολόγιοdriver TΠληκτρολόγιοdriver
var ποντίκιdriver TΠοντίκιdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var πληκτρολόγιοconsole TConsole = TConsole{}

func (self *TMyΠληκτρολόγιοΣυμβάνhandler) ΕνεργήΚλειδίΚάτω(κλειδί byte) {
	foo := [1]byte{' '}
	foo[0] = κλειδί

	πληκτρολόγιοconsole.MΕκτύπωσηbytesxy(foo[:], 1000, 1000)
}

func (self *TMyΠληκτρολόγιοΣυμβάνhandler) ΕνεργήΚλειδίΠάνω(κλειδί byte)	{}

var iΠοντίκιΣυμβάνhandler IΠοντίκιΣυμβάνhandler

type TMyΠοντίκιΣυμβάνhandler struct {
}

var ποντίκιconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xΘέση int16 = 0
var yΘέση int16 = 0

func (self *TMyΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΚάτω(κουμπί int8) {
	buffer := []byte("x")
	ποντίκιconsole.MΕκτύπωσηxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΠάνω(κουμπί int8)	{}
func (self *TMyΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΜετακίνηση(x int8, y int8) {

	xΘέση += int16(x)
	if xΘέση < 0 {
		xΘέση = 0
	}
	if xΘέση >= 80 {
		xΘέση = 79
	}

	yΘέση -= int16(y)

	if yΘέση < 0 {
		yΘέση = 0
	}
	if yΘέση >= 25 {
		yΘέση = 24
	}

	buffer := []byte(" ")
	ποντίκιconsole.MΕκτύπωσηxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	ποντίκιconsole.MΕκτύπωσηxy(buffer, uint16(xΘέση), uint16(yΘέση))

	previousx = xΘέση
	previousy = yΘέση
}

var συσκευήdescriptor TPeripheralcomponentinterconnectΣυσκευήdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ενεργήgetdriver(συσκευή TPeripheralcomponentinterconnectΣυσκευήdescriptor) {
	if συσκευή.ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ == 0x1022 && συσκευή.ΣυσκευήΤΑΥΤΌΤΗΤΑ == 0x2000 {
		console.MΕκτύπωσηxy([]byte("["), 0, 12)
		console.MΕκτύπωση(([]byte)("AMD am79c973"))
		console.MΕκτύπωση([]byte(":"))
		console.MUnsignedinteger16Εκτύπωση(συσκευή.ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ)
		console.MΕκτύπωση([]byte(":"))
		console.MUnsignedinteger16Εκτύπωση(συσκευή.ΣυσκευήΤΑΥΤΌΤΗΤΑ)
		console.MΕκτύπωση([]byte(":"))
		console.MUnsignedinteger16Εκτύπωση(uint16(συσκευή.Θύραbase))
		console.MΕκτύπωση([]byte(":"))
		console.MUnsignedinteger32Εκτύπωση(συσκευή.Διακοπή)

		console.MΕκτύπωση([]byte("]\n"))
		συσκευήdescriptor = συσκευή
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectΣυσκευήdescriptor {
	return συσκευήdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Εκτύπωσηstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MΕκτύπωση(str)
}

func GetΑρχείοΜέγεθος(όνομααρχείου []byte) uint32 {
	var ata0s = TΓιαπροχωρημένουςΤεχνολογίαattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionΠίνακας{}
	partition.Ανάγνωσηpartition(&ata0s)

	bios := TBiosparameterΜπλοκ32{}

	var μέγεθος uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου)
	ata0s.Flush()

	return μέγεθος
}

func ΑνάγνωσηΑρχείο(όνομααρχείου []byte, data []byte) {
	var ata0s = TΓιαπροχωρημένουςΤεχνολογίαattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionΠίνακας{}
	partition.Ανάγνωσηpartition(&ata0s)

	bios := TBiosparameterΜπλοκ32{}
	bios.Ανάγνωση(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου, data)

	ata0s.Flush()
}
func Φόρτοςelf() {

	var ata0s = TΓιαπροχωρημένουςΤεχνολογίαattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionΠίνακας{}
	partition.Ανάγνωσηpartition(&ata0s)

	bios := TBiosparameterΜπλοκ32{}

	var όνομααρχείου []byte = ([]byte)("TEST")
	var μέγεθος uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Ανάγνωση(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου, data)

	elf := Elf{}

	elf.Parse(data[:μέγεθος], 0x4f00000)

}

var διεργασίαconsole TConsole = TConsole{}

func TΣυνάρτηση1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func διεργασίαa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func διεργασίαb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func διεργασίαc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func διεργασίαd()

func διεργασίαd0() {
	esi := getesi()
	for {

		SysΕκτύπωσηunsignedinteger32(esi)

	}
}

func διεργασίαd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func είσοδοςΣυμβάνΔιεργασία() {
	for {
		ΔιεργασίαpendingΠληκτρολόγιοΓεγονότα()
		ΔιεργασίαpendingΠοντίκιΓεγονότα()
		halt()
	}
}

func memorytest(y int) {
	μνήμηmanager := &TΜνήμηmanager{}
	allocated := uint32(uintptr(μνήμηmanager.Malloc(1024)))
	console.MUnsignedinteger32Εκτύπωσηxy(allocated, 10, uint16(y))
	if y == 11 {
		μνήμηmanager.Ελεύθερα(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Παύσηloop()
func Επαναφόρτωσηcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Σύνολοcr3(cr3 uint32)
func Getcr4() uint32
func Ενεργοποίησηpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetΣυνάρτησηΌνομα(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcΌνομα = runtime.FuncForPC(address).Name()
	var funcbytes []byte = []byte(funcΌνομα)

	διεργασίαconsole.MΕκτύπωσηxy(funcbytes, 1, 5)
	διεργασίαconsole.MΕκτύπωση(([]byte)(":"))
	διεργασίαconsole.MUnsignedinteger32Εκτύπωση(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	διεργασίαconsole.MΕκτύπωσηunsignedinteger32(cr0, 2, 1)
}

var tss *Tssκαταχώρηση = &Tssκαταχώρηση{}

func KKernelEntry(ΣελίδαΚατάλογοςκαταχώρηση uintptr, stacktop uintptr, stackbottom uintptr) {

	MΣειριακόςαριθμόςΚαταγραφήinit()
	console.MΕκτύπωση("\n=== CYP BOOT ===\n")

	console.MΕκτύπωσηunsignedinteger32(uint32(ΣελίδαΚατάλογοςκαταχώρηση), 0, 2)
	console.MΕκτύπωσηunsignedinteger32(uint32(ΣελίδαΚατάλογοςκαταχώρηση), 10, 2)
	console.MΕκτύπωσηunsignedinteger32(uint32(stacktop), 0, 3)
	console.MΕκτύπωσηunsignedinteger32(uint32(stackbottom), 10, 3)

	μνήμηmanager := &TΜνήμηmanager{}
	μνήμηmanager.Init(0, ΜεγqueueΜέγεθος)

	paging := &Paging{}
	paging.Init(ΣελίδαΚατάλογοςκαταχώρηση, 0x500000, μνήμηmanager)
	paging.SharedΜνήμηregion()

	Σύνολοcr3(uint32(ΣελίδαΚατάλογοςκαταχώρηση))
	Ενεργοποίησηpaging()

	shareddescriptorΠίνακας := &TShareddescriptorΠίνακας{}
	shareddescriptorΠίνακας.Init()

	console.MΕκτύπωση("esp:")

	esp := getesp()
	console.MUnsignedinteger32Εκτύπωση(uint32(esp))

	tls := gettls()
	console.MΕκτύπωση(([]byte)("tls:"))
	console.MUnsignedinteger32Εκτύπωση(tls)

	tss.Εγκατάσταση(shareddescriptorΠίνακας, 7, Segkerneldata, esp)

	VirtΔοκιμή()

	cr3 := Επαναφόρτωσηcr3()
	console.MΕκτύπωση(([]byte)(":cr3:"))
	console.MUnsignedinteger32Εκτύπωση(cr3)

	cr0 := Getcr0()
	console.MΕκτύπωση(([]byte)(":cr0:"))
	console.MUnsignedinteger32Εκτύπωση(cr0)

	cr4 := Getcr4()
	console.MΕκτύπωση(([]byte)(":cr4:"))
	console.MUnsignedinteger32Εκτύπωση(cr4)

	διεργασίαmanager_2 := &TΔιεργασίαmanager{}
	διεργασίαmanager_2.Init()

	Διακοπήmanager := &TΔιακοπήmanager{}
	Διακοπήmanager.Init(0x20, shareddescriptorΠίνακας, διεργασίαmanager_2)

	paging.Σελίδαfault(Διακοπήmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(μνήμηmanager)

	διεργασίαhelper := Διεργασίαhelper{}
	διεργασίαhelper.Init(μνήμηmanager, ΣελίδαΚατάλογοςκαταχώρηση)

	sche := &Scheduler{}
	sche.Init(Διακοπήmanager, μνήμηmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Διακοπήmanager)

	διεργασίαhelper.Spawn(διεργασίαa, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση), true)
	διεργασίαhelper.Spawn(διεργασίαb, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση), true)
	διεργασίαhelper.Spawn(διεργασίαc, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση), true)
	διεργασίαhelper.Spawn(διεργασίαd1, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση), true)
	διεργασίαhelper.Spawn(είσοδοςΣυμβάνΔιεργασία, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση), true)

	var μέγεθος uint32

	var linkerΑρχείο []byte = ([]byte)("LINKER")
	μέγεθος = GetΑρχείοΜέγεθος(linkerΑρχείο)
	linkeraddress := μνήμηmanager.Malloc(μέγεθος)
	linkerdata := GetbytesfromΔείκτης(uintptr(linkeraddress), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(linkerΑρχείο, linkerdata)

	elf0 := Elf{}
	linkerκαταχώρηση := elf0.Getκαταχώρηση(linkerdata)
	elf0.Parse(linkerdata[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση))

	δεσμόςmap := Δεσμόςmap{}
	δεσμόςmap.Init(μνήμηmanager)

	var lib1Αρχείο []byte = ([]byte)("LIB1")
	μέγεθος = GetΑρχείοΜέγεθος(lib1Αρχείο)

	lib1address := μνήμηmanager.Malloc(μέγεθος)
	lib1data := GetbytesfromΔείκτης(uintptr(lib1address), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(lib1Αρχείο, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση))
	μνήμηmanager.Ελεύθερα(lib1address)

	δεσμόςmap.Append_to_list(uintptr(lib1elf.Δυναμικό))

	var lib2Αρχείο []byte = ([]byte)("LIB2")
	μέγεθος = GetΑρχείοΜέγεθος(lib2Αρχείο)

	lib2address := μνήμηmanager.Malloc(μέγεθος)
	lib2data := GetbytesfromΔείκτης(uintptr(lib2address), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(lib2Αρχείο, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση))
	μνήμηmanager.Ελεύθερα(lib2address)

	δεσμόςmap.Append_to_list(uintptr(lib2elf.Δυναμικό))

	libΔεσμόςmap := δεσμόςmap.Clone()
	δεσμόςmapaddress := uint32(uintptr(Pointer(libΔεσμόςmap.First)))

	lib1got := Getunsignedinteger32ΔιάταξηfromΔείκτης(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = δεσμόςmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ΔιάταξηfromΔείκτης(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = δεσμόςmapaddress
	lib2got[2] = 0x4000000

	console.MΕκτύπωσηxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Εκτύπωση(lib1elf.Got)
	console.MΕκτύπωση(":")
	console.MUnsignedinteger32Εκτύπωση(lib1elf.Δυναμικό)

	console.MΕκτύπωσηxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Εκτύπωση(lib2elf.Got)
	console.MΕκτύπωση(":")
	console.MUnsignedinteger32Εκτύπωση(lib2elf.Δυναμικό)

	var χρήστης1Αρχείο []byte = ([]byte)("USER1")
	μέγεθος = GetΑρχείοΜέγεθος(χρήστης1Αρχείο)
	χρήστης1address := μνήμηmanager.Malloc(μέγεθος)
	χρήστης1data := GetbytesfromΔείκτης(uintptr(χρήστης1address), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(χρήστης1Αρχείο, χρήστης1data)

	elf2 := Elf{}

	χρήστης1καταχώρηση := elf2.Getκαταχώρηση(χρήστης1data)
	elf2.Parse(χρήστης1data[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x1000))
	καθολικάoffsetΠίνακας := elf2.Got

	PΤιμή1Δεσμόςmap := δεσμόςmap.Clone()
	PΤιμή1Δεσμόςmap.Append_to_list(uintptr(elf2.Δυναμικό))

	μνήμηmanager.Ελεύθερα(χρήστης1address)

	var code1Δείκτης *uintptr
	var func1val func()

	code1Δείκτης = (*uintptr)(μνήμηmanager.Malloc(4))
	*code1Δείκτης = uintptr(linkerκαταχώρηση)
	func1val = *(*func())(Pointer(&code1Δείκτης))

	proc2 := διεργασίαhelper.Spawn(func1val, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ΕπεξεργαστήςΚατάσταση.Ecx = χρήστης1καταχώρηση
	thr2.ΕπεξεργαστήςΚατάσταση.Edx = καθολικάoffsetΠίνακας
	thr2.ΕπεξεργαστήςΚατάσταση.Esi = uint32(uintptr(Pointer(PΤιμή1Δεσμόςmap.First)))

	console.MΕκτύπωσηxy("user1: ", 1, 10)
	console.MUnsignedinteger32Εκτύπωση(elf2.Got)

	var χρήστης2Αρχείο []byte = ([]byte)("USER2")
	μέγεθος = GetΑρχείοΜέγεθος(χρήστης2Αρχείο)
	χρήστης2address := μνήμηmanager.Malloc(μέγεθος)
	χρήστης2data := GetbytesfromΔείκτης(uintptr(χρήστης2address), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(χρήστης2Αρχείο, χρήστης2data)

	elf3 := Elf{}

	χρήστης2καταχώρηση := elf3.Getκαταχώρηση(χρήστης2data)
	elf3.Parse(χρήστης2data[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x2000))
	καθολικάoffsetΠίνακας = elf3.Got

	PΤιμή2Δεσμόςmap := δεσμόςmap.Clone()
	PΤιμή2Δεσμόςmap.Append_to_list(uintptr(elf3.Δυναμικό))

	μνήμηmanager.Ελεύθερα(χρήστης2address)

	var code2Δείκτης *uintptr
	var func2val func()

	code2Δείκτης = (*uintptr)(μνήμηmanager.Malloc(4))
	*code2Δείκτης = uintptr(linkerκαταχώρηση)
	func2val = *(*func())(Pointer(&code2Δείκτης))

	proc3 := διεργασίαhelper.Spawn(func2val, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ΕπεξεργαστήςΚατάσταση.Ecx = χρήστης2καταχώρηση
	thr3.ΕπεξεργαστήςΚατάσταση.Edx = καθολικάoffsetΠίνακας
	thr3.ΕπεξεργαστήςΚατάσταση.Esi = uint32(uintptr(Pointer(PΤιμή2Δεσμόςmap.First)))

	console.MΕκτύπωσηxy("user2: ", 1, 11)
	console.MUnsignedinteger32Εκτύπωση(thr3.ΕπεξεργαστήςΚατάσταση.Esi)

	libΔεσμόςmap.Εκτύπωση(1, 11)

	var χρήστης3Αρχείο []byte = ([]byte)("USER3")
	μέγεθος = GetΑρχείοΜέγεθος(χρήστης3Αρχείο)
	χρήστης3address := μνήμηmanager.Malloc(μέγεθος)
	χρήστης3data := GetbytesfromΔείκτης(uintptr(χρήστης3address), int(μέγεθος), int(μέγεθος))
	ΑνάγνωσηΑρχείο(χρήστης3Αρχείο, χρήστης3data)

	elf4 := Elf{}

	χρήστης3καταχώρηση := elf4.Getκαταχώρηση(χρήστης3data)
	elf4.Parse(χρήστης3data[:], uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x3000))
	καθολικάoffsetΠίνακας = elf4.Got

	PΤιμή3Δεσμόςmap := δεσμόςmap.Clone()
	PΤιμή3Δεσμόςmap.Append_to_list(uintptr(elf4.Δυναμικό))

	μνήμηmanager.Ελεύθερα(χρήστης3address)

	var code3Δείκτης *uintptr
	var func3val func()

	code3Δείκτης = (*uintptr)(μνήμηmanager.Malloc(4))
	*code3Δείκτης = uintptr(linkerκαταχώρηση)
	func3val = *(*func())(Pointer(&code3Δείκτης))

	proc4 := διεργασίαhelper.Spawn(func3val, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ΕπεξεργαστήςΚατάσταση.Ecx = χρήστης3καταχώρηση
	thr4.ΕπεξεργαστήςΚατάσταση.Edx = καθολικάoffsetΠίνακας
	thr4.ΕπεξεργαστήςΚατάσταση.Esi = uint32(uintptr(Pointer(PΤιμή3Δεσμόςmap.First)))

	διεργασίαhelper.Spawn(TΣυνάρτηση1, threadhelper, sche, uint32(ΣελίδαΚατάλογοςκαταχώρηση+0x4000), true)

	iΠληκτρολόγιοΣυμβάνhandler = &myΠληκτρολόγιοΣυμβάνhandler
	πληκτρολόγιοdriver.Initdriver(Διακοπήmanager, iΠληκτρολόγιοΣυμβάνhandler)

	ποντίκιdriver.Initdriver(Διακοπήmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Επιλογήdriver(&Drivermanager, Διακοπήmanager)
	συσκευήdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Ενεργό_2(true)
	Διακοπήmanager.Ενεργό()

	for {
		halt()
	}

}
