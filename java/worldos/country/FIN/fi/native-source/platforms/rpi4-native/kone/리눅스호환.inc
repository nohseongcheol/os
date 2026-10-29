/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(käyttäjä_kuva *Tiedosto_merkintä) {
    käyttäjä_kuva 변환값 = *Tiedosto_merkintä;
    uintptr_t 수치 = Tiedosto_merkintä->rekisteri_data[8];
    switch (수치) {
    case 63: 변환값.rekisteri_data[8] = 2; break;   /* read */
    case 64: 변환값.rekisteri_data[8] = 1; break;   /* write */
    case 57: 변환값.rekisteri_data[8] = 4; break;   /* close */
    case 62: 변환값.rekisteri_data[8] = 5; break;   /* lseek */
    case 46: 변환값.rekisteri_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.rekisteri_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char polku_2[65]; int 반환값 = kopioida_polku(Tiedosto_merkintä->rekisteri_data[1], polku_2); if (반환값) return 반환값;
        if ((int)Tiedosto_merkintä->rekisteri_data[0] != -100 && polku_2[0] != '/') return -95;
        if (수치 == 35 && Tiedosto_merkintä->rekisteri_data[2]) return -95;
        if (수치 == 56 && (Tiedosto_merkintä->rekisteri_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.rekisteri_data[8] = 수치 == 56 ? 3 : 11;
        변환값.rekisteri_data[0] = Tiedosto_merkintä->rekisteri_data[1];
        변환값.rekisteri_data[1] = Tiedosto_merkintä->rekisteri_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.rekisteri_data[2] = Tiedosto_merkintä->rekisteri_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Edellinen = keko_lopettaa_puhelu;
        변환값.rekisteri_data[8] = 8;
        intptr_t 반환값 = alkuperäinen_Järjestelmä_KUTSU(&변환값);
        return 반환값 < 0 ? (intptr_t)Edellinen : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Tiedosto_merkintä->rekisteri_data[0] != 1) return -22;
        if (!käyttäjä_alue(Tiedosto_merkintä->rekisteri_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), ARVO[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Tiedosto_merkintä->rekisteri_data[1], ARVO, sizeof(ARVO)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return omistaja_objekti + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return alkuperäinen_Järjestelmä_KUTSU(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t aloituskohta) {
    uintptr_t 맨위 = käyttäjä_lopettaa_puhelu, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned kohde_LASKE = 전달인수길이[순번] + 1;
        맨위 -= kohde_LASKE; memcpy((void *)맨위, 전달인수[순번], kohde_LASKE); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t pinomuisti = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_toimi = (uint64_t *)pinomuisti;
    *data_toimi++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_toimi++ = 주소목록[순번];
    *data_toimi++ = 0; *data_toimi++ = 0;
    *data_toimi++ = 6; *data_toimi++ = sivukoko;
    *data_toimi++ = 9; *data_toimi++ = aloituskohta;
    *data_toimi++ = 0; *data_toimi++ = 0;
    return pinomuisti;
}
