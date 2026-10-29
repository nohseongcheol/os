/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t linuxSystemAufrufVorgang(benutzerRahmen *dateiEintrag) {
    benutzerRahmen übersetzt = *dateiEintrag;
    uintptr_t numerischWert = dateiEintrag->datenRegister[8];
    switch (numerischWert) {
    case 63: übersetzt.datenRegister[8] = 2; break;   /* read */
    case 64: übersetzt.datenRegister[8] = 1; break;   /* write */
    case 57: übersetzt.datenRegister[8] = 4; break;   /* close */
    case 62: übersetzt.datenRegister[8] = 5; break;   /* lseek */
    case 46: übersetzt.datenRegister[8] = 10; break;  /* ftruncate */
    case 82: übersetzt.datenRegister[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char pfad[65]; int zurückgegebenWert = pfadKopieren(dateiEintrag->datenRegister[1], pfad); if (zurückgegebenWert) return zurückgegebenWert;
        if ((int)dateiEintrag->datenRegister[0] != -100 && pfad[0] != '/') return -95;
        if (numerischWert == 35 && dateiEintrag->datenRegister[2]) return -95;
        if (numerischWert == 56 && (dateiEintrag->datenRegister[2] & ~(0x7fful | 0x80000ul))) return -95;
        übersetzt.datenRegister[8] = numerischWert == 56 ? 3 : 11;
        übersetzt.datenRegister[0] = dateiEintrag->datenRegister[1];
        übersetzt.datenRegister[1] = dateiEintrag->datenRegister[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        übersetzt.datenRegister[2] = dateiEintrag->datenRegister[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t vorherig = speicherhaldeEnde;
        übersetzt.datenRegister[8] = 8;
        intptr_t zurückgegebenWert = systemnahSystemAufrufVorgang(&übersetzt);
        return zurückgegebenWert < 0 ? (intptr_t)vorherig : zurückgegebenWert;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (dateiEintrag->datenRegister[0] != 1) return -22;
        if (!benutzerBereich(dateiEintrag->datenRegister[1], 16, 1)) return -14;
        uint64_t millisekunden = platineVergangeneMillisekunden(), Wert[2] = {millisekunden / 1000, (millisekunden % 1000) * 1000000};
        memcpy((void *)dateiEintrag->datenRegister[1], Wert, sizeof(Wert)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return eigentümerObjekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return systemnahSystemAufrufVorgang(&übersetzt);
}

static uintptr_t linuxStartenStapel(uintptr_t eintragPunkt) {
    uintptr_t oberkanteEintrag = benutzerEnde, adressen[8];
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < weitergeleitetArgumentAnzahl; ordnungszahlIndex++) {
        unsigned elementeintragAnzahl = weitergeleitetArgumentLänge[ordnungszahlIndex] + 1;
        oberkanteEintrag -= elementeintragAnzahl; memcpy((void *)oberkanteEintrag, weitergeleitetArgument[ordnungszahlIndex], elementeintragAnzahl); adressen[ordnungszahlIndex] = oberkanteEintrag;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t stapelSpeichergerät = (oberkanteEintrag - (weitergeleitetArgumentAnzahl + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *datenPosition = (uint64_t *)stapelSpeichergerät;
    *datenPosition++ = weitergeleitetArgumentAnzahl;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < weitergeleitetArgumentAnzahl; ordnungszahlIndex++) *datenPosition++ = adressen[ordnungszahlIndex];
    *datenPosition++ = 0; *datenPosition++ = 0;
    *datenPosition++ = 6; *datenPosition++ = seiteGröße;
    *datenPosition++ = 9; *datenPosition++ = eintragPunkt;
    *datenPosition++ = 0; *datenPosition++ = 0;
    return stapelSpeichergerät;
}
