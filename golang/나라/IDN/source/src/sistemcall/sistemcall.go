package sistemcall

import . "unsafe"

import . "interupsi"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "berkasSistem/msdospartition"
import . "berkasSistem/fat"
import . "berkasSistem/format_eksekusi_dan_penautan"
import mem "memorimanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualMemori"

var console_2 = TConsole{}

type TSyscall struct {
	TInterupsihandler
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
	Sysakses	uint32	= 33
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
	maksBukaBERKAS		= 128
)

type fdentri struct {
	dipakai		bool
	keterangan	int32
	fdTanda		uint32
}

type bukaBerkasKeterangan struct {
	dipakai	bool
	refs	uint32
	jenis	uint32
	tanda	uint32
	posisi	uint32
	ukuran	uint32
	nama	[12]byte
	namalen	uint32
	aux	uint32
}

const (
	fdJenisTakAda		uint32	= 0
	fdJenisfat		uint32	= 1
	fdJenisstdin		uint32	= 2
	fdJenisconsole		uint32	= 3
	fdJenisAkarDirektori	uint32	= 4
	fdJenisSoket		uint32	= 5

	oBacaonly	uint32	= 0
	oTulisonly	uint32	= 1
	oBacaTulis	uint32	= 2
	ocreate		uint32	= 0x40
	oPenggal	uint32	= 0x200
	oappend		uint32	= 0x400
	oDirektori	uint32	= 0x10000

	seekAtur	uint32	= 0
	seekSekarang	uint32	= 1
	seekAkhir	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fAturfd		uint32	= 2
	fgetfl		uint32	= 3
	fAturfl		uint32	= 4
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
	maksSoketpaket		= 8
	maksdatagramUkuran	= 512
)

type soketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Nol	[8]byte
}

type soketpacket struct {
	dipakai	bool
	ukuran	uint32
	sumber	soketaddressipv4
	data	[maksdatagramUkuran]byte
}

type lokaldatagramSoket struct {
	dipakai		bool
	bound		bool
	connected	bool
	lokal		soketaddressipv4
	jauh		soketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paket		[maksSoketpaket]soketpacket
}

type posixstat struct {
	Perangkat	uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Ukuran_2	int32
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
	maksexecvectorentri	= 16
	maksexecBenangPanjang	= 63
)

type execvector struct {
	count	uint32
	lengths	[maksexecvectorentri]uint32
	nilai_2	[maksexecvectorentri][maksexecBenangPanjang + 1]byte
}

type prosesentri struct {
	dipakai		bool
	pid		uint32
	orangtua	uint32
	keluar		bool
	status		uint32
	programbreak	uint32
	fds		[maksfd]fdentri
}

type benangheader struct {
	Data	uintptr
	Len	int
}

func syscallGalat(galat int32) uint32 {
	return *(*uint32)(Pointer(&galat))
}

var bukaBerkasTabel [maksBukaBERKAS]bukaBerkasKeterangan
var prosesTabel [32]prosesentri
var lokalsockets [makssockets]lokaldatagramSoket
var berikutnyaephemeralport uint16 = 49152

const (
	penggunaheapbase	uint32	= 0x06000000
	penggunaheapBatas	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinBaca uint32
var stdinTulis uint32

func Interupsi(eax, ebx, ecx, edx, esi, edi uint32) uint32

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
	h := (*benangheader)(Pointer(&buffer))
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

func SysBuka_2(alur uintptr, tanda uint32, mode uint32) int32 {
	return int32(Syscall(SysBuka, uint32(alur), tanda, mode))
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

func Syscall(param_2 ...uint32) uint32 {

	l := len(param_2)
	switch l {
	case 1:
		return Interupsi(param_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Interupsi(param_2[0], param_2[1], 0, 0, 0, 0)
	case 3:
		return Interupsi(param_2[0], param_2[1], param_2[2], 0, 0, 0)
	case 4:
		return Interupsi(param_2[0], param_2[1], param_2[2], param_2[3], 0, 0)
	case 5:
		return Interupsi(param_2[0], param_2[1], param_2[2], param_2[3], param_2[4], 0)
	case 6:
		return Interupsi(param_2[0], param_2[1], param_2[2], param_2[3], param_2[4], param_2[5])
	default:
		return syscallGalat(Enosys)
	}
}

func (dirisendiri *TSyscall) Init(manager *TInterupsimanager) {
	initBerkasdescriptor()

	interupsihandler = penangananInterupsi

	var address uintptr
	address = uintptr(Pointer(&interupsihandler))

	dirisendiri.TInterupsihandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interupsihandler func(uint32) uint32

func penangananInterupsi(esp uint32) uint32 {
	var cpu = (*TcpuStatus)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysKeluar:
		sysKeluar(cpu.Ebx)
		return uint32(uintptr(Pointer(HentikanSekarangthread(cpu))))
	case SysrtKeluar:
		sysKeluar(cpu.Ebx)
		return uint32(uintptr(Pointer(HentikanSekarangthread(cpu))))
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
		cpu.Eax = uint32(sysBuka(cpu.Ebx, ocreate|oTulisonly|oPenggal, cpu.Ecx))
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
		cpu.Eax = Sekarangpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Sekarangorangtuapid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysakses:
		cpu.Eax = uint32(sysakses(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = syscallGalat(Enosys)
		return esp
	}

	return esp
}

func initBerkasdescriptor() {
	for i := 0; i < maksBukaBERKAS; i++ {
		bukaBerkasTabel[i] = bukaBerkasKeterangan{}
	}
	for i := 0; i < len(prosesTabel); i++ {
		prosesTabel[i] = prosesentri{}
	}
	for i := 0; i < len(lokalsockets); i++ {
		lokalsockets[i] = lokaldatagramSoket{}
	}
	berikutnyaephemeralport = 49152
	bukaBerkasTabel[0] = bukaBerkasKeterangan{dipakai: true, jenis: fdJenisstdin, tanda: oBacaonly}
	bukaBerkasTabel[1] = bukaBerkasKeterangan{dipakai: true, jenis: fdJenisconsole, tanda: oTulisonly}
	bukaBerkasTabel[2] = bukaBerkasKeterangan{dipakai: true, jenis: fdJenisconsole, tanda: oTulisonly}
}

func cariProses(pid uint32) *prosesentri {
	for i := 0; i < len(prosesTabel); i++ {
		if prosesTabel[i].dipakai && prosesTabel[i].pid == pid {
			return &prosesTabel[i]
		}
	}
	return nil
}

func initializeProsesfds(proses *prosesentri) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proses.fds[fd] = fdentri{dipakai: true, keterangan: fd}
		bukaBerkasTabel[fd].refs++
	}
}

func ensureSekarangProses() *prosesentri {
	pid := Sekarangpid()
	if proses := cariProses(pid); proses != nil {
		return proses
	}
	for i := 0; i < len(prosesTabel); i++ {
		if !prosesTabel[i].dipakai {
			prosesTabel[i] = prosesentri{
				dipakai:	true,
				pid:		pid,
				orangtua:	Sekarangorangtuapid(),
				programbreak:	penggunaheapbase,
			}
			initializeProsesfds(&prosesTabel[i])
			return &prosesTabel[i]
		}
	}
	return nil
}

func getBukaBerkasfor(proses *prosesentri, fd int32) *bukaBerkasKeterangan {
	if proses == nil || fd < 0 || fd >= maksfd || !proses.fds[fd].dipakai {
		return nil
	}
	keterangan := proses.fds[fd].keterangan
	if keterangan < 0 || keterangan >= maksBukaBERKAS || !bukaBerkasTabel[keterangan].dipakai {
		return nil
	}
	return &bukaBerkasTabel[keterangan]
}

func getBukaBerkas(fd int32) *bukaBerkasKeterangan {
	return getBukaBerkasfor(ensureSekarangProses(), fd)
}

func allocateBukaBerkas() int32 {
	for i := int32(3); i < maksBukaBERKAS; i++ {
		if !bukaBerkasTabel[i].dipakai {
			bukaBerkasTabel[i] = bukaBerkasKeterangan{dipakai: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proses *prosesentri, keterangan int32, minimum int32) int32 {
	if proses == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maksfd {
		return Einval
	}
	for fd := minimum; fd < maksfd; fd++ {
		if !proses.fds[fd].dipakai {
			proses.fds[fd] = fdentri{dipakai: true, keterangan: keterangan}
			return fd
		}
	}
	return Emfile
}

func releaseBukaBerkas(keterangan int32) {
	if keterangan < 0 || keterangan >= maksBukaBERKAS {
		return
	}
	entri := &bukaBerkasTabel[keterangan]
	if entri.refs > 0 {
		entri.refs--
	}

	if entri.refs == 0 && keterangan > stderrfd {
		if entri.jenis == fdJenisSoket && entri.aux < makssockets {
			lokalsockets[entri.aux] = lokaldatagramSoket{}
		}
		*entri = bukaBerkasKeterangan{}
	}
}

func tutupProsesfd(proses *prosesentri, fd int32) int32 {
	if proses == nil || getBukaBerkasfor(proses, fd) == nil {
		return Ebadf
	}
	keterangan := proses.fds[fd].keterangan
	proses.fds[fd] = fdentri{}
	releaseBukaBerkas(keterangan)
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
	entri := getBukaBerkas(fd)
	if entri == nil {
		return Ebadf
	}
	if entri.jenis != fdJenisconsole {
		if entri.jenis == fdJenisSoket {
			return soketKirimto(fd, address, count, 0, 0)
		}
		if entri.jenis == fdJenisfat || entri.jenis == fdJenisAkarDirektori {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefromPenunjuk(uintptr(address), int(count), int(count))
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
	entri := getBukaBerkas(fd)
	if entri == nil {
		return Ebadf
	}
	if entri.jenis == fdJenisstdin {
		return bacastdin(address, count)
	}
	if entri.jenis == fdJenisAkarDirektori {
		return Eisdir
	}
	if entri.jenis == fdJenisSoket {
		return soketreceivefrom(fd, address, count, 0, 0)
	}
	if entri.jenis != fdJenisfat {
		return Ebadf
	}
	if entri.posisi >= entri.ukuran {
		return 0
	}
	remaining := entri.ukuran - entri.posisi
	if count > remaining {
		count = remaining
	}
	buffer := GetBytefromPenunjuk(uintptr(address), int(count), int(count))
	return bacavfsBerkas(entri, buffer, count)
}

func sysBuka(aluraddress uint32, tanda uint32, mode uint32) int32 {
	_ = mode
	if aluraddress == 0 {
		return Efault
	}
	aksesmode := tanda & 3
	if aksesmode == oTulisonly || aksesmode == oBacaTulis || (tanda&(ocreate|oPenggal|oappend)) != 0 {
		return Erofs
	}

	proses := ensureSekarangProses()
	if proses == nil {
		return Enfile
	}
	keterangan := allocateBukaBerkas()
	if keterangan < 0 {
		return keterangan
	}
	entri := &bukaBerkasTabel[keterangan]
	entri.tanda = tanda
	if isAkarAlur(aluraddress) {
		entri.jenis = fdJenisAkarDirektori
		entri.ukuran = 0
	} else {
		namalen, nama := salinAlur(aluraddress)
		if namalen == 0 {
			*entri = bukaBerkasKeterangan{}
			return Enoent
		}
		ukuran := berkasUkuran(nama[:namalen])
		if ukuran == 0 {
			*entri = bukaBerkasKeterangan{}
			return Enoent
		}
		if (tanda & oDirektori) != 0 {
			*entri = bukaBerkasKeterangan{}
			return Enotdir
		}
		entri.jenis = fdJenisfat
		entri.ukuran = ukuran
		entri.namalen = namalen
		entri.nama = nama
	}

	fd := allocatefd(proses, keterangan, 3)
	if fd < 0 {
		*entri = bukaBerkasKeterangan{}
		return fd
	}
	return fd
}

func sysTutup(fd int32) int32 {
	return tutupProsesfd(ensureSekarangProses(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	proses := ensureSekarangProses()
	entri := getBukaBerkasfor(proses, fd)
	if entri == nil {
		return Ebadf
	}
	barufd := allocatefd(proses, proses.fds[fd].keterangan, minimum)
	if barufd >= 0 {
		entri.refs++
	}
	return barufd
}

func sysdup2(oldfd int32, barufd int32) int32 {
	proses := ensureSekarangProses()
	entri := getBukaBerkasfor(proses, oldfd)
	if entri == nil {
		return Ebadf
	}
	if barufd < 0 || barufd >= maksfd {
		return Ebadf
	}
	if oldfd == barufd {
		return barufd
	}
	if proses.fds[barufd].dipakai {
		tutupProsesfd(proses, barufd)
	}
	proses.fds[barufd] = fdentri{dipakai: true, keterangan: proses.fds[oldfd].keterangan}
	entri.refs++
	return barufd
}

func sysfcntl(fd int32, perintah uint32, argument uint32) int32 {
	proses := ensureSekarangProses()
	entri := getBukaBerkasfor(proses, fd)
	if entri == nil {
		return Ebadf
	}
	switch perintah {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proses.fds[fd].fdTanda)
	case fAturfd:
		proses.fds[fd].fdTanda = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entri.tanda)
	case fAturfl:
		entri.tanda = (entri.tanda & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entri := getBukaBerkas(fd)
	if entri == nil {
		return Ebadf
	}
	if entri.jenis != fdJenisfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekAtur:
		base = 0
	case seekSekarang:
		base = int64(entri.posisi)
	case seekAkhir:
		base = int64(entri.ukuran)
	default:
		return Einval
	}
	posisi_2 := base + int64(offset)
	if posisi_2 < 0 || posisi_2 > 0x7FFFFFFF {
		return Einval
	}
	entri.posisi = uint32(posisi_2)
	return int32(entri.posisi)
}

func bacavfsBerkas(entri *bukaBerkasKeterangan, tujuan_2 []byte, count uint32) int32 {
	memorimanager := &mem.TMemorimanager{}
	tmpPenunjuk := memorimanager.Alokasikan_memori(entri.ukuran)
	if tmpPenunjuk == nil {
		return Einval
	}
	tmp := GetBytefromPenunjuk(uintptr(tmpPenunjuk), int(entri.ukuran), int(entri.ukuran))
	bacaBerkas(entri.nama[:entri.namalen], tmp)
	copy(tujuan_2[:count], tmp[entri.posisi:entri.posisi+count])
	entri.posisi += count
	memorimanager.Bebas(tmpPenunjuk)
	return int32(count)
}

func isAkarAlur(aluraddress uint32) bool {
	if aluraddress == 0 {
		return false
	}
	alur := GetBytefromPenunjuk(uintptr(aluraddress), 4, 4)
	if alur[0] == '/' && alur[1] == 0 {
		return true
	}
	if alur[0] == '.' && alur[1] == 0 {
		return true
	}
	if alur[0] == '/' && alur[1] == '.' && alur[2] == 0 {
		return true
	}
	return false
}

func sysakses(aluraddress uint32, mode uint32) int32 {
	if aluraddress == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isAkar := isAkarAlur(aluraddress)
	exists := isAkar
	if !exists {
		namalen, nama := salinAlur(aluraddress)
		exists = namalen != 0 && berkasUkuran(nama[:namalen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mode & 2) != 0 {
		return Eacces
	}

	if (mode&1) != 0 && !isAkar {
		return Eacces
	}
	return 0
}

func syschdir(aluraddress uint32) int32 {
	if aluraddress == 0 {
		return Efault
	}
	if !isAkarAlur(aluraddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, ukuran uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if ukuran < 2 {
		return Erange
	}
	buffer_2 := GetBytefromPenunjuk(uintptr(bufferaddress), int(ukuran), int(ukuran))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, ukuran uint32, inoda uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Perangkat = 1
	stat.Ino = inoda
	stat.Mode = mode
	stat.Nlink = 1
	stat.Ukuran_2 = int32(ukuran)
	stat.Blksize = 512
	stat.Blok = int32((ukuran + 511) / 512)
	return 0
}

func sysstat(aluraddress uint32, stataddress uint32) int32 {
	if aluraddress == 0 {
		return Efault
	}
	if isAkarAlur(aluraddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	namalen, nama := salinAlur(aluraddress)
	if namalen == 0 {
		return Enoent
	}
	ukuran := berkasUkuran(nama[:namalen])
	if ukuran == 0 {
		return Enoent
	}
	inoda := uint32(2)
	for i := uint32(0); i < namalen; i++ {
		inoda = inoda*33 + uint32(nama[i])
	}
	return fillposixstat(stataddress, sifreg|0444, ukuran, inoda)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entri := getBukaBerkas(fd)
	if entri == nil {
		return Ebadf
	}
	switch entri.jenis {
	case fdJenisstdin, fdJenisconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdJenisAkarDirektori:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdJenisfat:
		return fillposixstat(stataddress, sifreg|0444, entri.ukuran, uint32(fd+2))
	case fdJenisSoket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getBukaBerkas(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proses := ensureSekarangProses()
	if proses == nil {
		return 0
	}
	if proses.programbreak == 0 {
		proses.programbreak = penggunaheapbase
	}
	if address_2 == 0 {
		return proses.programbreak
	}
	if address_2 < penggunaheapbase || address_2 > penggunaheapBatas {
		return proses.programbreak
	}
	proses.programbreak = address_2
	return proses.programbreak
}

func salinutskolom(tujuan *[65]byte, nilai string) {
	batas := len(nilai)
	if batas > 64 {
		batas = 64
	}
	for i := 0; i < batas; i++ {
		tujuan[i] = nilai[i]
	}
	tujuan[batas] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	nama := (*posixutsname)(Pointer(uintptr(address_2)))
	*nama = posixutsname{}
	salinutskolom(&nama.Sysname, "EngOS")
	salinutskolom(&nama.Nodename, "engos")
	salinutskolom(&nama.Release, "0.1-posix")
	salinutskolom(&nama.Versi, "POSIX.1-2017 phase 1")
	salinutskolom(&nama.Machine, "i386")
	return 0
}

func swapunsignedinteger16(nilai uint16) uint16 {
	return (nilai << 8) | (nilai >> 8)
}

func soketcallargument(arguments_2 uint32, indeks uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + indeks*4)))
}

func soketforfd(fd int32) (*lokaldatagramSoket, int32) {
	entri := getBukaBerkas(fd)
	if entri == nil || entri.jenis != fdJenisSoket || entri.aux >= makssockets {
		return nil, Ebadf
	}
	soket := &lokalsockets[entri.aux]
	if !soket.dipakai {
		return nil, Ebadf
	}
	return soket, 0
}

func allocateSoket(domain uint32, soketTipe uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if soketTipe != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proses := ensureSekarangProses()
	if proses == nil {
		return Enfile
	}
	soketIndeks := -1
	for i := 0; i < makssockets; i++ {
		if !lokalsockets[i].dipakai {
			soketIndeks = i
			break
		}
	}
	if soketIndeks < 0 {
		return Enfile
	}
	keterangan := allocateBukaBerkas()
	if keterangan < 0 {
		return keterangan
	}
	lokalsockets[soketIndeks] = lokaldatagramSoket{dipakai: true}
	entri := &bukaBerkasTabel[keterangan]
	entri.jenis = fdJenisSoket
	entri.tanda = oBacaTulis
	entri.aux = uint32(soketIndeks)
	fd := allocatefd(proses, keterangan, 3)
	if fd < 0 {
		lokalsockets[soketIndeks] = lokaldatagramSoket{}
		*entri = bukaBerkasKeterangan{}
		return fd
	}
	return fd
}

func soketaddress(address_2 uint32, panjang uint32) (*soketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if panjang < 16 {
		return nil, Einval
	}
	hASIL := (*soketaddressipv4)(Pointer(uintptr(address_2)))
	if hASIL.Family != afinet {
		return nil, Eafnosupport
	}
	return hASIL, 0
}

func portMasukGunakan(port uint16, except *lokaldatagramSoket) bool {
	for i := 0; i < makssockets; i++ {
		soket := &lokalsockets[i]
		if soket != except && soket.dipakai && soket.bound && soket.lokal.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(soket *lokaldatagramSoket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(berikutnyaephemeralport)
		berikutnyaephemeralport++
		if berikutnyaephemeralport < 49152 {
			berikutnyaephemeralport = 49152
		}
		if !portMasukGunakan(port, soket) {
			soket.lokal = soketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			soket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func soketbind(fd int32, address_2 uint32, panjang uint32) int32 {
	soket, galat := soketforfd(fd)
	if galat != 0 {
		return galat
	}
	requested, galat := soketaddress(address_2, panjang)
	if galat != 0 {
		return galat
	}
	if soket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(soket)
	}
	if portMasukGunakan(requested.Port, soket) {
		return Eaddrinuse
	}
	soket.lokal = *requested
	soket.bound = true
	return 0
}

func soketSambung(fd int32, address_2 uint32, panjang uint32) int32 {
	soket, galat := soketforfd(fd)
	if galat != 0 {
		return galat
	}
	jauh, galat := soketaddress(address_2, panjang)
	if galat != 0 {
		return galat
	}
	if !soket.bound {
		if galat := bindephemeral(soket); galat != 0 {
			return galat
		}
	}
	soket.jauh = *jauh
	soket.connected = true
	return 0
}

func soketKirimto(fd int32, bufferaddress_2 uint32, panjang uint32, tujuanaddress uint32, tujuanPanjang uint32) int32 {
	soket, galat := soketforfd(fd)
	if galat != 0 {
		return galat
	}
	if panjang > maksdatagramUkuran {
		return Emsgsize
	}
	if panjang != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var tujuan soketaddressipv4
	if tujuanaddress != 0 {
		address_2, addressGalat := soketaddress(tujuanaddress, tujuanPanjang)
		if addressGalat != 0 {
			return addressGalat
		}
		tujuan = *address_2
	} else {
		if !soket.connected {
			return Enotconn
		}
		tujuan = soket.jauh
	}
	if !soket.bound {
		if bindGalat := bindephemeral(soket); bindGalat != 0 {
			return bindGalat
		}
	}
	var receiver *lokaldatagramSoket
	for i := 0; i < makssockets; i++ {
		candidate := &lokalsockets[i]
		if candidate.dipakai && candidate.bound && candidate.lokal.Port == tujuan.Port &&
			(candidate.lokal.Address == 0 || candidate.lokal.Address == tujuan.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksSoketpaket {
		return Eagain
	}
	packet := &receiver.paket[receiver.tail]
	*packet = soketpacket{dipakai: true, ukuran: panjang, sumber: soket.lokal}
	if panjang != 0 {
		sumber := GetBytefromPenunjuk(uintptr(bufferaddress_2), int(panjang), int(panjang))
		copy(packet.data[:panjang], sumber)
	}
	receiver.tail = (receiver.tail + 1) % maksSoketpaket
	receiver.count++
	return int32(panjang)
}

func soketreceivefrom(fd int32, bufferaddress_2 uint32, panjang uint32, sumberaddress uint32, sumberPanjangaddress uint32) int32 {
	soket, galat := soketforfd(fd)
	if galat != 0 {
		return galat
	}
	if panjang != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if soket.count == 0 {
		return Eagain
	}
	packet := &soket.paket[soket.head]
	salinPanjang := packet.ukuran
	if salinPanjang > panjang {
		salinPanjang = panjang
	}
	if salinPanjang != 0 {
		tujuan := GetBytefromPenunjuk(uintptr(bufferaddress_2), int(salinPanjang), int(salinPanjang))
		copy(tujuan, packet.data[:salinPanjang])
	}
	if sumberaddress != 0 {
		if sumberPanjangaddress == 0 {
			return Efault
		}
		providedPanjang := (*uint32)(Pointer(uintptr(sumberPanjangaddress)))
		if *providedPanjang >= 16 {
			*(*soketaddressipv4)(Pointer(uintptr(sumberaddress))) = packet.sumber
		}
		*providedPanjang = 16
	}
	*packet = soketpacket{}
	soket.head = (soket.head + 1) % maksSoketpaket
	soket.count--
	return int32(salinPanjang)
}

func salinSoketNama(fd int32, address_2 uint32, panjangaddress uint32, peer bool) int32 {
	soket, galat := soketforfd(fd)
	if galat != 0 {
		return galat
	}
	if address_2 == 0 || panjangaddress == 0 {
		return Efault
	}
	panjang := (*uint32)(Pointer(uintptr(panjangaddress)))
	if *panjang < 16 {
		*panjang = 16
		return Einval
	}
	if peer {
		if !soket.connected {
			return Enotconn
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.jauh
	} else {
		if !soket.bound {
			if bindGalat := bindephemeral(soket); bindGalat != 0 {
				return bindGalat
			}
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.lokal
	}
	*panjang = 16
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
		return soketKirimto(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return soketreceivefrom(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return soketKirimto(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), soketcallargument(arguments_2, 4), soketcallargument(arguments_2, 5))
	case 12:
		return soketreceivefrom(int32(soketcallargument(arguments_2, 0)), soketcallargument(arguments_2, 1), soketcallargument(arguments_2, 2), soketcallargument(arguments_2, 4), soketcallargument(arguments_2, 5))
	case 13:
		if _, galat := soketforfd(int32(soketcallargument(arguments_2, 0))); galat != 0 {
			return galat
		}
		return 0
	case 14:
		if _, galat := soketforfd(int32(soketcallargument(arguments_2, 0))); galat != 0 {
			return galat
		}
		return 0
	}
	return Eopnotsupp
}

func bacastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytefromPenunjuk(uintptr(address), int(count), int(count))
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
		sc := pollPapanketikscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinBaca]
	stdinBaca = (stdinBaca + 1) % uint32(len(stdinbuffer))
	return c
}

func pollPapanketikscancode() byte {
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

func salinexecvector(address_2 uint32, hASIL *execvector) int32 {
	*hASIL = execvector{}
	if address_2 == 0 {
		return 0
	}
	for indeks := uint32(0); indeks < maksexecvectorentri; indeks++ {
		benangaddress := *(*uint32)(Pointer(uintptr(address_2 + indeks*4)))
		if benangaddress == 0 {
			hASIL.count = indeks
			return 0
		}
		terminated := false
		for panjang := uint32(0); panjang <= maksexecBenangPanjang; panjang++ {
			nilai := *(*byte)(Pointer(uintptr(benangaddress + panjang)))
			hASIL.nilai_2[indeks][panjang] = nilai
			if nilai == 0 {
				hASIL.lengths[indeks] = panjang
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

func pushexecunsignedinteger32(memori_tumpukan *uint32, nilai uint32) {
	*memori_tumpukan -= 4
	*(*uint32)(Pointer(uintptr(*memori_tumpukan))) = nilai
}

func setupexecstack(cpu *TcpuStatus, arguments_2 *execvector, environment *execvector) int32 {
	const stackByte uint32 = 4096
	if !MakeCakupanprivatewritable(getcr3(), PenggunastackAtas-stackByte, stackByte) {
		return Enomem
	}
	memori_tumpukan := PenggunastackAtas
	var argumentpointers [maksexecvectorentri]uint32
	var environmentpointers [maksexecvectorentri]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		panjang := environment.lengths[i] + 1
		memori_tumpukan -= panjang
		tujuan := GetBytefromPenunjuk(uintptr(memori_tumpukan), int(panjang), int(panjang))
		copy(tujuan, environment.nilai_2[i][:panjang])
		environmentpointers[i] = memori_tumpukan
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		panjang := arguments_2.lengths[i] + 1
		memori_tumpukan -= panjang
		tujuan := GetBytefromPenunjuk(uintptr(memori_tumpukan), int(panjang), int(panjang))
		copy(tujuan, arguments_2.nilai_2[i][:panjang])
		argumentpointers[i] = memori_tumpukan
	}
	memori_tumpukan &= ^uint32(3)
	pushexecunsignedinteger32(&memori_tumpukan, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&memori_tumpukan, environmentpointers[i])
	}
	pushexecunsignedinteger32(&memori_tumpukan, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&memori_tumpukan, argumentpointers[i])
	}
	pushexecunsignedinteger32(&memori_tumpukan, arguments_2.count)
	cpu.Esp = memori_tumpukan
	cpu.Ebp = 0
	return 0
}

func tutupHidupexec(proses *prosesentri) {
	if proses == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proses.fds[fd].dipakai && (proses.fds[fd].fdTanda&fdcloexec) != 0 {
			tutupProsesfd(proses, fd)
		}
	}
}

func sysexecve(cpu *TcpuStatus, aluraddress uint32) int32 {
	if aluraddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if hASIL := salinexecvector(cpu.Ecx, &arguments_2); hASIL < 0 {
		return hASIL
	}
	if hASIL := salinexecvector(cpu.Edx, &environment); hASIL < 0 {
		return hASIL
	}
	namalen, nama := salinAlur(aluraddress)
	if namalen == 0 {
		return Enoent
	}
	ukuran := berkasUkuran(nama[:namalen])
	if ukuran == 0 {
		return Enoent
	}
	memorimanager := &mem.TMemorimanager{}
	berkasPenunjuk := memorimanager.Alokasikan_memori(ukuran)
	if berkasPenunjuk == nil {
		return Einval
	}
	data := GetBytefromPenunjuk(uintptr(berkasPenunjuk), int(ukuran), int(ukuran))
	bacaBerkas(nama[:namalen], data)
	if ukuran < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorimanager.Bebas(berkasPenunjuk)
		return Enoexec
	}
	loader := Elf{}
	entri := loader.Getentri(data)
	loader.Parse(data, getcr3())
	memorimanager.Bebas(berkasPenunjuk)
	if hASIL := setupexecstack(cpu, &arguments_2, &environment); hASIL < 0 {
		return hASIL
	}
	tutupHidupexec(ensureSekarangProses())
	cpu.Eip = entri
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStatus) int32 {
	orangtuapid := Sekarangpid()
	if ensureSekarangProses() == nil {
		return Enfile
	}
	pid := allocateProses(orangtuapid)
	if pid == 0 {
		return Einval
	}
	memorimanager := &mem.TMemorimanager{}
	threadPenunjuk := memorimanager.Alokasikan_memori(uint32(Sizeof(TThread{})))
	stackPenunjuk := memorimanager.Alokasikan_memori(ThreadstackUkuran)
	anakHalamanDirektori := CloneaddressSpasicow(getcr3())
	if threadPenunjuk == nil || stackPenunjuk == nil || anakHalamanDirektori == 0 {
		discardProses(pid)
		return Einval
	}
	anak := (*TThread)(threadPenunjuk)
	anak.Stack = uint32(uintptr(stackPenunjuk))
	anak.CpuStatus = (*TcpuStatus)(Pointer(uintptr(stackPenunjuk) + ThreadstackUkuran - Sizeof(TcpuStatus{})))
	*anak.CpuStatus = *cpu
	anak.CpuStatus.Eax = 0
	anak.Penggunastack_2 = cpu.Esp
	anak.PenggunastackUkuran_2 = 0
	anak.Pid = pid
	anak.Orangtuapid = orangtuapid
	anak.HalamanDirektorientri = anakHalamanDirektori
	anak.ThreadStatus = Siap
	anak.Fpuoffset = 0xffffffff
	anak.Iskernel = false
	Tambahrunnablethread(anak)
	return int32(pid)
}

func sysKeluar(status uint32) {
	pid := Sekarangpid()
	for i := 0; i < len(prosesTabel); i++ {
		if prosesTabel[i].dipakai && prosesTabel[i].pid == pid {
			tutupSemuaProsesfds(&prosesTabel[i])
			prosesTabel[i].keluar = true
			prosesTabel[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statusaddress uint32, opsi uint32) int32 {
	if (opsi & ^uint32(1)) != 0 {
		return Einval
	}
	orangtuapid := Sekarangpid()
	foundanak := false
	for i := 0; i < len(prosesTabel); i++ {
		p := &prosesTabel[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.dipakai && matches && p.orangtua == orangtuapid {
			foundanak = true
			if p.keluar {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				anakpid := p.pid
				*p = prosesentri{}
				return int32(anakpid)
			}
		}
	}
	if !foundanak {
		return Echild
	}

	if (opsi & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProses(orangtua uint32) uint32 {
	orangtuaProses := cariProses(orangtua)
	pid := Allocatepid()
	for i := 0; i < len(prosesTabel); i++ {
		if !prosesTabel[i].dipakai {
			prosesTabel[i] = prosesentri{
				dipakai:	true,
				pid:		pid,
				orangtua:	orangtua,
				programbreak:	penggunaheapbase,
			}
			if orangtuaProses != nil {
				prosesTabel[i].programbreak = orangtuaProses.programbreak
				for fd := 0; fd < maksfd; fd++ {
					if orangtuaProses.fds[fd].dipakai {
						prosesTabel[i].fds[fd] = orangtuaProses.fds[fd]
						keterangan := orangtuaProses.fds[fd].keterangan
						if keterangan >= 0 && keterangan < maksBukaBERKAS {
							bukaBerkasTabel[keterangan].refs++
						}
					}
				}
			} else {
				initializeProsesfds(&prosesTabel[i])
			}
			return pid
		}
	}
	return 0
}

func tutupSemuaProsesfds(proses *prosesentri) {
	if proses == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if proses.fds[fd].dipakai {
			tutupProsesfd(proses, fd)
		}
	}
}

func discardProses(pid uint32) {
	proses := cariProses(pid)
	if proses == nil {
		return
	}
	tutupSemuaProsesfds(proses)
	*proses = prosesentri{}
}

func salinAlur(aluraddress uint32) (uint32, [12]byte) {
	var nama [12]byte
	if aluraddress == 0 {
		return 0, nama
	}
	raw := GetBytefromPenunjuk(uintptr(aluraddress), 64, 64)
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

func berkasUkuran(namaberkas []byte) uint32 {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_berkas32{}
	ukuran := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namaberkas)
	ata0s.Flush()
	return ukuran
}

func bacaBerkas(namaberkas []byte, data []byte) {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_berkas32{}
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namaberkas, data)
	ata0s.Flush()
}

func getcr3() uint32
