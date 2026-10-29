/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(naudotojas_kadras *Failas_įrašas) {
    naudotojas_kadras 변환값 = *Failas_įrašas;
    uintptr_t 수치 = Failas_įrašas->registras_duomenys[8];
    switch (수치) {
    case 63: 변환값.registras_duomenys[8] = 2; break;   /* read */
    case 64: 변환값.registras_duomenys[8] = 1; break;   /* write */
    case 57: 변환값.registras_duomenys[8] = 4; break;   /* close */
    case 62: 변환값.registras_duomenys[8] = 5; break;   /* lseek */
    case 46: 변환값.registras_duomenys[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registras_duomenys[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char KELIAS[65]; int 반환값 = kopijuoti_kelias(Failas_įrašas->registras_duomenys[1], KELIAS); if (반환값) return 반환값;
        if ((int)Failas_įrašas->registras_duomenys[0] != -100 && KELIAS[0] != '/') return -95;
        if (수치 == 35 && Failas_įrašas->registras_duomenys[2]) return -95;
        if (수치 == 56 && (Failas_įrašas->registras_duomenys[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registras_duomenys[8] = 수치 == 56 ? 3 : 11;
        변환값.registras_duomenys[0] = Failas_įrašas->registras_duomenys[1];
        변환값.registras_duomenys[1] = Failas_įrašas->registras_duomenys[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registras_duomenys[2] = Failas_įrašas->registras_duomenys[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.registras_duomenys[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Failas_įrašas->registras_duomenys[0] != 1) return -22;
        if (!naudotojas_diapazonas(Failas_įrašas->registras_duomenys[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Failas_įrašas->registras_duomenys[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return savininkas_objektas + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t įrašas_p) {
    uintptr_t 맨위 = naudotojas_baigti_pokalbį, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned prekė_COUNT = 전달인수길이[순번] + 1;
        맨위 -= prekė_COUNT; memcpy((void *)맨위, 전달인수[순번], prekė_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t eilė_Saugykla = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *duomenys_padėtis = (uint64_t *)eilė_Saugykla;
    *duomenys_padėtis++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *duomenys_padėtis++ = 주소목록[순번];
    *duomenys_padėtis++ = 0; *duomenys_padėtis++ = 0;
    *duomenys_padėtis++ = 6; *duomenys_padėtis++ = puslapio_formatas;
    *duomenys_padėtis++ = 9; *duomenys_padėtis++ = įrašas_p;
    *duomenys_padėtis++ = 0; *duomenys_padėtis++ = 0;
    return eilė_Saugykla;
}
