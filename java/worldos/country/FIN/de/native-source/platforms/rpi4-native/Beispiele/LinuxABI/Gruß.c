/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long aufrufen(long Nummer, long ersterOperand, long zweiterOperand, long dritterOperand, long vierterOperand) {
    register long nullwertRegister __asm__("x0")=ersterOperand, einsRegister __asm__("x1")=zweiterOperand;
    register long zweiRegister __asm__("x2")=dritterOperand, dreiRegister __asm__("x3")=vierterOperand;
    register long achtRegister __asm__("x8")=Nummer;
    __asm__ volatile("svc #0" : "+r"(nullwertRegister) : "r"(einsRegister),"r"(zweiRegister),"r"(dreiRegister),"r"(achtRegister) : "memory","cc");
    return nullwertRegister;
}
static int Länge(const char *Text) { int Zahl=0;while(Text[Zahl])Zahl++;return Zahl; }
static int Ausgabe(const char *Text) { int Zahl=Länge(Text);return aufrufen(64,1,(long)Text,Zahl,0)==Zahl; }
int main(int argumentAnzahl,char **argumente) {
    if(argumentAnzahl!=2 || !argumente[0] || !argumente[1] || argumente[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long istNichtUnterstützt=aufrufen(6,99,0,0,0);
    if(istNichtUnterstützt!=-38 && istNichtUnterstützt!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(aufrufen(64,1,0x80000,1,0)!=-14)return 4;
    const char inhaltswertWert[]="LINUX ELF FILE IO\n";
    long Dokumentation=aufrufen(56,-100,(long)"linux.txt",578,0600);
    if(Dokumentation<0)return 5;
    if(aufrufen(64,Dokumentation,(long)inhaltswertWert,sizeof(inhaltswertWert)-1,0)!=sizeof(inhaltswertWert)-1)return 6;
    if(aufrufen(62,Dokumentation,0,0,0)!=0)return 7;
    char textWertLesen[sizeof(inhaltswertWert)]={0};
    if(aufrufen(63,Dokumentation,(long)textWertLesen,sizeof(inhaltswertWert)-1,0)!=sizeof(inhaltswertWert)-1)return 8;
    for(unsigned ordnungszahlIndex=0;ordnungszahlIndex<sizeof(inhaltswertWert);ordnungszahlIndex++)if(inhaltswertWert[ordnungszahlIndex]!=textWertLesen[ordnungszahlIndex])return 9;
    if(aufrufen(57,Dokumentation,0,0,0))return 10;
    long zeitWert[2];if(aufrufen(113,1,(long)zeitWert,0,0) || zeitWert[1]<0 || zeitWert[1]>=1000000000)return 11;
    if(!Ausgabe("LINUX ARM64 ELF PASS\n") || !Ausgabe(argumente[1]) || !Ausgabe("\n"))return 12;
    return 0;
}
