#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paket_iş.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char veri[16384];static unsigned süre_değer,geçerli_konum;static int bilgi_teknolojisi_geçersiz;
static unsigned Etiketler_Liste[512],첫째값[512],SANİYE_değer[512],sabit_havuz,geçerli_Sınıf;
static char metin[65536];static unsigned Metin_boyutu;
typedef struct {unsigned Yapılandırma_BITS,İsim,tanımlayıcı_veri,명령열,Boyut,지역변수들,yığın_belleği;} metot_girdi;
static metot_girdi 메소드목록[64];static unsigned 메소드개수;
static unsigned alan_adı[64],Alan_tanımlayıcı[64],Alan_sabit[64],필드개수;
static unsigned AL_değer(unsigned öğe_BAĞ_DEĞ_SAY){if(geçerli_konum>süre_değer||öğe_BAĞ_DEĞ_SAY>süre_değer-geçerli_konum){bilgi_teknolojisi_geçersiz=1;return 0;}unsigned veri_konum=geçerli_konum;geçerli_konum+=öğe_BAĞ_DEĞ_SAY;return veri_konum;}
static unsigned bayt_veri(void){unsigned veri_konum=AL_değer(1);return bilgi_teknolojisi_geçersiz?0:veri[veri_konum];}
static unsigned 절반값(void){unsigned x_koordinatı=bayt_veri();return x_koordinatı<<8|bayt_veri();}
static uint32_t 가득참(void){uint32_t x_koordinatı=절반값();return x_koordinatı<<16|절반값();}
static int UNICODE_değer(unsigned 순번,const char*dize_veri){return 순번>0&&순번<sabit_havuz&&Etiketler_Liste[순번]==1&&strlen(dize_veri)==SANİYE_değer[순번]&&!memcmp(veri+첫째값[순번],dize_veri,SANİYE_değer[순번]);}
static int 같음(unsigned x_koordinatı,unsigned Y_koordinat){return x_koordinatı>0&&x_koordinatı<sabit_havuz&&Y_koordinat>0&&Y_koordinat<sabit_havuz&&Etiketler_Liste[x_koordinatı]==1&&Etiketler_Liste[Y_koordinat]==1&&SANİYE_değer[x_koordinatı]==SANİYE_değer[Y_koordinat]&&!memcmp(veri+첫째값[x_koordinatı],veri+첫째값[Y_koordinat],SANİYE_değer[x_koordinatı]);}
static void 내보내기(const char*Dosya_girdi,...){if(bilgi_teknolojisi_geçersiz)return;va_list bağımsız_değişken_DİZİ;va_start(bağımsız_değişken_DİZİ,Dosya_girdi);int öğe_BAĞ_DEĞ_SAY=vsnprintf(metin+Metin_boyutu,sizeof(metin)-Metin_boyutu,Dosya_girdi,bağımsız_değişken_DİZİ);va_end(bağımsız_değişken_DİZİ);if(öğe_BAĞ_DEĞ_SAY<0||(unsigned)öğe_BAĞ_DEĞ_SAY>=sizeof(metin)-Metin_boyutu){bilgi_teknolojisi_geçersiz=1;return;}Metin_boyutu+=öğe_BAĞ_DEĞ_SAY;}
static int tanımlayıcı_girdi(unsigned tanımlayıcı_değer,int*sonuç){
    if(tanımlayıcı_değer<1||tanımlayıcı_değer>=sabit_havuz||Etiketler_Liste[tanımlayıcı_değer]!=1)return -1;unsigned veri_konum=첫째값[tanımlayıcı_değer],Bitiş_Ofset=veri_konum+SANİYE_değer[tanımlayıcı_değer];if(veri_konum>=Bitiş_Ofset||veri[veri_konum++]!='(')return -1;int girdi_BAĞ_DEĞ_SAY=0;
    while(veri_konum<Bitiş_Ofset&&veri[veri_konum]!=')'){
        unsigned kod_noktası=veri[veri_konum++];while(kod_noktası=='['&&veri_konum<Bitiş_Ofset)kod_noktası=veri[veri_konum++];
        if(kod_noktası=='L'){while(veri_konum<Bitiş_Ofset&&veri[veri_konum]!=';')veri_konum++;if(veri_konum==Bitiş_Ofset)return -1;veri_konum++;}
        else if(kod_noktası!='I'&&kod_noktası!='Z'&&kod_noktası!='B'&&kod_noktası!='C'&&kod_noktası!='S')return -1;
        if(++girdi_BAĞ_DEĞ_SAY>16)return -1;
    }
    if(veri_konum+1>=Bitiş_Ofset||veri[veri_konum++]!=')')return -1;*sonuç=veri[veri_konum]=='V'?0:1;
    if(veri[veri_konum]=='J'||veri[veri_konum]=='D'||veri[veri_konum]=='F')return -1;return girdi_BAĞ_DEĞ_SAY;
}
static void özellikler(void){unsigned öğe_BAĞ_DEĞ_SAY=절반값();for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY&&!bilgi_teknolojisi_geçersiz;순번++){절반값();unsigned Boyut=가득참();AL_değer(Boyut);}}
static int ayrıştırmak_artış(void){
    if(가득참()!=0xcafebabe)return -1;unsigned ikincil_sürüm=절반값(),sürüm_numarası=절반값();if(ikincil_sürüm||sürüm_numarası<45||sürüm_numarası>52)return -1;
    sabit_havuz=절반값();if(sabit_havuz<1||sabit_havuz>512)return -1;
    for(unsigned 순번=1;순번<sabit_havuz&&!bilgi_teknolojisi_geçersiz;순번++){
        Etiketler_Liste[순번]=bayt_veri();switch(Etiketler_Liste[순번]){
        case 1:SANİYE_değer[순번]=절반값();첫째값[순번]=AL_değer(SANİYE_değer[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:AL_değer(8);if(++순번>=sabit_havuz)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SANİYE_değer[순번]=절반값();break;
        case 15:첫째값[순번]=bayt_veri();SANİYE_değer[순번]=절반값();break;default:return -1;
        }
    }
    절반값();geçerli_Sınıf=절반값();절반값();if(geçerli_Sınıf<1||geçerli_Sınıf>=sabit_havuz||Etiketler_Liste[geçerli_Sınıf]!=7||첫째값[geçerli_Sınıf]<1||첫째값[geçerli_Sınıf]>=sabit_havuz||Etiketler_Liste[첫째값[geçerli_Sınıf]]!=1)return -1;unsigned 인터페이스목록=절반값();AL_değer(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!bilgi_teknolojisi_geçersiz;순번++){
        unsigned Yapılandırma_BITS=절반값();alan_adı[순번]=절반값();Alan_tanımlayıcı[순번]=절반값();
        if(!(Yapılandırma_BITS&8))return -1;
        unsigned girdi_BAĞ_DEĞ_SAY=절반값();for(unsigned 안쪽순번=0;안쪽순번<girdi_BAĞ_DEĞ_SAY&&!bilgi_teknolojisi_geçersiz;안쪽순번++){
            unsigned İsim=절반값(),Boyut=가득참();
            if(UNICODE_değer(İsim,"ConstantValue")){if(Boyut!=2)return -1;Alan_sabit[순번]=절반값();}
            else AL_değer(Boyut);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!bilgi_teknolojisi_geçersiz;순번++){
        metot_girdi*Grup_boyutlandırmak=메소드목록+순번;Grup_boyutlandırmak->Yapılandırma_BITS=절반값();Grup_boyutlandırmak->İsim=절반값();Grup_boyutlandırmak->tanımlayıcı_veri=절반값();unsigned girdi_BAĞ_DEĞ_SAY=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<girdi_BAĞ_DEĞ_SAY&&!bilgi_teknolojisi_geçersiz;안쪽순번++){
            unsigned İsim=절반값(),Boyut=가득참(),çalıştır=geçerli_konum;
            if(Boyut>süre_değer-geçerli_konum)return -1;
            if(UNICODE_değer(İsim,"Code")){
                Grup_boyutlandırmak->yığın_belleği=절반값();Grup_boyutlandırmak->지역변수들=절반값();Grup_boyutlandırmak->Boyut=가득참();Grup_boyutlandırmak->명령열=AL_değer(Grup_boyutlandırmak->Boyut);
                if(Grup_boyutlandırmak->yığın_belleği>128||Grup_boyutlandırmak->지역변수들>128||Grup_boyutlandırmak->Boyut>8192||절반값())return -1;özellikler();
            }else AL_değer(Boyut);
            if(geçerli_konum!=çalıştır+Boyut)return -1;
        }
        if(!UNICODE_değer(Grup_boyutlandırmak->İsim,"<init>")&&(!(Grup_boyutlandırmak->Yapılandırma_BITS&8)||(Grup_boyutlandırmak->Yapılandırma_BITS&(0x100|0x20))||!Grup_boyutlandırmak->Boyut))return -1;
    }
    özellikler();return bilgi_teknolojisi_geçersiz||geçerli_konum!=süre_değer?-1:0;
}
static void sabit_değer(unsigned tanımlayıcı_değer){
    if(!tanımlayıcı_değer||tanımlayıcı_değer>=sabit_havuz){bilgi_teknolojisi_geçersiz=1;return;}
    if(Etiketler_Liste[tanımlayıcı_değer]==3)내보내기("P(%uU);",첫째값[tanımlayıcı_değer]);
    else if(Etiketler_Liste[tanımlayıcı_değer]==8)내보내기("P((W)k%u);",tanımlayıcı_değer);else bilgi_teknolojisi_geçersiz=1;
}
static void 호출(unsigned tanımlayıcı_değer,int sanal_Ara){
    if(tanımlayıcı_değer<1||tanımlayıcı_değer>=sabit_havuz||(Etiketler_Liste[tanımlayıcı_değer]!=10&&Etiketler_Liste[tanımlayıcı_değer]!=11)||첫째값[tanımlayıcı_değer]<1||첫째값[tanımlayıcı_değer]>=sabit_havuz||Etiketler_Liste[첫째값[tanımlayıcı_değer]]!=7||SANİYE_değer[tanımlayıcı_değer]<1||SANİYE_değer[tanımlayıcı_değer]>=sabit_havuz||Etiketler_Liste[SANİYE_değer[tanımlayıcı_değer]]!=12){bilgi_teknolojisi_geçersiz=1;return;}
    unsigned sahip_nesne=첫째값[첫째값[tanımlayıcı_değer]],İsim=첫째값[SANİYE_değer[tanımlayıcı_değer]],tanımlayıcı_veri=SANİYE_değer[SANİYE_değer[tanımlayıcı_değer]];int sonuç=0,öğe_BAĞ_DEĞ_SAY=tanımlayıcı_girdi(tanımlayıcı_veri,&sonuç);if(öğe_BAĞ_DEĞ_SAY<0){bilgi_teknolojisi_geçersiz=1;return;}
    for(int 순번=öğe_BAĞ_DEĞ_SAY;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(sanal_Ara)내보내기("Q();");
    if(!sanal_Ara&&같음(sahip_nesne,첫째값[geçerli_Sınıf])){
        unsigned Grup_boyutlandırmak=0;for(;Grup_boyutlandırmak<메소드개수;Grup_boyutlandırmak++)if(같음(İsim,메소드목록[Grup_boyutlandırmak].İsim)&&같음(tanımlayıcı_veri,메소드목록[Grup_boyutlandırmak].tanımlayıcı_veri))break;
        if(Grup_boyutlandırmak==메소드개수||!(메소드목록[Grup_boyutlandırmak].Yapılandırma_BITS&8)){bilgi_teknolojisi_geçersiz=1;return;}
        if(sonuç)내보내기("P(");내보내기("m%u(",Grup_boyutlandırmak);for(int 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(sonuç?"));":" );");return;
    }
    if((sanal_Ara&&UNICODE_değer(sahip_nesne,"java/io/PrintStream")&& (UNICODE_değer(İsim,"print")||UNICODE_değer(İsim,"println")))||(!sanal_Ara&&UNICODE_değer(sahip_nesne,"Türkçe/Öz/metinÇıktısı"))){
        if(UNICODE_değer(tanımlayıcı_veri,"(I)V")&&(UNICODE_değer(İsim,"print")||UNICODE_değer(İsim,"println")||UNICODE_değer(İsim,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_değer(İsim,"print")?0:1);return;}
        if(UNICODE_değer(tanımlayıcı_veri,"(Ljava/lang/String;)V")&&(UNICODE_değer(İsim,"print")||UNICODE_değer(İsim,"println")||UNICODE_değer(İsim,"Yazma")||UNICODE_değer(İsim,"yazma_hat"))){내보내기("jprint(x[0],0,%d);",UNICODE_değer(İsim,"print")||UNICODE_değer(İsim,"Yazma")?0:1);return;}
        if(UNICODE_değer(tanımlayıcı_veri,"()V")&&UNICODE_değer(İsim,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!sanal_Ara&&UNICODE_değer(sahip_nesne,"Türkçe/Öz/dosya")){
        if(UNICODE_değer(İsim,"Yazma")&&UNICODE_değer(tanımlayıcı_veri,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_değer(İsim,"Okuma")&&UNICODE_değer(tanımlayıcı_veri,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    bilgi_teknolojisi_geçersiz=1;
}
static void derlemek_metot(unsigned ARA_Dizin){
    metot_girdi*Grup_boyutlandırmak=메소드목록+ARA_Dizin;if(UNICODE_değer(Grup_boyutlandırmak->İsim,"<init>"))return;int sonuç,öğe_BAĞ_DEĞ_SAY=tanımlayıcı_girdi(Grup_boyutlandırmak->tanımlayıcı_veri,&sonuç);if(öğe_BAĞ_DEĞ_SAY<0){bilgi_teknolojisi_geçersiz=1;return;}
    내보내기("static W m%u(",ARA_Dizin);for(int 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!öğe_BAĞ_DEĞ_SAY)내보내기("void");
    if((unsigned)öğe_BAĞ_DEĞ_SAY>Grup_boyutlandırmak->지역변수들){bilgi_teknolojisi_geçersiz=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Grup_boyutlandırmak->지역변수들?Grup_boyutlandırmak->지역변수들:1);for(int 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=süre_değer;süre_değer=Grup_boyutlandırmak->명령열+Grup_boyutlandırmak->Boyut;geçerli_konum=Grup_boyutlandırmak->명령열;
    while(geçerli_konum<süre_değer&&!bilgi_teknolojisi_geçersiz){unsigned komut_konum=geçerli_konum-Grup_boyutlandırmak->명령열,işlem_değer_c96707fb=bayt_veri();내보내기("L%u:;",komut_konum);
        if(işlem_değer_c96707fb==0){}
        else if(işlem_değer_c96707fb==1)내보내기("P(0);");
        else if(işlem_değer_c96707fb>=2&&işlem_değer_c96707fb<=8)내보내기("P(%uU);",işlem_değer_c96707fb-3);
        else if(işlem_değer_c96707fb==16){int değer=(int8_t)bayt_veri();내보내기("P(%uU);",(unsigned)değer);}
        else if(işlem_değer_c96707fb==17){int değer=(int16_t)절반값();내보내기("P(%uU);",(unsigned)değer);}
        else if(işlem_değer_c96707fb==18||işlem_değer_c96707fb==19)sabit_değer(işlem_değer_c96707fb==18?bayt_veri():절반값());
        else if(işlem_değer_c96707fb==21||işlem_değer_c96707fb==25){unsigned 순번=bayt_veri();if(순번>=Grup_boyutlandırmak->지역변수들)bilgi_teknolojisi_geçersiz=1;내보내기("P(v[%u]);",순번);}
        else if((işlem_değer_c96707fb>=26&&işlem_değer_c96707fb<=29)||(işlem_değer_c96707fb>=42&&işlem_değer_c96707fb<=45)){unsigned 순번=işlem_değer_c96707fb>=42?işlem_değer_c96707fb-42:işlem_değer_c96707fb-26;if(순번>=Grup_boyutlandırmak->지역변수들)bilgi_teknolojisi_geçersiz=1;내보내기("P(v[%u]);",순번);}
        else if(işlem_değer_c96707fb==54||işlem_değer_c96707fb==58){unsigned 순번=bayt_veri();if(순번>=Grup_boyutlandırmak->지역변수들)bilgi_teknolojisi_geçersiz=1;내보내기("v[%u]=Q();",순번);}
        else if((işlem_değer_c96707fb>=59&&işlem_değer_c96707fb<=62)||(işlem_değer_c96707fb>=75&&işlem_değer_c96707fb<=78)){unsigned 순번=işlem_değer_c96707fb>=75?işlem_değer_c96707fb-75:işlem_değer_c96707fb-59;if(순번>=Grup_boyutlandırmak->지역변수들)bilgi_teknolojisi_geçersiz=1;내보내기("v[%u]=Q();",순번);}
        else if(işlem_değer_c96707fb==46||işlem_değer_c96707fb==50||işlem_değer_c96707fb==51||işlem_değer_c96707fb==52||işlem_değer_c96707fb==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(işlem_değer_c96707fb==79||işlem_değer_c96707fb==83||işlem_değer_c96707fb==84||işlem_değer_c96707fb==85||işlem_değer_c96707fb==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",işlem_değer_c96707fb==84?"(unsigned)(signed char)q":işlem_değer_c96707fb==85?"(unsigned short)q":işlem_değer_c96707fb==86?"(unsigned)(short)q":"q");
        else if(işlem_değer_c96707fb==87)내보내기("Q();");
        else if(işlem_değer_c96707fb==89)내보내기("q=Q();P(q);P(q);");
        else if(işlem_değer_c96707fb==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(işlem_değer_c96707fb==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(işlem_değer_c96707fb==96||işlem_değer_c96707fb==100||işlem_değer_c96707fb==104||işlem_değer_c96707fb==120||işlem_değer_c96707fb==124||işlem_değer_c96707fb==126||işlem_değer_c96707fb==128||işlem_değer_c96707fb==130){const char*kodlama_değer=işlem_değer_c96707fb==96?"+":işlem_değer_c96707fb==100?"-":işlem_değer_c96707fb==104?"*":işlem_değer_c96707fb==120?"<<":işlem_değer_c96707fb==124?">>":işlem_değer_c96707fb==126?"&":işlem_değer_c96707fb==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",kodlama_değer,işlem_değer_c96707fb==120||işlem_değer_c96707fb==124?"%32":"");}
        else if(işlem_değer_c96707fb==108||işlem_değer_c96707fb==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",işlem_değer_c96707fb==112);
        else if(işlem_değer_c96707fb==116)내보내기("P(0U-(unsigned)Q());");
        else if(işlem_değer_c96707fb==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(işlem_değer_c96707fb==132){unsigned 순번=bayt_veri();int 차이=(int8_t)bayt_veri();if(순번>=Grup_boyutlandırmak->지역변수들)bilgi_teknolojisi_geçersiz=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(işlem_değer_c96707fb>=145&&işlem_değer_c96707fb<=147)내보내기("P((unsigned)(%s)Q());",işlem_değer_c96707fb==145?"signed char":işlem_değer_c96707fb==146?"unsigned short":"short");
        else if(işlem_değer_c96707fb>=153&&işlem_değer_c96707fb<=166){int hedef=(int)komut_konum+(int16_t)절반값();const char*Karşılaştırma_değer[]={"==","!=","<",">=",">","<="};if(hedef<0||hedef>=(int)Grup_boyutlandırmak->Boyut){bilgi_teknolojisi_geçersiz=1;break;}if(işlem_değer_c96707fb<159)내보내기("if((int)Q()%s0)goto L%d;",Karşılaştırma_değer[işlem_değer_c96707fb-153],hedef);else if(işlem_değer_c96707fb<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Karşılaştırma_değer[işlem_değer_c96707fb-159],hedef);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",işlem_değer_c96707fb==165?"==":"!=",hedef);}
        else if(işlem_değer_c96707fb==167){int hedef=(int)komut_konum+(int16_t)절반값();if(hedef<0||hedef>=(int)Grup_boyutlandırmak->Boyut)bilgi_teknolojisi_geçersiz=1;내보내기("goto L%d;",hedef);}
        else if(işlem_değer_c96707fb==172||işlem_değer_c96707fb==176)내보내기("return Q();");else if(işlem_değer_c96707fb==177)내보내기("return 0;");
        else if(işlem_değer_c96707fb==178||işlem_değer_c96707fb==179){unsigned tanımlayıcı_değer=절반값();if(tanımlayıcı_değer<1||tanımlayıcı_değer>=sabit_havuz||Etiketler_Liste[tanımlayıcı_değer]!=9||첫째값[tanımlayıcı_değer]>=sabit_havuz||SANİYE_değer[tanımlayıcı_değer]>=sabit_havuz||Etiketler_Liste[첫째값[tanımlayıcı_değer]]!=7||Etiketler_Liste[SANİYE_değer[tanımlayıcı_değer]]!=12){bilgi_teknolojisi_geçersiz=1;break;}unsigned sahip_nesne=첫째값[첫째값[tanımlayıcı_değer]],İsim=첫째값[SANİYE_değer[tanımlayıcı_değer]],tanımlayıcı_veri=SANİYE_değer[SANİYE_değer[tanımlayıcı_değer]];
            if(işlem_değer_c96707fb==178&&UNICODE_değer(sahip_nesne,"java/lang/System")&&UNICODE_değer(İsim,"out")&&UNICODE_değer(tanımlayıcı_veri,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned Dosya_girdi=0;while(Dosya_girdi<필드개수&&(!같음(İsim,alan_adı[Dosya_girdi])||!같음(tanımlayıcı_veri,Alan_tanımlayıcı[Dosya_girdi])))Dosya_girdi++;if(!같음(sahip_nesne,첫째값[geçerli_Sınıf])||Dosya_girdi==필드개수){bilgi_teknolojisi_geçersiz=1;break;}내보내기(işlem_değer_c96707fb==178?"P(fields[%u]);":"fields[%u]=Q();",Dosya_girdi);}}
        else if(işlem_değer_c96707fb==182||işlem_değer_c96707fb==184)호출(절반값(),işlem_değer_c96707fb==182);
        else if(işlem_değer_c96707fb==188){unsigned TÜR_alan=bayt_veri();if(TÜR_alan!=4&&TÜR_alan!=5&&TÜR_alan!=8&&TÜR_alan!=9&&TÜR_alan!=10)bilgi_teknolojisi_geçersiz=1;내보내기("P(jarray((int)Q()));");}
        else if(işlem_değer_c96707fb==190)내보내기("P(jlength(Q()));");
        else if(işlem_değer_c96707fb==198||işlem_değer_c96707fb==199){int hedef=(int)komut_konum+(int16_t)절반값();if(hedef<0||hedef>=(int)Grup_boyutlandırmak->Boyut)bilgi_teknolojisi_geçersiz=1;내보내기("if(Q()%s0)goto L%d;",işlem_değer_c96707fb==198?"==":"!=",hedef);}
        else bilgi_teknolojisi_geçersiz=1;
        if(bilgi_teknolojisi_geçersiz)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",ARA_Dizin,işlem_değer_c96707fb,komut_konum);
        내보내기("\n");
    }
    süre_değer=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned dize_ders(unsigned *veri_konum,unsigned Bitiş_Ofset){
    if(*veri_konum>=Bitiş_Ofset){bilgi_teknolojisi_geçersiz=1;return 0;}unsigned kod_noktası=veri[(*veri_konum)++];
    if(kod_noktası<128)return kod_noktası;
    unsigned öğe_BAĞ_DEĞ_SAY=kod_noktası>=0xc0&&kod_noktası<=0xdf?1:kod_noktası>=0xe0&&kod_noktası<=0xef?2:3;
    if(öğe_BAĞ_DEĞ_SAY==3||öğe_BAĞ_DEĞ_SAY>Bitiş_Ofset-*veri_konum){bilgi_teknolojisi_geçersiz=1;return 0;}unsigned değer=kod_noktası&((1u<<(6-öğe_BAĞ_DEĞ_SAY))-1);
    for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++){unsigned Sonraki_öğe=veri[(*veri_konum)++];if((Sonraki_öğe&0xc0)!=0x80)bilgi_teknolojisi_geçersiz=1;değer=değer<<6|(Sonraki_öğe&63);}
    if((öğe_BAĞ_DEĞ_SAY==1&&değer<128&&değer!=0)||(öğe_BAĞ_DEĞ_SAY==2&&değer<2048))bilgi_teknolojisi_geçersiz=1;return değer;
}
static void dize_sabit(unsigned tanımlayıcı_değer){
    unsigned 부호없는값=첫째값[tanımlayıcı_değer];if(부호없는값<1||부호없는값>=sabit_havuz||Etiketler_Liste[부호없는값]!=1){bilgi_teknolojisi_geçersiz=1;return;}내보내기("static const unsigned char k%u[]={",tanımlayıcı_değer);
    unsigned veri_konum=첫째값[부호없는값],Bitiş_Ofset=veri_konum+SANİYE_değer[부호없는값];
    while(veri_konum<Bitiş_Ofset&&!bilgi_teknolojisi_geçersiz){unsigned kod_noktası=dize_ders(&veri_konum,Bitiş_Ofset);
        if(kod_noktası>=0xd800&&kod_noktası<=0xdbff){unsigned 낮은부분=dize_ders(&veri_konum,Bitiş_Ofset);if(낮은부분<0xdc00||낮은부분>0xdfff){bilgi_teknolojisi_geçersiz=1;break;}kod_noktası=0x10000+((kod_noktası-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kod_noktası>=0xdc00&&kod_noktası<=0xdfff){bilgi_teknolojisi_geçersiz=1;break;}
        if(!kod_noktası){printf("jaot: embedded NUL string needs JVM mode\n");bilgi_teknolojisi_geçersiz=1;break;}
        if(kod_noktası<128)내보내기("%u,",kod_noktası);
        else{unsigned öğe_BAĞ_DEĞ_SAY=kod_noktası<2048?2:kod_noktası<65536?3:4;내보내기("%u,",(öğe_BAĞ_DEĞ_SAY==2?0xc0:öğe_BAĞ_DEĞ_SAY==3?0xe0:0xf0)|(kod_noktası>>(6*(öğe_BAĞ_DEĞ_SAY-1))));for(unsigned 순번=öğe_BAĞ_DEĞ_SAY-1;순번;순번--)내보내기("%u,",0x80|((kod_noktası>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*İsim){
    size_t öğe_BAĞ_DEĞ_SAY=strlen(İsim);
    if(öğe_BAĞ_DEĞ_SAY>4&&!strcmp(İsim+öğe_BAĞ_DEĞ_SAY-4,".jar")){
        if(꾸러미열기(İsim)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char yol[256];const char*girdi_metot=꾸러미진입클래스();öğe_BAĞ_DEĞ_SAY=strlen(girdi_metot);if(öğe_BAĞ_DEĞ_SAY+6>=sizeof(yol))return 0;
        for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)yol[순번]=girdi_metot[순번]=='.'?'/':girdi_metot[순번];strcpy(yol+öğe_BAĞ_DEĞ_SAY,".class");int girdi_BAĞ_DEĞ_SAY=꾸러미읽기(yol,veri,sizeof(veri));if(girdi_BAĞ_DEĞ_SAY<0)return 0;süre_değer=girdi_BAĞ_DEĞ_SAY;
    }else{intptr_t dosya_tanıtıcısı=사용자호출(3,(uintptr_t)İsim,0,0,0,0,0);if(dosya_tanıtıcısı<0)return 0;intptr_t girdi_BAĞ_DEĞ_SAY=사용자호출(9,dosya_tanıtıcısı,0,0,0,0,0);if(girdi_BAĞ_DEĞ_SAY<0||girdi_BAĞ_DEĞ_SAY>sizeof(veri)){사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);return 0;}intptr_t GETİRİ_BAĞ_DEĞ_SAY=사용자호출(2,dosya_tanıtıcısı,(uintptr_t)veri,girdi_BAĞ_DEĞ_SAY,0,0,0);사용자호출(4,dosya_tanıtıcısı,0,0,0,0,0);if(GETİRİ_BAĞ_DEĞ_SAY!=girdi_BAĞ_DEĞ_SAY)return 0;süre_değer=girdi_BAĞ_DEĞ_SAY;}
    if(ayrıştırmak_artış()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<sabit_havuz&&!bilgi_teknolojisi_geçersiz;순번++)if(Etiketler_Liste[순번]==8)dize_sabit(순번);
    if(bilgi_teknolojisi_geçersiz)return 0;
    int giriş_noktası=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_değer(메소드목록[순번].İsim,"<init>")){
        int sonuç,girdi_BAĞ_DEĞ_SAY=tanımlayıcı_girdi(메소드목록[순번].tanımlayıcı_veri,&sonuç);if(girdi_BAĞ_DEĞ_SAY<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<girdi_BAĞ_DEĞ_SAY;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!girdi_BAĞ_DEĞ_SAY)내보내기("void");내보내기(");\n");
        if(UNICODE_değer(메소드목록[순번].İsim,"main")&&UNICODE_değer(메소드목록[순번].tanımlayıcı_veri,"([Ljava/lang/String;)V")&&(메소드목록[순번].Yapılandırma_BITS&9)==9)giriş_noktası=순번;
        if(UNICODE_değer(메소드목록[순번].İsim,"<clinit>"))초기값=순번;
    }
    if(giriş_noktası<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!bilgi_teknolojisi_geçersiz;순번++)derlemek_metot(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(Alan_sabit[순번]){
        unsigned kod_noktası=Alan_sabit[순번];if(kod_noktası>=sabit_havuz)return 0;
        if(Etiketler_Liste[kod_noktası]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kod_noktası]);else if(Etiketler_Liste[kod_noktası]==8)내보내기("fields[%u]=(W)k%u;",순번,kod_noktası);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",giriş_noktası);
    return bilgi_teknolojisi_geçersiz?0:metin;
}
