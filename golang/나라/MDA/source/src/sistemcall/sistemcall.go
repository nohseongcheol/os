/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemcall

import . "unsafe"

import . "intrerupere"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "fișierSistem/msdospartition"
import . "fișierSistem/fat"
import . "fișierSistem/elf"
import mem "memoriemanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualăMemorie"

var console_2 = TConsole{}

type TSyscall struct {
	TIntreruperehandler
}

const (
	SysIeșire	uint32	= 1
	Sysfork		uint32	= 2
	SysCitire	uint32	= 3
	SysScriere	uint32	= 4
	SysDeschide	uint32	= 5
	SysÎnchide	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysacces	uint32	= 33
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
	SysrtIeșire	uint32	= 252

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
	stdinDescriptorfișier	int32	= 0
	stdoutDescriptorfișier	int32	= 1
	stderrDescriptorfișier	int32	= 2
	maxDescriptorfișier		= 32
	maxDeschideFIȘIERE		= 128
)

type descriptorfișierînregistrare struct {
	folosit				bool
	descriere			int32
	descriptorfișierIndicatori	uint32
}

type deschideFișierDescriere struct {
	folosit		bool
	refs		uint32
	gen		uint32
	indicatori	uint32
	poziție		uint32
	mărime		uint32
	nume		[12]byte
	numelen		uint32
	aux		uint32
}

const (
	descriptorfișierGenNimic		uint32	= 0
	descriptorfișierGenfat			uint32	= 1
	descriptorfișierGenstdin		uint32	= 2
	descriptorfișierGenconsole		uint32	= 3
	descriptorfișierGenRădăcinăDirector	uint32	= 4
	descriptorfișierGensocket		uint32	= 5

	oCitireonly	uint32	= 0
	oScriereonly	uint32	= 1
	oCitireScriere	uint32	= 2
	ocreate		uint32	= 0x40
	oTrunchiază	uint32	= 0x200
	oappend		uint32	= 0x400
	oDirector	uint32	= 0x10000

	seekdefinit	uint32	= 0
	seekCurentă	uint32	= 1
	seekSfârșit	uint32	= 2

	fdupDescriptorfișier		uint32	= 0
	fgetDescriptorfișier		uint32	= 1
	fdefinitDescriptorfișier	uint32	= 2
	fgetfl				uint32	= 3
	fdefinitfl			uint32	= 4
	descriptorfișiercloexec		uint32	= 1

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
	maxsockets		= 32
	maxsocketpachete	= 8
	maxdatagramMărime	= 512
)

type socketaddressiVp4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	folosit	bool
	mărime	uint32
	sursă	socketaddressiVp4
	data	[maxdatagramMărime]byte
}

type localdatagramsocket struct {
	folosit		bool
	bound		bool
	connected	bool
	local		socketaddressiVp4
	ladistanță	socketaddressiVp4
	head		uint32
	tail		uint32
	count		uint32
	pachete		[maxsocketpachete]socketpacket
}

type posixstat struct {
	Dispozitiv	uint32
	Ino		uint32
	MOD		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Mărime_2	int32
	Blksize		int32
	Bloc		int32
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
	Versiune	[65]byte
	Machine		[65]byte
}

const (
	maxExecuțievectorînregistrare	= 16
	maxExecuțieȘirDurată		= 63
)

type execuțievector struct {
	count	uint32
	lengths	[maxExecuțievectorînregistrare]uint32
	values	[maxExecuțievectorînregistrare][maxExecuțieȘirDurată + 1]byte
}

type procesînregistrare struct {
	folosit		bool
	pid		uint32
	părinte		uint32
	terminat	bool
	stare		uint32
	programbreak	uint32
	fds		[maxDescriptorfișier]descriptorfișierînregistrare
}

type șirheader struct {
	Data	uintptr
	Len	int
}

func syscallEroare(erori int32) uint32 {
	return *(*uint32)(Pointer(&erori))
}

var deschideFișierTabel [maxDeschideFIȘIERE]deschideFișierDescriere
var procesTabel [32]procesînregistrare
var localsockets [maxsockets]localdatagramsocket
var înainteephemeralport uint16 = 49152

const (
	utilizatorheapbase	uint32	= 0x06000000
	utilizatorheapLimită	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinCitire uint32
var stdinScriere uint32

func Intrerupere(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIeșire_2(index uint32) {
	Syscall(SysIeșire, index)
}

func SysCitire_2(descriptorfișier uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysCitire, descriptorfișier, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysTipăreștestr(buffer string) {
	h := (*șirheader)(Pointer(&buffer))
	Syscall(SysScriere, uint32(stdoutDescriptorfișier), uint32(h.Data), uint32(h.Len))
}

func SysTipăreșteunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysScriere, uint32(stdoutDescriptorfișier), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysDeschide_2(cALE uintptr, indicatori uint32, mOD uint32) int32 {
	return int32(Syscall(SysDeschide, uint32(cALE), indicatori, mOD))
}

func SysÎnchide_2(descriptorfișier uint32) int32 {
	return int32(Syscall(SysÎnchide, descriptorfișier))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametri ...uint32) uint32 {

	l := len(parametri)
	switch l {
	case 1:
		return Intrerupere(parametri[0], 0, 0, 0, 0, 0)
	case 2:
		return Intrerupere(parametri[0], parametri[1], 0, 0, 0, 0)
	case 3:
		return Intrerupere(parametri[0], parametri[1], parametri[2], 0, 0, 0)
	case 4:
		return Intrerupere(parametri[0], parametri[1], parametri[2], parametri[3], 0, 0)
	case 5:
		return Intrerupere(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], 0)
	case 6:
		return Intrerupere(parametri[0], parametri[1], parametri[2], parametri[3], parametri[4], parametri[5])
	default:
		return syscallEroare(Enosys)
	}
}

func (sine *TSyscall) Init(manager *TIntreruperemanager) {
	initFișierdescriptor()

	intreruperehandler = mânerIntrerupere

	var address uintptr
	address = uintptr(Pointer(&intreruperehandler))

	sine.TIntreruperehandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var intreruperehandler func(uint32) uint32

func mânerIntrerupere(esp uint32) uint32 {
	var cpu = (*TcpuStare)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysIeșire:
		sysIeșire(cpu.Ebx)
		return uint32(uintptr(Pointer(OpreșteCurentăthread(cpu))))
	case SysrtIeșire:
		sysIeșire(cpu.Ebx)
		return uint32(uintptr(Pointer(OpreșteCurentăthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysCitire:
		cpu.Eax = uint32(sysCitire(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysScriere:
		cpu.Eax = uint32(sysScriere(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysDeschide:
		cpu.Eax = uint32(sysDeschide(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysDeschide(cpu.Ebx, ocreate|oScriereonly|oTrunchiază, cpu.Ecx))
		return esp
	case SysÎnchide:
		cpu.Eax = uint32(sysÎnchide(int32(cpu.Ebx)))
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
		cpu.Eax = Curentăpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Curentăpărintepid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysacces:
		cpu.Eax = uint32(sysacces(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(syssocketcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Tipărește(cpu.Ebx)
		return esp

	default:
		console_2.MTipăreștexy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Tipărește(esp)
		console_2.MTipărește(([]byte)(":"))
		console_2.MUnsignedinteger32Tipărește(cpu.Eax)
		console_2.MTipărește(([]byte)(":"))
		console_2.MUnsignedinteger32Tipărește(cpu.Ebx)
		console_2.MTipărește(([]byte)(":"))
		console_2.MUnsignedinteger32Tipărește(cpu.Ecx)
		console_2.MTipărește(([]byte)(":"))
		console_2.MUnsignedinteger32Tipărește(cpu.Edx)
		console_2.MTipărește(([]byte)("]"))
		cpu.Eax = syscallEroare(Enosys)
		return esp
	}

	return esp
}

func initFișierdescriptor() {
	for i := 0; i < maxDeschideFIȘIERE; i++ {
		deschideFișierTabel[i] = deschideFișierDescriere{}
	}
	for i := 0; i < len(procesTabel); i++ {
		procesTabel[i] = procesînregistrare{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	înainteephemeralport = 49152
	deschideFișierTabel[0] = deschideFișierDescriere{folosit: true, gen: descriptorfișierGenstdin, indicatori: oCitireonly}
	deschideFișierTabel[1] = deschideFișierDescriere{folosit: true, gen: descriptorfișierGenconsole, indicatori: oScriereonly}
	deschideFișierTabel[2] = deschideFișierDescriere{folosit: true, gen: descriptorfișierGenconsole, indicatori: oScriereonly}
}

func cautăProces(pid uint32) *procesînregistrare {
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].folosit && procesTabel[i].pid == pid {
			return &procesTabel[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesînregistrare) {
	for descriptorfișier := int32(0); descriptorfișier <= stderrDescriptorfișier; descriptorfișier++ {
		proces.fds[descriptorfișier] = descriptorfișierînregistrare{folosit: true, descriere: descriptorfișier}
		deschideFișierTabel[descriptorfișier].refs++
	}
}

func ensureCurentăProces() *procesînregistrare {
	pid := Curentăpid()
	if proces := cautăProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].folosit {
			procesTabel[i] = procesînregistrare{
				folosit:	true,
				pid:		pid,
				părinte:	Curentăpărintepid(),
				programbreak:	utilizatorheapbase,
			}
			initializeProcesfds(&procesTabel[i])
			return &procesTabel[i]
		}
	}
	return nil
}

func getDeschideFișierfor(proces *procesînregistrare, descriptorfișier int32) *deschideFișierDescriere {
	if proces == nil || descriptorfișier < 0 || descriptorfișier >= maxDescriptorfișier || !proces.fds[descriptorfișier].folosit {
		return nil
	}
	descriere := proces.fds[descriptorfișier].descriere
	if descriere < 0 || descriere >= maxDeschideFIȘIERE || !deschideFișierTabel[descriere].folosit {
		return nil
	}
	return &deschideFișierTabel[descriere]
}

func getDeschideFișier(descriptorfișier int32) *deschideFișierDescriere {
	return getDeschideFișierfor(ensureCurentăProces(), descriptorfișier)
}

func allocateDeschideFișier() int32 {
	for i := int32(3); i < maxDeschideFIȘIERE; i++ {
		if !deschideFișierTabel[i].folosit {
			deschideFișierTabel[i] = deschideFișierDescriere{folosit: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateDescriptorfișier(proces *procesînregistrare, descriere int32, minim int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minim < 0 || minim >= maxDescriptorfișier {
		return Einval
	}
	for descriptorfișier := minim; descriptorfișier < maxDescriptorfișier; descriptorfișier++ {
		if !proces.fds[descriptorfișier].folosit {
			proces.fds[descriptorfișier] = descriptorfișierînregistrare{folosit: true, descriere: descriere}
			return descriptorfișier
		}
	}
	return Emfile
}

func releaseDeschideFișier(descriere int32) {
	if descriere < 0 || descriere >= maxDeschideFIȘIERE {
		return
	}
	înregistrare := &deschideFișierTabel[descriere]
	if înregistrare.refs > 0 {
		înregistrare.refs--
	}

	if înregistrare.refs == 0 && descriere > stderrDescriptorfișier {
		if înregistrare.gen == descriptorfișierGensocket && înregistrare.aux < maxsockets {
			localsockets[înregistrare.aux] = localdatagramsocket{}
		}
		*înregistrare = deschideFișierDescriere{}
	}
}

func închideProcesDescriptorfișier(proces *procesînregistrare, descriptorfișier int32) int32 {
	if proces == nil || getDeschideFișierfor(proces, descriptorfișier) == nil {
		return Ebadf
	}
	descriere := proces.fds[descriptorfișier].descriere
	proces.fds[descriptorfișier] = descriptorfișierînregistrare{}
	releaseDeschideFișier(descriere)
	return 0
}

func sysScriere(descriptorfișier int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	înregistrare := getDeschideFișier(descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	if înregistrare.gen != descriptorfișierGenconsole {
		if înregistrare.gen == descriptorfișierGensocket {
			return socketTrimiteto(descriptorfișier, address, count, 0, 0)
		}
		if înregistrare.gen == descriptorfișierGenfat || înregistrare.gen == descriptorfișierGenRădăcinăDirector {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetOctețifromIndicator(uintptr(address), int(count), int(count))
	console_2.MTipărește(buffer)
	return int32(count)
}

func sysCitire(descriptorfișier int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	înregistrare := getDeschideFișier(descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	if înregistrare.gen == descriptorfișierGenstdin {
		return citirestdin(address, count)
	}
	if înregistrare.gen == descriptorfișierGenRădăcinăDirector {
		return Eisdir
	}
	if înregistrare.gen == descriptorfișierGensocket {
		return socketreceivefrom(descriptorfișier, address, count, 0, 0)
	}
	if înregistrare.gen != descriptorfișierGenfat {
		return Ebadf
	}
	if înregistrare.poziție >= înregistrare.mărime {
		return 0
	}
	remaining := înregistrare.mărime - înregistrare.poziție
	if count > remaining {
		count = remaining
	}
	buffer := GetOctețifromIndicator(uintptr(address), int(count), int(count))
	return citirevfsFișier(înregistrare, buffer, count)
}

func sysDeschide(cALEaddress uint32, indicatori uint32, mOD uint32) int32 {
	_ = mOD
	if cALEaddress == 0 {
		return Efault
	}
	accesMOD := indicatori & 3
	if accesMOD == oScriereonly || accesMOD == oCitireScriere || (indicatori&(ocreate|oTrunchiază|oappend)) != 0 {
		return Erofs
	}

	proces := ensureCurentăProces()
	if proces == nil {
		return Enfile
	}
	descriere := allocateDeschideFișier()
	if descriere < 0 {
		return descriere
	}
	înregistrare := &deschideFișierTabel[descriere]
	înregistrare.indicatori = indicatori
	if isRădăcinăCALE(cALEaddress) {
		înregistrare.gen = descriptorfișierGenRădăcinăDirector
		înregistrare.mărime = 0
	} else {
		numelen, nume := copiazăCALE(cALEaddress)
		if numelen == 0 {
			*înregistrare = deschideFișierDescriere{}
			return Enoent
		}
		mărime := fișierMărime(nume[:numelen])
		if mărime == 0 {
			*înregistrare = deschideFișierDescriere{}
			return Enoent
		}
		if (indicatori & oDirector) != 0 {
			*înregistrare = deschideFișierDescriere{}
			return Enotdir
		}
		înregistrare.gen = descriptorfișierGenfat
		înregistrare.mărime = mărime
		înregistrare.numelen = numelen
		înregistrare.nume = nume
	}

	descriptorfișier := allocateDescriptorfișier(proces, descriere, 3)
	if descriptorfișier < 0 {
		*înregistrare = deschideFișierDescriere{}
		return descriptorfișier
	}
	return descriptorfișier
}

func sysÎnchide(descriptorfișier int32) int32 {
	return închideProcesDescriptorfișier(ensureCurentăProces(), descriptorfișier)
}

func sysdup(descriptorfișier int32, minim int32) int32 {
	proces := ensureCurentăProces()
	înregistrare := getDeschideFișierfor(proces, descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	nouDescriptorfișier := allocateDescriptorfișier(proces, proces.fds[descriptorfișier].descriere, minim)
	if nouDescriptorfișier >= 0 {
		înregistrare.refs++
	}
	return nouDescriptorfișier
}

func sysdup2(oldDescriptorfișier int32, nouDescriptorfișier int32) int32 {
	proces := ensureCurentăProces()
	înregistrare := getDeschideFișierfor(proces, oldDescriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	if nouDescriptorfișier < 0 || nouDescriptorfișier >= maxDescriptorfișier {
		return Ebadf
	}
	if oldDescriptorfișier == nouDescriptorfișier {
		return nouDescriptorfișier
	}
	if proces.fds[nouDescriptorfișier].folosit {
		închideProcesDescriptorfișier(proces, nouDescriptorfișier)
	}
	proces.fds[nouDescriptorfișier] = descriptorfișierînregistrare{folosit: true, descriere: proces.fds[oldDescriptorfișier].descriere}
	înregistrare.refs++
	return nouDescriptorfișier
}

func sysfcntl(descriptorfișier int32, comandă uint32, argument uint32) int32 {
	proces := ensureCurentăProces()
	înregistrare := getDeschideFișierfor(proces, descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	switch comandă {
	case fdupDescriptorfișier:
		return sysdup(descriptorfișier, int32(argument))
	case fgetDescriptorfișier:
		return int32(proces.fds[descriptorfișier].descriptorfișierIndicatori)
	case fdefinitDescriptorfișier:
		proces.fds[descriptorfișier].descriptorfișierIndicatori = argument & descriptorfișiercloexec
		return 0
	case fgetfl:
		return int32(înregistrare.indicatori)
	case fdefinitfl:
		înregistrare.indicatori = (înregistrare.indicatori & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(descriptorfișier int32, offset int32, whence uint32) int32 {
	înregistrare := getDeschideFișier(descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	if înregistrare.gen != descriptorfișierGenfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekdefinit:
		base = 0
	case seekCurentă:
		base = int64(înregistrare.poziție)
	case seekSfârșit:
		base = int64(înregistrare.mărime)
	default:
		return Einval
	}
	poziție_2 := base + int64(offset)
	if poziție_2 < 0 || poziție_2 > 0x7FFFFFFF {
		return Einval
	}
	înregistrare.poziție = uint32(poziție_2)
	return int32(înregistrare.poziție)
}

func citirevfsFișier(înregistrare *deschideFișierDescriere, destinație_2 []byte, count uint32) int32 {
	memoriemanager := &mem.TMemoriemanager{}
	tmpIndicator := memoriemanager.Malloc(înregistrare.mărime)
	if tmpIndicator == nil {
		return Einval
	}
	tmp := GetOctețifromIndicator(uintptr(tmpIndicator), int(înregistrare.mărime), int(înregistrare.mărime))
	citireFișier(înregistrare.nume[:înregistrare.numelen], tmp)
	copy(destinație_2[:count], tmp[înregistrare.poziție:înregistrare.poziție+count])
	înregistrare.poziție += count
	memoriemanager.Liber(tmpIndicator)
	return int32(count)
}

func isRădăcinăCALE(cALEaddress uint32) bool {
	if cALEaddress == 0 {
		return false
	}
	cALE := GetOctețifromIndicator(uintptr(cALEaddress), 4, 4)
	if cALE[0] == '/' && cALE[1] == 0 {
		return true
	}
	if cALE[0] == '.' && cALE[1] == 0 {
		return true
	}
	if cALE[0] == '/' && cALE[1] == '.' && cALE[2] == 0 {
		return true
	}
	return false
}

func sysacces(cALEaddress uint32, mOD uint32) int32 {
	if cALEaddress == 0 {
		return Efault
	}
	if (mOD & ^uint32(7)) != 0 {
		return Einval
	}
	isRădăcină := isRădăcinăCALE(cALEaddress)
	exists := isRădăcină
	if !exists {
		numelen, nume := copiazăCALE(cALEaddress)
		exists = numelen != 0 && fișierMărime(nume[:numelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mOD & 2) != 0 {
		return Eacces
	}

	if (mOD&1) != 0 && !isRădăcină {
		return Eacces
	}
	return 0
}

func syschdir(cALEaddress uint32) int32 {
	if cALEaddress == 0 {
		return Efault
	}
	if !isRădăcinăCALE(cALEaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, mărime uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if mărime < 2 {
		return Erange
	}
	buffer_2 := GetOctețifromIndicator(uintptr(bufferaddress), int(mărime), int(mărime))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mOD uint32, mărime uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dispozitiv = 1
	stat.Ino = inode
	stat.MOD = mOD
	stat.Nlink = 1
	stat.Mărime_2 = int32(mărime)
	stat.Blksize = 512
	stat.Bloc = int32((mărime + 511) / 512)
	return 0
}

func sysstat(cALEaddress uint32, stataddress uint32) int32 {
	if cALEaddress == 0 {
		return Efault
	}
	if isRădăcinăCALE(cALEaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	numelen, nume := copiazăCALE(cALEaddress)
	if numelen == 0 {
		return Enoent
	}
	mărime := fișierMărime(nume[:numelen])
	if mărime == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < numelen; i++ {
		inode = inode*33 + uint32(nume[i])
	}
	return fillposixstat(stataddress, sifreg|0444, mărime, inode)
}

func sysfstat(descriptorfișier int32, stataddress uint32) int32 {
	înregistrare := getDeschideFișier(descriptorfișier)
	if înregistrare == nil {
		return Ebadf
	}
	switch înregistrare.gen {
	case descriptorfișierGenstdin, descriptorfișierGenconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(descriptorfișier+1))
	case descriptorfișierGenRădăcinăDirector:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case descriptorfișierGenfat:
		return fillposixstat(stataddress, sifreg|0444, înregistrare.mărime, uint32(descriptorfișier+2))
	case descriptorfișierGensocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(descriptorfișier+2))
	}
	return Ebadf
}

func sysfsync(descriptorfișier int32) int32 {
	if getDeschideFișier(descriptorfișier) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureCurentăProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = utilizatorheapbase
	}
	if address_2 == 0 {
		return proces.programbreak
	}
	if address_2 < utilizatorheapbase || address_2 > utilizatorheapLimită {
		return proces.programbreak
	}
	proces.programbreak = address_2
	return proces.programbreak
}

func copiazăutscâmp(destinație *[65]byte, valoare string) {
	limită := len(valoare)
	if limită > 64 {
		limită = 64
	}
	for i := 0; i < limită; i++ {
		destinație[i] = valoare[i]
	}
	destinație[limită] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nume := (*posixutsname)(Pointer(uintptr(address_2)))
	*nume = posixutsname{}
	copiazăutscâmp(&nume.Sysname, "EngOS")
	copiazăutscâmp(&nume.Nodename, "engos")
	copiazăutscâmp(&nume.Release, "0.1-posix")
	copiazăutscâmp(&nume.Versiune, "POSIX.1-2017 phase 1")
	copiazăutscâmp(&nume.Machine, "i386")
	return 0
}

func spațiudeschimbunsignedinteger16(valoare uint16) uint16 {
	return (valoare << 8) | (valoare >> 8)
}

func socketcallargument(argumente_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumente_2 + index*4)))
}

func socketforDescriptorfișier(descriptorfișier int32) (*localdatagramsocket, int32) {
	înregistrare := getDeschideFișier(descriptorfișier)
	if înregistrare == nil || înregistrare.gen != descriptorfișierGensocket || înregistrare.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[înregistrare.aux]
	if !socket.folosit {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domeniu uint32, socketTip uint32, protocol uint32) int32 {
	if domeniu != afinet {
		return Eafnosupport
	}
	if socketTip != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureCurentăProces()
	if proces == nil {
		return Enfile
	}
	socketindex := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].folosit {
			socketindex = i
			break
		}
	}
	if socketindex < 0 {
		return Enfile
	}
	descriere := allocateDeschideFișier()
	if descriere < 0 {
		return descriere
	}
	localsockets[socketindex] = localdatagramsocket{folosit: true}
	înregistrare := &deschideFișierTabel[descriere]
	înregistrare.gen = descriptorfișierGensocket
	înregistrare.indicatori = oCitireScriere
	înregistrare.aux = uint32(socketindex)
	descriptorfișier := allocateDescriptorfișier(proces, descriere, 3)
	if descriptorfișier < 0 {
		localsockets[socketindex] = localdatagramsocket{}
		*înregistrare = deschideFișierDescriere{}
		return descriptorfișier
	}
	return descriptorfișier
}

func socketaddress(address_2 uint32, durată uint32) (*socketaddressiVp4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if durată < 16 {
		return nil, Einval
	}
	result := (*socketaddressiVp4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portIntrareuse(port uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.folosit && socket.bound && socket.local.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := spațiudeschimbunsignedinteger16(înainteephemeralport)
		înainteephemeralport++
		if înainteephemeralport < 49152 {
			înainteephemeralport = 49152
		}
		if !portIntrareuse(port, socket) {
			socket.local = socketaddressiVp4{Family: afinet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(descriptorfișier int32, address_2 uint32, durată uint32) int32 {
	socket, erori := socketforDescriptorfișier(descriptorfișier)
	if erori != 0 {
		return erori
	}
	requested, erori := socketaddress(address_2, durată)
	if erori != 0 {
		return erori
	}
	if socket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(socket)
	}
	if portIntrareuse(requested.Port, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketConectează(descriptorfișier int32, address_2 uint32, durată uint32) int32 {
	socket, erori := socketforDescriptorfișier(descriptorfișier)
	if erori != 0 {
		return erori
	}
	ladistanță, erori := socketaddress(address_2, durată)
	if erori != 0 {
		return erori
	}
	if !socket.bound {
		if erori := bindephemeral(socket); erori != 0 {
			return erori
		}
	}
	socket.ladistanță = *ladistanță
	socket.connected = true
	return 0
}

func socketTrimiteto(descriptorfișier int32, bufferaddress_2 uint32, durată uint32, destinațieaddress uint32, destinațieDurată uint32) int32 {
	socket, erori := socketforDescriptorfișier(descriptorfișier)
	if erori != 0 {
		return erori
	}
	if durată > maxdatagramMărime {
		return Emsgsize
	}
	if durată != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destinație socketaddressiVp4
	if destinațieaddress != 0 {
		address_2, addressEroare := socketaddress(destinațieaddress, destinațieDurată)
		if addressEroare != 0 {
			return addressEroare
		}
		destinație = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destinație = socket.ladistanță
	}
	if !socket.bound {
		if bindEroare := bindephemeral(socket); bindEroare != 0 {
			return bindEroare
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.folosit && candidate.bound && candidate.local.Port == destinație.Port &&
			(candidate.local.Address == 0 || candidate.local.Address == destinație.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxsocketpachete {
		return Eagain
	}
	packet := &receiver.pachete[receiver.tail]
	*packet = socketpacket{folosit: true, mărime: durată, sursă: socket.local}
	if durată != 0 {
		sursă := GetOctețifromIndicator(uintptr(bufferaddress_2), int(durată), int(durată))
		copy(packet.data[:durată], sursă)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpachete
	receiver.count++
	return int32(durată)
}

func socketreceivefrom(descriptorfișier int32, bufferaddress_2 uint32, durată uint32, sursăaddress uint32, sursăDuratăaddress uint32) int32 {
	socket, erori := socketforDescriptorfișier(descriptorfișier)
	if erori != 0 {
		return erori
	}
	if durată != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.pachete[socket.head]
	copiazăDurată := packet.mărime
	if copiazăDurată > durată {
		copiazăDurată = durată
	}
	if copiazăDurată != 0 {
		destinație := GetOctețifromIndicator(uintptr(bufferaddress_2), int(copiazăDurată), int(copiazăDurată))
		copy(destinație, packet.data[:copiazăDurată])
	}
	if sursăaddress != 0 {
		if sursăDuratăaddress == 0 {
			return Efault
		}
		providedDurată := (*uint32)(Pointer(uintptr(sursăDuratăaddress)))
		if *providedDurată >= 16 {
			*(*socketaddressiVp4)(Pointer(uintptr(sursăaddress))) = packet.sursă
		}
		*providedDurată = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpachete
	socket.count--
	return int32(copiazăDurată)
}

func copiazăsocketNume(descriptorfișier int32, address_2 uint32, duratăaddress uint32, peer bool) int32 {
	socket, erori := socketforDescriptorfișier(descriptorfișier)
	if erori != 0 {
		return erori
	}
	if address_2 == 0 || duratăaddress == 0 {
		return Efault
	}
	durată := (*uint32)(Pointer(uintptr(duratăaddress)))
	if *durată < 16 {
		*durată = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressiVp4)(Pointer(uintptr(address_2))) = socket.ladistanță
	} else {
		if !socket.bound {
			if bindEroare := bindephemeral(socket); bindEroare != 0 {
				return bindEroare
			}
		}
		*(*socketaddressiVp4)(Pointer(uintptr(address_2))) = socket.local
	}
	*durată = 16
	return 0
}

func syssocketcall(call uint32, argumente_2 uint32) int32 {
	if argumente_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(argumente_2, 0), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 3:
		return socketConectează(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copiazăsocketNume(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), false)
	case 7:
		return copiazăsocketNume(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), true)
	case 9:
		return socketTrimiteto(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), 0, 0)
	case 11:
		return socketTrimiteto(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), socketcallargument(argumente_2, 4), socketcallargument(argumente_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(argumente_2, 0)), socketcallargument(argumente_2, 1), socketcallargument(argumente_2, 2), socketcallargument(argumente_2, 4), socketcallargument(argumente_2, 5))
	case 13:
		if _, erori := socketforDescriptorfișier(int32(socketcallargument(argumente_2, 0))); erori != 0 {
			return erori
		}
		return 0
	case 14:
		if _, erori := socketforDescriptorfișier(int32(socketcallargument(argumente_2, 0))); erori != 0 {
			return erori
		}
		return 0
	}
	return Eopnotsupp
}

func citirestdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetOctețifromIndicator(uintptr(address), int(count), int(count))
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
	înainte := (stdinScriere + 1) % uint32(len(stdinbuffer))
	if înainte == stdinCitire {
		return
	}
	stdinbuffer[stdinScriere] = c
	stdinScriere = înainte
}

func stdingetblocking() byte {
	for stdinCitire == stdinScriere {
		sc := pollTastaturăscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinCitire]
	stdinCitire = (stdinCitire + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastaturăscancode() byte {
	for (PortCitirebyte(0x64) & 0x01) == 0 {
	}
	sc := PortCitirebyte(0x60)
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

func copiazăExecuțievector(address_2 uint32, result *execuțievector) int32 {
	*result = execuțievector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxExecuțievectorînregistrare; index++ {
		șiraddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if șiraddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for durată := uint32(0); durată <= maxExecuțieȘirDurată; durată++ {
			valoare := *(*byte)(Pointer(uintptr(șiraddress + durată)))
			result.values[index][durată] = valoare
			if valoare == 0 {
				result.lengths[index] = durată
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

func pushExecuțieunsignedinteger32(stack *uint32, valoare uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = valoare
}

func setupExecuțiestack(cpu *TcpuStare, argumente_2 *execuțievector, environment *execuțievector) int32 {
	const stackOcteți uint32 = 4096
	if !MakeIntervalPrivatwritable(getcr3(), UtilizatorstackSus-stackOcteți, stackOcteți) {
		return Enomem
	}
	stack := UtilizatorstackSus
	var argumentpointers [maxExecuțievectorînregistrare]uint32
	var environmentpointers [maxExecuțievectorînregistrare]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		durată := environment.lengths[i] + 1
		stack -= durată
		destinație := GetOctețifromIndicator(uintptr(stack), int(durată), int(durată))
		copy(destinație, environment.values[i][:durată])
		environmentpointers[i] = stack
	}
	for i := int(argumente_2.count) - 1; i >= 0; i-- {
		durată := argumente_2.lengths[i] + 1
		stack -= durată
		destinație := GetOctețifromIndicator(uintptr(stack), int(durată), int(durată))
		copy(destinație, argumente_2.values[i][:durată])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushExecuțieunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushExecuțieunsignedinteger32(&stack, environmentpointers[i])
	}
	pushExecuțieunsignedinteger32(&stack, 0)
	for i := int(argumente_2.count) - 1; i >= 0; i-- {
		pushExecuțieunsignedinteger32(&stack, argumentpointers[i])
	}
	pushExecuțieunsignedinteger32(&stack, argumente_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func închidePornitExecuție(proces *procesînregistrare) {
	if proces == nil {
		return
	}
	for descriptorfișier := int32(0); descriptorfișier < maxDescriptorfișier; descriptorfișier++ {
		if proces.fds[descriptorfișier].folosit && (proces.fds[descriptorfișier].descriptorfișierIndicatori&descriptorfișiercloexec) != 0 {
			închideProcesDescriptorfișier(proces, descriptorfișier)
		}
	}
}

func sysexecve(cpu *TcpuStare, cALEaddress uint32) int32 {
	if cALEaddress == 0 {
		return Efault
	}
	var argumente_2 execuțievector
	var environment execuțievector
	if result := copiazăExecuțievector(cpu.Ecx, &argumente_2); result < 0 {
		return result
	}
	if result := copiazăExecuțievector(cpu.Edx, &environment); result < 0 {
		return result
	}
	numelen, nume := copiazăCALE(cALEaddress)
	if numelen == 0 {
		return Enoent
	}
	mărime := fișierMărime(nume[:numelen])
	if mărime == 0 {
		return Enoent
	}
	memoriemanager := &mem.TMemoriemanager{}
	fișierIndicator := memoriemanager.Malloc(mărime)
	if fișierIndicator == nil {
		return Einval
	}
	data := GetOctețifromIndicator(uintptr(fișierIndicator), int(mărime), int(mărime))
	citireFișier(nume[:numelen], data)
	if mărime < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memoriemanager.Liber(fișierIndicator)
		return Enoexec
	}
	loader := Elf{}
	înregistrare := loader.Getînregistrare(data)
	loader.Parse(data, getcr3())
	memoriemanager.Liber(fișierIndicator)
	if result := setupExecuțiestack(cpu, &argumente_2, &environment); result < 0 {
		return result
	}
	închidePornitExecuție(ensureCurentăProces())
	cpu.Eip = înregistrare
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStare) int32 {
	părintepid := Curentăpid()
	if ensureCurentăProces() == nil {
		return Enfile
	}
	pid := allocateProces(părintepid)
	if pid == 0 {
		return Einval
	}
	memoriemanager := &mem.TMemoriemanager{}
	threadIndicator := memoriemanager.Malloc(uint32(Sizeof(TThread{})))
	stackIndicator := memoriemanager.Malloc(ThreadstackMărime)
	copilPAGINĂDirector := CloneaddressSpațiucow(getcr3())
	if threadIndicator == nil || stackIndicator == nil || copilPAGINĂDirector == 0 {
		eliminăProces(pid)
		return Einval
	}
	copil := (*TThread)(threadIndicator)
	copil.Stack = uint32(uintptr(stackIndicator))
	copil.CpuStare = (*TcpuStare)(Pointer(uintptr(stackIndicator) + ThreadstackMărime - Sizeof(TcpuStare{})))
	*copil.CpuStare = *cpu
	copil.CpuStare.Eax = 0
	copil.Utilizatorstack_2 = cpu.Esp
	copil.UtilizatorstackMărime_2 = 0
	copil.Pid = pid
	copil.Părintepid = părintepid
	copil.PAGINĂDirectorînregistrare = copilPAGINĂDirector
	copil.ThreadStare = Pregătit
	copil.Fpuoffset = 0xffffffff
	copil.Iskernel = false
	Adaugărunnablethread(copil)
	return int32(pid)
}

func sysIeșire(stare uint32) {
	pid := Curentăpid()
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].folosit && procesTabel[i].pid == pid {
			închideToateProcesfds(&procesTabel[i])
			procesTabel[i].terminat = true
			procesTabel[i].stare = (stare & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, stareaddress uint32, opțiuni uint32) int32 {
	if (opțiuni & ^uint32(1)) != 0 {
		return Einval
	}
	părintepid := Curentăpid()
	foundcopil := false
	for i := 0; i < len(procesTabel); i++ {
		p := &procesTabel[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.folosit && matches && p.părinte == părintepid {
			foundcopil = true
			if p.terminat {
				if stareaddress != 0 {
					*(*uint32)(Pointer(uintptr(stareaddress))) = p.stare
				}
				copilpid := p.pid
				*p = procesînregistrare{}
				return int32(copilpid)
			}
		}
	}
	if !foundcopil {
		return Echild
	}

	if (opțiuni & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(părinte uint32) uint32 {
	părinteProces := cautăProces(părinte)
	pid := Allocatepid()
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].folosit {
			procesTabel[i] = procesînregistrare{
				folosit:	true,
				pid:		pid,
				părinte:	părinte,
				programbreak:	utilizatorheapbase,
			}
			if părinteProces != nil {
				procesTabel[i].programbreak = părinteProces.programbreak
				for descriptorfișier := 0; descriptorfișier < maxDescriptorfișier; descriptorfișier++ {
					if părinteProces.fds[descriptorfișier].folosit {
						procesTabel[i].fds[descriptorfișier] = părinteProces.fds[descriptorfișier]
						descriere := părinteProces.fds[descriptorfișier].descriere
						if descriere >= 0 && descriere < maxDeschideFIȘIERE {
							deschideFișierTabel[descriere].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabel[i])
			}
			return pid
		}
	}
	return 0
}

func închideToateProcesfds(proces *procesînregistrare) {
	if proces == nil {
		return
	}
	for descriptorfișier := int32(0); descriptorfișier < maxDescriptorfișier; descriptorfișier++ {
		if proces.fds[descriptorfișier].folosit {
			închideProcesDescriptorfișier(proces, descriptorfișier)
		}
	}
}

func eliminăProces(pid uint32) {
	proces := cautăProces(pid)
	if proces == nil {
		return
	}
	închideToateProcesfds(proces)
	*proces = procesînregistrare{}
}

func copiazăCALE(cALEaddress uint32) (uint32, [12]byte) {
	var nume [12]byte
	if cALEaddress == 0 {
		return 0, nume
	}
	raw := GetOctețifromIndicator(uintptr(cALEaddress), 64, 64)
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
		nume[n] = c
		n++
	}
	return n, nume
}

func fișierMărime(numefișier []byte) uint32 {
	var ata0s = TAvansateTehnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Citirepartition(&ata0s)

	bios := TBiosparameterBloc32{}
	mărime := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], numefișier)
	ata0s.Flush()
	return mărime
}

func citireFișier(numefișier []byte, data []byte) {
	var ata0s = TAvansateTehnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Citirepartition(&ata0s)

	bios := TBiosparameterBloc32{}
	bios.Citire(&ata0s, partition.Mbr.Primarypartition[0], numefișier, data)
	ata0s.Flush()
}

func getcr3() uint32
