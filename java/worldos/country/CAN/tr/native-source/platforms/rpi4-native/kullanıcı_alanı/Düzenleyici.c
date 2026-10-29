/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "Dosya_ABI.h"
#define Düzenleyici_kapasite 16384
static unsigned char metin[Düzenleyici_kapasite],geri_alma_veri[Düzenleyici_kapasite],복사자료[Düzenleyici_kapasite],KR_veri[1024];
static int süre_değer,Dizin_değer,맨위,왼쪽,변경됨,Ekle,geri_alma_süre,위쪽,geri_alma_Değişiklikler,되돌림있음,örnek_süre,사용량,SÜTUNSAY=68,SATIR_BAĞ_DEĞ_SAY=19;
static char Dosya_girdi_ad[64],komut[128],BUL_girdi[128];
static const char *uyarı_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Beklemede_tuş;
static int yardım_alan,Durum_RESİM,Durum_sıra;
static void boşaltmak(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_veri,사용량,0,0,0);사용량=0;}}
static void bayt_veri(unsigned kod_noktası){if(Durum_RESİM){if((kod_noktası&192)!=128){Durum_sıra+=kod_noktası>=196?2:1;}if(Durum_sıra>=SÜTUNSAY)return;}if(사용량==(int)sizeof(KR_veri))boşaltmak();KR_veri[사용량++]=kod_noktası;}
static void 글내보내기(const char *dize_veri){while(*dize_veri)bayt_veri((unsigned char)*dize_veri++);}
static void 수치(unsigned öğe_BAĞ_DEĞ_SAY){char SANİYE_değer[12];int 순번=0;do{SANİYE_değer[순번++]='0'+öğe_BAĞ_DEĞ_SAY%10;öğe_BAĞ_DEĞ_SAY/=10;}while(öğe_BAĞ_DEĞ_SAY);while(순번)bayt_veri(SANİYE_değer[--순번]);}
static void taşımak_değer_83b651b8(int SATIR_konum,int SÜTUN_konum){글내보내기("\033[");수치(SATIR_konum);bayt_veri(';');수치(SÜTUN_konum);bayt_veri('H');}
static int Önceki(int veri_konum){if(veri_konum){veri_konum--;while(veri_konum>0&&(metin[veri_konum]&192)==128)veri_konum--;}return veri_konum;}
static int Sonraki_öğe(int veri_konum){if(veri_konum<süre_değer){veri_konum++;while(veri_konum<süre_değer&&(metin[veri_konum]&192)==128)veri_konum++;}return veri_konum;}
static int çalıştır(int veri_konum){while(veri_konum>0&&metin[veri_konum-1]!='\n')veri_konum--;return veri_konum;}
static int Bitiş_Ofset(int veri_konum){while(veri_konum<süre_değer&&metin[veri_konum]!='\n')veri_konum++;return veri_konum;}
static int 너비(unsigned kod_noktası){return kod_noktası>=196?2:1;}
static int SÜTUN(int veri_konum){int kod_noktası=0;for(int 순번=çalıştır(veri_konum);순번<veri_konum;순번=Sonraki_öğe(순번))kod_noktası+=metin[순번]=='\t'?4-kod_noktası%4:너비(metin[순번]);return kod_noktası;}
static void denetim_noktası(void){for(int 순번=0;순번<süre_değer;순번++)geri_alma_veri[순번]=metin[순번];geri_alma_süre=süre_değer;위쪽=Dizin_değer;geri_alma_Değişiklikler=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){denetim_noktası();for(int 순번=도착위치;순번<süre_değer;순번++)metin[출발위치+순번-도착위치]=metin[순번];süre_değer-=도착위치-출발위치;Dizin_değer=출발위치;변경됨=1;}
static int Ekleme_değer(const unsigned char *dize_veri,int öğe_BAĞ_DEĞ_SAY){if(öğe_BAĞ_DEĞ_SAY>Düzenleyici_kapasite-süre_değer){uyarı_SMS="File full (16384 bytes)";return 0;}denetim_noktası();for(int 순번=süre_değer-1;순번>=Dizin_değer;순번--)metin[순번+öğe_BAĞ_DEĞ_SAY]=metin[순번];for(int 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)metin[Dizin_değer+순번]=dize_veri[순번];süre_değer+=öğe_BAĞ_DEĞ_SAY;Dizin_değer+=öğe_BAĞ_DEĞ_SAY;변경됨=1;return 1;}
static void Dikey(int 차이){int SÜTUN_konum=SÜTUN(Dizin_değer),veri_konum=çalıştır(Dizin_değer);if(차이<0){if(!veri_konum)return;veri_konum=çalıştır(veri_konum-1);}else{veri_konum=Bitiş_Ofset(veri_konum);if(veri_konum==süre_değer)return;veri_konum++;}int kod_noktası=0;while(veri_konum<süre_değer&&metin[veri_konum]!='\n'&&kod_noktası<SÜTUN_konum){kod_noktası+=metin[veri_konum]=='\t'?4-kod_noktası%4:너비(metin[veri_konum]);veri_konum=Sonraki_öğe(veri_konum);}Dizin_değer=veri_konum;}
static void 화면그리기(void){
    if(Dizin_değer>süre_değer)Dizin_değer=süre_değer;if(맨위>Dizin_değer)맨위=çalıştır(Dizin_değer);맨위=çalıştır(맨위);
    int SATIR_konum=0;for(int 순번=맨위;순번<Dizin_değer;순번++)if(metin[순번]=='\n')SATIR_konum++;
    while(SATIR_konum>=SATIR_BAĞ_DEĞ_SAY-1){맨위=Bitiş_Ofset(맨위);if(맨위<süre_değer)맨위++;SATIR_konum--;}
    int SÜTUN_konum=SÜTUN(Dizin_değer);if(SÜTUN_konum<왼쪽)왼쪽=SÜTUN_konum;if(SÜTUN_konum-왼쪽>=SÜTUNSAY-1)왼쪽=SÜTUN_konum-SÜTUNSAY+2;
    글내보내기("\033[?25l");int veri_konum=맨위;
    for(int 반환값=0;반환값<SATIR_BAĞ_DEĞ_SAY-1;반환값++){
        taşımak_değer_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int kod_noktası=0,그려진상태=0;
        if(veri_konum>=süre_değer&&반환값>SATIR_konum){글내보내기("\033[90m~\033[0m");continue;}
        while(veri_konum<süre_değer&&metin[veri_konum]!='\n'){
            int Sonraki_Ofset=Sonraki_öğe(veri_konum),너비값=metin[veri_konum]=='\t'?4-kod_noktası%4:너비(metin[veri_konum]);
            if(kod_noktası>=왼쪽&&kod_noktası-왼쪽+너비값<SÜTUNSAY){
                if(metin[veri_konum]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bayt_veri(' ');}else if(metin[veri_konum]<32||metin[veri_konum]==127){bayt_veri('?');}else for(int 안쪽순번=veri_konum;안쪽순번<Sonraki_Ofset;안쪽순번++)bayt_veri(metin[안쪽순번]);그려진상태+=너비값;
            }kod_noktası+=너비값;veri_konum=Sonraki_Ofset;
        }
        (void)그려진상태;if(veri_konum<süre_değer)veri_konum++;
    }
    taşımak_değer_83b651b8(SATIR_BAĞ_DEĞ_SAY,1);글내보내기("\033[7m\033[2K");Durum_RESİM=1;Durum_sıra=0;글내보내기(Ekle?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Dosya_girdi_ad[이름바이트수]&&이름바이트수<30)bayt_veri(Dosya_girdi_ad[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int girdi_satırı=1;for(int 순번=0;순번<Dizin_değer;순번++)if(metin[순번]=='\n')girdi_satırı++;수치(girdi_satırı);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(uyarı_SMS){int öğe_BAĞ_DEĞ_SAY=0;글내보내기(" | ");while(uyarı_SMS[öğe_BAĞ_DEĞ_SAY]&&öğe_BAĞ_DEĞ_SAY<20)bayt_veri(uyarı_SMS[öğe_BAĞ_DEĞ_SAY++]);}
    Durum_RESİM=0;글내보내기("\033[0m");taşımak_değer_83b651b8(SATIR_konum+1,SÜTUN_konum-왼쪽+1);글내보내기("\033[?25h");boşaltmak();
}
static int 누름값(void){
    if(Beklemede_tuş){int 셋째순번=Beklemede_tuş;Beklemede_tuş=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Boyut=사용자호출(16,3,0,0,0,0,0);
        if(SÜTUNSAY!=(int)(Boyut&65535)||SATIR_BAĞ_DEĞ_SAY!=(int)(Boyut>>16)){
            SÜTUNSAY=Boyut&65535;SATIR_BAĞ_DEĞ_SAY=Boyut>>16;화면그리기();
            if(yardım_alan){taşımak_değer_83b651b8(SATIR_BAĞ_DEĞ_SAY,1);글내보내기("\033[0m\033[2K");bayt_veri(yardım_alan);글내보내기(komut);boşaltmak();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned geçerli_konum=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-geçerli_konum<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Beklemede_tuş=셋째순번;return 27;}
    int öğe_BAĞ_DEĞ_SAY=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){öğe_BAĞ_DEĞ_SAY=öğe_BAĞ_DEĞ_SAY*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return öğe_BAĞ_DEĞ_SAY==3?1007:öğe_BAĞ_DEĞ_SAY==5?1008:öğe_BAĞ_DEĞ_SAY==6?1009:öğe_BAĞ_DEĞ_SAY==1?1005:öğe_BAĞ_DEĞ_SAY==4?1006:27;return 27;}return 27;
}
static int depo_değer(void){
    int dosya_tanıtıcısı=açık_Dosya(Dosya_girdi_ad,R_W|없으면만들기|kesmek_içindekiler,0600);if(dosya_tanıtıcısı<0){uyarı_SMS="Cannot open for save";return 0;}
    intptr_t öğe_BAĞ_DEĞ_SAY=yazma_Dosya_veri(dosya_tanıtıcısı,metin,süre_değer);Kapat_Dosya(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY!=süre_değer){uyarı_SMS="Write failed";return 0;}변경됨=0;uyarı_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SANİYE_değer){while(*첫째값&&*첫째값==*SANİYE_değer){첫째값++;SANİYE_değer++;}return *첫째값==*SANİYE_değer;}
static void BUL_Sonraki(void){int öğe_BAĞ_DEĞ_SAY=0;while(BUL_girdi[öğe_BAĞ_DEĞ_SAY])öğe_BAĞ_DEĞ_SAY++;if(!öğe_BAĞ_DEĞ_SAY){uyarı_SMS="No search pattern";return;}for(int 순번=1;순번<=süre_değer;순번++){int veri_konum=(Dizin_değer+순번)%(süre_değer?süre_değer:1),안쪽순번=0;while(안쪽순번<öğe_BAĞ_DEĞ_SAY&&veri_konum+안쪽순번<süre_değer&&metin[veri_konum+안쪽순번]==(unsigned char)BUL_girdi[안쪽순번])안쪽순번++;if(안쪽순번==öğe_BAĞ_DEĞ_SAY){Dizin_değer=veri_konum;uyarı_SMS="Match";return;}}uyarı_SMS="Pattern not found";}
static int istem(int alan_değer){
    int öğe_BAĞ_DEĞ_SAY=0;komut[0]=0;
    for(;;){taşımak_değer_83b651b8(SATIR_BAĞ_DEĞ_SAY,1);글내보내기("\033[0m\033[2K");bayt_veri(alan_değer);글내보내기(komut);boşaltmak();yardım_alan=alan_değer;int 셋째순번=누름값();yardım_alan=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(öğe_BAĞ_DEĞ_SAY){öğe_BAĞ_DEĞ_SAY--;while(öğe_BAĞ_DEĞ_SAY>0&&((unsigned char)komut[öğe_BAĞ_DEĞ_SAY]&192)==128)öğe_BAĞ_DEĞ_SAY--;komut[öğe_BAĞ_DEĞ_SAY]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&öğe_BAĞ_DEĞ_SAY<120){komut[öğe_BAĞ_DEĞ_SAY++]=셋째순번;komut[öğe_BAĞ_DEĞ_SAY]=0;}
    }
    if(alan_değer=='/'){for(int 순번=0;순번<=öğe_BAĞ_DEĞ_SAY;순번++)BUL_girdi[순번]=komut[순번];BUL_Sonraki();return 0;}
    if(같은지(komut,"q!"))return 1;
    if(같은지(komut,"q")){if(!변경됨)return 1;uyarı_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(komut,"wq")||같은지(komut,"x"))return depo_değer();
    if(같은지(komut,"w")){depo_değer();return 0;}
    if(komut[0]=='w'&&komut[1]==' '){int 순번=2;while(komut[순번]==' ')순번++;int Boyut=öğe_BAĞ_DEĞ_SAY-순번;if(Boyut<1||Boyut>63){uyarı_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Boyut;안쪽순번++)Dosya_girdi_ad[안쪽순번]=komut[순번+안쪽순번];Dosya_girdi_ad[Boyut]=0;depo_değer();return 0;}
    int girdi_satırı=0;for(int 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++){if(komut[순번]<'0'||komut[순번]>'9'){girdi_satırı=0;break;}girdi_satırı=girdi_satırı*10+komut[순번]-'0';if(girdi_satırı>16384){girdi_satırı=0;break;}}
    if(girdi_satırı){Dizin_değer=0;while(--girdi_satırı&&Dizin_değer<süre_değer){Dizin_değer=Bitiş_Ofset(Dizin_değer);if(Dizin_değer<süre_değer)Dizin_değer++;}return 0;}
    uyarı_SMS="Unknown vi command";return 0;
}
int Start_kullanıcı_program(int 무시값){
    (void)무시값;if(kullanıcı_bağımsız_değişken_BAĞ_DEĞ_SAY()!=1||kullanıcı_bağımsız_değişken(0,Dosya_girdi_ad,sizeof(Dosya_girdi_ad))<0){글내보내기("Usage: vi FILE\n");boşaltmak();return 2;}
    int dosya_tanıtıcısı=açık_Dosya(Dosya_girdi_ad,salt_okunur_değer,0);
    if(dosya_tanıtıcısı>=0){int öğe_BAĞ_DEĞ_SAY=dosya_boyutu(dosya_tanıtıcısı);if(öğe_BAĞ_DEĞ_SAY<0||öğe_BAĞ_DEĞ_SAY>Düzenleyici_kapasite){Kapat_Dosya(dosya_tanıtıcısı);return 1;}süre_değer=파일자료읽기(dosya_tanıtıcısı,metin,öğe_BAĞ_DEĞ_SAY);Kapat_Dosya(dosya_tanıtıcısı);if(süre_değer!=öğe_BAĞ_DEĞ_SAY)return 1;for(int 순번=0;순번<süre_değer;순번++)if(!metin[순번]){글내보내기("vi: NUL byte in text file\n");boşaltmak();return 1;}}
    else if(hata_numarası!=2){글내보내기("vi: cannot read file\n");boşaltmak();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");boşaltmak();return 1;}SÜTUNSAY=흐린색&65535;SATIR_BAĞ_DEĞ_SAY=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");boşaltmak();
    int satır_aralığı_parça=0,çıkış_program=0;
    while(!çıkış_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();uyarı_SMS=0;
        if(셋째순번==1001){Dikey(-1);continue;}if(셋째순번==1002){Dikey(1);continue;}if(셋째순번==1003){Dizin_değer=Sonraki_öğe(Dizin_değer);continue;}if(셋째순번==1004){Dizin_değer=Önceki(Dizin_değer);continue;}
        if(셋째순번==1005){Dizin_değer=çalıştır(Dizin_değer);continue;}if(셋째순번==1006){Dizin_değer=Bitiş_Ofset(Dizin_değer);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<SATIR_BAĞ_DEĞ_SAY-2;순번++)Dikey(셋째순번==1008?-1:1);continue;}
        if(Ekle){
            if(셋째순번==27||셋째순번==3){Ekle=0;continue;}
            if(셋째순번==127||셋째순번==8){if(Dizin_değer)바이트지우기(Önceki(Dizin_değer),Dizin_değer);continue;}
            if(셋째순번==1007){if(Dizin_değer<süre_değer)바이트지우기(Dizin_değer,Sonraki_öğe(Dizin_değer));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SANİYE_değer[4];SANİYE_değer[0]=셋째순번;int öğe_BAĞ_DEĞ_SAY=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!öğe_BAĞ_DEĞ_SAY){uyarı_SMS="Invalid UTF-8";continue;}int geçerli=1;for(int 순번=1;순번<öğe_BAĞ_DEĞ_SAY;순번++){int kod_noktası=누름값();if(kod_noktası<128||kod_noktası>191){Beklemede_tuş=kod_noktası;geçerli=0;break;}SANİYE_değer[순번]=kod_noktası;}
                if(geçerli)Ekleme_değer(SANİYE_değer,öğe_BAĞ_DEĞ_SAY);
            }continue;
        }
        if(satır_aralığı_parça){int veri_konum=satır_aralığı_parça;satır_aralığı_parça=0;if(veri_konum=='g'&&셋째순번=='g'){Dizin_değer=0;continue;}if(veri_konum=='Z'&&셋째순번=='Z'){çıkış_program=depo_değer();continue;}if((veri_konum=='d'&&셋째순번=='d')||(veri_konum=='y'&&셋째순번=='y')){int 첫째값=çalıştır(Dizin_değer),SANİYE_değer=Bitiş_Ofset(Dizin_değer);if(SANİYE_değer<süre_değer)SANİYE_değer++;örnek_süre=SANİYE_değer-첫째값;for(int 순번=0;순번<örnek_süre;순번++)복사자료[순번]=metin[첫째값+순번];if(veri_konum=='d')바이트지우기(첫째값,SANİYE_değer);continue;}}
        if(셋째순번=='i'){Ekle=1;continue;}if(셋째순번=='a'){if(Dizin_değer<Bitiş_Ofset(Dizin_değer))Dizin_değer=Sonraki_öğe(Dizin_değer);Ekle=1;continue;}
        if(셋째순번=='I'){Dizin_değer=çalıştır(Dizin_değer);Ekle=1;continue;}if(셋째순번=='A'){Dizin_değer=Bitiş_Ofset(Dizin_değer);Ekle=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char hat_Bitiş='\n';Dizin_değer=셋째순번=='o'?Bitiş_Ofset(Dizin_değer):çalıştır(Dizin_değer);if(Ekleme_değer(&hat_Bitiş,1)){if(셋째순번=='O')Dizin_değer--;Ekle=1;}continue;}
        if(셋째순번=='h'){Dizin_değer=Önceki(Dizin_değer);continue;}if(셋째순번=='l'){Dizin_değer=Sonraki_öğe(Dizin_değer);continue;}if(셋째순번=='j'){Dikey(1);continue;}if(셋째순번=='k'){Dikey(-1);continue;}
        if(셋째순번=='0'){Dizin_değer=çalıştır(Dizin_değer);continue;}if(셋째순번=='$'){Dizin_değer=Bitiş_Ofset(Dizin_değer);continue;}if(셋째순번=='G'){Dizin_değer=çalıştır(süre_değer);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){satır_aralığı_parça=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(Dizin_değer<süre_değer)바이트지우기(Dizin_değer,Sonraki_öğe(Dizin_değer));continue;}
        if(셋째순번=='p'&&örnek_süre){Dizin_değer=Bitiş_Ofset(Dizin_değer);if(Dizin_değer<süre_değer)Dizin_değer++;Ekleme_değer(복사자료,örnek_süre);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Düzenleyici_kapasite;순번++){unsigned char SANİYE_değer=metin[순번];metin[순번]=geri_alma_veri[순번];geri_alma_veri[순번]=SANİYE_değer;}int öğe_BAĞ_DEĞ_SAY=süre_değer;süre_değer=geri_alma_süre;geri_alma_süre=öğe_BAĞ_DEĞ_SAY;öğe_BAĞ_DEĞ_SAY=Dizin_değer;Dizin_değer=위쪽;위쪽=öğe_BAĞ_DEĞ_SAY;öğe_BAĞ_DEĞ_SAY=변경됨;변경됨=geri_alma_Değişiklikler;geri_alma_Değişiklikler=öğe_BAĞ_DEĞ_SAY;continue;}
        if(셋째순번==':'||셋째순번=='/'){çıkış_program=istem(셋째순번);continue;}if(셋째순번=='n'){BUL_Sonraki();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");boşaltmak();사용자호출(16,2,0,0,0,0,0);return 0;
}
