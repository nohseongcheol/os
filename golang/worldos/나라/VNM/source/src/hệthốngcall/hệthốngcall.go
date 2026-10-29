/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package hệthốngcall

import . "unsafe"

import . "giánđoạn"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "tậptinHệthống/msdospartition"
import . "tậptinHệthống/fat"
import . "tậptinHệthống/định_dạng_thực_thi_và_liên_kết"
import mem "bộnhớmanager"
import . "paging"
import . "cổng"
import . "tasking/scheduler"
import . "tasking/thread"
import . "ảoBộnhớ"

var console_2 = TConsole{}

type TSyscall struct {
	TGiánđoạnhandler
}

const (
	SysThoát	uint32	= 1
	Sysfork		uint32	= 2
	SysĐọc		uint32	= 3
	SysGhi		uint32	= 4
	SysMở		uint32	= 5
	SysĐóng		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Systruycập	uint32	= 33
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
	SysrtThoát	uint32	= 252

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
	stdinTả		int32	= 0
	stdoutTả	int32	= 1
	stderrTả	int32	= 2
	maxTả			= 32
	maxMởfiles		= 128
)

type tảentry struct {
	dùng	bool
	môtả	int32
	tảCờ	uint32
}

type mởTậptinMôtả struct {
	dùng	bool
	refs	uint32
	kind	uint32
	cờ	uint32
	vịtrí	uint32
	cỡ	uint32
	tên	[12]byte
	tênlen	uint32
	aux	uint32
}

const (
	tảkindKhông	uint32	= 0
	tảkindfat	uint32	= 1
	tảkindstdin	uint32	= 2
	tảkindconsole	uint32	= 3
	tảkindGốcThưmục	uint32	= 4
	tảkindsocket	uint32	= 5

	oĐọconly	uint32	= 0
	oGhionly	uint32	= 1
	oĐọcGhi		uint32	= 2
	ocreate		uint32	= 0x40
	oCắt		uint32	= 0x200
	oappend		uint32	= 0x400
	oThưmục		uint32	= 0x10000

	seekĐặt		uint32	= 0
	seekHiệnhành	uint32	= 1
	seekKếtthúc	uint32	= 2

	fdupTả		uint32	= 0
	fgetTả		uint32	= 1
	fĐặtTả		uint32	= 2
	fgetfl		uint32	= 3
	fĐặtfl		uint32	= 4
	tảcloexec	uint32	= 1

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
	maxsocketcácgói	= 8
	maxdatagramCỡ	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Cổng	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	dùng	bool
	cỡ	uint32
	mãnguồn	socketaddressipv4
	data	[maxdatagramCỡ]byte
}

type cụcbộdatagramsocket struct {
	dùng		bool
	bound		bool
	connected	bool
	cụcbộ		socketaddressipv4
	từxa		socketaddressipv4
	head		uint32
	tail		uint32
	sốlượng		uint32
	cácgói		[maxsocketcácgói]socketpacket
}

type posixstat struct {
	Thiếtbị		uint32
	Ino		uint32
	Chếđộ		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Cỡ_2		int32
	Blksize		int32
	Tắcnghẽn	int32
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
	Phiênbản	[65]byte
	Machine		[65]byte
}

const (
	maxChạyvectorentry	= 16
	maxChạyCHUỖIĐộdài	= 63
)

type chạyvector struct {
	sốlượng	uint32
	lengths	[maxChạyvectorentry]uint32
	values	[maxChạyvectorentry][maxChạyCHUỖIĐộdài + 1]byte
}

type tiếntrìnhentry struct {
	dùng			bool
	pid			uint32
	mẹ			uint32
	exited			bool
	trạngthái		uint32
	chươngtrìnhbreak	uint32
	fds			[maxTả]tảentry
}

type cHUỖIheader struct {
	Data	uintptr
	Len	int
}

func syscallLỗi(lỗi int32) uint32 {
	return *(*uint32)(Pointer(&lỗi))
}

var mởTậptinBảng [maxMởfiles]mởTậptinMôtả
var tiếntrìnhBảng [32]tiếntrìnhentry
var cụcbộsockets [maxsockets]cụcbộdatagramsocket
var kếephemeralCổng uint16 = 49152

const (
	ngườidùngheapbase	uint32	= 0x06000000
	ngườidùngheapGiớihạn	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinĐọc uint32
var stdinGhi uint32

func Giánđoạn(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysThoát_2(chỉmục uint32) {
	Syscall(SysThoát, chỉmục)
}

func SysĐọc_2(tả uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysĐọc, tả, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysInstr(buffer string) {
	h := (*cHUỖIheader)(Pointer(&buffer))
	Syscall(SysGhi, uint32(stdoutTả), uint32(h.Data), uint32(h.Len))
}

func SysInunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysGhi, uint32(stdoutTả), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysMở_2(đƯỜNGDẪN uintptr, cờ uint32, chếđộ uint32) int32 {
	return int32(Syscall(SysMở, uint32(đƯỜNGDẪN), cờ, chếđộ))
}

func SysĐóng_2(tả uint32) int32 {
	return int32(Syscall(SysĐóng, tả))
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
		return Giánđoạn(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Giánđoạn(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Giánđoạn(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Giánđoạn(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Giánđoạn(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Giánđoạn(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallLỗi(Enosys)
	}
}

func (mình *TSyscall) Init(manager *TGiánđoạnmanager) {
	initTậptindescriptor()

	giánđoạnhandler = handleGiánđoạn

	var address uintptr
	address = uintptr(Pointer(&giánđoạnhandler))

	mình.TGiánđoạnhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var giánđoạnhandler func(uint32) uint32

func handleGiánđoạn(esp uint32) uint32 {
	var cpu = (*TcpuTrạngthái)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysThoát:
		sysThoát(cpu.Ebx)
		return uint32(uintptr(Pointer(DừngHiệnhànhthread(cpu))))
	case SysrtThoát:
		sysThoát(cpu.Ebx)
		return uint32(uintptr(Pointer(DừngHiệnhànhthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysĐọc:
		cpu.Eax = uint32(sysĐọc(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysGhi:
		cpu.Eax = uint32(sysGhi(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysMở:
		cpu.Eax = uint32(sysMở(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysMở(cpu.Ebx, ocreate|oGhionly|oCắt, cpu.Ecx))
		return esp
	case SysĐóng:
		cpu.Eax = uint32(sysĐóng(int32(cpu.Ebx)))
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
		cpu.Eax = Hiệnhànhpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Hiệnhànhmẹpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Systruycập:
		cpu.Eax = uint32(systruycập(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32In(cpu.Ebx)
		return esp

	default:
		console_2.MInxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32In(esp)
		console_2.MIn(([]byte)(":"))
		console_2.MUnsignedinteger32In(cpu.Eax)
		console_2.MIn(([]byte)(":"))
		console_2.MUnsignedinteger32In(cpu.Ebx)
		console_2.MIn(([]byte)(":"))
		console_2.MUnsignedinteger32In(cpu.Ecx)
		console_2.MIn(([]byte)(":"))
		console_2.MUnsignedinteger32In(cpu.Edx)
		console_2.MIn(([]byte)("]"))
		cpu.Eax = syscallLỗi(Enosys)
		return esp
	}

	return esp
}

func initTậptindescriptor() {
	for i := 0; i < maxMởfiles; i++ {
		mởTậptinBảng[i] = mởTậptinMôtả{}
	}
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		tiếntrìnhBảng[i] = tiếntrìnhentry{}
	}
	for i := 0; i < len(cụcbộsockets); i++ {
		cụcbộsockets[i] = cụcbộdatagramsocket{}
	}
	kếephemeralCổng = 49152
	mởTậptinBảng[0] = mởTậptinMôtả{dùng: true, kind: tảkindstdin, cờ: oĐọconly}
	mởTậptinBảng[1] = mởTậptinMôtả{dùng: true, kind: tảkindconsole, cờ: oGhionly}
	mởTậptinBảng[2] = mởTậptinMôtả{dùng: true, kind: tảkindconsole, cờ: oGhionly}
}

func tìmTiếntrình(pid uint32) *tiếntrìnhentry {
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		if tiếntrìnhBảng[i].dùng && tiếntrìnhBảng[i].pid == pid {
			return &tiếntrìnhBảng[i]
		}
	}
	return nil
}

func initializeTiếntrìnhfds(tiếntrình *tiếntrìnhentry) {
	for tả := int32(0); tả <= stderrTả; tả++ {
		tiếntrình.fds[tả] = tảentry{dùng: true, môtả: tả}
		mởTậptinBảng[tả].refs++
	}
}

func ensureHiệnhànhTiếntrình() *tiếntrìnhentry {
	pid := Hiệnhànhpid()
	if tiếntrình := tìmTiếntrình(pid); tiếntrình != nil {
		return tiếntrình
	}
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		if !tiếntrìnhBảng[i].dùng {
			tiếntrìnhBảng[i] = tiếntrìnhentry{
				dùng:			true,
				pid:			pid,
				mẹ:			Hiệnhànhmẹpid(),
				chươngtrìnhbreak:	ngườidùngheapbase,
			}
			initializeTiếntrìnhfds(&tiếntrìnhBảng[i])
			return &tiếntrìnhBảng[i]
		}
	}
	return nil
}

func getMởTậptinfor(tiếntrình *tiếntrìnhentry, tả int32) *mởTậptinMôtả {
	if tiếntrình == nil || tả < 0 || tả >= maxTả || !tiếntrình.fds[tả].dùng {
		return nil
	}
	môtả := tiếntrình.fds[tả].môtả
	if môtả < 0 || môtả >= maxMởfiles || !mởTậptinBảng[môtả].dùng {
		return nil
	}
	return &mởTậptinBảng[môtả]
}

func getMởTậptin(tả int32) *mởTậptinMôtả {
	return getMởTậptinfor(ensureHiệnhànhTiếntrình(), tả)
}

func allocateMởTậptin() int32 {
	for i := int32(3); i < maxMởfiles; i++ {
		if !mởTậptinBảng[i].dùng {
			mởTậptinBảng[i] = mởTậptinMôtả{dùng: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateTả(tiếntrình *tiếntrìnhentry, môtả int32, tốithiểu int32) int32 {
	if tiếntrình == nil {
		return Enfile
	}
	if tốithiểu < 0 || tốithiểu >= maxTả {
		return Einval
	}
	for tả := tốithiểu; tả < maxTả; tả++ {
		if !tiếntrình.fds[tả].dùng {
			tiếntrình.fds[tả] = tảentry{dùng: true, môtả: môtả}
			return tả
		}
	}
	return Emfile
}

func releaseMởTậptin(môtả int32) {
	if môtả < 0 || môtả >= maxMởfiles {
		return
	}
	entry := &mởTậptinBảng[môtả]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && môtả > stderrTả {
		if entry.kind == tảkindsocket && entry.aux < maxsockets {
			cụcbộsockets[entry.aux] = cụcbộdatagramsocket{}
		}
		*entry = mởTậptinMôtả{}
	}
}

func đóngTiếntrìnhTả(tiếntrình *tiếntrìnhentry, tả int32) int32 {
	if tiếntrình == nil || getMởTậptinfor(tiếntrình, tả) == nil {
		return Ebadf
	}
	môtả := tiếntrình.fds[tả].môtả
	tiếntrình.fds[tả] = tảentry{}
	releaseMởTậptin(môtả)
	return 0
}

func sysGhi(tả int32, address uint32, sốlượng uint32) int32 {
	if sốlượng == 0 {
		return 0
	}
	if address == 0 || address+sốlượng < address {
		return Efault
	}
	if sốlượng > 4096 {
		return Einval
	}
	entry := getMởTậptin(tả)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != tảkindconsole {
		if entry.kind == tảkindsocket {
			return socketGởito(tả, address, sốlượng, 0, 0)
		}
		if entry.kind == tảkindfat || entry.kind == tảkindGốcThưmục {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefromContrỏ(uintptr(address), int(sốlượng), int(sốlượng))
	console_2.MIn(buffer)
	return int32(sốlượng)
}

func sysĐọc(tả int32, address uint32, sốlượng uint32) int32 {
	if sốlượng == 0 {
		return 0
	}
	if address == 0 || address+sốlượng < address {
		return Efault
	}
	entry := getMởTậptin(tả)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == tảkindstdin {
		return đọcstdin(address, sốlượng)
	}
	if entry.kind == tảkindGốcThưmục {
		return Eisdir
	}
	if entry.kind == tảkindsocket {
		return socketreceivefrom(tả, address, sốlượng, 0, 0)
	}
	if entry.kind != tảkindfat {
		return Ebadf
	}
	if entry.vịtrí >= entry.cỡ {
		return 0
	}
	remaining := entry.cỡ - entry.vịtrí
	if sốlượng > remaining {
		sốlượng = remaining
	}
	buffer := GetBytefromContrỏ(uintptr(address), int(sốlượng), int(sốlượng))
	return đọcvfsTậptin(entry, buffer, sốlượng)
}

func sysMở(đƯỜNGDẪNaddress uint32, cờ uint32, chếđộ uint32) int32 {
	_ = chếđộ
	if đƯỜNGDẪNaddress == 0 {
		return Efault
	}
	truycậpChếđộ := cờ & 3
	if truycậpChếđộ == oGhionly || truycậpChếđộ == oĐọcGhi || (cờ&(ocreate|oCắt|oappend)) != 0 {
		return Erofs
	}

	tiếntrình := ensureHiệnhànhTiếntrình()
	if tiếntrình == nil {
		return Enfile
	}
	môtả := allocateMởTậptin()
	if môtả < 0 {
		return môtả
	}
	entry := &mởTậptinBảng[môtả]
	entry.cờ = cờ
	if isGốcĐƯỜNGDẪN(đƯỜNGDẪNaddress) {
		entry.kind = tảkindGốcThưmục
		entry.cỡ = 0
	} else {
		tênlen, tên := saochépĐƯỜNGDẪN(đƯỜNGDẪNaddress)
		if tênlen == 0 {
			*entry = mởTậptinMôtả{}
			return Enoent
		}
		cỡ := tậptinCỡ(tên[:tênlen])
		if cỡ == 0 {
			*entry = mởTậptinMôtả{}
			return Enoent
		}
		if (cờ & oThưmục) != 0 {
			*entry = mởTậptinMôtả{}
			return Enotdir
		}
		entry.kind = tảkindfat
		entry.cỡ = cỡ
		entry.tênlen = tênlen
		entry.tên = tên
	}

	tả := allocateTả(tiếntrình, môtả, 3)
	if tả < 0 {
		*entry = mởTậptinMôtả{}
		return tả
	}
	return tả
}

func sysĐóng(tả int32) int32 {
	return đóngTiếntrìnhTả(ensureHiệnhànhTiếntrình(), tả)
}

func sysdup(tả int32, tốithiểu int32) int32 {
	tiếntrình := ensureHiệnhànhTiếntrình()
	entry := getMởTậptinfor(tiếntrình, tả)
	if entry == nil {
		return Ebadf
	}
	mớiTả := allocateTả(tiếntrình, tiếntrình.fds[tả].môtả, tốithiểu)
	if mớiTả >= 0 {
		entry.refs++
	}
	return mớiTả
}

func sysdup2(oldTả int32, mớiTả int32) int32 {
	tiếntrình := ensureHiệnhànhTiếntrình()
	entry := getMởTậptinfor(tiếntrình, oldTả)
	if entry == nil {
		return Ebadf
	}
	if mớiTả < 0 || mớiTả >= maxTả {
		return Ebadf
	}
	if oldTả == mớiTả {
		return mớiTả
	}
	if tiếntrình.fds[mớiTả].dùng {
		đóngTiếntrìnhTả(tiếntrình, mớiTả)
	}
	tiếntrình.fds[mớiTả] = tảentry{dùng: true, môtả: tiếntrình.fds[oldTả].môtả}
	entry.refs++
	return mớiTả
}

func sysfcntl(tả int32, lệnh uint32, argument uint32) int32 {
	tiếntrình := ensureHiệnhànhTiếntrình()
	entry := getMởTậptinfor(tiếntrình, tả)
	if entry == nil {
		return Ebadf
	}
	switch lệnh {
	case fdupTả:
		return sysdup(tả, int32(argument))
	case fgetTả:
		return int32(tiếntrình.fds[tả].tảCờ)
	case fĐặtTả:
		tiếntrình.fds[tả].tảCờ = argument & tảcloexec
		return 0
	case fgetfl:
		return int32(entry.cờ)
	case fĐặtfl:
		entry.cờ = (entry.cờ & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(tả int32, offset int32, whence uint32) int32 {
	entry := getMởTậptin(tả)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != tảkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekĐặt:
		base = 0
	case seekHiệnhành:
		base = int64(entry.vịtrí)
	case seekKếtthúc:
		base = int64(entry.cỡ)
	default:
		return Einval
	}
	vịtrí_2 := base + int64(offset)
	if vịtrí_2 < 0 || vịtrí_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.vịtrí = uint32(vịtrí_2)
	return int32(entry.vịtrí)
}

func đọcvfsTậptin(entry *mởTậptinMôtả, destination_2 []byte, sốlượng uint32) int32 {
	bộnhớmanager := &mem.TBộnhớmanager{}
	tmpContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(entry.cỡ)
	if tmpContrỏ == nil {
		return Einval
	}
	tmp := GetBytefromContrỏ(uintptr(tmpContrỏ), int(entry.cỡ), int(entry.cỡ))
	đọcTậptin(entry.tên[:entry.tênlen], tmp)
	copy(destination_2[:sốlượng], tmp[entry.vịtrí:entry.vịtrí+sốlượng])
	entry.vịtrí += sốlượng
	bộnhớmanager.Rảnh(tmpContrỏ)
	return int32(sốlượng)
}

func isGốcĐƯỜNGDẪN(đƯỜNGDẪNaddress uint32) bool {
	if đƯỜNGDẪNaddress == 0 {
		return false
	}
	đƯỜNGDẪN := GetBytefromContrỏ(uintptr(đƯỜNGDẪNaddress), 4, 4)
	if đƯỜNGDẪN[0] == '/' && đƯỜNGDẪN[1] == 0 {
		return true
	}
	if đƯỜNGDẪN[0] == '.' && đƯỜNGDẪN[1] == 0 {
		return true
	}
	if đƯỜNGDẪN[0] == '/' && đƯỜNGDẪN[1] == '.' && đƯỜNGDẪN[2] == 0 {
		return true
	}
	return false
}

func systruycập(đƯỜNGDẪNaddress uint32, chếđộ uint32) int32 {
	if đƯỜNGDẪNaddress == 0 {
		return Efault
	}
	if (chếđộ & ^uint32(7)) != 0 {
		return Einval
	}
	isGốc := isGốcĐƯỜNGDẪN(đƯỜNGDẪNaddress)
	exists := isGốc
	if !exists {
		tênlen, tên := saochépĐƯỜNGDẪN(đƯỜNGDẪNaddress)
		exists = tênlen != 0 && tậptinCỡ(tên[:tênlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (chếđộ & 2) != 0 {
		return Eacces
	}

	if (chếđộ&1) != 0 && !isGốc {
		return Eacces
	}
	return 0
}

func syschdir(đƯỜNGDẪNaddress uint32) int32 {
	if đƯỜNGDẪNaddress == 0 {
		return Efault
	}
	if !isGốcĐƯỜNGDẪN(đƯỜNGDẪNaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, cỡ uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if cỡ < 2 {
		return Erange
	}
	buffer_2 := GetBytefromContrỏ(uintptr(bufferaddress), int(cỡ), int(cỡ))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, chếđộ uint32, cỡ uint32, nútthôngtin uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Thiếtbị = 1
	stat.Ino = nútthôngtin
	stat.Chếđộ = chếđộ
	stat.Nlink = 1
	stat.Cỡ_2 = int32(cỡ)
	stat.Blksize = 512
	stat.Tắcnghẽn = int32((cỡ + 511) / 512)
	return 0
}

func sysstat(đƯỜNGDẪNaddress uint32, stataddress uint32) int32 {
	if đƯỜNGDẪNaddress == 0 {
		return Efault
	}
	if isGốcĐƯỜNGDẪN(đƯỜNGDẪNaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	tênlen, tên := saochépĐƯỜNGDẪN(đƯỜNGDẪNaddress)
	if tênlen == 0 {
		return Enoent
	}
	cỡ := tậptinCỡ(tên[:tênlen])
	if cỡ == 0 {
		return Enoent
	}
	nútthôngtin := uint32(2)
	for i := uint32(0); i < tênlen; i++ {
		nútthôngtin = nútthôngtin*33 + uint32(tên[i])
	}
	return fillposixstat(stataddress, sifreg|0444, cỡ, nútthôngtin)
}

func sysfstat(tả int32, stataddress uint32) int32 {
	entry := getMởTậptin(tả)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case tảkindstdin, tảkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(tả+1))
	case tảkindGốcThưmục:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case tảkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.cỡ, uint32(tả+2))
	case tảkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(tả+2))
	}
	return Ebadf
}

func sysfsync(tả int32) int32 {
	if getMởTậptin(tả) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	tiếntrình := ensureHiệnhànhTiếntrình()
	if tiếntrình == nil {
		return 0
	}
	if tiếntrình.chươngtrìnhbreak == 0 {
		tiếntrình.chươngtrìnhbreak = ngườidùngheapbase
	}
	if address_2 == 0 {
		return tiếntrình.chươngtrìnhbreak
	}
	if address_2 < ngườidùngheapbase || address_2 > ngườidùngheapGiớihạn {
		return tiếntrình.chươngtrìnhbreak
	}
	tiếntrình.chươngtrìnhbreak = address_2
	return tiếntrình.chươngtrìnhbreak
}

func saochéputsfield(destination *[65]byte, giátrị string) {
	giớihạn := len(giátrị)
	if giớihạn > 64 {
		giớihạn = 64
	}
	for i := 0; i < giớihạn; i++ {
		destination[i] = giátrị[i]
	}
	destination[giớihạn] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	tên := (*posixutsname)(Pointer(uintptr(address_2)))
	*tên = posixutsname{}
	saochéputsfield(&tên.Sysname, "EngOS")
	saochéputsfield(&tên.Nodename, "engos")
	saochéputsfield(&tên.Release, "0.1-posix")
	saochéputsfield(&tên.Phiênbản, "POSIX.1-2017 phase 1")
	saochéputsfield(&tên.Machine, "i386")
	return 0
}

func traođổiunsignedinteger16(giátrị uint16) uint16 {
	return (giátrị << 8) | (giátrị >> 8)
}

func socketcallargument(đốisố_2 uint32, chỉmục uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(đốisố_2 + chỉmục*4)))
}

func socketforTả(tả int32) (*cụcbộdatagramsocket, int32) {
	entry := getMởTậptin(tả)
	if entry == nil || entry.kind != tảkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &cụcbộsockets[entry.aux]
	if !socket.dùng {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(miền uint32, socketKiểu uint32, protocol uint32) int32 {
	if miền != afinet {
		return Eafnosupport
	}
	if socketKiểu != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	tiếntrình := ensureHiệnhànhTiếntrình()
	if tiếntrình == nil {
		return Enfile
	}
	socketChỉmục := -1
	for i := 0; i < maxsockets; i++ {
		if !cụcbộsockets[i].dùng {
			socketChỉmục = i
			break
		}
	}
	if socketChỉmục < 0 {
		return Enfile
	}
	môtả := allocateMởTậptin()
	if môtả < 0 {
		return môtả
	}
	cụcbộsockets[socketChỉmục] = cụcbộdatagramsocket{dùng: true}
	entry := &mởTậptinBảng[môtả]
	entry.kind = tảkindsocket
	entry.cờ = oĐọcGhi
	entry.aux = uint32(socketChỉmục)
	tả := allocateTả(tiếntrình, môtả, 3)
	if tả < 0 {
		cụcbộsockets[socketChỉmục] = cụcbộdatagramsocket{}
		*entry = mởTậptinMôtả{}
		return tả
	}
	return tả
}

func socketaddress(address_2 uint32, độdài uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if độdài < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func cổngVàoDùng(cổng uint16, except *cụcbộdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &cụcbộsockets[i]
		if socket != except && socket.dùng && socket.bound && socket.cụcbộ.Cổng == cổng {
			return true
		}
	}
	return false
}

func bindephemeral(socket *cụcbộdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		cổng := traođổiunsignedinteger16(kếephemeralCổng)
		kếephemeralCổng++
		if kếephemeralCổng < 49152 {
			kếephemeralCổng = 49152
		}
		if !cổngVàoDùng(cổng, socket) {
			socket.cụcbộ = socketaddressipv4{Family: afinet, Cổng: cổng, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(tả int32, address_2 uint32, độdài uint32) int32 {
	socket, lỗi := socketforTả(tả)
	if lỗi != 0 {
		return lỗi
	}
	requested, lỗi := socketaddress(address_2, độdài)
	if lỗi != 0 {
		return lỗi
	}
	if socket.bound {
		return Einval
	}
	if requested.Cổng == 0 {
		return bindephemeral(socket)
	}
	if cổngVàoDùng(requested.Cổng, socket) {
		return Eaddrinuse
	}
	socket.cụcbộ = *requested
	socket.bound = true
	return 0
}

func socketKếtnối(tả int32, address_2 uint32, độdài uint32) int32 {
	socket, lỗi := socketforTả(tả)
	if lỗi != 0 {
		return lỗi
	}
	từxa, lỗi := socketaddress(address_2, độdài)
	if lỗi != 0 {
		return lỗi
	}
	if !socket.bound {
		if lỗi := bindephemeral(socket); lỗi != 0 {
			return lỗi
		}
	}
	socket.từxa = *từxa
	socket.connected = true
	return 0
}

func socketGởito(tả int32, bufferaddress_2 uint32, độdài uint32, destinationaddress uint32, destinationĐộdài uint32) int32 {
	socket, lỗi := socketforTả(tả)
	if lỗi != 0 {
		return lỗi
	}
	if độdài > maxdatagramCỡ {
		return Emsgsize
	}
	if độdài != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressLỗi := socketaddress(destinationaddress, destinationĐộdài)
		if addressLỗi != 0 {
			return addressLỗi
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.từxa
	}
	if !socket.bound {
		if bindLỗi := bindephemeral(socket); bindLỗi != 0 {
			return bindLỗi
		}
	}
	var receiver *cụcbộdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &cụcbộsockets[i]
		if candidate.dùng && candidate.bound && candidate.cụcbộ.Cổng == destination.Cổng &&
			(candidate.cụcbộ.Address == 0 || candidate.cụcbộ.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.sốlượng >= maxsocketcácgói {
		return Eagain
	}
	packet := &receiver.cácgói[receiver.tail]
	*packet = socketpacket{dùng: true, cỡ: độdài, mãnguồn: socket.cụcbộ}
	if độdài != 0 {
		mãnguồn := GetBytefromContrỏ(uintptr(bufferaddress_2), int(độdài), int(độdài))
		copy(packet.data[:độdài], mãnguồn)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketcácgói
	receiver.sốlượng++
	return int32(độdài)
}

func socketreceivefrom(tả int32, bufferaddress_2 uint32, độdài uint32, mãnguồnaddress uint32, mãnguồnĐộdàiaddress uint32) int32 {
	socket, lỗi := socketforTả(tả)
	if lỗi != 0 {
		return lỗi
	}
	if độdài != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.sốlượng == 0 {
		return Eagain
	}
	packet := &socket.cácgói[socket.head]
	saochépĐộdài := packet.cỡ
	if saochépĐộdài > độdài {
		saochépĐộdài = độdài
	}
	if saochépĐộdài != 0 {
		destination := GetBytefromContrỏ(uintptr(bufferaddress_2), int(saochépĐộdài), int(saochépĐộdài))
		copy(destination, packet.data[:saochépĐộdài])
	}
	if mãnguồnaddress != 0 {
		if mãnguồnĐộdàiaddress == 0 {
			return Efault
		}
		providedĐộdài := (*uint32)(Pointer(uintptr(mãnguồnĐộdàiaddress)))
		if *providedĐộdài >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(mãnguồnaddress))) = packet.mãnguồn
		}
		*providedĐộdài = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketcácgói
	socket.sốlượng--
	return int32(saochépĐộdài)
}

func saochépsocketTên(tả int32, address_2 uint32, độdàiaddress uint32, peer bool) int32 {
	socket, lỗi := socketforTả(tả)
	if lỗi != 0 {
		return lỗi
	}
	if address_2 == 0 || độdàiaddress == 0 {
		return Efault
	}
	độdài := (*uint32)(Pointer(uintptr(độdàiaddress)))
	if *độdài < 16 {
		*độdài = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.từxa
	} else {
		if !socket.bound {
			if bindLỗi := bindephemeral(socket); bindLỗi != 0 {
				return bindLỗi
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.cụcbộ
	}
	*độdài = 16
	return 0
}

func syssocketcall(call uint32, đốisố_2 uint32) int32 {
	if đốisố_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(đốisố_2, 0), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2))
	case 3:
		return socketKếtnối(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return saochépsocketTên(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), false)
	case 7:
		return saochépsocketTên(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), true)
	case 9:
		return socketGởito(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), 0, 0)
	case 11:
		return socketGởito(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), socketcallargument(đốisố_2, 4), socketcallargument(đốisố_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(đốisố_2, 0)), socketcallargument(đốisố_2, 1), socketcallargument(đốisố_2, 2), socketcallargument(đốisố_2, 4), socketcallargument(đốisố_2, 5))
	case 13:
		if _, lỗi := socketforTả(int32(socketcallargument(đốisố_2, 0))); lỗi != 0 {
			return lỗi
		}
		return 0
	case 14:
		if _, lỗi := socketforTả(int32(socketcallargument(đốisố_2, 0))); lỗi != 0 {
			return lỗi
		}
		return 0
	}
	return Eopnotsupp
}

func đọcstdin(address uint32, sốlượng uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytefromContrỏ(uintptr(address), int(sốlượng), int(sốlượng))
	var n uint32
	for n < sốlượng {
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
	kế := (stdinGhi + 1) % uint32(len(stdinbuffer))
	if kế == stdinĐọc {
		return
	}
	stdinbuffer[stdinGhi] = c
	stdinGhi = kế
}

func stdingetblocking() byte {
	for stdinĐọc == stdinGhi {
		sc := pollBànphímscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinĐọc]
	stdinĐọc = (stdinĐọc + 1) % uint32(len(stdinbuffer))
	return c
}

func pollBànphímscancode() byte {
	for (CổngĐọcbyte(0x64) & 0x01) == 0 {
	}
	sc := CổngĐọcbyte(0x60)
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

func saochépChạyvector(address_2 uint32, result *chạyvector) int32 {
	*result = chạyvector{}
	if address_2 == 0 {
		return 0
	}
	for chỉmục := uint32(0); chỉmục < maxChạyvectorentry; chỉmục++ {
		cHUỖIaddress := *(*uint32)(Pointer(uintptr(address_2 + chỉmục*4)))
		if cHUỖIaddress == 0 {
			result.sốlượng = chỉmục
			return 0
		}
		terminated := false
		for độdài := uint32(0); độdài <= maxChạyCHUỖIĐộdài; độdài++ {
			giátrị := *(*byte)(Pointer(uintptr(cHUỖIaddress + độdài)))
			result.values[chỉmục][độdài] = giátrị
			if giátrị == 0 {
				result.lengths[chỉmục] = độdài
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

func pushChạyunsignedinteger32(bộ_nhớ_ngăn_xếp *uint32, giátrị uint32) {
	*bộ_nhớ_ngăn_xếp -= 4
	*(*uint32)(Pointer(uintptr(*bộ_nhớ_ngăn_xếp))) = giátrị
}

func setupChạystack(cpu *TcpuTrạngthái, đốisố_2 *chạyvector, environment *chạyvector) int32 {
	const stackByte uint32 = 4096
	if !MakePhạmviRiêngwritable(getcr3(), NgườidùngstackTrên-stackByte, stackByte) {
		return Enomem
	}
	bộ_nhớ_ngăn_xếp := NgườidùngstackTrên
	var argumentpointers [maxChạyvectorentry]uint32
	var environmentpointers [maxChạyvectorentry]uint32

	for i := int(environment.sốlượng) - 1; i >= 0; i-- {
		độdài := environment.lengths[i] + 1
		bộ_nhớ_ngăn_xếp -= độdài
		destination := GetBytefromContrỏ(uintptr(bộ_nhớ_ngăn_xếp), int(độdài), int(độdài))
		copy(destination, environment.values[i][:độdài])
		environmentpointers[i] = bộ_nhớ_ngăn_xếp
	}
	for i := int(đốisố_2.sốlượng) - 1; i >= 0; i-- {
		độdài := đốisố_2.lengths[i] + 1
		bộ_nhớ_ngăn_xếp -= độdài
		destination := GetBytefromContrỏ(uintptr(bộ_nhớ_ngăn_xếp), int(độdài), int(độdài))
		copy(destination, đốisố_2.values[i][:độdài])
		argumentpointers[i] = bộ_nhớ_ngăn_xếp
	}
	bộ_nhớ_ngăn_xếp &= ^uint32(3)
	pushChạyunsignedinteger32(&bộ_nhớ_ngăn_xếp, 0)
	for i := int(environment.sốlượng) - 1; i >= 0; i-- {
		pushChạyunsignedinteger32(&bộ_nhớ_ngăn_xếp, environmentpointers[i])
	}
	pushChạyunsignedinteger32(&bộ_nhớ_ngăn_xếp, 0)
	for i := int(đốisố_2.sốlượng) - 1; i >= 0; i-- {
		pushChạyunsignedinteger32(&bộ_nhớ_ngăn_xếp, argumentpointers[i])
	}
	pushChạyunsignedinteger32(&bộ_nhớ_ngăn_xếp, đốisố_2.sốlượng)
	cpu.Esp = bộ_nhớ_ngăn_xếp
	cpu.Ebp = 0
	return 0
}

func đóngBậtChạy(tiếntrình *tiếntrìnhentry) {
	if tiếntrình == nil {
		return
	}
	for tả := int32(0); tả < maxTả; tả++ {
		if tiếntrình.fds[tả].dùng && (tiếntrình.fds[tả].tảCờ&tảcloexec) != 0 {
			đóngTiếntrìnhTả(tiếntrình, tả)
		}
	}
}

func sysexecve(cpu *TcpuTrạngthái, đƯỜNGDẪNaddress uint32) int32 {
	if đƯỜNGDẪNaddress == 0 {
		return Efault
	}
	var đốisố_2 chạyvector
	var environment chạyvector
	if result := saochépChạyvector(cpu.Ecx, &đốisố_2); result < 0 {
		return result
	}
	if result := saochépChạyvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	tênlen, tên := saochépĐƯỜNGDẪN(đƯỜNGDẪNaddress)
	if tênlen == 0 {
		return Enoent
	}
	cỡ := tậptinCỡ(tên[:tênlen])
	if cỡ == 0 {
		return Enoent
	}
	bộnhớmanager := &mem.TBộnhớmanager{}
	tậptinContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	if tậptinContrỏ == nil {
		return Einval
	}
	data := GetBytefromContrỏ(uintptr(tậptinContrỏ), int(cỡ), int(cỡ))
	đọcTậptin(tên[:tênlen], data)
	if cỡ < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		bộnhớmanager.Rảnh(tậptinContrỏ)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	bộnhớmanager.Rảnh(tậptinContrỏ)
	if result := setupChạystack(cpu, &đốisố_2, &environment); result < 0 {
		return result
	}
	đóngBậtChạy(ensureHiệnhànhTiếntrình())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuTrạngthái) int32 {
	mẹpid := Hiệnhànhpid()
	if ensureHiệnhànhTiếntrình() == nil {
		return Enfile
	}
	pid := allocateTiếntrình(mẹpid)
	if pid == 0 {
		return Einval
	}
	bộnhớmanager := &mem.TBộnhớmanager{}
	threadContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(uint32(Sizeof(TThread{})))
	stackContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(ThreadstackCỡ)
	conTrangThưmục := Cloneaddressspacecow(getcr3())
	if threadContrỏ == nil || stackContrỏ == nil || conTrangThưmục == 0 {
		discardTiếntrình(pid)
		return Einval
	}
	con := (*TThread)(threadContrỏ)
	con.Stack = uint32(uintptr(stackContrỏ))
	con.CpuTrạngthái = (*TcpuTrạngthái)(Pointer(uintptr(stackContrỏ) + ThreadstackCỡ - Sizeof(TcpuTrạngthái{})))
	*con.CpuTrạngthái = *cpu
	con.CpuTrạngthái.Eax = 0
	con.Ngườidùngstack_2 = cpu.Esp
	con.NgườidùngstackCỡ_2 = 0
	con.Pid = pid
	con.Mẹpid = mẹpid
	con.TrangThưmụcentry = conTrangThưmục
	con.ThreadTrạngthái = Sẵnsàng
	con.Fpuoffset = 0xffffffff
	con.Iskernel = false
	Thêmrunnablethread(con)
	return int32(pid)
}

func sysThoát(trạngthái uint32) {
	pid := Hiệnhànhpid()
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		if tiếntrìnhBảng[i].dùng && tiếntrìnhBảng[i].pid == pid {
			đóngTấtcảTiếntrìnhfds(&tiếntrìnhBảng[i])
			tiếntrìnhBảng[i].exited = true
			tiếntrìnhBảng[i].trạngthái = (trạngthái & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, trạngtháiaddress uint32, tùychọn uint32) int32 {
	if (tùychọn & ^uint32(1)) != 0 {
		return Einval
	}
	mẹpid := Hiệnhànhpid()
	foundcon := false
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		p := &tiếntrìnhBảng[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.dùng && matches && p.mẹ == mẹpid {
			foundcon = true
			if p.exited {
				if trạngtháiaddress != 0 {
					*(*uint32)(Pointer(uintptr(trạngtháiaddress))) = p.trạngthái
				}
				conpid := p.pid
				*p = tiếntrìnhentry{}
				return int32(conpid)
			}
		}
	}
	if !foundcon {
		return Echild
	}

	if (tùychọn & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateTiếntrình(mẹ uint32) uint32 {
	mẹTiếntrình := tìmTiếntrình(mẹ)
	pid := Allocatepid()
	for i := 0; i < len(tiếntrìnhBảng); i++ {
		if !tiếntrìnhBảng[i].dùng {
			tiếntrìnhBảng[i] = tiếntrìnhentry{
				dùng:			true,
				pid:			pid,
				mẹ:			mẹ,
				chươngtrìnhbreak:	ngườidùngheapbase,
			}
			if mẹTiếntrình != nil {
				tiếntrìnhBảng[i].chươngtrìnhbreak = mẹTiếntrình.chươngtrìnhbreak
				for tả := 0; tả < maxTả; tả++ {
					if mẹTiếntrình.fds[tả].dùng {
						tiếntrìnhBảng[i].fds[tả] = mẹTiếntrình.fds[tả]
						môtả := mẹTiếntrình.fds[tả].môtả
						if môtả >= 0 && môtả < maxMởfiles {
							mởTậptinBảng[môtả].refs++
						}
					}
				}
			} else {
				initializeTiếntrìnhfds(&tiếntrìnhBảng[i])
			}
			return pid
		}
	}
	return 0
}

func đóngTấtcảTiếntrìnhfds(tiếntrình *tiếntrìnhentry) {
	if tiếntrình == nil {
		return
	}
	for tả := int32(0); tả < maxTả; tả++ {
		if tiếntrình.fds[tả].dùng {
			đóngTiếntrìnhTả(tiếntrình, tả)
		}
	}
}

func discardTiếntrình(pid uint32) {
	tiếntrình := tìmTiếntrình(pid)
	if tiếntrình == nil {
		return
	}
	đóngTấtcảTiếntrìnhfds(tiếntrình)
	*tiếntrình = tiếntrìnhentry{}
}

func saochépĐƯỜNGDẪN(đƯỜNGDẪNaddress uint32) (uint32, [12]byte) {
	var tên [12]byte
	if đƯỜNGDẪNaddress == 0 {
		return 0, tên
	}
	raw := GetBytefromContrỏ(uintptr(đƯỜNGDẪNaddress), 64, 64)
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
		tên[n] = c
		n++
	}
	return n, tên
}

func tậptinCỡ(têntậptin []byte) uint32 {
	var ata0s = TNângcaoCôngnghệattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionBảng{}
	partition.Đọcpartition(&ata0s)

	bios := TTham_số_hệ_thống_tệp32{}
	cỡ := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], têntậptin)
	ata0s.Flush()
	return cỡ
}

func đọcTậptin(têntậptin []byte, data []byte) {
	var ata0s = TNângcaoCôngnghệattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionBảng{}
	partition.Đọcpartition(&ata0s)

	bios := TTham_số_hệ_thống_tệp32{}
	bios.Đọc(&ata0s, partition.Mbr.Primarypartition[0], têntậptin, data)
	ata0s.Flush()
}

func getcr3() uint32
