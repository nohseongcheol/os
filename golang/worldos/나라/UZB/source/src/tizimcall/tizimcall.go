/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tizimcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "faylTizim/msdospartition"
import . "faylTizim/fat"
import . "faylTizim/elf"
import mem "xotiramanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualXotira"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	SysOʻqish	uint32	= 3
	SysYozish	uint32	= 4
	SysOchish	uint32	= 5
	SysYopish	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysruxsat	uint32	= 33
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
	maxOchishfiles		= 128
)

type fdentry struct {
	ishlatilgan	bool
	taʼrifi		int32
	fdBayroqlar	uint32
}

type ochishFaylTaʼrifi struct {
	ishlatilgan	bool
	refs		uint32
	kind		uint32
	bayroqlar	uint32
	holati		uint32
	hajmi		uint32
	nomi		[12]byte
	nomilen		uint32
	aux		uint32
}

const (
	fdkindYoq	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindconsole	uint32	= 3
	fdkindrootJild	uint32	= 4
	fdkindsocket	uint32	= 5

	oOʻqishonly	uint32	= 0
	oYozishonly	uint32	= 1
	oOʻqishYozish	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oJild		uint32	= 0x10000

	seekset		uint32	= 0
	seekcurrent	uint32	= 1
	seekOxirga	uint32	= 2

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
	maxdatagramHajmi	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	ishlatilgan	bool
	hajmi		uint32
	source		socketaddressipv4
	data		[maxdatagramHajmi]byte
}

type mahalliydatagramsocket struct {
	ishlatilgan	bool
	bound		bool
	connected	bool
	mahalliy	socketaddressipv4
	remote		socketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Uskuna		uint32
	Ino		uint32
	Rejim		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Hajmi_2		int32
	Blksize		int32
	Blok		int32
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
	maxBajarishvectorentry		= 16
	maxBajarishstringUzunlik	= 63
)

type bajarishvector struct {
	count	uint32
	lengths	[maxBajarishvectorentry]uint32
	values	[maxBajarishvectorentry][maxBajarishstringUzunlik + 1]byte
}

type jarayonentry struct {
	ishlatilgan	bool
	pid		uint32
	parent		uint32
	exited		bool
	holat		uint32
	dasturbreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallXato(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var ochishFayltable [maxOchishfiles]ochishFaylTaʼrifi
var jarayontable [32]jarayonentry
var mahalliysockets [maxsockets]mahalliydatagramsocket
var keyingiephemeralport uint16 = 49152

const (
	foydalanuvchiheapbase	uint32	= 0x06000000
	foydalanuvchiheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinOʻqish uint32
var stdinYozish uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func SysOʻqish_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysOʻqish, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysChopetishstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(SysYozish, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysChopetishunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysYozish, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOchish_2(path uintptr, bayroqlar uint32, rejim uint32) int32 {
	return int32(Syscall(SysOchish, uint32(path), bayroqlar, rejim))
}

func SysYopish_2(fd uint32) int32 {
	return int32(Syscall(SysYopish, fd))
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
		return syscallXato(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initFayldescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Toʻxtatishcurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Toʻxtatishcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysOʻqish:
		cpu.Eax = uint32(sysOʻqish(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysYozish:
		cpu.Eax = uint32(sysYozish(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysOchish:
		cpu.Eax = uint32(sysOchish(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysOchish(cpu.Ebx, ocreate|oYozishonly|otruncate, cpu.Ecx))
		return esp
	case SysYopish:
		cpu.Eax = uint32(sysYopish(int32(cpu.Ebx)))
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
	case Sysruxsat:
		cpu.Eax = uint32(sysruxsat(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Chopetish(cpu.Ebx)
		return esp

	default:
		console_2.MChopetishxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Chopetish(esp)
		console_2.MChopetish(([]byte)(":"))
		console_2.MUnsignedinteger32Chopetish(cpu.Eax)
		console_2.MChopetish(([]byte)(":"))
		console_2.MUnsignedinteger32Chopetish(cpu.Ebx)
		console_2.MChopetish(([]byte)(":"))
		console_2.MUnsignedinteger32Chopetish(cpu.Ecx)
		console_2.MChopetish(([]byte)(":"))
		console_2.MUnsignedinteger32Chopetish(cpu.Edx)
		console_2.MChopetish(([]byte)("]"))
		cpu.Eax = syscallXato(Enosys)
		return esp
	}

	return esp
}

func initFayldescriptor() {
	for i := 0; i < maxOchishfiles; i++ {
		ochishFayltable[i] = ochishFaylTaʼrifi{}
	}
	for i := 0; i < len(jarayontable); i++ {
		jarayontable[i] = jarayonentry{}
	}
	for i := 0; i < len(mahalliysockets); i++ {
		mahalliysockets[i] = mahalliydatagramsocket{}
	}
	keyingiephemeralport = 49152
	ochishFayltable[0] = ochishFaylTaʼrifi{ishlatilgan: true, kind: fdkindstdin, bayroqlar: oOʻqishonly}
	ochishFayltable[1] = ochishFaylTaʼrifi{ishlatilgan: true, kind: fdkindconsole, bayroqlar: oYozishonly}
	ochishFayltable[2] = ochishFaylTaʼrifi{ishlatilgan: true, kind: fdkindconsole, bayroqlar: oYozishonly}
}

func topishJarayon(pid uint32) *jarayonentry {
	for i := 0; i < len(jarayontable); i++ {
		if jarayontable[i].ishlatilgan && jarayontable[i].pid == pid {
			return &jarayontable[i]
		}
	}
	return nil
}

func initializeJarayonfds(jarayon *jarayonentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		jarayon.fds[fd] = fdentry{ishlatilgan: true, taʼrifi: fd}
		ochishFayltable[fd].refs++
	}
}

func ensurecurrentJarayon() *jarayonentry {
	pid := Currentpid()
	if jarayon := topishJarayon(pid); jarayon != nil {
		return jarayon
	}
	for i := 0; i < len(jarayontable); i++ {
		if !jarayontable[i].ishlatilgan {
			jarayontable[i] = jarayonentry{
				ishlatilgan:	true,
				pid:		pid,
				parent:		Currentparentpid(),
				dasturbreak:	foydalanuvchiheapbase,
			}
			initializeJarayonfds(&jarayontable[i])
			return &jarayontable[i]
		}
	}
	return nil
}

func getOchishFaylfor(jarayon *jarayonentry, fd int32) *ochishFaylTaʼrifi {
	if jarayon == nil || fd < 0 || fd >= maxfd || !jarayon.fds[fd].ishlatilgan {
		return nil
	}
	taʼrifi := jarayon.fds[fd].taʼrifi
	if taʼrifi < 0 || taʼrifi >= maxOchishfiles || !ochishFayltable[taʼrifi].ishlatilgan {
		return nil
	}
	return &ochishFayltable[taʼrifi]
}

func getOchishFayl(fd int32) *ochishFaylTaʼrifi {
	return getOchishFaylfor(ensurecurrentJarayon(), fd)
}

func allocateOchishFayl() int32 {
	for i := int32(3); i < maxOchishfiles; i++ {
		if !ochishFayltable[i].ishlatilgan {
			ochishFayltable[i] = ochishFaylTaʼrifi{ishlatilgan: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(jarayon *jarayonentry, taʼrifi int32, minimum int32) int32 {
	if jarayon == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !jarayon.fds[fd].ishlatilgan {
			jarayon.fds[fd] = fdentry{ishlatilgan: true, taʼrifi: taʼrifi}
			return fd
		}
	}
	return Emfile
}

func releaseOchishFayl(taʼrifi int32) {
	if taʼrifi < 0 || taʼrifi >= maxOchishfiles {
		return
	}
	entry := &ochishFayltable[taʼrifi]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && taʼrifi > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			mahalliysockets[entry.aux] = mahalliydatagramsocket{}
		}
		*entry = ochishFaylTaʼrifi{}
	}
}

func yopishJarayonfd(jarayon *jarayonentry, fd int32) int32 {
	if jarayon == nil || getOchishFaylfor(jarayon, fd) == nil {
		return Ebadf
	}
	taʼrifi := jarayon.fds[fd].taʼrifi
	jarayon.fds[fd] = fdentry{}
	releaseOchishFayl(taʼrifi)
	return 0
}

func sysYozish(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getOchishFayl(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketJoʻnatishto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootJild {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBaytlarfromKorsatgich(uintptr(address), int(count), int(count))
	console_2.MChopetish(buffer)
	return int32(count)
}

func sysOʻqish(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getOchishFayl(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return oʻqishstdin(address, count)
	}
	if entry.kind == fdkindrootJild {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.holati >= entry.hajmi {
		return 0
	}
	remaining := entry.hajmi - entry.holati
	if count > remaining {
		count = remaining
	}
	buffer := GetBaytlarfromKorsatgich(uintptr(address), int(count), int(count))
	return oʻqishvfsFayl(entry, buffer, count)
}

func sysOchish(pathaddress uint32, bayroqlar uint32, rejim uint32) int32 {
	_ = rejim
	if pathaddress == 0 {
		return Efault
	}
	ruxsatRejim := bayroqlar & 3
	if ruxsatRejim == oYozishonly || ruxsatRejim == oOʻqishYozish || (bayroqlar&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	jarayon := ensurecurrentJarayon()
	if jarayon == nil {
		return Enfile
	}
	taʼrifi := allocateOchishFayl()
	if taʼrifi < 0 {
		return taʼrifi
	}
	entry := &ochishFayltable[taʼrifi]
	entry.bayroqlar = bayroqlar
	if isrootpath(pathaddress) {
		entry.kind = fdkindrootJild
		entry.hajmi = 0
	} else {
		nomilen, nomi := nusxaolishpath(pathaddress)
		if nomilen == 0 {
			*entry = ochishFaylTaʼrifi{}
			return Enoent
		}
		hajmi := faylHajmi(nomi[:nomilen])
		if hajmi == 0 {
			*entry = ochishFaylTaʼrifi{}
			return Enoent
		}
		if (bayroqlar & oJild) != 0 {
			*entry = ochishFaylTaʼrifi{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.hajmi = hajmi
		entry.nomilen = nomilen
		entry.nomi = nomi
	}

	fd := allocatefd(jarayon, taʼrifi, 3)
	if fd < 0 {
		*entry = ochishFaylTaʼrifi{}
		return fd
	}
	return fd
}

func sysYopish(fd int32) int32 {
	return yopishJarayonfd(ensurecurrentJarayon(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	jarayon := ensurecurrentJarayon()
	entry := getOchishFaylfor(jarayon, fd)
	if entry == nil {
		return Ebadf
	}
	yangifd := allocatefd(jarayon, jarayon.fds[fd].taʼrifi, minimum)
	if yangifd >= 0 {
		entry.refs++
	}
	return yangifd
}

func sysdup2(oldfd int32, yangifd int32) int32 {
	jarayon := ensurecurrentJarayon()
	entry := getOchishFaylfor(jarayon, oldfd)
	if entry == nil {
		return Ebadf
	}
	if yangifd < 0 || yangifd >= maxfd {
		return Ebadf
	}
	if oldfd == yangifd {
		return yangifd
	}
	if jarayon.fds[yangifd].ishlatilgan {
		yopishJarayonfd(jarayon, yangifd)
	}
	jarayon.fds[yangifd] = fdentry{ishlatilgan: true, taʼrifi: jarayon.fds[oldfd].taʼrifi}
	entry.refs++
	return yangifd
}

func sysfcntl(fd int32, buyruq uint32, argument uint32) int32 {
	jarayon := ensurecurrentJarayon()
	entry := getOchishFaylfor(jarayon, fd)
	if entry == nil {
		return Ebadf
	}
	switch buyruq {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(jarayon.fds[fd].fdBayroqlar)
	case fsetfd:
		jarayon.fds[fd].fdBayroqlar = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.bayroqlar)
	case fsetfl:
		entry.bayroqlar = (entry.bayroqlar & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getOchishFayl(fd)
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
		base = int64(entry.holati)
	case seekOxirga:
		base = int64(entry.hajmi)
	default:
		return Einval
	}
	holati_2 := base + int64(offset)
	if holati_2 < 0 || holati_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.holati = uint32(holati_2)
	return int32(entry.holati)
}

func oʻqishvfsFayl(entry *ochishFaylTaʼrifi, destination_2 []byte, count uint32) int32 {
	xotiramanager := &mem.TXotiramanager{}
	tmpKorsatgich := xotiramanager.Malloc(entry.hajmi)
	if tmpKorsatgich == nil {
		return Einval
	}
	tmp := GetBaytlarfromKorsatgich(uintptr(tmpKorsatgich), int(entry.hajmi), int(entry.hajmi))
	oʻqishFayl(entry.nomi[:entry.nomilen], tmp)
	copy(destination_2[:count], tmp[entry.holati:entry.holati+count])
	entry.holati += count
	xotiramanager.Bosh(tmpKorsatgich)
	return int32(count)
}

func isrootpath(pathaddress uint32) bool {
	if pathaddress == 0 {
		return false
	}
	path := GetBaytlarfromKorsatgich(uintptr(pathaddress), 4, 4)
	if path[0] == '/' && path[1] == 0 {
		return true
	}
	if path[0] == '.' && path[1] == 0 {
		return true
	}
	if path[0] == '/' && path[1] == '.' && path[2] == 0 {
		return true
	}
	return false
}

func sysruxsat(pathaddress uint32, rejim uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if (rejim & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootpath(pathaddress)
	exists := isroot
	if !exists {
		nomilen, nomi := nusxaolishpath(pathaddress)
		exists = nomilen != 0 && faylHajmi(nomi[:nomilen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (rejim & 2) != 0 {
		return Eacces
	}

	if (rejim&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(pathaddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if !isrootpath(pathaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, hajmi uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if hajmi < 2 {
		return Erange
	}
	buffer_2 := GetBaytlarfromKorsatgich(uintptr(bufferaddress), int(hajmi), int(hajmi))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, rejim uint32, hajmi uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Uskuna = 1
	stat.Ino = inode
	stat.Rejim = rejim
	stat.Nlink = 1
	stat.Hajmi_2 = int32(hajmi)
	stat.Blksize = 512
	stat.Blok = int32((hajmi + 511) / 512)
	return 0
}

func sysstat(pathaddress uint32, stataddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if isrootpath(pathaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nomilen, nomi := nusxaolishpath(pathaddress)
	if nomilen == 0 {
		return Enoent
	}
	hajmi := faylHajmi(nomi[:nomilen])
	if hajmi == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nomilen; i++ {
		inode = inode*33 + uint32(nomi[i])
	}
	return fillposixstat(stataddress, sifreg|0444, hajmi, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getOchishFayl(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootJild:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.hajmi, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOchishFayl(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	jarayon := ensurecurrentJarayon()
	if jarayon == nil {
		return 0
	}
	if jarayon.dasturbreak == 0 {
		jarayon.dasturbreak = foydalanuvchiheapbase
	}
	if address_2 == 0 {
		return jarayon.dasturbreak
	}
	if address_2 < foydalanuvchiheapbase || address_2 > foydalanuvchiheaplimit {
		return jarayon.dasturbreak
	}
	jarayon.dasturbreak = address_2
	return jarayon.dasturbreak
}

func nusxaolishutsfield(destination *[65]byte, qiymat string) {
	limit := len(qiymat)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = qiymat[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nomi := (*posixutsname)(Pointer(uintptr(address_2)))
	*nomi = posixutsname{}
	nusxaolishutsfield(&nomi.Sysname, "EngOS")
	nusxaolishutsfield(&nomi.Nodename, "engos")
	nusxaolishutsfield(&nomi.Release, "0.1-posix")
	nusxaolishutsfield(&nomi.Version, "POSIX.1-2017 phase 1")
	nusxaolishutsfield(&nomi.Machine, "i386")
	return 0
}

func swapunsignedinteger16(qiymat uint16) uint16 {
	return (qiymat << 8) | (qiymat >> 8)
}

func socketcallargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func socketforfd(fd int32) (*mahalliydatagramsocket, int32) {
	entry := getOchishFayl(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &mahalliysockets[entry.aux]
	if !socket.ishlatilgan {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domen uint32, socketTuri uint32, protocol uint32) int32 {
	if domen != afinet {
		return Eafnosupport
	}
	if socketTuri != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	jarayon := ensurecurrentJarayon()
	if jarayon == nil {
		return Enfile
	}
	socketindex := -1
	for i := 0; i < maxsockets; i++ {
		if !mahalliysockets[i].ishlatilgan {
			socketindex = i
			break
		}
	}
	if socketindex < 0 {
		return Enfile
	}
	taʼrifi := allocateOchishFayl()
	if taʼrifi < 0 {
		return taʼrifi
	}
	mahalliysockets[socketindex] = mahalliydatagramsocket{ishlatilgan: true}
	entry := &ochishFayltable[taʼrifi]
	entry.kind = fdkindsocket
	entry.bayroqlar = oOʻqishYozish
	entry.aux = uint32(socketindex)
	fd := allocatefd(jarayon, taʼrifi, 3)
	if fd < 0 {
		mahalliysockets[socketindex] = mahalliydatagramsocket{}
		*entry = ochishFaylTaʼrifi{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, uzunlik uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if uzunlik < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portYaqinlashtirishuse(port uint16, except *mahalliydatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &mahalliysockets[i]
		if socket != except && socket.ishlatilgan && socket.bound && socket.mahalliy.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(socket *mahalliydatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(keyingiephemeralport)
		keyingiephemeralport++
		if keyingiephemeralport < 49152 {
			keyingiephemeralport = 49152
		}
		if !portYaqinlashtirishuse(port, socket) {
			socket.mahalliy = socketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, uzunlik uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, uzunlik)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(socket)
	}
	if portYaqinlashtirishuse(requested.Port, socket) {
		return Eaddrinuse
	}
	socket.mahalliy = *requested
	socket.bound = true
	return 0
}

func socketUlanish(fd int32, address_2 uint32, uzunlik uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, uzunlik)
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

func socketJoʻnatishto(fd int32, bufferaddress_2 uint32, uzunlik uint32, destinationaddress uint32, destinationUzunlik uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if uzunlik > maxdatagramHajmi {
		return Emsgsize
	}
	if uzunlik != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressXato := socketaddress(destinationaddress, destinationUzunlik)
		if addressXato != 0 {
			return addressXato
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindXato := bindephemeral(socket); bindXato != 0 {
			return bindXato
		}
	}
	var receiver *mahalliydatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &mahalliysockets[i]
		if candidate.ishlatilgan && candidate.bound && candidate.mahalliy.Port == destination.Port &&
			(candidate.mahalliy.Address == 0 || candidate.mahalliy.Address == destination.Address) {
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
	*packet = socketpacket{ishlatilgan: true, hajmi: uzunlik, source: socket.mahalliy}
	if uzunlik != 0 {
		source := GetBaytlarfromKorsatgich(uintptr(bufferaddress_2), int(uzunlik), int(uzunlik))
		copy(packet.data[:uzunlik], source)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(uzunlik)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, uzunlik uint32, sourceaddress uint32, sourceUzunlikaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if uzunlik != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	nusxaolishUzunlik := packet.hajmi
	if nusxaolishUzunlik > uzunlik {
		nusxaolishUzunlik = uzunlik
	}
	if nusxaolishUzunlik != 0 {
		destination := GetBaytlarfromKorsatgich(uintptr(bufferaddress_2), int(nusxaolishUzunlik), int(nusxaolishUzunlik))
		copy(destination, packet.data[:nusxaolishUzunlik])
	}
	if sourceaddress != 0 {
		if sourceUzunlikaddress == 0 {
			return Efault
		}
		providedUzunlik := (*uint32)(Pointer(uintptr(sourceUzunlikaddress)))
		if *providedUzunlik >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(sourceaddress))) = packet.source
		}
		*providedUzunlik = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(nusxaolishUzunlik)
}

func nusxaolishsocketNomi(fd int32, address_2 uint32, uzunlikaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || uzunlikaddress == 0 {
		return Efault
	}
	uzunlik := (*uint32)(Pointer(uintptr(uzunlikaddress)))
	if *uzunlik < 16 {
		*uzunlik = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindXato := bindephemeral(socket); bindXato != 0 {
				return bindXato
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.mahalliy
	}
	*uzunlik = 16
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
		return socketUlanish(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return nusxaolishsocketNomi(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return nusxaolishsocketNomi(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
	case 9:
		return socketJoʻnatishto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return socketJoʻnatishto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
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

func oʻqishstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaytlarfromKorsatgich(uintptr(address), int(count), int(count))
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
	keyingi := (stdinYozish + 1) % uint32(len(stdinbuffer))
	if keyingi == stdinOʻqish {
		return
	}
	stdinbuffer[stdinYozish] = c
	stdinYozish = keyingi
}

func stdingetblocking() byte {
	for stdinOʻqish == stdinYozish {
		sc := pollKlaviaturascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinOʻqish]
	stdinOʻqish = (stdinOʻqish + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlaviaturascancode() byte {
	for (PortOʻqishbyte(0x64) & 0x01) == 0 {
	}
	sc := PortOʻqishbyte(0x60)
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

func nusxaolishBajarishvector(address_2 uint32, result *bajarishvector) int32 {
	*result = bajarishvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxBajarishvectorentry; index++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if stringaddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for uzunlik := uint32(0); uzunlik <= maxBajarishstringUzunlik; uzunlik++ {
			qiymat := *(*byte)(Pointer(uintptr(stringaddress + uzunlik)))
			result.values[index][uzunlik] = qiymat
			if qiymat == 0 {
				result.lengths[index] = uzunlik
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

func pushBajarishunsignedinteger32(stack *uint32, qiymat uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = qiymat
}

func setupBajarishstack(cpu *Tcpustate, arguments_2 *bajarishvector, environment *bajarishvector) int32 {
	const stackBaytlar uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), FoydalanuvchistackYuqori-stackBaytlar, stackBaytlar) {
		return Enomem
	}
	stack := FoydalanuvchistackYuqori
	var argumentpointers [maxBajarishvectorentry]uint32
	var environmentpointers [maxBajarishvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		uzunlik := environment.lengths[i] + 1
		stack -= uzunlik
		destination := GetBaytlarfromKorsatgich(uintptr(stack), int(uzunlik), int(uzunlik))
		copy(destination, environment.values[i][:uzunlik])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		uzunlik := arguments_2.lengths[i] + 1
		stack -= uzunlik
		destination := GetBaytlarfromKorsatgich(uintptr(stack), int(uzunlik), int(uzunlik))
		copy(destination, arguments_2.values[i][:uzunlik])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushBajarishunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushBajarishunsignedinteger32(&stack, environmentpointers[i])
	}
	pushBajarishunsignedinteger32(&stack, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushBajarishunsignedinteger32(&stack, argumentpointers[i])
	}
	pushBajarishunsignedinteger32(&stack, arguments_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func yopishYoqishBajarish(jarayon *jarayonentry) {
	if jarayon == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if jarayon.fds[fd].ishlatilgan && (jarayon.fds[fd].fdBayroqlar&fdcloexec) != 0 {
			yopishJarayonfd(jarayon, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, pathaddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	var arguments_2 bajarishvector
	var environment bajarishvector
	if result := nusxaolishBajarishvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := nusxaolishBajarishvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	nomilen, nomi := nusxaolishpath(pathaddress)
	if nomilen == 0 {
		return Enoent
	}
	hajmi := faylHajmi(nomi[:nomilen])
	if hajmi == 0 {
		return Enoent
	}
	xotiramanager := &mem.TXotiramanager{}
	faylKorsatgich := xotiramanager.Malloc(hajmi)
	if faylKorsatgich == nil {
		return Einval
	}
	data := GetBaytlarfromKorsatgich(uintptr(faylKorsatgich), int(hajmi), int(hajmi))
	oʻqishFayl(nomi[:nomilen], data)
	if hajmi < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		xotiramanager.Bosh(faylKorsatgich)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	xotiramanager.Bosh(faylKorsatgich)
	if result := setupBajarishstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	yopishYoqishBajarish(ensurecurrentJarayon())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
	parentpid := Currentpid()
	if ensurecurrentJarayon() == nil {
		return Enfile
	}
	pid := allocateJarayon(parentpid)
	if pid == 0 {
		return Einval
	}
	xotiramanager := &mem.TXotiramanager{}
	threadKorsatgich := xotiramanager.Malloc(uint32(Sizeof(TThread{})))
	stackKorsatgich := xotiramanager.Malloc(ThreadstackHajmi)
	childSAHIFAJild := CloneaddressBoʻshjoycow(getcr3())
	if threadKorsatgich == nil || stackKorsatgich == nil || childSAHIFAJild == 0 {
		discardJarayon(pid)
		return Einval
	}
	child := (*TThread)(threadKorsatgich)
	child.Stack = uint32(uintptr(stackKorsatgich))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackKorsatgich) + ThreadstackHajmi - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Foydalanuvchistack_2 = cpu.Esp
	child.FoydalanuvchistackHajmi_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.SAHIFAJildentry = childSAHIFAJild
	child.Threadstate = Tayyor
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Qoʻshishrunnablethread(child)
	return int32(pid)
}

func sysexit(holat uint32) {
	pid := Currentpid()
	for i := 0; i < len(jarayontable); i++ {
		if jarayontable[i].ishlatilgan && jarayontable[i].pid == pid {
			yopishHammasiJarayonfds(&jarayontable[i])
			jarayontable[i].exited = true
			jarayontable[i].holat = (holat & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, holataddress uint32, moslamalar uint32) int32 {
	if (moslamalar & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(jarayontable); i++ {
		p := &jarayontable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.ishlatilgan && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if holataddress != 0 {
					*(*uint32)(Pointer(uintptr(holataddress))) = p.holat
				}
				childpid := p.pid
				*p = jarayonentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (moslamalar & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateJarayon(parent uint32) uint32 {
	parentJarayon := topishJarayon(parent)
	pid := Allocatepid()
	for i := 0; i < len(jarayontable); i++ {
		if !jarayontable[i].ishlatilgan {
			jarayontable[i] = jarayonentry{
				ishlatilgan:	true,
				pid:		pid,
				parent:		parent,
				dasturbreak:	foydalanuvchiheapbase,
			}
			if parentJarayon != nil {
				jarayontable[i].dasturbreak = parentJarayon.dasturbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentJarayon.fds[fd].ishlatilgan {
						jarayontable[i].fds[fd] = parentJarayon.fds[fd]
						taʼrifi := parentJarayon.fds[fd].taʼrifi
						if taʼrifi >= 0 && taʼrifi < maxOchishfiles {
							ochishFayltable[taʼrifi].refs++
						}
					}
				}
			} else {
				initializeJarayonfds(&jarayontable[i])
			}
			return pid
		}
	}
	return 0
}

func yopishHammasiJarayonfds(jarayon *jarayonentry) {
	if jarayon == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if jarayon.fds[fd].ishlatilgan {
			yopishJarayonfd(jarayon, fd)
		}
	}
}

func discardJarayon(pid uint32) {
	jarayon := topishJarayon(pid)
	if jarayon == nil {
		return
	}
	yopishHammasiJarayonfds(jarayon)
	*jarayon = jarayonentry{}
}

func nusxaolishpath(pathaddress uint32) (uint32, [12]byte) {
	var nomi [12]byte
	if pathaddress == 0 {
		return 0, nomi
	}
	raw := GetBaytlarfromKorsatgich(uintptr(pathaddress), 64, 64)
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
		nomi[n] = c
		n++
	}
	return n, nomi
}

func faylHajmi(faylnomi []byte) uint32 {
	var ata0s = TMurakkabTexnologiyaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oʻqishpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	hajmi := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faylnomi)
	ata0s.Flush()
	return hajmi
}

func oʻqishFayl(faylnomi []byte, data []byte) {
	var ata0s = TMurakkabTexnologiyaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Oʻqishpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Oʻqish(&ata0s, partition.Mbr.Primarypartition[0], faylnomi, data)
	ata0s.Flush()
}

func getcr3() uint32
