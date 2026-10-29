/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t Linux系統呼叫(用戶幀 *檔案條目) {
    用戶幀 已翻譯 = *檔案條目;
    uintptr_t 數值值 = 檔案條目->寄存器資料[8];
    switch (數值值) {
    case 63: 已翻譯.寄存器資料[8] = 2; break;   /* read */
    case 64: 已翻譯.寄存器資料[8] = 1; break;   /* write */
    case 57: 已翻譯.寄存器資料[8] = 4; break;   /* close */
    case 62: 已翻譯.寄存器資料[8] = 5; break;   /* lseek */
    case 46: 已翻譯.寄存器資料[8] = 10; break;  /* ftruncate */
    case 82: 已翻譯.寄存器資料[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char 路徑[65]; int 已返回值 = 複製路徑(檔案條目->寄存器資料[1], 路徑); if (已返回值) return 已返回值;
        if ((int)檔案條目->寄存器資料[0] != -100 && 路徑[0] != '/') return -95;
        if (數值值 == 35 && 檔案條目->寄存器資料[2]) return -95;
        if (數值值 == 56 && (檔案條目->寄存器資料[2] & ~(0x7fful | 0x80000ul))) return -95;
        已翻譯.寄存器資料[8] = 數值值 == 56 ? 3 : 11;
        已翻譯.寄存器資料[0] = 檔案條目->寄存器資料[1];
        已翻譯.寄存器資料[1] = 檔案條目->寄存器資料[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        已翻譯.寄存器資料[2] = 檔案條目->寄存器資料[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 上一個 = 堆結束;
        已翻譯.寄存器資料[8] = 8;
        intptr_t 已返回值 = 原生系統呼叫(&已翻譯);
        return 已返回值 < 0 ? (intptr_t)上一個 : 已返回值;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (檔案條目->寄存器資料[0] != 1) return -22;
        if (!用戶範圍(檔案條目->寄存器資料[1], 16, 1)) return -14;
        uint64_t 毫秒 = 板經過毫秒(), 值[2] = {毫秒 / 1000, (毫秒 % 1000) * 1000000};
        memcpy((void *)檔案條目->寄存器資料[1], 值, sizeof(值)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return 所有者物件 + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 原生系統呼叫(&已翻譯);
}

static uintptr_t Linux開始棧(uintptr_t 條目分) {
    uintptr_t 頂端條目 = 用戶結束, 地址列[8];
    for (unsigned 序數索引 = 0; 序數索引 < 已轉發實際參數個數; 序數索引++) {
        unsigned 項目個數 = 已轉發實際參數長度[序數索引] + 1;
        頂端條目 -= 項目個數; memcpy((void *)頂端條目, 已轉發實際參數[序數索引], 項目個數); 地址列[序數索引] = 頂端條目;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t 棧存儲裝置 = (頂端條目 - (已轉發實際參數個數 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *資料位置 = (uint64_t *)棧存儲裝置;
    *資料位置++ = 已轉發實際參數個數;
    for (unsigned 序數索引 = 0; 序數索引 < 已轉發實際參數個數; 序數索引++) *資料位置++ = 地址列[序數索引];
    *資料位置++ = 0; *資料位置++ = 0;
    *資料位置++ = 6; *資料位置++ = 頁大小;
    *資料位置++ = 9; *資料位置++ = 條目分;
    *資料位置++ = 0; *資料位置++ = 0;
    return 棧存儲裝置;
}
