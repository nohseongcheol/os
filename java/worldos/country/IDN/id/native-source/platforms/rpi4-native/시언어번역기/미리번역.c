#include "../명명/기계연결이름.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "호출.h"
#include "paket.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned panjang_VALUE,saat_ini_posisi;static int teknologi_informasi_tidak_sahih;
static unsigned Label_Daftar[512],첫째값[512],SECOND_VALUE[512],konstanta_kumpulan,saat_ini_Kelas;
static char teks[65536];static unsigned Ukuran_teks;
typedef struct {unsigned konfigurasi_Background_Intelligent_Transfer_Service,Nama_2,서술값,instruksi_urutan,Ukuran,지역변수들,memori_tumpukan;} metode_entri;
static metode_entri 메소드목록[64];static unsigned 메소드개수;
static unsigned nama_bidang_isian[64],필드서술[64],bidang_konstanta[64],필드개수;
static unsigned TAKE_VALUE(unsigned item_COUNT){if(saat_ini_posisi>panjang_VALUE||item_COUNT>panjang_VALUE-saat_ini_posisi){teknologi_informasi_tidak_sahih=1;return 0;}unsigned data_posisi=saat_ini_posisi;saat_ini_posisi+=item_COUNT;return data_posisi;}
static unsigned byte_data(void){unsigned data_posisi=TAKE_VALUE(1);return teknologi_informasi_tidak_sahih?0:data[data_posisi];}
static unsigned 절반값(void){unsigned koordinat_x=byte_data();return koordinat_x<<8|byte_data();}
static uint32_t 가득참(void){uint32_t koordinat_x=절반값();return koordinat_x<<16|절반값();}
static int UNICODE_VALUE(unsigned 순번,const char*string_data){return 순번>0&&순번<konstanta_kumpulan&&Label_Daftar[순번]==1&&strlen(string_data)==SECOND_VALUE[순번]&&!memcmp(data+첫째값[순번],string_data,SECOND_VALUE[순번]);}
static int 같음(unsigned koordinat_x,unsigned Y_koordinat){return koordinat_x>0&&koordinat_x<konstanta_kumpulan&&Y_koordinat>0&&Y_koordinat<konstanta_kumpulan&&Label_Daftar[koordinat_x]==1&&Label_Daftar[Y_koordinat]==1&&SECOND_VALUE[koordinat_x]==SECOND_VALUE[Y_koordinat]&&!memcmp(data+첫째값[koordinat_x],data+첫째값[Y_koordinat],SECOND_VALUE[koordinat_x]);}
static void 내보내기(const char*file_entri,...){if(teknologi_informasi_tidak_sahih)return;va_list argumen_ARRAY;va_start(argumen_ARRAY,file_entri);int item_COUNT=vsnprintf(teks+Ukuran_teks,sizeof(teks)-Ukuran_teks,file_entri,argumen_ARRAY);va_end(argumen_ARRAY);if(item_COUNT<0||(unsigned)item_COUNT>=sizeof(teks)-Ukuran_teks){teknologi_informasi_tidak_sahih=1;return;}Ukuran_teks+=item_COUNT;}
static int 서술자(unsigned pengidentifikasi_VALUE,int*hasil){
    if(pengidentifikasi_VALUE<1||pengidentifikasi_VALUE>=konstanta_kumpulan||Label_Daftar[pengidentifikasi_VALUE]!=1)return -1;unsigned data_posisi=첫째값[pengidentifikasi_VALUE],mengakhiri_OFFSET=data_posisi+SECOND_VALUE[pengidentifikasi_VALUE];if(data_posisi>=mengakhiri_OFFSET||data[data_posisi++]!='(')return -1;int entri_COUNT=0;
    while(data_posisi<mengakhiri_OFFSET&&data[data_posisi]!=')'){
        unsigned kode_karakter=data[data_posisi++];while(kode_karakter=='['&&data_posisi<mengakhiri_OFFSET)kode_karakter=data[data_posisi++];
        if(kode_karakter=='L'){while(data_posisi<mengakhiri_OFFSET&&data[data_posisi]!=';')data_posisi++;if(data_posisi==mengakhiri_OFFSET)return -1;data_posisi++;}
        else if(kode_karakter!='I'&&kode_karakter!='Z'&&kode_karakter!='B'&&kode_karakter!='C'&&kode_karakter!='S')return -1;
        if(++entri_COUNT>16)return -1;
    }
    if(data_posisi+1>=mengakhiri_OFFSET||data[data_posisi++]!=')')return -1;*hasil=data[data_posisi]=='V'?0:1;
    if(data[data_posisi]=='J'||data[data_posisi]=='D'||data[data_posisi]=='F')return -1;return entri_COUNT;
}
static void atribut(void){unsigned item_COUNT=절반값();for(unsigned 순번=0;순번<item_COUNT&&!teknologi_informasi_tidak_sahih;순번++){절반값();unsigned Ukuran=가득참();TAKE_VALUE(Ukuran);}}
static int 해석하기(void){
    if(가득참()!=0xcafebabe)return -1;unsigned versi_minor=절반값(),nomor_versi=절반값();if(versi_minor||nomor_versi<45||nomor_versi>52)return -1;
    konstanta_kumpulan=절반값();if(konstanta_kumpulan<1||konstanta_kumpulan>512)return -1;
    for(unsigned 순번=1;순번<konstanta_kumpulan&&!teknologi_informasi_tidak_sahih;순번++){
        Label_Daftar[순번]=byte_data();switch(Label_Daftar[순번]){
        case 1:SECOND_VALUE[순번]=절반값();첫째값[순번]=TAKE_VALUE(SECOND_VALUE[순번]);break;case 3:case 4:첫째값[순번]=가득참();break;
        case 5:case 6:TAKE_VALUE(8);if(++순번>=konstanta_kumpulan)return -1;break;
        case 7:case 8:case 16:첫째값[순번]=절반값();break;
        case 9:case 10:case 11:case 12:case 18:첫째값[순번]=절반값();SECOND_VALUE[순번]=절반값();break;
        case 15:첫째값[순번]=byte_data();SECOND_VALUE[순번]=절반값();break;default:return -1;
        }
    }
    절반값();saat_ini_Kelas=절반값();절반값();if(saat_ini_Kelas<1||saat_ini_Kelas>=konstanta_kumpulan||Label_Daftar[saat_ini_Kelas]!=7||첫째값[saat_ini_Kelas]<1||첫째값[saat_ini_Kelas]>=konstanta_kumpulan||Label_Daftar[첫째값[saat_ini_Kelas]]!=1)return -1;unsigned 인터페이스목록=절반값();TAKE_VALUE(인터페이스목록*2);
    필드개수=절반값();if(필드개수>64)return -1;
    for(unsigned 순번=0;순번<필드개수&&!teknologi_informasi_tidak_sahih;순번++){
        unsigned konfigurasi_Background_Intelligent_Transfer_Service=절반값();nama_bidang_isian[순번]=절반값();필드서술[순번]=절반값();
        if(!(konfigurasi_Background_Intelligent_Transfer_Service&8))return -1;
        unsigned entri_COUNT=절반값();for(unsigned 안쪽순번=0;안쪽순번<entri_COUNT&&!teknologi_informasi_tidak_sahih;안쪽순번++){
            unsigned Nama_2=절반값(),Ukuran=가득참();
            if(UNICODE_VALUE(Nama_2,"ConstantValue")){if(Ukuran!=2)return -1;bidang_konstanta[순번]=절반값();}
            else TAKE_VALUE(Ukuran);
        }
    }
    메소드개수=절반값();if(메소드개수>64)return -1;
    for(unsigned 순번=0;순번<메소드개수&&!teknologi_informasi_tidak_sahih;순번++){
        metode_entri*grup_ukuran=메소드목록+순번;grup_ukuran->konfigurasi_Background_Intelligent_Transfer_Service=절반값();grup_ukuran->Nama_2=절반값();grup_ukuran->서술값=절반값();unsigned entri_COUNT=절반값();
        for(unsigned 안쪽순번=0;안쪽순번<entri_COUNT&&!teknologi_informasi_tidak_sahih;안쪽순번++){
            unsigned Nama_2=절반값(),Ukuran=가득참(),jalankan=saat_ini_posisi;
            if(Ukuran>panjang_VALUE-saat_ini_posisi)return -1;
            if(UNICODE_VALUE(Nama_2,"Code")){
                grup_ukuran->memori_tumpukan=절반값();grup_ukuran->지역변수들=절반값();grup_ukuran->Ukuran=가득참();grup_ukuran->instruksi_urutan=TAKE_VALUE(grup_ukuran->Ukuran);
                if(grup_ukuran->memori_tumpukan>128||grup_ukuran->지역변수들>128||grup_ukuran->Ukuran>8192||절반값())return -1;atribut();
            }else TAKE_VALUE(Ukuran);
            if(saat_ini_posisi!=jalankan+Ukuran)return -1;
        }
        if(!UNICODE_VALUE(grup_ukuran->Nama_2,"<init>")&&(!(grup_ukuran->konfigurasi_Background_Intelligent_Transfer_Service&8)||(grup_ukuran->konfigurasi_Background_Intelligent_Transfer_Service&(0x100|0x20))||!grup_ukuran->Ukuran))return -1;
    }
    atribut();return teknologi_informasi_tidak_sahih||saat_ini_posisi!=panjang_VALUE?-1:0;
}
static void konstanta_VALUE(unsigned pengidentifikasi_VALUE){
    if(!pengidentifikasi_VALUE||pengidentifikasi_VALUE>=konstanta_kumpulan){teknologi_informasi_tidak_sahih=1;return;}
    if(Label_Daftar[pengidentifikasi_VALUE]==3)내보내기("P(%uU);",첫째값[pengidentifikasi_VALUE]);
    else if(Label_Daftar[pengidentifikasi_VALUE]==8)내보내기("P((W)k%u);",pengidentifikasi_VALUE);else teknologi_informasi_tidak_sahih=1;
}
static void 호출(unsigned pengidentifikasi_VALUE,int maya_CALL){
    if(pengidentifikasi_VALUE<1||pengidentifikasi_VALUE>=konstanta_kumpulan||(Label_Daftar[pengidentifikasi_VALUE]!=10&&Label_Daftar[pengidentifikasi_VALUE]!=11)||첫째값[pengidentifikasi_VALUE]<1||첫째값[pengidentifikasi_VALUE]>=konstanta_kumpulan||Label_Daftar[첫째값[pengidentifikasi_VALUE]]!=7||SECOND_VALUE[pengidentifikasi_VALUE]<1||SECOND_VALUE[pengidentifikasi_VALUE]>=konstanta_kumpulan||Label_Daftar[SECOND_VALUE[pengidentifikasi_VALUE]]!=12){teknologi_informasi_tidak_sahih=1;return;}
    unsigned pemilik_objek=첫째값[첫째값[pengidentifikasi_VALUE]],Nama_2=첫째값[SECOND_VALUE[pengidentifikasi_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[pengidentifikasi_VALUE]];int hasil=0,item_COUNT=서술자(서술값,&hasil);if(item_COUNT<0){teknologi_informasi_tidak_sahih=1;return;}
    for(int 순번=item_COUNT;순번>0;순번--)내보내기("x[%d]=Q();",순번-1);if(maya_CALL)내보내기("Q();");
    if(!maya_CALL&&같음(pemilik_objek,첫째값[saat_ini_Kelas])){
        unsigned grup_ukuran=0;for(;grup_ukuran<메소드개수;grup_ukuran++)if(같음(Nama_2,메소드목록[grup_ukuran].Nama_2)&&같음(서술값,메소드목록[grup_ukuran].서술값))break;
        if(grup_ukuran==메소드개수||!(메소드목록[grup_ukuran].konfigurasi_Background_Intelligent_Transfer_Service&8)){teknologi_informasi_tidak_sahih=1;return;}
        if(hasil)내보내기("P(");내보내기("m%u(",grup_ukuran);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",x[%d]":"x[%d]",순번);내보내기(hasil?"));":" );");return;
    }
    if((maya_CALL&&UNICODE_VALUE(pemilik_objek,"java/io/PrintStream")&& (UNICODE_VALUE(Nama_2,"print")||UNICODE_VALUE(Nama_2,"println")))||(!maya_CALL&&UNICODE_VALUE(pemilik_objek,"Indonesia/Asli/keluaranTeks"))){
        if(UNICODE_VALUE(서술값,"(I)V")&&(UNICODE_VALUE(Nama_2,"print")||UNICODE_VALUE(Nama_2,"println")||UNICODE_VALUE(Nama_2,"수쓰기"))){내보내기("jprint(x[0],1,%d);",UNICODE_VALUE(Nama_2,"print")?0:1);return;}
        if(UNICODE_VALUE(서술값,"(Ljava/lang/String;)V")&&(UNICODE_VALUE(Nama_2,"print")||UNICODE_VALUE(Nama_2,"println")||UNICODE_VALUE(Nama_2,"Tulis")||UNICODE_VALUE(Nama_2,"tulis_baris"))){내보내기("jprint(x[0],0,%d);",UNICODE_VALUE(Nama_2,"print")||UNICODE_VALUE(Nama_2,"Tulis")?0:1);return;}
        if(UNICODE_VALUE(서술값,"()V")&&UNICODE_VALUE(Nama_2,"println")){내보내기("jprint((W)\"\",0,1);");return;}
    }
    if(!maya_CALL&&UNICODE_VALUE(pemilik_objek,"Indonesia/Asli/berkas")){
        if(UNICODE_VALUE(Nama_2,"Tulis")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;Ljava/lang/String;)V")){내보내기("jfwrite(x[0],x[1]);");return;}
        if(UNICODE_VALUE(Nama_2,"Baca")&&UNICODE_VALUE(서술값,"(Ljava/lang/String;)Ljava/lang/String;")){내보내기("P(jfread(x[0]));");return;}
    }
    teknologi_informasi_tidak_sahih=1;
}
static void bangun_metode(unsigned LOOKUP_INDEX){
    metode_entri*grup_ukuran=메소드목록+LOOKUP_INDEX;if(UNICODE_VALUE(grup_ukuran->Nama_2,"<init>"))return;int hasil,item_COUNT=서술자(grup_ukuran->서술값,&hasil);if(item_COUNT<0){teknologi_informasi_tidak_sahih=1;return;}
    내보내기("static W m%u(",LOOKUP_INDEX);for(int 순번=0;순번<item_COUNT;순번++)내보내기(순번?",W a%d":"W a%d",순번);if(!item_COUNT)내보내기("void");
    if((unsigned)item_COUNT>grup_ukuran->지역변수들){teknologi_informasi_tidak_sahih=1;return;}
    내보내기("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",grup_ukuran->지역변수들?grup_ukuran->지역변수들:1);for(int 순번=0;순번<item_COUNT;순번++)내보내기("v[%d]=a%d;",순번,순번);
    unsigned 저장값=panjang_VALUE;panjang_VALUE=grup_ukuran->instruksi_urutan+grup_ukuran->Ukuran;saat_ini_posisi=grup_ukuran->instruksi_urutan;
    while(saat_ini_posisi<panjang_VALUE&&!teknologi_informasi_tidak_sahih){unsigned perintah_posisi=saat_ini_posisi-grup_ukuran->instruksi_urutan,bedah_VALUE=byte_data();내보내기("L%u:;",perintah_posisi);
        if(bedah_VALUE==0){}
        else if(bedah_VALUE==1)내보내기("P(0);");
        else if(bedah_VALUE>=2&&bedah_VALUE<=8)내보내기("P(%uU);",bedah_VALUE-3);
        else if(bedah_VALUE==16){int VALUE=(int8_t)byte_data();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(bedah_VALUE==17){int VALUE=(int16_t)절반값();내보내기("P(%uU);",(unsigned)VALUE);}
        else if(bedah_VALUE==18||bedah_VALUE==19)konstanta_VALUE(bedah_VALUE==18?byte_data():절반값());
        else if(bedah_VALUE==21||bedah_VALUE==25){unsigned 순번=byte_data();if(순번>=grup_ukuran->지역변수들)teknologi_informasi_tidak_sahih=1;내보내기("P(v[%u]);",순번);}
        else if((bedah_VALUE>=26&&bedah_VALUE<=29)||(bedah_VALUE>=42&&bedah_VALUE<=45)){unsigned 순번=bedah_VALUE>=42?bedah_VALUE-42:bedah_VALUE-26;if(순번>=grup_ukuran->지역변수들)teknologi_informasi_tidak_sahih=1;내보내기("P(v[%u]);",순번);}
        else if(bedah_VALUE==54||bedah_VALUE==58){unsigned 순번=byte_data();if(순번>=grup_ukuran->지역변수들)teknologi_informasi_tidak_sahih=1;내보내기("v[%u]=Q();",순번);}
        else if((bedah_VALUE>=59&&bedah_VALUE<=62)||(bedah_VALUE>=75&&bedah_VALUE<=78)){unsigned 순번=bedah_VALUE>=75?bedah_VALUE-75:bedah_VALUE-59;if(순번>=grup_ukuran->지역변수들)teknologi_informasi_tidak_sahih=1;내보내기("v[%u]=Q();",순번);}
        else if(bedah_VALUE==46||bedah_VALUE==50||bedah_VALUE==51||bedah_VALUE==52||bedah_VALUE==53)내보내기("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(bedah_VALUE==79||bedah_VALUE==83||bedah_VALUE==84||bedah_VALUE==85||bedah_VALUE==86)내보내기("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",bedah_VALUE==84?"(unsigned)(signed char)q":bedah_VALUE==85?"(unsigned short)q":bedah_VALUE==86?"(unsigned)(short)q":"q");
        else if(bedah_VALUE==87)내보내기("Q();");
        else if(bedah_VALUE==89)내보내기("q=Q();P(q);P(q);");
        else if(bedah_VALUE==90)내보내기("q=Q();r=Q();P(q);P(r);P(q);");
        else if(bedah_VALUE==95)내보내기("q=Q();r=Q();P(q);P(r);");
        else if(bedah_VALUE==96||bedah_VALUE==100||bedah_VALUE==104||bedah_VALUE==120||bedah_VALUE==124||bedah_VALUE==126||bedah_VALUE==128||bedah_VALUE==130){const char*pengodean_VALUE=bedah_VALUE==96?"+":bedah_VALUE==100?"-":bedah_VALUE==104?"*":bedah_VALUE==120?"<<":bedah_VALUE==124?">>":bedah_VALUE==126?"&":bedah_VALUE==128?"|":"^";내보내기("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",pengodean_VALUE,bedah_VALUE==120||bedah_VALUE==124?"%32":"");}
        else if(bedah_VALUE==108||bedah_VALUE==112)내보내기("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",bedah_VALUE==112);
        else if(bedah_VALUE==116)내보내기("P(0U-(unsigned)Q());");
        else if(bedah_VALUE==122)내보내기("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(bedah_VALUE==132){unsigned 순번=byte_data();int 차이=(int8_t)byte_data();if(순번>=grup_ukuran->지역변수들)teknologi_informasi_tidak_sahih=1;내보내기("v[%u]=(unsigned)v[%u]+%uU;",순번,순번,(unsigned)차이);}
        else if(bedah_VALUE>=145&&bedah_VALUE<=147)내보내기("P((unsigned)(%s)Q());",bedah_VALUE==145?"signed char":bedah_VALUE==146?"unsigned short":"short");
        else if(bedah_VALUE>=153&&bedah_VALUE<=166){int target=(int)perintah_posisi+(int16_t)절반값();const char*Perbandingan_VALUE[]={"==","!=","<",">=",">","<="};if(target<0||target>=(int)grup_ukuran->Ukuran){teknologi_informasi_tidak_sahih=1;break;}if(bedah_VALUE<159)내보내기("if((int)Q()%s0)goto L%d;",Perbandingan_VALUE[bedah_VALUE-153],target);else if(bedah_VALUE<165)내보내기("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",Perbandingan_VALUE[bedah_VALUE-159],target);else 내보내기("q=Q();r=Q();if(r%sq)goto L%d;",bedah_VALUE==165?"==":"!=",target);}
        else if(bedah_VALUE==167){int target=(int)perintah_posisi+(int16_t)절반값();if(target<0||target>=(int)grup_ukuran->Ukuran)teknologi_informasi_tidak_sahih=1;내보내기("goto L%d;",target);}
        else if(bedah_VALUE==172||bedah_VALUE==176)내보내기("return Q();");else if(bedah_VALUE==177)내보내기("return 0;");
        else if(bedah_VALUE==178||bedah_VALUE==179){unsigned pengidentifikasi_VALUE=절반값();if(pengidentifikasi_VALUE<1||pengidentifikasi_VALUE>=konstanta_kumpulan||Label_Daftar[pengidentifikasi_VALUE]!=9||첫째값[pengidentifikasi_VALUE]>=konstanta_kumpulan||SECOND_VALUE[pengidentifikasi_VALUE]>=konstanta_kumpulan||Label_Daftar[첫째값[pengidentifikasi_VALUE]]!=7||Label_Daftar[SECOND_VALUE[pengidentifikasi_VALUE]]!=12){teknologi_informasi_tidak_sahih=1;break;}unsigned pemilik_objek=첫째값[첫째값[pengidentifikasi_VALUE]],Nama_2=첫째값[SECOND_VALUE[pengidentifikasi_VALUE]],서술값=SECOND_VALUE[SECOND_VALUE[pengidentifikasi_VALUE]];
            if(bedah_VALUE==178&&UNICODE_VALUE(pemilik_objek,"java/lang/System")&&UNICODE_VALUE(Nama_2,"out")&&UNICODE_VALUE(서술값,"Ljava/io/PrintStream;"))내보내기("P(1);");
            else {unsigned file_entri=0;while(file_entri<필드개수&&(!같음(Nama_2,nama_bidang_isian[file_entri])||!같음(서술값,필드서술[file_entri])))file_entri++;if(!같음(pemilik_objek,첫째값[saat_ini_Kelas])||file_entri==필드개수){teknologi_informasi_tidak_sahih=1;break;}내보내기(bedah_VALUE==178?"P(fields[%u]);":"fields[%u]=Q();",file_entri);}}
        else if(bedah_VALUE==182||bedah_VALUE==184)호출(절반값(),bedah_VALUE==182);
        else if(bedah_VALUE==188){unsigned TYPE_area=byte_data();if(TYPE_area!=4&&TYPE_area!=5&&TYPE_area!=8&&TYPE_area!=9&&TYPE_area!=10)teknologi_informasi_tidak_sahih=1;내보내기("P(jarray((int)Q()));");}
        else if(bedah_VALUE==190)내보내기("P(jlength(Q()));");
        else if(bedah_VALUE==198||bedah_VALUE==199){int target=(int)perintah_posisi+(int16_t)절반값();if(target<0||target>=(int)grup_ukuran->Ukuran)teknologi_informasi_tidak_sahih=1;내보내기("if(Q()%s0)goto L%d;",bedah_VALUE==198?"==":"!=",target);}
        else teknologi_informasi_tidak_sahih=1;
        if(teknologi_informasi_tidak_sahih)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",LOOKUP_INDEX,bedah_VALUE,perintah_posisi);
        내보내기("\n");
    }
    panjang_VALUE=저장값;내보내기("jfail();return 0;}\n");
}
static unsigned string_unit(unsigned *data_posisi,unsigned mengakhiri_OFFSET){
    if(*data_posisi>=mengakhiri_OFFSET){teknologi_informasi_tidak_sahih=1;return 0;}unsigned kode_karakter=data[(*data_posisi)++];
    if(kode_karakter<128)return kode_karakter;
    unsigned item_COUNT=kode_karakter>=0xc0&&kode_karakter<=0xdf?1:kode_karakter>=0xe0&&kode_karakter<=0xef?2:3;
    if(item_COUNT==3||item_COUNT>mengakhiri_OFFSET-*data_posisi){teknologi_informasi_tidak_sahih=1;return 0;}unsigned VALUE=kode_karakter&((1u<<(6-item_COUNT))-1);
    for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned Berikutnya_item=data[(*data_posisi)++];if((Berikutnya_item&0xc0)!=0x80)teknologi_informasi_tidak_sahih=1;VALUE=VALUE<<6|(Berikutnya_item&63);}
    if((item_COUNT==1&&VALUE<128&&VALUE!=0)||(item_COUNT==2&&VALUE<2048))teknologi_informasi_tidak_sahih=1;return VALUE;
}
static void string_konstanta(unsigned pengidentifikasi_VALUE){
    unsigned 부호없는값=첫째값[pengidentifikasi_VALUE];if(부호없는값<1||부호없는값>=konstanta_kumpulan||Label_Daftar[부호없는값]!=1){teknologi_informasi_tidak_sahih=1;return;}내보내기("static const unsigned char k%u[]={",pengidentifikasi_VALUE);
    unsigned data_posisi=첫째값[부호없는값],mengakhiri_OFFSET=data_posisi+SECOND_VALUE[부호없는값];
    while(data_posisi<mengakhiri_OFFSET&&!teknologi_informasi_tidak_sahih){unsigned kode_karakter=string_unit(&data_posisi,mengakhiri_OFFSET);
        if(kode_karakter>=0xd800&&kode_karakter<=0xdbff){unsigned 낮은부분=string_unit(&data_posisi,mengakhiri_OFFSET);if(낮은부분<0xdc00||낮은부분>0xdfff){teknologi_informasi_tidak_sahih=1;break;}kode_karakter=0x10000+((kode_karakter-0xd800)<<10)+낮은부분-0xdc00;}
        else if(kode_karakter>=0xdc00&&kode_karakter<=0xdfff){teknologi_informasi_tidak_sahih=1;break;}
        if(!kode_karakter){printf("jaot: embedded NUL string needs JVM mode\n");teknologi_informasi_tidak_sahih=1;break;}
        if(kode_karakter<128)내보내기("%u,",kode_karakter);
        else{unsigned item_COUNT=kode_karakter<2048?2:kode_karakter<65536?3:4;내보내기("%u,",(item_COUNT==2?0xc0:item_COUNT==3?0xe0:0xf0)|(kode_karakter>>(6*(item_COUNT-1))));for(unsigned 순번=item_COUNT-1;순번;순번--)내보내기("%u,",0x80|((kode_karakter>>(6*(순번-1)))&63));}
    }내보내기("0};\n");
}
const char *자바미리번역원문(const char*Nama_2){
    size_t item_COUNT=strlen(Nama_2);
    if(item_COUNT>4&&!strcmp(Nama_2+item_COUNT-4,".jar")){
        if(꾸러미열기(Nama_2)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char jalur[256];const char*entri_metode=꾸러미진입클래스();item_COUNT=strlen(entri_metode);if(item_COUNT+6>=sizeof(jalur))return 0;
        for(unsigned 순번=0;순번<item_COUNT;순번++)jalur[순번]=entri_metode[순번]=='.'?'/':entri_metode[순번];strcpy(jalur+item_COUNT,".class");int entri_COUNT=꾸러미읽기(jalur,data,sizeof(data));if(entri_COUNT<0)return 0;panjang_VALUE=entri_COUNT;
    }else{intptr_t file_handel=사용자호출(3,(uintptr_t)Nama_2,0,0,0,0,0);if(file_handel<0)return 0;intptr_t entri_COUNT=사용자호출(9,file_handel,0,0,0,0,0);if(entri_COUNT<0||entri_COUNT>sizeof(data)){사용자호출(4,file_handel,0,0,0,0,0);return 0;}intptr_t RECEIVED_COUNT=사용자호출(2,file_handel,(uintptr_t)data,entri_COUNT,0,0,0);사용자호출(4,file_handel,0,0,0,0,0);if(RECEIVED_COUNT!=entri_COUNT)return 0;panjang_VALUE=entri_COUNT;}
    if(해석하기()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    내보내기("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned 순번=1;순번<konstanta_kumpulan&&!teknologi_informasi_tidak_sahih;순번++)if(Label_Daftar[순번]==8)string_konstanta(순번);
    if(teknologi_informasi_tidak_sahih)return 0;
    int entri_p=-1,초기값=-1;
    for(unsigned 순번=0;순번<메소드개수;순번++)if(!UNICODE_VALUE(메소드목록[순번].Nama_2,"<init>")){
        int hasil,entri_COUNT=서술자(메소드목록[순번].서술값,&hasil);if(entri_COUNT<0)return 0;내보내기("static W m%u(",순번);for(int 안쪽순번=0;안쪽순번<entri_COUNT;안쪽순번++)내보내기(안쪽순번?",W":"W");if(!entri_COUNT)내보내기("void");내보내기(");\n");
        if(UNICODE_VALUE(메소드목록[순번].Nama_2,"main")&&UNICODE_VALUE(메소드목록[순번].서술값,"([Ljava/lang/String;)V")&&(메소드목록[순번].konfigurasi_Background_Intelligent_Transfer_Service&9)==9)entri_p=순번;
        if(UNICODE_VALUE(메소드목록[순번].Nama_2,"<clinit>"))초기값=순번;
    }
    if(entri_p<0)return 0;for(unsigned 순번=0;순번<메소드개수&&!teknologi_informasi_tidak_sahih;순번++)bangun_metode(순번);
    내보내기("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned 순번=0;순번<필드개수;순번++)if(bidang_konstanta[순번]){
        unsigned kode_karakter=bidang_konstanta[순번];if(kode_karakter>=konstanta_kumpulan)return 0;
        if(Label_Daftar[kode_karakter]==3)내보내기("fields[%u]=%uU;",순번,첫째값[kode_karakter]);else if(Label_Daftar[kode_karakter]==8)내보내기("fields[%u]=(W)k%u;",순번,kode_karakter);else return 0;
    }
    if(초기값>=0)내보내기("m%d();",초기값);내보내기("m%d((W)a);return 0;}\n",entri_p);
    return teknologi_informasi_tidak_sahih?0:teks;
}
