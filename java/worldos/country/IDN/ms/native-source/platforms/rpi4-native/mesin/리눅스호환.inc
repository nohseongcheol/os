/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(pengguna_bingkai *fail_pemasukan) {
    pengguna_bingkai 변환값 = *fail_pemasukan;
    uintptr_t 수치 = fail_pemasukan->daftar_data[8];
    switch (수치) {
    case 63: 변환값.daftar_data[8] = 2; break;   /* read */
    case 64: 변환값.daftar_data[8] = 1; break;   /* write */
    case 57: 변환값.daftar_data[8] = 4; break;   /* close */
    case 62: 변환값.daftar_data[8] = 5; break;   /* lseek */
    case 46: 변환값.daftar_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.daftar_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char LALUAN[65]; int 반환값 = tika_laluan(fail_pemasukan->daftar_data[1], LALUAN); if (반환값) return 반환값;
        if ((int)fail_pemasukan->daftar_data[0] != -100 && LALUAN[0] != '/') return -95;
        if (수치 == 35 && fail_pemasukan->daftar_data[2]) return -95;
        if (수치 == 56 && (fail_pemasukan->daftar_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.daftar_data[8] = 수치 == 56 ? 3 : 11;
        변환값.daftar_data[0] = fail_pemasukan->daftar_data[1];
        변환값.daftar_data[1] = fail_pemasukan->daftar_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.daftar_data[2] = fail_pemasukan->daftar_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = timbunan_tamat;
        변환값.daftar_data[8] = 8;
        intptr_t 반환값 = asal_sistem_CALL(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (fail_pemasukan->daftar_data[0] != 1) return -22;
        if (!pengguna_julat(fail_pemasukan->daftar_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)fail_pemasukan->daftar_data[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return pemilik_objek + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return asal_sistem_CALL(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t titik_permulaan) {
    uintptr_t 맨위 = pengguna_tamat, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned item_COUNT = 전달인수길이[순번] + 1;
        맨위 -= item_COUNT; memcpy((void *)맨위, 전달인수[순번], item_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t ingatan_tindanan = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_jawatan = (uint64_t *)ingatan_tindanan;
    *data_jawatan++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_jawatan++ = 주소목록[순번];
    *data_jawatan++ = 0; *data_jawatan++ = 0;
    *data_jawatan++ = 6; *data_jawatan++ = saiz_halaman;
    *data_jawatan++ = 9; *data_jawatan++ = titik_permulaan;
    *data_jawatan++ = 0; *data_jawatan++ = 0;
    return ingatan_tindanan;
}
