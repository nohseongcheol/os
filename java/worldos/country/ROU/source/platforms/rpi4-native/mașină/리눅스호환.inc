/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(utilizator_cadru *Fișier_intrare) {
    utilizator_cadru 변환값 = *Fișier_intrare;
    uintptr_t 수치 = Fișier_intrare->registru_date[8];
    switch (수치) {
    case 63: 변환값.registru_date[8] = 2; break;   /* read */
    case 64: 변환값.registru_date[8] = 1; break;   /* write */
    case 57: 변환값.registru_date[8] = 4; break;   /* close */
    case 62: 변환값.registru_date[8] = 5; break;   /* lseek */
    case 46: 변환값.registru_date[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registru_date[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Cale[65]; int 반환값 = copia_cale(Fișier_intrare->registru_date[1], Cale); if (반환값) return 반환값;
        if ((int)Fișier_intrare->registru_date[0] != -100 && Cale[0] != '/') return -95;
        if (수치 == 35 && Fișier_intrare->registru_date[2]) return -95;
        if (수치 == 56 && (Fișier_intrare->registru_date[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registru_date[8] = 수치 == 56 ? 3 : 11;
        변환값.registru_date[0] = Fișier_intrare->registru_date[1];
        변환값.registru_date[1] = Fișier_intrare->registru_date[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registru_date[2] = Fișier_intrare->registru_date[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Anteriorul = 동적기억끝;
        변환값.registru_date[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)Anteriorul : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fișier_intrare->registru_date[0] != 1) return -22;
        if (!utilizator_zonă(Fișier_intrare->registru_date[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fișier_intrare->registru_date[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return proprietar_obiect + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t intrare_p) {
    uintptr_t 맨위 = utilizator_termina_un_apel, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned element_COUNT = 전달인수길이[순번] + 1;
        맨위 -= element_COUNT; memcpy((void *)맨위, 전달인수[순번], element_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Teanc_Stocare = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *date_poziție = (uint64_t *)Teanc_Stocare;
    *date_poziție++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *date_poziție++ = 주소목록[순번];
    *date_poziție++ = 0; *date_poziție++ = 0;
    *date_poziție++ = 6; *date_poziție++ = dimensiune_pagină;
    *date_poziție++ = 9; *date_poziție++ = intrare_p;
    *date_poziție++ = 0; *date_poziție++ = 0;
    return Teanc_Stocare;
}
