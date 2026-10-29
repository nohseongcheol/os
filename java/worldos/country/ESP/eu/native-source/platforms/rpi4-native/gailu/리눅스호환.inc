/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(erabiltzaile_marko *fitxategi_sarrera) {
    erabiltzaile_marko 변환값 = *fitxategi_sarrera;
    uintptr_t 수치 = fitxategi_sarrera->izena_eman_datuak[8];
    switch (수치) {
    case 63: 변환값.izena_eman_datuak[8] = 2; break;   /* read */
    case 64: 변환값.izena_eman_datuak[8] = 1; break;   /* write */
    case 57: 변환값.izena_eman_datuak[8] = 4; break;   /* close */
    case 62: 변환값.izena_eman_datuak[8] = 5; break;   /* lseek */
    case 46: 변환값.izena_eman_datuak[8] = 10; break;  /* ftruncate */
    case 82: 변환값.izena_eman_datuak[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Bide_izena[65]; int 반환값 = kopiatu_bide_izen(fitxategi_sarrera->izena_eman_datuak[1], Bide_izena); if (반환값) return 반환값;
        if ((int)fitxategi_sarrera->izena_eman_datuak[0] != -100 && Bide_izena[0] != '/') return -95;
        if (수치 == 35 && fitxategi_sarrera->izena_eman_datuak[2]) return -95;
        if (수치 == 56 && (fitxategi_sarrera->izena_eman_datuak[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.izena_eman_datuak[8] = 수치 == 56 ? 3 : 11;
        변환값.izena_eman_datuak[0] = fitxategi_sarrera->izena_eman_datuak[1];
        변환값.izena_eman_datuak[1] = fitxategi_sarrera->izena_eman_datuak[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.izena_eman_datuak[2] = fitxategi_sarrera->izena_eman_datuak[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.izena_eman_datuak[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (fitxategi_sarrera->izena_eman_datuak[0] != 1) return -22;
        if (!erabiltzaile_barruti(fitxategi_sarrera->izena_eman_datuak[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), balio[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)fitxategi_sarrera->izena_eman_datuak[1], balio, sizeof(balio)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return jabe_objektu + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t sarrera_p) {
    uintptr_t 맨위 = erabiltzaile_amaitu, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned elementu_ZENBATU = 전달인수길이[순번] + 1;
        맨위 -= elementu_ZENBATU; memcpy((void *)맨위, 전달인수[순번], elementu_ZENBATU); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t pila_biltegi = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *datuak_kargu = (uint64_t *)pila_biltegi;
    *datuak_kargu++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *datuak_kargu++ = 주소목록[순번];
    *datuak_kargu++ = 0; *datuak_kargu++ = 0;
    *datuak_kargu++ = 6; *datuak_kargu++ = orrialdearen_tamaina;
    *datuak_kargu++ = 9; *datuak_kargu++ = sarrera_p;
    *datuak_kargu++ = 0; *datuak_kargu++ = 0;
    return pila_biltegi;
}
