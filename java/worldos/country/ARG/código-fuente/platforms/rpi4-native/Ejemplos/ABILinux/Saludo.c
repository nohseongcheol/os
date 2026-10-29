/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long invocar(long número, long operandoPrimero, long operandoSegundo, long operandoTercero, long operandoCuarto) {
    register long registroCero __asm__("x0")=operandoPrimero, registroUno __asm__("x1")=operandoSegundo;
    register long registroDos __asm__("x2")=operandoTercero, registroTres __asm__("x3")=operandoCuarto;
    register long registroOcho __asm__("x8")=número;
    __asm__ volatile("svc #0" : "+r"(registroCero) : "r"(registroUno),"r"(registroDos),"r"(registroTres),"r"(registroOcho) : "memory","cc");
    return registroCero;
}
static int longitud(const char *texto) { int númeroValor=0;while(texto[númeroValor])númeroValor++;return númeroValor; }
static int Salida(const char *texto) { int númeroValor=longitud(texto);return invocar(64,1,(long)texto,númeroValor,0)==númeroValor; }
int main(int númeroElementosArgumento,char **argumentos) {
    if(númeroElementosArgumento!=2 || !argumentos[0] || !argumentos[1] || argumentos[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long esNoAdmitido=invocar(6,99,0,0,0);
    if(esNoAdmitido!=-38 && esNoAdmitido!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(invocar(64,1,0x80000,1,0)!=-14)return 4;
    const char valorContenidoValor[]="LINUX ELF FILE IO\n";
    long Documentación=invocar(56,-100,(long)"linux.txt",578,0600);
    if(Documentación<0)return 5;
    if(invocar(64,Documentación,(long)valorContenidoValor,sizeof(valorContenidoValor)-1,0)!=sizeof(valorContenidoValor)-1)return 6;
    if(invocar(62,Documentación,0,0,0)!=0)return 7;
    char leerValorTexto[sizeof(valorContenidoValor)]={0};
    if(invocar(63,Documentación,(long)leerValorTexto,sizeof(valorContenidoValor)-1,0)!=sizeof(valorContenidoValor)-1)return 8;
    for(unsigned índiceOrdinal=0;índiceOrdinal<sizeof(valorContenidoValor);índiceOrdinal++)if(valorContenidoValor[índiceOrdinal]!=leerValorTexto[índiceOrdinal])return 9;
    if(invocar(57,Documentación,0,0,0))return 10;
    long valorTiempo[2];if(invocar(113,1,(long)valorTiempo,0,0) || valorTiempo[1]<0 || valorTiempo[1]>=1000000000)return 11;
    if(!Salida("LINUX ARM64 ELF PASS\n") || !Salida(argumentos[1]) || !Salida("\n"))return 12;
    return 0;
}
