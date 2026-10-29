/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package מערכתcall

import . "unsafe"

import . "פסק"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "קובץמערכת/msdospartition"
import . "קובץמערכת/fat"
import . "קובץמערכת/elf"
import mem "זיכרוןmanager"
import . "paging"
import . "שער"
import . "tasking/scheduler"
import . "tasking/thread"
import . "וירטואליזיכרון"

var console_2 = TConsole{}

type TSyscall struct {
	Tפסקhandler
}

const (
	Sysיציאה	uint32	= 1
	Sysfork		uint32	= 2
	Sysקריאה	uint32	= 3
	Sysכתיבה	uint32	= 4
	Sysפתח		uint32	= 5
	Sysסגור		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysגישה		uint32	= 33
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
	Sysrtיציאה	uint32	= 252

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
	stdinמזהה	int32	= 0
	stdoutמזהה	int32	= 1
	stderrמזהה	int32	= 2
	מקסימוםמזהה		= 32
	מקסימוםפתחקבצים		= 128
)

type מזההentry struct {
	בשימוש		bool
	תיאור		int32
	מזההדגלים	uint32
}

type פתחקובץתיאור struct {
	בשימוש	bool
	refs	uint32
	סוג	uint32
	דגלים	uint32
	מיקום	uint32
	גודל	uint32
	שם	[12]byte
	שםlen	uint32
	aux	uint32
}

const (
	מזההסוגללא		uint32	= 0
	מזההסוגfat		uint32	= 1
	מזההסוגstdin		uint32	= 2
	מזההסוגconsole		uint32	= 3
	מזההסוגשורשספרייה	uint32	= 4
	מזההסוגשקע		uint32	= 5

	oקריאהonly	uint32	= 0
	oכתיבהonly	uint32	= 1
	oקריאהכתיבה	uint32	= 2
	ocreate		uint32	= 0x40
	oקיצוץ		uint32	= 0x200
	oappend		uint32	= 0x400
	oספרייה		uint32	= 0x10000

	seekקבע		uint32	= 0
	seekנוכחי	uint32	= 1
	seekסיום	uint32	= 2

	fdupמזהה	uint32	= 0
	fgetמזהה	uint32	= 1
	fקבעמזהה	uint32	= 2
	fgetfl		uint32	= 3
	fקבעfl		uint32	= 4
	מזההcloexec	uint32	= 1

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
	מקסימוםsockets		= 32
	מקסימוםשקעמנותנתונים	= 8
	מקסימוםdatagramגודל	= 512
)

type שקעaddressipv4 struct {
	Family	uint16
	Pשער	uint16
	Address	uint32
	Zero	[8]byte
}

type שקעpacket struct {
	בשימוש	bool
	גודל	uint32
	מקור	שקעaddressipv4
	data	[מקסימוםdatagramגודל]byte
}

type מקומיdatagramשקע struct {
	בשימוש		bool
	bound		bool
	connected	bool
	מקומי		שקעaddressipv4
	מרוחק		שקעaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	מנותנתונים	[מקסימוםשקעמנותנתונים]שקעpacket
}

type posixstat struct {
	Dהתקן		uint32
	Ino		uint32
	Mמצב		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sגודל_2		int32
	Blksize		int32
	Bבלוק		int32
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
	Vגרסה		[65]byte
	Machine		[65]byte
}

const (
	מקסימוםהפעלהvectorentry	= 16
	מקסימוםהפעלהמחרוזתאורך	= 63
)

type הפעלהvector struct {
	count	uint32
	lengths	[מקסימוםהפעלהvectorentry]uint32
	ערכים	[מקסימוםהפעלהvectorentry][מקסימוםהפעלהמחרוזתאורך + 1]byte
}

type תהליךentry struct {
	בשימוש		bool
	מזההתהליך	uint32
	parent		uint32
	exited		bool
	מצב_2		uint32
	תכניתbreak	uint32
	fds		[מקסימוםמזהה]מזההentry
}

type מחרוזתheader struct {
	Data	uintptr
	Len	int
}

func syscallשגיאה(שגיאה int32) uint32 {
	return *(*uint32)(Pointer(&שגיאה))
}

var פתחקובץtable [מקסימוםפתחקבצים]פתחקובץתיאור
var תהליךtable [32]תהליךentry
var מקומיsockets [מקסימוםsockets]מקומיdatagramשקע
var הבאephemeralשער uint16 = 49152

const (
	משתמשheapbase	uint32	= 0x06000000
	משתמשheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinקריאה uint32
var stdinכתיבה uint32

func Iפסק(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysיציאה_2(מפתח uint32) {
	Syscall(Sysיציאה, מפתח)
}

func Sysקריאה_2(מזהה uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysקריאה, מזהה, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysהדפסהstr(buffer string) {
	h := (*מחרוזתheader)(Pointer(&buffer))
	Syscall(Sysכתיבה, uint32(stdoutמזהה), uint32(h.Data), uint32(h.Len))
}

func Sysהדפסהunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysכתיבה, uint32(stdoutמזהה), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysפתח_2(נתיב uintptr, דגלים uint32, מצב uint32) int32 {
	return int32(Syscall(Sysפתח, uint32(נתיב), דגלים, מצב))
}

func Sysסגור_2(מזהה uint32) int32 {
	return int32(Syscall(Sysסגור, מזהה))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(ארגומרנטים ...uint32) uint32 {

	l := len(ארגומרנטים)
	switch l {
	case 1:
		return Iפסק(ארגומרנטים[0], 0, 0, 0, 0, 0)
	case 2:
		return Iפסק(ארגומרנטים[0], ארגומרנטים[1], 0, 0, 0, 0)
	case 3:
		return Iפסק(ארגומרנטים[0], ארגומרנטים[1], ארגומרנטים[2], 0, 0, 0)
	case 4:
		return Iפסק(ארגומרנטים[0], ארגומרנטים[1], ארגומרנטים[2], ארגומרנטים[3], 0, 0)
	case 5:
		return Iפסק(ארגומרנטים[0], ארגומרנטים[1], ארגומרנטים[2], ארגומרנטים[3], ארגומרנטים[4], 0)
	case 6:
		return Iפסק(ארגומרנטים[0], ארגומרנטים[1], ארגומרנטים[2], ארגומרנטים[3], ארגומרנטים[4], ארגומרנטים[5])
	default:
		return syscallשגיאה(Enosys)
	}
}

func (self *TSyscall) Init(manager *Tפסקmanager) {
	initקובץdescriptor()

	פסקhandler = ידיתפסק

	var address uintptr
	address = uintptr(Pointer(&פסקhandler))

	self.Tפסקhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var פסקhandler func(uint32) uint32

func ידיתפסק(esp uint32) uint32 {
	var מעבד = (*Tcpuמצב)(Pointer(uintptr(esp)))

	switch מעבד.Eax {
	case Sysיציאה:
		sysיציאה(מעבד.Ebx)
		return uint32(uintptr(Pointer(Sעצורנוכחיthread(מעבד))))
	case Sysrtיציאה:
		sysיציאה(מעבד.Ebx)
		return uint32(uintptr(Pointer(Sעצורנוכחיthread(מעבד))))
	case Sysfork:
		מעבד.Eax = uint32(sysfork(מעבד))
		return esp
	case Sysקריאה:
		מעבד.Eax = uint32(sysקריאה(int32(מעבד.Ebx), מעבד.Ecx, מעבד.Edx))
		return esp
	case Sysכתיבה:
		מעבד.Eax = uint32(sysכתיבה(int32(מעבד.Ebx), מעבד.Ecx, מעבד.Edx))
		return esp
	case Sysפתח:
		מעבד.Eax = uint32(sysפתח(מעבד.Ebx, מעבד.Ecx, מעבד.Edx))
		return esp
	case Syscreat:
		מעבד.Eax = uint32(sysפתח(מעבד.Ebx, ocreate|oכתיבהonly|oקיצוץ, מעבד.Ecx))
		return esp
	case Sysסגור:
		מעבד.Eax = uint32(sysסגור(int32(מעבד.Ebx)))
		return esp
	case Syswaitpid:
		מעבד.Eax = uint32(syswaitpid(int32(מעבד.Ebx), מעבד.Ecx, מעבד.Edx))
		return esp
	case Syslseek:
		מעבד.Eax = uint32(syslseek(int32(מעבד.Ebx), int32(מעבד.Ecx), מעבד.Edx))
		return esp
	case Sysexecve:
		מעבד.Eax = uint32(sysexecve(מעבד, מעבד.Ebx))
		return esp
	case Sysgetpid:
		מעבד.Eax = Cנוכחימזההתהליך()
		return esp
	case Sysgetppid:
		מעבד.Eax = Cנוכחיparentמזההתהליך()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		מעבד.Eax = 0
		return esp
	case Sysגישה:
		מעבד.Eax = uint32(sysגישה(מעבד.Ebx, מעבד.Ecx))
		return esp
	case Syschdir:
		מעבד.Eax = uint32(syschdir(מעבד.Ebx))
		return esp
	case Sysgetcwd:
		מעבד.Eax = uint32(sysgetcwd(מעבד.Ebx, מעבד.Ecx))
		return esp
	case Sysdup:
		מעבד.Eax = uint32(sysdup(int32(מעבד.Ebx), 0))
		return esp
	case Sysdup2:
		מעבד.Eax = uint32(sysdup2(int32(מעבד.Ebx), int32(מעבד.Ecx)))
		return esp
	case Syssocketcall:
		מעבד.Eax = uint32(sysשקעcall(מעבד.Ebx, מעבד.Ecx))
		return esp
	case Sysfcntl:
		מעבד.Eax = uint32(sysfcntl(int32(מעבד.Ebx), מעבד.Ecx, מעבד.Edx))
		return esp
	case Sysstat, Syslstat:
		מעבד.Eax = uint32(sysstat(מעבד.Ebx, מעבד.Ecx))
		return esp
	case Sysfstat:
		מעבד.Eax = uint32(sysfstat(int32(מעבד.Ebx), מעבד.Ecx))
		return esp
	case Sysfsync:
		מעבד.Eax = uint32(sysfsync(int32(מעבד.Ebx)))
		return esp
	case Syssync:
		מעבד.Eax = 0
		return esp
	case Sysuname:
		מעבד.Eax = uint32(sysuname(מעבד.Ebx))
		return esp
	case Sysbrk:
		מעבד.Eax = sysbrk(מעבד.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32הדפסה(מעבד.Ebx)
		return esp

	default:
		console_2.Mהדפסהxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32הדפסה(esp)
		console_2.Mהדפסה(([]byte)(":"))
		console_2.MUnsignedinteger32הדפסה(מעבד.Eax)
		console_2.Mהדפסה(([]byte)(":"))
		console_2.MUnsignedinteger32הדפסה(מעבד.Ebx)
		console_2.Mהדפסה(([]byte)(":"))
		console_2.MUnsignedinteger32הדפסה(מעבד.Ecx)
		console_2.Mהדפסה(([]byte)(":"))
		console_2.MUnsignedinteger32הדפסה(מעבד.Edx)
		console_2.Mהדפסה(([]byte)("]"))
		מעבד.Eax = syscallשגיאה(Enosys)
		return esp
	}

	return esp
}

func initקובץdescriptor() {
	for i := 0; i < מקסימוםפתחקבצים; i++ {
		פתחקובץtable[i] = פתחקובץתיאור{}
	}
	for i := 0; i < len(תהליךtable); i++ {
		תהליךtable[i] = תהליךentry{}
	}
	for i := 0; i < len(מקומיsockets); i++ {
		מקומיsockets[i] = מקומיdatagramשקע{}
	}
	הבאephemeralשער = 49152
	פתחקובץtable[0] = פתחקובץתיאור{בשימוש: true, סוג: מזההסוגstdin, דגלים: oקריאהonly}
	פתחקובץtable[1] = פתחקובץתיאור{בשימוש: true, סוג: מזההסוגconsole, דגלים: oכתיבהonly}
	פתחקובץtable[2] = פתחקובץתיאור{בשימוש: true, סוג: מזההסוגconsole, דגלים: oכתיבהonly}
}

func חיפושתהליך(מזההתהליך uint32) *תהליךentry {
	for i := 0; i < len(תהליךtable); i++ {
		if תהליךtable[i].בשימוש && תהליךtable[i].מזההתהליך == מזההתהליך {
			return &תהליךtable[i]
		}
	}
	return nil
}

func initializeתהליךfds(תהליך *תהליךentry) {
	for מזהה := int32(0); מזהה <= stderrמזהה; מזהה++ {
		תהליך.fds[מזהה] = מזההentry{בשימוש: true, תיאור: מזהה}
		פתחקובץtable[מזהה].refs++
	}
}

func ensureנוכחיתהליך() *תהליךentry {
	מזההתהליך := Cנוכחימזההתהליך()
	if תהליך := חיפושתהליך(מזההתהליך); תהליך != nil {
		return תהליך
	}
	for i := 0; i < len(תהליךtable); i++ {
		if !תהליךtable[i].בשימוש {
			תהליךtable[i] = תהליךentry{
				בשימוש:		true,
				מזההתהליך:	מזההתהליך,
				parent:		Cנוכחיparentמזההתהליך(),
				תכניתbreak:	משתמשheapbase,
			}
			initializeתהליךfds(&תהליךtable[i])
			return &תהליךtable[i]
		}
	}
	return nil
}

func getפתחקובץfor(תהליך *תהליךentry, מזהה int32) *פתחקובץתיאור {
	if תהליך == nil || מזהה < 0 || מזהה >= מקסימוםמזהה || !תהליך.fds[מזהה].בשימוש {
		return nil
	}
	תיאור := תהליך.fds[מזהה].תיאור
	if תיאור < 0 || תיאור >= מקסימוםפתחקבצים || !פתחקובץtable[תיאור].בשימוש {
		return nil
	}
	return &פתחקובץtable[תיאור]
}

func getפתחקובץ(מזהה int32) *פתחקובץתיאור {
	return getפתחקובץfor(ensureנוכחיתהליך(), מזהה)
}

func allocateפתחקובץ() int32 {
	for i := int32(3); i < מקסימוםפתחקבצים; i++ {
		if !פתחקובץtable[i].בשימוש {
			פתחקובץtable[i] = פתחקובץתיאור{בשימוש: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateמזהה(תהליך *תהליךentry, תיאור int32, מזערי int32) int32 {
	if תהליך == nil {
		return Enfile
	}
	if מזערי < 0 || מזערי >= מקסימוםמזהה {
		return Einval
	}
	for מזהה := מזערי; מזהה < מקסימוםמזהה; מזהה++ {
		if !תהליך.fds[מזהה].בשימוש {
			תהליך.fds[מזהה] = מזההentry{בשימוש: true, תיאור: תיאור}
			return מזהה
		}
	}
	return Emfile
}

func releaseפתחקובץ(תיאור int32) {
	if תיאור < 0 || תיאור >= מקסימוםפתחקבצים {
		return
	}
	entry := &פתחקובץtable[תיאור]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && תיאור > stderrמזהה {
		if entry.סוג == מזההסוגשקע && entry.aux < מקסימוםsockets {
			מקומיsockets[entry.aux] = מקומיdatagramשקע{}
		}
		*entry = פתחקובץתיאור{}
	}
}

func סגורתהליךמזהה(תהליך *תהליךentry, מזהה int32) int32 {
	if תהליך == nil || getפתחקובץfor(תהליך, מזהה) == nil {
		return Ebadf
	}
	תיאור := תהליך.fds[מזהה].תיאור
	תהליך.fds[מזהה] = מזההentry{}
	releaseפתחקובץ(תיאור)
	return 0
}

func sysכתיבה(מזהה int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getפתחקובץ(מזהה)
	if entry == nil {
		return Ebadf
	}
	if entry.סוג != מזההסוגconsole {
		if entry.סוג == מזההסוגשקע {
			return שקעשלחto(מזהה, address, count, 0, 0)
		}
		if entry.סוג == מזההסוגfat || entry.סוג == מזההסוגשורשספרייה {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getבתיםfromסמן(uintptr(address), int(count), int(count))
	console_2.Mהדפסה(buffer)
	return int32(count)
}

func sysקריאה(מזהה int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getפתחקובץ(מזהה)
	if entry == nil {
		return Ebadf
	}
	if entry.סוג == מזההסוגstdin {
		return קריאהstdin(address, count)
	}
	if entry.סוג == מזההסוגשורשספרייה {
		return Eisdir
	}
	if entry.סוג == מזההסוגשקע {
		return שקעreceivefrom(מזהה, address, count, 0, 0)
	}
	if entry.סוג != מזההסוגfat {
		return Ebadf
	}
	if entry.מיקום >= entry.גודל {
		return 0
	}
	remaining := entry.גודל - entry.מיקום
	if count > remaining {
		count = remaining
	}
	buffer := Getבתיםfromסמן(uintptr(address), int(count), int(count))
	return קריאהvfsקובץ(entry, buffer, count)
}

func sysפתח(נתיבaddress uint32, דגלים uint32, מצב uint32) int32 {
	_ = מצב
	if נתיבaddress == 0 {
		return Efault
	}
	גישהמצב := דגלים & 3
	if גישהמצב == oכתיבהonly || גישהמצב == oקריאהכתיבה || (דגלים&(ocreate|oקיצוץ|oappend)) != 0 {
		return Erofs
	}

	תהליך := ensureנוכחיתהליך()
	if תהליך == nil {
		return Enfile
	}
	תיאור := allocateפתחקובץ()
	if תיאור < 0 {
		return תיאור
	}
	entry := &פתחקובץtable[תיאור]
	entry.דגלים = דגלים
	if isשורשנתיב(נתיבaddress) {
		entry.סוג = מזההסוגשורשספרייה
		entry.גודל = 0
	} else {
		שםlen, שם := העתקנתיב(נתיבaddress)
		if שםlen == 0 {
			*entry = פתחקובץתיאור{}
			return Enoent
		}
		גודל := קובץגודל(שם[:שםlen])
		if גודל == 0 {
			*entry = פתחקובץתיאור{}
			return Enoent
		}
		if (דגלים & oספרייה) != 0 {
			*entry = פתחקובץתיאור{}
			return Enotdir
		}
		entry.סוג = מזההסוגfat
		entry.גודל = גודל
		entry.שםlen = שםlen
		entry.שם = שם
	}

	מזהה := allocateמזהה(תהליך, תיאור, 3)
	if מזהה < 0 {
		*entry = פתחקובץתיאור{}
		return מזהה
	}
	return מזהה
}

func sysסגור(מזהה int32) int32 {
	return סגורתהליךמזהה(ensureנוכחיתהליך(), מזהה)
}

func sysdup(מזהה int32, מזערי int32) int32 {
	תהליך := ensureנוכחיתהליך()
	entry := getפתחקובץfor(תהליך, מזהה)
	if entry == nil {
		return Ebadf
	}
	חדשמזהה := allocateמזהה(תהליך, תהליך.fds[מזהה].תיאור, מזערי)
	if חדשמזהה >= 0 {
		entry.refs++
	}
	return חדשמזהה
}

func sysdup2(oldמזהה int32, חדשמזהה int32) int32 {
	תהליך := ensureנוכחיתהליך()
	entry := getפתחקובץfor(תהליך, oldמזהה)
	if entry == nil {
		return Ebadf
	}
	if חדשמזהה < 0 || חדשמזהה >= מקסימוםמזהה {
		return Ebadf
	}
	if oldמזהה == חדשמזהה {
		return חדשמזהה
	}
	if תהליך.fds[חדשמזהה].בשימוש {
		סגורתהליךמזהה(תהליך, חדשמזהה)
	}
	תהליך.fds[חדשמזהה] = מזההentry{בשימוש: true, תיאור: תהליך.fds[oldמזהה].תיאור}
	entry.refs++
	return חדשמזהה
}

func sysfcntl(מזהה int32, פקודה uint32, argument uint32) int32 {
	תהליך := ensureנוכחיתהליך()
	entry := getפתחקובץfor(תהליך, מזהה)
	if entry == nil {
		return Ebadf
	}
	switch פקודה {
	case fdupמזהה:
		return sysdup(מזהה, int32(argument))
	case fgetמזהה:
		return int32(תהליך.fds[מזהה].מזההדגלים)
	case fקבעמזהה:
		תהליך.fds[מזהה].מזההדגלים = argument & מזההcloexec
		return 0
	case fgetfl:
		return int32(entry.דגלים)
	case fקבעfl:
		entry.דגלים = (entry.דגלים & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(מזהה int32, offset int32, whence uint32) int32 {
	entry := getפתחקובץ(מזהה)
	if entry == nil {
		return Ebadf
	}
	if entry.סוג != מזההסוגfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekקבע:
		base = 0
	case seekנוכחי:
		base = int64(entry.מיקום)
	case seekסיום:
		base = int64(entry.גודל)
	default:
		return Einval
	}
	מיקום_2 := base + int64(offset)
	if מיקום_2 < 0 || מיקום_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.מיקום = uint32(מיקום_2)
	return int32(entry.מיקום)
}

func קריאהvfsקובץ(entry *פתחקובץתיאור, יעד_2 []byte, count uint32) int32 {
	זיכרוןmanager := &mem.Tזיכרוןmanager{}
	tmpסמן := זיכרוןmanager.Malloc(entry.גודל)
	if tmpסמן == nil {
		return Einval
	}
	tmp := Getבתיםfromסמן(uintptr(tmpסמן), int(entry.גודל), int(entry.גודל))
	קריאהקובץ(entry.שם[:entry.שםlen], tmp)
	copy(יעד_2[:count], tmp[entry.מיקום:entry.מיקום+count])
	entry.מיקום += count
	זיכרוןmanager.Fפנוי(tmpסמן)
	return int32(count)
}

func isשורשנתיב(נתיבaddress uint32) bool {
	if נתיבaddress == 0 {
		return false
	}
	נתיב := Getבתיםfromסמן(uintptr(נתיבaddress), 4, 4)
	if נתיב[0] == '/' && נתיב[1] == 0 {
		return true
	}
	if נתיב[0] == '.' && נתיב[1] == 0 {
		return true
	}
	if נתיב[0] == '/' && נתיב[1] == '.' && נתיב[2] == 0 {
		return true
	}
	return false
}

func sysגישה(נתיבaddress uint32, מצב uint32) int32 {
	if נתיבaddress == 0 {
		return Efault
	}
	if (מצב & ^uint32(7)) != 0 {
		return Einval
	}
	isשורש := isשורשנתיב(נתיבaddress)
	exists := isשורש
	if !exists {
		שםlen, שם := העתקנתיב(נתיבaddress)
		exists = שםlen != 0 && קובץגודל(שם[:שםlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (מצב & 2) != 0 {
		return Eacces
	}

	if (מצב&1) != 0 && !isשורש {
		return Eacces
	}
	return 0
}

func syschdir(נתיבaddress uint32) int32 {
	if נתיבaddress == 0 {
		return Efault
	}
	if !isשורשנתיב(נתיבaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, גודל uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if גודל < 2 {
		return Erange
	}
	buffer_2 := Getבתיםfromסמן(uintptr(bufferaddress), int(גודל), int(גודל))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, מצב uint32, גודל uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dהתקן = 1
	stat.Ino = inode
	stat.Mמצב = מצב
	stat.Nlink = 1
	stat.Sגודל_2 = int32(גודל)
	stat.Blksize = 512
	stat.Bבלוק = int32((גודל + 511) / 512)
	return 0
}

func sysstat(נתיבaddress uint32, stataddress uint32) int32 {
	if נתיבaddress == 0 {
		return Efault
	}
	if isשורשנתיב(נתיבaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	שםlen, שם := העתקנתיב(נתיבaddress)
	if שםlen == 0 {
		return Enoent
	}
	גודל := קובץגודל(שם[:שםlen])
	if גודל == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < שםlen; i++ {
		inode = inode*33 + uint32(שם[i])
	}
	return fillposixstat(stataddress, sifreg|0444, גודל, inode)
}

func sysfstat(מזהה int32, stataddress uint32) int32 {
	entry := getפתחקובץ(מזהה)
	if entry == nil {
		return Ebadf
	}
	switch entry.סוג {
	case מזההסוגstdin, מזההסוגconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(מזהה+1))
	case מזההסוגשורשספרייה:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case מזההסוגfat:
		return fillposixstat(stataddress, sifreg|0444, entry.גודל, uint32(מזהה+2))
	case מזההסוגשקע:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(מזהה+2))
	}
	return Ebadf
}

func sysfsync(מזהה int32) int32 {
	if getפתחקובץ(מזהה) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	תהליך := ensureנוכחיתהליך()
	if תהליך == nil {
		return 0
	}
	if תהליך.תכניתbreak == 0 {
		תהליך.תכניתbreak = משתמשheapbase
	}
	if address_2 == 0 {
		return תהליך.תכניתbreak
	}
	if address_2 < משתמשheapbase || address_2 > משתמשheaplimit {
		return תהליך.תכניתbreak
	}
	תהליך.תכניתbreak = address_2
	return תהליך.תכניתbreak
}

func העתקutsfield(יעד *[65]byte, ערך string) {
	limit := len(ערך)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		יעד[i] = ערך[i]
	}
	יעד[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	שם := (*posixutsname)(Pointer(uintptr(address_2)))
	*שם = posixutsname{}
	העתקutsfield(&שם.Sysname, "EngOS")
	העתקutsfield(&שם.Nodename, "engos")
	העתקutsfield(&שם.Release, "0.1-posix")
	העתקutsfield(&שם.Vגרסה, "POSIX.1-2017 phase 1")
	העתקutsfield(&שם.Machine, "i386")
	return 0
}

func תחלופהunsignedinteger16(ערך uint16) uint16 {
	return (ערך << 8) | (ערך >> 8)
}

func שקעcallargument(ארגומנטים_2 uint32, מפתח uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ארגומנטים_2 + מפתח*4)))
}

func שקעforמזהה(מזהה int32) (*מקומיdatagramשקע, int32) {
	entry := getפתחקובץ(מזהה)
	if entry == nil || entry.סוג != מזההסוגשקע || entry.aux >= מקסימוםsockets {
		return nil, Ebadf
	}
	שקע := &מקומיsockets[entry.aux]
	if !שקע.בשימוש {
		return nil, Ebadf
	}
	return שקע, 0
}

func allocateשקע(מתחם uint32, שקעסוג uint32, protocol uint32) int32 {
	if מתחם != afinet {
		return Eafnosupport
	}
	if שקעסוג != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	תהליך := ensureנוכחיתהליך()
	if תהליך == nil {
		return Enfile
	}
	שקעמפתח := -1
	for i := 0; i < מקסימוםsockets; i++ {
		if !מקומיsockets[i].בשימוש {
			שקעמפתח = i
			break
		}
	}
	if שקעמפתח < 0 {
		return Enfile
	}
	תיאור := allocateפתחקובץ()
	if תיאור < 0 {
		return תיאור
	}
	מקומיsockets[שקעמפתח] = מקומיdatagramשקע{בשימוש: true}
	entry := &פתחקובץtable[תיאור]
	entry.סוג = מזההסוגשקע
	entry.דגלים = oקריאהכתיבה
	entry.aux = uint32(שקעמפתח)
	מזהה := allocateמזהה(תהליך, תיאור, 3)
	if מזהה < 0 {
		מקומיsockets[שקעמפתח] = מקומיdatagramשקע{}
		*entry = פתחקובץתיאור{}
		return מזהה
	}
	return מזהה
}

func שקעaddress(address_2 uint32, אורך uint32) (*שקעaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if אורך < 16 {
		return nil, Einval
	}
	result := (*שקעaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func שערנכנסuse(שער uint16, except *מקומיdatagramשקע) bool {
	for i := 0; i < מקסימוםsockets; i++ {
		שקע := &מקומיsockets[i]
		if שקע != except && שקע.בשימוש && שקע.bound && שקע.מקומי.Pשער == שער {
			return true
		}
	}
	return false
}

func bindephemeral(שקע *מקומיdatagramשקע) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		שער := תחלופהunsignedinteger16(הבאephemeralשער)
		הבאephemeralשער++
		if הבאephemeralשער < 49152 {
			הבאephemeralשער = 49152
		}
		if !שערנכנסuse(שער, שקע) {
			שקע.מקומי = שקעaddressipv4{Family: afinet, Pשער: שער, Address: 0x0100007F}
			שקע.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func שקעbind(מזהה int32, address_2 uint32, אורך uint32) int32 {
	שקע, שגיאה := שקעforמזהה(מזהה)
	if שגיאה != 0 {
		return שגיאה
	}
	requested, שגיאה := שקעaddress(address_2, אורך)
	if שגיאה != 0 {
		return שגיאה
	}
	if שקע.bound {
		return Einval
	}
	if requested.Pשער == 0 {
		return bindephemeral(שקע)
	}
	if שערנכנסuse(requested.Pשער, שקע) {
		return Eaddrinuse
	}
	שקע.מקומי = *requested
	שקע.bound = true
	return 0
}

func שקעחיבור(מזהה int32, address_2 uint32, אורך uint32) int32 {
	שקע, שגיאה := שקעforמזהה(מזהה)
	if שגיאה != 0 {
		return שגיאה
	}
	מרוחק, שגיאה := שקעaddress(address_2, אורך)
	if שגיאה != 0 {
		return שגיאה
	}
	if !שקע.bound {
		if שגיאה := bindephemeral(שקע); שגיאה != 0 {
			return שגיאה
		}
	}
	שקע.מרוחק = *מרוחק
	שקע.connected = true
	return 0
}

func שקעשלחto(מזהה int32, bufferaddress_2 uint32, אורך uint32, יעדaddress uint32, יעדאורך uint32) int32 {
	שקע, שגיאה := שקעforמזהה(מזהה)
	if שגיאה != 0 {
		return שגיאה
	}
	if אורך > מקסימוםdatagramגודל {
		return Emsgsize
	}
	if אורך != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var יעד שקעaddressipv4
	if יעדaddress != 0 {
		address_2, addressשגיאה := שקעaddress(יעדaddress, יעדאורך)
		if addressשגיאה != 0 {
			return addressשגיאה
		}
		יעד = *address_2
	} else {
		if !שקע.connected {
			return Enotconn
		}
		יעד = שקע.מרוחק
	}
	if !שקע.bound {
		if bindשגיאה := bindephemeral(שקע); bindשגיאה != 0 {
			return bindשגיאה
		}
	}
	var receiver *מקומיdatagramשקע
	for i := 0; i < מקסימוםsockets; i++ {
		candidate := &מקומיsockets[i]
		if candidate.בשימוש && candidate.bound && candidate.מקומי.Pשער == יעד.Pשער &&
			(candidate.מקומי.Address == 0 || candidate.מקומי.Address == יעד.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= מקסימוםשקעמנותנתונים {
		return Eagain
	}
	packet := &receiver.מנותנתונים[receiver.tail]
	*packet = שקעpacket{בשימוש: true, גודל: אורך, מקור: שקע.מקומי}
	if אורך != 0 {
		מקור := Getבתיםfromסמן(uintptr(bufferaddress_2), int(אורך), int(אורך))
		copy(packet.data[:אורך], מקור)
	}
	receiver.tail = (receiver.tail + 1) % מקסימוםשקעמנותנתונים
	receiver.count++
	return int32(אורך)
}

func שקעreceivefrom(מזהה int32, bufferaddress_2 uint32, אורך uint32, מקורaddress uint32, מקוראורךaddress uint32) int32 {
	שקע, שגיאה := שקעforמזהה(מזהה)
	if שגיאה != 0 {
		return שגיאה
	}
	if אורך != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if שקע.count == 0 {
		return Eagain
	}
	packet := &שקע.מנותנתונים[שקע.head]
	העתקאורך := packet.גודל
	if העתקאורך > אורך {
		העתקאורך = אורך
	}
	if העתקאורך != 0 {
		יעד := Getבתיםfromסמן(uintptr(bufferaddress_2), int(העתקאורך), int(העתקאורך))
		copy(יעד, packet.data[:העתקאורך])
	}
	if מקורaddress != 0 {
		if מקוראורךaddress == 0 {
			return Efault
		}
		providedאורך := (*uint32)(Pointer(uintptr(מקוראורךaddress)))
		if *providedאורך >= 16 {
			*(*שקעaddressipv4)(Pointer(uintptr(מקורaddress))) = packet.מקור
		}
		*providedאורך = 16
	}
	*packet = שקעpacket{}
	שקע.head = (שקע.head + 1) % מקסימוםשקעמנותנתונים
	שקע.count--
	return int32(העתקאורך)
}

func העתקשקעשם(מזהה int32, address_2 uint32, אורךaddress uint32, peer bool) int32 {
	שקע, שגיאה := שקעforמזהה(מזהה)
	if שגיאה != 0 {
		return שגיאה
	}
	if address_2 == 0 || אורךaddress == 0 {
		return Efault
	}
	אורך := (*uint32)(Pointer(uintptr(אורךaddress)))
	if *אורך < 16 {
		*אורך = 16
		return Einval
	}
	if peer {
		if !שקע.connected {
			return Enotconn
		}
		*(*שקעaddressipv4)(Pointer(uintptr(address_2))) = שקע.מרוחק
	} else {
		if !שקע.bound {
			if bindשגיאה := bindephemeral(שקע); bindשגיאה != 0 {
				return bindשגיאה
			}
		}
		*(*שקעaddressipv4)(Pointer(uintptr(address_2))) = שקע.מקומי
	}
	*אורך = 16
	return 0
}

func sysשקעcall(call uint32, ארגומנטים_2 uint32) int32 {
	if ארגומנטים_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateשקע(שקעcallargument(ארגומנטים_2, 0), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2))
	case 2:
		return שקעbind(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2))
	case 3:
		return שקעחיבור(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return העתקשקעשם(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), false)
	case 7:
		return העתקשקעשם(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), true)
	case 9:
		return שקעשלחto(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), 0, 0)
	case 10:
		return שקעreceivefrom(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), 0, 0)
	case 11:
		return שקעשלחto(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), שקעcallargument(ארגומנטים_2, 4), שקעcallargument(ארגומנטים_2, 5))
	case 12:
		return שקעreceivefrom(int32(שקעcallargument(ארגומנטים_2, 0)), שקעcallargument(ארגומנטים_2, 1), שקעcallargument(ארגומנטים_2, 2), שקעcallargument(ארגומנטים_2, 4), שקעcallargument(ארגומנטים_2, 5))
	case 13:
		if _, שגיאה := שקעforמזהה(int32(שקעcallargument(ארגומנטים_2, 0))); שגיאה != 0 {
			return שגיאה
		}
		return 0
	case 14:
		if _, שגיאה := שקעforמזהה(int32(שקעcallargument(ארגומנטים_2, 0))); שגיאה != 0 {
			return שגיאה
		}
		return 0
	}
	return Eopnotsupp
}

func קריאהstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getבתיםfromסמן(uintptr(address), int(count), int(count))
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
	הבא := (stdinכתיבה + 1) % uint32(len(stdinbuffer))
	if הבא == stdinקריאה {
		return
	}
	stdinbuffer[stdinכתיבה] = c
	stdinכתיבה = הבא
}

func stdingetblocking() byte {
	for stdinקריאה == stdinכתיבה {
		sc := pollמקלדתscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinקריאה]
	stdinקריאה = (stdinקריאה + 1) % uint32(len(stdinbuffer))
	return c
}

func pollמקלדתscancode() byte {
	for (Pשערקריאהbyte(0x64) & 0x01) == 0 {
	}
	sc := Pשערקריאהbyte(0x60)
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

func העתקהפעלהvector(address_2 uint32, result *הפעלהvector) int32 {
	*result = הפעלהvector{}
	if address_2 == 0 {
		return 0
	}
	for מפתח := uint32(0); מפתח < מקסימוםהפעלהvectorentry; מפתח++ {
		מחרוזתaddress := *(*uint32)(Pointer(uintptr(address_2 + מפתח*4)))
		if מחרוזתaddress == 0 {
			result.count = מפתח
			return 0
		}
		terminated := false
		for אורך := uint32(0); אורך <= מקסימוםהפעלהמחרוזתאורך; אורך++ {
			ערך := *(*byte)(Pointer(uintptr(מחרוזתaddress + אורך)))
			result.ערכים[מפתח][אורך] = ערך
			if ערך == 0 {
				result.lengths[מפתח] = אורך
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

func pushהפעלהunsignedinteger32(stack *uint32, ערך uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = ערך
}

func setupהפעלהstack(מעבד *Tcpuמצב, ארגומנטים_2 *הפעלהvector, environment *הפעלהvector) int32 {
	const stackבתים uint32 = 4096
	if !Makerangeפרטיwritable(getcr3(), Uמשתמשstackמלמעלה-stackבתים, stackבתים) {
		return Enomem
	}
	stack := Uמשתמשstackמלמעלה
	var argumentpointers [מקסימוםהפעלהvectorentry]uint32
	var environmentpointers [מקסימוםהפעלהvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		אורך := environment.lengths[i] + 1
		stack -= אורך
		יעד := Getבתיםfromסמן(uintptr(stack), int(אורך), int(אורך))
		copy(יעד, environment.ערכים[i][:אורך])
		environmentpointers[i] = stack
	}
	for i := int(ארגומנטים_2.count) - 1; i >= 0; i-- {
		אורך := ארגומנטים_2.lengths[i] + 1
		stack -= אורך
		יעד := Getבתיםfromסמן(uintptr(stack), int(אורך), int(אורך))
		copy(יעד, ארגומנטים_2.ערכים[i][:אורך])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushהפעלהunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushהפעלהunsignedinteger32(&stack, environmentpointers[i])
	}
	pushהפעלהunsignedinteger32(&stack, 0)
	for i := int(ארגומנטים_2.count) - 1; i >= 0; i-- {
		pushהפעלהunsignedinteger32(&stack, argumentpointers[i])
	}
	pushהפעלהunsignedinteger32(&stack, ארגומנטים_2.count)
	מעבד.Esp = stack
	מעבד.Ebp = 0
	return 0
}

func סגורפעילהפעלה(תהליך *תהליךentry) {
	if תהליך == nil {
		return
	}
	for מזהה := int32(0); מזהה < מקסימוםמזהה; מזהה++ {
		if תהליך.fds[מזהה].בשימוש && (תהליך.fds[מזהה].מזההדגלים&מזההcloexec) != 0 {
			סגורתהליךמזהה(תהליך, מזהה)
		}
	}
}

func sysexecve(מעבד *Tcpuמצב, נתיבaddress uint32) int32 {
	if נתיבaddress == 0 {
		return Efault
	}
	var ארגומנטים_2 הפעלהvector
	var environment הפעלהvector
	if result := העתקהפעלהvector(מעבד.Ecx, &ארגומנטים_2); result < 0 {
		return result
	}
	if result := העתקהפעלהvector(מעבד.Edx, &environment); result < 0 {
		return result
	}
	שםlen, שם := העתקנתיב(נתיבaddress)
	if שםlen == 0 {
		return Enoent
	}
	גודל := קובץגודל(שם[:שםlen])
	if גודל == 0 {
		return Enoent
	}
	זיכרוןmanager := &mem.Tזיכרוןmanager{}
	קובץסמן := זיכרוןmanager.Malloc(גודל)
	if קובץסמן == nil {
		return Einval
	}
	data := Getבתיםfromסמן(uintptr(קובץסמן), int(גודל), int(גודל))
	קריאהקובץ(שם[:שםlen], data)
	if גודל < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		זיכרוןmanager.Fפנוי(קובץסמן)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	זיכרוןmanager.Fפנוי(קובץסמן)
	if result := setupהפעלהstack(מעבד, &ארגומנטים_2, &environment); result < 0 {
		return result
	}
	סגורפעילהפעלה(ensureנוכחיתהליך())
	מעבד.Eip = entry
	מעבד.Eax = 0
	return 0
}

func sysfork(מעבד *Tcpuמצב) int32 {
	parentמזההתהליך := Cנוכחימזההתהליך()
	if ensureנוכחיתהליך() == nil {
		return Enfile
	}
	מזההתהליך := allocateתהליך(parentמזההתהליך)
	if מזההתהליך == 0 {
		return Einval
	}
	זיכרוןmanager := &mem.Tזיכרוןmanager{}
	threadסמן := זיכרוןmanager.Malloc(uint32(Sizeof(TThread{})))
	stackסמן := זיכרוןmanager.Malloc(Threadstackגודל)
	childעמודספרייה := Cloneaddressרווחcow(getcr3())
	if threadסמן == nil || stackסמן == nil || childעמודספרייה == 0 {
		שכחתהליך(מזההתהליך)
		return Einval
	}
	child := (*TThread)(threadסמן)
	child.Stack = uint32(uintptr(stackסמן))
	child.Cמעבדמצב = (*Tcpuמצב)(Pointer(uintptr(stackסמן) + Threadstackגודל - Sizeof(Tcpuמצב{})))
	*child.Cמעבדמצב = *מעבד
	child.Cמעבדמצב.Eax = 0
	child.Uמשתמשstack_2 = מעבד.Esp
	child.Uמשתמשstackגודל_2 = 0
	child.Pמזההתהליך = מזההתהליך
	child.Parentמזההתהליך = parentמזההתהליך
	child.Pעמודספרייהentry = childעמודספרייה
	child.Threadמצב = Rמוכן
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Aהוספהrunnablethread(child)
	return int32(מזההתהליך)
}

func sysיציאה(מצב_2 uint32) {
	מזההתהליך := Cנוכחימזההתהליך()
	for i := 0; i < len(תהליךtable); i++ {
		if תהליךtable[i].בשימוש && תהליךtable[i].מזההתהליך == מזההתהליך {
			סגורהכלתהליךfds(&תהליךtable[i])
			תהליךtable[i].exited = true
			תהליךtable[i].מצב_2 = (מצב_2 & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(מזההתהליך int32, מצבaddress uint32, אפשרויות uint32) int32 {
	if (אפשרויות & ^uint32(1)) != 0 {
		return Einval
	}
	parentמזההתהליך := Cנוכחימזההתהליך()
	foundchild := false
	for i := 0; i < len(תהליךtable); i++ {
		p := &תהליךtable[i]
		matches := מזההתהליך == -1 || מזההתהליך == 0 || p.מזההתהליך == uint32(מזההתהליך)
		if p.בשימוש && matches && p.parent == parentמזההתהליך {
			foundchild = true
			if p.exited {
				if מצבaddress != 0 {
					*(*uint32)(Pointer(uintptr(מצבaddress))) = p.מצב_2
				}
				childמזההתהליך := p.מזההתהליך
				*p = תהליךentry{}
				return int32(childמזההתהליך)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (אפשרויות & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateתהליך(parent uint32) uint32 {
	parentתהליך := חיפושתהליך(parent)
	מזההתהליך := Allocateמזההתהליך()
	for i := 0; i < len(תהליךtable); i++ {
		if !תהליךtable[i].בשימוש {
			תהליךtable[i] = תהליךentry{
				בשימוש:		true,
				מזההתהליך:	מזההתהליך,
				parent:		parent,
				תכניתbreak:	משתמשheapbase,
			}
			if parentתהליך != nil {
				תהליךtable[i].תכניתbreak = parentתהליך.תכניתbreak
				for מזהה := 0; מזהה < מקסימוםמזהה; מזהה++ {
					if parentתהליך.fds[מזהה].בשימוש {
						תהליךtable[i].fds[מזהה] = parentתהליך.fds[מזהה]
						תיאור := parentתהליך.fds[מזהה].תיאור
						if תיאור >= 0 && תיאור < מקסימוםפתחקבצים {
							פתחקובץtable[תיאור].refs++
						}
					}
				}
			} else {
				initializeתהליךfds(&תהליךtable[i])
			}
			return מזההתהליך
		}
	}
	return 0
}

func סגורהכלתהליךfds(תהליך *תהליךentry) {
	if תהליך == nil {
		return
	}
	for מזהה := int32(0); מזהה < מקסימוםמזהה; מזהה++ {
		if תהליך.fds[מזהה].בשימוש {
			סגורתהליךמזהה(תהליך, מזהה)
		}
	}
}

func שכחתהליך(מזההתהליך uint32) {
	תהליך := חיפושתהליך(מזההתהליך)
	if תהליך == nil {
		return
	}
	סגורהכלתהליךfds(תהליך)
	*תהליך = תהליךentry{}
}

func העתקנתיב(נתיבaddress uint32) (uint32, [12]byte) {
	var שם [12]byte
	if נתיבaddress == 0 {
		return 0, שם
	}
	raw := Getבתיםfromסמן(uintptr(נתיבaddress), 64, 64)
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
		שם[n] = c
		n++
	}
	return n, שם
}

func קובץגודל(שםהקובץ []byte) uint32 {
	var ata0s = Tמתקדםטכנולוגיהattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Rקריאהpartition(&ata0s)

	bios := TBiosparameterבלוק32{}
	גודל := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ)
	ata0s.Flush()
	return גודל
}

func קריאהקובץ(שםהקובץ []byte, data []byte) {
	var ata0s = Tמתקדםטכנולוגיהattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Rקריאהpartition(&ata0s)

	bios := TBiosparameterבלוק32{}
	bios.Rקריאה(&ata0s, partition.Mbr.Primarypartition[0], שםהקובץ, data)
	ata0s.Flush()
}

func getcr3() uint32
