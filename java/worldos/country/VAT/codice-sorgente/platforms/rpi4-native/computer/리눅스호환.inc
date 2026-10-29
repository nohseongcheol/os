/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(USER_frame *File_voce) {
    USER_frame 변환값 = *File_voce;
    uintptr_t 수치 = File_voce->registro_dati[8];
    switch (수치) {
    case 63: 변환값.registro_dati[8] = 2; break;   /* read */
    case 64: 변환값.registro_dati[8] = 1; break;   /* write */
    case 57: 변환값.registro_dati[8] = 4; break;   /* close */
    case 62: 변환값.registro_dati[8] = 5; break;   /* lseek */
    case 46: 변환값.registro_dati[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registro_dati[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char percorso[65]; int 반환값 = copiare_percorso(File_voce->registro_dati[1], percorso); if (반환값) return 반환값;
        if ((int)File_voce->registro_dati[0] != -100 && percorso[0] != '/') return -95;
        if (수치 == 35 && File_voce->registro_dati[2]) return -95;
        if (수치 == 56 && (File_voce->registro_dati[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registro_dati[8] = 수치 == 56 ? 3 : 11;
        변환값.registro_dati[0] = File_voce->registro_dati[1];
        변환값.registro_dati[1] = File_voce->registro_dati[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registro_dati[2] = File_voce->registro_dati[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Indietro = heap_chiudere;
        변환값.registro_dati[8] = 8;
        intptr_t 반환값 = nativo_Sistema_Chiama(&변환값);
        return 반환값 < 0 ? (intptr_t)Indietro : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (File_voce->registro_dati[0] != 1) return -22;
        if (!USER_intervallo(File_voce->registro_dati[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALORE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)File_voce->registro_dati[1], VALORE, sizeof(VALORE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return proprietario_oggetto + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return nativo_Sistema_Chiama(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t punto_di_ingresso) {
    uintptr_t 맨위 = USER_chiudere, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned articolo_CONTA_NUMERI = 전달인수길이[순번] + 1;
        맨위 -= articolo_CONTA_NUMERI; memcpy((void *)맨위, 전달인수[순번], articolo_CONTA_NUMERI); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t memoria_a_pila = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dati_funzione = (uint64_t *)memoria_a_pila;
    *dati_funzione++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *dati_funzione++ = 주소목록[순번];
    *dati_funzione++ = 0; *dati_funzione++ = 0;
    *dati_funzione++ = 6; *dati_funzione++ = dimensioni_della_pagina;
    *dati_funzione++ = 9; *dati_funzione++ = punto_di_ingresso;
    *dati_funzione++ = 0; *dati_funzione++ = 0;
    return memoria_a_pila;
}
