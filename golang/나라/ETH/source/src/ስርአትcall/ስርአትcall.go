package ስርአትcall

import . "unsafe"

import . "ማቋረጫ"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "ፋይልስርአት/msdospartition"
import . "ፋይልስርአት/fat"
import . "ፋይልስርአት/elf"
import mem "ማስታወሻmanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualማስታወሻ"

var console_2 = TConsole{}

type TSyscall struct {
	Tማቋረጫhandler
}

const (
	Sysውጣ		uint32	= 1
	Sysfork		uint32	= 2
	Sysማንበቢያ	uint32	= 3
	Sysመጻፊያ		uint32	= 4
	Sysመክፈቻ		uint32	= 5
	Sysመዝጊያ		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysመድረሻ		uint32	= 33
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
	Sysrtውጣ		uint32	= 252

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
	maxመክፈቻfiles		= 128
)

type fdentry struct {
	የተጠቀሙት		bool
	መግለጫ		int32
	fdባንዲራዎች	uint32
}

type መክፈቻፋይልመግለጫ struct {
	የተጠቀሙት	bool
	refs	uint32
	kind	uint32
	ባንዲራዎች	uint32
	አካባቢ_2	uint32
	መጠን	uint32
	ስም	[12]byte
	ስምlen	uint32
	aux	uint32
}

const (
	fdkindምንም		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindrootዳይሬክቶሪ	uint32	= 4
	fdkindሶኬት		uint32	= 5

	oማንበቢያonly	uint32	= 0
	oመጻፊያonly	uint32	= 1
	oማንበቢያመጻፊያ	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oዳይሬክቶሪ		uint32	= 0x10000

	seekset		uint32	= 0
	seekcurrent	uint32	= 1
	seekመጨረሻ	uint32	= 2

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
	afinet		= 2
	sockdatagram	= 2
	ipprotocoludp	= 17
	maxsockets	= 32
	maxሶኬትpackets	= 8
	maxdatagramመጠን	= 512
)

type ሶኬትaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type ሶኬትpacket struct {
	የተጠቀሙት	bool
	መጠን	uint32
	ምንጩ	ሶኬትaddressipv4
	data	[maxdatagramመጠን]byte
}

type አካባቢdatagramሶኬት struct {
	የተጠቀሙት		bool
	bound		bool
	connected	bool
	አካባቢ		ሶኬትaddressipv4
	remote		ሶኬትaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxሶኬትpackets]ሶኬትpacket
}

type posixstat struct {
	Dዲቫይስ		uint32
	Ino		uint32
	Mዘዴ		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sመጠን_2		int32
	Blksize		int32
	Bመከልከያ		int32
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
	Vእትም		[65]byte
	Machine		[65]byte
}

const (
	maxexecvectorentry	= 16
	maxexecሐረግእርዝመት		= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecሐረግእርዝመት + 1]byte
}

type ሂደቶችentry struct {
	የተጠቀሙት		bool
	pid		uint32
	ወላጅ		uint32
	ወጥቷል		bool
	ሁኔታ		uint32
	ፕሮግራምbreak	uint32
	fds		[maxfd]fdentry
}

type ሐረግheader struct {
	Data	uintptr
	Len	int
}

func syscallስህተት(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var መክፈቻፋይልሰንጠረዥ [maxመክፈቻfiles]መክፈቻፋይልመግለጫ
var ሂደቶችሰንጠረዥ [32]ሂደቶችentry
var አካባቢsockets [maxsockets]አካባቢdatagramሶኬት
var የሚቀጥለውephemeralport uint16 = 49152

const (
	ተጠቃሚheapbase	uint32	= 0x06000000
	ተጠቃሚheapገደብ	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinማንበቢያ uint32
var stdinመጻፊያ uint32

func Iማቋረጫ(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysውጣ_2(ማውጫ uint32) {
	Syscall(Sysውጣ, ማውጫ)
}

func Sysማንበቢያ_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysማንበቢያ, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysማተሚያstr(buffer string) {
	h := (*ሐረግheader)(Pointer(&buffer))
	Syscall(Sysመጻፊያ, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysማተሚያunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysመጻፊያ, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysመክፈቻ_2(መተላለፊያ uintptr, ባንዲራዎች uint32, ዘዴ uint32) int32 {
	return int32(Syscall(Sysመክፈቻ, uint32(መተላለፊያ), ባንዲራዎች, ዘዴ))
}

func Sysመዝጊያ_2(fd uint32) int32 {
	return int32(Syscall(Sysመዝጊያ, fd))
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
		return Iማቋረጫ(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Iማቋረጫ(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Iማቋረጫ(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Iማቋረጫ(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Iማቋረጫ(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Iማቋረጫ(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallስህተት(Enosys)
	}
}

func (self *TSyscall) Init(manager *Tማቋረጫmanager) {
	initፋይልdescriptor()

	ማቋረጫhandler = handleማቋረጫ

	var address uintptr
	address = uintptr(Pointer(&ማቋረጫhandler))

	self.Tማቋረጫhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var ማቋረጫhandler func(uint32) uint32

func handleማቋረጫ(esp uint32) uint32 {
	var cpu = (*Tcpuሁኔታ)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysውጣ:
		sysውጣ(cpu.Ebx)
		return uint32(uintptr(Pointer(Sማስቆሚያcurrentthread(cpu))))
	case Sysrtውጣ:
		sysውጣ(cpu.Ebx)
		return uint32(uintptr(Pointer(Sማስቆሚያcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysማንበቢያ:
		cpu.Eax = uint32(sysማንበቢያ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysመጻፊያ:
		cpu.Eax = uint32(sysመጻፊያ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysመክፈቻ:
		cpu.Eax = uint32(sysመክፈቻ(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysመክፈቻ(cpu.Ebx, ocreate|oመጻፊያonly|otruncate, cpu.Ecx))
		return esp
	case Sysመዝጊያ:
		cpu.Eax = uint32(sysመዝጊያ(int32(cpu.Ebx)))
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
		cpu.Eax = Currentወላጅpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysመድረሻ:
		cpu.Eax = uint32(sysመድረሻ(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysሶኬትcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32ማተሚያ(cpu.Ebx)
		return esp

	default:
		console_2.Mማተሚያxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32ማተሚያ(esp)
		console_2.Mማተሚያ(([]byte)(":"))
		console_2.MUnsignedinteger32ማተሚያ(cpu.Eax)
		console_2.Mማተሚያ(([]byte)(":"))
		console_2.MUnsignedinteger32ማተሚያ(cpu.Ebx)
		console_2.Mማተሚያ(([]byte)(":"))
		console_2.MUnsignedinteger32ማተሚያ(cpu.Ecx)
		console_2.Mማተሚያ(([]byte)(":"))
		console_2.MUnsignedinteger32ማተሚያ(cpu.Edx)
		console_2.Mማተሚያ(([]byte)("]"))
		cpu.Eax = syscallስህተት(Enosys)
		return esp
	}

	return esp
}

func initፋይልdescriptor() {
	for i := 0; i < maxመክፈቻfiles; i++ {
		መክፈቻፋይልሰንጠረዥ[i] = መክፈቻፋይልመግለጫ{}
	}
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		ሂደቶችሰንጠረዥ[i] = ሂደቶችentry{}
	}
	for i := 0; i < len(አካባቢsockets); i++ {
		አካባቢsockets[i] = አካባቢdatagramሶኬት{}
	}
	የሚቀጥለውephemeralport = 49152
	መክፈቻፋይልሰንጠረዥ[0] = መክፈቻፋይልመግለጫ{የተጠቀሙት: true, kind: fdkindstdin, ባንዲራዎች: oማንበቢያonly}
	መክፈቻፋይልሰንጠረዥ[1] = መክፈቻፋይልመግለጫ{የተጠቀሙት: true, kind: fdkindconsole, ባንዲራዎች: oመጻፊያonly}
	መክፈቻፋይልሰንጠረዥ[2] = መክፈቻፋይልመግለጫ{የተጠቀሙት: true, kind: fdkindconsole, ባንዲራዎች: oመጻፊያonly}
}

func መፈለጊያሂደቶች(pid uint32) *ሂደቶችentry {
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		if ሂደቶችሰንጠረዥ[i].የተጠቀሙት && ሂደቶችሰንጠረዥ[i].pid == pid {
			return &ሂደቶችሰንጠረዥ[i]
		}
	}
	return nil
}

func initializeሂደቶችfds(ሂደቶች *ሂደቶችentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		ሂደቶች.fds[fd] = fdentry{የተጠቀሙት: true, መግለጫ: fd}
		መክፈቻፋይልሰንጠረዥ[fd].refs++
	}
}

func ensurecurrentሂደቶች() *ሂደቶችentry {
	pid := Currentpid()
	if ሂደቶች := መፈለጊያሂደቶች(pid); ሂደቶች != nil {
		return ሂደቶች
	}
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		if !ሂደቶችሰንጠረዥ[i].የተጠቀሙት {
			ሂደቶችሰንጠረዥ[i] = ሂደቶችentry{
				የተጠቀሙት:		true,
				pid:		pid,
				ወላጅ:		Currentወላጅpid(),
				ፕሮግራምbreak:	ተጠቃሚheapbase,
			}
			initializeሂደቶችfds(&ሂደቶችሰንጠረዥ[i])
			return &ሂደቶችሰንጠረዥ[i]
		}
	}
	return nil
}

func getመክፈቻፋይልfor(ሂደቶች *ሂደቶችentry, fd int32) *መክፈቻፋይልመግለጫ {
	if ሂደቶች == nil || fd < 0 || fd >= maxfd || !ሂደቶች.fds[fd].የተጠቀሙት {
		return nil
	}
	መግለጫ := ሂደቶች.fds[fd].መግለጫ
	if መግለጫ < 0 || መግለጫ >= maxመክፈቻfiles || !መክፈቻፋይልሰንጠረዥ[መግለጫ].የተጠቀሙት {
		return nil
	}
	return &መክፈቻፋይልሰንጠረዥ[መግለጫ]
}

func getመክፈቻፋይል(fd int32) *መክፈቻፋይልመግለጫ {
	return getመክፈቻፋይልfor(ensurecurrentሂደቶች(), fd)
}

func allocateመክፈቻፋይል() int32 {
	for i := int32(3); i < maxመክፈቻfiles; i++ {
		if !መክፈቻፋይልሰንጠረዥ[i].የተጠቀሙት {
			መክፈቻፋይልሰንጠረዥ[i] = መክፈቻፋይልመግለጫ{የተጠቀሙት: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(ሂደቶች *ሂደቶችentry, መግለጫ int32, አነስተኛ int32) int32 {
	if ሂደቶች == nil {
		return Enfile
	}
	if አነስተኛ < 0 || አነስተኛ >= maxfd {
		return Einval
	}
	for fd := አነስተኛ; fd < maxfd; fd++ {
		if !ሂደቶች.fds[fd].የተጠቀሙት {
			ሂደቶች.fds[fd] = fdentry{የተጠቀሙት: true, መግለጫ: መግለጫ}
			return fd
		}
	}
	return Emfile
}

func releaseመክፈቻፋይል(መግለጫ int32) {
	if መግለጫ < 0 || መግለጫ >= maxመክፈቻfiles {
		return
	}
	entry := &መክፈቻፋይልሰንጠረዥ[መግለጫ]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && መግለጫ > stderrfd {
		if entry.kind == fdkindሶኬት && entry.aux < maxsockets {
			አካባቢsockets[entry.aux] = አካባቢdatagramሶኬት{}
		}
		*entry = መክፈቻፋይልመግለጫ{}
	}
}

func መዝጊያሂደቶችfd(ሂደቶች *ሂደቶችentry, fd int32) int32 {
	if ሂደቶች == nil || getመክፈቻፋይልfor(ሂደቶች, fd) == nil {
		return Ebadf
	}
	መግለጫ := ሂደቶች.fds[fd].መግለጫ
	ሂደቶች.fds[fd] = fdentry{}
	releaseመክፈቻፋይል(መግለጫ)
	return 0
}

func sysመጻፊያ(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getመክፈቻፋይል(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindሶኬት {
			return ሶኬትsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootዳይሬክቶሪ {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getባይትስfromጠቋሚ(uintptr(address), int(count), int(count))
	console_2.Mማተሚያ(buffer)
	return int32(count)
}

func sysማንበቢያ(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getመክፈቻፋይል(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return ማንበቢያstdin(address, count)
	}
	if entry.kind == fdkindrootዳይሬክቶሪ {
		return Eisdir
	}
	if entry.kind == fdkindሶኬት {
		return ሶኬትreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.አካባቢ_2 >= entry.መጠን {
		return 0
	}
	remaining := entry.መጠን - entry.አካባቢ_2
	if count > remaining {
		count = remaining
	}
	buffer := Getባይትስfromጠቋሚ(uintptr(address), int(count), int(count))
	return ማንበቢያvfsፋይል(entry, buffer, count)
}

func sysመክፈቻ(መተላለፊያaddress uint32, ባንዲራዎች uint32, ዘዴ uint32) int32 {
	_ = ዘዴ
	if መተላለፊያaddress == 0 {
		return Efault
	}
	መድረሻዘዴ := ባንዲራዎች & 3
	if መድረሻዘዴ == oመጻፊያonly || መድረሻዘዴ == oማንበቢያመጻፊያ || (ባንዲራዎች&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	ሂደቶች := ensurecurrentሂደቶች()
	if ሂደቶች == nil {
		return Enfile
	}
	መግለጫ := allocateመክፈቻፋይል()
	if መግለጫ < 0 {
		return መግለጫ
	}
	entry := &መክፈቻፋይልሰንጠረዥ[መግለጫ]
	entry.ባንዲራዎች = ባንዲራዎች
	if isrootመተላለፊያ(መተላለፊያaddress) {
		entry.kind = fdkindrootዳይሬክቶሪ
		entry.መጠን = 0
	} else {
		ስምlen, ስም := ኮፒመተላለፊያ(መተላለፊያaddress)
		if ስምlen == 0 {
			*entry = መክፈቻፋይልመግለጫ{}
			return Enoent
		}
		መጠን := ፋይልመጠን(ስም[:ስምlen])
		if መጠን == 0 {
			*entry = መክፈቻፋይልመግለጫ{}
			return Enoent
		}
		if (ባንዲራዎች & oዳይሬክቶሪ) != 0 {
			*entry = መክፈቻፋይልመግለጫ{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.መጠን = መጠን
		entry.ስምlen = ስምlen
		entry.ስም = ስም
	}

	fd := allocatefd(ሂደቶች, መግለጫ, 3)
	if fd < 0 {
		*entry = መክፈቻፋይልመግለጫ{}
		return fd
	}
	return fd
}

func sysመዝጊያ(fd int32) int32 {
	return መዝጊያሂደቶችfd(ensurecurrentሂደቶች(), fd)
}

func sysdup(fd int32, አነስተኛ int32) int32 {
	ሂደቶች := ensurecurrentሂደቶች()
	entry := getመክፈቻፋይልfor(ሂደቶች, fd)
	if entry == nil {
		return Ebadf
	}
	አዲስfd := allocatefd(ሂደቶች, ሂደቶች.fds[fd].መግለጫ, አነስተኛ)
	if አዲስfd >= 0 {
		entry.refs++
	}
	return አዲስfd
}

func sysdup2(oldfd int32, አዲስfd int32) int32 {
	ሂደቶች := ensurecurrentሂደቶች()
	entry := getመክፈቻፋይልfor(ሂደቶች, oldfd)
	if entry == nil {
		return Ebadf
	}
	if አዲስfd < 0 || አዲስfd >= maxfd {
		return Ebadf
	}
	if oldfd == አዲስfd {
		return አዲስfd
	}
	if ሂደቶች.fds[አዲስfd].የተጠቀሙት {
		መዝጊያሂደቶችfd(ሂደቶች, አዲስfd)
	}
	ሂደቶች.fds[አዲስfd] = fdentry{የተጠቀሙት: true, መግለጫ: ሂደቶች.fds[oldfd].መግለጫ}
	entry.refs++
	return አዲስfd
}

func sysfcntl(fd int32, ትእዛዝ uint32, argument uint32) int32 {
	ሂደቶች := ensurecurrentሂደቶች()
	entry := getመክፈቻፋይልfor(ሂደቶች, fd)
	if entry == nil {
		return Ebadf
	}
	switch ትእዛዝ {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(ሂደቶች.fds[fd].fdባንዲራዎች)
	case fsetfd:
		ሂደቶች.fds[fd].fdባንዲራዎች = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.ባንዲራዎች)
	case fsetfl:
		entry.ባንዲራዎች = (entry.ባንዲራዎች & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getመክፈቻፋይል(fd)
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
		base = int64(entry.አካባቢ_2)
	case seekመጨረሻ:
		base = int64(entry.መጠን)
	default:
		return Einval
	}
	አካባቢ_3 := base + int64(offset)
	if አካባቢ_3 < 0 || አካባቢ_3 > 0x7FFFFFFF {
		return Einval
	}
	entry.አካባቢ_2 = uint32(አካባቢ_3)
	return int32(entry.አካባቢ_2)
}

func ማንበቢያvfsፋይል(entry *መክፈቻፋይልመግለጫ, destination_2 []byte, count uint32) int32 {
	ማስታወሻmanager := &mem.Tማስታወሻmanager{}
	tmpጠቋሚ := ማስታወሻmanager.Malloc(entry.መጠን)
	if tmpጠቋሚ == nil {
		return Einval
	}
	tmp := Getባይትስfromጠቋሚ(uintptr(tmpጠቋሚ), int(entry.መጠን), int(entry.መጠን))
	ማንበቢያፋይል(entry.ስም[:entry.ስምlen], tmp)
	copy(destination_2[:count], tmp[entry.አካባቢ_2:entry.አካባቢ_2+count])
	entry.አካባቢ_2 += count
	ማስታወሻmanager.Fነፃ(tmpጠቋሚ)
	return int32(count)
}

func isrootመተላለፊያ(መተላለፊያaddress uint32) bool {
	if መተላለፊያaddress == 0 {
		return false
	}
	መተላለፊያ := Getባይትስfromጠቋሚ(uintptr(መተላለፊያaddress), 4, 4)
	if መተላለፊያ[0] == '/' && መተላለፊያ[1] == 0 {
		return true
	}
	if መተላለፊያ[0] == '.' && መተላለፊያ[1] == 0 {
		return true
	}
	if መተላለፊያ[0] == '/' && መተላለፊያ[1] == '.' && መተላለፊያ[2] == 0 {
		return true
	}
	return false
}

func sysመድረሻ(መተላለፊያaddress uint32, ዘዴ uint32) int32 {
	if መተላለፊያaddress == 0 {
		return Efault
	}
	if (ዘዴ & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootመተላለፊያ(መተላለፊያaddress)
	exists := isroot
	if !exists {
		ስምlen, ስም := ኮፒመተላለፊያ(መተላለፊያaddress)
		exists = ስምlen != 0 && ፋይልመጠን(ስም[:ስምlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (ዘዴ & 2) != 0 {
		return Eacces
	}

	if (ዘዴ&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(መተላለፊያaddress uint32) int32 {
	if መተላለፊያaddress == 0 {
		return Efault
	}
	if !isrootመተላለፊያ(መተላለፊያaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, መጠን uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if መጠን < 2 {
		return Erange
	}
	buffer_2 := Getባይትስfromጠቋሚ(uintptr(bufferaddress), int(መጠን), int(መጠን))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, ዘዴ uint32, መጠን uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dዲቫይስ = 1
	stat.Ino = inode
	stat.Mዘዴ = ዘዴ
	stat.Nlink = 1
	stat.Sመጠን_2 = int32(መጠን)
	stat.Blksize = 512
	stat.Bመከልከያ = int32((መጠን + 511) / 512)
	return 0
}

func sysstat(መተላለፊያaddress uint32, stataddress uint32) int32 {
	if መተላለፊያaddress == 0 {
		return Efault
	}
	if isrootመተላለፊያ(መተላለፊያaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	ስምlen, ስም := ኮፒመተላለፊያ(መተላለፊያaddress)
	if ስምlen == 0 {
		return Enoent
	}
	መጠን := ፋይልመጠን(ስም[:ስምlen])
	if መጠን == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < ስምlen; i++ {
		inode = inode*33 + uint32(ስም[i])
	}
	return fillposixstat(stataddress, sifreg|0444, መጠን, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getመክፈቻፋይል(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootዳይሬክቶሪ:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.መጠን, uint32(fd+2))
	case fdkindሶኬት:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getመክፈቻፋይል(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	ሂደቶች := ensurecurrentሂደቶች()
	if ሂደቶች == nil {
		return 0
	}
	if ሂደቶች.ፕሮግራምbreak == 0 {
		ሂደቶች.ፕሮግራምbreak = ተጠቃሚheapbase
	}
	if address_2 == 0 {
		return ሂደቶች.ፕሮግራምbreak
	}
	if address_2 < ተጠቃሚheapbase || address_2 > ተጠቃሚheapገደብ {
		return ሂደቶች.ፕሮግራምbreak
	}
	ሂደቶች.ፕሮግራምbreak = address_2
	return ሂደቶች.ፕሮግራምbreak
}

func ኮፒutsfield(destination *[65]byte, ዋጋ string) {
	ገደብ := len(ዋጋ)
	if ገደብ > 64 {
		ገደብ = 64
	}
	for i := 0; i < ገደብ; i++ {
		destination[i] = ዋጋ[i]
	}
	destination[ገደብ] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	ስም := (*posixutsname)(Pointer(uintptr(address_2)))
	*ስም = posixutsname{}
	ኮፒutsfield(&ስም.Sysname, "EngOS")
	ኮፒutsfield(&ስም.Nodename, "engos")
	ኮፒutsfield(&ስም.Release, "0.1-posix")
	ኮፒutsfield(&ስም.Vእትም, "POSIX.1-2017 phase 1")
	ኮፒutsfield(&ስም.Machine, "i386")
	return 0
}

func swapunsignedinteger16(ዋጋ uint16) uint16 {
	return (ዋጋ << 8) | (ዋጋ >> 8)
}

func ሶኬትcallargument(arguments_2 uint32, ማውጫ uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + ማውጫ*4)))
}

func ሶኬትforfd(fd int32) (*አካባቢdatagramሶኬት, int32) {
	entry := getመክፈቻፋይል(fd)
	if entry == nil || entry.kind != fdkindሶኬት || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	ሶኬት := &አካባቢsockets[entry.aux]
	if !ሶኬት.የተጠቀሙት {
		return nil, Ebadf
	}
	return ሶኬት, 0
}

func allocateሶኬት(ዶሜን uint32, ሶኬትአይነት uint32, protocol uint32) int32 {
	if ዶሜን != afinet {
		return Eafnosupport
	}
	if ሶኬትአይነት != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	ሂደቶች := ensurecurrentሂደቶች()
	if ሂደቶች == nil {
		return Enfile
	}
	ሶኬትማውጫ := -1
	for i := 0; i < maxsockets; i++ {
		if !አካባቢsockets[i].የተጠቀሙት {
			ሶኬትማውጫ = i
			break
		}
	}
	if ሶኬትማውጫ < 0 {
		return Enfile
	}
	መግለጫ := allocateመክፈቻፋይል()
	if መግለጫ < 0 {
		return መግለጫ
	}
	አካባቢsockets[ሶኬትማውጫ] = አካባቢdatagramሶኬት{የተጠቀሙት: true}
	entry := &መክፈቻፋይልሰንጠረዥ[መግለጫ]
	entry.kind = fdkindሶኬት
	entry.ባንዲራዎች = oማንበቢያመጻፊያ
	entry.aux = uint32(ሶኬትማውጫ)
	fd := allocatefd(ሂደቶች, መግለጫ, 3)
	if fd < 0 {
		አካባቢsockets[ሶኬትማውጫ] = አካባቢdatagramሶኬት{}
		*entry = መክፈቻፋይልመግለጫ{}
		return fd
	}
	return fd
}

func ሶኬትaddress(address_2 uint32, እርዝመት_2 uint32) (*ሶኬትaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if እርዝመት_2 < 16 {
		return nil, Einval
	}
	result := (*ሶኬትaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portውስጥuse(port uint16, except *አካባቢdatagramሶኬት) bool {
	for i := 0; i < maxsockets; i++ {
		ሶኬት := &አካባቢsockets[i]
		if ሶኬት != except && ሶኬት.የተጠቀሙት && ሶኬት.bound && ሶኬት.አካባቢ.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(ሶኬት *አካባቢdatagramሶኬት) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(የሚቀጥለውephemeralport)
		የሚቀጥለውephemeralport++
		if የሚቀጥለውephemeralport < 49152 {
			የሚቀጥለውephemeralport = 49152
		}
		if !portውስጥuse(port, ሶኬት) {
			ሶኬት.አካባቢ = ሶኬትaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			ሶኬት.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func ሶኬትbind(fd int32, address_2 uint32, እርዝመት_2 uint32) int32 {
	ሶኬት, err := ሶኬትforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := ሶኬትaddress(address_2, እርዝመት_2)
	if err != 0 {
		return err
	}
	if ሶኬት.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(ሶኬት)
	}
	if portውስጥuse(requested.Port, ሶኬት) {
		return Eaddrinuse
	}
	ሶኬት.አካባቢ = *requested
	ሶኬት.bound = true
	return 0
}

func ሶኬትመገናኛ(fd int32, address_2 uint32, እርዝመት_2 uint32) int32 {
	ሶኬት, err := ሶኬትforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := ሶኬትaddress(address_2, እርዝመት_2)
	if err != 0 {
		return err
	}
	if !ሶኬት.bound {
		if err := bindephemeral(ሶኬት); err != 0 {
			return err
		}
	}
	ሶኬት.remote = *remote
	ሶኬት.connected = true
	return 0
}

func ሶኬትsendto(fd int32, bufferaddress_2 uint32, እርዝመት_2 uint32, destinationaddress uint32, destinationእርዝመት uint32) int32 {
	ሶኬት, err := ሶኬትforfd(fd)
	if err != 0 {
		return err
	}
	if እርዝመት_2 > maxdatagramመጠን {
		return Emsgsize
	}
	if እርዝመት_2 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination ሶኬትaddressipv4
	if destinationaddress != 0 {
		address_2, addressስህተት := ሶኬትaddress(destinationaddress, destinationእርዝመት)
		if addressስህተት != 0 {
			return addressስህተት
		}
		destination = *address_2
	} else {
		if !ሶኬት.connected {
			return Enotconn
		}
		destination = ሶኬት.remote
	}
	if !ሶኬት.bound {
		if bindስህተት := bindephemeral(ሶኬት); bindስህተት != 0 {
			return bindስህተት
		}
	}
	var receiver *አካባቢdatagramሶኬት
	for i := 0; i < maxsockets; i++ {
		candidate := &አካባቢsockets[i]
		if candidate.የተጠቀሙት && candidate.bound && candidate.አካባቢ.Port == destination.Port &&
			(candidate.አካባቢ.Address == 0 || candidate.አካባቢ.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxሶኬትpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = ሶኬትpacket{የተጠቀሙት: true, መጠን: እርዝመት_2, ምንጩ: ሶኬት.አካባቢ}
	if እርዝመት_2 != 0 {
		ምንጩ := Getባይትስfromጠቋሚ(uintptr(bufferaddress_2), int(እርዝመት_2), int(እርዝመት_2))
		copy(packet.data[:እርዝመት_2], ምንጩ)
	}
	receiver.tail = (receiver.tail + 1) % maxሶኬትpackets
	receiver.count++
	return int32(እርዝመት_2)
}

func ሶኬትreceivefrom(fd int32, bufferaddress_2 uint32, እርዝመት_2 uint32, ምንጩaddress uint32, ምንጩእርዝመትaddress uint32) int32 {
	ሶኬት, err := ሶኬትforfd(fd)
	if err != 0 {
		return err
	}
	if እርዝመት_2 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if ሶኬት.count == 0 {
		return Eagain
	}
	packet := &ሶኬት.packets[ሶኬት.head]
	ኮፒእርዝመት := packet.መጠን
	if ኮፒእርዝመት > እርዝመት_2 {
		ኮፒእርዝመት = እርዝመት_2
	}
	if ኮፒእርዝመት != 0 {
		destination := Getባይትስfromጠቋሚ(uintptr(bufferaddress_2), int(ኮፒእርዝመት), int(ኮፒእርዝመት))
		copy(destination, packet.data[:ኮፒእርዝመት])
	}
	if ምንጩaddress != 0 {
		if ምንጩእርዝመትaddress == 0 {
			return Efault
		}
		providedእርዝመት := (*uint32)(Pointer(uintptr(ምንጩእርዝመትaddress)))
		if *providedእርዝመት >= 16 {
			*(*ሶኬትaddressipv4)(Pointer(uintptr(ምንጩaddress))) = packet.ምንጩ
		}
		*providedእርዝመት = 16
	}
	*packet = ሶኬትpacket{}
	ሶኬት.head = (ሶኬት.head + 1) % maxሶኬትpackets
	ሶኬት.count--
	return int32(ኮፒእርዝመት)
}

func ኮፒሶኬትስም(fd int32, address_2 uint32, እርዝመትaddress uint32, peer bool) int32 {
	ሶኬት, err := ሶኬትforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || እርዝመትaddress == 0 {
		return Efault
	}
	እርዝመት_2 := (*uint32)(Pointer(uintptr(እርዝመትaddress)))
	if *እርዝመት_2 < 16 {
		*እርዝመት_2 = 16
		return Einval
	}
	if peer {
		if !ሶኬት.connected {
			return Enotconn
		}
		*(*ሶኬትaddressipv4)(Pointer(uintptr(address_2))) = ሶኬት.remote
	} else {
		if !ሶኬት.bound {
			if bindስህተት := bindephemeral(ሶኬት); bindስህተት != 0 {
				return bindስህተት
			}
		}
		*(*ሶኬትaddressipv4)(Pointer(uintptr(address_2))) = ሶኬት.አካባቢ
	}
	*እርዝመት_2 = 16
	return 0
}

func sysሶኬትcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateሶኬት(ሶኬትcallargument(arguments_2, 0), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2))
	case 2:
		return ሶኬትbind(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2))
	case 3:
		return ሶኬትመገናኛ(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return ኮፒሶኬትስም(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), false)
	case 7:
		return ኮፒሶኬትስም(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), true)
	case 9:
		return ሶኬትsendto(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), 0, 0)
	case 10:
		return ሶኬትreceivefrom(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), 0, 0)
	case 11:
		return ሶኬትsendto(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), ሶኬትcallargument(arguments_2, 4), ሶኬትcallargument(arguments_2, 5))
	case 12:
		return ሶኬትreceivefrom(int32(ሶኬትcallargument(arguments_2, 0)), ሶኬትcallargument(arguments_2, 1), ሶኬትcallargument(arguments_2, 2), ሶኬትcallargument(arguments_2, 4), ሶኬትcallargument(arguments_2, 5))
	case 13:
		if _, err := ሶኬትforfd(int32(ሶኬትcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := ሶኬትforfd(int32(ሶኬትcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func ማንበቢያstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getባይትስfromጠቋሚ(uintptr(address), int(count), int(count))
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
	የሚቀጥለው := (stdinመጻፊያ + 1) % uint32(len(stdinbuffer))
	if የሚቀጥለው == stdinማንበቢያ {
		return
	}
	stdinbuffer[stdinመጻፊያ] = c
	stdinመጻፊያ = የሚቀጥለው
}

func stdingetblocking() byte {
	for stdinማንበቢያ == stdinመጻፊያ {
		sc := pollየፊደልሠሌዳscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinማንበቢያ]
	stdinማንበቢያ = (stdinማንበቢያ + 1) % uint32(len(stdinbuffer))
	return c
}

func pollየፊደልሠሌዳscancode() byte {
	for (Portማንበቢያbyte(0x64) & 0x01) == 0 {
	}
	sc := Portማንበቢያbyte(0x60)
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

func ኮፒexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for ማውጫ := uint32(0); ማውጫ < maxexecvectorentry; ማውጫ++ {
		ሐረግaddress := *(*uint32)(Pointer(uintptr(address_2 + ማውጫ*4)))
		if ሐረግaddress == 0 {
			result.count = ማውጫ
			return 0
		}
		terminated := false
		for እርዝመት_2 := uint32(0); እርዝመት_2 <= maxexecሐረግእርዝመት; እርዝመት_2++ {
			ዋጋ := *(*byte)(Pointer(uintptr(ሐረግaddress + እርዝመት_2)))
			result.values[ማውጫ][እርዝመት_2] = ዋጋ
			if ዋጋ == 0 {
				result.lengths[ማውጫ] = እርዝመት_2
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

func pushexecunsignedinteger32(stack *uint32, ዋጋ uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = ዋጋ
}

func setupexecstack(cpu *Tcpuሁኔታ, arguments_2 *execvector, environment *execvector) int32 {
	const stackባይትስ uint32 = 4096
	if !Makeመጠንprivatewritable(getcr3(), Uተጠቃሚstackወደላይ-stackባይትስ, stackባይትስ) {
		return Enomem
	}
	stack := Uተጠቃሚstackወደላይ
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		እርዝመት_2 := environment.lengths[i] + 1
		stack -= እርዝመት_2
		destination := Getባይትስfromጠቋሚ(uintptr(stack), int(እርዝመት_2), int(እርዝመት_2))
		copy(destination, environment.values[i][:እርዝመት_2])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		እርዝመት_2 := arguments_2.lengths[i] + 1
		stack -= እርዝመት_2
		destination := Getባይትስfromጠቋሚ(uintptr(stack), int(እርዝመት_2), int(እርዝመት_2))
		copy(destination, arguments_2.values[i][:እርዝመት_2])
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

func መዝጊያማብሪያexec(ሂደቶች *ሂደቶችentry) {
	if ሂደቶች == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if ሂደቶች.fds[fd].የተጠቀሙት && (ሂደቶች.fds[fd].fdባንዲራዎች&fdcloexec) != 0 {
			መዝጊያሂደቶችfd(ሂደቶች, fd)
		}
	}
}

func sysexecve(cpu *Tcpuሁኔታ, መተላለፊያaddress uint32) int32 {
	if መተላለፊያaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := ኮፒexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := ኮፒexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	ስምlen, ስም := ኮፒመተላለፊያ(መተላለፊያaddress)
	if ስምlen == 0 {
		return Enoent
	}
	መጠን := ፋይልመጠን(ስም[:ስምlen])
	if መጠን == 0 {
		return Enoent
	}
	ማስታወሻmanager := &mem.Tማስታወሻmanager{}
	ፋይልጠቋሚ := ማስታወሻmanager.Malloc(መጠን)
	if ፋይልጠቋሚ == nil {
		return Einval
	}
	data := Getባይትስfromጠቋሚ(uintptr(ፋይልጠቋሚ), int(መጠን), int(መጠን))
	ማንበቢያፋይል(ስም[:ስምlen], data)
	if መጠን < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		ማስታወሻmanager.Fነፃ(ፋይልጠቋሚ)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	ማስታወሻmanager.Fነፃ(ፋይልጠቋሚ)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	መዝጊያማብሪያexec(ensurecurrentሂደቶች())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpuሁኔታ) int32 {
	ወላጅpid := Currentpid()
	if ensurecurrentሂደቶች() == nil {
		return Enfile
	}
	pid := allocateሂደቶች(ወላጅpid)
	if pid == 0 {
		return Einval
	}
	ማስታወሻmanager := &mem.Tማስታወሻmanager{}
	threadጠቋሚ := ማስታወሻmanager.Malloc(uint32(Sizeof(TThread{})))
	stackጠቋሚ := ማስታወሻmanager.Malloc(Threadstackመጠን)
	ልጅገጽዳይሬክቶሪ := Cloneaddressspacecow(getcr3())
	if threadጠቋሚ == nil || stackጠቋሚ == nil || ልጅገጽዳይሬክቶሪ == 0 {
		discardሂደቶች(pid)
		return Einval
	}
	ልጅ := (*TThread)(threadጠቋሚ)
	ልጅ.Stack = uint32(uintptr(stackጠቋሚ))
	ልጅ.Cpuሁኔታ = (*Tcpuሁኔታ)(Pointer(uintptr(stackጠቋሚ) + Threadstackመጠን - Sizeof(Tcpuሁኔታ{})))
	*ልጅ.Cpuሁኔታ = *cpu
	ልጅ.Cpuሁኔታ.Eax = 0
	ልጅ.Uተጠቃሚstack_2 = cpu.Esp
	ልጅ.Uተጠቃሚstackመጠን_2 = 0
	ልጅ.Pid = pid
	ልጅ.Pወላጅpid = ወላጅpid
	ልጅ.Pገጽዳይሬክቶሪentry = ልጅገጽዳይሬክቶሪ
	ልጅ.Threadሁኔታ = Rዝግጁ
	ልጅ.Fpuoffset = 0xffffffff
	ልጅ.Iskernel = false
	Aመጨመሪያrunnablethread(ልጅ)
	return int32(pid)
}

func sysውጣ(ሁኔታ uint32) {
	pid := Currentpid()
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		if ሂደቶችሰንጠረዥ[i].የተጠቀሙት && ሂደቶችሰንጠረዥ[i].pid == pid {
			መዝጊያሁሉንምሂደቶችfds(&ሂደቶችሰንጠረዥ[i])
			ሂደቶችሰንጠረዥ[i].ወጥቷል = true
			ሂደቶችሰንጠረዥ[i].ሁኔታ = (ሁኔታ & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, ሁኔታaddress uint32, ምርጫዎች uint32) int32 {
	if (ምርጫዎች & ^uint32(1)) != 0 {
		return Einval
	}
	ወላጅpid := Currentpid()
	foundልጅ := false
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		p := &ሂደቶችሰንጠረዥ[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.የተጠቀሙት && matches && p.ወላጅ == ወላጅpid {
			foundልጅ = true
			if p.ወጥቷል {
				if ሁኔታaddress != 0 {
					*(*uint32)(Pointer(uintptr(ሁኔታaddress))) = p.ሁኔታ
				}
				ልጅpid := p.pid
				*p = ሂደቶችentry{}
				return int32(ልጅpid)
			}
		}
	}
	if !foundልጅ {
		return Echild
	}

	if (ምርጫዎች & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateሂደቶች(ወላጅ uint32) uint32 {
	ወላጅሂደቶች := መፈለጊያሂደቶች(ወላጅ)
	pid := Allocatepid()
	for i := 0; i < len(ሂደቶችሰንጠረዥ); i++ {
		if !ሂደቶችሰንጠረዥ[i].የተጠቀሙት {
			ሂደቶችሰንጠረዥ[i] = ሂደቶችentry{
				የተጠቀሙት:		true,
				pid:		pid,
				ወላጅ:		ወላጅ,
				ፕሮግራምbreak:	ተጠቃሚheapbase,
			}
			if ወላጅሂደቶች != nil {
				ሂደቶችሰንጠረዥ[i].ፕሮግራምbreak = ወላጅሂደቶች.ፕሮግራምbreak
				for fd := 0; fd < maxfd; fd++ {
					if ወላጅሂደቶች.fds[fd].የተጠቀሙት {
						ሂደቶችሰንጠረዥ[i].fds[fd] = ወላጅሂደቶች.fds[fd]
						መግለጫ := ወላጅሂደቶች.fds[fd].መግለጫ
						if መግለጫ >= 0 && መግለጫ < maxመክፈቻfiles {
							መክፈቻፋይልሰንጠረዥ[መግለጫ].refs++
						}
					}
				}
			} else {
				initializeሂደቶችfds(&ሂደቶችሰንጠረዥ[i])
			}
			return pid
		}
	}
	return 0
}

func መዝጊያሁሉንምሂደቶችfds(ሂደቶች *ሂደቶችentry) {
	if ሂደቶች == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if ሂደቶች.fds[fd].የተጠቀሙት {
			መዝጊያሂደቶችfd(ሂደቶች, fd)
		}
	}
}

func discardሂደቶች(pid uint32) {
	ሂደቶች := መፈለጊያሂደቶች(pid)
	if ሂደቶች == nil {
		return
	}
	መዝጊያሁሉንምሂደቶችfds(ሂደቶች)
	*ሂደቶች = ሂደቶችentry{}
}

func ኮፒመተላለፊያ(መተላለፊያaddress uint32) (uint32, [12]byte) {
	var ስም [12]byte
	if መተላለፊያaddress == 0 {
		return 0, ስም
	}
	raw := Getባይትስfromጠቋሚ(uintptr(መተላለፊያaddress), 64, 64)
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
		ስም[n] = c
		n++
	}
	return n, ስም
}

func ፋይልመጠን(የፋይልስም []byte) uint32 {
	var ata0s = Tጠለቅቴክኖሎጂattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionሰንጠረዥ{}
	partition.Rማንበቢያpartition(&ata0s)

	bios := TBiosparameterመከልከያ32{}
	መጠን := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም)
	ata0s.Flush()
	return መጠን
}

func ማንበቢያፋይል(የፋይልስም []byte, data []byte) {
	var ata0s = Tጠለቅቴክኖሎጂattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionሰንጠረዥ{}
	partition.Rማንበቢያpartition(&ata0s)

	bios := TBiosparameterመከልከያ32{}
	bios.Rማንበቢያ(&ata0s, partition.Mbr.Primarypartition[0], የፋይልስም, data)
	ata0s.Flush()
}

func getcr3() uint32
