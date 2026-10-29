/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package rafitracall

import . "unsafe"

import . "interrupt"
import . "konsoly"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "rakitraRafitra/msdospartition"
import . "rakitraRafitra/fat"
import . "rakitraRafitra/elf"
import mem "arikaMpandrindra"
import . "paging"
import . "irika"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualArika"

var konsoly_2 = TKonsoly{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	SysMamaky	uint32	= 3
	SysManoratra	uint32	= 4
	SysSokafy	uint32	= 5
	Syshidio	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaccess	uint32	= 33
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
	Sysrtexit	uint32	= 252

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
	stdinfd		int32	= 0
	stdoutfd	int32	= 1
	stderrfd	int32	= 2
	maxfd			= 32
	maxSokafyfiles		= 128
)

type fdentry struct {
	ampiasaina	bool
	fanoritsoritana	int32
	fdSaina		uint32
}

type sokafyRakitraFanoritsoritana struct {
	ampiasaina	bool
	refs		uint32
	kind		uint32
	saina		uint32
	position	uint32
	habe		uint32
	anarana		[12]byte
	anaranalen	uint32
	aux		uint32
}

const (
	fdkindTsymisy		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindKonsoly		uint32	= 3
	fdkindFakaLahatahiry	uint32	= 4
	fdkindsocket		uint32	= 5

	oMamakyonly		uint32	= 0
	oManoratraonly		uint32	= 1
	oMamakyManoratra	uint32	= 2
	ocreate			uint32	= 0x40
	otruncate		uint32	= 0x200
	oappend			uint32	= 0x400
	oLahatahiry		uint32	= 0x10000

	seekset		uint32	= 0
	seekcurrent	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fsetfd		uint32	= 2
	fgetfl		uint32	= 3
	fsetfl		uint32	= 4
	fdcloexec	uint32	= 1

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
	maxsocketpackets	= 8
	maxdatagramHabe		= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Irika	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	ampiasaina	bool
	habe		uint32
	loharano	socketaddressipv4
	data		[maxdatagramHabe]byte
}

type localdatagramsocket struct {
	ampiasaina	bool
	bound		bool
	connected	bool
	local		socketaddressipv4
	remote		socketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Periferika	uint32
	Ino		uint32
	Fomba		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Habe_2		int32
	Blksize		int32
	Block		int32
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
	Version		[65]byte
	Machine		[65]byte
}

const (
	maxexecvectorentry	= 16
	maxexecstringlength	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecstringlength + 1]byte
}

type processentry struct {
	ampiasaina	bool
	pid		uint32
	reny		uint32
	exited		bool
	fivoarana	uint32
	rindranasabreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallDiso(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var sokafyRakitraFafana [maxSokafyfiles]sokafyRakitraFanoritsoritana
var processFafana [32]processentry
var localsockets [maxsockets]localdatagramsocket
var manarakaephemeralIrika uint16 = 49152

const (
	mpampiasaheapbase	uint32	= 0x06000000
	mpampiasaheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinMamaky uint32
var stdinManoratra uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(fizahantakila uint32) {
	Syscall(Sysexit, fizahantakila)
}

func SysMamaky_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysMamaky, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysAtontaystr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(SysManoratra, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysAtontayunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysManoratra, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysSokafy_2(sORIDALANA uintptr, saina uint32, fomba uint32) int32 {
	return int32(Syscall(SysSokafy, uint32(sORIDALANA), saina, fomba))
}

func Syshidio_2(fd uint32) int32 {
	return int32(Syscall(Syshidio, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(params ...uint32) uint32 {

	l := len(params)
	switch l {
	case 1:
		return Interrupt(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Interrupt(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallDiso(Enosys)
	}
}

func (nytena *TSyscall) Init(mpandrindra *TInterruptMpandrindra) {
	initRakitradescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	nytena.TInterrupthandler.Init(0x80, uintptr(Pointer(mpandrindra)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Ajanonycurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Ajanonycurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysMamaky:
		cpu.Eax = uint32(sysMamaky(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysManoratra:
		cpu.Eax = uint32(sysManoratra(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSokafy:
		cpu.Eax = uint32(sysSokafy(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysSokafy(cpu.Ebx, ocreate|oManoratraonly|otruncate, cpu.Ecx))
		return esp
	case Syshidio:
		cpu.Eax = uint32(syshidio(int32(cpu.Ebx)))
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
		cpu.Eax = Currentpid()
		return esp
	case Sysgetppid:
		cpu.Eax = CurrentRenypid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysaccess:
		cpu.Eax = uint32(sysaccess(cpu.Ebx, cpu.Ecx))
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
		konsoly_2.MUnsignedinteger32Atontay(cpu.Ebx)
		return esp

	default:
		konsoly_2.MAtontayxy(([]byte)("sys["), 1, 23)
		konsoly_2.MUnsignedinteger32Atontay(esp)
		konsoly_2.MAtontay(([]byte)(":"))
		konsoly_2.MUnsignedinteger32Atontay(cpu.Eax)
		konsoly_2.MAtontay(([]byte)(":"))
		konsoly_2.MUnsignedinteger32Atontay(cpu.Ebx)
		konsoly_2.MAtontay(([]byte)(":"))
		konsoly_2.MUnsignedinteger32Atontay(cpu.Ecx)
		konsoly_2.MAtontay(([]byte)(":"))
		konsoly_2.MUnsignedinteger32Atontay(cpu.Edx)
		konsoly_2.MAtontay(([]byte)("]"))
		cpu.Eax = syscallDiso(Enosys)
		return esp
	}

	return esp
}

func initRakitradescriptor() {
	for i := 0; i < maxSokafyfiles; i++ {
		sokafyRakitraFafana[i] = sokafyRakitraFanoritsoritana{}
	}
	for i := 0; i < len(processFafana); i++ {
		processFafana[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	manarakaephemeralIrika = 49152
	sokafyRakitraFafana[0] = sokafyRakitraFanoritsoritana{ampiasaina: true, kind: fdkindstdin, saina: oMamakyonly}
	sokafyRakitraFafana[1] = sokafyRakitraFanoritsoritana{ampiasaina: true, kind: fdkindKonsoly, saina: oManoratraonly}
	sokafyRakitraFafana[2] = sokafyRakitraFanoritsoritana{ampiasaina: true, kind: fdkindKonsoly, saina: oManoratraonly}
}

func tadiavoprocess(pid uint32) *processentry {
	for i := 0; i < len(processFafana); i++ {
		if processFafana[i].ampiasaina && processFafana[i].pid == pid {
			return &processFafana[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{ampiasaina: true, fanoritsoritana: fd}
		sokafyRakitraFafana[fd].refs++
	}
}

func ensurecurrentprocess() *processentry {
	pid := Currentpid()
	if process := tadiavoprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processFafana); i++ {
		if !processFafana[i].ampiasaina {
			processFafana[i] = processentry{
				ampiasaina:		true,
				pid:			pid,
				reny:			CurrentRenypid(),
				rindranasabreak:	mpampiasaheapbase,
			}
			initializeprocessfds(&processFafana[i])
			return &processFafana[i]
		}
	}
	return nil
}

func getSokafyRakitrafor(process *processentry, fd int32) *sokafyRakitraFanoritsoritana {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].ampiasaina {
		return nil
	}
	fanoritsoritana := process.fds[fd].fanoritsoritana
	if fanoritsoritana < 0 || fanoritsoritana >= maxSokafyfiles || !sokafyRakitraFafana[fanoritsoritana].ampiasaina {
		return nil
	}
	return &sokafyRakitraFafana[fanoritsoritana]
}

func getSokafyRakitra(fd int32) *sokafyRakitraFanoritsoritana {
	return getSokafyRakitrafor(ensurecurrentprocess(), fd)
}

func allocateSokafyRakitra() int32 {
	for i := int32(3); i < maxSokafyfiles; i++ {
		if !sokafyRakitraFafana[i].ampiasaina {
			sokafyRakitraFafana[i] = sokafyRakitraFanoritsoritana{ampiasaina: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, fanoritsoritana int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].ampiasaina {
			process.fds[fd] = fdentry{ampiasaina: true, fanoritsoritana: fanoritsoritana}
			return fd
		}
	}
	return Emfile
}

func releaseSokafyRakitra(fanoritsoritana int32) {
	if fanoritsoritana < 0 || fanoritsoritana >= maxSokafyfiles {
		return
	}
	entry := &sokafyRakitraFafana[fanoritsoritana]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && fanoritsoritana > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = sokafyRakitraFanoritsoritana{}
	}
}

func hidioprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getSokafyRakitrafor(process, fd) == nil {
		return Ebadf
	}
	fanoritsoritana := process.fds[fd].fanoritsoritana
	process.fds[fd] = fdentry{}
	releaseSokafyRakitra(fanoritsoritana)
	return 0
}

func sysManoratra(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getSokafyRakitra(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindKonsoly {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindFakaLahatahiry {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetOctetfrompointer(uintptr(address), int(count), int(count))
	konsoly_2.MAtontay(buffer)
	return int32(count)
}

func sysMamaky(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getSokafyRakitra(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return mamakystdin(address, count)
	}
	if entry.kind == fdkindFakaLahatahiry {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.habe {
		return 0
	}
	remaining := entry.habe - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := GetOctetfrompointer(uintptr(address), int(count), int(count))
	return mamakyvfsRakitra(entry, buffer, count)
}

func sysSokafy(sORIDALANAaddress uint32, saina uint32, fomba uint32) int32 {
	_ = fomba
	if sORIDALANAaddress == 0 {
		return Efault
	}
	accessFomba := saina & 3
	if accessFomba == oManoratraonly || accessFomba == oMamakyManoratra || (saina&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	fanoritsoritana := allocateSokafyRakitra()
	if fanoritsoritana < 0 {
		return fanoritsoritana
	}
	entry := &sokafyRakitraFafana[fanoritsoritana]
	entry.saina = saina
	if isFakaSORIDALANA(sORIDALANAaddress) {
		entry.kind = fdkindFakaLahatahiry
		entry.habe = 0
	} else {
		anaranalen, anarana := adikaoSORIDALANA(sORIDALANAaddress)
		if anaranalen == 0 {
			*entry = sokafyRakitraFanoritsoritana{}
			return Enoent
		}
		habe := rakitraHabe(anarana[:anaranalen])
		if habe == 0 {
			*entry = sokafyRakitraFanoritsoritana{}
			return Enoent
		}
		if (saina & oLahatahiry) != 0 {
			*entry = sokafyRakitraFanoritsoritana{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.habe = habe
		entry.anaranalen = anaranalen
		entry.anarana = anarana
	}

	fd := allocatefd(process, fanoritsoritana, 3)
	if fd < 0 {
		*entry = sokafyRakitraFanoritsoritana{}
		return fd
	}
	return fd
}

func syshidio(fd int32) int32 {
	return hidioprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getSokafyRakitrafor(process, fd)
	if entry == nil {
		return Ebadf
	}
	vaovaofd := allocatefd(process, process.fds[fd].fanoritsoritana, minimum)
	if vaovaofd >= 0 {
		entry.refs++
	}
	return vaovaofd
}

func sysdup2(oldfd int32, vaovaofd int32) int32 {
	process := ensurecurrentprocess()
	entry := getSokafyRakitrafor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if vaovaofd < 0 || vaovaofd >= maxfd {
		return Ebadf
	}
	if oldfd == vaovaofd {
		return vaovaofd
	}
	if process.fds[vaovaofd].ampiasaina {
		hidioprocessfd(process, vaovaofd)
	}
	process.fds[vaovaofd] = fdentry{ampiasaina: true, fanoritsoritana: process.fds[oldfd].fanoritsoritana}
	entry.refs++
	return vaovaofd
}

func sysfcntl(fd int32, baiko uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getSokafyRakitrafor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch baiko {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdSaina)
	case fsetfd:
		process.fds[fd].fdSaina = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.saina)
	case fsetfl:
		entry.saina = (entry.saina & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getSokafyRakitra(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekset:
		base = 0
	case seekcurrent:
		base = int64(entry.position)
	case seekend:
		base = int64(entry.habe)
	default:
		return Einval
	}
	position_2 := base + int64(offset)
	if position_2 < 0 || position_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.position = uint32(position_2)
	return int32(entry.position)
}

func mamakyvfsRakitra(entry *sokafyRakitraFanoritsoritana, destination_2 []byte, count uint32) int32 {
	arikaMpandrindra := &mem.TArikaMpandrindra{}
	tmppointer := arikaMpandrindra.Malloc(entry.habe)
	if tmppointer == nil {
		return Einval
	}
	tmp := GetOctetfrompointer(uintptr(tmppointer), int(entry.habe), int(entry.habe))
	mamakyRakitra(entry.anarana[:entry.anaranalen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	arikaMpandrindra.Malalaka(tmppointer)
	return int32(count)
}

func isFakaSORIDALANA(sORIDALANAaddress uint32) bool {
	if sORIDALANAaddress == 0 {
		return false
	}
	sORIDALANA := GetOctetfrompointer(uintptr(sORIDALANAaddress), 4, 4)
	if sORIDALANA[0] == '/' && sORIDALANA[1] == 0 {
		return true
	}
	if sORIDALANA[0] == '.' && sORIDALANA[1] == 0 {
		return true
	}
	if sORIDALANA[0] == '/' && sORIDALANA[1] == '.' && sORIDALANA[2] == 0 {
		return true
	}
	return false
}

func sysaccess(sORIDALANAaddress uint32, fomba uint32) int32 {
	if sORIDALANAaddress == 0 {
		return Efault
	}
	if (fomba & ^uint32(7)) != 0 {
		return Einval
	}
	isFaka := isFakaSORIDALANA(sORIDALANAaddress)
	exists := isFaka
	if !exists {
		anaranalen, anarana := adikaoSORIDALANA(sORIDALANAaddress)
		exists = anaranalen != 0 && rakitraHabe(anarana[:anaranalen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (fomba & 2) != 0 {
		return Eacces
	}

	if (fomba&1) != 0 && !isFaka {
		return Eacces
	}
	return 0
}

func syschdir(sORIDALANAaddress uint32) int32 {
	if sORIDALANAaddress == 0 {
		return Efault
	}
	if !isFakaSORIDALANA(sORIDALANAaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, habe uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if habe < 2 {
		return Erange
	}
	buffer_2 := GetOctetfrompointer(uintptr(bufferaddress), int(habe), int(habe))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, fomba uint32, habe uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Periferika = 1
	stat.Ino = inode
	stat.Fomba = fomba
	stat.Nlink = 1
	stat.Habe_2 = int32(habe)
	stat.Blksize = 512
	stat.Block = int32((habe + 511) / 512)
	return 0
}

func sysstat(sORIDALANAaddress uint32, stataddress uint32) int32 {
	if sORIDALANAaddress == 0 {
		return Efault
	}
	if isFakaSORIDALANA(sORIDALANAaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	anaranalen, anarana := adikaoSORIDALANA(sORIDALANAaddress)
	if anaranalen == 0 {
		return Enoent
	}
	habe := rakitraHabe(anarana[:anaranalen])
	if habe == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < anaranalen; i++ {
		inode = inode*33 + uint32(anarana[i])
	}
	return fillposixstat(stataddress, sifreg|0444, habe, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getSokafyRakitra(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindKonsoly:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindFakaLahatahiry:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.habe, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getSokafyRakitra(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensurecurrentprocess()
	if process == nil {
		return 0
	}
	if process.rindranasabreak == 0 {
		process.rindranasabreak = mpampiasaheapbase
	}
	if address_2 == 0 {
		return process.rindranasabreak
	}
	if address_2 < mpampiasaheapbase || address_2 > mpampiasaheaplimit {
		return process.rindranasabreak
	}
	process.rindranasabreak = address_2
	return process.rindranasabreak
}

func adikaoutsfield(destination *[65]byte, sanda string) {
	limit := len(sanda)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = sanda[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	anarana := (*posixutsname)(Pointer(uintptr(address_2)))
	*anarana = posixutsname{}
	adikaoutsfield(&anarana.Sysname, "EngOS")
	adikaoutsfield(&anarana.Nodename, "engos")
	adikaoutsfield(&anarana.Release, "0.1-posix")
	adikaoutsfield(&anarana.Version, "POSIX.1-2017 phase 1")
	adikaoutsfield(&anarana.Machine, "i386")
	return 0
}

func swapunsignedinteger16(sanda uint16) uint16 {
	return (sanda << 8) | (sanda >> 8)
}

func socketcallargument(arguments_2 uint32, fizahantakila uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + fizahantakila*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getSokafyRakitra(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.ampiasaina {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketKarazana uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketKarazana != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	socketFizahantakila := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].ampiasaina {
			socketFizahantakila = i
			break
		}
	}
	if socketFizahantakila < 0 {
		return Enfile
	}
	fanoritsoritana := allocateSokafyRakitra()
	if fanoritsoritana < 0 {
		return fanoritsoritana
	}
	localsockets[socketFizahantakila] = localdatagramsocket{ampiasaina: true}
	entry := &sokafyRakitraFafana[fanoritsoritana]
	entry.kind = fdkindsocket
	entry.saina = oMamakyManoratra
	entry.aux = uint32(socketFizahantakila)
	fd := allocatefd(process, fanoritsoritana, 3)
	if fd < 0 {
		localsockets[socketFizahantakila] = localdatagramsocket{}
		*entry = sokafyRakitraFanoritsoritana{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, length uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if length < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func irikaAnatyuse(irika uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.ampiasaina && socket.bound && socket.local.Irika == irika {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		irika := swapunsignedinteger16(manarakaephemeralIrika)
		manarakaephemeralIrika++
		if manarakaephemeralIrika < 49152 {
			manarakaephemeralIrika = 49152
		}
		if !irikaAnatyuse(irika, socket) {
			socket.local = socketaddressipv4{Family: afinet, Irika: irika, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, length uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, length)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Irika == 0 {
		return bindephemeral(socket)
	}
	if irikaAnatyuse(requested.Irika, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketAtomboy(fd int32, address_2 uint32, length uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, length)
	if err != 0 {
		return err
	}
	if !socket.bound {
		if err := bindephemeral(socket); err != 0 {
			return err
		}
	}
	socket.remote = *remote
	socket.connected = true
	return 0
}

func socketsendto(fd int32, bufferaddress_2 uint32, length uint32, destinationaddress uint32, destinationlength uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if length > maxdatagramHabe {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressDiso := socketaddress(destinationaddress, destinationlength)
		if addressDiso != 0 {
			return addressDiso
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindDiso := bindephemeral(socket); bindDiso != 0 {
			return bindDiso
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.ampiasaina && candidate.bound && candidate.local.Irika == destination.Irika &&
			(candidate.local.Address == 0 || candidate.local.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxsocketpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = socketpacket{ampiasaina: true, habe: length, loharano: socket.local}
	if length != 0 {
		loharano := GetOctetfrompointer(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], loharano)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, loharanoaddress uint32, loharanolengthaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	adikaolength := packet.habe
	if adikaolength > length {
		adikaolength = length
	}
	if adikaolength != 0 {
		destination := GetOctetfrompointer(uintptr(bufferaddress_2), int(adikaolength), int(adikaolength))
		copy(destination, packet.data[:adikaolength])
	}
	if loharanoaddress != 0 {
		if loharanolengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(loharanolengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(loharanoaddress))) = packet.loharano
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(adikaolength)
}

func adikaosocketAnarana(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || lengthaddress == 0 {
		return Efault
	}
	length := (*uint32)(Pointer(uintptr(lengthaddress)))
	if *length < 16 {
		*length = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindDiso := bindephemeral(socket); bindDiso != 0 {
				return bindDiso
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*length = 16
	return 0
}

func syssocketcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(arguments_2, 0), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 3:
		return socketAtomboy(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return adikaosocketAnarana(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return adikaosocketAnarana(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
	case 9:
		return socketsendto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return socketsendto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 13:
		if _, err := socketforfd(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketforfd(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func mamakystdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetOctetfrompointer(uintptr(address), int(count), int(count))
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
	manaraka := (stdinManoratra + 1) % uint32(len(stdinbuffer))
	if manaraka == stdinMamaky {
		return
	}
	stdinbuffer[stdinManoratra] = c
	stdinManoratra = manaraka
}

func stdingetblocking() byte {
	for stdinMamaky == stdinManoratra {
		sc := pollFafantenyscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinMamaky]
	stdinMamaky = (stdinMamaky + 1) % uint32(len(stdinbuffer))
	return c
}

func pollFafantenyscancode() byte {
	for (IrikaMamakybyte(0x64) & 0x01) == 0 {
	}
	sc := IrikaMamakybyte(0x60)
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

func adikaoexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for fizahantakila := uint32(0); fizahantakila < maxexecvectorentry; fizahantakila++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + fizahantakila*4)))
		if stringaddress == 0 {
			result.count = fizahantakila
			return 0
		}
		terminated := false
		for length := uint32(0); length <= maxexecstringlength; length++ {
			sanda := *(*byte)(Pointer(uintptr(stringaddress + length)))
			result.values[fizahantakila][length] = sanda
			if sanda == 0 {
				result.lengths[fizahantakila] = length
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

func pushexecunsignedinteger32(stack *uint32, sanda uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = sanda
}

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackOctet uint32 = 4096
	if !MakeElanelanaprivatewritable(getcr3(), Mpampiasastackambony-stackOctet, stackOctet) {
		return Enomem
	}
	stack := Mpampiasastackambony
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := GetOctetfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := GetOctetfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, arguments_2.values[i][:length])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushexecunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, environmentpointers[i])
	}
	pushexecunsignedinteger32(&stack, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, argumentpointers[i])
	}
	pushexecunsignedinteger32(&stack, arguments_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func hidioonexec(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].ampiasaina && (process.fds[fd].fdSaina&fdcloexec) != 0 {
			hidioprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, sORIDALANAaddress uint32) int32 {
	if sORIDALANAaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := adikaoexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := adikaoexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	anaranalen, anarana := adikaoSORIDALANA(sORIDALANAaddress)
	if anaranalen == 0 {
		return Enoent
	}
	habe := rakitraHabe(anarana[:anaranalen])
	if habe == 0 {
		return Enoent
	}
	arikaMpandrindra := &mem.TArikaMpandrindra{}
	rakitrapointer := arikaMpandrindra.Malloc(habe)
	if rakitrapointer == nil {
		return Einval
	}
	data := GetOctetfrompointer(uintptr(rakitrapointer), int(habe), int(habe))
	mamakyRakitra(anarana[:anaranalen], data)
	if habe < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		arikaMpandrindra.Malalaka(rakitrapointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	arikaMpandrindra.Malalaka(rakitrapointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	hidioonexec(ensurecurrentprocess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
	renypid := Currentpid()
	if ensurecurrentprocess() == nil {
		return Enfile
	}
	pid := allocateprocess(renypid)
	if pid == 0 {
		return Einval
	}
	arikaMpandrindra := &mem.TArikaMpandrindra{}
	threadpointer := arikaMpandrindra.Malloc(uint32(Sizeof(TThread{})))
	stackpointer := arikaMpandrindra.Malloc(ThreadstackHabe)
	zanakaPEJYLahatahiry := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || zanakaPEJYLahatahiry == 0 {
		discardprocess(pid)
		return Einval
	}
	zanaka := (*TThread)(threadpointer)
	zanaka.Stack = uint32(uintptr(stackpointer))
	zanaka.Cpustate = (*Tcpustate)(Pointer(uintptr(stackpointer) + ThreadstackHabe - Sizeof(Tcpustate{})))
	*zanaka.Cpustate = *cpu
	zanaka.Cpustate.Eax = 0
	zanaka.Mpampiasastack_2 = cpu.Esp
	zanaka.MpampiasastackHabe_2 = 0
	zanaka.Pid = pid
	zanaka.Renypid = renypid
	zanaka.PEJYLahatahiryentry = zanakaPEJYLahatahiry
	zanaka.Threadstate = Vonona
	zanaka.Fpuoffset = 0xffffffff
	zanaka.Iskernel = false
	Ampidirorunnablethread(zanaka)
	return int32(pid)
}

func sysexit(fivoarana uint32) {
	pid := Currentpid()
	for i := 0; i < len(processFafana); i++ {
		if processFafana[i].ampiasaina && processFafana[i].pid == pid {
			hidioallprocessfds(&processFafana[i])
			processFafana[i].exited = true
			processFafana[i].fivoarana = (fivoarana & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, fivoaranaaddress uint32, safidy uint32) int32 {
	if (safidy & ^uint32(1)) != 0 {
		return Einval
	}
	renypid := Currentpid()
	foundZanaka := false
	for i := 0; i < len(processFafana); i++ {
		p := &processFafana[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.ampiasaina && matches && p.reny == renypid {
			foundZanaka = true
			if p.exited {
				if fivoaranaaddress != 0 {
					*(*uint32)(Pointer(uintptr(fivoaranaaddress))) = p.fivoarana
				}
				zanakapid := p.pid
				*p = processentry{}
				return int32(zanakapid)
			}
		}
	}
	if !foundZanaka {
		return Echild
	}

	if (safidy & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(reny uint32) uint32 {
	renyprocess := tadiavoprocess(reny)
	pid := Allocatepid()
	for i := 0; i < len(processFafana); i++ {
		if !processFafana[i].ampiasaina {
			processFafana[i] = processentry{
				ampiasaina:		true,
				pid:			pid,
				reny:			reny,
				rindranasabreak:	mpampiasaheapbase,
			}
			if renyprocess != nil {
				processFafana[i].rindranasabreak = renyprocess.rindranasabreak
				for fd := 0; fd < maxfd; fd++ {
					if renyprocess.fds[fd].ampiasaina {
						processFafana[i].fds[fd] = renyprocess.fds[fd]
						fanoritsoritana := renyprocess.fds[fd].fanoritsoritana
						if fanoritsoritana >= 0 && fanoritsoritana < maxSokafyfiles {
							sokafyRakitraFafana[fanoritsoritana].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processFafana[i])
			}
			return pid
		}
	}
	return 0
}

func hidioallprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].ampiasaina {
			hidioprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := tadiavoprocess(pid)
	if process == nil {
		return
	}
	hidioallprocessfds(process)
	*process = processentry{}
}

func adikaoSORIDALANA(sORIDALANAaddress uint32) (uint32, [12]byte) {
	var anarana [12]byte
	if sORIDALANAaddress == 0 {
		return 0, anarana
	}
	raw := GetOctetfrompointer(uintptr(sORIDALANAaddress), 64, 64)
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
		anarana[n] = c
		n++
	}
	return n, anarana
}

func rakitraHabe(anarandrakitra []byte) uint32 {
	var ata0s = TAvolentatechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionFafana{}
	partition.Mamakypartition(&ata0s)

	bios := TBiosparameterblock32{}
	habe := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra)
	ata0s.Flush()
	return habe
}

func mamakyRakitra(anarandrakitra []byte, data []byte) {
	var ata0s = TAvolentatechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionFafana{}
	partition.Mamakypartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Mamaky(&ata0s, partition.Mbr.Primarypartition[0], anarandrakitra, data)
	ata0s.Flush()
}

func getcr3() uint32
