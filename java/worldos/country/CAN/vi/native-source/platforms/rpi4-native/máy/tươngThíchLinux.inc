/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t gọiHệThốngLinux(khungNgườiDùng *mụcTệp) {
    khungNgườiDùng đãDịch = *mụcTệp;
    uintptr_t giáTrịThuộcSố = mụcTệp->thanhGhiDữLiệu[8];
    switch (giáTrịThuộcSố) {
    case 63: đãDịch.thanhGhiDữLiệu[8] = 2; break;   /* read */
    case 64: đãDịch.thanhGhiDữLiệu[8] = 1; break;   /* write */
    case 57: đãDịch.thanhGhiDữLiệu[8] = 4; break;   /* close */
    case 62: đãDịch.thanhGhiDữLiệu[8] = 5; break;   /* lseek */
    case 46: đãDịch.thanhGhiDữLiệu[8] = 10; break;  /* ftruncate */
    case 82: đãDịch.thanhGhiDữLiệu[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char đườngDẫn[65]; int giáTrịĐãTrảVề = saoChépĐườngDẫn(mụcTệp->thanhGhiDữLiệu[1], đườngDẫn); if (giáTrịĐãTrảVề) return giáTrịĐãTrảVề;
        if ((int)mụcTệp->thanhGhiDữLiệu[0] != -100 && đườngDẫn[0] != '/') return -95;
        if (giáTrịThuộcSố == 35 && mụcTệp->thanhGhiDữLiệu[2]) return -95;
        if (giáTrịThuộcSố == 56 && (mụcTệp->thanhGhiDữLiệu[2] & ~(0x7fful | 0x80000ul))) return -95;
        đãDịch.thanhGhiDữLiệu[8] = giáTrịThuộcSố == 56 ? 3 : 11;
        đãDịch.thanhGhiDữLiệu[0] = mụcTệp->thanhGhiDữLiệu[1];
        đãDịch.thanhGhiDữLiệu[1] = mụcTệp->thanhGhiDữLiệu[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        đãDịch.thanhGhiDữLiệu[2] = mụcTệp->thanhGhiDữLiệu[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t trướcĐó = kếtThúcVùngNhớĐộng;
        đãDịch.thanhGhiDữLiệu[8] = 8;
        intptr_t giáTrịĐãTrảVề = gọiHệThốngBảnĐịa(&đãDịch);
        return giáTrịĐãTrảVề < 0 ? (intptr_t)trướcĐó : giáTrịĐãTrảVề;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (mụcTệp->thanhGhiDữLiệu[0] != 1) return -22;
        if (!khoảngNgườiDùng(mụcTệp->thanhGhiDữLiệu[1], 16, 1)) return -14;
        uint64_t miliGiây = miliGiâyGọnBoMạch(), giáTrị[2] = {miliGiây / 1000, (miliGiây % 1000) * 1000000};
        memcpy((void *)mụcTệp->thanhGhiDữLiệu[1], giáTrị, sizeof(giáTrị)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return đốiTượngChủSởHữu + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return gọiHệThốngBảnĐịa(&đãDịch);
}

static uintptr_t ngănXếpBắtChạyLinux(uintptr_t điểmMục) {
    uintptr_t mụcĐỉnh = kếtThúcNgườiDùng, cácĐịaChỉ[8];
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngĐốiSốĐãChuyểnTiếp; chỉSốThứBậc++) {
        unsigned sốLượngPhầnMục = độDàiĐốiSốĐãChuyểnTiếp[chỉSốThứBậc] + 1;
        mụcĐỉnh -= sốLượngPhầnMục; memcpy((void *)mụcĐỉnh, đốiSốĐãChuyểnTiếp[chỉSốThứBậc], sốLượngPhầnMục); cácĐịaChỉ[chỉSốThứBậc] = mụcĐỉnh;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t lưuTrữNgănXếp = (mụcĐỉnh - (sốLượngĐốiSốĐãChuyểnTiếp + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *vịTríDữLiệu = (uint64_t *)lưuTrữNgănXếp;
    *vịTríDữLiệu++ = sốLượngĐốiSốĐãChuyểnTiếp;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngĐốiSốĐãChuyểnTiếp; chỉSốThứBậc++) *vịTríDữLiệu++ = cácĐịaChỉ[chỉSốThứBậc];
    *vịTríDữLiệu++ = 0; *vịTríDữLiệu++ = 0;
    *vịTríDữLiệu++ = 6; *vịTríDữLiệu++ = cỡTrang;
    *vịTríDữLiệu++ = 9; *vịTríDữLiệu++ = điểmMục;
    *vịTríDữLiệu++ = 0; *vịTríDữLiệu++ = 0;
    return lưuTrữNgănXếp;
}
