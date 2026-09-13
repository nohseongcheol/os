package სისტემაcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "ფაილისისტემა/msdospartition"
import . "ფაილისისტემა/fat"
import . "ფაილისისტემა/elf"
import mem "მეხსიერებაmanager"
import . "paging"
import . "პორტი"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualმეხსიერება"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysგასვლა	uint32	= 1
	Sysfork		uint32	= 2
	Sysკითხვა	uint32	= 3
	Sysჩაწერა	uint32	= 4
	Sysგახსნა	uint32	= 5
	Sysდახურვა	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysწვდომა	uint32	= 33
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
	Sysrtგასვლა	uint32	= 252

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
	maxგახსნაfiles		= 128
)

type fdentry struct {
	გამოყეებულია	bool
	აღწერილობა	int32
	fdალმები	uint32
}

type გახსნაფაილიაღწერილობა struct {
	გამოყეებულია	bool
	refs		uint32
	kind		uint32
	ალმები		uint32
	position	uint32
	ზომა		uint32
	სახელი		[12]byte
	სახელიlen	uint32
	aux		uint32
}

const (
	fdkindარა	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindconsole	uint32	= 3
	fdkindrootდასტა	uint32	= 4
	fdkindsocket	uint32	= 5

	oკითხვაonly	uint32	= 0
	oჩაწერაonly	uint32	= 1
	oკითხვაჩაწერა	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oდასტა		uint32	= 0x10000

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
	maxdatagramზომა		= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Pპორტი	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	გამოყეებულია	bool
	ზომა		uint32
	წყარო		socketaddressipv4
	data		[maxdatagramზომა]byte
}

type localdatagramsocket struct {
	გამოყეებულია	bool
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
	Dმოწყობილობა	uint32
	Ino		uint32
	Mრეჟიმი		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sზომა_2		int32
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

type პროცესიentry struct {
	გამოყეებულია	bool
	pid		uint32
	parent		uint32
	exited		bool
	სტატუსი		uint32
	პროგრამაbreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallშეცდომა(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var გახსნაფაილიცხრილი [maxგახსნაfiles]გახსნაფაილიაღწერილობა
var პროცესიცხრილი [32]პროცესიentry
var localsockets [maxsockets]localdatagramsocket
var შემდეგიephemeralპორტი uint16 = 49152

const (
	მომხმარებელიheapbase	uint32	= 0x06000000
	მომხმარებელიheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinკითხვა uint32
var stdinჩაწერა uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysგასვლა_2(ინდექსი uint32) {
	Syscall(Sysგასვლა, ინდექსი)
}

func Sysკითხვა_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysკითხვა, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysბეჭდვაstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(Sysჩაწერა, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysბეჭდვაunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysჩაწერა, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysგახსნა_2(გეზი uintptr, ალმები uint32, რეჟიმი uint32) int32 {
	return int32(Syscall(Sysგახსნა, uint32(გეზი), ალმები, რეჟიმი))
}

func Sysდახურვა_2(fd uint32) int32 {
	return int32(Syscall(Sysდახურვა, fd))
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
		return syscallშეცდომა(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initფაილიdescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysგასვლა:
		sysგასვლა(cpu.Ebx)
		return uint32(uintptr(Pointer(Sშეჩერებაcurrentthread(cpu))))
	case Sysrtგასვლა:
		sysგასვლა(cpu.Ebx)
		return uint32(uintptr(Pointer(Sშეჩერებაcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysკითხვა:
		cpu.Eax = uint32(sysკითხვა(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysჩაწერა:
		cpu.Eax = uint32(sysჩაწერა(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysგახსნა:
		cpu.Eax = uint32(sysგახსნა(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysგახსნა(cpu.Ebx, ocreate|oჩაწერაonly|otruncate, cpu.Ecx))
		return esp
	case Sysდახურვა:
		cpu.Eax = uint32(sysდახურვა(int32(cpu.Ebx)))
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
	case Sysწვდომა:
		cpu.Eax = uint32(sysწვდომა(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32ბეჭდვა(cpu.Ebx)
		return esp

	default:
		console_2.Mბეჭდვაxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32ბეჭდვა(esp)
		console_2.Mბეჭდვა(([]byte)(":"))
		console_2.MUnsignedinteger32ბეჭდვა(cpu.Eax)
		console_2.Mბეჭდვა(([]byte)(":"))
		console_2.MUnsignedinteger32ბეჭდვა(cpu.Ebx)
		console_2.Mბეჭდვა(([]byte)(":"))
		console_2.MUnsignedinteger32ბეჭდვა(cpu.Ecx)
		console_2.Mბეჭდვა(([]byte)(":"))
		console_2.MUnsignedinteger32ბეჭდვა(cpu.Edx)
		console_2.Mბეჭდვა(([]byte)("]"))
		cpu.Eax = syscallშეცდომა(Enosys)
		return esp
	}

	return esp
}

func initფაილიdescriptor() {
	for i := 0; i < maxგახსნაfiles; i++ {
		გახსნაფაილიცხრილი[i] = გახსნაფაილიაღწერილობა{}
	}
	for i := 0; i < len(პროცესიცხრილი); i++ {
		პროცესიცხრილი[i] = პროცესიentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	შემდეგიephemeralპორტი = 49152
	გახსნაფაილიცხრილი[0] = გახსნაფაილიაღწერილობა{გამოყეებულია: true, kind: fdkindstdin, ალმები: oკითხვაonly}
	გახსნაფაილიცხრილი[1] = გახსნაფაილიაღწერილობა{გამოყეებულია: true, kind: fdkindconsole, ალმები: oჩაწერაonly}
	გახსნაფაილიცხრილი[2] = გახსნაფაილიაღწერილობა{გამოყეებულია: true, kind: fdkindconsole, ალმები: oჩაწერაonly}
}

func ძიებაპროცესი(pid uint32) *პროცესიentry {
	for i := 0; i < len(პროცესიცხრილი); i++ {
		if პროცესიცხრილი[i].გამოყეებულია && პროცესიცხრილი[i].pid == pid {
			return &პროცესიცხრილი[i]
		}
	}
	return nil
}

func initializeპროცესიfds(პროცესი *პროცესიentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		პროცესი.fds[fd] = fdentry{გამოყეებულია: true, აღწერილობა: fd}
		გახსნაფაილიცხრილი[fd].refs++
	}
}

func ensurecurrentპროცესი() *პროცესიentry {
	pid := Currentpid()
	if პროცესი := ძიებაპროცესი(pid); პროცესი != nil {
		return პროცესი
	}
	for i := 0; i < len(პროცესიცხრილი); i++ {
		if !პროცესიცხრილი[i].გამოყეებულია {
			პროცესიცხრილი[i] = პროცესიentry{
				გამოყეებულია:	true,
				pid:	pid,
				parent:	Currentparentpid(),
				პროგრამაbreak:	მომხმარებელიheapbase,
			}
			initializeპროცესიfds(&პროცესიცხრილი[i])
			return &პროცესიცხრილი[i]
		}
	}
	return nil
}

func getგახსნაფაილიfor(პროცესი *პროცესიentry, fd int32) *გახსნაფაილიაღწერილობა {
	if პროცესი == nil || fd < 0 || fd >= maxfd || !პროცესი.fds[fd].გამოყეებულია {
		return nil
	}
	აღწერილობა := პროცესი.fds[fd].აღწერილობა
	if აღწერილობა < 0 || აღწერილობა >= maxგახსნაfiles || !გახსნაფაილიცხრილი[აღწერილობა].გამოყეებულია {
		return nil
	}
	return &გახსნაფაილიცხრილი[აღწერილობა]
}

func getგახსნაფაილი(fd int32) *გახსნაფაილიაღწერილობა {
	return getგახსნაფაილიfor(ensurecurrentპროცესი(), fd)
}

func allocateგახსნაფაილი() int32 {
	for i := int32(3); i < maxგახსნაfiles; i++ {
		if !გახსნაფაილიცხრილი[i].გამოყეებულია {
			გახსნაფაილიცხრილი[i] = გახსნაფაილიაღწერილობა{გამოყეებულია: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(პროცესი *პროცესიentry, აღწერილობა int32, minimum int32) int32 {
	if პროცესი == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !პროცესი.fds[fd].გამოყეებულია {
			პროცესი.fds[fd] = fdentry{გამოყეებულია: true, აღწერილობა: აღწერილობა}
			return fd
		}
	}
	return Emfile
}

func releaseგახსნაფაილი(აღწერილობა int32) {
	if აღწერილობა < 0 || აღწერილობა >= maxგახსნაfiles {
		return
	}
	entry := &გახსნაფაილიცხრილი[აღწერილობა]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && აღწერილობა > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = გახსნაფაილიაღწერილობა{}
	}
}

func დახურვაპროცესიfd(პროცესი *პროცესიentry, fd int32) int32 {
	if პროცესი == nil || getგახსნაფაილიfor(პროცესი, fd) == nil {
		return Ebadf
	}
	აღწერილობა := პროცესი.fds[fd].აღწერილობა
	პროცესი.fds[fd] = fdentry{}
	releaseგახსნაფაილი(აღწერილობა)
	return 0
}

func sysჩაწერა(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getგახსნაფაილი(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketგაგზავნაto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootდასტა {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getბაიტიfromკურსორი(uintptr(address), int(count), int(count))
	console_2.Mბეჭდვა(buffer)
	return int32(count)
}

func sysკითხვა(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getგახსნაფაილი(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return კითხვაstdin(address, count)
	}
	if entry.kind == fdkindrootდასტა {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.ზომა {
		return 0
	}
	remaining := entry.ზომა - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := Getბაიტიfromკურსორი(uintptr(address), int(count), int(count))
	return კითხვაvfsფაილი(entry, buffer, count)
}

func sysგახსნა(გეზიaddress uint32, ალმები uint32, რეჟიმი uint32) int32 {
	_ = რეჟიმი
	if გეზიaddress == 0 {
		return Efault
	}
	წვდომარეჟიმი := ალმები & 3
	if წვდომარეჟიმი == oჩაწერაonly || წვდომარეჟიმი == oკითხვაჩაწერა || (ალმები&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	პროცესი := ensurecurrentპროცესი()
	if პროცესი == nil {
		return Enfile
	}
	აღწერილობა := allocateგახსნაფაილი()
	if აღწერილობა < 0 {
		return აღწერილობა
	}
	entry := &გახსნაფაილიცხრილი[აღწერილობა]
	entry.ალმები = ალმები
	if isrootგეზი(გეზიaddress) {
		entry.kind = fdkindrootდასტა
		entry.ზომა = 0
	} else {
		სახელიlen, სახელი := დააკოპირეგეზი(გეზიaddress)
		if სახელიlen == 0 {
			*entry = გახსნაფაილიაღწერილობა{}
			return Enoent
		}
		ზომა := ფაილიზომა(სახელი[:სახელიlen])
		if ზომა == 0 {
			*entry = გახსნაფაილიაღწერილობა{}
			return Enoent
		}
		if (ალმები & oდასტა) != 0 {
			*entry = გახსნაფაილიაღწერილობა{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.ზომა = ზომა
		entry.სახელიlen = სახელიlen
		entry.სახელი = სახელი
	}

	fd := allocatefd(პროცესი, აღწერილობა, 3)
	if fd < 0 {
		*entry = გახსნაფაილიაღწერილობა{}
		return fd
	}
	return fd
}

func sysდახურვა(fd int32) int32 {
	return დახურვაპროცესიfd(ensurecurrentპროცესი(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	პროცესი := ensurecurrentპროცესი()
	entry := getგახსნაფაილიfor(პროცესი, fd)
	if entry == nil {
		return Ebadf
	}
	ახალიfd := allocatefd(პროცესი, პროცესი.fds[fd].აღწერილობა, minimum)
	if ახალიfd >= 0 {
		entry.refs++
	}
	return ახალიfd
}

func sysdup2(oldfd int32, ახალიfd int32) int32 {
	პროცესი := ensurecurrentპროცესი()
	entry := getგახსნაფაილიfor(პროცესი, oldfd)
	if entry == nil {
		return Ebadf
	}
	if ახალიfd < 0 || ახალიfd >= maxfd {
		return Ebadf
	}
	if oldfd == ახალიfd {
		return ახალიfd
	}
	if პროცესი.fds[ახალიfd].გამოყეებულია {
		დახურვაპროცესიfd(პროცესი, ახალიfd)
	}
	პროცესი.fds[ახალიfd] = fdentry{გამოყეებულია: true, აღწერილობა: პროცესი.fds[oldfd].აღწერილობა}
	entry.refs++
	return ახალიfd
}

func sysfcntl(fd int32, ბრძანება uint32, argument uint32) int32 {
	პროცესი := ensurecurrentპროცესი()
	entry := getგახსნაფაილიfor(პროცესი, fd)
	if entry == nil {
		return Ebadf
	}
	switch ბრძანება {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(პროცესი.fds[fd].fdალმები)
	case fsetfd:
		პროცესი.fds[fd].fdალმები = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.ალმები)
	case fsetfl:
		entry.ალმები = (entry.ალმები & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getგახსნაფაილი(fd)
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
		base = int64(entry.ზომა)
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

func კითხვაvfsფაილი(entry *გახსნაფაილიაღწერილობა, destination_2 []byte, count uint32) int32 {
	მეხსიერებაmanager := &mem.Tმეხსიერებაmanager{}
	tmpკურსორი := მეხსიერებაmanager.Malloc(entry.ზომა)
	if tmpკურსორი == nil {
		return Einval
	}
	tmp := Getბაიტიfromკურსორი(uintptr(tmpკურსორი), int(entry.ზომა), int(entry.ზომა))
	კითხვაფაილი(entry.სახელი[:entry.სახელიlen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	მეხსიერებაmanager.Fთავისუფალი(tmpკურსორი)
	return int32(count)
}

func isrootგეზი(გეზიaddress uint32) bool {
	if გეზიaddress == 0 {
		return false
	}
	გეზი := Getბაიტიfromკურსორი(uintptr(გეზიaddress), 4, 4)
	if გეზი[0] == '/' && გეზი[1] == 0 {
		return true
	}
	if გეზი[0] == '.' && გეზი[1] == 0 {
		return true
	}
	if გეზი[0] == '/' && გეზი[1] == '.' && გეზი[2] == 0 {
		return true
	}
	return false
}

func sysწვდომა(გეზიaddress uint32, რეჟიმი uint32) int32 {
	if გეზიaddress == 0 {
		return Efault
	}
	if (რეჟიმი & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootგეზი(გეზიaddress)
	exists := isroot
	if !exists {
		სახელიlen, სახელი := დააკოპირეგეზი(გეზიaddress)
		exists = სახელიlen != 0 && ფაილიზომა(სახელი[:სახელიlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (რეჟიმი & 2) != 0 {
		return Eacces
	}

	if (რეჟიმი&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(გეზიaddress uint32) int32 {
	if გეზიaddress == 0 {
		return Efault
	}
	if !isrootგეზი(გეზიaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, ზომა uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if ზომა < 2 {
		return Erange
	}
	buffer_2 := Getბაიტიfromკურსორი(uintptr(bufferaddress), int(ზომა), int(ზომა))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, რეჟიმი uint32, ზომა uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dმოწყობილობა = 1
	stat.Ino = inode
	stat.Mრეჟიმი = რეჟიმი
	stat.Nlink = 1
	stat.Sზომა_2 = int32(ზომა)
	stat.Blksize = 512
	stat.Block = int32((ზომა + 511) / 512)
	return 0
}

func sysstat(გეზიaddress uint32, stataddress uint32) int32 {
	if გეზიaddress == 0 {
		return Efault
	}
	if isrootგეზი(გეზიaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	სახელიlen, სახელი := დააკოპირეგეზი(გეზიaddress)
	if სახელიlen == 0 {
		return Enoent
	}
	ზომა := ფაილიზომა(სახელი[:სახელიlen])
	if ზომა == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < სახელიlen; i++ {
		inode = inode*33 + uint32(სახელი[i])
	}
	return fillposixstat(stataddress, sifreg|0444, ზომა, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getგახსნაფაილი(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootდასტა:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.ზომა, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getგახსნაფაილი(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	პროცესი := ensurecurrentპროცესი()
	if პროცესი == nil {
		return 0
	}
	if პროცესი.პროგრამაbreak == 0 {
		პროცესი.პროგრამაbreak = მომხმარებელიheapbase
	}
	if address_2 == 0 {
		return პროცესი.პროგრამაbreak
	}
	if address_2 < მომხმარებელიheapbase || address_2 > მომხმარებელიheaplimit {
		return პროცესი.პროგრამაbreak
	}
	პროცესი.პროგრამაbreak = address_2
	return პროცესი.პროგრამაbreak
}

func დააკოპირეutsfield(destination *[65]byte, მნიშვნელობა string) {
	limit := len(მნიშვნელობა)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = მნიშვნელობა[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	სახელი := (*posixutsname)(Pointer(uintptr(address_2)))
	*სახელი = posixutsname{}
	დააკოპირეutsfield(&სახელი.Sysname, "EngOS")
	დააკოპირეutsfield(&სახელი.Nodename, "engos")
	დააკოპირეutsfield(&სახელი.Release, "0.1-posix")
	დააკოპირეutsfield(&სახელი.Version, "POSIX.1-2017 phase 1")
	დააკოპირეutsfield(&სახელი.Machine, "i386")
	return 0
}

func swapunsignedinteger16(მნიშვნელობა uint16) uint16 {
	return (მნიშვნელობა << 8) | (მნიშვნელობა >> 8)
}

func socketcallargument(arguments_2 uint32, ინდექსი uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + ინდექსი*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getგახსნაფაილი(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.გამოყეებულია {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketტიპი uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketტიპი != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	პროცესი := ensurecurrentპროცესი()
	if პროცესი == nil {
		return Enfile
	}
	socketინდექსი := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].გამოყეებულია {
			socketინდექსი = i
			break
		}
	}
	if socketინდექსი < 0 {
		return Enfile
	}
	აღწერილობა := allocateგახსნაფაილი()
	if აღწერილობა < 0 {
		return აღწერილობა
	}
	localsockets[socketინდექსი] = localdatagramsocket{გამოყეებულია: true}
	entry := &გახსნაფაილიცხრილი[აღწერილობა]
	entry.kind = fdkindsocket
	entry.ალმები = oკითხვაჩაწერა
	entry.aux = uint32(socketინდექსი)
	fd := allocatefd(პროცესი, აღწერილობა, 3)
	if fd < 0 {
		localsockets[socketინდექსი] = localdatagramsocket{}
		*entry = გახსნაფაილიაღწერილობა{}
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

func პორტიგადიდებაuse(პორტი uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.გამოყეებულია && socket.bound && socket.local.Pპორტი == პორტი {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		პორტი := swapunsignedinteger16(შემდეგიephemeralპორტი)
		შემდეგიephemeralპორტი++
		if შემდეგიephemeralპორტი < 49152 {
			შემდეგიephemeralპორტი = 49152
		}
		if !პორტიგადიდებაuse(პორტი, socket) {
			socket.local = socketaddressipv4{Family: afinet, Pპორტი: პორტი, Address: 0x0100007F}
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
	if requested.Pპორტი == 0 {
		return bindephemeral(socket)
	}
	if პორტიგადიდებაuse(requested.Pპორტი, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketდაკავშირება(fd int32, address_2 uint32, length uint32) int32 {
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

func socketგაგზავნაto(fd int32, bufferaddress_2 uint32, length uint32, destinationaddress uint32, destinationlength uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if length > maxdatagramზომა {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressშეცდომა := socketaddress(destinationaddress, destinationlength)
		if addressშეცდომა != 0 {
			return addressშეცდომა
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindშეცდომა := bindephemeral(socket); bindშეცდომა != 0 {
			return bindშეცდომა
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.გამოყეებულია && candidate.bound && candidate.local.Pპორტი == destination.Pპორტი &&
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
	*packet = socketpacket{გამოყეებულია: true, ზომა: length, წყარო: socket.local}
	if length != 0 {
		წყარო := Getბაიტიfromკურსორი(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], წყარო)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, წყაროaddress uint32, წყაროlengthaddress uint32) int32 {
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
	დააკოპირეlength := packet.ზომა
	if დააკოპირეlength > length {
		დააკოპირეlength = length
	}
	if დააკოპირეlength != 0 {
		destination := Getბაიტიfromკურსორი(uintptr(bufferaddress_2), int(დააკოპირეlength), int(დააკოპირეlength))
		copy(destination, packet.data[:დააკოპირეlength])
	}
	if წყაროaddress != 0 {
		if წყაროlengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(წყაროlengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(წყაროaddress))) = packet.წყარო
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(დააკოპირეlength)
}

func დააკოპირეsocketსახელი(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
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
			if bindშეცდომა := bindephemeral(socket); bindშეცდომა != 0 {
				return bindშეცდომა
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
		return socketდაკავშირება(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return დააკოპირეsocketსახელი(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return დააკოპირეsocketსახელი(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
	case 9:
		return socketგაგზავნაto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return socketგაგზავნაto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
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

func კითხვაstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getბაიტიfromკურსორი(uintptr(address), int(count), int(count))
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
	შემდეგი := (stdinჩაწერა + 1) % uint32(len(stdinbuffer))
	if შემდეგი == stdinკითხვა {
		return
	}
	stdinbuffer[stdinჩაწერა] = c
	stdinჩაწერა = შემდეგი
}

func stdingetblocking() byte {
	for stdinკითხვა == stdinჩაწერა {
		sc := pollკლავიატურაscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinკითხვა]
	stdinკითხვა = (stdinკითხვა + 1) % uint32(len(stdinbuffer))
	return c
}

func pollკლავიატურაscancode() byte {
	for (Pპორტიკითხვაbyte(0x64) & 0x01) == 0 {
	}
	sc := Pპორტიკითხვაbyte(0x60)
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

func დააკოპირეexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for ინდექსი := uint32(0); ინდექსი < maxexecvectorentry; ინდექსი++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + ინდექსი*4)))
		if stringaddress == 0 {
			result.count = ინდექსი
			return 0
		}
		terminated := false
		for length := uint32(0); length <= maxexecstringlength; length++ {
			მნიშვნელობა := *(*byte)(Pointer(uintptr(stringaddress + length)))
			result.values[ინდექსი][length] = მნიშვნელობა
			if მნიშვნელობა == 0 {
				result.lengths[ინდექსი] = length
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

func pushexecunsignedinteger32(stack *uint32, მნიშვნელობა uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = მნიშვნელობა
}

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackბაიტი uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Uმომხმარებელიstackზემოთ-stackბაიტი, stackბაიტი) {
		return Enomem
	}
	stack := Uმომხმარებელიstackზემოთ
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := Getბაიტიfromკურსორი(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := Getბაიტიfromკურსორი(uintptr(stack), int(length), int(length))
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

func დახურვაonexec(პროცესი *პროცესიentry) {
	if პროცესი == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if პროცესი.fds[fd].გამოყეებულია && (პროცესი.fds[fd].fdალმები&fdcloexec) != 0 {
			დახურვაპროცესიfd(პროცესი, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, გეზიaddress uint32) int32 {
	if გეზიaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := დააკოპირეexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := დააკოპირეexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	სახელიlen, სახელი := დააკოპირეგეზი(გეზიaddress)
	if სახელიlen == 0 {
		return Enoent
	}
	ზომა := ფაილიზომა(სახელი[:სახელიlen])
	if ზომა == 0 {
		return Enoent
	}
	მეხსიერებაmanager := &mem.Tმეხსიერებაmanager{}
	ფაილიკურსორი := მეხსიერებაmanager.Malloc(ზომა)
	if ფაილიკურსორი == nil {
		return Einval
	}
	data := Getბაიტიfromკურსორი(uintptr(ფაილიკურსორი), int(ზომა), int(ზომა))
	კითხვაფაილი(სახელი[:სახელიlen], data)
	if ზომა < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		მეხსიერებაmanager.Fთავისუფალი(ფაილიკურსორი)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	მეხსიერებაmanager.Fთავისუფალი(ფაილიკურსორი)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	დახურვაonexec(ensurecurrentპროცესი())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
	parentpid := Currentpid()
	if ensurecurrentპროცესი() == nil {
		return Enfile
	}
	pid := allocateპროცესი(parentpid)
	if pid == 0 {
		return Einval
	}
	მეხსიერებაmanager := &mem.Tმეხსიერებაmanager{}
	threadკურსორი := მეხსიერებაmanager.Malloc(uint32(Sizeof(TThread{})))
	stackკურსორი := მეხსიერებაmanager.Malloc(Threadstackზომა)
	childგვერდიდასტა := Cloneaddressspacecow(getcr3())
	if threadკურსორი == nil || stackკურსორი == nil || childგვერდიდასტა == 0 {
		discardპროცესი(pid)
		return Einval
	}
	child := (*TThread)(threadკურსორი)
	child.Stack = uint32(uintptr(stackკურსორი))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackკურსორი) + Threadstackზომა - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Uმომხმარებელიstack_2 = cpu.Esp
	child.Uმომხმარებელიstackზომა_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pგვერდიდასტაentry = childგვერდიდასტა
	child.Threadstate = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Aდამატებაrunnablethread(child)
	return int32(pid)
}

func sysგასვლა(სტატუსი uint32) {
	pid := Currentpid()
	for i := 0; i < len(პროცესიცხრილი); i++ {
		if პროცესიცხრილი[i].გამოყეებულია && პროცესიცხრილი[i].pid == pid {
			დახურვაყველაპროცესიfds(&პროცესიცხრილი[i])
			პროცესიცხრილი[i].exited = true
			პროცესიცხრილი[i].სტატუსი = (სტატუსი & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, სტატუსიaddress uint32, ოფციები uint32) int32 {
	if (ოფციები & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(პროცესიცხრილი); i++ {
		p := &პროცესიცხრილი[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.გამოყეებულია && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if სტატუსიaddress != 0 {
					*(*uint32)(Pointer(uintptr(სტატუსიaddress))) = p.სტატუსი
				}
				childpid := p.pid
				*p = პროცესიentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (ოფციები & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateპროცესი(parent uint32) uint32 {
	parentპროცესი := ძიებაპროცესი(parent)
	pid := Allocatepid()
	for i := 0; i < len(პროცესიცხრილი); i++ {
		if !პროცესიცხრილი[i].გამოყეებულია {
			პროცესიცხრილი[i] = პროცესიentry{
				გამოყეებულია:	true,
				pid:	pid,
				parent:	parent,
				პროგრამაbreak:	მომხმარებელიheapbase,
			}
			if parentპროცესი != nil {
				პროცესიცხრილი[i].პროგრამაbreak = parentპროცესი.პროგრამაbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentპროცესი.fds[fd].გამოყეებულია {
						პროცესიცხრილი[i].fds[fd] = parentპროცესი.fds[fd]
						აღწერილობა := parentპროცესი.fds[fd].აღწერილობა
						if აღწერილობა >= 0 && აღწერილობა < maxგახსნაfiles {
							გახსნაფაილიცხრილი[აღწერილობა].refs++
						}
					}
				}
			} else {
				initializeპროცესიfds(&პროცესიცხრილი[i])
			}
			return pid
		}
	}
	return 0
}

func დახურვაყველაპროცესიfds(პროცესი *პროცესიentry) {
	if პროცესი == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if პროცესი.fds[fd].გამოყეებულია {
			დახურვაპროცესიfd(პროცესი, fd)
		}
	}
}

func discardპროცესი(pid uint32) {
	პროცესი := ძიებაპროცესი(pid)
	if პროცესი == nil {
		return
	}
	დახურვაყველაპროცესიfds(პროცესი)
	*პროცესი = პროცესიentry{}
}

func დააკოპირეგეზი(გეზიaddress uint32) (uint32, [12]byte) {
	var სახელი [12]byte
	if გეზიaddress == 0 {
		return 0, სახელი
	}
	raw := Getბაიტიfromკურსორი(uintptr(გეზიaddress), 64, 64)
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
		სახელი[n] = c
		n++
	}
	return n, სახელი
}

func ფაილიზომა(ფაილისსახელი []byte) uint32 {
	var ata0s = Tდეტალურიtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionცხრილი{}
	partition.Rკითხვაpartition(&ata0s)

	bios := TBiosparameterblock32{}
	ზომა := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი)
	ata0s.Flush()
	return ზომა
}

func კითხვაფაილი(ფაილისსახელი []byte, data []byte) {
	var ata0s = Tდეტალურიtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionცხრილი{}
	partition.Rკითხვაpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Rკითხვა(&ata0s, partition.Mbr.Primarypartition[0], ფაილისსახელი, data)
	ata0s.Flush()
}

func getcr3() uint32
