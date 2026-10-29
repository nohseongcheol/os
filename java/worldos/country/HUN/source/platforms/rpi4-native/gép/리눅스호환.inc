/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(felhasználó_doboz *Fájl_bejegyzés) {
    felhasználó_doboz 변환값 = *Fájl_bejegyzés;
    uintptr_t 수치 = Fájl_bejegyzés->jegyzék_adat[8];
    switch (수치) {
    case 63: 변환값.jegyzék_adat[8] = 2; break;   /* read */
    case 64: 변환값.jegyzék_adat[8] = 1; break;   /* write */
    case 57: 변환값.jegyzék_adat[8] = 4; break;   /* close */
    case 62: 변환값.jegyzék_adat[8] = 5; break;   /* lseek */
    case 46: 변환값.jegyzék_adat[8] = 10; break;  /* ftruncate */
    case 82: 변환값.jegyzék_adat[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ÚTVONAL[65]; int 반환값 = másol_útvonal(Fájl_bejegyzés->jegyzék_adat[1], ÚTVONAL); if (반환값) return 반환값;
        if ((int)Fájl_bejegyzés->jegyzék_adat[0] != -100 && ÚTVONAL[0] != '/') return -95;
        if (수치 == 35 && Fájl_bejegyzés->jegyzék_adat[2]) return -95;
        if (수치 == 56 && (Fájl_bejegyzés->jegyzék_adat[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.jegyzék_adat[8] = 수치 == 56 ? 3 : 11;
        변환값.jegyzék_adat[0] = Fájl_bejegyzés->jegyzék_adat[1];
        변환값.jegyzék_adat[1] = Fájl_bejegyzés->jegyzék_adat[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.jegyzék_adat[2] = Fájl_bejegyzés->jegyzék_adat[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Előző = halommemória_megszüntet;
        변환값.jegyzék_adat[8] = 8;
        intptr_t 반환값 = natív_Rendszer_hív(&변환값);
        return 반환값 < 0 ? (intptr_t)Előző : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fájl_bejegyzés->jegyzék_adat[0] != 1) return -22;
        if (!felhasználó_tartomány(Fájl_bejegyzés->jegyzék_adat[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), ÉRTÉK[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fájl_bejegyzés->jegyzék_adat[1], ÉRTÉK, sizeof(ÉRTÉK)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return tulajdonos_objektum + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return natív_Rendszer_hív(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t belépési_pont) {
    uintptr_t 맨위 = felhasználó_megszüntet, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned cikk_DARAB = 전달인수길이[순번] + 1;
        맨위 -= cikk_DARAB; memcpy((void *)맨위, 전달인수[순번], cikk_DARAB); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Sor_tár = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *adat_pozíció = (uint64_t *)Sor_tár;
    *adat_pozíció++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *adat_pozíció++ = 주소목록[순번];
    *adat_pozíció++ = 0; *adat_pozíció++ = 0;
    *adat_pozíció++ = 6; *adat_pozíció++ = oldalméret;
    *adat_pozíció++ = 9; *adat_pozíció++ = belépési_pont;
    *adat_pozíció++ = 0; *adat_pozíció++ = 0;
    return Sor_tár;
}
