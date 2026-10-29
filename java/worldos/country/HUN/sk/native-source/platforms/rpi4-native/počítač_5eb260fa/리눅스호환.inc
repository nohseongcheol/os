/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(používateľ_rám *Súbor_položka) {
    používateľ_rám 변환값 = *Súbor_položka;
    uintptr_t 수치 = Súbor_položka->register_údaje[8];
    switch (수치) {
    case 63: 변환값.register_údaje[8] = 2; break;   /* read */
    case 64: 변환값.register_údaje[8] = 1; break;   /* write */
    case 57: 변환값.register_údaje[8] = 4; break;   /* close */
    case 62: 변환값.register_údaje[8] = 5; break;   /* lseek */
    case 46: 변환값.register_údaje[8] = 10; break;  /* ftruncate */
    case 82: 변환값.register_údaje[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Cesta[65]; int 반환값 = inštancia_cesta(Súbor_položka->register_údaje[1], Cesta); if (반환값) return 반환값;
        if ((int)Súbor_položka->register_údaje[0] != -100 && Cesta[0] != '/') return -95;
        if (수치 == 35 && Súbor_položka->register_údaje[2]) return -95;
        if (수치 == 56 && (Súbor_položka->register_údaje[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.register_údaje[8] = 수치 == 56 ? 3 : 11;
        변환값.register_údaje[0] = Súbor_položka->register_údaje[1];
        변환값.register_údaje[1] = Súbor_položka->register_údaje[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.register_údaje[2] = Súbor_položka->register_údaje[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = halda_ukončiť_hovor;
        변환값.register_údaje[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Súbor_položka->register_údaje[0] != 1) return -22;
        if (!používateľ_rozsah(Súbor_položka->register_údaje[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Súbor_položka->register_údaje[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return vlastník_objekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t položka_bod) {
    uintptr_t 맨위 = používateľ_ukončiť_hovor, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned položka_COUNT = 전달인수길이[순번] + 1;
        맨위 -= položka_COUNT; memcpy((void *)맨위, 전달인수[순번], položka_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Vrstvy_Úložisko = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *údaje_pozícia = (uint64_t *)Vrstvy_Úložisko;
    *údaje_pozícia++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *údaje_pozícia++ = 주소목록[순번];
    *údaje_pozícia++ = 0; *údaje_pozícia++ = 0;
    *údaje_pozícia++ = 6; *údaje_pozícia++ = veľkosť_stránky;
    *údaje_pozícia++ = 9; *údaje_pozícia++ = položka_bod;
    *údaje_pozícia++ = 0; *údaje_pozícia++ = 0;
    return Vrstvy_Úložisko;
}
