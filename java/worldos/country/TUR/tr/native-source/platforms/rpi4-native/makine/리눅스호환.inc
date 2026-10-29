/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(kullanıcı_kare *Dosya_girdi) {
    kullanıcı_kare 변환값 = *Dosya_girdi;
    uintptr_t 수치 = Dosya_girdi->yazmaç_veri[8];
    switch (수치) {
    case 63: 변환값.yazmaç_veri[8] = 2; break;   /* read */
    case 64: 변환값.yazmaç_veri[8] = 1; break;   /* write */
    case 57: 변환값.yazmaç_veri[8] = 4; break;   /* close */
    case 62: 변환값.yazmaç_veri[8] = 5; break;   /* lseek */
    case 46: 변환값.yazmaç_veri[8] = 10; break;  /* ftruncate */
    case 82: 변환값.yazmaç_veri[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char yol[65]; int 반환값 = örnek_yol(Dosya_girdi->yazmaç_veri[1], yol); if (반환값) return 반환값;
        if ((int)Dosya_girdi->yazmaç_veri[0] != -100 && yol[0] != '/') return -95;
        if (수치 == 35 && Dosya_girdi->yazmaç_veri[2]) return -95;
        if (수치 == 56 && (Dosya_girdi->yazmaç_veri[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.yazmaç_veri[8] = 수치 == 56 ? 3 : 11;
        변환값.yazmaç_veri[0] = Dosya_girdi->yazmaç_veri[1];
        변환값.yazmaç_veri[1] = Dosya_girdi->yazmaç_veri[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.yazmaç_veri[2] = Dosya_girdi->yazmaç_veri[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Önceki = yığın_Bitiş;
        변환값.yazmaç_veri[8] = 8;
        intptr_t 반환값 = yerel_Sistem_Ara(&변환값);
        return 반환값 < 0 ? (intptr_t)Önceki : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Dosya_girdi->yazmaç_veri[0] != 1) return -22;
        if (!kullanıcı_aralık(Dosya_girdi->yazmaç_veri[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), değer[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Dosya_girdi->yazmaç_veri[1], değer, sizeof(değer)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return sahip_nesne + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return yerel_Sistem_Ara(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t giriş_noktası) {
    uintptr_t 맨위 = kullanıcı_Bitiş, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned öğe_BAĞ_DEĞ_SAY = 전달인수길이[순번] + 1;
        맨위 -= öğe_BAĞ_DEĞ_SAY; memcpy((void *)맨위, 전달인수[순번], öğe_BAĞ_DEĞ_SAY); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t yığın_belleği = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *veri_konum = (uint64_t *)yığın_belleği;
    *veri_konum++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *veri_konum++ = 주소목록[순번];
    *veri_konum++ = 0; *veri_konum++ = 0;
    *veri_konum++ = 6; *veri_konum++ = sayfa_boyutu;
    *veri_konum++ = 9; *veri_konum++ = giriş_noktası;
    *veri_konum++ = 0; *veri_konum++ = 0;
    return yığın_belleği;
}
