/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemacall

import . "unsafe"

import . "pertraukimas"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "failasSistema/msdospartition"
import . "failasSistema/fat"
import . "failasSistema/elf"
import mem "atmintismanager"
import . "paging"
import . "prievadas"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualiAtmintis"

var console_2 = TConsole{}

type TSyscall struct {
	TPertraukimashandler
}

const (
	SysIšeiti	uint32	= 1
	Sysfork		uint32	= 2
	SysSkaitymas	uint32	= 3
	SysRašymas	uint32	= 4
	SysAtverti	uint32	= 5
	SysUžverti	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysprieiti	uint32	= 33
	Syssync		uint32	= 36
	Sysdup		uint32	= 41
	Sysbrk		uint32	= 45
	Sysgetgid	uint32	= 47
	Sysgeteuid	uint32	= 49
	Sysgetegid	uint32	= 50
	Sysfcntl	uint32	= 55
	Sysdup2		uint32	= 63
	Sysgetppid	uint32	= 64
	Syssocketcall	uint32	= 102
	Sysstat		uint32	= 106
	Syslstat	uint32	= 107
	Sysfstat	uint32	= 108
	Sysfsync	uint32	= 118
	Sysuname	uint32	= 122
	Sysgetcwd	uint32	= 183
	SysrtIšeiti	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2big		int32	= -7
	Enoexec		int32	= -8
	Ebadf		int32	= -9
	Echild		int32	= -10
	Eagain		int32	= -11
	Enomem		int32	= -12
	Eacces		int32	= -13
	Efault		int32	= -14
	Ebusy		int32	= -16
	Eexist		int32	= -17
	Enodev		int32	= -19
	Enotdir		int32	= -20
	Eisdir		int32	= -21
	Einval		int32	= -22
	Enfile		int32	= -23
	Emfile		int32	= -24
	Enotty		int32	= -25
	Efbig		int32	= -27
	Enospc		int32	= -28
	Espipe		int32	= -29
	Erofs		int32	= -30
	Erange		int32	= -34
	Enosys		int32	= -38
	Emsgsize	int32	= -90
	Eprotonosupport	int32	= -93
	Eopnotsupp	int32	= -95
	Eafnosupport	int32	= -97
	Eaddrinuse	int32	= -98
	Enetunreach	int32	= -101
	Enotconn	int32	= -107
)

const (
	stdinFA			int32	= 0
	stdoutFA		int32	= 1
	stderrFA		int32	= 2
	maksFA				= 32
	maksAtvertiFAILAI		= 128
)

type fAįrašas struct {
	naudojama	bool
	aprašymas	int32
	fAParametrai	uint32
}

type atvertiFailasAprašymas struct {
	naudojama	bool
	refs		uint32
	rūšis		uint32
	parametrai	uint32
	pozicija	uint32
	dydis		uint32
	pavadinimas	[12]byte
	pavadinimaslen	uint32
	aux		uint32
}

const (
	fARūšisJoks		uint32	= 0
	fARūšisfat		uint32	= 1
	fARūšisstdin		uint32	= 2
	fARūšisconsole		uint32	= 3
	fARūšisŠakniskatalogas	uint32	= 4
	fARūšisLizdas		uint32	= 5

	oSkaitymasonly		uint32	= 0
	oRašymasonly		uint32	= 1
	oSkaitymasRašymas	uint32	= 2
	ocreate			uint32	= 0x40
	oAtmest			uint32	= 0x200
	oappend			uint32	= 0x400
	okatalogas		uint32	= 0x10000

	seeknustatyta	uint32	= 0
	seekDabartinis	uint32	= 1
	seekPab		uint32	= 2

	fdupFA		uint32	= 0
	fgetFA		uint32	= 1
	fnustatytaFA	uint32	= 2
	fgetfl		uint32	= 3
	fnustatytafl	uint32	= 4
	fAcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet			= 2
	sockdatagram		= 2
	ipprotocoludp		= 17
	makssockets		= 32
	maksLizdaspaketų	= 8
	maksdatagramDydis	= 512
)

type lizdasaddressiEv4 struct {
	Family		uint16
	Prievadas	uint16
	Address		uint32
	Nulis		[8]byte
}

type lizdaspacket struct {
	naudojama	bool
	dydis		uint32
	šaltinis	lizdasaddressiEv4
	data		[maksdatagramDydis]byte
}

type vietinisdatagramLizdas struct {
	naudojama	bool
	bound		bool
	connected	bool
	vietinis	lizdasaddressiEv4
	nutolęs		lizdasaddressiEv4
	head		uint32
	tail		uint32
	count		uint32
	paketų		[maksLizdaspaketų]lizdaspacket
}

type posixstat struct {
	Įrenginys	uint32
	Ino		uint32
	REŽIMAS		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Dydis_2		int32
	Blksize		int32
	Blokas		int32
	Atime		int32
	Atimensec	int32
	Mtime		int32
	Mtimensec	int32
	Ctime		int32
	Ctimensec	int32
}

type posixutsname struct {
	Sysname		[65]byte
	Nodename	[65]byte
	Release		[65]byte
	Versija		[65]byte
	Machine		[65]byte
}

const (
	maksVykdytivectorįrašas	= 16
	maksVykdytiEilutėTrukmė	= 63
)

type vykdytivector struct {
	count		uint32
	lengths		[maksVykdytivectorįrašas]uint32
	reikšmės	[maksVykdytivectorįrašas][maksVykdytiEilutėTrukmė + 1]byte
}

type procesasįrašas struct {
	naudojama	bool
	pid		uint32
	parent		uint32
	išėjo		bool
	būsena		uint32
	programabreak	uint32
	fds		[maksFA]fAįrašas
}

type eilutėheader struct {
	Data	uintptr
	Len	int
}

func syscallKlaida(klaidos int32) uint32 {
	return *(*uint32)(Pointer(&klaidos))
}

var atvertiFailasLentelė [maksAtvertiFAILAI]atvertiFailasAprašymas
var procesasLentelė [32]procesasįrašas
var vietinissockets [makssockets]vietinisdatagramLizdas
var kitasephemeralPrievadas uint16 = 49152

const (
	naudotojasheapbase	uint32	= 0x06000000
	naudotojasheapRiba	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinSkaitymas uint32
var stdinRašymas uint32

func Pertraukimas(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIšeiti_2(rodyklė uint32) {
	Syscall(SysIšeiti, rodyklė)
}

func SysSkaitymas_2(fA uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysSkaitymas, fA, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysSpausdintistr(buffer string) {
	h := (*eilutėheader)(Pointer(&buffer))
	Syscall(SysRašymas, uint32(stdoutFA), uint32(h.Data), uint32(h.Len))
}

func SysSpausdintiunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysRašymas, uint32(stdoutFA), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAtverti_2(kELIAS uintptr, parametrai uint32, rEŽIMAS uint32) int32 {
	return int32(Syscall(SysAtverti, uint32(kELIAS), parametrai, rEŽIMAS))
}

func SysUžverti_2(fA uint32) int32 {
	return int32(Syscall(SysUžverti, fA))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametrai_2 ...uint32) uint32 {

	l := len(parametrai_2)
	switch l {
	case 1:
		return Pertraukimas(parametrai_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Pertraukimas(parametrai_2[0], parametrai_2[1], 0, 0, 0, 0)
	case 3:
		return Pertraukimas(parametrai_2[0], parametrai_2[1], parametrai_2[2], 0, 0, 0)
	case 4:
		return Pertraukimas(parametrai_2[0], parametrai_2[1], parametrai_2[2], parametrai_2[3], 0, 0)
	case 5:
		return Pertraukimas(parametrai_2[0], parametrai_2[1], parametrai_2[2], parametrai_2[3], parametrai_2[4], 0)
	case 6:
		return Pertraukimas(parametrai_2[0], parametrai_2[1], parametrai_2[2], parametrai_2[3], parametrai_2[4], parametrai_2[5])
	default:
		return syscallKlaida(Enosys)
	}
}

func (self *TSyscall) Init(manager *TPertraukimasmanager) {
	initFailasdescriptor()

	pertraukimashandler = pozicijaPertraukimas

	var address uintptr
	address = uintptr(Pointer(&pertraukimashandler))

	self.TPertraukimashandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var pertraukimashandler func(uint32) uint32

func pozicijaPertraukimas(esp uint32) uint32 {
	var cpu = (*TcpuBūsena)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysIšeiti:
		sysIšeiti(cpu.Ebx)
		return uint32(uintptr(Pointer(SustabdytiDabartinisthread(cpu))))
	case SysrtIšeiti:
		sysIšeiti(cpu.Ebx)
		return uint32(uintptr(Pointer(SustabdytiDabartinisthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysSkaitymas:
		cpu.Eax = uint32(sysSkaitymas(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysRašymas:
		cpu.Eax = uint32(sysRašymas(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysAtverti:
		cpu.Eax = uint32(sysAtverti(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysAtverti(cpu.Ebx, ocreate|oRašymasonly|oAtmest, cpu.Ecx))
		return esp
	case SysUžverti:
		cpu.Eax = uint32(sysUžverti(int32(cpu.Ebx)))
		return esp
	case Syswaitpid:
		cpu.Eax = uint32(syswaitpid(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Syslseek:
		cpu.Eax = uint32(syslseek(int32(cpu.Ebx), int32(cpu.Ecx), cpu.Edx))
		return esp
	case Sysexecve:
		cpu.Eax = uint32(sysexecve(cpu, cpu.Ebx))
		return esp
	case Sysgetpid:
		cpu.Eax = Dabartinispid()
		return esp
	case Sysgetppid:
		cpu.Eax = Dabartinisparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysprieiti:
		cpu.Eax = uint32(sysprieiti(cpu.Ebx, cpu.Ecx))
		return esp
	case Syschdir:
		cpu.Eax = uint32(syschdir(cpu.Ebx))
		return esp
	case Sysgetcwd:
		cpu.Eax = uint32(sysgetcwd(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysdup:
		cpu.Eax = uint32(sysdup(int32(cpu.Ebx), 0))
		return esp
	case Sysdup2:
		cpu.Eax = uint32(sysdup2(int32(cpu.Ebx), int32(cpu.Ecx)))
		return esp
	case Syssocketcall:
		cpu.Eax = uint32(sysLizdascall(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfcntl:
		cpu.Eax = uint32(sysfcntl(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysstat, Syslstat:
		cpu.Eax = uint32(sysstat(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfstat:
		cpu.Eax = uint32(sysfstat(int32(cpu.Ebx), cpu.Ecx))
		return esp
	case Sysfsync:
		cpu.Eax = uint32(sysfsync(int32(cpu.Ebx)))
		return esp
	case Syssync:
		cpu.Eax = 0
		return esp
	case Sysuname:
		cpu.Eax = uint32(sysuname(cpu.Ebx))
		return esp
	case Sysbrk:
		cpu.Eax = sysbrk(cpu.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Spausdinti(cpu.Ebx)
		return esp

	default:
		console_2.MSpausdintixy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Spausdinti(esp)
		console_2.MSpausdinti(([]byte)(":"))
		console_2.MUnsignedinteger32Spausdinti(cpu.Eax)
		console_2.MSpausdinti(([]byte)(":"))
		console_2.MUnsignedinteger32Spausdinti(cpu.Ebx)
		console_2.MSpausdinti(([]byte)(":"))
		console_2.MUnsignedinteger32Spausdinti(cpu.Ecx)
		console_2.MSpausdinti(([]byte)(":"))
		console_2.MUnsignedinteger32Spausdinti(cpu.Edx)
		console_2.MSpausdinti(([]byte)("]"))
		cpu.Eax = syscallKlaida(Enosys)
		return esp
	}

	return esp
}

func initFailasdescriptor() {
	for i := 0; i < maksAtvertiFAILAI; i++ {
		atvertiFailasLentelė[i] = atvertiFailasAprašymas{}
	}
	for i := 0; i < len(procesasLentelė); i++ {
		procesasLentelė[i] = procesasįrašas{}
	}
	for i := 0; i < len(vietinissockets); i++ {
		vietinissockets[i] = vietinisdatagramLizdas{}
	}
	kitasephemeralPrievadas = 49152
	atvertiFailasLentelė[0] = atvertiFailasAprašymas{naudojama: true, rūšis: fARūšisstdin, parametrai: oSkaitymasonly}
	atvertiFailasLentelė[1] = atvertiFailasAprašymas{naudojama: true, rūšis: fARūšisconsole, parametrai: oRašymasonly}
	atvertiFailasLentelė[2] = atvertiFailasAprašymas{naudojama: true, rūšis: fARūšisconsole, parametrai: oRašymasonly}
}

func ieškotiProcesas(pid uint32) *procesasįrašas {
	for i := 0; i < len(procesasLentelė); i++ {
		if procesasLentelė[i].naudojama && procesasLentelė[i].pid == pid {
			return &procesasLentelė[i]
		}
	}
	return nil
}

func initializeProcesasfds(procesas *procesasįrašas) {
	for fA := int32(0); fA <= stderrFA; fA++ {
		procesas.fds[fA] = fAįrašas{naudojama: true, aprašymas: fA}
		atvertiFailasLentelė[fA].refs++
	}
}

func ensureDabartinisProcesas() *procesasįrašas {
	pid := Dabartinispid()
	if procesas := ieškotiProcesas(pid); procesas != nil {
		return procesas
	}
	for i := 0; i < len(procesasLentelė); i++ {
		if !procesasLentelė[i].naudojama {
			procesasLentelė[i] = procesasįrašas{
				naudojama:	true,
				pid:		pid,
				parent:		Dabartinisparentpid(),
				programabreak:	naudotojasheapbase,
			}
			initializeProcesasfds(&procesasLentelė[i])
			return &procesasLentelė[i]
		}
	}
	return nil
}

func getAtvertiFailasfor(procesas *procesasįrašas, fA int32) *atvertiFailasAprašymas {
	if procesas == nil || fA < 0 || fA >= maksFA || !procesas.fds[fA].naudojama {
		return nil
	}
	aprašymas := procesas.fds[fA].aprašymas
	if aprašymas < 0 || aprašymas >= maksAtvertiFAILAI || !atvertiFailasLentelė[aprašymas].naudojama {
		return nil
	}
	return &atvertiFailasLentelė[aprašymas]
}

func getAtvertiFailas(fA int32) *atvertiFailasAprašymas {
	return getAtvertiFailasfor(ensureDabartinisProcesas(), fA)
}

func allocateAtvertiFailas() int32 {
	for i := int32(3); i < maksAtvertiFAILAI; i++ {
		if !atvertiFailasLentelė[i].naudojama {
			atvertiFailasLentelė[i] = atvertiFailasAprašymas{naudojama: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateFA(procesas *procesasįrašas, aprašymas int32, minimumas int32) int32 {
	if procesas == nil {
		return Enfile
	}
	if minimumas < 0 || minimumas >= maksFA {
		return Einval
	}
	for fA := minimumas; fA < maksFA; fA++ {
		if !procesas.fds[fA].naudojama {
			procesas.fds[fA] = fAįrašas{naudojama: true, aprašymas: aprašymas}
			return fA
		}
	}
	return Emfile
}

func releaseAtvertiFailas(aprašymas int32) {
	if aprašymas < 0 || aprašymas >= maksAtvertiFAILAI {
		return
	}
	įrašas := &atvertiFailasLentelė[aprašymas]
	if įrašas.refs > 0 {
		įrašas.refs--
	}

	if įrašas.refs == 0 && aprašymas > stderrFA {
		if įrašas.rūšis == fARūšisLizdas && įrašas.aux < makssockets {
			vietinissockets[įrašas.aux] = vietinisdatagramLizdas{}
		}
		*įrašas = atvertiFailasAprašymas{}
	}
}

func užvertiProcesasFA(procesas *procesasįrašas, fA int32) int32 {
	if procesas == nil || getAtvertiFailasfor(procesas, fA) == nil {
		return Ebadf
	}
	aprašymas := procesas.fds[fA].aprašymas
	procesas.fds[fA] = fAįrašas{}
	releaseAtvertiFailas(aprašymas)
	return 0
}

func sysRašymas(fA int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	įrašas := getAtvertiFailas(fA)
	if įrašas == nil {
		return Ebadf
	}
	if įrašas.rūšis != fARūšisconsole {
		if įrašas.rūšis == fARūšisLizdas {
			return lizdasSiųstito(fA, address, count, 0, 0)
		}
		if įrašas.rūšis == fARūšisfat || įrašas.rūšis == fARūšisŠakniskatalogas {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBaitųfromRodyklė(uintptr(address), int(count), int(count))
	console_2.MSpausdinti(buffer)
	return int32(count)
}

func sysSkaitymas(fA int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	įrašas := getAtvertiFailas(fA)
	if įrašas == nil {
		return Ebadf
	}
	if įrašas.rūšis == fARūšisstdin {
		return skaitymasstdin(address, count)
	}
	if įrašas.rūšis == fARūšisŠakniskatalogas {
		return Eisdir
	}
	if įrašas.rūšis == fARūšisLizdas {
		return lizdasreceivefrom(fA, address, count, 0, 0)
	}
	if įrašas.rūšis != fARūšisfat {
		return Ebadf
	}
	if įrašas.pozicija >= įrašas.dydis {
		return 0
	}
	remaining := įrašas.dydis - įrašas.pozicija
	if count > remaining {
		count = remaining
	}
	buffer := GetBaitųfromRodyklė(uintptr(address), int(count), int(count))
	return skaitymasvfsFailas(įrašas, buffer, count)
}

func sysAtverti(kELIASaddress uint32, parametrai uint32, rEŽIMAS uint32) int32 {
	_ = rEŽIMAS
	if kELIASaddress == 0 {
		return Efault
	}
	prieitiREŽIMAS := parametrai & 3
	if prieitiREŽIMAS == oRašymasonly || prieitiREŽIMAS == oSkaitymasRašymas || (parametrai&(ocreate|oAtmest|oappend)) != 0 {
		return Erofs
	}

	procesas := ensureDabartinisProcesas()
	if procesas == nil {
		return Enfile
	}
	aprašymas := allocateAtvertiFailas()
	if aprašymas < 0 {
		return aprašymas
	}
	įrašas := &atvertiFailasLentelė[aprašymas]
	įrašas.parametrai = parametrai
	if isŠaknisKELIAS(kELIASaddress) {
		įrašas.rūšis = fARūšisŠakniskatalogas
		įrašas.dydis = 0
	} else {
		pavadinimaslen, pavadinimas := kopijuotiKELIAS(kELIASaddress)
		if pavadinimaslen == 0 {
			*įrašas = atvertiFailasAprašymas{}
			return Enoent
		}
		dydis := failasDydis(pavadinimas[:pavadinimaslen])
		if dydis == 0 {
			*įrašas = atvertiFailasAprašymas{}
			return Enoent
		}
		if (parametrai & okatalogas) != 0 {
			*įrašas = atvertiFailasAprašymas{}
			return Enotdir
		}
		įrašas.rūšis = fARūšisfat
		įrašas.dydis = dydis
		įrašas.pavadinimaslen = pavadinimaslen
		įrašas.pavadinimas = pavadinimas
	}

	fA := allocateFA(procesas, aprašymas, 3)
	if fA < 0 {
		*įrašas = atvertiFailasAprašymas{}
		return fA
	}
	return fA
}

func sysUžverti(fA int32) int32 {
	return užvertiProcesasFA(ensureDabartinisProcesas(), fA)
}

func sysdup(fA int32, minimumas int32) int32 {
	procesas := ensureDabartinisProcesas()
	įrašas := getAtvertiFailasfor(procesas, fA)
	if įrašas == nil {
		return Ebadf
	}
	naujasFA := allocateFA(procesas, procesas.fds[fA].aprašymas, minimumas)
	if naujasFA >= 0 {
		įrašas.refs++
	}
	return naujasFA
}

func sysdup2(oldFA int32, naujasFA int32) int32 {
	procesas := ensureDabartinisProcesas()
	įrašas := getAtvertiFailasfor(procesas, oldFA)
	if įrašas == nil {
		return Ebadf
	}
	if naujasFA < 0 || naujasFA >= maksFA {
		return Ebadf
	}
	if oldFA == naujasFA {
		return naujasFA
	}
	if procesas.fds[naujasFA].naudojama {
		užvertiProcesasFA(procesas, naujasFA)
	}
	procesas.fds[naujasFA] = fAįrašas{naudojama: true, aprašymas: procesas.fds[oldFA].aprašymas}
	įrašas.refs++
	return naujasFA
}

func sysfcntl(fA int32, komanda uint32, argument uint32) int32 {
	procesas := ensureDabartinisProcesas()
	įrašas := getAtvertiFailasfor(procesas, fA)
	if įrašas == nil {
		return Ebadf
	}
	switch komanda {
	case fdupFA:
		return sysdup(fA, int32(argument))
	case fgetFA:
		return int32(procesas.fds[fA].fAParametrai)
	case fnustatytaFA:
		procesas.fds[fA].fAParametrai = argument & fAcloexec
		return 0
	case fgetfl:
		return int32(įrašas.parametrai)
	case fnustatytafl:
		įrašas.parametrai = (įrašas.parametrai & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fA int32, offset int32, whence uint32) int32 {
	įrašas := getAtvertiFailas(fA)
	if įrašas == nil {
		return Ebadf
	}
	if įrašas.rūšis != fARūšisfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seeknustatyta:
		base = 0
	case seekDabartinis:
		base = int64(įrašas.pozicija)
	case seekPab:
		base = int64(įrašas.dydis)
	default:
		return Einval
	}
	pozicija_2 := base + int64(offset)
	if pozicija_2 < 0 || pozicija_2 > 0x7FFFFFFF {
		return Einval
	}
	įrašas.pozicija = uint32(pozicija_2)
	return int32(įrašas.pozicija)
}

func skaitymasvfsFailas(įrašas *atvertiFailasAprašymas, tikslas_2 []byte, count uint32) int32 {
	atmintismanager := &mem.TAtmintismanager{}
	tmpRodyklė := atmintismanager.Malloc(įrašas.dydis)
	if tmpRodyklė == nil {
		return Einval
	}
	tmp := GetBaitųfromRodyklė(uintptr(tmpRodyklė), int(įrašas.dydis), int(įrašas.dydis))
	skaitymasFailas(įrašas.pavadinimas[:įrašas.pavadinimaslen], tmp)
	copy(tikslas_2[:count], tmp[įrašas.pozicija:įrašas.pozicija+count])
	įrašas.pozicija += count
	atmintismanager.Laisva(tmpRodyklė)
	return int32(count)
}

func isŠaknisKELIAS(kELIASaddress uint32) bool {
	if kELIASaddress == 0 {
		return false
	}
	kELIAS := GetBaitųfromRodyklė(uintptr(kELIASaddress), 4, 4)
	if kELIAS[0] == '/' && kELIAS[1] == 0 {
		return true
	}
	if kELIAS[0] == '.' && kELIAS[1] == 0 {
		return true
	}
	if kELIAS[0] == '/' && kELIAS[1] == '.' && kELIAS[2] == 0 {
		return true
	}
	return false
}

func sysprieiti(kELIASaddress uint32, rEŽIMAS uint32) int32 {
	if kELIASaddress == 0 {
		return Efault
	}
	if (rEŽIMAS & ^uint32(7)) != 0 {
		return Einval
	}
	isŠaknis := isŠaknisKELIAS(kELIASaddress)
	exists := isŠaknis
	if !exists {
		pavadinimaslen, pavadinimas := kopijuotiKELIAS(kELIASaddress)
		exists = pavadinimaslen != 0 && failasDydis(pavadinimas[:pavadinimaslen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (rEŽIMAS & 2) != 0 {
		return Eacces
	}

	if (rEŽIMAS&1) != 0 && !isŠaknis {
		return Eacces
	}
	return 0
}

func syschdir(kELIASaddress uint32) int32 {
	if kELIASaddress == 0 {
		return Efault
	}
	if !isŠaknisKELIAS(kELIASaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, dydis uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if dydis < 2 {
		return Erange
	}
	buffer_2 := GetBaitųfromRodyklė(uintptr(bufferaddress), int(dydis), int(dydis))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, rEŽIMAS uint32, dydis uint32, inodas uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Įrenginys = 1
	stat.Ino = inodas
	stat.REŽIMAS = rEŽIMAS
	stat.Nlink = 1
	stat.Dydis_2 = int32(dydis)
	stat.Blksize = 512
	stat.Blokas = int32((dydis + 511) / 512)
	return 0
}

func sysstat(kELIASaddress uint32, stataddress uint32) int32 {
	if kELIASaddress == 0 {
		return Efault
	}
	if isŠaknisKELIAS(kELIASaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	pavadinimaslen, pavadinimas := kopijuotiKELIAS(kELIASaddress)
	if pavadinimaslen == 0 {
		return Enoent
	}
	dydis := failasDydis(pavadinimas[:pavadinimaslen])
	if dydis == 0 {
		return Enoent
	}
	inodas := uint32(2)
	for i := uint32(0); i < pavadinimaslen; i++ {
		inodas = inodas*33 + uint32(pavadinimas[i])
	}
	return fillposixstat(stataddress, sifreg|0444, dydis, inodas)
}

func sysfstat(fA int32, stataddress uint32) int32 {
	įrašas := getAtvertiFailas(fA)
	if įrašas == nil {
		return Ebadf
	}
	switch įrašas.rūšis {
	case fARūšisstdin, fARūšisconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fA+1))
	case fARūšisŠakniskatalogas:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fARūšisfat:
		return fillposixstat(stataddress, sifreg|0444, įrašas.dydis, uint32(fA+2))
	case fARūšisLizdas:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fA+2))
	}
	return Ebadf
}

func sysfsync(fA int32) int32 {
	if getAtvertiFailas(fA) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	procesas := ensureDabartinisProcesas()
	if procesas == nil {
		return 0
	}
	if procesas.programabreak == 0 {
		procesas.programabreak = naudotojasheapbase
	}
	if address_2 == 0 {
		return procesas.programabreak
	}
	if address_2 < naudotojasheapbase || address_2 > naudotojasheapRiba {
		return procesas.programabreak
	}
	procesas.programabreak = address_2
	return procesas.programabreak
}

func kopijuotiutslaukas(tikslas *[65]byte, reikšmė string) {
	riba := len(reikšmė)
	if riba > 64 {
		riba = 64
	}
	for i := 0; i < riba; i++ {
		tikslas[i] = reikšmė[i]
	}
	tikslas[riba] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	pavadinimas := (*posixutsname)(Pointer(uintptr(address_2)))
	*pavadinimas = posixutsname{}
	kopijuotiutslaukas(&pavadinimas.Sysname, "EngOS")
	kopijuotiutslaukas(&pavadinimas.Nodename, "engos")
	kopijuotiutslaukas(&pavadinimas.Release, "0.1-posix")
	kopijuotiutslaukas(&pavadinimas.Versija, "POSIX.1-2017 phase 1")
	kopijuotiutslaukas(&pavadinimas.Machine, "i386")
	return 0
}

func swapunsignedinteger16(reikšmė uint16) uint16 {
	return (reikšmė << 8) | (reikšmė >> 8)
}

func lizdascallargument(argumentai_2 uint32, rodyklė uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumentai_2 + rodyklė*4)))
}

func lizdasforFA(fA int32) (*vietinisdatagramLizdas, int32) {
	įrašas := getAtvertiFailas(fA)
	if įrašas == nil || įrašas.rūšis != fARūšisLizdas || įrašas.aux >= makssockets {
		return nil, Ebadf
	}
	lizdas := &vietinissockets[įrašas.aux]
	if !lizdas.naudojama {
		return nil, Ebadf
	}
	return lizdas, 0
}

func allocateLizdas(domenas uint32, lizdasTipas uint32, protocol uint32) int32 {
	if domenas != afinet {
		return Eafnosupport
	}
	if lizdasTipas != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	procesas := ensureDabartinisProcesas()
	if procesas == nil {
		return Enfile
	}
	lizdasRodyklė := -1
	for i := 0; i < makssockets; i++ {
		if !vietinissockets[i].naudojama {
			lizdasRodyklė = i
			break
		}
	}
	if lizdasRodyklė < 0 {
		return Enfile
	}
	aprašymas := allocateAtvertiFailas()
	if aprašymas < 0 {
		return aprašymas
	}
	vietinissockets[lizdasRodyklė] = vietinisdatagramLizdas{naudojama: true}
	įrašas := &atvertiFailasLentelė[aprašymas]
	įrašas.rūšis = fARūšisLizdas
	įrašas.parametrai = oSkaitymasRašymas
	įrašas.aux = uint32(lizdasRodyklė)
	fA := allocateFA(procesas, aprašymas, 3)
	if fA < 0 {
		vietinissockets[lizdasRodyklė] = vietinisdatagramLizdas{}
		*įrašas = atvertiFailasAprašymas{}
		return fA
	}
	return fA
}

func lizdasaddress(address_2 uint32, trukmė uint32) (*lizdasaddressiEv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if trukmė < 16 {
		return nil, Einval
	}
	rEZULTATAS := (*lizdasaddressiEv4)(Pointer(uintptr(address_2)))
	if rEZULTATAS.Family != afinet {
		return nil, Eafnosupport
	}
	return rEZULTATAS, 0
}

func prievadasĮNaudoti(prievadas uint16, except *vietinisdatagramLizdas) bool {
	for i := 0; i < makssockets; i++ {
		lizdas := &vietinissockets[i]
		if lizdas != except && lizdas.naudojama && lizdas.bound && lizdas.vietinis.Prievadas == prievadas {
			return true
		}
	}
	return false
}

func bindephemeral(lizdas *vietinisdatagramLizdas) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		prievadas := swapunsignedinteger16(kitasephemeralPrievadas)
		kitasephemeralPrievadas++
		if kitasephemeralPrievadas < 49152 {
			kitasephemeralPrievadas = 49152
		}
		if !prievadasĮNaudoti(prievadas, lizdas) {
			lizdas.vietinis = lizdasaddressiEv4{Family: afinet, Prievadas: prievadas, Address: 0x0100007F}
			lizdas.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func lizdasbind(fA int32, address_2 uint32, trukmė uint32) int32 {
	lizdas, klaidos := lizdasforFA(fA)
	if klaidos != 0 {
		return klaidos
	}
	requested, klaidos := lizdasaddress(address_2, trukmė)
	if klaidos != 0 {
		return klaidos
	}
	if lizdas.bound {
		return Einval
	}
	if requested.Prievadas == 0 {
		return bindephemeral(lizdas)
	}
	if prievadasĮNaudoti(requested.Prievadas, lizdas) {
		return Eaddrinuse
	}
	lizdas.vietinis = *requested
	lizdas.bound = true
	return 0
}

func lizdasPrisijungti(fA int32, address_2 uint32, trukmė uint32) int32 {
	lizdas, klaidos := lizdasforFA(fA)
	if klaidos != 0 {
		return klaidos
	}
	nutolęs, klaidos := lizdasaddress(address_2, trukmė)
	if klaidos != 0 {
		return klaidos
	}
	if !lizdas.bound {
		if klaidos := bindephemeral(lizdas); klaidos != 0 {
			return klaidos
		}
	}
	lizdas.nutolęs = *nutolęs
	lizdas.connected = true
	return 0
}

func lizdasSiųstito(fA int32, bufferaddress_2 uint32, trukmė uint32, tikslasaddress uint32, tikslasTrukmė uint32) int32 {
	lizdas, klaidos := lizdasforFA(fA)
	if klaidos != 0 {
		return klaidos
	}
	if trukmė > maksdatagramDydis {
		return Emsgsize
	}
	if trukmė != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var tikslas lizdasaddressiEv4
	if tikslasaddress != 0 {
		address_2, addressKlaida := lizdasaddress(tikslasaddress, tikslasTrukmė)
		if addressKlaida != 0 {
			return addressKlaida
		}
		tikslas = *address_2
	} else {
		if !lizdas.connected {
			return Enotconn
		}
		tikslas = lizdas.nutolęs
	}
	if !lizdas.bound {
		if bindKlaida := bindephemeral(lizdas); bindKlaida != 0 {
			return bindKlaida
		}
	}
	var receiver *vietinisdatagramLizdas
	for i := 0; i < makssockets; i++ {
		candidate := &vietinissockets[i]
		if candidate.naudojama && candidate.bound && candidate.vietinis.Prievadas == tikslas.Prievadas &&
			(candidate.vietinis.Address == 0 || candidate.vietinis.Address == tikslas.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksLizdaspaketų {
		return Eagain
	}
	packet := &receiver.paketų[receiver.tail]
	*packet = lizdaspacket{naudojama: true, dydis: trukmė, šaltinis: lizdas.vietinis}
	if trukmė != 0 {
		šaltinis := GetBaitųfromRodyklė(uintptr(bufferaddress_2), int(trukmė), int(trukmė))
		copy(packet.data[:trukmė], šaltinis)
	}
	receiver.tail = (receiver.tail + 1) % maksLizdaspaketų
	receiver.count++
	return int32(trukmė)
}

func lizdasreceivefrom(fA int32, bufferaddress_2 uint32, trukmė uint32, šaltinisaddress uint32, šaltinisTrukmėaddress uint32) int32 {
	lizdas, klaidos := lizdasforFA(fA)
	if klaidos != 0 {
		return klaidos
	}
	if trukmė != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if lizdas.count == 0 {
		return Eagain
	}
	packet := &lizdas.paketų[lizdas.head]
	kopijuotiTrukmė := packet.dydis
	if kopijuotiTrukmė > trukmė {
		kopijuotiTrukmė = trukmė
	}
	if kopijuotiTrukmė != 0 {
		tikslas := GetBaitųfromRodyklė(uintptr(bufferaddress_2), int(kopijuotiTrukmė), int(kopijuotiTrukmė))
		copy(tikslas, packet.data[:kopijuotiTrukmė])
	}
	if šaltinisaddress != 0 {
		if šaltinisTrukmėaddress == 0 {
			return Efault
		}
		providedTrukmė := (*uint32)(Pointer(uintptr(šaltinisTrukmėaddress)))
		if *providedTrukmė >= 16 {
			*(*lizdasaddressiEv4)(Pointer(uintptr(šaltinisaddress))) = packet.šaltinis
		}
		*providedTrukmė = 16
	}
	*packet = lizdaspacket{}
	lizdas.head = (lizdas.head + 1) % maksLizdaspaketų
	lizdas.count--
	return int32(kopijuotiTrukmė)
}

func kopijuotiLizdasPavadinimas(fA int32, address_2 uint32, trukmėaddress uint32, peer bool) int32 {
	lizdas, klaidos := lizdasforFA(fA)
	if klaidos != 0 {
		return klaidos
	}
	if address_2 == 0 || trukmėaddress == 0 {
		return Efault
	}
	trukmė := (*uint32)(Pointer(uintptr(trukmėaddress)))
	if *trukmė < 16 {
		*trukmė = 16
		return Einval
	}
	if peer {
		if !lizdas.connected {
			return Enotconn
		}
		*(*lizdasaddressiEv4)(Pointer(uintptr(address_2))) = lizdas.nutolęs
	} else {
		if !lizdas.bound {
			if bindKlaida := bindephemeral(lizdas); bindKlaida != 0 {
				return bindKlaida
			}
		}
		*(*lizdasaddressiEv4)(Pointer(uintptr(address_2))) = lizdas.vietinis
	}
	*trukmė = 16
	return 0
}

func sysLizdascall(call uint32, argumentai_2 uint32) int32 {
	if argumentai_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateLizdas(lizdascallargument(argumentai_2, 0), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2))
	case 2:
		return lizdasbind(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2))
	case 3:
		return lizdasPrisijungti(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopijuotiLizdasPavadinimas(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), false)
	case 7:
		return kopijuotiLizdasPavadinimas(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), true)
	case 9:
		return lizdasSiųstito(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), 0, 0)
	case 10:
		return lizdasreceivefrom(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), 0, 0)
	case 11:
		return lizdasSiųstito(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), lizdascallargument(argumentai_2, 4), lizdascallargument(argumentai_2, 5))
	case 12:
		return lizdasreceivefrom(int32(lizdascallargument(argumentai_2, 0)), lizdascallargument(argumentai_2, 1), lizdascallargument(argumentai_2, 2), lizdascallargument(argumentai_2, 4), lizdascallargument(argumentai_2, 5))
	case 13:
		if _, klaidos := lizdasforFA(int32(lizdascallargument(argumentai_2, 0))); klaidos != 0 {
			return klaidos
		}
		return 0
	case 14:
		if _, klaidos := lizdasforFA(int32(lizdascallargument(argumentai_2, 0))); klaidos != 0 {
			return klaidos
		}
		return 0
	}
	return Eopnotsupp
}

func skaitymasstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaitųfromRodyklė(uintptr(address), int(count), int(count))
	var n uint32
	for n < count {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputbyte(c byte) {
	kitas := (stdinRašymas + 1) % uint32(len(stdinbuffer))
	if kitas == stdinSkaitymas {
		return
	}
	stdinbuffer[stdinRašymas] = c
	stdinRašymas = kitas
}

func stdingetblocking() byte {
	for stdinSkaitymas == stdinRašymas {
		sc := pollKlaviatūrascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinSkaitymas]
	stdinSkaitymas = (stdinSkaitymas + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlaviatūrascancode() byte {
	for (PrievadasSkaitymasbyte(0x64) & 0x01) == 0 {
	}
	sc := PrievadasSkaitymasbyte(0x60)
	return scancodetobyte(sc)
}

func scancodetobyte(sc uint8) byte {
	if sc >= 0x80 {
		return 0
	}
	switch sc {
	case 0x02:
		return '1'
	case 0x03:
		return '2'
	case 0x04:
		return '3'
	case 0x05:
		return '4'
	case 0x06:
		return '5'
	case 0x07:
		return '6'
	case 0x08:
		return '7'
	case 0x09:
		return '8'
	case 0x0A:
		return '9'
	case 0x0B:
		return '0'
	case 0x10:
		return 'q'
	case 0x11:
		return 'w'
	case 0x12:
		return 'e'
	case 0x13:
		return 'r'
	case 0x14:
		return 't'
	case 0x15:
		return 'y'
	case 0x16:
		return 'u'
	case 0x17:
		return 'i'
	case 0x18:
		return 'o'
	case 0x19:
		return 'p'
	case 0x1E:
		return 'a'
	case 0x1F:
		return 's'
	case 0x20:
		return 'd'
	case 0x21:
		return 'f'
	case 0x22:
		return 'g'
	case 0x23:
		return 'h'
	case 0x24:
		return 'j'
	case 0x25:
		return 'k'
	case 0x26:
		return 'l'
	case 0x2C:
		return 'z'
	case 0x2D:
		return 'x'
	case 0x2E:
		return 'c'
	case 0x2F:
		return 'v'
	case 0x30:
		return 'b'
	case 0x31:
		return 'n'
	case 0x32:
		return 'm'
	case 0x33:
		return ','
	case 0x34:
		return '.'
	case 0x35:
		return '/'
	case 0x1C:
		return '\n'
	case 0x39:
		return ' '
	}
	return 0
}

func kopijuotiVykdytivector(address_2 uint32, rEZULTATAS *vykdytivector) int32 {
	*rEZULTATAS = vykdytivector{}
	if address_2 == 0 {
		return 0
	}
	for rodyklė := uint32(0); rodyklė < maksVykdytivectorįrašas; rodyklė++ {
		eilutėaddress := *(*uint32)(Pointer(uintptr(address_2 + rodyklė*4)))
		if eilutėaddress == 0 {
			rEZULTATAS.count = rodyklė
			return 0
		}
		terminated := false
		for trukmė := uint32(0); trukmė <= maksVykdytiEilutėTrukmė; trukmė++ {
			reikšmė := *(*byte)(Pointer(uintptr(eilutėaddress + trukmė)))
			rEZULTATAS.reikšmės[rodyklė][trukmė] = reikšmė
			if reikšmė == 0 {
				rEZULTATAS.lengths[rodyklė] = trukmė
				terminated = true
				break
			}
		}
		if !terminated {
			return E2big
		}
	}
	return E2big
}

func pushVykdytiunsignedinteger32(stack *uint32, reikšmė uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = reikšmė
}

func setupVykdytistack(cpu *TcpuBūsena, argumentai_2 *vykdytivector, environment *vykdytivector) int32 {
	const stackBaitų uint32 = 4096
	if !MakeSritisPrivatuswritable(getcr3(), NaudotojasstackViršuje-stackBaitų, stackBaitų) {
		return Enomem
	}
	stack := NaudotojasstackViršuje
	var argumentpointers [maksVykdytivectorįrašas]uint32
	var environmentpointers [maksVykdytivectorįrašas]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		trukmė := environment.lengths[i] + 1
		stack -= trukmė
		tikslas := GetBaitųfromRodyklė(uintptr(stack), int(trukmė), int(trukmė))
		copy(tikslas, environment.reikšmės[i][:trukmė])
		environmentpointers[i] = stack
	}
	for i := int(argumentai_2.count) - 1; i >= 0; i-- {
		trukmė := argumentai_2.lengths[i] + 1
		stack -= trukmė
		tikslas := GetBaitųfromRodyklė(uintptr(stack), int(trukmė), int(trukmė))
		copy(tikslas, argumentai_2.reikšmės[i][:trukmė])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushVykdytiunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushVykdytiunsignedinteger32(&stack, environmentpointers[i])
	}
	pushVykdytiunsignedinteger32(&stack, 0)
	for i := int(argumentai_2.count) - 1; i >= 0; i-- {
		pushVykdytiunsignedinteger32(&stack, argumentpointers[i])
	}
	pushVykdytiunsignedinteger32(&stack, argumentai_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func užvertiĮjungtaVykdyti(procesas *procesasįrašas) {
	if procesas == nil {
		return
	}
	for fA := int32(0); fA < maksFA; fA++ {
		if procesas.fds[fA].naudojama && (procesas.fds[fA].fAParametrai&fAcloexec) != 0 {
			užvertiProcesasFA(procesas, fA)
		}
	}
}

func sysexecve(cpu *TcpuBūsena, kELIASaddress uint32) int32 {
	if kELIASaddress == 0 {
		return Efault
	}
	var argumentai_2 vykdytivector
	var environment vykdytivector
	if rEZULTATAS := kopijuotiVykdytivector(cpu.Ecx, &argumentai_2); rEZULTATAS < 0 {
		return rEZULTATAS
	}
	if rEZULTATAS := kopijuotiVykdytivector(cpu.Edx, &environment); rEZULTATAS < 0 {
		return rEZULTATAS
	}
	pavadinimaslen, pavadinimas := kopijuotiKELIAS(kELIASaddress)
	if pavadinimaslen == 0 {
		return Enoent
	}
	dydis := failasDydis(pavadinimas[:pavadinimaslen])
	if dydis == 0 {
		return Enoent
	}
	atmintismanager := &mem.TAtmintismanager{}
	failasRodyklė := atmintismanager.Malloc(dydis)
	if failasRodyklė == nil {
		return Einval
	}
	data := GetBaitųfromRodyklė(uintptr(failasRodyklė), int(dydis), int(dydis))
	skaitymasFailas(pavadinimas[:pavadinimaslen], data)
	if dydis < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		atmintismanager.Laisva(failasRodyklė)
		return Enoexec
	}
	loader := Elf{}
	įrašas := loader.Getįrašas(data)
	loader.Parse(data, getcr3())
	atmintismanager.Laisva(failasRodyklė)
	if rEZULTATAS := setupVykdytistack(cpu, &argumentai_2, &environment); rEZULTATAS < 0 {
		return rEZULTATAS
	}
	užvertiĮjungtaVykdyti(ensureDabartinisProcesas())
	cpu.Eip = įrašas
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuBūsena) int32 {
	parentpid := Dabartinispid()
	if ensureDabartinisProcesas() == nil {
		return Enfile
	}
	pid := allocateProcesas(parentpid)
	if pid == 0 {
		return Einval
	}
	atmintismanager := &mem.TAtmintismanager{}
	threadRodyklė := atmintismanager.Malloc(uint32(Sizeof(TThread{})))
	stackRodyklė := atmintismanager.Malloc(ThreadstackDydis)
	childPuslapiskatalogas := CloneaddressTarpascow(getcr3())
	if threadRodyklė == nil || stackRodyklė == nil || childPuslapiskatalogas == 0 {
		išmestiProcesas(pid)
		return Einval
	}
	child := (*TThread)(threadRodyklė)
	child.Stack = uint32(uintptr(stackRodyklė))
	child.CpuBūsena = (*TcpuBūsena)(Pointer(uintptr(stackRodyklė) + ThreadstackDydis - Sizeof(TcpuBūsena{})))
	*child.CpuBūsena = *cpu
	child.CpuBūsena.Eax = 0
	child.Naudotojasstack_2 = cpu.Esp
	child.NaudotojasstackDydis_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Puslapiskatalogasįrašas = childPuslapiskatalogas
	child.ThreadBūsena = Pasiruošęs
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Pridėtirunnablethread(child)
	return int32(pid)
}

func sysIšeiti(būsena uint32) {
	pid := Dabartinispid()
	for i := 0; i < len(procesasLentelė); i++ {
		if procesasLentelė[i].naudojama && procesasLentelė[i].pid == pid {
			užvertiVisiProcesasfds(&procesasLentelė[i])
			procesasLentelė[i].išėjo = true
			procesasLentelė[i].būsena = (būsena & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, būsenaaddress uint32, parinktys uint32) int32 {
	if (parinktys & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Dabartinispid()
	foundchild := false
	for i := 0; i < len(procesasLentelė); i++ {
		p := &procesasLentelė[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.naudojama && matches && p.parent == parentpid {
			foundchild = true
			if p.išėjo {
				if būsenaaddress != 0 {
					*(*uint32)(Pointer(uintptr(būsenaaddress))) = p.būsena
				}
				childpid := p.pid
				*p = procesasįrašas{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (parinktys & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProcesas(parent uint32) uint32 {
	parentProcesas := ieškotiProcesas(parent)
	pid := Allocatepid()
	for i := 0; i < len(procesasLentelė); i++ {
		if !procesasLentelė[i].naudojama {
			procesasLentelė[i] = procesasįrašas{
				naudojama:	true,
				pid:		pid,
				parent:		parent,
				programabreak:	naudotojasheapbase,
			}
			if parentProcesas != nil {
				procesasLentelė[i].programabreak = parentProcesas.programabreak
				for fA := 0; fA < maksFA; fA++ {
					if parentProcesas.fds[fA].naudojama {
						procesasLentelė[i].fds[fA] = parentProcesas.fds[fA]
						aprašymas := parentProcesas.fds[fA].aprašymas
						if aprašymas >= 0 && aprašymas < maksAtvertiFAILAI {
							atvertiFailasLentelė[aprašymas].refs++
						}
					}
				}
			} else {
				initializeProcesasfds(&procesasLentelė[i])
			}
			return pid
		}
	}
	return 0
}

func užvertiVisiProcesasfds(procesas *procesasįrašas) {
	if procesas == nil {
		return
	}
	for fA := int32(0); fA < maksFA; fA++ {
		if procesas.fds[fA].naudojama {
			užvertiProcesasFA(procesas, fA)
		}
	}
}

func išmestiProcesas(pid uint32) {
	procesas := ieškotiProcesas(pid)
	if procesas == nil {
		return
	}
	užvertiVisiProcesasfds(procesas)
	*procesas = procesasįrašas{}
}

func kopijuotiKELIAS(kELIASaddress uint32) (uint32, [12]byte) {
	var pavadinimas [12]byte
	if kELIASaddress == 0 {
		return 0, pavadinimas
	}
	raw := GetBaitųfromRodyklė(uintptr(kELIASaddress), 64, 64)
	var n uint32
	for i := 0; i < 64 && n < 12; i++ {
		c := raw[i]
		if c == 0 {
			break
		}
		if c == '/' {
			n = 0
			continue
		}
		if c >= 'a' && c <= 'z' {
			c = c - 32
		}
		if c == '.' {
			continue
		}
		pavadinimas[n] = c
		n++
	}
	return n, pavadinimas
}

func failasDydis(failopavadinimas []byte) uint32 {
	var ata0s = TIšsamiauTechnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionLentelė{}
	partition.Skaitymaspartition(&ata0s)

	bios := TBiosparameterBlokas32{}
	dydis := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas)
	ata0s.Flush()
	return dydis
}

func skaitymasFailas(failopavadinimas []byte, data []byte) {
	var ata0s = TIšsamiauTechnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionLentelė{}
	partition.Skaitymaspartition(&ata0s)

	bios := TBiosparameterBlokas32{}
	bios.Skaitymas(&ata0s, partition.Mbr.Primarypartition[0], failopavadinimas, data)
	ata0s.Flush()
}

func getcr3() uint32
