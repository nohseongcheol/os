/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemcall

import . "unsafe"

import . "sampuk"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "failSistem/msdospartition"
import . "failSistem/fat"
import . "failSistem/format_pelaksanaan_dan_pemautan"
import mem "ingatanmanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualIngatan"

var console_2 = TConsole{}

type TSyscall struct {
	TSampukhandler
}

const (
	SysKeluar	uint32	= 1
	Sysfork		uint32	= 2
	SysBaca		uint32	= 3
	SysTulis	uint32	= 4
	SysBuka		uint32	= 5
	SysTutup	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syscapai	uint32	= 33
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
	SysrtKeluar	uint32	= 252

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
	maksfd			= 32
	maksBukafiles		= 128
)

type fdentry struct {
	digunakan	bool
	keterangan	int32
	fdBendera	uint32
}

type bukaFailKeterangan struct {
	digunakan	bool
	refs		uint32
	kind		uint32
	bendera		uint32
	kedudukan	uint32
	saiz		uint32
	nama		[12]byte
	namalen		uint32
	aux		uint32
}

const (
	fdkindTiada		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindrootdirektori	uint32	= 4
	fdkindSoket		uint32	= 5

	oBacaonly	uint32	= 0
	oTulisonly	uint32	= 1
	oBacaTulis	uint32	= 2
	ocreate		uint32	= 0x40
	oPangkas	uint32	= 0x200
	oappend		uint32	= 0x400
	odirektori	uint32	= 0x10000

	seekTetapkan	uint32	= 0
	seekSemasa	uint32	= 1
	seekTamat	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fTetapkanfd	uint32	= 2
	fgetfl		uint32	= 3
	fTetapkanfl	uint32	= 4
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
	makssockets		= 32
	maksSoketpaketpaket	= 8
	maksdatagramSaiz	= 512
)

type soketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type soketpacket struct {
	digunakan	bool
	saiz		uint32
	sumber		soketaddressipv4
	data		[maksdatagramSaiz]byte
}

type setempatdatagramSoket struct {
	digunakan	bool
	bound		bool
	connected	bool
	setempat	soketaddressipv4
	remote		soketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paketpaket	[maksSoketpaketpaket]soketpacket
}

type posixstat struct {
	Peranti		uint32
	Ino		uint32
	Mod		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Saiz_2		int32
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
	Versi		[65]byte
	Machine		[65]byte
}

const (
	maksJalankanvectorentry		= 16
	maksJalankanRentetanJarak	= 63
)

type jalankanvector struct {
	count	uint32
	lengths	[maksJalankanvectorentry]uint32
	nilai_2	[maksJalankanvectorentry][maksJalankanRentetanJarak + 1]byte
}

type prosesentry struct {
	digunakan	bool
	iDP		uint32
	induk		uint32
	keluar		bool
	status		uint32
	programbreak	uint32
	fds		[maksfd]fdentry
}

type rentetanheader struct {
	Data	uintptr
	Len	int
}

func syscallRalat(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var bukaFailJadual [maksBukafiles]bukaFailKeterangan
var prosesJadual [32]prosesentry
var setempatsockets [makssockets]setempatdatagramSoket
var berikutnyaephemeralport uint16 = 49152

const (
	penggunaheapbase	uint32	= 0x06000000
	penggunaheapHad		uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinBaca uint32
var stdinTulis uint32

func Sampuk(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysKeluar_2(indeks uint32) {
	Syscall(SysKeluar, indeks)
}

func SysBaca_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysBaca, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysCetakstr(buffer string) {
	h := (*rentetanheader)(Pointer(&buffer))
	Syscall(SysTulis, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysCetakunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysTulis, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysBuka_2(lALUAN uintptr, bendera uint32, mod uint32) int32 {
	return int32(Syscall(SysBuka, uint32(lALUAN), bendera, mod))
}

func SysTutup_2(fd uint32) int32 {
	return int32(Syscall(SysTutup, fd))
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
		return Sampuk(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Sampuk(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Sampuk(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Sampuk(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Sampuk(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Sampuk(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallRalat(Enosys)
	}
}

func (diri *TSyscall) Init(manager *TSampukmanager) {
	initFaildescriptor()

	sampukhandler = kendaliSampuk

	var address uintptr
	address = uintptr(Pointer(&sampukhandler))

	diri.TSampukhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var sampukhandler func(uint32) uint32

func kendaliSampuk(esp uint32) uint32 {
	var cpu = (*TcpuKeadaan)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysKeluar:
		sysKeluar(cpu.Ebx)
		return uint32(uintptr(Pointer(HentiSemasathread(cpu))))
	case SysrtKeluar:
		sysKeluar(cpu.Ebx)
		return uint32(uintptr(Pointer(HentiSemasathread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysBaca:
		cpu.Eax = uint32(sysBaca(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysTulis:
		cpu.Eax = uint32(sysTulis(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysBuka:
		cpu.Eax = uint32(sysBuka(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysBuka(cpu.Ebx, ocreate|oTulisonly|oPangkas, cpu.Ecx))
		return esp
	case SysTutup:
		cpu.Eax = uint32(sysTutup(int32(cpu.Ebx)))
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
		cpu.Eax = SemasaIDP()
		return esp
	case Sysgetppid:
		cpu.Eax = SemasaindukIDP()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syscapai:
		cpu.Eax = uint32(syscapai(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysSoketcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Cetak(cpu.Ebx)
		return esp

	default:
		console_2.MCetakxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Cetak(esp)
		console_2.MCetak(([]byte)(":"))
		console_2.MUnsignedinteger32Cetak(cpu.Eax)
		console_2.MCetak(([]byte)(":"))
		console_2.MUnsignedinteger32Cetak(cpu.Ebx)
		console_2.MCetak(([]byte)(":"))
		console_2.MUnsignedinteger32Cetak(cpu.Ecx)
		console_2.MCetak(([]byte)(":"))
		console_2.MUnsignedinteger32Cetak(cpu.Edx)
		console_2.MCetak(([]byte)("]"))
		cpu.Eax = syscallRalat(Enosys)
		return esp
	}

	return esp
}

func initFaildescriptor() {
	for i := 0; i < maksBukafiles; i++ {
		bukaFailJadual[i] = bukaFailKeterangan{}
	}
	for i := 0; i < len(prosesJadual); i++ {
		prosesJadual[i] = prosesentry{}
	}
	for i := 0; i < len(setempatsockets); i++ {
		setempatsockets[i] = setempatdatagramSoket{}
	}
	berikutnyaephemeralport = 49152
	bukaFailJadual[0] = bukaFailKeterangan{digunakan: true, kind: fdkindstdin, bendera: oBacaonly}
	bukaFailJadual[1] = bukaFailKeterangan{digunakan: true, kind: fdkindconsole, bendera: oTulisonly}
	bukaFailJadual[2] = bukaFailKeterangan{digunakan: true, kind: fdkindconsole, bendera: oTulisonly}
}

func cariProses(iDP uint32) *prosesentry {
	for i := 0; i < len(prosesJadual); i++ {
		if prosesJadual[i].digunakan && prosesJadual[i].iDP == iDP {
			return &prosesJadual[i]
		}
	}
	return nil
}

func initializeProsesfds(proses *prosesentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proses.fds[fd] = fdentry{digunakan: true, keterangan: fd}
		bukaFailJadual[fd].refs++
	}
}

func ensureSemasaProses() *prosesentry {
	iDP := SemasaIDP()
	if proses := cariProses(iDP); proses != nil {
		return proses
	}
	for i := 0; i < len(prosesJadual); i++ {
		if !prosesJadual[i].digunakan {
			prosesJadual[i] = prosesentry{
				digunakan:	true,
				iDP:		iDP,
				induk:		SemasaindukIDP(),
				programbreak:	penggunaheapbase,
			}
			initializeProsesfds(&prosesJadual[i])
			return &prosesJadual[i]
		}
	}
	return nil
}

func getBukaFailfor(proses *prosesentry, fd int32) *bukaFailKeterangan {
	if proses == nil || fd < 0 || fd >= maksfd || !proses.fds[fd].digunakan {
		return nil
	}
	keterangan := proses.fds[fd].keterangan
	if keterangan < 0 || keterangan >= maksBukafiles || !bukaFailJadual[keterangan].digunakan {
		return nil
	}
	return &bukaFailJadual[keterangan]
}

func getBukaFail(fd int32) *bukaFailKeterangan {
	return getBukaFailfor(ensureSemasaProses(), fd)
}

func allocateBukaFail() int32 {
	for i := int32(3); i < maksBukafiles; i++ {
		if !bukaFailJadual[i].digunakan {
			bukaFailJadual[i] = bukaFailKeterangan{digunakan: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proses *prosesentry, keterangan int32, minimum int32) int32 {
	if proses == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maksfd {
		return Einval
	}
	for fd := minimum; fd < maksfd; fd++ {
		if !proses.fds[fd].digunakan {
			proses.fds[fd] = fdentry{digunakan: true, keterangan: keterangan}
			return fd
		}
	}
	return Emfile
}

func releaseBukaFail(keterangan int32) {
	if keterangan < 0 || keterangan >= maksBukafiles {
		return
	}
	entry := &bukaFailJadual[keterangan]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && keterangan > stderrfd {
		if entry.kind == fdkindSoket && entry.aux < makssockets {
			setempatsockets[entry.aux] = setempatdatagramSoket{}
		}
		*entry = bukaFailKeterangan{}
	}
}

func tutupProsesfd(proses *prosesentry, fd int32) int32 {
	if proses == nil || getBukaFailfor(proses, fd) == nil {
		return Ebadf
	}
	keterangan := proses.fds[fd].keterangan
	proses.fds[fd] = fdentry{}
	releaseBukaFail(keterangan)
	return 0
}

func sysTulis(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getBukaFail(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindSoket {
			return soketHantarto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootdirektori {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBaitfromPenuding(uintptr(address), int(count), int(count))
	console_2.MCetak(buffer)
	return int32(count)
}

func sysBaca(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getBukaFail(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return bacastdin(address, count)
	}
	if entry.kind == fdkindrootdirektori {
		return Eisdir
	}
	if entry.kind == fdkindSoket {
		return soketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.kedudukan >= entry.saiz {
		return 0
	}
	remaining := entry.saiz - entry.kedudukan
	if count > remaining {
		count = remaining
	}
	buffer := GetBaitfromPenuding(uintptr(address), int(count), int(count))
	return bacavfsFail(entry, buffer, count)
}

func sysBuka(lALUANaddress uint32, bendera uint32, mod uint32) int32 {
	_ = mod
	if lALUANaddress == 0 {
		return Efault
	}
	capaimod := bendera & 3
	if capaimod == oTulisonly || capaimod == oBacaTulis || (bendera&(ocreate|oPangkas|oappend)) != 0 {
		return Erofs
	}

	proses := ensureSemasaProses()
	if proses == nil {
		return Enfile
	}
	keterangan := allocateBukaFail()
	if keterangan < 0 {
		return keterangan
	}
	entry := &bukaFailJadual[keterangan]
	entry.bendera = bendera
	if isrootLALUAN(lALUANaddress) {
		entry.kind = fdkindrootdirektori
		entry.saiz = 0
	} else {
		namalen, nama := salinLALUAN(lALUANaddress)
		if namalen == 0 {
			*entry = bukaFailKeterangan{}
			return Enoent
		}
		saiz := failSaiz(nama[:namalen])
		if saiz == 0 {
			*entry = bukaFailKeterangan{}
			return Enoent
		}
		if (bendera & odirektori) != 0 {
			*entry = bukaFailKeterangan{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.saiz = saiz
		entry.namalen = namalen
		entry.nama = nama
	}

	fd := allocatefd(proses, keterangan, 3)
	if fd < 0 {
		*entry = bukaFailKeterangan{}
		return fd
	}
	return fd
}

func sysTutup(fd int32) int32 {
	return tutupProsesfd(ensureSemasaProses(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	proses := ensureSemasaProses()
	entry := getBukaFailfor(proses, fd)
	if entry == nil {
		return Ebadf
	}
	baharufd := allocatefd(proses, proses.fds[fd].keterangan, minimum)
	if baharufd >= 0 {
		entry.refs++
	}
	return baharufd
}

func sysdup2(oldfd int32, baharufd int32) int32 {
	proses := ensureSemasaProses()
	entry := getBukaFailfor(proses, oldfd)
	if entry == nil {
		return Ebadf
	}
	if baharufd < 0 || baharufd >= maksfd {
		return Ebadf
	}
	if oldfd == baharufd {
		return baharufd
	}
	if proses.fds[baharufd].digunakan {
		tutupProsesfd(proses, baharufd)
	}
	proses.fds[baharufd] = fdentry{digunakan: true, keterangan: proses.fds[oldfd].keterangan}
	entry.refs++
	return baharufd
}

func sysfcntl(fd int32, perintah uint32, argument uint32) int32 {
	proses := ensureSemasaProses()
	entry := getBukaFailfor(proses, fd)
	if entry == nil {
		return Ebadf
	}
	switch perintah {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proses.fds[fd].fdBendera)
	case fTetapkanfd:
		proses.fds[fd].fdBendera = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.bendera)
	case fTetapkanfl:
		entry.bendera = (entry.bendera & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getBukaFail(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekTetapkan:
		base = 0
	case seekSemasa:
		base = int64(entry.kedudukan)
	case seekTamat:
		base = int64(entry.saiz)
	default:
		return Einval
	}
	kedudukan_2 := base + int64(offset)
	if kedudukan_2 < 0 || kedudukan_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.kedudukan = uint32(kedudukan_2)
	return int32(entry.kedudukan)
}

func bacavfsFail(entry *bukaFailKeterangan, destination_2 []byte, count uint32) int32 {
	ingatanmanager := &mem.TIngatanmanager{}
	tmpPenuding := ingatanmanager.Peruntukkan_ingatan(entry.saiz)
	if tmpPenuding == nil {
		return Einval
	}
	tmp := GetBaitfromPenuding(uintptr(tmpPenuding), int(entry.saiz), int(entry.saiz))
	bacaFail(entry.nama[:entry.namalen], tmp)
	copy(destination_2[:count], tmp[entry.kedudukan:entry.kedudukan+count])
	entry.kedudukan += count
	ingatanmanager.Bebas(tmpPenuding)
	return int32(count)
}

func isrootLALUAN(lALUANaddress uint32) bool {
	if lALUANaddress == 0 {
		return false
	}
	lALUAN := GetBaitfromPenuding(uintptr(lALUANaddress), 4, 4)
	if lALUAN[0] == '/' && lALUAN[1] == 0 {
		return true
	}
	if lALUAN[0] == '.' && lALUAN[1] == 0 {
		return true
	}
	if lALUAN[0] == '/' && lALUAN[1] == '.' && lALUAN[2] == 0 {
		return true
	}
	return false
}

func syscapai(lALUANaddress uint32, mod uint32) int32 {
	if lALUANaddress == 0 {
		return Efault
	}
	if (mod & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootLALUAN(lALUANaddress)
	exists := isroot
	if !exists {
		namalen, nama := salinLALUAN(lALUANaddress)
		exists = namalen != 0 && failSaiz(nama[:namalen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mod & 2) != 0 {
		return Eacces
	}

	if (mod&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(lALUANaddress uint32) int32 {
	if lALUANaddress == 0 {
		return Efault
	}
	if !isrootLALUAN(lALUANaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, saiz uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if saiz < 2 {
		return Erange
	}
	buffer_2 := GetBaitfromPenuding(uintptr(bufferaddress), int(saiz), int(saiz))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mod uint32, saiz uint32, inod uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Peranti = 1
	stat.Ino = inod
	stat.Mod = mod
	stat.Nlink = 1
	stat.Saiz_2 = int32(saiz)
	stat.Blksize = 512
	stat.Blok = int32((saiz + 511) / 512)
	return 0
}

func sysstat(lALUANaddress uint32, stataddress uint32) int32 {
	if lALUANaddress == 0 {
		return Efault
	}
	if isrootLALUAN(lALUANaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	namalen, nama := salinLALUAN(lALUANaddress)
	if namalen == 0 {
		return Enoent
	}
	saiz := failSaiz(nama[:namalen])
	if saiz == 0 {
		return Enoent
	}
	inod := uint32(2)
	for i := uint32(0); i < namalen; i++ {
		inod = inod*33 + uint32(nama[i])
	}
	return fillposixstat(stataddress, sifreg|0444, saiz, inod)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getBukaFail(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootdirektori:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.saiz, uint32(fd+2))
	case fdkindSoket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getBukaFail(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proses := ensureSemasaProses()
	if proses == nil {
		return 0
	}
	if proses.programbreak == 0 {
		proses.programbreak = penggunaheapbase
	}
	if address_2 == 0 {
		return proses.programbreak
	}
	if address_2 < penggunaheapbase || address_2 > penggunaheapHad {
		return proses.programbreak
	}
	proses.programbreak = address_2
	return proses.programbreak
}

func salinutsfield(destination *[65]byte, nilai string) {
	had := len(nilai)
	if had > 64 {
		had = 64
	}
	for i := 0; i < had; i++ {
		destination[i] = nilai[i]
	}
	destination[had] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nama := (*posixutsname)(Pointer(uintptr(address_2)))
	*nama = posixutsname{}
	salinutsfield(&nama.Sysname, "EngOS")
	salinutsfield(&nama.Nodename, "engos")
	salinutsfield(&nama.Release, "0.1-posix")
	salinutsfield(&nama.Versi, "POSIX.1-2017 phase 1")
	salinutsfield(&nama.Machine, "i386")
	return 0
}

func silihunsignedinteger16(nilai uint16) uint16 {
	return (nilai << 8) | (nilai >> 8)
}

func soketcallargument(arguments_2 uint32, indeks uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + indeks*4)))
}

func soketforfd(fd int32) (*setempatdatagramSoket, int32) {
	entry := getBukaFail(fd)
	if entry == nil || entry.kind != fdkindSoket || entry.aux >= makssockets {
		return nil, Ebadf
	}
	soket := &setempatsockets[entry.aux]
	if !soket.digunakan {
		return nil, Ebadf
	}
	return soket, 0
}

func allocateSoket(domain uint32, soketJenis uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if soketJenis != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proses := ensureSemasaProses()
	if proses == nil {
		return Enfile
	}
	soketIndeks := -1
	for i := 0; i < makssockets; i++ {
		if !setempatsockets[i].digunakan {
			soketIndeks = i
			break
		}
	}
	if soketIndeks < 0 {
		return Enfile
	}
	keterangan := allocateBukaFail()
	if keterangan < 0 {
		return keterangan
	}
	setempatsockets[soketIndeks] = setempatdatagramSoket{digunakan: true}
	entry := &bukaFailJadual[keterangan]
	entry.kind = fdkindSoket
	entry.bendera = oBacaTulis
	entry.aux = uint32(soketIndeks)
	fd := allocatefd(proses, keterangan, 3)
	if fd < 0 {
		setempatsockets[soketIndeks] = setempatdatagramSoket{}
		*entry = bukaFailKeterangan{}
		return fd
	}
	return fd
}

func soketaddress(address_2 uint32, jarak uint32) (*soketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if jarak < 16 {
		return nil, Einval
	}
	result := (*soketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portMasukGuna(port uint16, except *setempatdatagramSoket) bool {
	for i := 0; i < makssockets; i++ {
		soket := &setempatsockets[i]
		if soket != except && soket.digunakan && soket.bound && soket.setempat.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(soket *setempatdatagramSoket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := silihunsignedinteger16(berikutnyaephemeralport)
		berikutnyaephemeralport++
		if berikutnyaephemeralport < 49152 {
			berikutnyaephemeralport = 49152
		}
		if !portMasukGuna(port, soket) {
			soket.setempat = soketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			soket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func soketbind(fd int32, address_2 uint32, jarak uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := soketaddress(address_2, jarak)
	if err != 0 {
		return err
	}
	if soket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(soket)
	}
	if portMasukGuna(requested.Port, soket) {
		return Eaddrinuse
	}
	soket.setempat = *requested
	soket.bound = true
	return 0
}

func soketSambung(fd int32, address_2 uint32, jarak uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := soketaddress(address_2, jarak)
	if err != 0 {
		return err
	}
	if !soket.bound {
		if err := bindephemeral(soket); err != 0 {
			return err
		}
	}
	soket.remote = *remote
	soket.connected = true
	return 0
}

func soketHantarto(fd int32, bufferaddress_2 uint32, jarak uint32, destinationaddress uint32, destinationJarak uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if jarak > maksdatagramSaiz {
		return Emsgsize
	}
	if jarak != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination soketaddressipv4
	if destinationaddress != 0 {
		address_2, addressRalat := soketaddress(destinationaddress, destinationJarak)
		if addressRalat != 0 {
			return addressRalat
		}
		destination = *address_2
	} else {
		if !soket.connected {
			return Enotconn
		}
		destination = soket.remote
	}
	if !soket.bound {
		if bindRalat := bindephemeral(soket); bindRalat != 0 {
			return bindRalat
		}
	}
	var receiver *setempatdatagramSoket
	for i := 0; i < makssockets; i++ {
		candidate := &setempatsockets[i]
		if candidate.digunakan && candidate.bound && candidate.setempat.Port == destination.Port &&
			(candidate.setempat.Address == 0 || candidate.setempat.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksSoketpaketpaket {
		return Eagain
	}
	packet := &receiver.paketpaket[receiver.tail]
	*packet = soketpacket{digunakan: true, saiz: jarak, sumber: soket.setempat}
	if jarak != 0 {
		sumber := GetBaitfromPenuding(uintptr(bufferaddress_2), int(jarak), int(jarak))
		copy(packet.data[:jarak], sumber)
	}
	receiver.tail = (receiver.tail + 1) % maksSoketpaketpaket
	receiver.count++
	return int32(jarak)
}

func soketreceivefrom(fd int32, bufferaddress_2 uint32, jarak uint32, sumberaddress uint32, sumberJarakaddress uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if jarak != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if soket.count == 0 {
		return Eagain
	}
	packet := &soket.paketpaket[soket.head]
	salinJarak := packet.saiz
	if salinJarak > jarak {
		salinJarak = jarak
	}
	if salinJarak != 0 {
		destination := GetBaitfromPenuding(uintptr(bufferaddress_2), int(salinJarak), int(salinJarak))
		copy(destination, packet.data[:salinJarak])
	}
	if sumberaddress != 0 {
		if sumberJarakaddress == 0 {
			return Efault
		}
		providedJarak := (*uint32)(Pointer(uintptr(sumberJarakaddress)))
		if *providedJarak >= 16 {
			*(*soketaddressipv4)(Pointer(uintptr(sumberaddress))) = packet.sumber
		}
		*providedJarak = 16
	}
	*packet = soketpacket{}
	soket.head = (soket.head + 1) % maksSoketpaketpaket
	soket.count--
	return int32(salinJarak)
}

func salinSoketNama(fd int32, address_2 uint32, jarakaddress uint32, peer bool) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || jarakaddress == 0 {
		return Efault
	}
	jarak := (*uint32)(Pointer(uintptr(jarakaddress)))
	if *jarak < 16 {
		*jarak = 16
		return Einval
	}
	if peer {
		if !soket.connected {
			return Enotconn
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.remote
	} else {
		if !soket.bound {
			if bindRalat := bindephemeral(soket); bindRalat != 0 {
				return bindRalat
			}
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.setempat
	}
	*jarak = 16
	return 0
}

func sysSoketcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSoket(soketcallargument(arguments_2, 0), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2))
	case 2:
		return soketbind(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2))
	case 3:
		return soketSambung(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return salinSoketNama(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), false)
	case 7:
		return salinSoketNama(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), true)
	case 9:
		return soketHantarto(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return soketreceivefrom(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return soketHantarto(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), soketcallargument(arguments_2, 4), soketcallargument(arguments_2, 5))
	case 12:
		return soketreceivefrom(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), soketcallargument(arguments_2, 4), soketcallargument(arguments_2, 5))
	case 13:
		if _, err := soketforfd(int32(soketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := soketforfd(int32(soketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func bacastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaitfromPenuding(uintptr(address), int(count), int(count))
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
	berikutnya := (stdinTulis + 1) % uint32(len(stdinbuffer))
	if berikutnya == stdinBaca {
		return
	}
	stdinbuffer[stdinTulis] = c
	stdinTulis = berikutnya
}

func stdingetblocking() byte {
	for stdinBaca == stdinTulis {
		sc := pollPapankekunciscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinBaca]
	stdinBaca = (stdinBaca + 1) % uint32(len(stdinbuffer))
	return c
}

func pollPapankekunciscancode() byte {
	for (PortBacabyte(0x64) & 0x01) == 0 {
	}
	sc := PortBacabyte(0x60)
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

func salinJalankanvector(address_2 uint32, result *jalankanvector) int32 {
	*result = jalankanvector{}
	if address_2 == 0 {
		return 0
	}
	for indeks := uint32(0); indeks < maksJalankanvectorentry; indeks++ {
		rentetanaddress := *(*uint32)(Pointer(uintptr(address_2 + indeks*4)))
		if rentetanaddress == 0 {
			result.count = indeks
			return 0
		}
		terminated := false
		for jarak := uint32(0); jarak <= maksJalankanRentetanJarak; jarak++ {
			nilai := *(*byte)(Pointer(uintptr(rentetanaddress + jarak)))
			result.nilai_2[indeks][jarak] = nilai
			if nilai == 0 {
				result.lengths[indeks] = jarak
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

func pushJalankanunsignedinteger32(ingatan_tindanan *uint32, nilai uint32) {
	*ingatan_tindanan -= 4
	*(*uint32)(Pointer(uintptr(*ingatan_tindanan))) = nilai
}

func setupJalankanstack(cpu *TcpuKeadaan, arguments_2 *jalankanvector, environment *jalankanvector) int32 {
	const stackBait uint32 = 4096
	if !MakeJulatprivatewritable(getcr3(), PenggunastackAtas-stackBait, stackBait) {
		return Enomem
	}
	ingatan_tindanan := PenggunastackAtas
	var argumentpointers [maksJalankanvectorentry]uint32
	var environmentpointers [maksJalankanvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		jarak := environment.lengths[i] + 1
		ingatan_tindanan -= jarak
		destination := GetBaitfromPenuding(uintptr(ingatan_tindanan), int(jarak), int(jarak))
		copy(destination, environment.nilai_2[i][:jarak])
		environmentpointers[i] = ingatan_tindanan
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		jarak := arguments_2.lengths[i] + 1
		ingatan_tindanan -= jarak
		destination := GetBaitfromPenuding(uintptr(ingatan_tindanan), int(jarak), int(jarak))
		copy(destination, arguments_2.nilai_2[i][:jarak])
		argumentpointers[i] = ingatan_tindanan
	}
	ingatan_tindanan &= ^uint32(3)
	pushJalankanunsignedinteger32(&ingatan_tindanan, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushJalankanunsignedinteger32(&ingatan_tindanan, environmentpointers[i])
	}
	pushJalankanunsignedinteger32(&ingatan_tindanan, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushJalankanunsignedinteger32(&ingatan_tindanan, argumentpointers[i])
	}
	pushJalankanunsignedinteger32(&ingatan_tindanan, arguments_2.count)
	cpu.Esp = ingatan_tindanan
	cpu.Ebp = 0
	return 0
}

func tutupBukaJalankan(proses *prosesentry) {
	if proses == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proses.fds[fd].digunakan && (proses.fds[fd].fdBendera&fdcloexec) != 0 {
			tutupProsesfd(proses, fd)
		}
	}
}

func sysexecve(cpu *TcpuKeadaan, lALUANaddress uint32) int32 {
	if lALUANaddress == 0 {
		return Efault
	}
	var arguments_2 jalankanvector
	var environment jalankanvector
	if result := salinJalankanvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := salinJalankanvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	namalen, nama := salinLALUAN(lALUANaddress)
	if namalen == 0 {
		return Enoent
	}
	saiz := failSaiz(nama[:namalen])
	if saiz == 0 {
		return Enoent
	}
	ingatanmanager := &mem.TIngatanmanager{}
	failPenuding := ingatanmanager.Peruntukkan_ingatan(saiz)
	if failPenuding == nil {
		return Einval
	}
	data := GetBaitfromPenuding(uintptr(failPenuding), int(saiz), int(saiz))
	bacaFail(nama[:namalen], data)
	if saiz < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		ingatanmanager.Bebas(failPenuding)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	ingatanmanager.Bebas(failPenuding)
	if result := setupJalankanstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	tutupBukaJalankan(ensureSemasaProses())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuKeadaan) int32 {
	indukIDP := SemasaIDP()
	if ensureSemasaProses() == nil {
		return Enfile
	}
	iDP := allocateProses(indukIDP)
	if iDP == 0 {
		return Einval
	}
	ingatanmanager := &mem.TIngatanmanager{}
	threadPenuding := ingatanmanager.Peruntukkan_ingatan(uint32(Sizeof(TThread{})))
	stackPenuding := ingatanmanager.Peruntukkan_ingatan(ThreadstackSaiz)
	anakHalamandirektori := CloneaddressRuangcow(getcr3())
	if threadPenuding == nil || stackPenuding == nil || anakHalamandirektori == 0 {
		discardProses(iDP)
		return Einval
	}
	anak := (*TThread)(threadPenuding)
	anak.Stack = uint32(uintptr(stackPenuding))
	anak.CpuKeadaan = (*TcpuKeadaan)(Pointer(uintptr(stackPenuding) + ThreadstackSaiz - Sizeof(TcpuKeadaan{})))
	*anak.CpuKeadaan = *cpu
	anak.CpuKeadaan.Eax = 0
	anak.Penggunastack_2 = cpu.Esp
	anak.PenggunastackSaiz_2 = 0
	anak.IDP = iDP
	anak.IndukIDP = indukIDP
	anak.Halamandirektorientry = anakHalamandirektori
	anak.ThreadKeadaan = Sedia
	anak.Fpuoffset = 0xffffffff
	anak.Iskernel = false
	Tambahrunnablethread(anak)
	return int32(iDP)
}

func sysKeluar(status uint32) {
	iDP := SemasaIDP()
	for i := 0; i < len(prosesJadual); i++ {
		if prosesJadual[i].digunakan && prosesJadual[i].iDP == iDP {
			tutupSemuaProsesfds(&prosesJadual[i])
			prosesJadual[i].keluar = true
			prosesJadual[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(iDP int32, statusaddress uint32, opsyen uint32) int32 {
	if (opsyen & ^uint32(1)) != 0 {
		return Einval
	}
	indukIDP := SemasaIDP()
	foundanak := false
	for i := 0; i < len(prosesJadual); i++ {
		p := &prosesJadual[i]
		matches := iDP == -1 || iDP == 0 || p.iDP == uint32(iDP)
		if p.digunakan && matches && p.induk == indukIDP {
			foundanak = true
			if p.keluar {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				anakIDP := p.iDP
				*p = prosesentry{}
				return int32(anakIDP)
			}
		}
	}
	if !foundanak {
		return Echild
	}

	if (opsyen & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProses(induk uint32) uint32 {
	indukProses := cariProses(induk)
	iDP := AllocateIDP()
	for i := 0; i < len(prosesJadual); i++ {
		if !prosesJadual[i].digunakan {
			prosesJadual[i] = prosesentry{
				digunakan:	true,
				iDP:		iDP,
				induk:		induk,
				programbreak:	penggunaheapbase,
			}
			if indukProses != nil {
				prosesJadual[i].programbreak = indukProses.programbreak
				for fd := 0; fd < maksfd; fd++ {
					if indukProses.fds[fd].digunakan {
						prosesJadual[i].fds[fd] = indukProses.fds[fd]
						keterangan := indukProses.fds[fd].keterangan
						if keterangan >= 0 && keterangan < maksBukafiles {
							bukaFailJadual[keterangan].refs++
						}
					}
				}
			} else {
				initializeProsesfds(&prosesJadual[i])
			}
			return iDP
		}
	}
	return 0
}

func tutupSemuaProsesfds(proses *prosesentry) {
	if proses == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proses.fds[fd].digunakan {
			tutupProsesfd(proses, fd)
		}
	}
}

func discardProses(iDP uint32) {
	proses := cariProses(iDP)
	if proses == nil {
		return
	}
	tutupSemuaProsesfds(proses)
	*proses = prosesentry{}
}

func salinLALUAN(lALUANaddress uint32) (uint32, [12]byte) {
	var nama [12]byte
	if lALUANaddress == 0 {
		return 0, nama
	}
	raw := GetBaitfromPenuding(uintptr(lALUANaddress), 64, 64)
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
		nama[n] = c
		n++
	}
	return n, nama
}

func failSaiz(namafail []byte) uint32 {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionJadual{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_fail32{}
	saiz := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namafail)
	ata0s.Flush()
	return saiz
}

func bacaFail(namafail []byte, data []byte) {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionJadual{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_fail32{}
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namafail, data)
	ata0s.Flush()
}

func getcr3() uint32
