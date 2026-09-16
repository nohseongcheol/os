/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemcall

import . "unsafe"

import . "kesme"
import . "konsol"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "dosyaSistem/msdospartition"
import . "dosyaSistem/fat"
import . "dosyaSistem/çalıştırılabilir_ve_bağlanabilir_biçim"
import mem "bellekmanager"
import . "paging"
import . "bağlantıNoktası"
import . "tasking/scheduler"
import . "tasking/thread"
import . "sanalBellek"

var konsol_2 = TKonsol{}

type TSyscall struct {
	TKesmehandler
}

const (
	SysÇık		uint32	= 1
	Sysfork		uint32	= 2
	SysOkuma	uint32	= 3
	SysYazma	uint32	= 4
	SysAç		uint32	= 5
	SysKapat	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syserişim	uint32	= 33
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
	SysrtÇık	uint32	= 252

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
	stdinDT		int32	= 0
	stdoutDT	int32	= 1
	stderrDT	int32	= 2
	makDT			= 32
	makAçDOSYALAR		= 128
)

type dTgirdi struct {
	kullanılan	bool
	açıklama	int32
	dTİmler		uint32
}

type açDosyaAçıklama struct {
	kullanılan	bool
	refs		uint32
	tür		uint32
	imler		uint32
	konum		uint32
	boyut		uint32
	isim		[12]byte
	isimlen		uint32
	aux		uint32
}

const (
	dTTürHiçbiri		uint32	= 0
	dTTürfat		uint32	= 1
	dTTürstdin		uint32	= 2
	dTTürKonsol		uint32	= 3
	dTTürKökDizinDizin	uint32	= 4
	dTTürYuva		uint32	= 5

	oOkumaonly	uint32	= 0
	oYazmaonly	uint32	= 1
	oOkumaYazma	uint32	= 2
	ocreate		uint32	= 0x40
	oKırp		uint32	= 0x200
	oappend		uint32	= 0x400
	oDizin		uint32	= 0x10000

	seekayarla	uint32	= 0
	seekŞuan	uint32	= 1
	seekSon		uint32	= 2

	fdupDT		uint32	= 0
	fgetDT		uint32	= 1
	fayarlaDT	uint32	= 2
	fgetfl		uint32	= 3
	fayarlafl	uint32	= 4
	dTcloexec	uint32	= 1

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
	maksockets		= 32
	makYuvapaket		= 8
	makdatagramBoyut	= 512
)

type yuvaaddressipv4 struct {
	Family		uint16
	BağlantıNoktası	uint16
	Address		uint32
	Sıfır		[8]byte
}

type yuvaPAKET struct {
	kullanılan	bool
	boyut		uint32
	kaynak		yuvaaddressipv4
	data		[makdatagramBoyut]byte
}

type yereldatagramYuva struct {
	kullanılan	bool
	bound		bool
	connected	bool
	yerel		yuvaaddressipv4
	uzak		yuvaaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paket		[makYuvapaket]yuvaPAKET
}

type posixstat struct {
	Aygıt		uint32
	Ino		uint32
	KİP		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Boyut_2		int32
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
	Sürüm		[65]byte
	Machine		[65]byte
}

const (
	makÇalıştırvectorgirdi	= 16
	makÇalıştırKatarSüre	= 63
)

type çalıştırvector struct {
	count		uint32
	lengths		[makÇalıştırvectorgirdi]uint32
	değerler	[makÇalıştırvectorgirdi][makÇalıştırKatarSüre + 1]byte
}

type süreçgirdi struct {
	kullanılan	bool
	pid		uint32
	üst		uint32
	çıkıldı		bool
	durum		uint32
	uygulamabreak	uint32
	fds		[makDT]dTgirdi
}

type katarheader struct {
	Data	uintptr
	Len	int
}

func syscallHata(hata int32) uint32 {
	return *(*uint32)(Pointer(&hata))
}

var açDosyaTablo [makAçDOSYALAR]açDosyaAçıklama
var süreçTablo [32]süreçgirdi
var yerelsockets [maksockets]yereldatagramYuva
var sonrakiephemeralBağlantıNoktası uint16 = 49152

const (
	kullanıcıheapbase	uint32	= 0x06000000
	kullanıcıheapKısıtla	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinOkuma uint32
var stdinYazma uint32

func Kesme(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysÇık_2(içindekiler uint32) {
	Syscall(SysÇık, içindekiler)
}

func SysOkuma_2(dT uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysOkuma, dT, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysYazdırstr(buffer string) {
	h := (*katarheader)(Pointer(&buffer))
	Syscall(SysYazma, uint32(stdoutDT), uint32(h.Data), uint32(h.Len))
}

func SysYazdırunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysYazma, uint32(stdoutDT), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAç_2(yOL uintptr, imler uint32, kİP uint32) int32 {
	return int32(Syscall(SysAç, uint32(yOL), imler, kİP))
}

func SysKapat_2(dT uint32) int32 {
	return int32(Syscall(SysKapat, dT))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametreler ...uint32) uint32 {

	l := len(parametreler)
	switch l {
	case 1:
		return Kesme(parametreler[0], 0, 0, 0, 0, 0)
	case 2:
		return Kesme(parametreler[0], parametreler[1], 0, 0, 0, 0)
	case 3:
		return Kesme(parametreler[0], parametreler[1], parametreler[2], 0, 0, 0)
	case 4:
		return Kesme(parametreler[0], parametreler[1], parametreler[2], parametreler[3], 0, 0)
	case 5:
		return Kesme(parametreler[0], parametreler[1], parametreler[2], parametreler[3], parametreler[4], 0)
	case 6:
		return Kesme(parametreler[0], parametreler[1], parametreler[2], parametreler[3], parametreler[4], parametreler[5])
	default:
		return syscallHata(Enosys)
	}
}

func (self *TSyscall) Init(manager *TKesmemanager) {
	initDosyadescriptor()

	kesmehandler = handleKesme

	var address uintptr
	address = uintptr(Pointer(&kesmehandler))

	self.TKesmehandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var kesmehandler func(uint32) uint32

func handleKesme(esp uint32) uint32 {
	var mİB = (*TcpuDurum)(Pointer(uintptr(esp)))

	switch mİB.Eax {
	case SysÇık:
		sysÇık(mİB.Ebx)
		return uint32(uintptr(Pointer(DurdurŞuanthread(mİB))))
	case SysrtÇık:
		sysÇık(mİB.Ebx)
		return uint32(uintptr(Pointer(DurdurŞuanthread(mİB))))
	case Sysfork:
		mİB.Eax = uint32(sysfork(mİB))
		return esp
	case SysOkuma:
		mİB.Eax = uint32(sysOkuma(int32(mİB.Ebx), mİB.Ecx, mİB.Edx))
		return esp
	case SysYazma:
		mİB.Eax = uint32(sysYazma(int32(mİB.Ebx), mİB.Ecx, mİB.Edx))
		return esp
	case SysAç:
		mİB.Eax = uint32(sysAç(mİB.Ebx, mİB.Ecx, mİB.Edx))
		return esp
	case Syscreat:
		mİB.Eax = uint32(sysAç(mİB.Ebx, ocreate|oYazmaonly|oKırp, mİB.Ecx))
		return esp
	case SysKapat:
		mİB.Eax = uint32(sysKapat(int32(mİB.Ebx)))
		return esp
	case Syswaitpid:
		mİB.Eax = uint32(syswaitpid(int32(mİB.Ebx), mİB.Ecx, mİB.Edx))
		return esp
	case Syslseek:
		mİB.Eax = uint32(syslseek(int32(mİB.Ebx), int32(mİB.Ecx), mİB.Edx))
		return esp
	case Sysexecve:
		mİB.Eax = uint32(sysexecve(mİB, mİB.Ebx))
		return esp
	case Sysgetpid:
		mİB.Eax = Şuanpid()
		return esp
	case Sysgetppid:
		mİB.Eax = Şuanüstpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		mİB.Eax = 0
		return esp
	case Syserişim:
		mİB.Eax = uint32(syserişim(mİB.Ebx, mİB.Ecx))
		return esp
	case Syschdir:
		mİB.Eax = uint32(syschdir(mİB.Ebx))
		return esp
	case Sysgetcwd:
		mİB.Eax = uint32(sysgetcwd(mİB.Ebx, mİB.Ecx))
		return esp
	case Sysdup:
		mİB.Eax = uint32(sysdup(int32(mİB.Ebx), 0))
		return esp
	case Sysdup2:
		mİB.Eax = uint32(sysdup2(int32(mİB.Ebx), int32(mİB.Ecx)))
		return esp
	case Syssocketcall:
		mİB.Eax = uint32(sysYuvacall(mİB.Ebx, mİB.Ecx))
		return esp
	case Sysfcntl:
		mİB.Eax = uint32(sysfcntl(int32(mİB.Ebx), mİB.Ecx, mİB.Edx))
		return esp
	case Sysstat, Syslstat:
		mİB.Eax = uint32(sysstat(mİB.Ebx, mİB.Ecx))
		return esp
	case Sysfstat:
		mİB.Eax = uint32(sysfstat(int32(mİB.Ebx), mİB.Ecx))
		return esp
	case Sysfsync:
		mİB.Eax = uint32(sysfsync(int32(mİB.Ebx)))
		return esp
	case Syssync:
		mİB.Eax = 0
		return esp
	case Sysuname:
		mİB.Eax = uint32(sysuname(mİB.Ebx))
		return esp
	case Sysbrk:
		mİB.Eax = sysbrk(mİB.Ebx)
		return esp
	case 9:
		konsol_2.MUnsignedinteger32Yazdır(mİB.Ebx)
		return esp

	default:
		konsol_2.MYazdırxy(([]byte)("sys["), 1, 23)
		konsol_2.MUnsignedinteger32Yazdır(esp)
		konsol_2.MYazdır(([]byte)(":"))
		konsol_2.MUnsignedinteger32Yazdır(mİB.Eax)
		konsol_2.MYazdır(([]byte)(":"))
		konsol_2.MUnsignedinteger32Yazdır(mİB.Ebx)
		konsol_2.MYazdır(([]byte)(":"))
		konsol_2.MUnsignedinteger32Yazdır(mİB.Ecx)
		konsol_2.MYazdır(([]byte)(":"))
		konsol_2.MUnsignedinteger32Yazdır(mİB.Edx)
		konsol_2.MYazdır(([]byte)("]"))
		mİB.Eax = syscallHata(Enosys)
		return esp
	}

	return esp
}

func initDosyadescriptor() {
	for i := 0; i < makAçDOSYALAR; i++ {
		açDosyaTablo[i] = açDosyaAçıklama{}
	}
	for i := 0; i < len(süreçTablo); i++ {
		süreçTablo[i] = süreçgirdi{}
	}
	for i := 0; i < len(yerelsockets); i++ {
		yerelsockets[i] = yereldatagramYuva{}
	}
	sonrakiephemeralBağlantıNoktası = 49152
	açDosyaTablo[0] = açDosyaAçıklama{kullanılan: true, tür: dTTürstdin, imler: oOkumaonly}
	açDosyaTablo[1] = açDosyaAçıklama{kullanılan: true, tür: dTTürKonsol, imler: oYazmaonly}
	açDosyaTablo[2] = açDosyaAçıklama{kullanılan: true, tür: dTTürKonsol, imler: oYazmaonly}
}

func bulSüreç(pid uint32) *süreçgirdi {
	for i := 0; i < len(süreçTablo); i++ {
		if süreçTablo[i].kullanılan && süreçTablo[i].pid == pid {
			return &süreçTablo[i]
		}
	}
	return nil
}

func initializeSüreçfds(süreç *süreçgirdi) {
	for dT := int32(0); dT <= stderrDT; dT++ {
		süreç.fds[dT] = dTgirdi{kullanılan: true, açıklama: dT}
		açDosyaTablo[dT].refs++
	}
}

func ensureŞuanSüreç() *süreçgirdi {
	pid := Şuanpid()
	if süreç := bulSüreç(pid); süreç != nil {
		return süreç
	}
	for i := 0; i < len(süreçTablo); i++ {
		if !süreçTablo[i].kullanılan {
			süreçTablo[i] = süreçgirdi{
				kullanılan:	true,
				pid:		pid,
				üst:		Şuanüstpid(),
				uygulamabreak:	kullanıcıheapbase,
			}
			initializeSüreçfds(&süreçTablo[i])
			return &süreçTablo[i]
		}
	}
	return nil
}

func getAçDosyafor(süreç *süreçgirdi, dT int32) *açDosyaAçıklama {
	if süreç == nil || dT < 0 || dT >= makDT || !süreç.fds[dT].kullanılan {
		return nil
	}
	açıklama := süreç.fds[dT].açıklama
	if açıklama < 0 || açıklama >= makAçDOSYALAR || !açDosyaTablo[açıklama].kullanılan {
		return nil
	}
	return &açDosyaTablo[açıklama]
}

func getAçDosya(dT int32) *açDosyaAçıklama {
	return getAçDosyafor(ensureŞuanSüreç(), dT)
}

func allocateAçDosya() int32 {
	for i := int32(3); i < makAçDOSYALAR; i++ {
		if !açDosyaTablo[i].kullanılan {
			açDosyaTablo[i] = açDosyaAçıklama{kullanılan: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateDT(süreç *süreçgirdi, açıklama int32, enaz int32) int32 {
	if süreç == nil {
		return Enfile
	}
	if enaz < 0 || enaz >= makDT {
		return Einval
	}
	for dT := enaz; dT < makDT; dT++ {
		if !süreç.fds[dT].kullanılan {
			süreç.fds[dT] = dTgirdi{kullanılan: true, açıklama: açıklama}
			return dT
		}
	}
	return Emfile
}

func releaseAçDosya(açıklama int32) {
	if açıklama < 0 || açıklama >= makAçDOSYALAR {
		return
	}
	girdi := &açDosyaTablo[açıklama]
	if girdi.refs > 0 {
		girdi.refs--
	}

	if girdi.refs == 0 && açıklama > stderrDT {
		if girdi.tür == dTTürYuva && girdi.aux < maksockets {
			yerelsockets[girdi.aux] = yereldatagramYuva{}
		}
		*girdi = açDosyaAçıklama{}
	}
}

func kapatSüreçDT(süreç *süreçgirdi, dT int32) int32 {
	if süreç == nil || getAçDosyafor(süreç, dT) == nil {
		return Ebadf
	}
	açıklama := süreç.fds[dT].açıklama
	süreç.fds[dT] = dTgirdi{}
	releaseAçDosya(açıklama)
	return 0
}

func sysYazma(dT int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	girdi := getAçDosya(dT)
	if girdi == nil {
		return Ebadf
	}
	if girdi.tür != dTTürKonsol {
		if girdi.tür == dTTürYuva {
			return yuvaGönderto(dT, address, count, 0, 0)
		}
		if girdi.tür == dTTürfat || girdi.tür == dTTürKökDizinDizin {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBaytfromBelirteç(uintptr(address), int(count), int(count))
	konsol_2.MYazdır(buffer)
	return int32(count)
}

func sysOkuma(dT int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	girdi := getAçDosya(dT)
	if girdi == nil {
		return Ebadf
	}
	if girdi.tür == dTTürstdin {
		return okumastdin(address, count)
	}
	if girdi.tür == dTTürKökDizinDizin {
		return Eisdir
	}
	if girdi.tür == dTTürYuva {
		return yuvareceivefrom(dT, address, count, 0, 0)
	}
	if girdi.tür != dTTürfat {
		return Ebadf
	}
	if girdi.konum >= girdi.boyut {
		return 0
	}
	remaining := girdi.boyut - girdi.konum
	if count > remaining {
		count = remaining
	}
	buffer := GetBaytfromBelirteç(uintptr(address), int(count), int(count))
	return okumavfsDosya(girdi, buffer, count)
}

func sysAç(yOLaddress uint32, imler uint32, kİP uint32) int32 {
	_ = kİP
	if yOLaddress == 0 {
		return Efault
	}
	erişimKİP := imler & 3
	if erişimKİP == oYazmaonly || erişimKİP == oOkumaYazma || (imler&(ocreate|oKırp|oappend)) != 0 {
		return Erofs
	}

	süreç := ensureŞuanSüreç()
	if süreç == nil {
		return Enfile
	}
	açıklama := allocateAçDosya()
	if açıklama < 0 {
		return açıklama
	}
	girdi := &açDosyaTablo[açıklama]
	girdi.imler = imler
	if isKökDizinYOL(yOLaddress) {
		girdi.tür = dTTürKökDizinDizin
		girdi.boyut = 0
	} else {
		isimlen, isim := kopyalaYOL(yOLaddress)
		if isimlen == 0 {
			*girdi = açDosyaAçıklama{}
			return Enoent
		}
		boyut := dosyaBoyut(isim[:isimlen])
		if boyut == 0 {
			*girdi = açDosyaAçıklama{}
			return Enoent
		}
		if (imler & oDizin) != 0 {
			*girdi = açDosyaAçıklama{}
			return Enotdir
		}
		girdi.tür = dTTürfat
		girdi.boyut = boyut
		girdi.isimlen = isimlen
		girdi.isim = isim
	}

	dT := allocateDT(süreç, açıklama, 3)
	if dT < 0 {
		*girdi = açDosyaAçıklama{}
		return dT
	}
	return dT
}

func sysKapat(dT int32) int32 {
	return kapatSüreçDT(ensureŞuanSüreç(), dT)
}

func sysdup(dT int32, enaz int32) int32 {
	süreç := ensureŞuanSüreç()
	girdi := getAçDosyafor(süreç, dT)
	if girdi == nil {
		return Ebadf
	}
	yeniDT := allocateDT(süreç, süreç.fds[dT].açıklama, enaz)
	if yeniDT >= 0 {
		girdi.refs++
	}
	return yeniDT
}

func sysdup2(oldDT int32, yeniDT int32) int32 {
	süreç := ensureŞuanSüreç()
	girdi := getAçDosyafor(süreç, oldDT)
	if girdi == nil {
		return Ebadf
	}
	if yeniDT < 0 || yeniDT >= makDT {
		return Ebadf
	}
	if oldDT == yeniDT {
		return yeniDT
	}
	if süreç.fds[yeniDT].kullanılan {
		kapatSüreçDT(süreç, yeniDT)
	}
	süreç.fds[yeniDT] = dTgirdi{kullanılan: true, açıklama: süreç.fds[oldDT].açıklama}
	girdi.refs++
	return yeniDT
}

func sysfcntl(dT int32, komut uint32, argument uint32) int32 {
	süreç := ensureŞuanSüreç()
	girdi := getAçDosyafor(süreç, dT)
	if girdi == nil {
		return Ebadf
	}
	switch komut {
	case fdupDT:
		return sysdup(dT, int32(argument))
	case fgetDT:
		return int32(süreç.fds[dT].dTİmler)
	case fayarlaDT:
		süreç.fds[dT].dTİmler = argument & dTcloexec
		return 0
	case fgetfl:
		return int32(girdi.imler)
	case fayarlafl:
		girdi.imler = (girdi.imler & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(dT int32, offset int32, whence uint32) int32 {
	girdi := getAçDosya(dT)
	if girdi == nil {
		return Ebadf
	}
	if girdi.tür != dTTürfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekayarla:
		base = 0
	case seekŞuan:
		base = int64(girdi.konum)
	case seekSon:
		base = int64(girdi.boyut)
	default:
		return Einval
	}
	konum_2 := base + int64(offset)
	if konum_2 < 0 || konum_2 > 0x7FFFFFFF {
		return Einval
	}
	girdi.konum = uint32(konum_2)
	return int32(girdi.konum)
}

func okumavfsDosya(girdi *açDosyaAçıklama, hedef_2 []byte, count uint32) int32 {
	bellekmanager := &mem.TBellekmanager{}
	tmpBelirteç := bellekmanager.Bellek_ayır(girdi.boyut)
	if tmpBelirteç == nil {
		return Einval
	}
	tmp := GetBaytfromBelirteç(uintptr(tmpBelirteç), int(girdi.boyut), int(girdi.boyut))
	okumaDosya(girdi.isim[:girdi.isimlen], tmp)
	copy(hedef_2[:count], tmp[girdi.konum:girdi.konum+count])
	girdi.konum += count
	bellekmanager.Boş(tmpBelirteç)
	return int32(count)
}

func isKökDizinYOL(yOLaddress uint32) bool {
	if yOLaddress == 0 {
		return false
	}
	yOL := GetBaytfromBelirteç(uintptr(yOLaddress), 4, 4)
	if yOL[0] == '/' && yOL[1] == 0 {
		return true
	}
	if yOL[0] == '.' && yOL[1] == 0 {
		return true
	}
	if yOL[0] == '/' && yOL[1] == '.' && yOL[2] == 0 {
		return true
	}
	return false
}

func syserişim(yOLaddress uint32, kİP uint32) int32 {
	if yOLaddress == 0 {
		return Efault
	}
	if (kİP & ^uint32(7)) != 0 {
		return Einval
	}
	isKökDizin := isKökDizinYOL(yOLaddress)
	exists := isKökDizin
	if !exists {
		isimlen, isim := kopyalaYOL(yOLaddress)
		exists = isimlen != 0 && dosyaBoyut(isim[:isimlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (kİP & 2) != 0 {
		return Eacces
	}

	if (kİP&1) != 0 && !isKökDizin {
		return Eacces
	}
	return 0
}

func syschdir(yOLaddress uint32) int32 {
	if yOLaddress == 0 {
		return Efault
	}
	if !isKökDizinYOL(yOLaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, boyut uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if boyut < 2 {
		return Erange
	}
	buffer_2 := GetBaytfromBelirteç(uintptr(bufferaddress), int(boyut), int(boyut))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, kİP uint32, boyut uint32, dosyaindeksi uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Aygıt = 1
	stat.Ino = dosyaindeksi
	stat.KİP = kİP
	stat.Nlink = 1
	stat.Boyut_2 = int32(boyut)
	stat.Blksize = 512
	stat.Blok = int32((boyut + 511) / 512)
	return 0
}

func sysstat(yOLaddress uint32, stataddress uint32) int32 {
	if yOLaddress == 0 {
		return Efault
	}
	if isKökDizinYOL(yOLaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	isimlen, isim := kopyalaYOL(yOLaddress)
	if isimlen == 0 {
		return Enoent
	}
	boyut := dosyaBoyut(isim[:isimlen])
	if boyut == 0 {
		return Enoent
	}
	dosyaindeksi := uint32(2)
	for i := uint32(0); i < isimlen; i++ {
		dosyaindeksi = dosyaindeksi*33 + uint32(isim[i])
	}
	return fillposixstat(stataddress, sifreg|0444, boyut, dosyaindeksi)
}

func sysfstat(dT int32, stataddress uint32) int32 {
	girdi := getAçDosya(dT)
	if girdi == nil {
		return Ebadf
	}
	switch girdi.tür {
	case dTTürstdin, dTTürKonsol:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(dT+1))
	case dTTürKökDizinDizin:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case dTTürfat:
		return fillposixstat(stataddress, sifreg|0444, girdi.boyut, uint32(dT+2))
	case dTTürYuva:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(dT+2))
	}
	return Ebadf
}

func sysfsync(dT int32) int32 {
	if getAçDosya(dT) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	süreç := ensureŞuanSüreç()
	if süreç == nil {
		return 0
	}
	if süreç.uygulamabreak == 0 {
		süreç.uygulamabreak = kullanıcıheapbase
	}
	if address_2 == 0 {
		return süreç.uygulamabreak
	}
	if address_2 < kullanıcıheapbase || address_2 > kullanıcıheapKısıtla {
		return süreç.uygulamabreak
	}
	süreç.uygulamabreak = address_2
	return süreç.uygulamabreak
}

func kopyalautsalan(hedef *[65]byte, değer string) {
	kısıtla := len(değer)
	if kısıtla > 64 {
		kısıtla = 64
	}
	for i := 0; i < kısıtla; i++ {
		hedef[i] = değer[i]
	}
	hedef[kısıtla] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	isim := (*posixutsname)(Pointer(uintptr(address_2)))
	*isim = posixutsname{}
	kopyalautsalan(&isim.Sysname, "EngOS")
	kopyalautsalan(&isim.Nodename, "engos")
	kopyalautsalan(&isim.Release, "0.1-posix")
	kopyalautsalan(&isim.Sürüm, "POSIX.1-2017 phase 1")
	kopyalautsalan(&isim.Machine, "i386")
	return 0
}

func takasAlanıunsignedinteger16(değer uint16) uint16 {
	return (değer << 8) | (değer >> 8)
}

func yuvacallargument(argümanlar_2 uint32, içindekiler uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argümanlar_2 + içindekiler*4)))
}

func yuvaforDT(dT int32) (*yereldatagramYuva, int32) {
	girdi := getAçDosya(dT)
	if girdi == nil || girdi.tür != dTTürYuva || girdi.aux >= maksockets {
		return nil, Ebadf
	}
	yuva := &yerelsockets[girdi.aux]
	if !yuva.kullanılan {
		return nil, Ebadf
	}
	return yuva, 0
}

func allocateYuva(alanAdı uint32, yuvaTür uint32, protocol uint32) int32 {
	if alanAdı != afinet {
		return Eafnosupport
	}
	if yuvaTür != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	süreç := ensureŞuanSüreç()
	if süreç == nil {
		return Enfile
	}
	yuvaİçindekiler := -1
	for i := 0; i < maksockets; i++ {
		if !yerelsockets[i].kullanılan {
			yuvaİçindekiler = i
			break
		}
	}
	if yuvaİçindekiler < 0 {
		return Enfile
	}
	açıklama := allocateAçDosya()
	if açıklama < 0 {
		return açıklama
	}
	yerelsockets[yuvaİçindekiler] = yereldatagramYuva{kullanılan: true}
	girdi := &açDosyaTablo[açıklama]
	girdi.tür = dTTürYuva
	girdi.imler = oOkumaYazma
	girdi.aux = uint32(yuvaİçindekiler)
	dT := allocateDT(süreç, açıklama, 3)
	if dT < 0 {
		yerelsockets[yuvaİçindekiler] = yereldatagramYuva{}
		*girdi = açDosyaAçıklama{}
		return dT
	}
	return dT
}

func yuvaaddress(address_2 uint32, süre uint32) (*yuvaaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if süre < 16 {
		return nil, Einval
	}
	sONUÇ := (*yuvaaddressipv4)(Pointer(uintptr(address_2)))
	if sONUÇ.Family != afinet {
		return nil, Eafnosupport
	}
	return sONUÇ, 0
}

func bağlantıNoktasıGelenKullan(bağlantıNoktası uint16, except *yereldatagramYuva) bool {
	for i := 0; i < maksockets; i++ {
		yuva := &yerelsockets[i]
		if yuva != except && yuva.kullanılan && yuva.bound && yuva.yerel.BağlantıNoktası == bağlantıNoktası {
			return true
		}
	}
	return false
}

func bindephemeral(yuva *yereldatagramYuva) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		bağlantıNoktası := takasAlanıunsignedinteger16(sonrakiephemeralBağlantıNoktası)
		sonrakiephemeralBağlantıNoktası++
		if sonrakiephemeralBağlantıNoktası < 49152 {
			sonrakiephemeralBağlantıNoktası = 49152
		}
		if !bağlantıNoktasıGelenKullan(bağlantıNoktası, yuva) {
			yuva.yerel = yuvaaddressipv4{Family: afinet, BağlantıNoktası: bağlantıNoktası, Address: 0x0100007F}
			yuva.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func yuvabind(dT int32, address_2 uint32, süre uint32) int32 {
	yuva, hata := yuvaforDT(dT)
	if hata != 0 {
		return hata
	}
	requested, hata := yuvaaddress(address_2, süre)
	if hata != 0 {
		return hata
	}
	if yuva.bound {
		return Einval
	}
	if requested.BağlantıNoktası == 0 {
		return bindephemeral(yuva)
	}
	if bağlantıNoktasıGelenKullan(requested.BağlantıNoktası, yuva) {
		return Eaddrinuse
	}
	yuva.yerel = *requested
	yuva.bound = true
	return 0
}

func yuvaBağlan(dT int32, address_2 uint32, süre uint32) int32 {
	yuva, hata := yuvaforDT(dT)
	if hata != 0 {
		return hata
	}
	uzak, hata := yuvaaddress(address_2, süre)
	if hata != 0 {
		return hata
	}
	if !yuva.bound {
		if hata := bindephemeral(yuva); hata != 0 {
			return hata
		}
	}
	yuva.uzak = *uzak
	yuva.connected = true
	return 0
}

func yuvaGönderto(dT int32, bufferaddress_2 uint32, süre uint32, hedefaddress uint32, hedefSüre uint32) int32 {
	yuva, hata := yuvaforDT(dT)
	if hata != 0 {
		return hata
	}
	if süre > makdatagramBoyut {
		return Emsgsize
	}
	if süre != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var hedef yuvaaddressipv4
	if hedefaddress != 0 {
		address_2, addressHata := yuvaaddress(hedefaddress, hedefSüre)
		if addressHata != 0 {
			return addressHata
		}
		hedef = *address_2
	} else {
		if !yuva.connected {
			return Enotconn
		}
		hedef = yuva.uzak
	}
	if !yuva.bound {
		if bindHata := bindephemeral(yuva); bindHata != 0 {
			return bindHata
		}
	}
	var receiver *yereldatagramYuva
	for i := 0; i < maksockets; i++ {
		candidate := &yerelsockets[i]
		if candidate.kullanılan && candidate.bound && candidate.yerel.BağlantıNoktası == hedef.BağlantıNoktası &&
			(candidate.yerel.Address == 0 || candidate.yerel.Address == hedef.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= makYuvapaket {
		return Eagain
	}
	pAKET := &receiver.paket[receiver.tail]
	*pAKET = yuvaPAKET{kullanılan: true, boyut: süre, kaynak: yuva.yerel}
	if süre != 0 {
		kaynak := GetBaytfromBelirteç(uintptr(bufferaddress_2), int(süre), int(süre))
		copy(pAKET.data[:süre], kaynak)
	}
	receiver.tail = (receiver.tail + 1) % makYuvapaket
	receiver.count++
	return int32(süre)
}

func yuvareceivefrom(dT int32, bufferaddress_2 uint32, süre uint32, kaynakaddress uint32, kaynakSüreaddress uint32) int32 {
	yuva, hata := yuvaforDT(dT)
	if hata != 0 {
		return hata
	}
	if süre != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if yuva.count == 0 {
		return Eagain
	}
	pAKET := &yuva.paket[yuva.head]
	kopyalaSüre := pAKET.boyut
	if kopyalaSüre > süre {
		kopyalaSüre = süre
	}
	if kopyalaSüre != 0 {
		hedef := GetBaytfromBelirteç(uintptr(bufferaddress_2), int(kopyalaSüre), int(kopyalaSüre))
		copy(hedef, pAKET.data[:kopyalaSüre])
	}
	if kaynakaddress != 0 {
		if kaynakSüreaddress == 0 {
			return Efault
		}
		providedSüre := (*uint32)(Pointer(uintptr(kaynakSüreaddress)))
		if *providedSüre >= 16 {
			*(*yuvaaddressipv4)(Pointer(uintptr(kaynakaddress))) = pAKET.kaynak
		}
		*providedSüre = 16
	}
	*pAKET = yuvaPAKET{}
	yuva.head = (yuva.head + 1) % makYuvapaket
	yuva.count--
	return int32(kopyalaSüre)
}

func kopyalaYuvaİsim(dT int32, address_2 uint32, süreaddress uint32, peer bool) int32 {
	yuva, hata := yuvaforDT(dT)
	if hata != 0 {
		return hata
	}
	if address_2 == 0 || süreaddress == 0 {
		return Efault
	}
	süre := (*uint32)(Pointer(uintptr(süreaddress)))
	if *süre < 16 {
		*süre = 16
		return Einval
	}
	if peer {
		if !yuva.connected {
			return Enotconn
		}
		*(*yuvaaddressipv4)(Pointer(uintptr(address_2))) = yuva.uzak
	} else {
		if !yuva.bound {
			if bindHata := bindephemeral(yuva); bindHata != 0 {
				return bindHata
			}
		}
		*(*yuvaaddressipv4)(Pointer(uintptr(address_2))) = yuva.yerel
	}
	*süre = 16
	return 0
}

func sysYuvacall(call uint32, argümanlar_2 uint32) int32 {
	if argümanlar_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateYuva(yuvacallargument(argümanlar_2, 0), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2))
	case 2:
		return yuvabind(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2))
	case 3:
		return yuvaBağlan(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopyalaYuvaİsim(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), false)
	case 7:
		return kopyalaYuvaİsim(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), true)
	case 9:
		return yuvaGönderto(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), 0, 0)
	case 10:
		return yuvareceivefrom(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), 0, 0)
	case 11:
		return yuvaGönderto(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), yuvacallargument(argümanlar_2, 4), yuvacallargument(argümanlar_2, 5))
	case 12:
		return yuvareceivefrom(int32(yuvacallargument(argümanlar_2, 0)), yuvacallargument(argümanlar_2, 1), yuvacallargument(argümanlar_2, 2), yuvacallargument(argümanlar_2, 4), yuvacallargument(argümanlar_2, 5))
	case 13:
		if _, hata := yuvaforDT(int32(yuvacallargument(argümanlar_2, 0))); hata != 0 {
			return hata
		}
		return 0
	case 14:
		if _, hata := yuvaforDT(int32(yuvacallargument(argümanlar_2, 0))); hata != 0 {
			return hata
		}
		return 0
	}
	return Eopnotsupp
}

func okumastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaytfromBelirteç(uintptr(address), int(count), int(count))
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
	sonraki := (stdinYazma + 1) % uint32(len(stdinbuffer))
	if sonraki == stdinOkuma {
		return
	}
	stdinbuffer[stdinYazma] = c
	stdinYazma = sonraki
}

func stdingetblocking() byte {
	for stdinOkuma == stdinYazma {
		sc := pollKlavyescancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinOkuma]
	stdinOkuma = (stdinOkuma + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlavyescancode() byte {
	for (BağlantıNoktasıOkumabyte(0x64) & 0x01) == 0 {
	}
	sc := BağlantıNoktasıOkumabyte(0x60)
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

func kopyalaÇalıştırvector(address_2 uint32, sONUÇ *çalıştırvector) int32 {
	*sONUÇ = çalıştırvector{}
	if address_2 == 0 {
		return 0
	}
	for içindekiler := uint32(0); içindekiler < makÇalıştırvectorgirdi; içindekiler++ {
		kataraddress := *(*uint32)(Pointer(uintptr(address_2 + içindekiler*4)))
		if kataraddress == 0 {
			sONUÇ.count = içindekiler
			return 0
		}
		terminated := false
		for süre := uint32(0); süre <= makÇalıştırKatarSüre; süre++ {
			değer := *(*byte)(Pointer(uintptr(kataraddress + süre)))
			sONUÇ.değerler[içindekiler][süre] = değer
			if değer == 0 {
				sONUÇ.lengths[içindekiler] = süre
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

func pushÇalıştırunsignedinteger32(yığın_belleği *uint32, değer uint32) {
	*yığın_belleği -= 4
	*(*uint32)(Pointer(uintptr(*yığın_belleği))) = değer
}

func setupÇalıştırstack(mİB *TcpuDurum, argümanlar_2 *çalıştırvector, environment *çalıştırvector) int32 {
	const stackBayt uint32 = 4096
	if !MakeAralıkGizliÖzelwritable(getcr3(), KullanıcıstackÜst-stackBayt, stackBayt) {
		return Enomem
	}
	yığın_belleği := KullanıcıstackÜst
	var argumentpointers [makÇalıştırvectorgirdi]uint32
	var environmentpointers [makÇalıştırvectorgirdi]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		süre := environment.lengths[i] + 1
		yığın_belleği -= süre
		hedef := GetBaytfromBelirteç(uintptr(yığın_belleği), int(süre), int(süre))
		copy(hedef, environment.değerler[i][:süre])
		environmentpointers[i] = yığın_belleği
	}
	for i := int(argümanlar_2.count) - 1; i >= 0; i-- {
		süre := argümanlar_2.lengths[i] + 1
		yığın_belleği -= süre
		hedef := GetBaytfromBelirteç(uintptr(yığın_belleği), int(süre), int(süre))
		copy(hedef, argümanlar_2.değerler[i][:süre])
		argumentpointers[i] = yığın_belleği
	}
	yığın_belleği &= ^uint32(3)
	pushÇalıştırunsignedinteger32(&yığın_belleği, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushÇalıştırunsignedinteger32(&yığın_belleği, environmentpointers[i])
	}
	pushÇalıştırunsignedinteger32(&yığın_belleği, 0)
	for i := int(argümanlar_2.count) - 1; i >= 0; i-- {
		pushÇalıştırunsignedinteger32(&yığın_belleği, argumentpointers[i])
	}
	pushÇalıştırunsignedinteger32(&yığın_belleği, argümanlar_2.count)
	mİB.Esp = yığın_belleği
	mİB.Ebp = 0
	return 0
}

func kapatAçıkÇalıştır(süreç *süreçgirdi) {
	if süreç == nil {
		return
	}
	for dT := int32(0); dT < makDT; dT++ {
		if süreç.fds[dT].kullanılan && (süreç.fds[dT].dTİmler&dTcloexec) != 0 {
			kapatSüreçDT(süreç, dT)
		}
	}
}

func sysexecve(mİB *TcpuDurum, yOLaddress uint32) int32 {
	if yOLaddress == 0 {
		return Efault
	}
	var argümanlar_2 çalıştırvector
	var environment çalıştırvector
	if sONUÇ := kopyalaÇalıştırvector(mİB.Ecx, &argümanlar_2); sONUÇ < 0 {
		return sONUÇ
	}
	if sONUÇ := kopyalaÇalıştırvector(mİB.Edx, &environment); sONUÇ < 0 {
		return sONUÇ
	}
	isimlen, isim := kopyalaYOL(yOLaddress)
	if isimlen == 0 {
		return Enoent
	}
	boyut := dosyaBoyut(isim[:isimlen])
	if boyut == 0 {
		return Enoent
	}
	bellekmanager := &mem.TBellekmanager{}
	dosyaBelirteç := bellekmanager.Bellek_ayır(boyut)
	if dosyaBelirteç == nil {
		return Einval
	}
	data := GetBaytfromBelirteç(uintptr(dosyaBelirteç), int(boyut), int(boyut))
	okumaDosya(isim[:isimlen], data)
	if boyut < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		bellekmanager.Boş(dosyaBelirteç)
		return Enoexec
	}
	loader := Elf{}
	girdi := loader.Getgirdi(data)
	loader.Parse(data, getcr3())
	bellekmanager.Boş(dosyaBelirteç)
	if sONUÇ := setupÇalıştırstack(mİB, &argümanlar_2, &environment); sONUÇ < 0 {
		return sONUÇ
	}
	kapatAçıkÇalıştır(ensureŞuanSüreç())
	mİB.Eip = girdi
	mİB.Eax = 0
	return 0
}

func sysfork(mİB *TcpuDurum) int32 {
	üstpid := Şuanpid()
	if ensureŞuanSüreç() == nil {
		return Enfile
	}
	pid := allocateSüreç(üstpid)
	if pid == 0 {
		return Einval
	}
	bellekmanager := &mem.TBellekmanager{}
	threadBelirteç := bellekmanager.Bellek_ayır(uint32(Sizeof(TThread{})))
	stackBelirteç := bellekmanager.Bellek_ayır(ThreadstackBoyut)
	childSayfaDizin := CloneaddressBoşlukcow(getcr3())
	if threadBelirteç == nil || stackBelirteç == nil || childSayfaDizin == 0 {
		vazgeçSüreç(pid)
		return Einval
	}
	child := (*TThread)(threadBelirteç)
	child.Stack = uint32(uintptr(stackBelirteç))
	child.MİBDurum = (*TcpuDurum)(Pointer(uintptr(stackBelirteç) + ThreadstackBoyut - Sizeof(TcpuDurum{})))
	*child.MİBDurum = *mİB
	child.MİBDurum.Eax = 0
	child.Kullanıcıstack_2 = mİB.Esp
	child.KullanıcıstackBoyut_2 = 0
	child.Pid = pid
	child.Üstpid = üstpid
	child.SayfaDizingirdi = childSayfaDizin
	child.ThreadDurum = Hazır
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Eklerunnablethread(child)
	return int32(pid)
}

func sysÇık(durum uint32) {
	pid := Şuanpid()
	for i := 0; i < len(süreçTablo); i++ {
		if süreçTablo[i].kullanılan && süreçTablo[i].pid == pid {
			kapatHepsiSüreçfds(&süreçTablo[i])
			süreçTablo[i].çıkıldı = true
			süreçTablo[i].durum = (durum & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, durumaddress uint32, seçenekler uint32) int32 {
	if (seçenekler & ^uint32(1)) != 0 {
		return Einval
	}
	üstpid := Şuanpid()
	foundchild := false
	for i := 0; i < len(süreçTablo); i++ {
		p := &süreçTablo[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.kullanılan && matches && p.üst == üstpid {
			foundchild = true
			if p.çıkıldı {
				if durumaddress != 0 {
					*(*uint32)(Pointer(uintptr(durumaddress))) = p.durum
				}
				childpid := p.pid
				*p = süreçgirdi{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (seçenekler & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateSüreç(üst uint32) uint32 {
	üstSüreç := bulSüreç(üst)
	pid := Allocatepid()
	for i := 0; i < len(süreçTablo); i++ {
		if !süreçTablo[i].kullanılan {
			süreçTablo[i] = süreçgirdi{
				kullanılan:	true,
				pid:		pid,
				üst:		üst,
				uygulamabreak:	kullanıcıheapbase,
			}
			if üstSüreç != nil {
				süreçTablo[i].uygulamabreak = üstSüreç.uygulamabreak
				for dT := 0; dT < makDT; dT++ {
					if üstSüreç.fds[dT].kullanılan {
						süreçTablo[i].fds[dT] = üstSüreç.fds[dT]
						açıklama := üstSüreç.fds[dT].açıklama
						if açıklama >= 0 && açıklama < makAçDOSYALAR {
							açDosyaTablo[açıklama].refs++
						}
					}
				}
			} else {
				initializeSüreçfds(&süreçTablo[i])
			}
			return pid
		}
	}
	return 0
}

func kapatHepsiSüreçfds(süreç *süreçgirdi) {
	if süreç == nil {
		return
	}
	for dT := int32(0); dT < makDT; dT++ {
		if süreç.fds[dT].kullanılan {
			kapatSüreçDT(süreç, dT)
		}
	}
}

func vazgeçSüreç(pid uint32) {
	süreç := bulSüreç(pid)
	if süreç == nil {
		return
	}
	kapatHepsiSüreçfds(süreç)
	*süreç = süreçgirdi{}
}

func kopyalaYOL(yOLaddress uint32) (uint32, [12]byte) {
	var isim [12]byte
	if yOLaddress == 0 {
		return 0, isim
	}
	raw := GetBaytfromBelirteç(uintptr(yOLaddress), 64, 64)
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
		isim[n] = c
		n++
	}
	return n, isim
}

func dosyaBoyut(dosyaadı []byte) uint32 {
	var ata0s = TGelişmişTeknolojiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablo{}
	partition.Okumapartition(&ata0s)

	bios := TDosya_sistemi_parametreleri32{}
	boyut := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı)
	ata0s.Flush()
	return boyut
}

func okumaDosya(dosyaadı []byte, data []byte) {
	var ata0s = TGelişmişTeknolojiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablo{}
	partition.Okumapartition(&ata0s)

	bios := TDosya_sistemi_parametreleri32{}
	bios.Okuma(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı, data)
	ata0s.Flush()
}

func getcr3() uint32
