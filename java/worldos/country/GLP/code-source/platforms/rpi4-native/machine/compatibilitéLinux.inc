/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t appelSystèmeLinux(cadreUtilisateur *entréeÉlémentFichier) {
    cadreUtilisateur traduit = *entréeÉlémentFichier;
    uintptr_t valeurNumérique = entréeÉlémentFichier->registreDonnées[8];
    switch (valeurNumérique) {
    case 63: traduit.registreDonnées[8] = 2; break;   /* read */
    case 64: traduit.registreDonnées[8] = 1; break;   /* write */
    case 57: traduit.registreDonnées[8] = 4; break;   /* close */
    case 62: traduit.registreDonnées[8] = 5; break;   /* lseek */
    case 46: traduit.registreDonnées[8] = 10; break;  /* ftruncate */
    case 82: traduit.registreDonnées[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char chemin[65]; int valeurRetourné = copierChemin(entréeÉlémentFichier->registreDonnées[1], chemin); if (valeurRetourné) return valeurRetourné;
        if ((int)entréeÉlémentFichier->registreDonnées[0] != -100 && chemin[0] != '/') return -95;
        if (valeurNumérique == 35 && entréeÉlémentFichier->registreDonnées[2]) return -95;
        if (valeurNumérique == 56 && (entréeÉlémentFichier->registreDonnées[2] & ~(0x7fful | 0x80000ul))) return -95;
        traduit.registreDonnées[8] = valeurNumérique == 56 ? 3 : 11;
        traduit.registreDonnées[0] = entréeÉlémentFichier->registreDonnées[1];
        traduit.registreDonnées[1] = entréeÉlémentFichier->registreDonnées[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        traduit.registreDonnées[2] = entréeÉlémentFichier->registreDonnées[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t précédentÉlément = finTas;
        traduit.registreDonnées[8] = 8;
        intptr_t valeurRetourné = appelSystèmeNatif(&traduit);
        return valeurRetourné < 0 ? (intptr_t)précédentÉlément : valeurRetourné;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (entréeÉlémentFichier->registreDonnées[0] != 1) return -22;
        if (!plageUtilisateur(entréeÉlémentFichier->registreDonnées[1], 16, 1)) return -14;
        uint64_t millisecondes = millisecondesÉcouléesCarteMatérielle(), valeur[2] = {millisecondes / 1000, (millisecondes % 1000) * 1000000};
        memcpy((void *)entréeÉlémentFichier->registreDonnées[1], valeur, sizeof(valeur)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return objetPropriétaire + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return appelSystèmeNatif(&traduit);
}

static uintptr_t pileDémarrerLinux(uintptr_t pointEntréeÉlément) {
    uintptr_t entréeÉlémentSommet = finUtilisateur, adresses[8];
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsArgumentTransféré; indiceOrdinal++) {
        unsigned nombreÉlémentsÉlémentListe = longueurArgumentTransféré[indiceOrdinal] + 1;
        entréeÉlémentSommet -= nombreÉlémentsÉlémentListe; memcpy((void *)entréeÉlémentSommet, argumentTransféré[indiceOrdinal], nombreÉlémentsÉlémentListe); adresses[indiceOrdinal] = entréeÉlémentSommet;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t stockagePile = (entréeÉlémentSommet - (nombreÉlémentsArgumentTransféré + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *positionDonnées = (uint64_t *)stockagePile;
    *positionDonnées++ = nombreÉlémentsArgumentTransféré;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsArgumentTransféré; indiceOrdinal++) *positionDonnées++ = adresses[indiceOrdinal];
    *positionDonnées++ = 0; *positionDonnées++ = 0;
    *positionDonnées++ = 6; *positionDonnées++ = taillePage;
    *positionDonnées++ = 9; *positionDonnées++ = pointEntréeÉlément;
    *positionDonnées++ = 0; *positionDonnées++ = 0;
    return stockagePile;
}
