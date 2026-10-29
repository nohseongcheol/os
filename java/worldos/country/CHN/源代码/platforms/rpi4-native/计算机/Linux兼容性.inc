/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t Linux系统调用(用户帧 *文件条目) {
    用户帧 已翻译 = *文件条目;
    uintptr_t 数值值 = 文件条目->寄存器数据[8];
    switch (数值值) {
    case 63: 已翻译.寄存器数据[8] = 2; break;   /* read */
    case 64: 已翻译.寄存器数据[8] = 1; break;   /* write */
    case 57: 已翻译.寄存器数据[8] = 4; break;   /* close */
    case 62: 已翻译.寄存器数据[8] = 5; break;   /* lseek */
    case 46: 已翻译.寄存器数据[8] = 10; break;  /* ftruncate */
    case 82: 已翻译.寄存器数据[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char 路径[65]; int 已返回值 = 复制路径(文件条目->寄存器数据[1], 路径); if (已返回值) return 已返回值;
        if ((int)文件条目->寄存器数据[0] != -100 && 路径[0] != '/') return -95;
        if (数值值 == 35 && 文件条目->寄存器数据[2]) return -95;
        if (数值值 == 56 && (文件条目->寄存器数据[2] & ~(0x7fful | 0x80000ul))) return -95;
        已翻译.寄存器数据[8] = 数值值 == 56 ? 3 : 11;
        已翻译.寄存器数据[0] = 文件条目->寄存器数据[1];
        已翻译.寄存器数据[1] = 文件条目->寄存器数据[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        已翻译.寄存器数据[2] = 文件条目->寄存器数据[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 上一个 = 堆结束;
        已翻译.寄存器数据[8] = 8;
        intptr_t 已返回值 = 原生系统调用(&已翻译);
        return 已返回值 < 0 ? (intptr_t)上一个 : 已返回值;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (文件条目->寄存器数据[0] != 1) return -22;
        if (!用户范围(文件条目->寄存器数据[1], 16, 1)) return -14;
        uint64_t 毫秒 = 板经过毫秒(), 值[2] = {毫秒 / 1000, (毫秒 % 1000) * 1000000};
        memcpy((void *)文件条目->寄存器数据[1], 值, sizeof(值)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return 所有者对象 + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 原生系统调用(&已翻译);
}

static uintptr_t Linux开始栈(uintptr_t 条目分) {
    uintptr_t 顶端条目 = 用户结束, 地址列[8];
    for (unsigned 序数索引 = 0; 序数索引 < 已转发参数个数; 序数索引++) {
        unsigned 项目个数 = 已转发参数长度[序数索引] + 1;
        顶端条目 -= 项目个数; memcpy((void *)顶端条目, 已转发参数[序数索引], 项目个数); 地址列[序数索引] = 顶端条目;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t 栈存储装置 = (顶端条目 - (已转发参数个数 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *数据位置 = (uint64_t *)栈存储装置;
    *数据位置++ = 已转发参数个数;
    for (unsigned 序数索引 = 0; 序数索引 < 已转发参数个数; 序数索引++) *数据位置++ = 地址列[序数索引];
    *数据位置++ = 0; *数据位置++ = 0;
    *数据位置++ = 6; *数据位置++ = 页大小;
    *数据位置++ = 9; *数据位置++ = 条目分;
    *数据位置++ = 0; *数据位置++ = 0;
    return 栈存储装置;
}
