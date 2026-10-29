/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(użytkownik_kadr *Plik_wpis) {
    użytkownik_kadr 변환값 = *Plik_wpis;
    uintptr_t 수치 = Plik_wpis->rejestr_dane[8];
    switch (수치) {
    case 63: 변환값.rejestr_dane[8] = 2; break;   /* read */
    case 64: 변환값.rejestr_dane[8] = 1; break;   /* write */
    case 57: 변환값.rejestr_dane[8] = 4; break;   /* close */
    case 62: 변환값.rejestr_dane[8] = 5; break;   /* lseek */
    case 46: 변환값.rejestr_dane[8] = 10; break;  /* ftruncate */
    case 82: 변환값.rejestr_dane[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ścieżka_2[65]; int 반환값 = kopiować_ścieżka(Plik_wpis->rejestr_dane[1], ścieżka_2); if (반환값) return 반환값;
        if ((int)Plik_wpis->rejestr_dane[0] != -100 && ścieżka_2[0] != '/') return -95;
        if (수치 == 35 && Plik_wpis->rejestr_dane[2]) return -95;
        if (수치 == 56 && (Plik_wpis->rejestr_dane[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.rejestr_dane[8] = 수치 == 56 ? 3 : 11;
        변환값.rejestr_dane[0] = Plik_wpis->rejestr_dane[1];
        변환값.rejestr_dane[1] = Plik_wpis->rejestr_dane[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.rejestr_dane[2] = Plik_wpis->rejestr_dane[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Wstecz = sterta_Koniec;
        변환값.rejestr_dane[8] = 8;
        intptr_t 반환값 = natywny_System_Połącz(&변환값);
        return 반환값 < 0 ? (intptr_t)Wstecz : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Plik_wpis->rejestr_dane[0] != 1) return -22;
        if (!użytkownik_zakres(Plik_wpis->rejestr_dane[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), WARTOŚĆ[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Plik_wpis->rejestr_dane[1], WARTOŚĆ, sizeof(WARTOŚĆ)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return właściciel_obiekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return natywny_System_Połącz(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t punkt_wejścia) {
    uintptr_t 맨위 = użytkownik_Koniec, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned towar_ILE_LICZB = 전달인수길이[순번] + 1;
        맨위 -= towar_ILE_LICZB; memcpy((void *)맨위, 전달인수[순번], towar_ILE_LICZB); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t pamięć_stosu = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dane_stanowisko = (uint64_t *)pamięć_stosu;
    *dane_stanowisko++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *dane_stanowisko++ = 주소목록[순번];
    *dane_stanowisko++ = 0; *dane_stanowisko++ = 0;
    *dane_stanowisko++ = 6; *dane_stanowisko++ = rozmiar_strony;
    *dane_stanowisko++ = 9; *dane_stanowisko++ = punkt_wejścia;
    *dane_stanowisko++ = 0; *dane_stanowisko++ = 0;
    return pamięć_stosu;
}
