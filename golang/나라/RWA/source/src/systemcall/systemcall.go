package systemcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "idosiyesystem/msdospartition"
import . "idosiyesystem/fat"
import . "idosiyesystem/elf"
import mem "ububikomanager"
import . "paging"
import . "umuyoboro"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualUbubiko"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysGusohoka	uint32	= 1
	Sysfork		uint32	= 2
	Sysgusoma	uint32	= 3
	Syskwandika	uint32	= 4
	SysGufungura	uint32	= 5
	SysGufunga	uint32	= 6
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
	SysrtGusohoka	uint32	= 252

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
	stdinfd			int32	= 0
	stdoutfd		int32	= 1
	stderrfd		int32	= 2
	maxfd				= 32
	maxGufungurafiles		= 128
)

type fdentry struct {
	used		bool
	umwirondoro	int32
	fdAmabendera	uint32
}

type gufunguraIdosiyeUmwirondoro struct {
	used		bool
	refs		uint32
	kind		uint32
	amabendera	uint32
	position	uint32
	ingano		uint32
	izina		[12]byte
	izinalen	uint32
	aux		uint32
}

const (
	fdkindNtanakimwe	uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindImiziUbubiko	uint32	= 4
	fdkindsocket		uint32	= 5

	ogusomaonly	uint32	= 0
	okwandikaonly	uint32	= 1
	ogusomakwandika	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oUbubiko	uint32	= 0x10000

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
	maxdatagramIngano	= 512
)

type socketaddressiAgacirokikigihe4 struct {
	Family		uint16
	Umuyoboro	uint16
	Address		uint32
	Zero		[8]byte
}

type socketpacket struct {
	used		bool
	ingano		uint32
	inkomoko	socketaddressiAgacirokikigihe4
	data		[maxdatagramIngano]byte
}

type localdatagramsocket struct {
	used		bool
	bound		bool
	connected	bool
	local		socketaddressiAgacirokikigihe4
	remote		socketaddressiAgacirokikigihe4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Ububiko		uint32
	Ino		uint32
	Ubwoko		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Ingano_2	int32
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
	used		bool
	pid		uint32
	parent		uint32
	exited		bool
	imimerere	uint32
	porogaramubreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallIkosa(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var gufunguraIdosiyeImbonerahamwe [maxGufungurafiles]gufunguraIdosiyeUmwirondoro
var processImbonerahamwe [32]processentry
var localsockets [maxsockets]localdatagramsocket
var ikurikiraephemeralUmuyoboro uint16 = 49152

const (
	ukoreshaheapbase	uint32	= 0x06000000
	ukoreshaheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdingusoma uint32
var stdinkwandika uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysGusohoka_2(umubarendanga uint32) {
	Syscall(SysGusohoka, umubarendanga)
}

func Sysgusoma_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysgusoma, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysGucapastr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(Syskwandika, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysGucapaunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Syskwandika, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysGufungura_2(inzira uintptr, amabendera uint32, ubwoko uint32) int32 {
	return int32(Syscall(SysGufungura, uint32(inzira), amabendera, ubwoko))
}

func SysGufunga_2(fd uint32) int32 {
	return int32(Syscall(SysGufunga, fd))
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
		return syscallIkosa(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initIdosiyedescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysGusohoka:
		sysGusohoka(cpu.Ebx)
		return uint32(uintptr(Pointer(Guhagararacurrentthread(cpu))))
	case SysrtGusohoka:
		sysGusohoka(cpu.Ebx)
		return uint32(uintptr(Pointer(Guhagararacurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysgusoma:
		cpu.Eax = uint32(sysgusoma(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Syskwandika:
		cpu.Eax = uint32(syskwandika(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysGufungura:
		cpu.Eax = uint32(sysGufungura(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysGufungura(cpu.Ebx, ocreate|okwandikaonly|otruncate, cpu.Ecx))
		return esp
	case SysGufunga:
		cpu.Eax = uint32(sysGufunga(int32(cpu.Ebx)))
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
		cpu.Eax = Currentparentpid()
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
		console_2.MUnsignedinteger32Gucapa(cpu.Ebx)
		return esp

	default:
		console_2.MGucapaxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Gucapa(esp)
		console_2.MGucapa(([]byte)(":"))
		console_2.MUnsignedinteger32Gucapa(cpu.Eax)
		console_2.MGucapa(([]byte)(":"))
		console_2.MUnsignedinteger32Gucapa(cpu.Ebx)
		console_2.MGucapa(([]byte)(":"))
		console_2.MUnsignedinteger32Gucapa(cpu.Ecx)
		console_2.MGucapa(([]byte)(":"))
		console_2.MUnsignedinteger32Gucapa(cpu.Edx)
		console_2.MGucapa(([]byte)("]"))
		cpu.Eax = syscallIkosa(Enosys)
		return esp
	}

	return esp
}

func initIdosiyedescriptor() {
	for i := 0; i < maxGufungurafiles; i++ {
		gufunguraIdosiyeImbonerahamwe[i] = gufunguraIdosiyeUmwirondoro{}
	}
	for i := 0; i < len(processImbonerahamwe); i++ {
		processImbonerahamwe[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	ikurikiraephemeralUmuyoboro = 49152
	gufunguraIdosiyeImbonerahamwe[0] = gufunguraIdosiyeUmwirondoro{used: true, kind: fdkindstdin, amabendera: ogusomaonly}
	gufunguraIdosiyeImbonerahamwe[1] = gufunguraIdosiyeUmwirondoro{used: true, kind: fdkindconsole, amabendera: okwandikaonly}
	gufunguraIdosiyeImbonerahamwe[2] = gufunguraIdosiyeUmwirondoro{used: true, kind: fdkindconsole, amabendera: okwandikaonly}
}

func gushakaprocess(pid uint32) *processentry {
	for i := 0; i < len(processImbonerahamwe); i++ {
		if processImbonerahamwe[i].used && processImbonerahamwe[i].pid == pid {
			return &processImbonerahamwe[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{used: true, umwirondoro: fd}
		gufunguraIdosiyeImbonerahamwe[fd].refs++
	}
}

func ensurecurrentprocess() *processentry {
	pid := Currentpid()
	if process := gushakaprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processImbonerahamwe); i++ {
		if !processImbonerahamwe[i].used {
			processImbonerahamwe[i] = processentry{
				used:			true,
				pid:			pid,
				parent:			Currentparentpid(),
				porogaramubreak:	ukoreshaheapbase,
			}
			initializeprocessfds(&processImbonerahamwe[i])
			return &processImbonerahamwe[i]
		}
	}
	return nil
}

func getGufunguraIdosiyefor(process *processentry, fd int32) *gufunguraIdosiyeUmwirondoro {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].used {
		return nil
	}
	umwirondoro := process.fds[fd].umwirondoro
	if umwirondoro < 0 || umwirondoro >= maxGufungurafiles || !gufunguraIdosiyeImbonerahamwe[umwirondoro].used {
		return nil
	}
	return &gufunguraIdosiyeImbonerahamwe[umwirondoro]
}

func getGufunguraIdosiye(fd int32) *gufunguraIdosiyeUmwirondoro {
	return getGufunguraIdosiyefor(ensurecurrentprocess(), fd)
}

func allocateGufunguraIdosiye() int32 {
	for i := int32(3); i < maxGufungurafiles; i++ {
		if !gufunguraIdosiyeImbonerahamwe[i].used {
			gufunguraIdosiyeImbonerahamwe[i] = gufunguraIdosiyeUmwirondoro{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, umwirondoro int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].used {
			process.fds[fd] = fdentry{used: true, umwirondoro: umwirondoro}
			return fd
		}
	}
	return Emfile
}

func releaseGufunguraIdosiye(umwirondoro int32) {
	if umwirondoro < 0 || umwirondoro >= maxGufungurafiles {
		return
	}
	entry := &gufunguraIdosiyeImbonerahamwe[umwirondoro]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && umwirondoro > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = gufunguraIdosiyeUmwirondoro{}
	}
}

func gufungaprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getGufunguraIdosiyefor(process, fd) == nil {
		return Ebadf
	}
	umwirondoro := process.fds[fd].umwirondoro
	process.fds[fd] = fdentry{}
	releaseGufunguraIdosiye(umwirondoro)
	return 0
}

func syskwandika(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getGufunguraIdosiye(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindImiziUbubiko {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBayitefrompointer(uintptr(address), int(count), int(count))
	console_2.MGucapa(buffer)
	return int32(count)
}

func sysgusoma(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getGufunguraIdosiye(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return gusomastdin(address, count)
	}
	if entry.kind == fdkindImiziUbubiko {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.ingano {
		return 0
	}
	remaining := entry.ingano - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := GetBayitefrompointer(uintptr(address), int(count), int(count))
	return gusomavfsIdosiye(entry, buffer, count)
}

func sysGufungura(inziraaddress uint32, amabendera uint32, ubwoko uint32) int32 {
	_ = ubwoko
	if inziraaddress == 0 {
		return Efault
	}
	accessUbwoko := amabendera & 3
	if accessUbwoko == okwandikaonly || accessUbwoko == ogusomakwandika || (amabendera&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	umwirondoro := allocateGufunguraIdosiye()
	if umwirondoro < 0 {
		return umwirondoro
	}
	entry := &gufunguraIdosiyeImbonerahamwe[umwirondoro]
	entry.amabendera = amabendera
	if isImiziInzira(inziraaddress) {
		entry.kind = fdkindImiziUbubiko
		entry.ingano = 0
	} else {
		izinalen, izina := gukopororaInzira(inziraaddress)
		if izinalen == 0 {
			*entry = gufunguraIdosiyeUmwirondoro{}
			return Enoent
		}
		ingano := idosiyeIngano(izina[:izinalen])
		if ingano == 0 {
			*entry = gufunguraIdosiyeUmwirondoro{}
			return Enoent
		}
		if (amabendera & oUbubiko) != 0 {
			*entry = gufunguraIdosiyeUmwirondoro{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.ingano = ingano
		entry.izinalen = izinalen
		entry.izina = izina
	}

	fd := allocatefd(process, umwirondoro, 3)
	if fd < 0 {
		*entry = gufunguraIdosiyeUmwirondoro{}
		return fd
	}
	return fd
}

func sysGufunga(fd int32) int32 {
	return gufungaprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getGufunguraIdosiyefor(process, fd)
	if entry == nil {
		return Ebadf
	}
	newfd := allocatefd(process, process.fds[fd].umwirondoro, minimum)
	if newfd >= 0 {
		entry.refs++
	}
	return newfd
}

func sysdup2(oldfd int32, newfd int32) int32 {
	process := ensurecurrentprocess()
	entry := getGufunguraIdosiyefor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if newfd < 0 || newfd >= maxfd {
		return Ebadf
	}
	if oldfd == newfd {
		return newfd
	}
	if process.fds[newfd].used {
		gufungaprocessfd(process, newfd)
	}
	process.fds[newfd] = fdentry{used: true, umwirondoro: process.fds[oldfd].umwirondoro}
	entry.refs++
	return newfd
}

func sysfcntl(fd int32, icyowifuza uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getGufunguraIdosiyefor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch icyowifuza {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdAmabendera)
	case fsetfd:
		process.fds[fd].fdAmabendera = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.amabendera)
	case fsetfl:
		entry.amabendera = (entry.amabendera & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getGufunguraIdosiye(fd)
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
		base = int64(entry.ingano)
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

func gusomavfsIdosiye(entry *gufunguraIdosiyeUmwirondoro, destination_2 []byte, count uint32) int32 {
	ububikomanager := &mem.TUbubikomanager{}
	tmppointer := ububikomanager.Malloc(entry.ingano)
	if tmppointer == nil {
		return Einval
	}
	tmp := GetBayitefrompointer(uintptr(tmppointer), int(entry.ingano), int(entry.ingano))
	gusomaIdosiye(entry.izina[:entry.izinalen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	ububikomanager.Kigenga(tmppointer)
	return int32(count)
}

func isImiziInzira(inziraaddress uint32) bool {
	if inziraaddress == 0 {
		return false
	}
	inzira := GetBayitefrompointer(uintptr(inziraaddress), 4, 4)
	if inzira[0] == '/' && inzira[1] == 0 {
		return true
	}
	if inzira[0] == '.' && inzira[1] == 0 {
		return true
	}
	if inzira[0] == '/' && inzira[1] == '.' && inzira[2] == 0 {
		return true
	}
	return false
}

func sysaccess(inziraaddress uint32, ubwoko uint32) int32 {
	if inziraaddress == 0 {
		return Efault
	}
	if (ubwoko & ^uint32(7)) != 0 {
		return Einval
	}
	isImizi := isImiziInzira(inziraaddress)
	exists := isImizi
	if !exists {
		izinalen, izina := gukopororaInzira(inziraaddress)
		exists = izinalen != 0 && idosiyeIngano(izina[:izinalen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (ubwoko & 2) != 0 {
		return Eacces
	}

	if (ubwoko&1) != 0 && !isImizi {
		return Eacces
	}
	return 0
}

func syschdir(inziraaddress uint32) int32 {
	if inziraaddress == 0 {
		return Efault
	}
	if !isImiziInzira(inziraaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, ingano uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if ingano < 2 {
		return Erange
	}
	buffer_2 := GetBayitefrompointer(uintptr(bufferaddress), int(ingano), int(ingano))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, ubwoko uint32, ingano uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Ububiko = 1
	stat.Ino = inode
	stat.Ubwoko = ubwoko
	stat.Nlink = 1
	stat.Ingano_2 = int32(ingano)
	stat.Blksize = 512
	stat.Block = int32((ingano + 511) / 512)
	return 0
}

func sysstat(inziraaddress uint32, stataddress uint32) int32 {
	if inziraaddress == 0 {
		return Efault
	}
	if isImiziInzira(inziraaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	izinalen, izina := gukopororaInzira(inziraaddress)
	if izinalen == 0 {
		return Enoent
	}
	ingano := idosiyeIngano(izina[:izinalen])
	if ingano == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < izinalen; i++ {
		inode = inode*33 + uint32(izina[i])
	}
	return fillposixstat(stataddress, sifreg|0444, ingano, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getGufunguraIdosiye(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindImiziUbubiko:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.ingano, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getGufunguraIdosiye(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensurecurrentprocess()
	if process == nil {
		return 0
	}
	if process.porogaramubreak == 0 {
		process.porogaramubreak = ukoreshaheapbase
	}
	if address_2 == 0 {
		return process.porogaramubreak
	}
	if address_2 < ukoreshaheapbase || address_2 > ukoreshaheaplimit {
		return process.porogaramubreak
	}
	process.porogaramubreak = address_2
	return process.porogaramubreak
}

func gukopororautsfield(destination *[65]byte, agaciro string) {
	limit := len(agaciro)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = agaciro[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	izina := (*posixutsname)(Pointer(uintptr(address_2)))
	*izina = posixutsname{}
	gukopororautsfield(&izina.Sysname, "EngOS")
	gukopororautsfield(&izina.Nodename, "engos")
	gukopororautsfield(&izina.Release, "0.1-posix")
	gukopororautsfield(&izina.Version, "POSIX.1-2017 phase 1")
	gukopororautsfield(&izina.Machine, "i386")
	return 0
}

func swapunsignedinteger16(agaciro uint16) uint16 {
	return (agaciro << 8) | (agaciro >> 8)
}

func socketcallargument(arguments_2 uint32, umubarendanga uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + umubarendanga*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getGufunguraIdosiye(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.used {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketUbwoko uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketUbwoko != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	socketUmubarendanga := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].used {
			socketUmubarendanga = i
			break
		}
	}
	if socketUmubarendanga < 0 {
		return Enfile
	}
	umwirondoro := allocateGufunguraIdosiye()
	if umwirondoro < 0 {
		return umwirondoro
	}
	localsockets[socketUmubarendanga] = localdatagramsocket{used: true}
	entry := &gufunguraIdosiyeImbonerahamwe[umwirondoro]
	entry.kind = fdkindsocket
	entry.amabendera = ogusomakwandika
	entry.aux = uint32(socketUmubarendanga)
	fd := allocatefd(process, umwirondoro, 3)
	if fd < 0 {
		localsockets[socketUmubarendanga] = localdatagramsocket{}
		*entry = gufunguraIdosiyeUmwirondoro{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, length uint32) (*socketaddressiAgacirokikigihe4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if length < 16 {
		return nil, Einval
	}
	result := (*socketaddressiAgacirokikigihe4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func umuyoboroImbereuse(umuyoboro uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.used && socket.bound && socket.local.Umuyoboro == umuyoboro {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		umuyoboro := swapunsignedinteger16(ikurikiraephemeralUmuyoboro)
		ikurikiraephemeralUmuyoboro++
		if ikurikiraephemeralUmuyoboro < 49152 {
			ikurikiraephemeralUmuyoboro = 49152
		}
		if !umuyoboroImbereuse(umuyoboro, socket) {
			socket.local = socketaddressiAgacirokikigihe4{Family: afinet, Umuyoboro: umuyoboro, Address: 0x0100007F}
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
	if requested.Umuyoboro == 0 {
		return bindephemeral(socket)
	}
	if umuyoboroImbereuse(requested.Umuyoboro, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketconnect(fd int32, address_2 uint32, length uint32) int32 {
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
	if length > maxdatagramIngano {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressiAgacirokikigihe4
	if destinationaddress != 0 {
		address_2, addressIkosa := socketaddress(destinationaddress, destinationlength)
		if addressIkosa != 0 {
			return addressIkosa
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindIkosa := bindephemeral(socket); bindIkosa != 0 {
			return bindIkosa
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.used && candidate.bound && candidate.local.Umuyoboro == destination.Umuyoboro &&
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
	*packet = socketpacket{used: true, ingano: length, inkomoko: socket.local}
	if length != 0 {
		inkomoko := GetBayitefrompointer(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], inkomoko)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, inkomokoaddress uint32, inkomokolengthaddress uint32) int32 {
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
	gukopororalength := packet.ingano
	if gukopororalength > length {
		gukopororalength = length
	}
	if gukopororalength != 0 {
		destination := GetBayitefrompointer(uintptr(bufferaddress_2), int(gukopororalength), int(gukopororalength))
		copy(destination, packet.data[:gukopororalength])
	}
	if inkomokoaddress != 0 {
		if inkomokolengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(inkomokolengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressiAgacirokikigihe4)(Pointer(uintptr(inkomokoaddress))) = packet.inkomoko
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(gukopororalength)
}

func gukopororasocketIzina(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
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
		*(*socketaddressiAgacirokikigihe4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindIkosa := bindephemeral(socket); bindIkosa != 0 {
				return bindIkosa
			}
		}
		*(*socketaddressiAgacirokikigihe4)(Pointer(uintptr(address_2))) = socket.local
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
		return socketconnect(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return gukopororasocketIzina(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return gukopororasocketIzina(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
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

func gusomastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBayitefrompointer(uintptr(address), int(count), int(count))
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
	ikurikira := (stdinkwandika + 1) % uint32(len(stdinbuffer))
	if ikurikira == stdingusoma {
		return
	}
	stdinbuffer[stdinkwandika] = c
	stdinkwandika = ikurikira
}

func stdingetblocking() byte {
	for stdingusoma == stdinkwandika {
		sc := pollMwandikishoscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdingusoma]
	stdingusoma = (stdingusoma + 1) % uint32(len(stdinbuffer))
	return c
}

func pollMwandikishoscancode() byte {
	for (Umuyoborogusomabyte(0x64) & 0x01) == 0 {
	}
	sc := Umuyoborogusomabyte(0x60)
	return scancodetobyte_2(sc)
}

func scancodetobyte_2(sc uint8) byte {
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

func gukopororaexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for umubarendanga := uint32(0); umubarendanga < maxexecvectorentry; umubarendanga++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + umubarendanga*4)))
		if stringaddress == 0 {
			result.count = umubarendanga
			return 0
		}
		terminated := false
		for length := uint32(0); length <= maxexecstringlength; length++ {
			agaciro := *(*byte)(Pointer(uintptr(stringaddress + length)))
			result.values[umubarendanga][length] = agaciro
			if agaciro == 0 {
				result.lengths[umubarendanga] = length
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

func pushexecunsignedinteger32(stack *uint32, agaciro uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = agaciro
}

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackBayite uint32 = 4096
	if !MakeIgiceprivatewritable(getcr3(), Ukoreshastacktop-stackBayite, stackBayite) {
		return Enomem
	}
	stack := Ukoreshastacktop
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := GetBayitefrompointer(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := GetBayitefrompointer(uintptr(stack), int(length), int(length))
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

func gufungaKuriexec(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used && (process.fds[fd].fdAmabendera&fdcloexec) != 0 {
			gufungaprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, inziraaddress uint32) int32 {
	if inziraaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := gukopororaexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := gukopororaexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	izinalen, izina := gukopororaInzira(inziraaddress)
	if izinalen == 0 {
		return Enoent
	}
	ingano := idosiyeIngano(izina[:izinalen])
	if ingano == 0 {
		return Enoent
	}
	ububikomanager := &mem.TUbubikomanager{}
	idosiyepointer := ububikomanager.Malloc(ingano)
	if idosiyepointer == nil {
		return Einval
	}
	data := GetBayitefrompointer(uintptr(idosiyepointer), int(ingano), int(ingano))
	gusomaIdosiye(izina[:izinalen], data)
	if ingano < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		ububikomanager.Kigenga(idosiyepointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	ububikomanager.Kigenga(idosiyepointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	gufungaKuriexec(ensurecurrentprocess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
	parentpid := Currentpid()
	if ensurecurrentprocess() == nil {
		return Enfile
	}
	pid := allocateprocess(parentpid)
	if pid == 0 {
		return Einval
	}
	ububikomanager := &mem.TUbubikomanager{}
	threadpointer := ububikomanager.Malloc(uint32(Sizeof(TThread{})))
	stackpointer := ububikomanager.Malloc(ThreadstackIngano)
	childIpajiUbubiko := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childIpajiUbubiko == 0 {
		discardprocess(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackpointer) + ThreadstackIngano - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Ukoreshastack_2 = cpu.Esp
	child.UkoreshastackIngano_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.IpajiUbubikoentry = childIpajiUbubiko
	child.Threadstate = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Kongerarunnablethread(child)
	return int32(pid)
}

func sysGusohoka(imimerere uint32) {
	pid := Currentpid()
	for i := 0; i < len(processImbonerahamwe); i++ {
		if processImbonerahamwe[i].used && processImbonerahamwe[i].pid == pid {
			gufungaByoseprocessfds(&processImbonerahamwe[i])
			processImbonerahamwe[i].exited = true
			processImbonerahamwe[i].imimerere = (imimerere & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, imimerereaddress uint32, amahitamo uint32) int32 {
	if (amahitamo & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(processImbonerahamwe); i++ {
		p := &processImbonerahamwe[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.used && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if imimerereaddress != 0 {
					*(*uint32)(Pointer(uintptr(imimerereaddress))) = p.imimerere
				}
				childpid := p.pid
				*p = processentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (amahitamo & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(parent uint32) uint32 {
	parentprocess := gushakaprocess(parent)
	pid := Allocatepid()
	for i := 0; i < len(processImbonerahamwe); i++ {
		if !processImbonerahamwe[i].used {
			processImbonerahamwe[i] = processentry{
				used:			true,
				pid:			pid,
				parent:			parent,
				porogaramubreak:	ukoreshaheapbase,
			}
			if parentprocess != nil {
				processImbonerahamwe[i].porogaramubreak = parentprocess.porogaramubreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocess.fds[fd].used {
						processImbonerahamwe[i].fds[fd] = parentprocess.fds[fd]
						umwirondoro := parentprocess.fds[fd].umwirondoro
						if umwirondoro >= 0 && umwirondoro < maxGufungurafiles {
							gufunguraIdosiyeImbonerahamwe[umwirondoro].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processImbonerahamwe[i])
			}
			return pid
		}
	}
	return 0
}

func gufungaByoseprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used {
			gufungaprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := gushakaprocess(pid)
	if process == nil {
		return
	}
	gufungaByoseprocessfds(process)
	*process = processentry{}
}

func gukopororaInzira(inziraaddress uint32) (uint32, [12]byte) {
	var izina [12]byte
	if inziraaddress == 0 {
		return 0, izina
	}
	raw := GetBayitefrompointer(uintptr(inziraaddress), 64, 64)
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
		izina[n] = c
		n++
	}
	return n, izina
}

func idosiyeIngano(izinaryidosiye []byte) uint32 {
	var ata0s = TUrwegorwohejurutechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionImbonerahamwe{}
	partition.Gusomapartition(&ata0s)

	bios := TBiosparameterblock32{}
	ingano := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye)
	ata0s.Flush()
	return ingano
}

func gusomaIdosiye(izinaryidosiye []byte, data []byte) {
	var ata0s = TUrwegorwohejurutechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionImbonerahamwe{}
	partition.Gusomapartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Gusoma(&ata0s, partition.Mbr.Primarypartition[0], izinaryidosiye, data)
	ata0s.Flush()
}

func getcr3() uint32
