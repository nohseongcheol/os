/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(usuário_quadro *Arquivo_entrada) {
    usuário_quadro 변환값 = *Arquivo_entrada;
    uintptr_t 수치 = Arquivo_entrada->registro_dados[8];
    switch (수치) {
    case 63: 변환값.registro_dados[8] = 2; break;   /* read */
    case 64: 변환값.registro_dados[8] = 1; break;   /* write */
    case 57: 변환값.registro_dados[8] = 4; break;   /* close */
    case 62: 변환값.registro_dados[8] = 5; break;   /* lseek */
    case 46: 변환값.registro_dados[8] = 10; break;  /* ftruncate */
    case 82: 변환값.registro_dados[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char caminho[65]; int 반환값 = copiar_caminho(Arquivo_entrada->registro_dados[1], caminho); if (반환값) return 반환값;
        if ((int)Arquivo_entrada->registro_dados[0] != -100 && caminho[0] != '/') return -95;
        if (수치 == 35 && Arquivo_entrada->registro_dados[2]) return -95;
        if (수치 == 56 && (Arquivo_entrada->registro_dados[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.registro_dados[8] = 수치 == 56 ? 3 : 11;
        변환값.registro_dados[0] = Arquivo_entrada->registro_dados[1];
        변환값.registro_dados[1] = Arquivo_entrada->registro_dados[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.registro_dados[2] = Arquivo_entrada->registro_dados[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Anterior = heap_encerrar;
        변환값.registro_dados[8] = 8;
        intptr_t 반환값 = nativo_Sistema_Ligar(&변환값);
        return 반환값 < 0 ? (intptr_t)Anterior : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Arquivo_entrada->registro_dados[0] != 1) return -22;
        if (!usuário_alcance(Arquivo_entrada->registro_dados[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALOR[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Arquivo_entrada->registro_dados[1], VALOR, sizeof(VALOR)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return proprietário_objeto + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return nativo_Sistema_Ligar(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ponto_de_entrada) {
    uintptr_t 맨위 = usuário_encerrar, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned item_CONT_NÚM = 전달인수길이[순번] + 1;
        맨위 -= item_CONT_NÚM; memcpy((void *)맨위, 전달인수[순번], item_CONT_NÚM); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t memória_de_pilha = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dados_cargo = (uint64_t *)memória_de_pilha;
    *dados_cargo++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *dados_cargo++ = 주소목록[순번];
    *dados_cargo++ = 0; *dados_cargo++ = 0;
    *dados_cargo++ = 6; *dados_cargo++ = tamanho_da_página;
    *dados_cargo++ = 9; *dados_cargo++ = ponto_de_entrada;
    *dados_cargo++ = 0; *dados_cargo++ = 0;
    return memória_de_pilha;
}
