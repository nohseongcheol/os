/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long 呼出(long 番号, long 先頭位置被演算子, long 第二被演算子, long 第三被演算子, long 第四被演算子) {
    register long 零レジスタ __asm__("x0")=先頭位置被演算子, 一レジスタ __asm__("x1")=第二被演算子;
    register long 二レジスタ __asm__("x2")=第三被演算子, 三レジスタ __asm__("x3")=第四被演算子;
    register long 八レジスタ __asm__("x8")=番号;
    __asm__ volatile("svc #0" : "+r"(零レジスタ) : "r"(一レジスタ),"r"(二レジスタ),"r"(三レジスタ),"r"(八レジスタ) : "memory","cc");
    return 零レジスタ;
}
static int 長さ(const char *文) { int 数=0;while(文[数])数++;return 数; }
static int 出力(const char *文) { int 数=長さ(文);return 呼出(64,1,(long)文,数,0)==数; }
int main(int 引数個数,char **引数) {
    if(引数個数!=2 || !引数[0] || !引数[1] || 引数[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long 判定未対応=呼出(6,99,0,0,0);
    if(判定未対応!=-38 && 判定未対応!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(呼出(64,1,0x80000,1,0)!=-14)return 4;
    const char 内容物値[]="LINUX ELF FILE IO\n";
    long 文書=呼出(56,-100,(long)"linux.txt",578,0600);
    if(文書<0)return 5;
    if(呼出(64,文書,(long)内容物値,sizeof(内容物値)-1,0)!=sizeof(内容物値)-1)return 6;
    if(呼出(62,文書,0,0,0)!=0)return 7;
    char 本文値読取[sizeof(内容物値)]={0};
    if(呼出(63,文書,(long)本文値読取,sizeof(内容物値)-1,0)!=sizeof(内容物値)-1)return 8;
    for(unsigned 序数添字=0;序数添字<sizeof(内容物値);序数添字++)if(内容物値[序数添字]!=本文値読取[序数添字])return 9;
    if(呼出(57,文書,0,0,0))return 10;
    long 時間値[2];if(呼出(113,1,(long)時間値,0,0) || 時間値[1]<0 || 時間値[1]>=1000000000)return 11;
    if(!出力("LINUX ARM64 ELF PASS\n") || !出力(引数[1]) || !出力("\n"))return 12;
    return 0;
}
