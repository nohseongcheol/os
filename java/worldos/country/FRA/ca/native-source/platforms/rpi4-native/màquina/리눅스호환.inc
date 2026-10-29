/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(usuari_marc *arxiu_introducció) {
    usuari_marc 변환값 = *arxiu_introducció;
    uintptr_t 수치 = arxiu_introducció->registrar_se_dades[8];
    switch (수치) {
    case 63: 변환값.registrar_se_dades[8] = 2; break;   /* read */
    case 64: 변환값.registrar_se_dades[8] = 1; break;   /* write */
    case 57: 변환값.registrar_se_dades[8] = 4; break;   /* close */
    case 62: 변환값.registrar_se_dades[8] = 5; break;   /* lseek */
    case 46: 변환값.registrar_se_dades[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registrar_se_dades[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Camí[65]; int 반환값 = copiar_camí(arxiu_introducció->registrar_se_dades[1], Camí); if (반환값) return 반환값;
        if ((int)arxiu_introducció->registrar_se_dades[0] != -100 && Camí[0] != '/') return -95;
        if (수치 == 35 && arxiu_introducció->registrar_se_dades[2]) return -95;
        if (수치 == 56 && (arxiu_introducció->registrar_se_dades[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registrar_se_dades[8] = 수치 == 56 ? 3 : 11;
        변환값.registrar_se_dades[0] = arxiu_introducció->registrar_se_dades[1];
        변환값.registrar_se_dades[1] = arxiu_introducció->registrar_se_dades[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registrar_se_dades[2] = arxiu_introducció->registrar_se_dades[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.registrar_se_dades[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (arxiu_introducció->registrar_se_dades[0] != 1) return -22;
        if (!usuari_interval(arxiu_introducció->registrar_se_dades[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALOR[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)arxiu_introducció->registrar_se_dades[1], VALOR, sizeof(VALOR)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return propietari_objecte + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t introducció_p) {
    uintptr_t 맨위 = usuari_finalitzar, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned element_COMPT = 전달인수길이[순번] + 1;
        맨위 -= element_COMPT; memcpy((void *)맨위, 전달인수[순번], element_COMPT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Pila_Emmagatzematge = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dades_càrrec = (uint64_t *)Pila_Emmagatzematge;
    *dades_càrrec++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *dades_càrrec++ = 주소목록[순번];
    *dades_càrrec++ = 0; *dades_càrrec++ = 0;
    *dades_càrrec++ = 6; *dades_càrrec++ = mida_de_la_pàgina;
    *dades_càrrec++ = 9; *dades_càrrec++ = introducció_p;
    *dades_càrrec++ = 0; *dades_càrrec++ = 0;
    return Pila_Emmagatzematge;
}
