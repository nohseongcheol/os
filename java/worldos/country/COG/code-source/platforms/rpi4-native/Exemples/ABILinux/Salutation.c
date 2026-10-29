/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long invoquer(long numéro, long opérandePremier, long opérandeDeuxième, long opérandeTroisième, long opérandeQuatrième) {
    register long registreZéro __asm__("x0")=opérandePremier, registreUn __asm__("x1")=opérandeDeuxième;
    register long registreDeux __asm__("x2")=opérandeTroisième, registreTrois __asm__("x3")=opérandeQuatrième;
    register long registreHuit __asm__("x8")=numéro;
    __asm__ volatile("svc #0" : "+r"(registreZéro) : "r"(registreUn),"r"(registreDeux),"r"(registreTrois),"r"(registreHuit) : "memory","cc");
    return registreZéro;
}
static int longueur(const char *texte) { int nombre=0;while(texte[nombre])nombre++;return nombre; }
static int Sortie(const char *texte) { int nombre=longueur(texte);return invoquer(64,1,(long)texte,nombre,0)==nombre; }
int main(int nombreÉlémentsArgument,char **arguments) {
    if(nombreÉlémentsArgument!=2 || !arguments[0] || !arguments[1] || arguments[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long estNonPrisEnCharge=invoquer(6,99,0,0,0);
    if(estNonPrisEnCharge!=-38 && estNonPrisEnCharge!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(invoquer(64,1,0x80000,1,0)!=-14)return 4;
    const char valeurContenuValeur[]="LINUX ELF FILE IO\n";
    long Documentation=invoquer(56,-100,(long)"linux.txt",578,0600);
    if(Documentation<0)return 5;
    if(invoquer(64,Documentation,(long)valeurContenuValeur,sizeof(valeurContenuValeur)-1,0)!=sizeof(valeurContenuValeur)-1)return 6;
    if(invoquer(62,Documentation,0,0,0)!=0)return 7;
    char lireValeurTexte[sizeof(valeurContenuValeur)]={0};
    if(invoquer(63,Documentation,(long)lireValeurTexte,sizeof(valeurContenuValeur)-1,0)!=sizeof(valeurContenuValeur)-1)return 8;
    for(unsigned indiceOrdinal=0;indiceOrdinal<sizeof(valeurContenuValeur);indiceOrdinal++)if(valeurContenuValeur[indiceOrdinal]!=lireValeurTexte[indiceOrdinal])return 9;
    if(invoquer(57,Documentation,0,0,0))return 10;
    long valeurTemps[2];if(invoquer(113,1,(long)valeurTemps,0,0) || valeurTemps[1]<0 || valeurTemps[1]>=1000000000)return 11;
    if(!Sortie("LINUX ARM64 ELF PASS\n") || !Sortie(arguments[1]) || !Sortie("\n"))return 12;
    return 0;
}
