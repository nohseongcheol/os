/* A real Linux AArch64 static ELF example. No jkoros headers or ABI note. */
static long gọiThựcHiện(long sốHiệu, long toánHạngĐầuTiên, long toánHạngThứHai, long toánHạngThứBa, long toánHạngThứTư) {
    register long thanhGhiKhôngSố __asm__("x0")=toánHạngĐầuTiên, thanhGhiMột __asm__("x1")=toánHạngThứHai;
    register long thanhGhiHai __asm__("x2")=toánHạngThứBa, thanhGhiBa __asm__("x3")=toánHạngThứTư;
    register long thanhGhiTám __asm__("x8")=sốHiệu;
    __asm__ volatile("svc #0" : "+r"(thanhGhiKhôngSố) : "r"(thanhGhiMột),"r"(thanhGhiHai),"r"(thanhGhiBa),"r"(thanhGhiTám) : "memory","cc");
    return thanhGhiKhôngSố;
}
static int độDài(const char *vănBản) { int trịSố=0;while(vănBản[trịSố])trịSố++;return trịSố; }
static int ĐầuRa(const char *vănBản) { int trịSố=độDài(vănBản);return gọiThựcHiện(64,1,(long)vănBản,trịSố,0)==trịSố; }
int main(int sốLượngĐốiSố,char **cácĐốiSố) {
    if(sốLượngĐốiSố!=2 || !cácĐốiSố[0] || !cácĐốiSố[1] || cácĐốiSố[2])return 2;
    /* Linux syscall 6 is not jkoros's exit syscall. */
    long làKhôngHỗTrợ=gọiThựcHiện(6,99,0,0,0);
    if(làKhôngHỗTrợ!=-38 && làKhôngHỗTrợ!=-14)return 3; /* Linux: EFAULT; subset: ENOSYS */
    if(gọiThựcHiện(64,1,0x80000,1,0)!=-14)return 4;
    const char giáTrịNộiDung[]="LINUX ELF FILE IO\n";
    long TàiLiệu=gọiThựcHiện(56,-100,(long)"linux.txt",578,0600);
    if(TàiLiệu<0)return 5;
    if(gọiThựcHiện(64,TàiLiệu,(long)giáTrịNộiDung,sizeof(giáTrịNộiDung)-1,0)!=sizeof(giáTrịNộiDung)-1)return 6;
    if(gọiThựcHiện(62,TàiLiệu,0,0,0)!=0)return 7;
    char đọcGiáTrịVănBản[sizeof(giáTrịNộiDung)]={0};
    if(gọiThựcHiện(63,TàiLiệu,(long)đọcGiáTrịVănBản,sizeof(giáTrịNộiDung)-1,0)!=sizeof(giáTrịNộiDung)-1)return 8;
    for(unsigned chỉSốThứBậc=0;chỉSốThứBậc<sizeof(giáTrịNộiDung);chỉSốThứBậc++)if(giáTrịNộiDung[chỉSốThứBậc]!=đọcGiáTrịVănBản[chỉSốThứBậc])return 9;
    if(gọiThựcHiện(57,TàiLiệu,0,0,0))return 10;
    long giáTrịThờiGian[2];if(gọiThựcHiện(113,1,(long)giáTrịThờiGian,0,0) || giáTrịThờiGian[1]<0 || giáTrịThờiGian[1]>=1000000000)return 11;
    if(!ĐầuRa("LINUX ARM64 ELF PASS\n") || !ĐầuRa(cácĐốiSố[1]) || !ĐầuRa("\n"))return 12;
    return 0;
}
