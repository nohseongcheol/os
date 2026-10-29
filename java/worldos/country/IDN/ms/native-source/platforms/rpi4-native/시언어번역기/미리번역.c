#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "pakej.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned kepanjangan_VALUE,현재위치;static int teknologi_maklumat_tak_sah;
static unsigned Tag_Senarai[512],첫째값[512],SECOND_VALUE[512],pemalar_himpunan,현재클래스;
static char Teks[65536];static unsigned Saiz_teks;
typedef struct {unsigned konfigurasi_Background_Intelligent_Transfer_Service,Nama,서술값,suruhan_jujukan,Saiz,지역변수들,ingatan_tindanan;} kaedah_pemasukan;
static kaedah_pemasukan 메소드목록[64];static unsigned 메소드개수;
static unsigned nama_medan_98daa19b[64],필드서술[64],medan_pemalar[64],필드개수;
static unsigned TAKE_VALUE(unsigned item_COUNT){if(현재위치>kepanjangan_VALUE||item_COUNT>kepanjangan_VALUE-현재위치){teknologi_maklumat_tak_sah=1;return 0;}unsigned data_jawatan=현재위치;현재위치+=item_COUNT;return data_jawatan;}
static unsigned bait_data(void){unsigned data_jawatan=TAKE_VALUE(1);return teknologi_maklumat_tak_sah?0:data[data_jawatan];}
static unsigned 절반값(void){unsigned koordinat_x=bait_data();return koordinat_x<<8|bait_data();}
static uint32_t 가득참(void){uint32_t koordinat_x=절반값();return koordinat_x<<16|절반값();}
static int Unikod_VALUE(unsigned 순번,const char*rentetan_data){return 순번>0&&순번<pemalar_himpunan&&Tag_Senarai[순번]==1&&strlen(rentetan_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],rentetan_data,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinat_x,unsigned Y_koordinat){return koordinat_x>0&&koordinat_x<pemalar_himpunan&&Y_koordinat>0&&Y_koordinat<pemalar_himpunan&&Tag_Senarai[koordinat_x]==1&&Tag_Senarai[Y_koordinat]==1&&SECOND_VALUE[koordinat_x]==SECOND_VALUE[Y_koordinat]&&!memcmp(data+첫째값[koordinat_x],data+첫째값[Y_koordinat],SECOND_VALUE[koordinat_x]);}
static void 내보내기(const char*fail_pemasukan,...){if(teknologi_maklumat_tak_sah)return;va_list argumen_ARRAY;va_start(argumen_ARRAY,fail_pemasukan);int item_COUNT=vsnprintf(Teks+Saiz_teks,sizeof(Teks)-Saiz_teks,fail_pemasukan,argumen_ARRAY);va_end(argumen_ARRAY);if(item_COUNT<0||(unsigned)item_COUNT>=sizeof(Teks)-Saiz_teks){teknologi_maklumat_tak_sah=1;return;}Saiz_teks+=item_COUNT;}
static int 서술자(unsigned 식별자,int*ukuran){
    if(식별자<1||식별자>=pemalar_himpunan||Tag_Senarai[식별자]!=1)return -1;unsigned data_jawatan=첫째값[식별자],tamat_Ofset=data_jawatan+SECOND_VALUE[식별자];if(data_jawatan>=tamat_Ofset||data[data_jawatan++]!='(')return -1;int pemasukan_COUNT=0;
    while(data_jawatan<tamat_Ofset&&data[data_jawatan]!=')'){
        unsigned titik_kod=data[data_jawatan++];while(titik_kod=='['&&data_jawatan<tamat_Ofset)titik_kod=data[data_jawatan++];
        if(titik_kod=='L'){while(data_jawatan<tamat_Ofset&&data[data_jawatan]!=';')data_jawatan++;if(data_jawatan==tamat_Ofset)return -1;data_jawatan++;}
        else if(titik_kod!='I'&&titik_kod!='Z'&&titik_kod!='B'&&titik_kod!='C'&&titik_kod!='S')return -1;
        if(++pemasukan_COUNT>16)return -1;
    }
    if(data_jawatan+1>=tamat_Ofset||data[data_jawatan++]!=')')return -1;*ukuran=data[data_jawatan]=='V'?0:1;
    if(data[data_jawatan]=='J'||data[data_jawatan]=='D'||data[data_jawatan]=='F')return -1;return pemasukan_COUNT;
}
static void atribut(void){unsigned item_COUNT=절반값();for(unsigned 순번=0;순번<item_COUNT&&!teknologi_maklumat_tak_sah;순번++){절반값();unsigned Saiz=가득참();TAKE_VALUE(Saiz);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned versi_minor=절반값(),nombor_versi=절반값();if(versi_minor||nombor_versi<45||nombor_versi>52)return -1;
    pemalar_himpunan=절반값();if(pemalar_himpunan<1||pemalar_himpunan>512)return -1;
    for(unsigned 순번=1;순번<pemalar_himpunan&&!teknologi_maklumat_tak_sah;순번++){
        Tag_Senarai[순번]=bait_data();switch(Tag_Senarai[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=pemalar_himpunan)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=bait_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();현재클래스=절반값();절반값();if(현재클래스<1||현재클래스>=pemalar_himpunan||Tag_Senarai[현재클래스]!=7||첫째값[현재클래스]<1||첫째값[현재클래스]>=pemalar_himpunan||Tag_Senarai[첫째값[현재클래스]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!teknologi_maklumat_tak_sah;순번++){
        unsigned konfigurasi_Background_Intelligent_Transfer_Service=절반값();nama_medan_98daa19b[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurasi_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned pemasukan_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<pemasukan_COUNT&&!teknologi_maklumat_tak_sah;안쪽순번++){
            unsigned Nama=절반값(),Saiz=가득참();
            if(Unikod_VALUE(Nama,"ConstantValue")){if(Saiz!=2)return -1;medan_pemalar[순번]=절반값();}
            else TAKE_VALUE(Saiz);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!teknologi_maklumat_tak_sah;순번++){
        kaedah_pemasukan*Kumpulan_saiz=메소드목록+순번;Kumpulan_saiz->konfigurasi_Background_Intelligent_Transfer_Service=절반값();Kumpulan_saiz->Nama=절반값();Kumpulan_saiz->서술값=절반값();unsigned pemasukan_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<pemasukan_COUNT&&!teknologi_maklumat_tak_sah;안쪽순번++){
            unsigned Nama=절반값(),Saiz=가득참(),Jalan=현재위치;
            if(Saiz>kepanjangan_VALUE-현재위치)return -1;
            if(Unikod_VALUE(Nama,"Code")){
                Kumpulan_saiz->ingatan_tindanan=절반값();Kumpulan_saiz->지역변수들=절반값();Kumpulan_saiz->Saiz=가득참();Kumpulan_saiz->suruhan_jujukan=TAKE_VALUE(Kumpulan_saiz->Saiz);
                if(Kumpulan_saiz->ingatan_tindanan>128||Kumpulan_saiz->지역변수들>128||Kumpulan_saiz->Saiz>8192||절반값())return -1;atribut();
            }else TAKE_VALUE(Saiz);
            if(현재위치!=Jalan+Saiz)return -1;
        }
        if(!Unikod_VALUE(Kumpulan_saiz->Nama,"<init>")&&(!(Kumpulan_saiz->konfigurasi_Background_Intelligent_Transfer_Service&8)||(Kumpulan_saiz->konfigurasi_Background_Intelligent_Transfer_Service&(0x100|0x20))||!Kumpulan_saiz->Saiz))return -1;
    }
    atribut();return teknologi_maklumat_tak_sah||현재위치!=kepanjangan_VALUE?-1:0;
}
static void pemalar_VALUE(unsigned 식별자){
    if(!식별자||식별자>=pemalar_himpunan){teknologi_maklumat_tak_sah=1;return;}
    if(Tag_Senarai[식별자]==3)내보내기("P(%uU);",첫째값[식별자]);
    else if(Tag_Senarai[식별자]==8)내보내기("P((W)k%u);",식별자);else teknologi_maklumat_tak_sah=1;
}
static void 호출(unsigned 식별자,int maya_CALL){
    if(식별자<1||식별자>=pemalar_himpunan||(Tag_Senarai[식별자]!=10&&Tag_Senarai[식별자]!=11)||첫째값[식별자]<1||첫째값[식별자]>=pemalar_himpunan||Tag_Senarai[첫째값[식별자]]!=7||SECOND_VALUE[식별자]<1||SECOND_VALUE[식별자]>=pemalar_himpunan||Tag_Senarai[SECOND_VALUE[식별자]]!=12){teknologi_maklumat_tak_sah=1;return;}
    unsigned pemilik_objek=첫째값[첫째값[식별자]],Nama=첫째값[SECOND_VALUE[식별자]],서술값=SECOND_VALUE[SECOND_VALUE[식별자]];int ukuran=0,item_COUNT=서술자(서술값,&ukuran);if(item_COUNT<0){teknologi_maklumat_tak_sah=1;return;}
    for(int 순번=item_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(maya_CALL)내보내기("Q();");
    if(!maya_CALL&&같음(pemilik_objek,첫째값[현재클래스])){
        unsigned Kumpulan_saiz=0;for(;Kumpulan_saiz<메소드개수;Kumpulan_saiz++)if(같음(Nama,메소드목록[Kumpulan_saiz].Nama)&&같음(서술값,메소드목록[Kumpulan_saiz].서술값))break;
        if(Kumpulan_saiz==메소드개수||!(메소드목록[Kumpulan_saiz].konfigurasi_Background_Intelligent_Transfer_Service&8)){teknologi_maklumat_tak_sah=1;return;}
        if(ukuran)내보내기("P(");내보내기("m%u(",Kumpulan_saiz);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(ukuran?"));":" );");return;
    }
    if((maya_CALL&&Unikod_VALUE(pemilik_objek,"java/io/PrintStream")&& (Unikod_VALUE(Nama,"print")||Unikod_VALUE(Nama,"println")))||(!maya_CALL&&Unikod_VALUE(pemilik_objek,"Melayu/Asli/출력"))){
        if(Unikod_VALUE(서술값,"(I)V")&&(Unikod_VALUE(Nama,"print")||Unikod_VALUE(Nama,"println")||Unikod_VALUE(Nama,"수쓰기"))){내보내기("jprint(x[0],1,%d);",Unikod_VALUE(Nama,"print")?0:1);return;}
        if(Unikod_VALUE(서술값,"(Ljava/lang/String;)V")&&(Unikod_VALUE(Nama,"print")||Unikod_VALUE(Nama,"println")||Unikod_VALUE(Nama,"Tulis")||Unikod_VALUE(Nama,"tulis_baris"))){내보내기("jprint(x[0],0,%d);",Unikod_VALUE(Nama,"print")||Unikod_VALUE(Nama,"Tulis")?0:1);return;}
        if(Unikod_VALUE(서술값,"()V")&&Unikod_VALUE(Nama,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!maya_CALL&&Unikod_VALUE(pemilik_objek,"Melayu/Asli/Fail")){
        if(Unikod_VALUE(Nama,"Tulis")&&Unikod_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(Unikod_VALUE(Nama,"Baca")&&Unikod_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    teknologi_maklumat_tak_sah=1;
}
static void bina_kaedah(unsigned Carian_INDEX){
    kaedah_pemasukan*Kumpulan_saiz=메소드목록+Carian_INDEX;if(Unikod_VALUE(Kumpulan_saiz->Nama,"<init>"))return;int ukuran,item_COUNT=서술자(Kumpulan_saiz->서술값,&ukuran);if(item_COUNT<0){teknologi_maklumat_tak_sah=1;return;}
    내보내기("static W m%u(",Carian_INDEX);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_COUNT)내보내기("void");
    if((unsigned)item_COUNT>Kumpulan_saiz->지역변수들){teknologi_maklumat_tak_sah=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",Kumpulan_saiz->지역변수들?Kumpulan_saiz->지역변수들:1);for(int 순번=0;순번<item_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=kepanjangan_VALUE;kepanjangan_VALUE=Kumpulan_saiz->suruhan_jujukan+Kumpulan_saiz->Saiz;현재위치=Kumpulan_saiz->suruhan_jujukan;
    while(현재위치<kepanjangan_VALUE&&!teknologi_maklumat_tak_sah){unsigned perintah_jawatan=현재위치-Kumpulan_saiz->suruhan_jujukan,operasi_VALUE=bait_data();내보내기("L%u:;",perintah_jawatan);
        if(operasi_VALUE==0){}
        else if(operasi_VALUE==1)내보내기("P(0);");
        else if(operasi_VALUE>=2&&operasi_VALUE<=8)내보내기("P(%uU);",operasi_VALUE-3);
        else if(operasi_VALUE==16){int VALUE=(int8_t)bait_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasi_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(operasi_VALUE==18||operasi_VALUE==19)pemalar_VALUE(operasi_VALUE==18?bait_data():절반값());
        else if(operasi_VALUE==21||operasi_VALUE==25){unsigned 순번=bait_data();if(순번>=Kumpulan_saiz->지역변수들)teknologi_maklumat_tak_sah=1;내보내기("P(v[%u]);",순번);}
        else if((operasi_VALUE>=26&&operasi_VALUE<=29)||(operasi_VALUE>=42&&operasi_VALUE<=45)){unsigned 순번=operasi_VALUE>=42?operasi_VALUE-42:operasi_VALUE-26;if(순번>=Kumpulan_saiz->지역변수들)teknologi_maklumat_tak_sah=1;내보내기("P(v[%u]);",순번);}
        else if(operasi_VALUE==54||operasi_VALUE==58){unsigned 순번=bait_data();if(순번>=Kumpulan_saiz->지역변수들)teknologi_maklumat_tak_sah=1;내보내기("v[%u]=Q();",순번);}
        else if((operasi_VALUE>=59&&operasi_VALUE<=62)||(operasi_VALUE>=75&&operasi_VALUE<=78)){unsigned 순번=operasi_VALUE>=75?operasi_VALUE-75:operasi_VALUE-59;if(순번>=Kumpulan_saiz->지역변수들)teknologi_maklumat_tak_sah=1;내보내기("v[%u]=Q();",순번);}
        else if(operasi_VALUE==46||operasi_VALUE==50||operasi_VALUE==51||operasi_VALUE==52||operasi_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operasi_VALUE==79||operasi_VALUE==83||operasi_VALUE==84||operasi_VALUE==85||operasi_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operasi_VALUE==84?"(unsigned)(signed char)q":operasi_VALUE==85?"(unsigned short)q":operasi_VALUE==86?"(unsigned)(short)q":"q");
        else if(operasi_VALUE==87)내보내기("Q();");
        else if(operasi_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(operasi_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operasi_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(operasi_VALUE==96||operasi_VALUE==100||operasi_VALUE==104||operasi_VALUE==120||operasi_VALUE==124||operasi_VALUE==126||operasi_VALUE==128||operasi_VALUE==130){const char*pengekodan_VALUE=operasi_VALUE==96?"+":operasi_VALUE==100?"-":operasi_VALUE==104?"*":operasi_VALUE==120?"<<":operasi_VALUE==124?">>":operasi_VALUE==126?"&":operasi_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",pengekodan_VALUE,operasi_VALUE==120||operasi_VALUE==124?"%32":"");}
        else if(operasi_VALUE==108||operasi_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operasi_VALUE==112);
        else if(operasi_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(operasi_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operasi_VALUE==132){unsigned 순번=bait_data();int 차이=(int8_t)bait_data();if(순번>=Kumpulan_saiz->지역변수들)teknologi_maklumat_tak_sah=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(operasi_VALUE>=145&&operasi_VALUE<=147)내보내기("P((unsigned)(%s)Q());",operasi_VALUE==145?"signed char":operasi_VALUE==146?"unsigned short":"short");
        else if(operasi_VALUE>=153&&operasi_VALUE<=166){int sasaran=(int)perintah_jawatan+(int16_t)절반값();const char*Perbandingan_VALUE[]={"==","!=","<",">=",">","<="};if(sasaran<0||sasaran>=(int)Kumpulan_saiz->Saiz){teknologi_maklumat_tak_sah=1;break;}if(operasi_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Perbandingan_VALUE[operasi_VALUE-153],sasaran);else if(operasi_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Perbandingan_VALUE[operasi_VALUE-159],sasaran);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",operasi_VALUE==165?"==":"!=",sasaran);}
        else if(operasi_VALUE==167){int sasaran=(int)perintah_jawatan+(int16_t)절반값();if(sasaran<0||sasaran>=(int)Kumpulan_saiz->Saiz)teknologi_maklumat_tak_sah=1;내보내기("goto L%d;",sasaran);}
        else if(operasi_VALUE==172||operasi_VALUE==176)내보내기("return Q();");else if(operasi_VALUE==177)내보내기("return 0;");
        else if(operasi_VALUE==178||operasi_VALUE==179){unsigned 식별자=절반값();if(식별자<1||식별자>=pemalar_himpunan||Tag_Senarai[식별자]!=9||첫째값[식별자]>=pemalar_himpunan||SECOND_VALUE[식별자]>=pemalar_himpunan||Tag_Senarai[첫째값[식별자]]!=7||Tag_Senarai[SECOND_VALUE[식별자]]!=12){teknologi_maklumat_tak_sah=1;break;}unsigned pemilik_objek=첫째값[첫째값[식별자]],Nama=첫째값[SECOND_VALUE[식별자]],서술값=SECOND_VALUE[SECOND_VALUE[식별자]];
            if(operasi_VALUE==178&&Unikod_VALUE(pemilik_objek,"java/lang/System")&&Unikod_VALUE(Nama,"out")&&Unikod_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned fail_pemasukan=0;while(fail_pemasukan<필드개수&&(!같음(Nama,nama_medan_98daa19b[fail_pemasukan])||!같음(서술값,필드서술[fail_pemasukan])))fail_pemasukan++;if(!같음(pemilik_objek,첫째값[현재클래스])||fail_pemasukan==필드개수){teknologi_maklumat_tak_sah=1;break;}내보내기(operasi_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",fail_pemasukan);}}
        else if(operasi_VALUE==182||operasi_VALUE==184)호출(절반값(),operasi_VALUE==182);
        else if(operasi_VALUE==188){unsigned TYPE_bidang=bait_data();if(TYPE_bidang!=4&&TYPE_bidang!=5&&TYPE_bidang!=8&&TYPE_bidang!=9&&TYPE_bidang!=10)teknologi_maklumat_tak_sah=1;내보내기("P(jarray((int)Q()));");}
        else if(operasi_VALUE==190)내보내기("P(jlength(Q()));");
        else if(operasi_VALUE==198||operasi_VALUE==199){int sasaran=(int)perintah_jawatan+(int16_t)절반값();if(sasaran<0||sasaran>=(int)Kumpulan_saiz->Saiz)teknologi_maklumat_tak_sah=1;내보내기("if(Q()%s0)goto L%d;",operasi_VALUE==198?"==":"!=",sasaran);}
        else teknologi_maklumat_tak_sah=1;
        if(teknologi_maklumat_tak_sah)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",Carian_INDEX,operasi_VALUE,perintah_jawatan);
        내보내기("\n");
    }
    kepanjangan_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned rentetan_unit(unsigned *data_jawatan,unsigned tamat_Ofset){
    if(*data_jawatan>=tamat_Ofset){teknologi_maklumat_tak_sah=1;return 0;}unsigned titik_kod=data[(*data_jawatan)++];
    if(titik_kod<128)return titik_kod;
    unsigned item_COUNT=titik_kod>=0xc0&&titik_kod<=0xdf?1:titik_kod>=0xe0&&titik_kod<=0xef?2:3;
    if(item_COUNT==3||item_COUNT>tamat_Ofset-*data_jawatan){teknologi_maklumat_tak_sah=1;return 0;}unsigned VALUE=titik_kod&((1u<<(6-item_COUNT))-1);
    for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned Seterusnya_item=data[(*data_jawatan)++];if((Seterusnya_item&0xc0)!=0x80)teknologi_maklumat_tak_sah=1;VALUE=VALUE<<6|(Seterusnya_item&63);}
    if((item_COUNT==1&&VALUE<128&&VALUE!=0)||(item_COUNT==2&&VALUE<2048))teknologi_maklumat_tak_sah=1;return VALUE;
}
static void rentetan_pemalar(unsigned 식별자){
    unsigned 부호없는값=첫째값[식별자];if(부호없는값<1||부호없는값>=pemalar_himpunan||Tag_Senarai[부호없는값]!=1){teknologi_maklumat_tak_sah=1;return;}내보내기("static const unsigned char k%u[]={",식별자);
    unsigned data_jawatan=첫째값[부호없는값],tamat_Ofset=data_jawatan+SECOND_VALUE[부호없는값];
    while(data_jawatan<tamat_Ofset&&!teknologi_maklumat_tak_sah){unsigned titik_kod=rentetan_unit(&data_jawatan,tamat_Ofset);
        if(titik_kod>=0xd800&&titik_kod<=0xdbff){unsigned 낮은부분=rentetan_unit(&data_jawatan,tamat_Ofset);if(낮은부분<0xdc00||낮은부분>0xdfff){teknologi_maklumat_tak_sah=1;break;}titik_kod=0x10000+((titik_kod-0xd800)<<10)+낮은부분-0xdc00;}
        else if(titik_kod>=0xdc00&&titik_kod<=0xdfff){teknologi_maklumat_tak_sah=1;break;}
        if(!titik_kod){printf("jaot: embedded NUL string needs JVM mode\n");teknologi_maklumat_tak_sah=1;break;}
        if(titik_kod<128)내보내기("%u,",titik_kod);
        else{unsigned item_COUNT=titik_kod<2048?2:titik_kod<65536?3:4;내보내기("%u,",(item_COUNT==2?0xc0:item_COUNT==3?0xe0:0xf0)|(titik_kod>>(6*(item_COUNT-1))));for(unsigned 순번=item_COUNT-1;순번;순번--)내보내기("%u,",0x80|((titik_kod>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nama){
    size_t item_COUNT=strlen(Nama);
    if(item_COUNT>4&&!strcmp(Nama+item_COUNT-4,".jar")){
        if(꾸러미열기(Nama)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char LALUAN[256];const char*pemasukan_kaedah=꾸러미진입클래스();item_COUNT=strlen(pemasukan_kaedah);if(item_COUNT+6>=sizeof(LALUAN))return 0;
        for(unsigned 순번=0;순번<item_COUNT;순번++)LALUAN[순번]=pemasukan_kaedah[순번]=='.'?'/':pemasukan_kaedah[순번];strcpy(LALUAN+item_COUNT,".class");int pemasukan_COUNT=꾸러미읽기(LALUAN,data,sizeof(data));if(pemasukan_COUNT<0)return 0;kepanjangan_VALUE=pemasukan_COUNT;
    }else{intptr_t fail_pemegang=사용자호출(3,(uintptr_t)Nama,0,0,0,0,0);if(fail_pemegang<0)return 0;intptr_t pemasukan_COUNT=사용자호출(9,fail_pemegang,0,0,0,0,0);if(pemasukan_COUNT<0||pemasukan_COUNT>sizeof(data)){사용자호출(4,fail_pemegang,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,fail_pemegang,(uintptr_t)data,pemasukan_COUNT,0,0,0);사용자호출(4,fail_pemegang,0,0,0,0,0);if(RECEIVED_COUNT!=pemasukan_COUNT)return 0;kepanjangan_VALUE=pemasukan_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<pemalar_himpunan&&!teknologi_maklumat_tak_sah;순번++)if(Tag_Senarai[순번]==8)rentetan_pemalar(순번);
    if(teknologi_maklumat_tak_sah)return 0;
    int titik_permulaan=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!Unikod_VALUE(메소드목록[순번].Nama,"<init>")){
        int ukuran,pemasukan_COUNT=서술자(메소드목록[순번].서술값,&ukuran);if(pemasukan_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<pemasukan_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!pemasukan_COUNT)내보내기("void");내보내기(");\n");
        if(Unikod_VALUE(메소드목록[순번].Nama,"main")&&Unikod_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurasi_Background_Intelligent_Transfer_Service&9)==9)titik_permulaan=순번;
        if(Unikod_VALUE(메소드목록[순번].Nama,"<clinit>"))초기값=순번;
    }
    if(titik_permulaan<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!teknologi_maklumat_tak_sah;순번++)bina_kaedah(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(medan_pemalar[순번]){
        unsigned titik_kod=medan_pemalar[순번];if(titik_kod>=pemalar_himpunan)return 0;
        if(Tag_Senarai[titik_kod]==3)내보내기("fields[%u]=%uU;",순번,첫째값[titik_kod]);else if(Tag_Senarai[titik_kod]==8)내보내기("fields[%u]=(W)k%u;",순번,titik_kod);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",titik_permulaan);
    return teknologi_maklumat_tak_sah?0:Teks;
}
