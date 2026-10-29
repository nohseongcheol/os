/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(uživatel_rámec *Soubor_položka) {
    uživatel_rámec 변환값 = *Soubor_položka;
    uintptr_t 수치 = Soubor_položka->registr_data[8];
    switch (수치) {
    case 63: 변환값.registr_data[8] = 2; break;   /* read */
    case 64: 변환값.registr_data[8] = 1; break;   /* write */
    case 57: 변환값.registr_data[8] = 4; break;   /* close */
    case 62: 변환값.registr_data[8] = 5; break;   /* lseek */
    case 46: 변환값.registr_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registr_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char cesta_2[65]; int 반환값 = instance_cesta(Soubor_položka->registr_data[1], cesta_2); if (반환값) return 반환값;
        if ((int)Soubor_položka->registr_data[0] != -100 && cesta_2[0] != '/') return -95;
        if (수치 == 35 && Soubor_položka->registr_data[2]) return -95;
        if (수치 == 56 && (Soubor_položka->registr_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registr_data[8] = 수치 == 56 ? 3 : 11;
        변환값.registr_data[0] = Soubor_položka->registr_data[1];
        변환값.registr_data[1] = Soubor_položka->registr_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registr_data[2] = Soubor_položka->registr_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Předchozí = halda_konec;
        변환값.registr_data[8] = 8;
        intptr_t 반환값 = nativní_Systém_VOLAT(&변환값);
        return 반환값 < 0 ? (intptr_t)Předchozí : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Soubor_položka->registr_data[0] != 1) return -22;
        if (!uživatel_oblast(Soubor_položka->registr_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), HODNOTA[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Soubor_položka->registr_data[1], HODNOTA, sizeof(HODNOTA)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return vlastník_objekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return nativní_Systém_VOLAT(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t vstupní_bod) {
    uintptr_t 맨위 = uživatel_konec, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned zboží_POČET = 전달인수길이[순번] + 1;
        맨위 -= zboží_POČET; memcpy((void *)맨위, 전달인수[순번], zboží_POČET); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t paměť_zásobníku = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_pozice = (uint64_t *)paměť_zásobníku;
    *data_pozice++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_pozice++ = 주소목록[순번];
    *data_pozice++ = 0; *data_pozice++ = 0;
    *data_pozice++ = 6; *data_pozice++ = velikost_stránky;
    *data_pozice++ = 9; *data_pozice++ = vstupní_bod;
    *data_pozice++ = 0; *data_pozice++ = 0;
    return paměť_zásobníku;
}
