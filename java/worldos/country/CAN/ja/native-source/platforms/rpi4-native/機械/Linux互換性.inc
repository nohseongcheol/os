/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t Linuxシステム呼出し(利用者枠組 *ファイル入口) {
    利用者枠組 翻訳済み = *ファイル入口;
    uintptr_t 数値値 = ファイル入口->データレジスタ[8];
    switch (数値値) {
    case 63: 翻訳済み.データレジスタ[8] = 2; break;   /* read */
    case 64: 翻訳済み.データレジスタ[8] = 1; break;   /* write */
    case 57: 翻訳済み.データレジスタ[8] = 4; break;   /* close */
    case 62: 翻訳済み.データレジスタ[8] = 5; break;   /* lseek */
    case 46: 翻訳済み.データレジスタ[8] = 10; break;  /* ftruncate */
    case 82: 翻訳済み.データレジスタ[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char 経路[65]; int 返却済み値 = 経路複写(ファイル入口->データレジスタ[1], 経路); if (返却済み値) return 返却済み値;
        if ((int)ファイル入口->データレジスタ[0] != -100 && 経路[0] != '/') return -95;
        if (数値値 == 35 && ファイル入口->データレジスタ[2]) return -95;
        if (数値値 == 56 && (ファイル入口->データレジスタ[2] & ~(0x7fful | 0x80000ul))) return -95;
        翻訳済み.データレジスタ[8] = 数値値 == 56 ? 3 : 11;
        翻訳済み.データレジスタ[0] = ファイル入口->データレジスタ[1];
        翻訳済み.データレジスタ[1] = ファイル入口->データレジスタ[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        翻訳済み.データレジスタ[2] = ファイル入口->データレジスタ[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 前回 = ヒープ終端位置;
        翻訳済み.データレジスタ[8] = 8;
        intptr_t 返却済み値 = 自前システム呼出し(&翻訳済み);
        return 返却済み値 < 0 ? (intptr_t)前回 : 返却済み値;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (ファイル入口->データレジスタ[0] != 1) return -22;
        if (!利用者範囲(ファイル入口->データレジスタ[1], 16, 1)) return -14;
        uint64_t ミリ秒 = 基板経過ミリ秒(), 値[2] = {ミリ秒 / 1000, (ミリ秒 % 1000) * 1000000};
        memcpy((void *)ファイル入口->データレジスタ[1], 値, sizeof(値)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return 所有者オブジェクト + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 自前システム呼出し(&翻訳済み);
}

static uintptr_t Linux開始処理スタック(uintptr_t 入口点) {
    uintptr_t 上端入口 = 利用者終端位置, 番地一覧[8];
    for (unsigned 序数添字 = 0; 序数添字 < 転送済み引数個数; 序数添字++) {
        unsigned 項目個数 = 転送済み引数長さ[序数添字] + 1;
        上端入口 -= 項目個数; memcpy((void *)上端入口, 転送済み引数[序数添字], 項目個数); 番地一覧[序数添字] = 上端入口;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t スタック記憶装置 = (上端入口 - (転送済み引数個数 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *データ位置 = (uint64_t *)スタック記憶装置;
    *データ位置++ = 転送済み引数個数;
    for (unsigned 序数添字 = 0; 序数添字 < 転送済み引数個数; 序数添字++) *データ位置++ = 番地一覧[序数添字];
    *データ位置++ = 0; *データ位置++ = 0;
    *データ位置++ = 6; *データ位置++ = ページ容量;
    *データ位置++ = 9; *データ位置++ = 入口点;
    *データ位置++ = 0; *データ位置++ = 0;
    return スタック記憶装置;
}
