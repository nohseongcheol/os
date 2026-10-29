/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t llamadaSistemaLinux(marcoUsuario *entradaElementoArchivo) {
    marcoUsuario traducido = *entradaElementoArchivo;
    uintptr_t valorNumérico = entradaElementoArchivo->registroDatos[8];
    switch (valorNumérico) {
    case 63: traducido.registroDatos[8] = 2; break;   /* read */
    case 64: traducido.registroDatos[8] = 1; break;   /* write */
    case 57: traducido.registroDatos[8] = 4; break;   /* close */
    case 62: traducido.registroDatos[8] = 5; break;   /* lseek */
    case 46: traducido.registroDatos[8] = 10; break;  /* ftruncate */
    case 82: traducido.registroDatos[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ruta[65]; int valorDevuelto = copiarRuta(entradaElementoArchivo->registroDatos[1], ruta); if (valorDevuelto) return valorDevuelto;
        if ((int)entradaElementoArchivo->registroDatos[0] != -100 && ruta[0] != '/') return -95;
        if (valorNumérico == 35 && entradaElementoArchivo->registroDatos[2]) return -95;
        if (valorNumérico == 56 && (entradaElementoArchivo->registroDatos[2] & ~(0x7fful | 0x80000ul))) return -95;
        traducido.registroDatos[8] = valorNumérico == 56 ? 3 : 11;
        traducido.registroDatos[0] = entradaElementoArchivo->registroDatos[1];
        traducido.registroDatos[1] = entradaElementoArchivo->registroDatos[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        traducido.registroDatos[2] = entradaElementoArchivo->registroDatos[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t elementoPrevio = finMontículo;
        traducido.registroDatos[8] = 8;
        intptr_t valorDevuelto = llamadaSistemaNativo(&traducido);
        return valorDevuelto < 0 ? (intptr_t)elementoPrevio : valorDevuelto;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (entradaElementoArchivo->registroDatos[0] != 1) return -22;
        if (!rangoUsuario(entradaElementoArchivo->registroDatos[1], 16, 1)) return -14;
        uint64_t milisegundos = milisegundosTranscurridosPlaca(), valor[2] = {milisegundos / 1000, (milisegundos % 1000) * 1000000};
        memcpy((void *)entradaElementoArchivo->registroDatos[1], valor, sizeof(valor)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return objetoPropietario + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return llamadaSistemaNativo(&traducido);
}

static uintptr_t pilaIniciarLinux(uintptr_t puntoEntradaElemento) {
    uintptr_t entradaElementoExtremoSuperior = finUsuario, direcciones[8];
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosArgumentoReenviado; índiceOrdinal++) {
        unsigned númeroElementosElementoLista = longitudArgumentoReenviado[índiceOrdinal] + 1;
        entradaElementoExtremoSuperior -= númeroElementosElementoLista; memcpy((void *)entradaElementoExtremoSuperior, argumentoReenviado[índiceOrdinal], númeroElementosElementoLista); direcciones[índiceOrdinal] = entradaElementoExtremoSuperior;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t almacenamientoPila = (entradaElementoExtremoSuperior - (númeroElementosArgumentoReenviado + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *posiciónDatos = (uint64_t *)almacenamientoPila;
    *posiciónDatos++ = númeroElementosArgumentoReenviado;
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosArgumentoReenviado; índiceOrdinal++) *posiciónDatos++ = direcciones[índiceOrdinal];
    *posiciónDatos++ = 0; *posiciónDatos++ = 0;
    *posiciónDatos++ = 6; *posiciónDatos++ = tamañoPágina;
    *posiciónDatos++ = 9; *posiciónDatos++ = puntoEntradaElemento;
    *posiciónDatos++ = 0; *posiciónDatos++ = 0;
    return almacenamientoPila;
}
