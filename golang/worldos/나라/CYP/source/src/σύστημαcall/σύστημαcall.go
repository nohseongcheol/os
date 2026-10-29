/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package σύστημαcall

import . "unsafe"

import . "διακοπή"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "αρχείοΣύστημα/msdospartition"
import . "αρχείοΣύστημα/fat"
import . "αρχείοΣύστημα/elf"
import mem "μνήμηmanager"
import . "paging"
import . "θύρα"
import . "tasking/scheduler"
import . "tasking/thread"
import . "εικονικήΜνήμη"

var console_2 = TConsole{}

type TSyscall struct {
	TΔιακοπήhandler
}

const (
	SysΈξοδος	uint32	= 1
	Sysfork		uint32	= 2
	SysΑνάγνωση	uint32	= 3
	SysΕγγραφή	uint32	= 4
	SysΆνοιγμα	uint32	= 5
	SysΚλείσιμο	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysπροσπέλαση	uint32	= 33
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
	SysrtΈξοδος	uint32	= 252

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
	μεγfd				= 32
	μεγΆνοιγμαΑΡΧΕΙΑ		= 128
)

type fdκαταχώρηση struct {
	σεχρήση		bool
	περιγραφή	int32
	fdΔιακόπτες	uint32
}

type άνοιγμαΑρχείοΠεριγραφή struct {
	σεχρήση		bool
	refs		uint32
	είδος		uint32
	διακόπτες	uint32
	θέση		uint32
	μέγεθος		uint32
	όνομα		[12]byte
	όνομαlen	uint32
	aux		uint32
}

const (
	fdΕίδοςΚανένα				uint32	= 0
	fdΕίδοςfat				uint32	= 1
	fdΕίδοςstdin				uint32	= 2
	fdΕίδοςconsole				uint32	= 3
	fdΕίδοςΡιζικόςκατάλογοςΚατάλογος	uint32	= 4
	fdΕίδοςΥποδοχή				uint32	= 5

	oΑνάγνωσηonly		uint32	= 0
	oΕγγραφήonly		uint32	= 1
	oΑνάγνωσηΕγγραφή	uint32	= 2
	ocreate			uint32	= 0x40
	oΑποκοπήψηφίων		uint32	= 0x200
	oappend			uint32	= 0x400
	oΚατάλογος		uint32	= 0x10000

	seekσύνολο	uint32	= 0
	seekΤρέχον	uint32	= 1
	seekΤέλος	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fσύνολοfd	uint32	= 2
	fgetfl		uint32	= 3
	fσύνολοfl	uint32	= 4
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
	μεγsockets		= 32
	μεγΥποδοχήπακέτα	= 8
	μεγdatagramΜέγεθος	= 512
)

type υποδοχήaddressipv4 struct {
	Family	uint16
	Θύρα	uint16
	Address	uint32
	Μηδέν	[8]byte
}

type υποδοχήpacket struct {
	σεχρήση	bool
	μέγεθος	uint32
	πηγή	υποδοχήaddressipv4
	data	[μεγdatagramΜέγεθος]byte
}

type τοπικόdatagramΥποδοχή struct {
	σεχρήση		bool
	bound		bool
	connected	bool
	τοπικό		υποδοχήaddressipv4
	απομακρυσμένο	υποδοχήaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	πακέτα		[μεγΥποδοχήπακέτα]υποδοχήpacket
}

type posixstat struct {
	Συσκευή		uint32
	Ino		uint32
	ΚΑΤΑΣΤΑΣΗ	uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Μέγεθος_2	int32
	Blksize		int32
	Μπλοκ		int32
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
	Έκδοση		[65]byte
	Machine		[65]byte
}

const (
	μεγΕκτέλεσηvectorκαταχώρηση	= 16
	μεγΕκτέλεσηΣυμβολοσειράΔιάρκεια	= 63
)

type εκτέλεσηvector struct {
	count	uint32
	lengths	[μεγΕκτέλεσηvectorκαταχώρηση]uint32
	τιμές	[μεγΕκτέλεσηvectorκαταχώρηση][μεγΕκτέλεσηΣυμβολοσειράΔιάρκεια + 1]byte
}

type διεργασίακαταχώρηση struct {
	σεχρήση		bool
	pid		uint32
	γονικό		uint32
	τερματίστηκε	bool
	κατάσταση	uint32
	πρόγραμμαbreak	uint32
	fds		[μεγfd]fdκαταχώρηση
}

type συμβολοσειράheader struct {
	Data	uintptr
	Len	int
}

func syscallΣφάλμα(σφάλλω int32) uint32 {
	return *(*uint32)(Pointer(&σφάλλω))
}

var άνοιγμαΑρχείοΠίνακας [μεγΆνοιγμαΑΡΧΕΙΑ]άνοιγμαΑρχείοΠεριγραφή
var διεργασίαΠίνακας [32]διεργασίακαταχώρηση
var τοπικόsockets [μεγsockets]τοπικόdatagramΥποδοχή
var επόμενοephemeralΘύρα uint16 = 49152

const (
	χρήστηςheapbase	uint32	= 0x06000000
	χρήστηςheapΌριο	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinΑνάγνωση uint32
var stdinΕγγραφή uint32

func Διακοπή(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysΈξοδος_2(κατάλογος uint32) {
	Syscall(SysΈξοδος, κατάλογος)
}

func SysΑνάγνωση_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysΑνάγνωση, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysΕκτύπωσηstr(buffer string) {
	h := (*συμβολοσειράheader)(Pointer(&buffer))
	Syscall(SysΕγγραφή, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysΕκτύπωσηunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysΕγγραφή, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysΆνοιγμα_2(δΙΑΔΡΟΜΗ uintptr, διακόπτες uint32, κΑΤΑΣΤΑΣΗ uint32) int32 {
	return int32(Syscall(SysΆνοιγμα, uint32(δΙΑΔΡΟΜΗ), διακόπτες, κΑΤΑΣΤΑΣΗ))
}

func SysΚλείσιμο_2(fd uint32) int32 {
	return int32(Syscall(SysΚλείσιμο, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(παράμετροι_3 ...uint32) uint32 {

	l := len(παράμετροι_3)
	switch l {
	case 1:
		return Διακοπή(παράμετροι_3[0], 0, 0, 0, 0, 0)
	case 2:
		return Διακοπή(παράμετροι_3[0], παράμετροι_3[1], 0, 0, 0, 0)
	case 3:
		return Διακοπή(παράμετροι_3[0], παράμετροι_3[1], παράμετροι_3[2], 0, 0, 0)
	case 4:
		return Διακοπή(παράμετροι_3[0], παράμετροι_3[1], παράμετροι_3[2], παράμετροι_3[3], 0, 0)
	case 5:
		return Διακοπή(παράμετροι_3[0], παράμετροι_3[1], παράμετροι_3[2], παράμετροι_3[3], παράμετροι_3[4], 0)
	case 6:
		return Διακοπή(παράμετροι_3[0], παράμετροι_3[1], παράμετροι_3[2], παράμετροι_3[3], παράμετροι_3[4], παράμετροι_3[5])
	default:
		return syscallΣφάλμα(Enosys)
	}
}

func (self *TSyscall) Init(manager *TΔιακοπήmanager) {
	initΑρχείοdescriptor()

	διακοπήhandler = χειρολαβήΔιακοπή

	var address uintptr
	address = uintptr(Pointer(&διακοπήhandler))

	self.TΔιακοπήhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var διακοπήhandler func(uint32) uint32

func χειρολαβήΔιακοπή(esp uint32) uint32 {
	var επεξεργαστής = (*TcpuΚατάσταση)(Pointer(uintptr(esp)))

	switch επεξεργαστής.Eax {
	case SysΈξοδος:
		sysΈξοδος(επεξεργαστής.Ebx)
		return uint32(uintptr(Pointer(ΔιακοπήΤρέχονthread(επεξεργαστής))))
	case SysrtΈξοδος:
		sysΈξοδος(επεξεργαστής.Ebx)
		return uint32(uintptr(Pointer(ΔιακοπήΤρέχονthread(επεξεργαστής))))
	case Sysfork:
		επεξεργαστής.Eax = uint32(sysfork(επεξεργαστής))
		return esp
	case SysΑνάγνωση:
		επεξεργαστής.Eax = uint32(sysΑνάγνωση(int32(επεξεργαστής.Ebx), επεξεργαστής.Ecx, επεξεργαστής.Edx))
		return esp
	case SysΕγγραφή:
		επεξεργαστής.Eax = uint32(sysΕγγραφή(int32(επεξεργαστής.Ebx), επεξεργαστής.Ecx, επεξεργαστής.Edx))
		return esp
	case SysΆνοιγμα:
		επεξεργαστής.Eax = uint32(sysΆνοιγμα(επεξεργαστής.Ebx, επεξεργαστής.Ecx, επεξεργαστής.Edx))
		return esp
	case Syscreat:
		επεξεργαστής.Eax = uint32(sysΆνοιγμα(επεξεργαστής.Ebx, ocreate|oΕγγραφήonly|oΑποκοπήψηφίων, επεξεργαστής.Ecx))
		return esp
	case SysΚλείσιμο:
		επεξεργαστής.Eax = uint32(sysΚλείσιμο(int32(επεξεργαστής.Ebx)))
		return esp
	case Syswaitpid:
		επεξεργαστής.Eax = uint32(syswaitpid(int32(επεξεργαστής.Ebx), επεξεργαστής.Ecx, επεξεργαστής.Edx))
		return esp
	case Syslseek:
		επεξεργαστής.Eax = uint32(syslseek(int32(επεξεργαστής.Ebx), int32(επεξεργαστής.Ecx), επεξεργαστής.Edx))
		return esp
	case Sysexecve:
		επεξεργαστής.Eax = uint32(sysexecve(επεξεργαστής, επεξεργαστής.Ebx))
		return esp
	case Sysgetpid:
		επεξεργαστής.Eax = Τρέχονpid()
		return esp
	case Sysgetppid:
		επεξεργαστής.Eax = Τρέχονγονικόpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		επεξεργαστής.Eax = 0
		return esp
	case Sysπροσπέλαση:
		επεξεργαστής.Eax = uint32(sysπροσπέλαση(επεξεργαστής.Ebx, επεξεργαστής.Ecx))
		return esp
	case Syschdir:
		επεξεργαστής.Eax = uint32(syschdir(επεξεργαστής.Ebx))
		return esp
	case Sysgetcwd:
		επεξεργαστής.Eax = uint32(sysgetcwd(επεξεργαστής.Ebx, επεξεργαστής.Ecx))
		return esp
	case Sysdup:
		επεξεργαστής.Eax = uint32(sysdup(int32(επεξεργαστής.Ebx), 0))
		return esp
	case Sysdup2:
		επεξεργαστής.Eax = uint32(sysdup2(int32(επεξεργαστής.Ebx), int32(επεξεργαστής.Ecx)))
		return esp
	case Syssocketcall:
		επεξεργαστής.Eax = uint32(sysΥποδοχήcall(επεξεργαστής.Ebx, επεξεργαστής.Ecx))
		return esp
	case Sysfcntl:
		επεξεργαστής.Eax = uint32(sysfcntl(int32(επεξεργαστής.Ebx), επεξεργαστής.Ecx, επεξεργαστής.Edx))
		return esp
	case Sysstat, Syslstat:
		επεξεργαστής.Eax = uint32(sysstat(επεξεργαστής.Ebx, επεξεργαστής.Ecx))
		return esp
	case Sysfstat:
		επεξεργαστής.Eax = uint32(sysfstat(int32(επεξεργαστής.Ebx), επεξεργαστής.Ecx))
		return esp
	case Sysfsync:
		επεξεργαστής.Eax = uint32(sysfsync(int32(επεξεργαστής.Ebx)))
		return esp
	case Syssync:
		επεξεργαστής.Eax = 0
		return esp
	case Sysuname:
		επεξεργαστής.Eax = uint32(sysuname(επεξεργαστής.Ebx))
		return esp
	case Sysbrk:
		επεξεργαστής.Eax = sysbrk(επεξεργαστής.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Εκτύπωση(επεξεργαστής.Ebx)
		return esp

	default:
		console_2.MΕκτύπωσηxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Εκτύπωση(esp)
		console_2.MΕκτύπωση(([]byte)(":"))
		console_2.MUnsignedinteger32Εκτύπωση(επεξεργαστής.Eax)
		console_2.MΕκτύπωση(([]byte)(":"))
		console_2.MUnsignedinteger32Εκτύπωση(επεξεργαστής.Ebx)
		console_2.MΕκτύπωση(([]byte)(":"))
		console_2.MUnsignedinteger32Εκτύπωση(επεξεργαστής.Ecx)
		console_2.MΕκτύπωση(([]byte)(":"))
		console_2.MUnsignedinteger32Εκτύπωση(επεξεργαστής.Edx)
		console_2.MΕκτύπωση(([]byte)("]"))
		επεξεργαστής.Eax = syscallΣφάλμα(Enosys)
		return esp
	}

	return esp
}

func initΑρχείοdescriptor() {
	for i := 0; i < μεγΆνοιγμαΑΡΧΕΙΑ; i++ {
		άνοιγμαΑρχείοΠίνακας[i] = άνοιγμαΑρχείοΠεριγραφή{}
	}
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		διεργασίαΠίνακας[i] = διεργασίακαταχώρηση{}
	}
	for i := 0; i < len(τοπικόsockets); i++ {
		τοπικόsockets[i] = τοπικόdatagramΥποδοχή{}
	}
	επόμενοephemeralΘύρα = 49152
	άνοιγμαΑρχείοΠίνακας[0] = άνοιγμαΑρχείοΠεριγραφή{σεχρήση: true, είδος: fdΕίδοςstdin, διακόπτες: oΑνάγνωσηonly}
	άνοιγμαΑρχείοΠίνακας[1] = άνοιγμαΑρχείοΠεριγραφή{σεχρήση: true, είδος: fdΕίδοςconsole, διακόπτες: oΕγγραφήonly}
	άνοιγμαΑρχείοΠίνακας[2] = άνοιγμαΑρχείοΠεριγραφή{σεχρήση: true, είδος: fdΕίδοςconsole, διακόπτες: oΕγγραφήonly}
}

func εύρεσηΔιεργασία(pid uint32) *διεργασίακαταχώρηση {
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		if διεργασίαΠίνακας[i].σεχρήση && διεργασίαΠίνακας[i].pid == pid {
			return &διεργασίαΠίνακας[i]
		}
	}
	return nil
}

func initializeΔιεργασίαfds(διεργασία *διεργασίακαταχώρηση) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		διεργασία.fds[fd] = fdκαταχώρηση{σεχρήση: true, περιγραφή: fd}
		άνοιγμαΑρχείοΠίνακας[fd].refs++
	}
}

func ensureΤρέχονΔιεργασία() *διεργασίακαταχώρηση {
	pid := Τρέχονpid()
	if διεργασία := εύρεσηΔιεργασία(pid); διεργασία != nil {
		return διεργασία
	}
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		if !διεργασίαΠίνακας[i].σεχρήση {
			διεργασίαΠίνακας[i] = διεργασίακαταχώρηση{
				σεχρήση:	true,
				pid:		pid,
				γονικό:		Τρέχονγονικόpid(),
				πρόγραμμαbreak:	χρήστηςheapbase,
			}
			initializeΔιεργασίαfds(&διεργασίαΠίνακας[i])
			return &διεργασίαΠίνακας[i]
		}
	}
	return nil
}

func getΆνοιγμαΑρχείοfor(διεργασία *διεργασίακαταχώρηση, fd int32) *άνοιγμαΑρχείοΠεριγραφή {
	if διεργασία == nil || fd < 0 || fd >= μεγfd || !διεργασία.fds[fd].σεχρήση {
		return nil
	}
	περιγραφή := διεργασία.fds[fd].περιγραφή
	if περιγραφή < 0 || περιγραφή >= μεγΆνοιγμαΑΡΧΕΙΑ || !άνοιγμαΑρχείοΠίνακας[περιγραφή].σεχρήση {
		return nil
	}
	return &άνοιγμαΑρχείοΠίνακας[περιγραφή]
}

func getΆνοιγμαΑρχείο(fd int32) *άνοιγμαΑρχείοΠεριγραφή {
	return getΆνοιγμαΑρχείοfor(ensureΤρέχονΔιεργασία(), fd)
}

func allocateΆνοιγμαΑρχείο() int32 {
	for i := int32(3); i < μεγΆνοιγμαΑΡΧΕΙΑ; i++ {
		if !άνοιγμαΑρχείοΠίνακας[i].σεχρήση {
			άνοιγμαΑρχείοΠίνακας[i] = άνοιγμαΑρχείοΠεριγραφή{σεχρήση: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(διεργασία *διεργασίακαταχώρηση, περιγραφή int32, ελάχιστο int32) int32 {
	if διεργασία == nil {
		return Enfile
	}
	if ελάχιστο < 0 || ελάχιστο >= μεγfd {
		return Einval
	}
	for fd := ελάχιστο; fd < μεγfd; fd++ {
		if !διεργασία.fds[fd].σεχρήση {
			διεργασία.fds[fd] = fdκαταχώρηση{σεχρήση: true, περιγραφή: περιγραφή}
			return fd
		}
	}
	return Emfile
}

func releaseΆνοιγμαΑρχείο(περιγραφή int32) {
	if περιγραφή < 0 || περιγραφή >= μεγΆνοιγμαΑΡΧΕΙΑ {
		return
	}
	καταχώρηση := &άνοιγμαΑρχείοΠίνακας[περιγραφή]
	if καταχώρηση.refs > 0 {
		καταχώρηση.refs--
	}

	if καταχώρηση.refs == 0 && περιγραφή > stderrfd {
		if καταχώρηση.είδος == fdΕίδοςΥποδοχή && καταχώρηση.aux < μεγsockets {
			τοπικόsockets[καταχώρηση.aux] = τοπικόdatagramΥποδοχή{}
		}
		*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
	}
}

func κλείσιμοΔιεργασίαfd(διεργασία *διεργασίακαταχώρηση, fd int32) int32 {
	if διεργασία == nil || getΆνοιγμαΑρχείοfor(διεργασία, fd) == nil {
		return Ebadf
	}
	περιγραφή := διεργασία.fds[fd].περιγραφή
	διεργασία.fds[fd] = fdκαταχώρηση{}
	releaseΆνοιγμαΑρχείο(περιγραφή)
	return 0
}

func sysΕγγραφή(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	καταχώρηση := getΆνοιγμαΑρχείο(fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	if καταχώρηση.είδος != fdΕίδοςconsole {
		if καταχώρηση.είδος == fdΕίδοςΥποδοχή {
			return υποδοχήΑποστολήto(fd, address, count, 0, 0)
		}
		if καταχώρηση.είδος == fdΕίδοςfat || καταχώρηση.είδος == fdΕίδοςΡιζικόςκατάλογοςΚατάλογος {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesfromΔείκτης(uintptr(address), int(count), int(count))
	console_2.MΕκτύπωση(buffer)
	return int32(count)
}

func sysΑνάγνωση(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	καταχώρηση := getΆνοιγμαΑρχείο(fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	if καταχώρηση.είδος == fdΕίδοςstdin {
		return ανάγνωσηstdin(address, count)
	}
	if καταχώρηση.είδος == fdΕίδοςΡιζικόςκατάλογοςΚατάλογος {
		return Eisdir
	}
	if καταχώρηση.είδος == fdΕίδοςΥποδοχή {
		return υποδοχήreceivefrom(fd, address, count, 0, 0)
	}
	if καταχώρηση.είδος != fdΕίδοςfat {
		return Ebadf
	}
	if καταχώρηση.θέση >= καταχώρηση.μέγεθος {
		return 0
	}
	remaining := καταχώρηση.μέγεθος - καταχώρηση.θέση
	if count > remaining {
		count = remaining
	}
	buffer := GetbytesfromΔείκτης(uintptr(address), int(count), int(count))
	return ανάγνωσηvfsΑρχείο(καταχώρηση, buffer, count)
}

func sysΆνοιγμα(δΙΑΔΡΟΜΗaddress uint32, διακόπτες uint32, κΑΤΑΣΤΑΣΗ uint32) int32 {
	_ = κΑΤΑΣΤΑΣΗ
	if δΙΑΔΡΟΜΗaddress == 0 {
		return Efault
	}
	προσπέλασηΚΑΤΑΣΤΑΣΗ := διακόπτες & 3
	if προσπέλασηΚΑΤΑΣΤΑΣΗ == oΕγγραφήonly || προσπέλασηΚΑΤΑΣΤΑΣΗ == oΑνάγνωσηΕγγραφή || (διακόπτες&(ocreate|oΑποκοπήψηφίων|oappend)) != 0 {
		return Erofs
	}

	διεργασία := ensureΤρέχονΔιεργασία()
	if διεργασία == nil {
		return Enfile
	}
	περιγραφή := allocateΆνοιγμαΑρχείο()
	if περιγραφή < 0 {
		return περιγραφή
	}
	καταχώρηση := &άνοιγμαΑρχείοΠίνακας[περιγραφή]
	καταχώρηση.διακόπτες = διακόπτες
	if isΡιζικόςκατάλογοςΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress) {
		καταχώρηση.είδος = fdΕίδοςΡιζικόςκατάλογοςΚατάλογος
		καταχώρηση.μέγεθος = 0
	} else {
		όνομαlen, όνομα := αντιγραφήΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress)
		if όνομαlen == 0 {
			*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
			return Enoent
		}
		μέγεθος := αρχείοΜέγεθος(όνομα[:όνομαlen])
		if μέγεθος == 0 {
			*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
			return Enoent
		}
		if (διακόπτες & oΚατάλογος) != 0 {
			*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
			return Enotdir
		}
		καταχώρηση.είδος = fdΕίδοςfat
		καταχώρηση.μέγεθος = μέγεθος
		καταχώρηση.όνομαlen = όνομαlen
		καταχώρηση.όνομα = όνομα
	}

	fd := allocatefd(διεργασία, περιγραφή, 3)
	if fd < 0 {
		*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
		return fd
	}
	return fd
}

func sysΚλείσιμο(fd int32) int32 {
	return κλείσιμοΔιεργασίαfd(ensureΤρέχονΔιεργασία(), fd)
}

func sysdup(fd int32, ελάχιστο int32) int32 {
	διεργασία := ensureΤρέχονΔιεργασία()
	καταχώρηση := getΆνοιγμαΑρχείοfor(διεργασία, fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	νέοfd := allocatefd(διεργασία, διεργασία.fds[fd].περιγραφή, ελάχιστο)
	if νέοfd >= 0 {
		καταχώρηση.refs++
	}
	return νέοfd
}

func sysdup2(oldfd int32, νέοfd int32) int32 {
	διεργασία := ensureΤρέχονΔιεργασία()
	καταχώρηση := getΆνοιγμαΑρχείοfor(διεργασία, oldfd)
	if καταχώρηση == nil {
		return Ebadf
	}
	if νέοfd < 0 || νέοfd >= μεγfd {
		return Ebadf
	}
	if oldfd == νέοfd {
		return νέοfd
	}
	if διεργασία.fds[νέοfd].σεχρήση {
		κλείσιμοΔιεργασίαfd(διεργασία, νέοfd)
	}
	διεργασία.fds[νέοfd] = fdκαταχώρηση{σεχρήση: true, περιγραφή: διεργασία.fds[oldfd].περιγραφή}
	καταχώρηση.refs++
	return νέοfd
}

func sysfcntl(fd int32, εντολή uint32, argument uint32) int32 {
	διεργασία := ensureΤρέχονΔιεργασία()
	καταχώρηση := getΆνοιγμαΑρχείοfor(διεργασία, fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	switch εντολή {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(διεργασία.fds[fd].fdΔιακόπτες)
	case fσύνολοfd:
		διεργασία.fds[fd].fdΔιακόπτες = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(καταχώρηση.διακόπτες)
	case fσύνολοfl:
		καταχώρηση.διακόπτες = (καταχώρηση.διακόπτες & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	καταχώρηση := getΆνοιγμαΑρχείο(fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	if καταχώρηση.είδος != fdΕίδοςfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekσύνολο:
		base = 0
	case seekΤρέχον:
		base = int64(καταχώρηση.θέση)
	case seekΤέλος:
		base = int64(καταχώρηση.μέγεθος)
	default:
		return Einval
	}
	θέση_2 := base + int64(offset)
	if θέση_2 < 0 || θέση_2 > 0x7FFFFFFF {
		return Einval
	}
	καταχώρηση.θέση = uint32(θέση_2)
	return int32(καταχώρηση.θέση)
}

func ανάγνωσηvfsΑρχείο(καταχώρηση *άνοιγμαΑρχείοΠεριγραφή, προορισμός_2 []byte, count uint32) int32 {
	μνήμηmanager := &mem.TΜνήμηmanager{}
	tmpΔείκτης := μνήμηmanager.Malloc(καταχώρηση.μέγεθος)
	if tmpΔείκτης == nil {
		return Einval
	}
	tmp := GetbytesfromΔείκτης(uintptr(tmpΔείκτης), int(καταχώρηση.μέγεθος), int(καταχώρηση.μέγεθος))
	ανάγνωσηΑρχείο(καταχώρηση.όνομα[:καταχώρηση.όνομαlen], tmp)
	copy(προορισμός_2[:count], tmp[καταχώρηση.θέση:καταχώρηση.θέση+count])
	καταχώρηση.θέση += count
	μνήμηmanager.Ελεύθερα(tmpΔείκτης)
	return int32(count)
}

func isΡιζικόςκατάλογοςΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress uint32) bool {
	if δΙΑΔΡΟΜΗaddress == 0 {
		return false
	}
	δΙΑΔΡΟΜΗ := GetbytesfromΔείκτης(uintptr(δΙΑΔΡΟΜΗaddress), 4, 4)
	if δΙΑΔΡΟΜΗ[0] == '/' && δΙΑΔΡΟΜΗ[1] == 0 {
		return true
	}
	if δΙΑΔΡΟΜΗ[0] == '.' && δΙΑΔΡΟΜΗ[1] == 0 {
		return true
	}
	if δΙΑΔΡΟΜΗ[0] == '/' && δΙΑΔΡΟΜΗ[1] == '.' && δΙΑΔΡΟΜΗ[2] == 0 {
		return true
	}
	return false
}

func sysπροσπέλαση(δΙΑΔΡΟΜΗaddress uint32, κΑΤΑΣΤΑΣΗ uint32) int32 {
	if δΙΑΔΡΟΜΗaddress == 0 {
		return Efault
	}
	if (κΑΤΑΣΤΑΣΗ & ^uint32(7)) != 0 {
		return Einval
	}
	isΡιζικόςκατάλογος := isΡιζικόςκατάλογοςΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress)
	exists := isΡιζικόςκατάλογος
	if !exists {
		όνομαlen, όνομα := αντιγραφήΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress)
		exists = όνομαlen != 0 && αρχείοΜέγεθος(όνομα[:όνομαlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (κΑΤΑΣΤΑΣΗ & 2) != 0 {
		return Eacces
	}

	if (κΑΤΑΣΤΑΣΗ&1) != 0 && !isΡιζικόςκατάλογος {
		return Eacces
	}
	return 0
}

func syschdir(δΙΑΔΡΟΜΗaddress uint32) int32 {
	if δΙΑΔΡΟΜΗaddress == 0 {
		return Efault
	}
	if !isΡιζικόςκατάλογοςΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, μέγεθος uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if μέγεθος < 2 {
		return Erange
	}
	buffer_2 := GetbytesfromΔείκτης(uintptr(bufferaddress), int(μέγεθος), int(μέγεθος))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, κΑΤΑΣΤΑΣΗ uint32, μέγεθος uint32, κόμβος uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Συσκευή = 1
	stat.Ino = κόμβος
	stat.ΚΑΤΑΣΤΑΣΗ = κΑΤΑΣΤΑΣΗ
	stat.Nlink = 1
	stat.Μέγεθος_2 = int32(μέγεθος)
	stat.Blksize = 512
	stat.Μπλοκ = int32((μέγεθος + 511) / 512)
	return 0
}

func sysstat(δΙΑΔΡΟΜΗaddress uint32, stataddress uint32) int32 {
	if δΙΑΔΡΟΜΗaddress == 0 {
		return Efault
	}
	if isΡιζικόςκατάλογοςΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	όνομαlen, όνομα := αντιγραφήΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress)
	if όνομαlen == 0 {
		return Enoent
	}
	μέγεθος := αρχείοΜέγεθος(όνομα[:όνομαlen])
	if μέγεθος == 0 {
		return Enoent
	}
	κόμβος := uint32(2)
	for i := uint32(0); i < όνομαlen; i++ {
		κόμβος = κόμβος*33 + uint32(όνομα[i])
	}
	return fillposixstat(stataddress, sifreg|0444, μέγεθος, κόμβος)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	καταχώρηση := getΆνοιγμαΑρχείο(fd)
	if καταχώρηση == nil {
		return Ebadf
	}
	switch καταχώρηση.είδος {
	case fdΕίδοςstdin, fdΕίδοςconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdΕίδοςΡιζικόςκατάλογοςΚατάλογος:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdΕίδοςfat:
		return fillposixstat(stataddress, sifreg|0444, καταχώρηση.μέγεθος, uint32(fd+2))
	case fdΕίδοςΥποδοχή:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getΆνοιγμαΑρχείο(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	διεργασία := ensureΤρέχονΔιεργασία()
	if διεργασία == nil {
		return 0
	}
	if διεργασία.πρόγραμμαbreak == 0 {
		διεργασία.πρόγραμμαbreak = χρήστηςheapbase
	}
	if address_2 == 0 {
		return διεργασία.πρόγραμμαbreak
	}
	if address_2 < χρήστηςheapbase || address_2 > χρήστηςheapΌριο {
		return διεργασία.πρόγραμμαbreak
	}
	διεργασία.πρόγραμμαbreak = address_2
	return διεργασία.πρόγραμμαbreak
}

func αντιγραφήutsπεδίο(προορισμός *[65]byte, τιμή string) {
	όριο := len(τιμή)
	if όριο > 64 {
		όριο = 64
	}
	for i := 0; i < όριο; i++ {
		προορισμός[i] = τιμή[i]
	}
	προορισμός[όριο] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	όνομα := (*posixutsname)(Pointer(uintptr(address_2)))
	*όνομα = posixutsname{}
	αντιγραφήutsπεδίο(&όνομα.Sysname, "EngOS")
	αντιγραφήutsπεδίο(&όνομα.Nodename, "engos")
	αντιγραφήutsπεδίο(&όνομα.Release, "0.1-posix")
	αντιγραφήutsπεδίο(&όνομα.Έκδοση, "POSIX.1-2017 phase 1")
	αντιγραφήutsπεδίο(&όνομα.Machine, "i386")
	return 0
}

func swapunsignedinteger16(τιμή uint16) uint16 {
	return (τιμή << 8) | (τιμή >> 8)
}

func υποδοχήcallargument(παράμετροι_2 uint32, κατάλογος uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(παράμετροι_2 + κατάλογος*4)))
}

func υποδοχήforfd(fd int32) (*τοπικόdatagramΥποδοχή, int32) {
	καταχώρηση := getΆνοιγμαΑρχείο(fd)
	if καταχώρηση == nil || καταχώρηση.είδος != fdΕίδοςΥποδοχή || καταχώρηση.aux >= μεγsockets {
		return nil, Ebadf
	}
	υποδοχή := &τοπικόsockets[καταχώρηση.aux]
	if !υποδοχή.σεχρήση {
		return nil, Ebadf
	}
	return υποδοχή, 0
}

func allocateΥποδοχή(τομέας uint32, υποδοχήΤύπος uint32, protocol uint32) int32 {
	if τομέας != afinet {
		return Eafnosupport
	}
	if υποδοχήΤύπος != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	διεργασία := ensureΤρέχονΔιεργασία()
	if διεργασία == nil {
		return Enfile
	}
	υποδοχήΚατάλογος := -1
	for i := 0; i < μεγsockets; i++ {
		if !τοπικόsockets[i].σεχρήση {
			υποδοχήΚατάλογος = i
			break
		}
	}
	if υποδοχήΚατάλογος < 0 {
		return Enfile
	}
	περιγραφή := allocateΆνοιγμαΑρχείο()
	if περιγραφή < 0 {
		return περιγραφή
	}
	τοπικόsockets[υποδοχήΚατάλογος] = τοπικόdatagramΥποδοχή{σεχρήση: true}
	καταχώρηση := &άνοιγμαΑρχείοΠίνακας[περιγραφή]
	καταχώρηση.είδος = fdΕίδοςΥποδοχή
	καταχώρηση.διακόπτες = oΑνάγνωσηΕγγραφή
	καταχώρηση.aux = uint32(υποδοχήΚατάλογος)
	fd := allocatefd(διεργασία, περιγραφή, 3)
	if fd < 0 {
		τοπικόsockets[υποδοχήΚατάλογος] = τοπικόdatagramΥποδοχή{}
		*καταχώρηση = άνοιγμαΑρχείοΠεριγραφή{}
		return fd
	}
	return fd
}

func υποδοχήaddress(address_2 uint32, διάρκεια uint32) (*υποδοχήaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if διάρκεια < 16 {
		return nil, Einval
	}
	result := (*υποδοχήaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func θύρασεΧρήση(θύρα uint16, except *τοπικόdatagramΥποδοχή) bool {
	for i := 0; i < μεγsockets; i++ {
		υποδοχή := &τοπικόsockets[i]
		if υποδοχή != except && υποδοχή.σεχρήση && υποδοχή.bound && υποδοχή.τοπικό.Θύρα == θύρα {
			return true
		}
	}
	return false
}

func bindephemeral(υποδοχή *τοπικόdatagramΥποδοχή) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		θύρα := swapunsignedinteger16(επόμενοephemeralΘύρα)
		επόμενοephemeralΘύρα++
		if επόμενοephemeralΘύρα < 49152 {
			επόμενοephemeralΘύρα = 49152
		}
		if !θύρασεΧρήση(θύρα, υποδοχή) {
			υποδοχή.τοπικό = υποδοχήaddressipv4{Family: afinet, Θύρα: θύρα, Address: 0x0100007F}
			υποδοχή.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func υποδοχήbind(fd int32, address_2 uint32, διάρκεια uint32) int32 {
	υποδοχή, σφάλλω := υποδοχήforfd(fd)
	if σφάλλω != 0 {
		return σφάλλω
	}
	requested, σφάλλω := υποδοχήaddress(address_2, διάρκεια)
	if σφάλλω != 0 {
		return σφάλλω
	}
	if υποδοχή.bound {
		return Einval
	}
	if requested.Θύρα == 0 {
		return bindephemeral(υποδοχή)
	}
	if θύρασεΧρήση(requested.Θύρα, υποδοχή) {
		return Eaddrinuse
	}
	υποδοχή.τοπικό = *requested
	υποδοχή.bound = true
	return 0
}

func υποδοχήΣύνδεση(fd int32, address_2 uint32, διάρκεια uint32) int32 {
	υποδοχή, σφάλλω := υποδοχήforfd(fd)
	if σφάλλω != 0 {
		return σφάλλω
	}
	απομακρυσμένο, σφάλλω := υποδοχήaddress(address_2, διάρκεια)
	if σφάλλω != 0 {
		return σφάλλω
	}
	if !υποδοχή.bound {
		if σφάλλω := bindephemeral(υποδοχή); σφάλλω != 0 {
			return σφάλλω
		}
	}
	υποδοχή.απομακρυσμένο = *απομακρυσμένο
	υποδοχή.connected = true
	return 0
}

func υποδοχήΑποστολήto(fd int32, bufferaddress_2 uint32, διάρκεια uint32, προορισμόςaddress uint32, προορισμόςΔιάρκεια uint32) int32 {
	υποδοχή, σφάλλω := υποδοχήforfd(fd)
	if σφάλλω != 0 {
		return σφάλλω
	}
	if διάρκεια > μεγdatagramΜέγεθος {
		return Emsgsize
	}
	if διάρκεια != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var προορισμός υποδοχήaddressipv4
	if προορισμόςaddress != 0 {
		address_2, addressΣφάλμα := υποδοχήaddress(προορισμόςaddress, προορισμόςΔιάρκεια)
		if addressΣφάλμα != 0 {
			return addressΣφάλμα
		}
		προορισμός = *address_2
	} else {
		if !υποδοχή.connected {
			return Enotconn
		}
		προορισμός = υποδοχή.απομακρυσμένο
	}
	if !υποδοχή.bound {
		if bindΣφάλμα := bindephemeral(υποδοχή); bindΣφάλμα != 0 {
			return bindΣφάλμα
		}
	}
	var receiver *τοπικόdatagramΥποδοχή
	for i := 0; i < μεγsockets; i++ {
		candidate := &τοπικόsockets[i]
		if candidate.σεχρήση && candidate.bound && candidate.τοπικό.Θύρα == προορισμός.Θύρα &&
			(candidate.τοπικό.Address == 0 || candidate.τοπικό.Address == προορισμός.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= μεγΥποδοχήπακέτα {
		return Eagain
	}
	packet := &receiver.πακέτα[receiver.tail]
	*packet = υποδοχήpacket{σεχρήση: true, μέγεθος: διάρκεια, πηγή: υποδοχή.τοπικό}
	if διάρκεια != 0 {
		πηγή := GetbytesfromΔείκτης(uintptr(bufferaddress_2), int(διάρκεια), int(διάρκεια))
		copy(packet.data[:διάρκεια], πηγή)
	}
	receiver.tail = (receiver.tail + 1) % μεγΥποδοχήπακέτα
	receiver.count++
	return int32(διάρκεια)
}

func υποδοχήreceivefrom(fd int32, bufferaddress_2 uint32, διάρκεια uint32, πηγήaddress uint32, πηγήΔιάρκειαaddress uint32) int32 {
	υποδοχή, σφάλλω := υποδοχήforfd(fd)
	if σφάλλω != 0 {
		return σφάλλω
	}
	if διάρκεια != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if υποδοχή.count == 0 {
		return Eagain
	}
	packet := &υποδοχή.πακέτα[υποδοχή.head]
	αντιγραφήΔιάρκεια := packet.μέγεθος
	if αντιγραφήΔιάρκεια > διάρκεια {
		αντιγραφήΔιάρκεια = διάρκεια
	}
	if αντιγραφήΔιάρκεια != 0 {
		προορισμός := GetbytesfromΔείκτης(uintptr(bufferaddress_2), int(αντιγραφήΔιάρκεια), int(αντιγραφήΔιάρκεια))
		copy(προορισμός, packet.data[:αντιγραφήΔιάρκεια])
	}
	if πηγήaddress != 0 {
		if πηγήΔιάρκειαaddress == 0 {
			return Efault
		}
		providedΔιάρκεια := (*uint32)(Pointer(uintptr(πηγήΔιάρκειαaddress)))
		if *providedΔιάρκεια >= 16 {
			*(*υποδοχήaddressipv4)(Pointer(uintptr(πηγήaddress))) = packet.πηγή
		}
		*providedΔιάρκεια = 16
	}
	*packet = υποδοχήpacket{}
	υποδοχή.head = (υποδοχή.head + 1) % μεγΥποδοχήπακέτα
	υποδοχή.count--
	return int32(αντιγραφήΔιάρκεια)
}

func αντιγραφήΥποδοχήΌνομα(fd int32, address_2 uint32, διάρκειαaddress uint32, peer bool) int32 {
	υποδοχή, σφάλλω := υποδοχήforfd(fd)
	if σφάλλω != 0 {
		return σφάλλω
	}
	if address_2 == 0 || διάρκειαaddress == 0 {
		return Efault
	}
	διάρκεια := (*uint32)(Pointer(uintptr(διάρκειαaddress)))
	if *διάρκεια < 16 {
		*διάρκεια = 16
		return Einval
	}
	if peer {
		if !υποδοχή.connected {
			return Enotconn
		}
		*(*υποδοχήaddressipv4)(Pointer(uintptr(address_2))) = υποδοχή.απομακρυσμένο
	} else {
		if !υποδοχή.bound {
			if bindΣφάλμα := bindephemeral(υποδοχή); bindΣφάλμα != 0 {
				return bindΣφάλμα
			}
		}
		*(*υποδοχήaddressipv4)(Pointer(uintptr(address_2))) = υποδοχή.τοπικό
	}
	*διάρκεια = 16
	return 0
}

func sysΥποδοχήcall(call uint32, παράμετροι_2 uint32) int32 {
	if παράμετροι_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateΥποδοχή(υποδοχήcallargument(παράμετροι_2, 0), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2))
	case 2:
		return υποδοχήbind(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2))
	case 3:
		return υποδοχήΣύνδεση(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return αντιγραφήΥποδοχήΌνομα(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), false)
	case 7:
		return αντιγραφήΥποδοχήΌνομα(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), true)
	case 9:
		return υποδοχήΑποστολήto(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), 0, 0)
	case 10:
		return υποδοχήreceivefrom(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), 0, 0)
	case 11:
		return υποδοχήΑποστολήto(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), υποδοχήcallargument(παράμετροι_2, 4), υποδοχήcallargument(παράμετροι_2, 5))
	case 12:
		return υποδοχήreceivefrom(int32(υποδοχήcallargument(παράμετροι_2, 0)), υποδοχήcallargument(παράμετροι_2, 1), υποδοχήcallargument(παράμετροι_2, 2), υποδοχήcallargument(παράμετροι_2, 4), υποδοχήcallargument(παράμετροι_2, 5))
	case 13:
		if _, σφάλλω := υποδοχήforfd(int32(υποδοχήcallargument(παράμετροι_2, 0))); σφάλλω != 0 {
			return σφάλλω
		}
		return 0
	case 14:
		if _, σφάλλω := υποδοχήforfd(int32(υποδοχήcallargument(παράμετροι_2, 0))); σφάλλω != 0 {
			return σφάλλω
		}
		return 0
	}
	return Eopnotsupp
}

func ανάγνωσηstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetbytesfromΔείκτης(uintptr(address), int(count), int(count))
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
	επόμενο := (stdinΕγγραφή + 1) % uint32(len(stdinbuffer))
	if επόμενο == stdinΑνάγνωση {
		return
	}
	stdinbuffer[stdinΕγγραφή] = c
	stdinΕγγραφή = επόμενο
}

func stdingetblocking() byte {
	for stdinΑνάγνωση == stdinΕγγραφή {
		sc := pollΠληκτρολόγιοscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinΑνάγνωση]
	stdinΑνάγνωση = (stdinΑνάγνωση + 1) % uint32(len(stdinbuffer))
	return c
}

func pollΠληκτρολόγιοscancode() byte {
	for (ΘύραΑνάγνωσηbyte(0x64) & 0x01) == 0 {
	}
	sc := ΘύραΑνάγνωσηbyte(0x60)
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

func αντιγραφήΕκτέλεσηvector(address_2 uint32, result *εκτέλεσηvector) int32 {
	*result = εκτέλεσηvector{}
	if address_2 == 0 {
		return 0
	}
	for κατάλογος := uint32(0); κατάλογος < μεγΕκτέλεσηvectorκαταχώρηση; κατάλογος++ {
		συμβολοσειράaddress := *(*uint32)(Pointer(uintptr(address_2 + κατάλογος*4)))
		if συμβολοσειράaddress == 0 {
			result.count = κατάλογος
			return 0
		}
		terminated := false
		for διάρκεια := uint32(0); διάρκεια <= μεγΕκτέλεσηΣυμβολοσειράΔιάρκεια; διάρκεια++ {
			τιμή := *(*byte)(Pointer(uintptr(συμβολοσειράaddress + διάρκεια)))
			result.τιμές[κατάλογος][διάρκεια] = τιμή
			if τιμή == 0 {
				result.lengths[κατάλογος] = διάρκεια
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

func pushΕκτέλεσηunsignedinteger32(stack *uint32, τιμή uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = τιμή
}

func setupΕκτέλεσηstack(επεξεργαστής *TcpuΚατάσταση, παράμετροι_2 *εκτέλεσηvector, environment *εκτέλεσηvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeΕύροςΙδιωτικόwritable(getcr3(), ΧρήστηςstackΠάνω-stackbytes, stackbytes) {
		return Enomem
	}
	stack := ΧρήστηςstackΠάνω
	var argumentpointers [μεγΕκτέλεσηvectorκαταχώρηση]uint32
	var environmentpointers [μεγΕκτέλεσηvectorκαταχώρηση]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		διάρκεια := environment.lengths[i] + 1
		stack -= διάρκεια
		προορισμός := GetbytesfromΔείκτης(uintptr(stack), int(διάρκεια), int(διάρκεια))
		copy(προορισμός, environment.τιμές[i][:διάρκεια])
		environmentpointers[i] = stack
	}
	for i := int(παράμετροι_2.count) - 1; i >= 0; i-- {
		διάρκεια := παράμετροι_2.lengths[i] + 1
		stack -= διάρκεια
		προορισμός := GetbytesfromΔείκτης(uintptr(stack), int(διάρκεια), int(διάρκεια))
		copy(προορισμός, παράμετροι_2.τιμές[i][:διάρκεια])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushΕκτέλεσηunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushΕκτέλεσηunsignedinteger32(&stack, environmentpointers[i])
	}
	pushΕκτέλεσηunsignedinteger32(&stack, 0)
	for i := int(παράμετροι_2.count) - 1; i >= 0; i-- {
		pushΕκτέλεσηunsignedinteger32(&stack, argumentpointers[i])
	}
	pushΕκτέλεσηunsignedinteger32(&stack, παράμετροι_2.count)
	επεξεργαστής.Esp = stack
	επεξεργαστής.Ebp = 0
	return 0
}

func κλείσιμοΕνεργήΕκτέλεση(διεργασία *διεργασίακαταχώρηση) {
	if διεργασία == nil {
		return
	}
	for fd := int32(0); fd < μεγfd; fd++ {
		if διεργασία.fds[fd].σεχρήση && (διεργασία.fds[fd].fdΔιακόπτες&fdcloexec) != 0 {
			κλείσιμοΔιεργασίαfd(διεργασία, fd)
		}
	}
}

func sysexecve(επεξεργαστής *TcpuΚατάσταση, δΙΑΔΡΟΜΗaddress uint32) int32 {
	if δΙΑΔΡΟΜΗaddress == 0 {
		return Efault
	}
	var παράμετροι_2 εκτέλεσηvector
	var environment εκτέλεσηvector
	if result := αντιγραφήΕκτέλεσηvector(επεξεργαστής.Ecx, &παράμετροι_2); result < 0 {
		return result
	}
	if result := αντιγραφήΕκτέλεσηvector(επεξεργαστής.Edx, &environment); result < 0 {
		return result
	}
	όνομαlen, όνομα := αντιγραφήΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress)
	if όνομαlen == 0 {
		return Enoent
	}
	μέγεθος := αρχείοΜέγεθος(όνομα[:όνομαlen])
	if μέγεθος == 0 {
		return Enoent
	}
	μνήμηmanager := &mem.TΜνήμηmanager{}
	αρχείοΔείκτης := μνήμηmanager.Malloc(μέγεθος)
	if αρχείοΔείκτης == nil {
		return Einval
	}
	data := GetbytesfromΔείκτης(uintptr(αρχείοΔείκτης), int(μέγεθος), int(μέγεθος))
	ανάγνωσηΑρχείο(όνομα[:όνομαlen], data)
	if μέγεθος < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		μνήμηmanager.Ελεύθερα(αρχείοΔείκτης)
		return Enoexec
	}
	loader := Elf{}
	καταχώρηση := loader.Getκαταχώρηση(data)
	loader.Parse(data, getcr3())
	μνήμηmanager.Ελεύθερα(αρχείοΔείκτης)
	if result := setupΕκτέλεσηstack(επεξεργαστής, &παράμετροι_2, &environment); result < 0 {
		return result
	}
	κλείσιμοΕνεργήΕκτέλεση(ensureΤρέχονΔιεργασία())
	επεξεργαστής.Eip = καταχώρηση
	επεξεργαστής.Eax = 0
	return 0
}

func sysfork(επεξεργαστής *TcpuΚατάσταση) int32 {
	γονικόpid := Τρέχονpid()
	if ensureΤρέχονΔιεργασία() == nil {
		return Enfile
	}
	pid := allocateΔιεργασία(γονικόpid)
	if pid == 0 {
		return Einval
	}
	μνήμηmanager := &mem.TΜνήμηmanager{}
	threadΔείκτης := μνήμηmanager.Malloc(uint32(Sizeof(TThread{})))
	stackΔείκτης := μνήμηmanager.Malloc(ThreadstackΜέγεθος)
	θυγατρικήΣελίδαΚατάλογος := CloneaddressΔιάστημαcow(getcr3())
	if threadΔείκτης == nil || stackΔείκτης == nil || θυγατρικήΣελίδαΚατάλογος == 0 {
		απόρριψηΔιεργασία(pid)
		return Einval
	}
	θυγατρική := (*TThread)(threadΔείκτης)
	θυγατρική.Stack = uint32(uintptr(stackΔείκτης))
	θυγατρική.ΕπεξεργαστήςΚατάσταση = (*TcpuΚατάσταση)(Pointer(uintptr(stackΔείκτης) + ThreadstackΜέγεθος - Sizeof(TcpuΚατάσταση{})))
	*θυγατρική.ΕπεξεργαστήςΚατάσταση = *επεξεργαστής
	θυγατρική.ΕπεξεργαστήςΚατάσταση.Eax = 0
	θυγατρική.Χρήστηςstack_2 = επεξεργαστής.Esp
	θυγατρική.ΧρήστηςstackΜέγεθος_2 = 0
	θυγατρική.Pid = pid
	θυγατρική.Γονικόpid = γονικόpid
	θυγατρική.ΣελίδαΚατάλογοςκαταχώρηση = θυγατρικήΣελίδαΚατάλογος
	θυγατρική.ThreadΚατάσταση = Έτοιμο
	θυγατρική.Fpuoffset = 0xffffffff
	θυγατρική.Iskernel = false
	Προσθήκηrunnablethread(θυγατρική)
	return int32(pid)
}

func sysΈξοδος(κατάσταση uint32) {
	pid := Τρέχονpid()
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		if διεργασίαΠίνακας[i].σεχρήση && διεργασίαΠίνακας[i].pid == pid {
			κλείσιμοΌλαΔιεργασίαfds(&διεργασίαΠίνακας[i])
			διεργασίαΠίνακας[i].τερματίστηκε = true
			διεργασίαΠίνακας[i].κατάσταση = (κατάσταση & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, κατάστασηaddress uint32, επιλογές uint32) int32 {
	if (επιλογές & ^uint32(1)) != 0 {
		return Einval
	}
	γονικόpid := Τρέχονpid()
	foundθυγατρική := false
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		p := &διεργασίαΠίνακας[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.σεχρήση && matches && p.γονικό == γονικόpid {
			foundθυγατρική = true
			if p.τερματίστηκε {
				if κατάστασηaddress != 0 {
					*(*uint32)(Pointer(uintptr(κατάστασηaddress))) = p.κατάσταση
				}
				θυγατρικήpid := p.pid
				*p = διεργασίακαταχώρηση{}
				return int32(θυγατρικήpid)
			}
		}
	}
	if !foundθυγατρική {
		return Echild
	}

	if (επιλογές & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateΔιεργασία(γονικό uint32) uint32 {
	γονικόΔιεργασία := εύρεσηΔιεργασία(γονικό)
	pid := Allocatepid()
	for i := 0; i < len(διεργασίαΠίνακας); i++ {
		if !διεργασίαΠίνακας[i].σεχρήση {
			διεργασίαΠίνακας[i] = διεργασίακαταχώρηση{
				σεχρήση:	true,
				pid:		pid,
				γονικό:		γονικό,
				πρόγραμμαbreak:	χρήστηςheapbase,
			}
			if γονικόΔιεργασία != nil {
				διεργασίαΠίνακας[i].πρόγραμμαbreak = γονικόΔιεργασία.πρόγραμμαbreak
				for fd := 0; fd < μεγfd; fd++ {
					if γονικόΔιεργασία.fds[fd].σεχρήση {
						διεργασίαΠίνακας[i].fds[fd] = γονικόΔιεργασία.fds[fd]
						περιγραφή := γονικόΔιεργασία.fds[fd].περιγραφή
						if περιγραφή >= 0 && περιγραφή < μεγΆνοιγμαΑΡΧΕΙΑ {
							άνοιγμαΑρχείοΠίνακας[περιγραφή].refs++
						}
					}
				}
			} else {
				initializeΔιεργασίαfds(&διεργασίαΠίνακας[i])
			}
			return pid
		}
	}
	return 0
}

func κλείσιμοΌλαΔιεργασίαfds(διεργασία *διεργασίακαταχώρηση) {
	if διεργασία == nil {
		return
	}
	for fd := int32(0); fd < μεγfd; fd++ {
		if διεργασία.fds[fd].σεχρήση {
			κλείσιμοΔιεργασίαfd(διεργασία, fd)
		}
	}
}

func απόρριψηΔιεργασία(pid uint32) {
	διεργασία := εύρεσηΔιεργασία(pid)
	if διεργασία == nil {
		return
	}
	κλείσιμοΌλαΔιεργασίαfds(διεργασία)
	*διεργασία = διεργασίακαταχώρηση{}
}

func αντιγραφήΔΙΑΔΡΟΜΗ(δΙΑΔΡΟΜΗaddress uint32) (uint32, [12]byte) {
	var όνομα [12]byte
	if δΙΑΔΡΟΜΗaddress == 0 {
		return 0, όνομα
	}
	raw := GetbytesfromΔείκτης(uintptr(δΙΑΔΡΟΜΗaddress), 64, 64)
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
		όνομα[n] = c
		n++
	}
	return n, όνομα
}

func αρχείοΜέγεθος(όνομααρχείου []byte) uint32 {
	var ata0s = TΓιαπροχωρημένουςΤεχνολογίαattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionΠίνακας{}
	partition.Ανάγνωσηpartition(&ata0s)

	bios := TBiosparameterΜπλοκ32{}
	μέγεθος := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου)
	ata0s.Flush()
	return μέγεθος
}

func ανάγνωσηΑρχείο(όνομααρχείου []byte, data []byte) {
	var ata0s = TΓιαπροχωρημένουςΤεχνολογίαattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionΠίνακας{}
	partition.Ανάγνωσηpartition(&ata0s)

	bios := TBiosparameterΜπλοκ32{}
	bios.Ανάγνωση(&ata0s, partition.Mbr.Primarypartition[0], όνομααρχείου, data)
	ata0s.Flush()
}

func getcr3() uint32
