/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(uporabnik_okvir *Datoteka_vnos) {
    uporabnik_okvir 변환값 = *Datoteka_vnos;
    uintptr_t 수치 = Datoteka_vnos->register_podatki[8];
    switch (수치) {
    case 63: 변환값.register_podatki[8] = 2; break;   /* read */
    case 64: 변환값.register_podatki[8] = 1; break;   /* write */
    case 57: 변환값.register_podatki[8] = 4; break;   /* close */
    case 62: 변환값.register_podatki[8] = 5; break;   /* lseek */
    case 46: 변환값.register_podatki[8] = 10; break;  /* ftruncate */
    case 82: 변환값.register_podatki[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char POT[65]; int 반환값 = kopirati_pot(Datoteka_vnos->register_podatki[1], POT); if (반환값) return 반환값;
        if ((int)Datoteka_vnos->register_podatki[0] != -100 && POT[0] != '/') return -95;
        if (수치 == 35 && Datoteka_vnos->register_podatki[2]) return -95;
        if (수치 == 56 && (Datoteka_vnos->register_podatki[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.register_podatki[8] = 수치 == 56 ? 3 : 11;
        변환값.register_podatki[0] = Datoteka_vnos->register_podatki[1];
        변환값.register_podatki[1] = Datoteka_vnos->register_podatki[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.register_podatki[2] = Datoteka_vnos->register_podatki[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = kopica_končati_klic;
        변환값.register_podatki[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Datoteka_vnos->register_podatki[0] != 1) return -22;
        if (!uporabnik_obseg(Datoteka_vnos->register_podatki[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Datoteka_vnos->register_podatki[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return lastnik_predmet + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t vnos_p) {
    uintptr_t 맨위 = uporabnik_končati_klic, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned element_COUNT = 전달인수길이[순번] + 1;
        맨위 -= element_COUNT; memcpy((void *)맨위, 전달인수[순번], element_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Sklad_Senzor_prostora = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *podatki_položaj = (uint64_t *)Sklad_Senzor_prostora;
    *podatki_položaj++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *podatki_položaj++ = 주소목록[순번];
    *podatki_položaj++ = 0; *podatki_položaj++ = 0;
    *podatki_položaj++ = 6; *podatki_položaj++ = velikost_strani;
    *podatki_položaj++ = 9; *podatki_položaj++ = vnos_p;
    *podatki_položaj++ = 0; *podatki_položaj++ = 0;
    return Sklad_Senzor_prostora;
}
