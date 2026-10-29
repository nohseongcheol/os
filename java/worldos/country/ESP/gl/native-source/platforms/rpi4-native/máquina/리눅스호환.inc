/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(usuario_marco *Ficheiro_introdución) {
    usuario_marco 변환값 = *Ficheiro_introdución;
    uintptr_t 수치 = Ficheiro_introdución->rexistrarse_datos[8];
    switch (수치) {
    case 63: 변환값.rexistrarse_datos[8] = 2; break;   /* read */
    case 64: 변환값.rexistrarse_datos[8] = 1; break;   /* write */
    case 57: 변환값.rexistrarse_datos[8] = 4; break;   /* close */
    case 62: 변환값.rexistrarse_datos[8] = 5; break;   /* lseek */
    case 46: 변환값.rexistrarse_datos[8] = 10; break;  /* ftruncate */
    case 82: 변환값.rexistrarse_datos[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char CAMIÑO[65]; int 반환값 = copiar_camiño(Ficheiro_introdución->rexistrarse_datos[1], CAMIÑO); if (반환값) return 반환값;
        if ((int)Ficheiro_introdución->rexistrarse_datos[0] != -100 && CAMIÑO[0] != '/') return -95;
        if (수치 == 35 && Ficheiro_introdución->rexistrarse_datos[2]) return -95;
        if (수치 == 56 && (Ficheiro_introdución->rexistrarse_datos[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.rexistrarse_datos[8] = 수치 == 56 ? 3 : 11;
        변환값.rexistrarse_datos[0] = Ficheiro_introdución->rexistrarse_datos[1];
        변환값.rexistrarse_datos[1] = Ficheiro_introdución->rexistrarse_datos[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.rexistrarse_datos[2] = Ficheiro_introdución->rexistrarse_datos[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.rexistrarse_datos[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Ficheiro_introdución->rexistrarse_datos[0] != 1) return -22;
        if (!usuario_intervalo(Ficheiro_introdución->rexistrarse_datos[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALOR[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Ficheiro_introdución->rexistrarse_datos[1], VALOR, sizeof(VALOR)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return propietario_obxecto + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t introdución_p) {
    uintptr_t 맨위 = usuario_finalizar, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned elemento_CONTAR = 전달인수길이[순번] + 1;
        맨위 -= elemento_CONTAR; memcpy((void *)맨위, 전달인수[순번], elemento_CONTAR); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Montón_Almacenamento = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *datos_cargo = (uint64_t *)Montón_Almacenamento;
    *datos_cargo++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *datos_cargo++ = 주소목록[순번];
    *datos_cargo++ = 0; *datos_cargo++ = 0;
    *datos_cargo++ = 6; *datos_cargo++ = tamaño_da_páxina;
    *datos_cargo++ = 9; *datos_cargo++ = introdución_p;
    *datos_cargo++ = 0; *datos_cargo++ = 0;
    return Montón_Almacenamento;
}
