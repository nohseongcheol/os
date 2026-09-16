/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 系統呼叫

import . "unsafe"

import . "中斷"
import . "控制台"
import . "工具"
import . "多重工作管理"
import . "驅動程式/ata"
import . "檔案系統/msdos分割區"
import . "檔案系統/fat"
import . "檔案系統/可執行與可連結格式"
import mem "記憶體管理器"
import . "分頁管理"
import . "連接埠"
import . "工作管理/排程器"
import . "工作管理/執行緒"
import . "虛擬記憶體"

var 控制台_2 = T控制台{}

type TSyscall struct {
	T中斷handler
}

const (
	Sys離開		uint32	= 1
	Sysfork		uint32	= 2
	Sys讀取		uint32	= 3
	Sys寫入		uint32	= 4
	Sys開啟		uint32	= 5
	Sys關閉		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sys存取		uint32	= 33
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
	Sysrt離開		uint32	= 252

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
	最大fd			= 32
	最大開啟檔案			= 128
)

type fd項目 struct {
	已使用	bool
	描述	int32
	fd旗標	uint32
}

type 開啟檔案描述 struct {
	已使用	bool
	refs	uint32
	種類	uint32
	旗標	uint32
	位置	uint32
	大小	uint32
	名稱	[12]byte
	名稱len	uint32
	aux	uint32
}

const (
	fd種類無		uint32	= 0
	fd種類fat		uint32	= 1
	fd種類stdin	uint32	= 2
	fd種類控制台		uint32	= 3
	fd種類根目錄目錄	uint32	= 4
	fd種類通訊端		uint32	= 5

	o讀取僅用	uint32	= 0
	o寫入僅用	uint32	= 1
	o讀取寫入	uint32	= 2
	o建立	uint32	= 0x40
	o截短	uint32	= 0x200
	oappend	uint32	= 0x400
	o目錄	uint32	= 0x10000

	seek設定	uint32	= 0
	seek目前	uint32	= 1
	seek結束	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	f設定fd		uint32	= 2
	fgetfl		uint32	= 3
	f設定fl		uint32	= 4
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
	最大sockets	= 32
	最大通訊端封包		= 8
	最大datagram大小	= 512
)

type 通訊端addressipv4 struct {
	Family	uint16
	P連接埠	uint16
	Address	uint32
	Z零	[8]byte
}

type 通訊端packet struct {
	已使用	bool
	大小	uint32
	來源	通訊端addressipv4
	資料	[最大datagram大小]byte
}

type 本地datagram通訊端 struct {
	已使用		bool
	bound		bool
	connected	bool
	本地		通訊端addressipv4
	遠端		通訊端addressipv4
	head		uint32
	tail		uint32
	計數		uint32
	封包		[最大通訊端封包]通訊端packet
}

type posixstat struct {
	D裝置		uint32
	Ino		uint32
	M模式		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	S大小_2		int32
	Blksize		int32
	B區塊		int32
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
	V版本		[65]byte
	Machine		[65]byte
}

const (
	最大執行vector項目	= 16
	最大執行字串長度	= 63
)

type 執行vector struct {
	計數	uint32
	lengths	[最大執行vector項目]uint32
	值	[最大執行vector項目][最大執行字串長度 + 1]byte
}

type 程序項目 struct {
	已使用	bool
	行程代碼	uint32
	parent	uint32
	已離開	bool
	狀態	uint32
	程式break	uint32
	fds	[最大fd]fd項目
}

type 字串標頭 struct {
	Data	uintptr
	Len	int
}

func syscall錯誤(出錯 int32) uint32 {
	return *(*uint32)(Pointer(&出錯))
}

var 開啟檔案table [最大開啟檔案]開啟檔案描述
var 程序table [32]程序項目
var 本地sockets [最大sockets]本地datagram通訊端
var 下一個ephemeral連接埠 uint16 = 49152

const (
	使用者heapbase	uint32	= 0x06000000
	使用者heap限制	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdin讀取 uint32
var stdin寫入 uint32

func I中斷(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sys離開_2(索引 uint32) {
	Syscall(Sys離開, 索引)
}

func Sys讀取_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sys讀取, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sys列印str(buffer string) {
	h := (*字串標頭)(Pointer(&buffer))
	Syscall(Sys寫入, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sys列印unsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sys寫入, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sys開啟_2(路徑 uintptr, 旗標 uint32, 模式 uint32) int32 {
	return int32(Syscall(Sys開啟, uint32(路徑), 旗標, 模式))
}

func Sys關閉_2(fd uint32) int32 {
	return int32(Syscall(Sys關閉, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(參數_3 ...uint32) uint32 {

	l := len(參數_3)
	switch l {
	case 1:
		return I中斷(參數_3[0], 0, 0, 0, 0, 0)
	case 2:
		return I中斷(參數_3[0], 參數_3[1], 0, 0, 0, 0)
	case 3:
		return I中斷(參數_3[0], 參數_3[1], 參數_3[2], 0, 0, 0)
	case 4:
		return I中斷(參數_3[0], 參數_3[1], 參數_3[2], 參數_3[3], 0, 0)
	case 5:
		return I中斷(參數_3[0], 參數_3[1], 參數_3[2], 參數_3[3], 參數_3[4], 0)
	case 6:
		return I中斷(參數_3[0], 參數_3[1], 參數_3[2], 參數_3[3], 參數_3[4], 參數_3[5])
	default:
		return syscall錯誤(Enosys)
	}
}

func (self *TSyscall) Init(管理器 *T中斷管理器) {
	init檔案descriptor()

	中斷handler = 控制把中斷

	var address uintptr
	address = uintptr(Pointer(&中斷handler))

	self.T中斷handler.Init(0x80, uintptr(Pointer(管理器)), address)
}

var 中斷handler func(uint32) uint32

func 控制把中斷(esp uint32) uint32 {
	var cpu = (*Tcpu狀態)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sys離開:
		sys離開(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止目前執行緒(cpu))))
	case Sysrt離開:
		sys離開(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止目前執行緒(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sys讀取:
		cpu.Eax = uint32(sys讀取(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys寫入:
		cpu.Eax = uint32(sys寫入(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys開啟:
		cpu.Eax = uint32(sys開啟(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sys開啟(cpu.Ebx, o建立|o寫入僅用|o截短, cpu.Ecx))
		return esp
	case Sys關閉:
		cpu.Eax = uint32(sys關閉(int32(cpu.Ebx)))
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
		cpu.Eax = C目前行程代碼()
		return esp
	case Sysgetppid:
		cpu.Eax = C目前parent行程代碼()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sys存取:
		cpu.Eax = uint32(sys存取(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sys通訊端呼叫(cpu.Ebx, cpu.Ecx))
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
		控制台_2.MUnsignedinteger32列印(cpu.Ebx)
		return esp

	default:
		控制台_2.M列印xy(([]byte)("sys["), 1, 23)
		控制台_2.MUnsignedinteger32列印(esp)
		控制台_2.M列印(([]byte)(":"))
		控制台_2.MUnsignedinteger32列印(cpu.Eax)
		控制台_2.M列印(([]byte)(":"))
		控制台_2.MUnsignedinteger32列印(cpu.Ebx)
		控制台_2.M列印(([]byte)(":"))
		控制台_2.MUnsignedinteger32列印(cpu.Ecx)
		控制台_2.M列印(([]byte)(":"))
		控制台_2.MUnsignedinteger32列印(cpu.Edx)
		控制台_2.M列印(([]byte)("]"))
		cpu.Eax = syscall錯誤(Enosys)
		return esp
	}

	return esp
}

func init檔案descriptor() {
	for i := 0; i < 最大開啟檔案; i++ {
		開啟檔案table[i] = 開啟檔案描述{}
	}
	for i := 0; i < len(程序table); i++ {
		程序table[i] = 程序項目{}
	}
	for i := 0; i < len(本地sockets); i++ {
		本地sockets[i] = 本地datagram通訊端{}
	}
	下一個ephemeral連接埠 = 49152
	開啟檔案table[0] = 開啟檔案描述{已使用: true, 種類: fd種類stdin, 旗標: o讀取僅用}
	開啟檔案table[1] = 開啟檔案描述{已使用: true, 種類: fd種類控制台, 旗標: o寫入僅用}
	開啟檔案table[2] = 開啟檔案描述{已使用: true, 種類: fd種類控制台, 旗標: o寫入僅用}
}

func 尋找程序(行程代碼 uint32) *程序項目 {
	for i := 0; i < len(程序table); i++ {
		if 程序table[i].已使用 && 程序table[i].行程代碼 == 行程代碼 {
			return &程序table[i]
		}
	}
	return nil
}

func initialize程序fds(程序 *程序項目) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		程序.fds[fd] = fd項目{已使用: true, 描述: fd}
		開啟檔案table[fd].refs++
	}
}

func ensure目前程序() *程序項目 {
	行程代碼 := C目前行程代碼()
	if 程序 := 尋找程序(行程代碼); 程序 != nil {
		return 程序
	}
	for i := 0; i < len(程序table); i++ {
		if !程序table[i].已使用 {
			程序table[i] = 程序項目{
				已使用:		true,
				行程代碼:		行程代碼,
				parent:		C目前parent行程代碼(),
				程式break:	使用者heapbase,
			}
			initialize程序fds(&程序table[i])
			return &程序table[i]
		}
	}
	return nil
}

func get開啟檔案for(程序 *程序項目, fd int32) *開啟檔案描述 {
	if 程序 == nil || fd < 0 || fd >= 最大fd || !程序.fds[fd].已使用 {
		return nil
	}
	描述 := 程序.fds[fd].描述
	if 描述 < 0 || 描述 >= 最大開啟檔案 || !開啟檔案table[描述].已使用 {
		return nil
	}
	return &開啟檔案table[描述]
}

func get開啟檔案(fd int32) *開啟檔案描述 {
	return get開啟檔案for(ensure目前程序(), fd)
}

func allocate開啟檔案() int32 {
	for i := int32(3); i < 最大開啟檔案; i++ {
		if !開啟檔案table[i].已使用 {
			開啟檔案table[i] = 開啟檔案描述{已使用: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(程序 *程序項目, 描述 int32, 最小值 int32) int32 {
	if 程序 == nil {
		return Enfile
	}
	if 最小值 < 0 || 最小值 >= 最大fd {
		return Einval
	}
	for fd := 最小值; fd < 最大fd; fd++ {
		if !程序.fds[fd].已使用 {
			程序.fds[fd] = fd項目{已使用: true, 描述: 描述}
			return fd
		}
	}
	return Emfile
}

func release開啟檔案(描述 int32) {
	if 描述 < 0 || 描述 >= 最大開啟檔案 {
		return
	}
	項目 := &開啟檔案table[描述]
	if 項目.refs > 0 {
		項目.refs--
	}

	if 項目.refs == 0 && 描述 > stderrfd {
		if 項目.種類 == fd種類通訊端 && 項目.aux < 最大sockets {
			本地sockets[項目.aux] = 本地datagram通訊端{}
		}
		*項目 = 開啟檔案描述{}
	}
}

func 關閉程序fd(程序 *程序項目, fd int32) int32 {
	if 程序 == nil || get開啟檔案for(程序, fd) == nil {
		return Ebadf
	}
	描述 := 程序.fds[fd].描述
	程序.fds[fd] = fd項目{}
	release開啟檔案(描述)
	return 0
}

func sys寫入(fd int32, address uint32, 計數 uint32) int32 {
	if 計數 == 0 {
		return 0
	}
	if address == 0 || address+計數 < address {
		return Efault
	}
	if 計數 > 4096 {
		return Einval
	}
	項目 := get開啟檔案(fd)
	if 項目 == nil {
		return Ebadf
	}
	if 項目.種類 != fd種類控制台 {
		if 項目.種類 == fd種類通訊端 {
			return 通訊端送出to(fd, address, 計數, 0, 0)
		}
		if 項目.種類 == fd種類fat || 項目.種類 == fd種類根目錄目錄 {
			return Erofs
		}
		return Ebadf
	}
	buffer := Get位元組from指標(uintptr(address), int(計數), int(計數))
	控制台_2.M列印(buffer)
	return int32(計數)
}

func sys讀取(fd int32, address uint32, 計數 uint32) int32 {
	if 計數 == 0 {
		return 0
	}
	if address == 0 || address+計數 < address {
		return Efault
	}
	項目 := get開啟檔案(fd)
	if 項目 == nil {
		return Ebadf
	}
	if 項目.種類 == fd種類stdin {
		return 讀取stdin(address, 計數)
	}
	if 項目.種類 == fd種類根目錄目錄 {
		return Eisdir
	}
	if 項目.種類 == fd種類通訊端 {
		return 通訊端receivefrom(fd, address, 計數, 0, 0)
	}
	if 項目.種類 != fd種類fat {
		return Ebadf
	}
	if 項目.位置 >= 項目.大小 {
		return 0
	}
	remaining := 項目.大小 - 項目.位置
	if 計數 > remaining {
		計數 = remaining
	}
	buffer := Get位元組from指標(uintptr(address), int(計數), int(計數))
	return 讀取vfs檔案(項目, buffer, 計數)
}

func sys開啟(路徑address uint32, 旗標 uint32, 模式 uint32) int32 {
	_ = 模式
	if 路徑address == 0 {
		return Efault
	}
	存取模式 := 旗標 & 3
	if 存取模式 == o寫入僅用 || 存取模式 == o讀取寫入 || (旗標&(o建立|o截短|oappend)) != 0 {
		return Erofs
	}

	程序 := ensure目前程序()
	if 程序 == nil {
		return Enfile
	}
	描述 := allocate開啟檔案()
	if 描述 < 0 {
		return 描述
	}
	項目 := &開啟檔案table[描述]
	項目.旗標 = 旗標
	if is根目錄路徑(路徑address) {
		項目.種類 = fd種類根目錄目錄
		項目.大小 = 0
	} else {
		名稱len, 名稱 := 複製路徑(路徑address)
		if 名稱len == 0 {
			*項目 = 開啟檔案描述{}
			return Enoent
		}
		大小 := 檔案大小(名稱[:名稱len])
		if 大小 == 0 {
			*項目 = 開啟檔案描述{}
			return Enoent
		}
		if (旗標 & o目錄) != 0 {
			*項目 = 開啟檔案描述{}
			return Enotdir
		}
		項目.種類 = fd種類fat
		項目.大小 = 大小
		項目.名稱len = 名稱len
		項目.名稱 = 名稱
	}

	fd := allocatefd(程序, 描述, 3)
	if fd < 0 {
		*項目 = 開啟檔案描述{}
		return fd
	}
	return fd
}

func sys關閉(fd int32) int32 {
	return 關閉程序fd(ensure目前程序(), fd)
}

func sysdup(fd int32, 最小值 int32) int32 {
	程序 := ensure目前程序()
	項目 := get開啟檔案for(程序, fd)
	if 項目 == nil {
		return Ebadf
	}
	新增fd := allocatefd(程序, 程序.fds[fd].描述, 最小值)
	if 新增fd >= 0 {
		項目.refs++
	}
	return 新增fd
}

func sysdup2(oldfd int32, 新增fd int32) int32 {
	程序 := ensure目前程序()
	項目 := get開啟檔案for(程序, oldfd)
	if 項目 == nil {
		return Ebadf
	}
	if 新增fd < 0 || 新增fd >= 最大fd {
		return Ebadf
	}
	if oldfd == 新增fd {
		return 新增fd
	}
	if 程序.fds[新增fd].已使用 {
		關閉程序fd(程序, 新增fd)
	}
	程序.fds[新增fd] = fd項目{已使用: true, 描述: 程序.fds[oldfd].描述}
	項目.refs++
	return 新增fd
}

func sysfcntl(fd int32, 指令 uint32, argument uint32) int32 {
	程序 := ensure目前程序()
	項目 := get開啟檔案for(程序, fd)
	if 項目 == nil {
		return Ebadf
	}
	switch 指令 {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(程序.fds[fd].fd旗標)
	case f設定fd:
		程序.fds[fd].fd旗標 = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(項目.旗標)
	case f設定fl:
		項目.旗標 = (項目.旗標 & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, 位移 int32, whence uint32) int32 {
	項目 := get開啟檔案(fd)
	if 項目 == nil {
		return Ebadf
	}
	if 項目.種類 != fd種類fat {
		return Espipe
	}
	var base int64
	switch whence {
	case seek設定:
		base = 0
	case seek目前:
		base = int64(項目.位置)
	case seek結束:
		base = int64(項目.大小)
	default:
		return Einval
	}
	位置_2 := base + int64(位移)
	if 位置_2 < 0 || 位置_2 > 0x7FFFFFFF {
		return Einval
	}
	項目.位置 = uint32(位置_2)
	return int32(項目.位置)
}

func 讀取vfs檔案(項目 *開啟檔案描述, 目的地_2 []byte, 計數 uint32) int32 {
	記憶體管理器 := &mem.T記憶體管理器{}
	tmp指標 := 記憶體管理器.M配置記憶體(項目.大小)
	if tmp指標 == nil {
		return Einval
	}
	tmp := Get位元組from指標(uintptr(tmp指標), int(項目.大小), int(項目.大小))
	讀取檔案(項目.名稱[:項目.名稱len], tmp)
	copy(目的地_2[:計數], tmp[項目.位置:項目.位置+計數])
	項目.位置 += 計數
	記憶體管理器.F剩餘(tmp指標)
	return int32(計數)
}

func is根目錄路徑(路徑address uint32) bool {
	if 路徑address == 0 {
		return false
	}
	路徑 := Get位元組from指標(uintptr(路徑address), 4, 4)
	if 路徑[0] == '/' && 路徑[1] == 0 {
		return true
	}
	if 路徑[0] == '.' && 路徑[1] == 0 {
		return true
	}
	if 路徑[0] == '/' && 路徑[1] == '.' && 路徑[2] == 0 {
		return true
	}
	return false
}

func sys存取(路徑address uint32, 模式 uint32) int32 {
	if 路徑address == 0 {
		return Efault
	}
	if (模式 & ^uint32(7)) != 0 {
		return Einval
	}
	is根目錄 := is根目錄路徑(路徑address)
	exists := is根目錄
	if !exists {
		名稱len, 名稱 := 複製路徑(路徑address)
		exists = 名稱len != 0 && 檔案大小(名稱[:名稱len]) != 0
	}
	if !exists {
		return Enoent
	}
	if (模式 & 2) != 0 {
		return Eacces
	}

	if (模式&1) != 0 && !is根目錄 {
		return Eacces
	}
	return 0
}

func syschdir(路徑address uint32) int32 {
	if 路徑address == 0 {
		return Efault
	}
	if !is根目錄路徑(路徑address) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, 大小 uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if 大小 < 2 {
		return Erange
	}
	buffer_2 := Get位元組from指標(uintptr(bufferaddress), int(大小), int(大小))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, 模式 uint32, 大小 uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.D裝置 = 1
	stat.Ino = inode
	stat.M模式 = 模式
	stat.Nlink = 1
	stat.S大小_2 = int32(大小)
	stat.Blksize = 512
	stat.B區塊 = int32((大小 + 511) / 512)
	return 0
}

func sysstat(路徑address uint32, stataddress uint32) int32 {
	if 路徑address == 0 {
		return Efault
	}
	if is根目錄路徑(路徑address) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	名稱len, 名稱 := 複製路徑(路徑address)
	if 名稱len == 0 {
		return Enoent
	}
	大小 := 檔案大小(名稱[:名稱len])
	if 大小 == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < 名稱len; i++ {
		inode = inode*33 + uint32(名稱[i])
	}
	return fillposixstat(stataddress, sifreg|0444, 大小, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	項目 := get開啟檔案(fd)
	if 項目 == nil {
		return Ebadf
	}
	switch 項目.種類 {
	case fd種類stdin, fd種類控制台:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fd種類根目錄目錄:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fd種類fat:
		return fillposixstat(stataddress, sifreg|0444, 項目.大小, uint32(fd+2))
	case fd種類通訊端:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if get開啟檔案(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	程序 := ensure目前程序()
	if 程序 == nil {
		return 0
	}
	if 程序.程式break == 0 {
		程序.程式break = 使用者heapbase
	}
	if address_2 == 0 {
		return 程序.程式break
	}
	if address_2 < 使用者heapbase || address_2 > 使用者heap限制 {
		return 程序.程式break
	}
	程序.程式break = address_2
	return 程序.程式break
}

func 複製uts欄位(目的地 *[65]byte, 數值 string) {
	限制 := len(數值)
	if 限制 > 64 {
		限制 = 64
	}
	for i := 0; i < 限制; i++ {
		目的地[i] = 數值[i]
	}
	目的地[限制] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	名稱 := (*posixutsname)(Pointer(uintptr(address_2)))
	*名稱 = posixutsname{}
	複製uts欄位(&名稱.Sysname, "EngOS")
	複製uts欄位(&名稱.Nodename, "engos")
	複製uts欄位(&名稱.Release, "0.1-posix")
	複製uts欄位(&名稱.V版本, "POSIX.1-2017 phase 1")
	複製uts欄位(&名稱.Machine, "i386")
	return 0
}

func 置換unsignedinteger16(數值 uint16) uint16 {
	return (數值 << 8) | (數值 >> 8)
}

func 通訊端呼叫argument(參數_2 uint32, 索引 uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(參數_2 + 索引*4)))
}

func 通訊端forfd(fd int32) (*本地datagram通訊端, int32) {
	項目 := get開啟檔案(fd)
	if 項目 == nil || 項目.種類 != fd種類通訊端 || 項目.aux >= 最大sockets {
		return nil, Ebadf
	}
	通訊端 := &本地sockets[項目.aux]
	if !通訊端.已使用 {
		return nil, Ebadf
	}
	return 通訊端, 0
}

func allocate通訊端(網域 uint32, 通訊端類型 uint32, protocol uint32) int32 {
	if 網域 != afinet {
		return Eafnosupport
	}
	if 通訊端類型 != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	程序 := ensure目前程序()
	if 程序 == nil {
		return Enfile
	}
	通訊端索引 := -1
	for i := 0; i < 最大sockets; i++ {
		if !本地sockets[i].已使用 {
			通訊端索引 = i
			break
		}
	}
	if 通訊端索引 < 0 {
		return Enfile
	}
	描述 := allocate開啟檔案()
	if 描述 < 0 {
		return 描述
	}
	本地sockets[通訊端索引] = 本地datagram通訊端{已使用: true}
	項目 := &開啟檔案table[描述]
	項目.種類 = fd種類通訊端
	項目.旗標 = o讀取寫入
	項目.aux = uint32(通訊端索引)
	fd := allocatefd(程序, 描述, 3)
	if fd < 0 {
		本地sockets[通訊端索引] = 本地datagram通訊端{}
		*項目 = 開啟檔案描述{}
		return fd
	}
	return fd
}

func 通訊端address(address_2 uint32, 長度 uint32) (*通訊端addressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if 長度 < 16 {
		return nil, Einval
	}
	結果 := (*通訊端addressipv4)(Pointer(uintptr(address_2)))
	if 結果.Family != afinet {
		return nil, Eafnosupport
	}
	return 結果, 0
}

func 連接埠進使用(連接埠 uint16, except *本地datagram通訊端) bool {
	for i := 0; i < 最大sockets; i++ {
		通訊端 := &本地sockets[i]
		if 通訊端 != except && 通訊端.已使用 && 通訊端.bound && 通訊端.本地.P連接埠 == 連接埠 {
			return true
		}
	}
	return false
}

func bindephemeral(通訊端 *本地datagram通訊端) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		連接埠 := 置換unsignedinteger16(下一個ephemeral連接埠)
		下一個ephemeral連接埠++
		if 下一個ephemeral連接埠 < 49152 {
			下一個ephemeral連接埠 = 49152
		}
		if !連接埠進使用(連接埠, 通訊端) {
			通訊端.本地 = 通訊端addressipv4{Family: afinet, P連接埠: 連接埠, Address: 0x0100007F}
			通訊端.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func 通訊端bind(fd int32, address_2 uint32, 長度 uint32) int32 {
	通訊端, 出錯 := 通訊端forfd(fd)
	if 出錯 != 0 {
		return 出錯
	}
	requested, 出錯 := 通訊端address(address_2, 長度)
	if 出錯 != 0 {
		return 出錯
	}
	if 通訊端.bound {
		return Einval
	}
	if requested.P連接埠 == 0 {
		return bindephemeral(通訊端)
	}
	if 連接埠進使用(requested.P連接埠, 通訊端) {
		return Eaddrinuse
	}
	通訊端.本地 = *requested
	通訊端.bound = true
	return 0
}

func 通訊端連接(fd int32, address_2 uint32, 長度 uint32) int32 {
	通訊端, 出錯 := 通訊端forfd(fd)
	if 出錯 != 0 {
		return 出錯
	}
	遠端, 出錯 := 通訊端address(address_2, 長度)
	if 出錯 != 0 {
		return 出錯
	}
	if !通訊端.bound {
		if 出錯 := bindephemeral(通訊端); 出錯 != 0 {
			return 出錯
		}
	}
	通訊端.遠端 = *遠端
	通訊端.connected = true
	return 0
}

func 通訊端送出to(fd int32, bufferaddress_2 uint32, 長度 uint32, 目的地address uint32, 目的地長度 uint32) int32 {
	通訊端, 出錯 := 通訊端forfd(fd)
	if 出錯 != 0 {
		return 出錯
	}
	if 長度 > 最大datagram大小 {
		return Emsgsize
	}
	if 長度 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var 目的地 通訊端addressipv4
	if 目的地address != 0 {
		address_2, address錯誤 := 通訊端address(目的地address, 目的地長度)
		if address錯誤 != 0 {
			return address錯誤
		}
		目的地 = *address_2
	} else {
		if !通訊端.connected {
			return Enotconn
		}
		目的地 = 通訊端.遠端
	}
	if !通訊端.bound {
		if bind錯誤 := bindephemeral(通訊端); bind錯誤 != 0 {
			return bind錯誤
		}
	}
	var receiver *本地datagram通訊端
	for i := 0; i < 最大sockets; i++ {
		candidate := &本地sockets[i]
		if candidate.已使用 && candidate.bound && candidate.本地.P連接埠 == 目的地.P連接埠 &&
			(candidate.本地.Address == 0 || candidate.本地.Address == 目的地.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.計數 >= 最大通訊端封包 {
		return Eagain
	}
	packet := &receiver.封包[receiver.tail]
	*packet = 通訊端packet{已使用: true, 大小: 長度, 來源: 通訊端.本地}
	if 長度 != 0 {
		來源 := Get位元組from指標(uintptr(bufferaddress_2), int(長度), int(長度))
		copy(packet.資料[:長度], 來源)
	}
	receiver.tail = (receiver.tail + 1) % 最大通訊端封包
	receiver.計數++
	return int32(長度)
}

func 通訊端receivefrom(fd int32, bufferaddress_2 uint32, 長度 uint32, 來源address uint32, 來源長度address uint32) int32 {
	通訊端, 出錯 := 通訊端forfd(fd)
	if 出錯 != 0 {
		return 出錯
	}
	if 長度 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if 通訊端.計數 == 0 {
		return Eagain
	}
	packet := &通訊端.封包[通訊端.head]
	複製長度 := packet.大小
	if 複製長度 > 長度 {
		複製長度 = 長度
	}
	if 複製長度 != 0 {
		目的地 := Get位元組from指標(uintptr(bufferaddress_2), int(複製長度), int(複製長度))
		copy(目的地, packet.資料[:複製長度])
	}
	if 來源address != 0 {
		if 來源長度address == 0 {
			return Efault
		}
		provided長度 := (*uint32)(Pointer(uintptr(來源長度address)))
		if *provided長度 >= 16 {
			*(*通訊端addressipv4)(Pointer(uintptr(來源address))) = packet.來源
		}
		*provided長度 = 16
	}
	*packet = 通訊端packet{}
	通訊端.head = (通訊端.head + 1) % 最大通訊端封包
	通訊端.計數--
	return int32(複製長度)
}

func 複製通訊端名稱(fd int32, address_2 uint32, 長度address uint32, peer bool) int32 {
	通訊端, 出錯 := 通訊端forfd(fd)
	if 出錯 != 0 {
		return 出錯
	}
	if address_2 == 0 || 長度address == 0 {
		return Efault
	}
	長度 := (*uint32)(Pointer(uintptr(長度address)))
	if *長度 < 16 {
		*長度 = 16
		return Einval
	}
	if peer {
		if !通訊端.connected {
			return Enotconn
		}
		*(*通訊端addressipv4)(Pointer(uintptr(address_2))) = 通訊端.遠端
	} else {
		if !通訊端.bound {
			if bind錯誤 := bindephemeral(通訊端); bind錯誤 != 0 {
				return bind錯誤
			}
		}
		*(*通訊端addressipv4)(Pointer(uintptr(address_2))) = 通訊端.本地
	}
	*長度 = 16
	return 0
}

func sys通訊端呼叫(呼叫 uint32, 參數_2 uint32) int32 {
	if 參數_2 == 0 {
		return Efault
	}
	switch 呼叫 {
	case 1:
		return allocate通訊端(通訊端呼叫argument(參數_2, 0), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2))
	case 2:
		return 通訊端bind(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2))
	case 3:
		return 通訊端連接(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return 複製通訊端名稱(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), false)
	case 7:
		return 複製通訊端名稱(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), true)
	case 9:
		return 通訊端送出to(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), 0, 0)
	case 10:
		return 通訊端receivefrom(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), 0, 0)
	case 11:
		return 通訊端送出to(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), 通訊端呼叫argument(參數_2, 4), 通訊端呼叫argument(參數_2, 5))
	case 12:
		return 通訊端receivefrom(int32(通訊端呼叫argument(參數_2, 0)), 通訊端呼叫argument(參數_2, 1), 通訊端呼叫argument(參數_2, 2), 通訊端呼叫argument(參數_2, 4), 通訊端呼叫argument(參數_2, 5))
	case 13:
		if _, 出錯 := 通訊端forfd(int32(通訊端呼叫argument(參數_2, 0))); 出錯 != 0 {
			return 出錯
		}
		return 0
	case 14:
		if _, 出錯 := 通訊端forfd(int32(通訊端呼叫argument(參數_2, 0))); 出錯 != 0 {
			return 出錯
		}
		return 0
	}
	return Eopnotsupp
}

func 讀取stdin(address uint32, 計數 uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Get位元組from指標(uintptr(address), int(計數), int(計數))
	var n uint32
	for n < 計數 {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinput位元組(c byte) {
	下一個 := (stdin寫入 + 1) % uint32(len(stdinbuffer))
	if 下一個 == stdin讀取 {
		return
	}
	stdinbuffer[stdin寫入] = c
	stdin寫入 = 下一個
}

func stdingetblocking() byte {
	for stdin讀取 == stdin寫入 {
		sc := poll鍵盤scancode()
		if sc != 0 {
			Stdinput位元組(sc)
		}
	}
	c := stdinbuffer[stdin讀取]
	stdin讀取 = (stdin讀取 + 1) % uint32(len(stdinbuffer))
	return c
}

func poll鍵盤scancode() byte {
	for (P連接埠讀取位元組(0x64) & 0x01) == 0 {
	}
	sc := P連接埠讀取位元組(0x60)
	return scancodeto位元組(sc)
}

func scancodeto位元組(sc uint8) byte {
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

func 複製執行vector(address_2 uint32, 結果 *執行vector) int32 {
	*結果 = 執行vector{}
	if address_2 == 0 {
		return 0
	}
	for 索引 := uint32(0); 索引 < 最大執行vector項目; 索引++ {
		字串address := *(*uint32)(Pointer(uintptr(address_2 + 索引*4)))
		if 字串address == 0 {
			結果.計數 = 索引
			return 0
		}
		terminated := false
		for 長度 := uint32(0); 長度 <= 最大執行字串長度; 長度++ {
			數值 := *(*byte)(Pointer(uintptr(字串address + 長度)))
			結果.值[索引][長度] = 數值
			if 數值 == 0 {
				結果.lengths[索引] = 長度
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

func push執行unsignedinteger32(堆疊記憶區 *uint32, 數值 uint32) {
	*堆疊記憶區 -= 4
	*(*uint32)(Pointer(uintptr(*堆疊記憶區))) = 數值
}

func setup執行stack(cpu *Tcpu狀態, 參數_2 *執行vector, environment *執行vector) int32 {
	const stack位元組 uint32 = 4096
	if !Makerange私密writable(getcr3(), U使用者stack上-stack位元組, stack位元組) {
		return Enomem
	}
	堆疊記憶區 := U使用者stack上
	var argumentpointers [最大執行vector項目]uint32
	var environmentpointers [最大執行vector項目]uint32

	for i := int(environment.計數) - 1; i >= 0; i-- {
		長度 := environment.lengths[i] + 1
		堆疊記憶區 -= 長度
		目的地 := Get位元組from指標(uintptr(堆疊記憶區), int(長度), int(長度))
		copy(目的地, environment.值[i][:長度])
		environmentpointers[i] = 堆疊記憶區
	}
	for i := int(參數_2.計數) - 1; i >= 0; i-- {
		長度 := 參數_2.lengths[i] + 1
		堆疊記憶區 -= 長度
		目的地 := Get位元組from指標(uintptr(堆疊記憶區), int(長度), int(長度))
		copy(目的地, 參數_2.值[i][:長度])
		argumentpointers[i] = 堆疊記憶區
	}
	堆疊記憶區 &= ^uint32(3)
	push執行unsignedinteger32(&堆疊記憶區, 0)
	for i := int(environment.計數) - 1; i >= 0; i-- {
		push執行unsignedinteger32(&堆疊記憶區, environmentpointers[i])
	}
	push執行unsignedinteger32(&堆疊記憶區, 0)
	for i := int(參數_2.計數) - 1; i >= 0; i-- {
		push執行unsignedinteger32(&堆疊記憶區, argumentpointers[i])
	}
	push執行unsignedinteger32(&堆疊記憶區, 參數_2.計數)
	cpu.Esp = 堆疊記憶區
	cpu.Ebp = 0
	return 0
}

func 關閉時執行(程序 *程序項目) {
	if 程序 == nil {
		return
	}
	for fd := int32(0); fd < 最大fd; fd++ {
		if 程序.fds[fd].已使用 && (程序.fds[fd].fd旗標&fdcloexec) != 0 {
			關閉程序fd(程序, fd)
		}
	}
}

func sysexecve(cpu *Tcpu狀態, 路徑address uint32) int32 {
	if 路徑address == 0 {
		return Efault
	}
	var 參數_2 執行vector
	var environment 執行vector
	if 結果 := 複製執行vector(cpu.Ecx, &參數_2); 結果 < 0 {
		return 結果
	}
	if 結果 := 複製執行vector(cpu.Edx, &environment); 結果 < 0 {
		return 結果
	}
	名稱len, 名稱 := 複製路徑(路徑address)
	if 名稱len == 0 {
		return Enoent
	}
	大小 := 檔案大小(名稱[:名稱len])
	if 大小 == 0 {
		return Enoent
	}
	記憶體管理器 := &mem.T記憶體管理器{}
	檔案指標 := 記憶體管理器.M配置記憶體(大小)
	if 檔案指標 == nil {
		return Einval
	}
	資料 := Get位元組from指標(uintptr(檔案指標), int(大小), int(大小))
	讀取檔案(名稱[:名稱len], 資料)
	if 大小 < 52 || 資料[0] != 0x7F || 資料[1] != 'E' || 資料[2] != 'L' || 資料[3] != 'F' {
		記憶體管理器.F剩餘(檔案指標)
		return Enoexec
	}
	loader := Elf{}
	項目 := loader.Get項目(資料)
	loader.Parse(資料, getcr3())
	記憶體管理器.F剩餘(檔案指標)
	if 結果 := setup執行stack(cpu, &參數_2, &environment); 結果 < 0 {
		return 結果
	}
	關閉時執行(ensure目前程序())
	cpu.Eip = 項目
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpu狀態) int32 {
	parent行程代碼 := C目前行程代碼()
	if ensure目前程序() == nil {
		return Enfile
	}
	行程代碼 := allocate程序(parent行程代碼)
	if 行程代碼 == 0 {
		return Einval
	}
	記憶體管理器 := &mem.T記憶體管理器{}
	執行緒指標 := 記憶體管理器.M配置記憶體(uint32(Sizeof(T執行緒{})))
	stack指標 := 記憶體管理器.M配置記憶體(T執行緒stack大小)
	child頁目錄 := Cloneaddress空白cow(getcr3())
	if 執行緒指標 == nil || stack指標 == nil || child頁目錄 == 0 {
		丟棄程序(行程代碼)
		return Einval
	}
	child := (*T執行緒)(執行緒指標)
	child.Stack = uint32(uintptr(stack指標))
	child.Cpu狀態 = (*Tcpu狀態)(Pointer(uintptr(stack指標) + T執行緒stack大小 - Sizeof(Tcpu狀態{})))
	*child.Cpu狀態 = *cpu
	child.Cpu狀態.Eax = 0
	child.U使用者stack_2 = cpu.Esp
	child.U使用者stack大小_2 = 0
	child.P行程代碼 = 行程代碼
	child.Parent行程代碼 = parent行程代碼
	child.P頁目錄項目 = child頁目錄
	child.T執行緒狀態 = R準備就緒
	child.Fpu位移 = 0xffffffff
	child.Is核心 = false
	A加入runnable執行緒(child)
	return int32(行程代碼)
}

func sys離開(狀態 uint32) {
	行程代碼 := C目前行程代碼()
	for i := 0; i < len(程序table); i++ {
		if 程序table[i].已使用 && 程序table[i].行程代碼 == 行程代碼 {
			關閉全部程序fds(&程序table[i])
			程序table[i].已離開 = true
			程序table[i].狀態 = (狀態 & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(行程代碼 int32, 狀態address uint32, 選項 uint32) int32 {
	if (選項 & ^uint32(1)) != 0 {
		return Einval
	}
	parent行程代碼 := C目前行程代碼()
	foundchild := false
	for i := 0; i < len(程序table); i++ {
		p := &程序table[i]
		matches := 行程代碼 == -1 || 行程代碼 == 0 || p.行程代碼 == uint32(行程代碼)
		if p.已使用 && matches && p.parent == parent行程代碼 {
			foundchild = true
			if p.已離開 {
				if 狀態address != 0 {
					*(*uint32)(Pointer(uintptr(狀態address))) = p.狀態
				}
				child行程代碼 := p.行程代碼
				*p = 程序項目{}
				return int32(child行程代碼)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (選項 & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocate程序(parent uint32) uint32 {
	parent程序 := 尋找程序(parent)
	行程代碼 := Allocate行程代碼()
	for i := 0; i < len(程序table); i++ {
		if !程序table[i].已使用 {
			程序table[i] = 程序項目{
				已使用:		true,
				行程代碼:		行程代碼,
				parent:		parent,
				程式break:	使用者heapbase,
			}
			if parent程序 != nil {
				程序table[i].程式break = parent程序.程式break
				for fd := 0; fd < 最大fd; fd++ {
					if parent程序.fds[fd].已使用 {
						程序table[i].fds[fd] = parent程序.fds[fd]
						描述 := parent程序.fds[fd].描述
						if 描述 >= 0 && 描述 < 最大開啟檔案 {
							開啟檔案table[描述].refs++
						}
					}
				}
			} else {
				initialize程序fds(&程序table[i])
			}
			return 行程代碼
		}
	}
	return 0
}

func 關閉全部程序fds(程序 *程序項目) {
	if 程序 == nil {
		return
	}
	for fd := int32(0); fd < 最大fd; fd++ {
		if 程序.fds[fd].已使用 {
			關閉程序fd(程序, fd)
		}
	}
}

func 丟棄程序(行程代碼 uint32) {
	程序 := 尋找程序(行程代碼)
	if 程序 == nil {
		return
	}
	關閉全部程序fds(程序)
	*程序 = 程序項目{}
}

func 複製路徑(路徑address uint32) (uint32, [12]byte) {
	var 名稱 [12]byte
	if 路徑address == 0 {
		return 0, 名稱
	}
	raw := Get位元組from指標(uintptr(路徑address), 64, 64)
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
		名稱[n] = c
		n++
	}
	return n, 名稱
}

func 檔案大小(檔案名稱 []byte) uint32 {
	var ata0s = T進階科技attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分割區 := Tmsdos分割區table{}
	分割區.R讀取分割區(&ata0s)

	bios := T檔案系統參數32{}
	大小 := bios.Len(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱)
	ata0s.Flush()
	return 大小
}

func 讀取檔案(檔案名稱 []byte, 資料 []byte) {
	var ata0s = T進階科技attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分割區 := Tmsdos分割區table{}
	分割區.R讀取分割區(&ata0s)

	bios := T檔案系統參數32{}
	bios.R讀取(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱, 資料)
	ata0s.Flush()
}

func getcr3() uint32
