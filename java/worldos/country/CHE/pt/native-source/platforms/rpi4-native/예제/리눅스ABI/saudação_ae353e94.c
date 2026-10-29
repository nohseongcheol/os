/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 호출(long ÍNDICE, long 가, long SEGUNDO_operando, long 다, long 라) {
    register long registro_zero __asm__("x0")=가, 저장기일 __asm__("x1")=SEGUNDO_operando;
    register long 저장기이 __asm__("x2")=다, 저장기삼 __asm__("x3")=라;
    register long 저장기팔 __asm__("x8")=ÍNDICE;
    __asm__ volatile("svc #0" : "+r"(registro_zero) : "r"(저장기일),"r"(저장기이),"r"(저장기삼),"r"(저장기팔) : "memory","cc");
    return registro_zero;
}
static int duração_VALOR(const char *texto) { int número=0;while(texto[número])número++;return número; }
static int saídaTexto(const char *texto) { int número=duração_VALOR(texto);return 호출(64,1,(long)texto,número,0)==número; }
int main(int argumento_CONT_NÚM,char **argumentos) {
    if(argumento_CONT_NÚM!=2 || !argumentos[0] || !argumentos[1] || argumentos[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 미지원=호출(6,99,0,0,0);
    if(미지원!=-38 && 미지원!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(호출(64,1,0x80000,1,0)!=-14)return 4;
    const char Conteúdo_VALOR[]="LINUX ELF FILE IO\n";
    long 문서=호출(56,-100,(long)"linux.txt",578,0600);
    if(문서<0)return 5;
    if(호출(64,문서,(long)Conteúdo_VALOR,sizeof(Conteúdo_VALOR)-1,0)!=sizeof(Conteúdo_VALOR)-1)return 6;
    if(호출(62,문서,0,0,0)!=0)return 7;
    char leitura_SMS_VALOR[sizeof(Conteúdo_VALOR)]={0};
    if(호출(63,문서,(long)leitura_SMS_VALOR,sizeof(Conteúdo_VALOR)-1,0)!=sizeof(Conteúdo_VALOR)-1)return 8;
    for(unsigned 순번=0;순번<sizeof(Conteúdo_VALOR);순번++)if(Conteúdo_VALOR[순번]!=leitura_SMS_VALOR[순번])return 9;
    if(호출(57,문서,0,0,0))return 10;
    long valor_temporal[2];if(호출(113,1,(long)valor_temporal,0,0) || valor_temporal[1]<0 || valor_temporal[1]>=1000000000)return 11;
    if(!saídaTexto("LINUX ARM64 ELF PASS\n") || !saídaTexto(argumentos[1]) || !saídaTexto("\n"))return 12;
    return 0;
}
