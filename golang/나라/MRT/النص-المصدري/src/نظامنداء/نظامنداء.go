package نظامنداء

import . "unsafe"

import . "مقاطعة"
import . "طرفية"
import . "أداة"
import . "متعددإدارةمهام"
import . "مشغل/ata"
import . "ملفنظام/msdosتجزئة"
import . "ملفنظام/fat"
import . "ملفنظام/صيغة_التنفيذ_والربط"
import mem "ذاكرةمدير"
import . "إدارةصفحات"
import . "منفذ"
import . "إدارةمهام/مجدول"
import . "إدارةمهام/خيطتنفيذ"
import . "افتراضيذاكرة"

var طرفية_2 = Tطرفية{}

type TSyscall struct {
	Tمقاطعةhandler
}

const (
	Sysخروج		uint32	= 1
	Sysfork		uint32	= 2
	Sysقراءة	uint32	= 3
	Sysكتابة	uint32	= 4
	Sysفتح		uint32	= 5
	Sysإغلاق	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysنفاذ		uint32	= 33
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
	Sysrtخروج	uint32	= 252

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
	أقصىfd			= 32
	أقصىفتحملفات		= 128
)

type fdentry struct {
	used		bool
	الوصف		int32
	fdخيارات	uint32
}

type فتحملفالوصف struct {
	used		bool
	refs		uint32
	kind		uint32
	خيارات		uint32
	الموضع		uint32
	الحجم		uint32
	الاسم		[12]byte
	الاسمlen	uint32
	aux		uint32
}

const (
	fdkindلاشيء	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindطرفية	uint32	= 3
	fdkindالجذردليل	uint32	= 4
	fdkindمقبس	uint32	= 5

	oقراءةفقط	uint32	= 0
	oكتابةفقط	uint32	= 1
	oقراءةكتابة	uint32	= 2
	oإنشاء		uint32	= 0x40
	oناقص		uint32	= 0x200
	oappend		uint32	= 0x400
	oدليل		uint32	= 0x10000

	seekتحديد	uint32	= 0
	seekالحالي	uint32	= 1
	seekنهاية	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fتحديدfd	uint32	= 2
	fgetfl		uint32	= 3
	fتحديدfl	uint32	= 4
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
	ipالبروتوكولudp		= 17
	أقصىsockets		= 32
	أقصىمقبسpackets		= 8
	أقصىdatagramالحجم	= 512
)

type مقبسaddressiالقيمةالحالية4 struct {
	Family	uint16
	Pمنفذ	uint16
	Address	uint32
	Zero	[8]byte
}

type مقبسpacket struct {
	used	bool
	الحجم	uint32
	المصدر	مقبسaddressiالقيمةالحالية4
	بيانات	[أقصىdatagramالحجم]byte
}

type محليdatagramمقبس struct {
	used		bool
	bound		bool
	connected	bool
	محلي		مقبسaddressiالقيمةالحالية4
	البعيد		مقبسaddressiالقيمةالحالية4
	head		uint32
	tail		uint32
	count		uint32
	packets		[أقصىمقبسpackets]مقبسpacket
}

type posixstat struct {
	Dالجهاز		uint32
	Ino		uint32
	Mوضع		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sالحجم_2	int32
	Blksize		int32
	Bحظر		int32
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
	Vإصدار		[65]byte
	Machine		[65]byte
}

const (
	أقصىexecvectorentry	= 16
	أقصىexecسلسلةالمدة	= 63
)

type execvector struct {
	count	uint32
	lengths	[أقصىexecvectorentry]uint32
	قيم	[أقصىexecvectorentry][أقصىexecسلسلةالمدة + 1]byte
}

type عمليةentry struct {
	used		bool
	الهوية_2	uint32
	أب		uint32
	exited		bool
	الحالة		uint32
	برنامجbreak	uint32
	fds		[أقصىfd]fdentry
}

type سلسلةترويسة struct {
	Data	uintptr
	Len	int
}

func syscallخطأ(خطأ int32) uint32 {
	return *(*uint32)(Pointer(&خطأ))
}

var فتحملفجدول [أقصىفتحملفات]فتحملفالوصف
var عمليةجدول [32]عمليةentry
var محليsockets [أقصىsockets]محليdatagramمقبس
var التاليephemeralمنفذ uint16 = 49152

const (
	مستخدمheapbase	uint32	= 0x06000000
	مستخدمheapتحديد	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinقراءة uint32
var stdinكتابة uint32

func Iمقاطعة(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysخروج_2(فهرس uint32) {
	Syscall(Sysخروج, فهرس)
}

func Sysقراءة_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysقراءة, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysاطبعstr(buffer string) {
	h := (*سلسلةترويسة)(Pointer(&buffer))
	Syscall(Sysكتابة, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysاطبعunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysكتابة, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysفتح_2(مسار uintptr, خيارات uint32, وضع uint32) int32 {
	return int32(Syscall(Sysفتح, uint32(مسار), خيارات, وضع))
}

func Sysإغلاق_2(fd uint32) int32 {
	return int32(Syscall(Sysإغلاق, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(المعاملات ...uint32) uint32 {

	l := len(المعاملات)
	switch l {
	case 1:
		return Iمقاطعة(المعاملات[0], 0, 0, 0, 0, 0)
	case 2:
		return Iمقاطعة(المعاملات[0], المعاملات[1], 0, 0, 0, 0)
	case 3:
		return Iمقاطعة(المعاملات[0], المعاملات[1], المعاملات[2], 0, 0, 0)
	case 4:
		return Iمقاطعة(المعاملات[0], المعاملات[1], المعاملات[2], المعاملات[3], 0, 0)
	case 5:
		return Iمقاطعة(المعاملات[0], المعاملات[1], المعاملات[2], المعاملات[3], المعاملات[4], 0)
	case 6:
		return Iمقاطعة(المعاملات[0], المعاملات[1], المعاملات[2], المعاملات[3], المعاملات[4], المعاملات[5])
	default:
		return syscallخطأ(Enosys)
	}
}

func (نفسه *TSyscall) Init(مدير *Tمقاطعةمدير) {
	initملفdescriptor()

	مقاطعةhandler = التعاملمقاطعة

	var address uintptr
	address = uintptr(Pointer(&مقاطعةhandler))

	نفسه.Tمقاطعةhandler.Init(0x80, uintptr(Pointer(مدير)), address)
}

var مقاطعةhandler func(uint32) uint32

func التعاملمقاطعة(esp uint32) uint32 {
	var المعالج = (*Tcpuالحالة)(Pointer(uintptr(esp)))

	switch المعالج.Eax {
	case Sysخروج:
		sysخروج(المعالج.Ebx)
		return uint32(uintptr(Pointer(Sأوقفالحاليخيطتنفيذ(المعالج))))
	case Sysrtخروج:
		sysخروج(المعالج.Ebx)
		return uint32(uintptr(Pointer(Sأوقفالحاليخيطتنفيذ(المعالج))))
	case Sysfork:
		المعالج.Eax = uint32(sysfork(المعالج))
		return esp
	case Sysقراءة:
		المعالج.Eax = uint32(sysقراءة(int32(المعالج.Ebx), المعالج.Ecx, المعالج.Edx))
		return esp
	case Sysكتابة:
		المعالج.Eax = uint32(sysكتابة(int32(المعالج.Ebx), المعالج.Ecx, المعالج.Edx))
		return esp
	case Sysفتح:
		المعالج.Eax = uint32(sysفتح(المعالج.Ebx, المعالج.Ecx, المعالج.Edx))
		return esp
	case Syscreat:
		المعالج.Eax = uint32(sysفتح(المعالج.Ebx, oإنشاء|oكتابةفقط|oناقص, المعالج.Ecx))
		return esp
	case Sysإغلاق:
		المعالج.Eax = uint32(sysإغلاق(int32(المعالج.Ebx)))
		return esp
	case Syswaitpid:
		المعالج.Eax = uint32(syswaitpid(int32(المعالج.Ebx), المعالج.Ecx, المعالج.Edx))
		return esp
	case Syslseek:
		المعالج.Eax = uint32(syslseek(int32(المعالج.Ebx), int32(المعالج.Ecx), المعالج.Edx))
		return esp
	case Sysexecve:
		المعالج.Eax = uint32(sysexecve(المعالج, المعالج.Ebx))
		return esp
	case Sysgetpid:
		المعالج.Eax = Cالحاليالهوية()
		return esp
	case Sysgetppid:
		المعالج.Eax = Cالحاليأبالهوية()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		المعالج.Eax = 0
		return esp
	case Sysنفاذ:
		المعالج.Eax = uint32(sysنفاذ(المعالج.Ebx, المعالج.Ecx))
		return esp
	case Syschdir:
		المعالج.Eax = uint32(syschdir(المعالج.Ebx))
		return esp
	case Sysgetcwd:
		المعالج.Eax = uint32(sysgetcwd(المعالج.Ebx, المعالج.Ecx))
		return esp
	case Sysdup:
		المعالج.Eax = uint32(sysdup(int32(المعالج.Ebx), 0))
		return esp
	case Sysdup2:
		المعالج.Eax = uint32(sysdup2(int32(المعالج.Ebx), int32(المعالج.Ecx)))
		return esp
	case Syssocketcall:
		المعالج.Eax = uint32(sysمقبسنداء(المعالج.Ebx, المعالج.Ecx))
		return esp
	case Sysfcntl:
		المعالج.Eax = uint32(sysfcntl(int32(المعالج.Ebx), المعالج.Ecx, المعالج.Edx))
		return esp
	case Sysstat, Syslstat:
		المعالج.Eax = uint32(sysstat(المعالج.Ebx, المعالج.Ecx))
		return esp
	case Sysfstat:
		المعالج.Eax = uint32(sysfstat(int32(المعالج.Ebx), المعالج.Ecx))
		return esp
	case Sysfsync:
		المعالج.Eax = uint32(sysfsync(int32(المعالج.Ebx)))
		return esp
	case Syssync:
		المعالج.Eax = 0
		return esp
	case Sysuname:
		المعالج.Eax = uint32(sysuname(المعالج.Ebx))
		return esp
	case Sysbrk:
		المعالج.Eax = sysbrk(المعالج.Ebx)
		return esp
	case 9:
		طرفية_2.MUnsignedinteger32اطبع(المعالج.Ebx)
		return esp

	default:
		طرفية_2.Mاطبعxy(([]byte)("sys["), 1, 23)
		طرفية_2.MUnsignedinteger32اطبع(esp)
		طرفية_2.Mاطبع(([]byte)(":"))
		طرفية_2.MUnsignedinteger32اطبع(المعالج.Eax)
		طرفية_2.Mاطبع(([]byte)(":"))
		طرفية_2.MUnsignedinteger32اطبع(المعالج.Ebx)
		طرفية_2.Mاطبع(([]byte)(":"))
		طرفية_2.MUnsignedinteger32اطبع(المعالج.Ecx)
		طرفية_2.Mاطبع(([]byte)(":"))
		طرفية_2.MUnsignedinteger32اطبع(المعالج.Edx)
		طرفية_2.Mاطبع(([]byte)("]"))
		المعالج.Eax = syscallخطأ(Enosys)
		return esp
	}

	return esp
}

func initملفdescriptor() {
	for i := 0; i < أقصىفتحملفات; i++ {
		فتحملفجدول[i] = فتحملفالوصف{}
	}
	for i := 0; i < len(عمليةجدول); i++ {
		عمليةجدول[i] = عمليةentry{}
	}
	for i := 0; i < len(محليsockets); i++ {
		محليsockets[i] = محليdatagramمقبس{}
	}
	التاليephemeralمنفذ = 49152
	فتحملفجدول[0] = فتحملفالوصف{used: true, kind: fdkindstdin, خيارات: oقراءةفقط}
	فتحملفجدول[1] = فتحملفالوصف{used: true, kind: fdkindطرفية, خيارات: oكتابةفقط}
	فتحملفجدول[2] = فتحملفالوصف{used: true, kind: fdkindطرفية, خيارات: oكتابةفقط}
}

func ابحثعملية(الهوية_2 uint32) *عمليةentry {
	for i := 0; i < len(عمليةجدول); i++ {
		if عمليةجدول[i].used && عمليةجدول[i].الهوية_2 == الهوية_2 {
			return &عمليةجدول[i]
		}
	}
	return nil
}

func initializeعمليةfds(عملية *عمليةentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		عملية.fds[fd] = fdentry{used: true, الوصف: fd}
		فتحملفجدول[fd].refs++
	}
}

func ensureالحاليعملية() *عمليةentry {
	الهوية_2 := Cالحاليالهوية()
	if عملية := ابحثعملية(الهوية_2); عملية != nil {
		return عملية
	}
	for i := 0; i < len(عمليةجدول); i++ {
		if !عمليةجدول[i].used {
			عمليةجدول[i] = عمليةentry{
				used:		true,
				الهوية_2:	الهوية_2,
				أب:		Cالحاليأبالهوية(),
				برنامجbreak:	مستخدمheapbase,
			}
			initializeعمليةfds(&عمليةجدول[i])
			return &عمليةجدول[i]
		}
	}
	return nil
}

func getفتحملفfor(عملية *عمليةentry, fd int32) *فتحملفالوصف {
	if عملية == nil || fd < 0 || fd >= أقصىfd || !عملية.fds[fd].used {
		return nil
	}
	الوصف := عملية.fds[fd].الوصف
	if الوصف < 0 || الوصف >= أقصىفتحملفات || !فتحملفجدول[الوصف].used {
		return nil
	}
	return &فتحملفجدول[الوصف]
}

func getفتحملف(fd int32) *فتحملفالوصف {
	return getفتحملفfor(ensureالحاليعملية(), fd)
}

func allocateفتحملف() int32 {
	for i := int32(3); i < أقصىفتحملفات; i++ {
		if !فتحملفجدول[i].used {
			فتحملفجدول[i] = فتحملفالوصف{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(عملية *عمليةentry, الوصف int32, أدنى int32) int32 {
	if عملية == nil {
		return Enfile
	}
	if أدنى < 0 || أدنى >= أقصىfd {
		return Einval
	}
	for fd := أدنى; fd < أقصىfd; fd++ {
		if !عملية.fds[fd].used {
			عملية.fds[fd] = fdentry{used: true, الوصف: الوصف}
			return fd
		}
	}
	return Emfile
}

func releaseفتحملف(الوصف int32) {
	if الوصف < 0 || الوصف >= أقصىفتحملفات {
		return
	}
	entry := &فتحملفجدول[الوصف]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && الوصف > stderrfd {
		if entry.kind == fdkindمقبس && entry.aux < أقصىsockets {
			محليsockets[entry.aux] = محليdatagramمقبس{}
		}
		*entry = فتحملفالوصف{}
	}
}

func إغلاقعمليةfd(عملية *عمليةentry, fd int32) int32 {
	if عملية == nil || getفتحملفfor(عملية, fd) == nil {
		return Ebadf
	}
	الوصف := عملية.fds[fd].الوصف
	عملية.fds[fd] = fdentry{}
	releaseفتحملف(الوصف)
	return 0
}

func sysكتابة(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getفتحملف(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindطرفية {
		if entry.kind == fdkindمقبس {
			return مقبسأرسلto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindالجذردليل {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getبايتfromالمؤشر(uintptr(address), int(count), int(count))
	طرفية_2.Mاطبع(buffer)
	return int32(count)
}

func sysقراءة(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getفتحملف(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return قراءةstdin(address, count)
	}
	if entry.kind == fdkindالجذردليل {
		return Eisdir
	}
	if entry.kind == fdkindمقبس {
		return مقبسreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.الموضع >= entry.الحجم {
		return 0
	}
	remaining := entry.الحجم - entry.الموضع
	if count > remaining {
		count = remaining
	}
	buffer := Getبايتfromالمؤشر(uintptr(address), int(count), int(count))
	return قراءةvfsملف(entry, buffer, count)
}

func sysفتح(مسارaddress uint32, خيارات uint32, وضع uint32) int32 {
	_ = وضع
	if مسارaddress == 0 {
		return Efault
	}
	نفاذوضع := خيارات & 3
	if نفاذوضع == oكتابةفقط || نفاذوضع == oقراءةكتابة || (خيارات&(oإنشاء|oناقص|oappend)) != 0 {
		return Erofs
	}

	عملية := ensureالحاليعملية()
	if عملية == nil {
		return Enfile
	}
	الوصف := allocateفتحملف()
	if الوصف < 0 {
		return الوصف
	}
	entry := &فتحملفجدول[الوصف]
	entry.خيارات = خيارات
	if isالجذرمسار(مسارaddress) {
		entry.kind = fdkindالجذردليل
		entry.الحجم = 0
	} else {
		الاسمlen, الاسم := نسخمسار(مسارaddress)
		if الاسمlen == 0 {
			*entry = فتحملفالوصف{}
			return Enoent
		}
		الحجم := ملفالحجم(الاسم[:الاسمlen])
		if الحجم == 0 {
			*entry = فتحملفالوصف{}
			return Enoent
		}
		if (خيارات & oدليل) != 0 {
			*entry = فتحملفالوصف{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.الحجم = الحجم
		entry.الاسمlen = الاسمlen
		entry.الاسم = الاسم
	}

	fd := allocatefd(عملية, الوصف, 3)
	if fd < 0 {
		*entry = فتحملفالوصف{}
		return fd
	}
	return fd
}

func sysإغلاق(fd int32) int32 {
	return إغلاقعمليةfd(ensureالحاليعملية(), fd)
}

func sysdup(fd int32, أدنى int32) int32 {
	عملية := ensureالحاليعملية()
	entry := getفتحملفfor(عملية, fd)
	if entry == nil {
		return Ebadf
	}
	جديدfd := allocatefd(عملية, عملية.fds[fd].الوصف, أدنى)
	if جديدfd >= 0 {
		entry.refs++
	}
	return جديدfd
}

func sysdup2(oldfd int32, جديدfd int32) int32 {
	عملية := ensureالحاليعملية()
	entry := getفتحملفfor(عملية, oldfd)
	if entry == nil {
		return Ebadf
	}
	if جديدfd < 0 || جديدfd >= أقصىfd {
		return Ebadf
	}
	if oldfd == جديدfd {
		return جديدfd
	}
	if عملية.fds[جديدfd].used {
		إغلاقعمليةfd(عملية, جديدfd)
	}
	عملية.fds[جديدfd] = fdentry{used: true, الوصف: عملية.fds[oldfd].الوصف}
	entry.refs++
	return جديدfd
}

func sysfcntl(fd int32, أمر uint32, argument uint32) int32 {
	عملية := ensureالحاليعملية()
	entry := getفتحملفfor(عملية, fd)
	if entry == nil {
		return Ebadf
	}
	switch أمر {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(عملية.fds[fd].fdخيارات)
	case fتحديدfd:
		عملية.fds[fd].fdخيارات = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.خيارات)
	case fتحديدfl:
		entry.خيارات = (entry.خيارات & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getفتحملف(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekتحديد:
		base = 0
	case seekالحالي:
		base = int64(entry.الموضع)
	case seekنهاية:
		base = int64(entry.الحجم)
	default:
		return Einval
	}
	الموضع_2 := base + int64(offset)
	if الموضع_2 < 0 || الموضع_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.الموضع = uint32(الموضع_2)
	return int32(entry.الموضع)
}

func قراءةvfsملف(entry *فتحملفالوصف, المقصد_2 []byte, count uint32) int32 {
	ذاكرةمدير := &mem.Tذاكرةمدير{}
	tmpالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(entry.الحجم)
	if tmpالمؤشر == nil {
		return Einval
	}
	tmp := Getبايتfromالمؤشر(uintptr(tmpالمؤشر), int(entry.الحجم), int(entry.الحجم))
	قراءةملف(entry.الاسم[:entry.الاسمlen], tmp)
	copy(المقصد_2[:count], tmp[entry.الموضع:entry.الموضع+count])
	entry.الموضع += count
	ذاكرةمدير.Fخالي(tmpالمؤشر)
	return int32(count)
}

func isالجذرمسار(مسارaddress uint32) bool {
	if مسارaddress == 0 {
		return false
	}
	مسار := Getبايتfromالمؤشر(uintptr(مسارaddress), 4, 4)
	if مسار[0] == '/' && مسار[1] == 0 {
		return true
	}
	if مسار[0] == '.' && مسار[1] == 0 {
		return true
	}
	if مسار[0] == '/' && مسار[1] == '.' && مسار[2] == 0 {
		return true
	}
	return false
}

func sysنفاذ(مسارaddress uint32, وضع uint32) int32 {
	if مسارaddress == 0 {
		return Efault
	}
	if (وضع & ^uint32(7)) != 0 {
		return Einval
	}
	isالجذر := isالجذرمسار(مسارaddress)
	exists := isالجذر
	if !exists {
		الاسمlen, الاسم := نسخمسار(مسارaddress)
		exists = الاسمlen != 0 && ملفالحجم(الاسم[:الاسمlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (وضع & 2) != 0 {
		return Eacces
	}

	if (وضع&1) != 0 && !isالجذر {
		return Eacces
	}
	return 0
}

func syschdir(مسارaddress uint32) int32 {
	if مسارaddress == 0 {
		return Efault
	}
	if !isالجذرمسار(مسارaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, الحجم uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if الحجم < 2 {
		return Erange
	}
	buffer_2 := Getبايتfromالمؤشر(uintptr(bufferaddress), int(الحجم), int(الحجم))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, وضع uint32, الحجم uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dالجهاز = 1
	stat.Ino = inode
	stat.Mوضع = وضع
	stat.Nlink = 1
	stat.Sالحجم_2 = int32(الحجم)
	stat.Blksize = 512
	stat.Bحظر = int32((الحجم + 511) / 512)
	return 0
}

func sysstat(مسارaddress uint32, stataddress uint32) int32 {
	if مسارaddress == 0 {
		return Efault
	}
	if isالجذرمسار(مسارaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	الاسمlen, الاسم := نسخمسار(مسارaddress)
	if الاسمlen == 0 {
		return Enoent
	}
	الحجم := ملفالحجم(الاسم[:الاسمlen])
	if الحجم == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < الاسمlen; i++ {
		inode = inode*33 + uint32(الاسم[i])
	}
	return fillposixstat(stataddress, sifreg|0444, الحجم, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getفتحملف(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindطرفية:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindالجذردليل:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.الحجم, uint32(fd+2))
	case fdkindمقبس:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getفتحملف(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	عملية := ensureالحاليعملية()
	if عملية == nil {
		return 0
	}
	if عملية.برنامجbreak == 0 {
		عملية.برنامجbreak = مستخدمheapbase
	}
	if address_2 == 0 {
		return عملية.برنامجbreak
	}
	if address_2 < مستخدمheapbase || address_2 > مستخدمheapتحديد {
		return عملية.برنامجbreak
	}
	عملية.برنامجbreak = address_2
	return عملية.برنامجbreak
}

func نسخutsfield(المقصد *[65]byte, القيمة string) {
	تحديد := len(القيمة)
	if تحديد > 64 {
		تحديد = 64
	}
	for i := 0; i < تحديد; i++ {
		المقصد[i] = القيمة[i]
	}
	المقصد[تحديد] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	الاسم := (*posixutsname)(Pointer(uintptr(address_2)))
	*الاسم = posixutsname{}
	نسخutsfield(&الاسم.Sysname, "EngOS")
	نسخutsfield(&الاسم.Nodename, "engos")
	نسخutsfield(&الاسم.Release, "0.1-posix")
	نسخutsfield(&الاسم.Vإصدار, "POSIX.1-2017 phase 1")
	نسخutsfield(&الاسم.Machine, "i386")
	return 0
}

func مساحةالتبديلunsignedinteger16(القيمة uint16) uint16 {
	return (القيمة << 8) | (القيمة >> 8)
}

func مقبسنداءargument(arguments_2 uint32, فهرس uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + فهرس*4)))
}

func مقبسforfd(fd int32) (*محليdatagramمقبس, int32) {
	entry := getفتحملف(fd)
	if entry == nil || entry.kind != fdkindمقبس || entry.aux >= أقصىsockets {
		return nil, Ebadf
	}
	مقبس := &محليsockets[entry.aux]
	if !مقبس.used {
		return nil, Ebadf
	}
	return مقبس, 0
}

func allocateمقبس(المجال uint32, مقبسنوع uint32, البروتوكول uint32) int32 {
	if المجال != afinet {
		return Eafnosupport
	}
	if مقبسنوع != sockdatagram {
		return Eprotonosupport
	}
	if البروتوكول != 0 && البروتوكول != ipالبروتوكولudp {
		return Eprotonosupport
	}
	عملية := ensureالحاليعملية()
	if عملية == nil {
		return Enfile
	}
	مقبسفهرس := -1
	for i := 0; i < أقصىsockets; i++ {
		if !محليsockets[i].used {
			مقبسفهرس = i
			break
		}
	}
	if مقبسفهرس < 0 {
		return Enfile
	}
	الوصف := allocateفتحملف()
	if الوصف < 0 {
		return الوصف
	}
	محليsockets[مقبسفهرس] = محليdatagramمقبس{used: true}
	entry := &فتحملفجدول[الوصف]
	entry.kind = fdkindمقبس
	entry.خيارات = oقراءةكتابة
	entry.aux = uint32(مقبسفهرس)
	fd := allocatefd(عملية, الوصف, 3)
	if fd < 0 {
		محليsockets[مقبسفهرس] = محليdatagramمقبس{}
		*entry = فتحملفالوصف{}
		return fd
	}
	return fd
}

func مقبسaddress(address_2 uint32, المدة uint32) (*مقبسaddressiالقيمةالحالية4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if المدة < 16 {
		return nil, Einval
	}
	result := (*مقبسaddressiالقيمةالحالية4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func منفذداخلاستخدم(منفذ uint16, except *محليdatagramمقبس) bool {
	for i := 0; i < أقصىsockets; i++ {
		مقبس := &محليsockets[i]
		if مقبس != except && مقبس.used && مقبس.bound && مقبس.محلي.Pمنفذ == منفذ {
			return true
		}
	}
	return false
}

func bindephemeral(مقبس *محليdatagramمقبس) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		منفذ := مساحةالتبديلunsignedinteger16(التاليephemeralمنفذ)
		التاليephemeralمنفذ++
		if التاليephemeralمنفذ < 49152 {
			التاليephemeralمنفذ = 49152
		}
		if !منفذداخلاستخدم(منفذ, مقبس) {
			مقبس.محلي = مقبسaddressiالقيمةالحالية4{Family: afinet, Pمنفذ: منفذ, Address: 0x0100007F}
			مقبس.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func مقبسbind(fd int32, address_2 uint32, المدة uint32) int32 {
	مقبس, خطأ := مقبسforfd(fd)
	if خطأ != 0 {
		return خطأ
	}
	requested, خطأ := مقبسaddress(address_2, المدة)
	if خطأ != 0 {
		return خطأ
	}
	if مقبس.bound {
		return Einval
	}
	if requested.Pمنفذ == 0 {
		return bindephemeral(مقبس)
	}
	if منفذداخلاستخدم(requested.Pمنفذ, مقبس) {
		return Eaddrinuse
	}
	مقبس.محلي = *requested
	مقبس.bound = true
	return 0
}

func مقبسconnect(fd int32, address_2 uint32, المدة uint32) int32 {
	مقبس, خطأ := مقبسforfd(fd)
	if خطأ != 0 {
		return خطأ
	}
	البعيد, خطأ := مقبسaddress(address_2, المدة)
	if خطأ != 0 {
		return خطأ
	}
	if !مقبس.bound {
		if خطأ := bindephemeral(مقبس); خطأ != 0 {
			return خطأ
		}
	}
	مقبس.البعيد = *البعيد
	مقبس.connected = true
	return 0
}

func مقبسأرسلto(fd int32, bufferaddress_2 uint32, المدة uint32, المقصدaddress uint32, المقصدالمدة uint32) int32 {
	مقبس, خطأ := مقبسforfd(fd)
	if خطأ != 0 {
		return خطأ
	}
	if المدة > أقصىdatagramالحجم {
		return Emsgsize
	}
	if المدة != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var المقصد مقبسaddressiالقيمةالحالية4
	if المقصدaddress != 0 {
		address_2, addressخطأ := مقبسaddress(المقصدaddress, المقصدالمدة)
		if addressخطأ != 0 {
			return addressخطأ
		}
		المقصد = *address_2
	} else {
		if !مقبس.connected {
			return Enotconn
		}
		المقصد = مقبس.البعيد
	}
	if !مقبس.bound {
		if bindخطأ := bindephemeral(مقبس); bindخطأ != 0 {
			return bindخطأ
		}
	}
	var receiver *محليdatagramمقبس
	for i := 0; i < أقصىsockets; i++ {
		candidate := &محليsockets[i]
		if candidate.used && candidate.bound && candidate.محلي.Pمنفذ == المقصد.Pمنفذ &&
			(candidate.محلي.Address == 0 || candidate.محلي.Address == المقصد.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= أقصىمقبسpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = مقبسpacket{used: true, الحجم: المدة, المصدر: مقبس.محلي}
	if المدة != 0 {
		المصدر := Getبايتfromالمؤشر(uintptr(bufferaddress_2), int(المدة), int(المدة))
		copy(packet.بيانات[:المدة], المصدر)
	}
	receiver.tail = (receiver.tail + 1) % أقصىمقبسpackets
	receiver.count++
	return int32(المدة)
}

func مقبسreceivefrom(fd int32, bufferaddress_2 uint32, المدة uint32, المصدرaddress uint32, المصدرالمدةaddress uint32) int32 {
	مقبس, خطأ := مقبسforfd(fd)
	if خطأ != 0 {
		return خطأ
	}
	if المدة != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if مقبس.count == 0 {
		return Eagain
	}
	packet := &مقبس.packets[مقبس.head]
	نسخالمدة := packet.الحجم
	if نسخالمدة > المدة {
		نسخالمدة = المدة
	}
	if نسخالمدة != 0 {
		المقصد := Getبايتfromالمؤشر(uintptr(bufferaddress_2), int(نسخالمدة), int(نسخالمدة))
		copy(المقصد, packet.بيانات[:نسخالمدة])
	}
	if المصدرaddress != 0 {
		if المصدرالمدةaddress == 0 {
			return Efault
		}
		providedالمدة := (*uint32)(Pointer(uintptr(المصدرالمدةaddress)))
		if *providedالمدة >= 16 {
			*(*مقبسaddressiالقيمةالحالية4)(Pointer(uintptr(المصدرaddress))) = packet.المصدر
		}
		*providedالمدة = 16
	}
	*packet = مقبسpacket{}
	مقبس.head = (مقبس.head + 1) % أقصىمقبسpackets
	مقبس.count--
	return int32(نسخالمدة)
}

func نسخمقبسالاسم(fd int32, address_2 uint32, المدةaddress uint32, peer bool) int32 {
	مقبس, خطأ := مقبسforfd(fd)
	if خطأ != 0 {
		return خطأ
	}
	if address_2 == 0 || المدةaddress == 0 {
		return Efault
	}
	المدة := (*uint32)(Pointer(uintptr(المدةaddress)))
	if *المدة < 16 {
		*المدة = 16
		return Einval
	}
	if peer {
		if !مقبس.connected {
			return Enotconn
		}
		*(*مقبسaddressiالقيمةالحالية4)(Pointer(uintptr(address_2))) = مقبس.البعيد
	} else {
		if !مقبس.bound {
			if bindخطأ := bindephemeral(مقبس); bindخطأ != 0 {
				return bindخطأ
			}
		}
		*(*مقبسaddressiالقيمةالحالية4)(Pointer(uintptr(address_2))) = مقبس.محلي
	}
	*المدة = 16
	return 0
}

func sysمقبسنداء(نداء uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch نداء {
	case 1:
		return allocateمقبس(مقبسنداءargument(arguments_2, 0), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2))
	case 2:
		return مقبسbind(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2))
	case 3:
		return مقبسconnect(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return نسخمقبسالاسم(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), false)
	case 7:
		return نسخمقبسالاسم(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), true)
	case 9:
		return مقبسأرسلto(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), 0, 0)
	case 10:
		return مقبسreceivefrom(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), 0, 0)
	case 11:
		return مقبسأرسلto(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), مقبسنداءargument(arguments_2, 4), مقبسنداءargument(arguments_2, 5))
	case 12:
		return مقبسreceivefrom(int32(مقبسنداءargument(arguments_2, 0)), مقبسنداءargument(arguments_2, 1), مقبسنداءargument(arguments_2, 2), مقبسنداءargument(arguments_2, 4), مقبسنداءargument(arguments_2, 5))
	case 13:
		if _, خطأ := مقبسforfd(int32(مقبسنداءargument(arguments_2, 0))); خطأ != 0 {
			return خطأ
		}
		return 0
	case 14:
		if _, خطأ := مقبسforfd(int32(مقبسنداءargument(arguments_2, 0))); خطأ != 0 {
			return خطأ
		}
		return 0
	}
	return Eopnotsupp
}

func قراءةstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getبايتfromالمؤشر(uintptr(address), int(count), int(count))
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

func Stdinputبايت(c byte) {
	التالي := (stdinكتابة + 1) % uint32(len(stdinbuffer))
	if التالي == stdinقراءة {
		return
	}
	stdinbuffer[stdinكتابة] = c
	stdinكتابة = التالي
}

func stdingetblocking() byte {
	for stdinقراءة == stdinكتابة {
		sc := pollلوحةمفاتيحscancode()
		if sc != 0 {
			Stdinputبايت(sc)
		}
	}
	c := stdinbuffer[stdinقراءة]
	stdinقراءة = (stdinقراءة + 1) % uint32(len(stdinbuffer))
	return c
}

func pollلوحةمفاتيحscancode() byte {
	for (Pمنفذقراءةبايت(0x64) & 0x01) == 0 {
	}
	sc := Pمنفذقراءةبايت(0x60)
	return scancodetoبايت(sc)
}

func scancodetoبايت(sc uint8) byte {
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

func نسخexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for فهرس := uint32(0); فهرس < أقصىexecvectorentry; فهرس++ {
		سلسلةaddress := *(*uint32)(Pointer(uintptr(address_2 + فهرس*4)))
		if سلسلةaddress == 0 {
			result.count = فهرس
			return 0
		}
		terminated := false
		for المدة := uint32(0); المدة <= أقصىexecسلسلةالمدة; المدة++ {
			القيمة := *(*byte)(Pointer(uintptr(سلسلةaddress + المدة)))
			result.قيم[فهرس][المدة] = القيمة
			if القيمة == 0 {
				result.lengths[فهرس] = المدة
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

func pushexecunsignedinteger32(ذاكرة_مكدس *uint32, القيمة uint32) {
	*ذاكرة_مكدس -= 4
	*(*uint32)(Pointer(uintptr(*ذاكرة_مكدس))) = القيمة
}

func setupexecstack(المعالج *Tcpuالحالة, arguments_2 *execvector, environment *execvector) int32 {
	const stackبايت uint32 = 4096
	if !Makeمدىprivatewritable(getcr3(), Uمستخدمstackالأعلى-stackبايت, stackبايت) {
		return Enomem
	}
	ذاكرة_مكدس := Uمستخدمstackالأعلى
	var argumentpointers [أقصىexecvectorentry]uint32
	var environmentpointers [أقصىexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		المدة := environment.lengths[i] + 1
		ذاكرة_مكدس -= المدة
		المقصد := Getبايتfromالمؤشر(uintptr(ذاكرة_مكدس), int(المدة), int(المدة))
		copy(المقصد, environment.قيم[i][:المدة])
		environmentpointers[i] = ذاكرة_مكدس
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		المدة := arguments_2.lengths[i] + 1
		ذاكرة_مكدس -= المدة
		المقصد := Getبايتfromالمؤشر(uintptr(ذاكرة_مكدس), int(المدة), int(المدة))
		copy(المقصد, arguments_2.قيم[i][:المدة])
		argumentpointers[i] = ذاكرة_مكدس
	}
	ذاكرة_مكدس &= ^uint32(3)
	pushexecunsignedinteger32(&ذاكرة_مكدس, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&ذاكرة_مكدس, environmentpointers[i])
	}
	pushexecunsignedinteger32(&ذاكرة_مكدس, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&ذاكرة_مكدس, argumentpointers[i])
	}
	pushexecunsignedinteger32(&ذاكرة_مكدس, arguments_2.count)
	المعالج.Esp = ذاكرة_مكدس
	المعالج.Ebp = 0
	return 0
}

func إغلاقعندexec(عملية *عمليةentry) {
	if عملية == nil {
		return
	}
	for fd := int32(0); fd < أقصىfd; fd++ {
		if عملية.fds[fd].used && (عملية.fds[fd].fdخيارات&fdcloexec) != 0 {
			إغلاقعمليةfd(عملية, fd)
		}
	}
}

func sysexecve(المعالج *Tcpuالحالة, مسارaddress uint32) int32 {
	if مسارaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := نسخexecvector(المعالج.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := نسخexecvector(المعالج.Edx, &environment); result < 0 {
		return result
	}
	الاسمlen, الاسم := نسخمسار(مسارaddress)
	if الاسمlen == 0 {
		return Enoent
	}
	الحجم := ملفالحجم(الاسم[:الاسمlen])
	if الحجم == 0 {
		return Enoent
	}
	ذاكرةمدير := &mem.Tذاكرةمدير{}
	ملفالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	if ملفالمؤشر == nil {
		return Einval
	}
	بيانات := Getبايتfromالمؤشر(uintptr(ملفالمؤشر), int(الحجم), int(الحجم))
	قراءةملف(الاسم[:الاسمlen], بيانات)
	if الحجم < 52 || بيانات[0] != 0x7F || بيانات[1] != 'E' || بيانات[2] != 'L' || بيانات[3] != 'F' {
		ذاكرةمدير.Fخالي(ملفالمؤشر)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(بيانات)
	loader.Parse(بيانات, getcr3())
	ذاكرةمدير.Fخالي(ملفالمؤشر)
	if result := setupexecstack(المعالج, &arguments_2, &environment); result < 0 {
		return result
	}
	إغلاقعندexec(ensureالحاليعملية())
	المعالج.Eip = entry
	المعالج.Eax = 0
	return 0
}

func sysfork(المعالج *Tcpuالحالة) int32 {
	أبالهوية := Cالحاليالهوية()
	if ensureالحاليعملية() == nil {
		return Enfile
	}
	الهوية_2 := allocateعملية(أبالهوية)
	if الهوية_2 == 0 {
		return Einval
	}
	ذاكرةمدير := &mem.Tذاكرةمدير{}
	خيطتنفيذالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(uint32(Sizeof(Tخيطتنفيذ{})))
	stackالمؤشر := ذاكرةمدير.Mتخصيص_الذاكرة(Tخيطتنفيذstackالحجم)
	ابنةصفحةدليل := Cloneaddressspacecow(getcr3())
	if خيطتنفيذالمؤشر == nil || stackالمؤشر == nil || ابنةصفحةدليل == 0 {
		ارفضعملية(الهوية_2)
		return Einval
	}
	ابنة := (*Tخيطتنفيذ)(خيطتنفيذالمؤشر)
	ابنة.Stack = uint32(uintptr(stackالمؤشر))
	ابنة.Cالمعالجالحالة = (*Tcpuالحالة)(Pointer(uintptr(stackالمؤشر) + Tخيطتنفيذstackالحجم - Sizeof(Tcpuالحالة{})))
	*ابنة.Cالمعالجالحالة = *المعالج
	ابنة.Cالمعالجالحالة.Eax = 0
	ابنة.Uمستخدمstack_2 = المعالج.Esp
	ابنة.Uمستخدمstackالحجم_2 = 0
	ابنة.Pالهوية = الهوية_2
	ابنة.Pأبالهوية = أبالهوية
	ابنة.Pصفحةدليلentry = ابنةصفحةدليل
	ابنة.Tخيطتنفيذالحالة = Rجاهز
	ابنة.Fpuoffset = 0xffffffff
	ابنة.Isنواة = false
	Aأضفrunnableخيطتنفيذ(ابنة)
	return int32(الهوية_2)
}

func sysخروج(الحالة uint32) {
	الهوية_2 := Cالحاليالهوية()
	for i := 0; i < len(عمليةجدول); i++ {
		if عمليةجدول[i].used && عمليةجدول[i].الهوية_2 == الهوية_2 {
			إغلاقالكلعمليةfds(&عمليةجدول[i])
			عمليةجدول[i].exited = true
			عمليةجدول[i].الحالة = (الحالة & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(الهوية_2 int32, الحالةaddress uint32, خيارات_2 uint32) int32 {
	if (خيارات_2 & ^uint32(1)) != 0 {
		return Einval
	}
	أبالهوية := Cالحاليالهوية()
	foundابنة := false
	for i := 0; i < len(عمليةجدول); i++ {
		p := &عمليةجدول[i]
		matches := الهوية_2 == -1 || الهوية_2 == 0 || p.الهوية_2 == uint32(الهوية_2)
		if p.used && matches && p.أب == أبالهوية {
			foundابنة = true
			if p.exited {
				if الحالةaddress != 0 {
					*(*uint32)(Pointer(uintptr(الحالةaddress))) = p.الحالة
				}
				ابنةالهوية := p.الهوية_2
				*p = عمليةentry{}
				return int32(ابنةالهوية)
			}
		}
	}
	if !foundابنة {
		return Echild
	}

	if (خيارات_2 & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateعملية(أب uint32) uint32 {
	أبعملية := ابحثعملية(أب)
	الهوية_2 := Allocateالهوية()
	for i := 0; i < len(عمليةجدول); i++ {
		if !عمليةجدول[i].used {
			عمليةجدول[i] = عمليةentry{
				used:		true,
				الهوية_2:	الهوية_2,
				أب:		أب,
				برنامجbreak:	مستخدمheapbase,
			}
			if أبعملية != nil {
				عمليةجدول[i].برنامجbreak = أبعملية.برنامجbreak
				for fd := 0; fd < أقصىfd; fd++ {
					if أبعملية.fds[fd].used {
						عمليةجدول[i].fds[fd] = أبعملية.fds[fd]
						الوصف := أبعملية.fds[fd].الوصف
						if الوصف >= 0 && الوصف < أقصىفتحملفات {
							فتحملفجدول[الوصف].refs++
						}
					}
				}
			} else {
				initializeعمليةfds(&عمليةجدول[i])
			}
			return الهوية_2
		}
	}
	return 0
}

func إغلاقالكلعمليةfds(عملية *عمليةentry) {
	if عملية == nil {
		return
	}
	for fd := int32(0); fd < أقصىfd; fd++ {
		if عملية.fds[fd].used {
			إغلاقعمليةfd(عملية, fd)
		}
	}
}

func ارفضعملية(الهوية_2 uint32) {
	عملية := ابحثعملية(الهوية_2)
	if عملية == nil {
		return
	}
	إغلاقالكلعمليةfds(عملية)
	*عملية = عمليةentry{}
}

func نسخمسار(مسارaddress uint32) (uint32, [12]byte) {
	var الاسم [12]byte
	if مسارaddress == 0 {
		return 0, الاسم
	}
	raw := Getبايتfromالمؤشر(uintptr(مسارaddress), 64, 64)
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
		الاسم[n] = c
		n++
	}
	return n, الاسم
}

func ملفالحجم(اسمالملف []byte) uint32 {
	var ata0s = Tمتقدمالتقنيةattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	تجزئة := Tmsdosتجزئةجدول{}
	تجزئة.Rقراءةتجزئة(&ata0s)

	bios := Tمعلمات_نظام_الملفات32{}
	الحجم := bios.Len(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف)
	ata0s.Flush()
	return الحجم
}

func قراءةملف(اسمالملف []byte, بيانات []byte) {
	var ata0s = Tمتقدمالتقنيةattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	تجزئة := Tmsdosتجزئةجدول{}
	تجزئة.Rقراءةتجزئة(&ata0s)

	bios := Tمعلمات_نظام_الملفات32{}
	bios.Rقراءة(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف, بيانات)
	ata0s.Flush()
}

func getcr3() uint32
