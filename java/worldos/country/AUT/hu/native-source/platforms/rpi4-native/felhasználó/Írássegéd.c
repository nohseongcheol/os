/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Írássegéd_kapacitás 16384
static unsigned char Szöveg[Írássegéd_kapacitás],visszavon_adat[Írássegéd_kapacitás],복사자료[Írássegéd_kapacitás],KR_adat[1024];
static int hossz_ÉRTÉK,INDEX_ÉRTÉK,맨위,왼쪽,변경됨,Beszúrás,visszavon_hossz,위쪽,visszavon_Módosítások,되돌림있음,másol_hossz,사용량,OSZLOPOK=68,SOR_DARAB=19;
static char Fájl_bejegyzés_név[64],Parancs[128],keres_bejegyzés[128];
static const char *alapelv_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Függő_Kulcs;
static int súgó_terület,Állapot_KÉP,Állapot_várólista;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_adat,사용량,0,0,0);사용량=0;}}
static void bájt_adat(unsigned kódpont){if(Állapot_KÉP){if((kódpont&192)!=128){Állapot_várólista+=kódpont>=196?2:1;}if(Állapot_várólista>=OSZLOPOK)return;}if(사용량==(int)sizeof(KR_adat))출력비우기();KR_adat[사용량++]=kódpont;}
static void 글내보내기(const char *sztring_adat){while(*sztring_adat)bájt_adat((unsigned char)*sztring_adat++);}
static void 수치(unsigned cikk_DARAB){char MPERC_ÉRTÉK[12];int 순번=0;do{MPERC_ÉRTÉK[순번++]='0'+cikk_DARAB%10;cikk_DARAB/=10;}while(cikk_DARAB);while(순번)bájt_adat(MPERC_ÉRTÉK[--순번]);}
static void áthelyez_ÉRTÉK(int SOR_pozíció,int OSZLOP_pozíció){글내보내기("\033[");수치(SOR_pozíció);bájt_adat(';');수치(OSZLOP_pozíció);bájt_adat('H');}
static int Előző(int adat_pozíció){if(adat_pozíció){adat_pozíció--;while(adat_pozíció>0&&(Szöveg[adat_pozíció]&192)==128)adat_pozíció--;}return adat_pozíció;}
static int Tovább_cikk(int adat_pozíció){if(adat_pozíció<hossz_ÉRTÉK){adat_pozíció++;while(adat_pozíció<hossz_ÉRTÉK&&(Szöveg[adat_pozíció]&192)==128)adat_pozíció++;}return adat_pozíció;}
static int Futtatás(int adat_pozíció){while(adat_pozíció>0&&Szöveg[adat_pozíció-1]!='\n')adat_pozíció--;return adat_pozíció;}
static int megszüntet_Ofszet(int adat_pozíció){while(adat_pozíció<hossz_ÉRTÉK&&Szöveg[adat_pozíció]!='\n')adat_pozíció++;return adat_pozíció;}
static int 너비(unsigned kódpont){return kódpont>=196?2:1;}
static int OSZLOP(int adat_pozíció){int kódpont=0;for(int 순번=Futtatás(adat_pozíció);순번<adat_pozíció;순번=Tovább_cikk(순번))kódpont+=Szöveg[순번]=='\t'?4-kódpont%4:너비(Szöveg[순번]);return kódpont;}
static void ellenőrzőpont(void){for(int 순번=0;순번<hossz_ÉRTÉK;순번++)visszavon_adat[순번]=Szöveg[순번];visszavon_hossz=hossz_ÉRTÉK;위쪽=INDEX_ÉRTÉK;visszavon_Módosítások=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){ellenőrzőpont();for(int 순번=도착위치;순번<hossz_ÉRTÉK;순번++)Szöveg[출발위치+순번-도착위치]=Szöveg[순번];hossz_ÉRTÉK-=도착위치-출발위치;INDEX_ÉRTÉK=출발위치;변경됨=1;}
static int hozzáfűz_ÉRTÉK(const unsigned char *sztring_adat,int cikk_DARAB){if(cikk_DARAB>Írássegéd_kapacitás-hossz_ÉRTÉK){alapelv_SMS="File full (16384 bytes)";return 0;}ellenőrzőpont();for(int 순번=hossz_ÉRTÉK-1;순번>=INDEX_ÉRTÉK;순번--)Szöveg[순번+cikk_DARAB]=Szöveg[순번];for(int 순번=0;순번<cikk_DARAB;순번++)Szöveg[INDEX_ÉRTÉK+순번]=sztring_adat[순번];hossz_ÉRTÉK+=cikk_DARAB;INDEX_ÉRTÉK+=cikk_DARAB;변경됨=1;return 1;}
static void szektor(int 차이){int OSZLOP_pozíció=OSZLOP(INDEX_ÉRTÉK),adat_pozíció=Futtatás(INDEX_ÉRTÉK);if(차이<0){if(!adat_pozíció)return;adat_pozíció=Futtatás(adat_pozíció-1);}else{adat_pozíció=megszüntet_Ofszet(adat_pozíció);if(adat_pozíció==hossz_ÉRTÉK)return;adat_pozíció++;}int kódpont=0;while(adat_pozíció<hossz_ÉRTÉK&&Szöveg[adat_pozíció]!='\n'&&kódpont<OSZLOP_pozíció){kódpont+=Szöveg[adat_pozíció]=='\t'?4-kódpont%4:너비(Szöveg[adat_pozíció]);adat_pozíció=Tovább_cikk(adat_pozíció);}INDEX_ÉRTÉK=adat_pozíció;}
static void 화면그리기(void){
    if(INDEX_ÉRTÉK>hossz_ÉRTÉK)INDEX_ÉRTÉK=hossz_ÉRTÉK;if(맨위>INDEX_ÉRTÉK)맨위=Futtatás(INDEX_ÉRTÉK);맨위=Futtatás(맨위);
    int SOR_pozíció=0;for(int 순번=맨위;순번<INDEX_ÉRTÉK;순번++)if(Szöveg[순번]=='\n')SOR_pozíció++;
    while(SOR_pozíció>=SOR_DARAB-1){맨위=megszüntet_Ofszet(맨위);if(맨위<hossz_ÉRTÉK)맨위++;SOR_pozíció--;}
    int OSZLOP_pozíció=OSZLOP(INDEX_ÉRTÉK);if(OSZLOP_pozíció<왼쪽)왼쪽=OSZLOP_pozíció;if(OSZLOP_pozíció-왼쪽>=OSZLOPOK-1)왼쪽=OSZLOP_pozíció-OSZLOPOK+2;
    글내보내기("\033[?25l");int adat_pozíció=맨위;
    for(int 반환값=0;반환값<SOR_DARAB-1;반환값++){
        áthelyez_ÉRTÉK(반환값+1,1);글내보내기("\033[0m\033[2K");int kódpont=0,그려진상태=0;
        if(adat_pozíció>=hossz_ÉRTÉK&&반환값>SOR_pozíció){글내보내기("\033[90m~\033[0m");continue;}
        while(adat_pozíció<hossz_ÉRTÉK&&Szöveg[adat_pozíció]!='\n'){
            int Tovább_Ofszet=Tovább_cikk(adat_pozíció),너비값=Szöveg[adat_pozíció]=='\t'?4-kódpont%4:너비(Szöveg[adat_pozíció]);
            if(kódpont>=왼쪽&&kódpont-왼쪽+너비값<OSZLOPOK){
                if(Szöveg[adat_pozíció]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bájt_adat(' ');}else if(Szöveg[adat_pozíció]<32||Szöveg[adat_pozíció]==127){bájt_adat('?');}else for(int 안쪽순번=adat_pozíció;안쪽순번<Tovább_Ofszet;안쪽순번++)bájt_adat(Szöveg[안쪽순번]);그려진상태+=너비값;
            }kódpont+=너비값;adat_pozíció=Tovább_Ofszet;
        }
        (void)그려진상태;if(adat_pozíció<hossz_ÉRTÉK)adat_pozíció++;
    }
    áthelyez_ÉRTÉK(SOR_DARAB,1);글내보내기("\033[7m\033[2K");Állapot_KÉP=1;Állapot_várólista=0;글내보내기(Beszúrás?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fájl_bejegyzés_név[이름바이트수]&&이름바이트수<30)bájt_adat(Fájl_bejegyzés_név[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Vonal=1;for(int 순번=0;순번<INDEX_ÉRTÉK;순번++)if(Szöveg[순번]=='\n')Vonal++;수치(Vonal);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(alapelv_SMS){int cikk_DARAB=0;글내보내기(" | ");while(alapelv_SMS[cikk_DARAB]&&cikk_DARAB<20)bájt_adat(alapelv_SMS[cikk_DARAB++]);}
    Állapot_KÉP=0;글내보내기("\033[0m");áthelyez_ÉRTÉK(SOR_pozíció+1,OSZLOP_pozíció-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Függő_Kulcs){int 셋째순번=Függő_Kulcs;Függő_Kulcs=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Méret=사용자호출(16,3,0,0,0,0,0);
        if(OSZLOPOK!=(int)(Méret&65535)||SOR_DARAB!=(int)(Méret>>16)){
            OSZLOPOK=Méret&65535;SOR_DARAB=Méret>>16;화면그리기();
            if(súgó_terület){áthelyez_ÉRTÉK(SOR_DARAB,1);글내보내기("\033[0m\033[2K");bájt_adat(súgó_terület);글내보내기(Parancs);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned aktuális_pozíció=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-aktuális_pozíció<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Függő_Kulcs=셋째순번;return 27;}
    int cikk_DARAB=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){cikk_DARAB=cikk_DARAB*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return cikk_DARAB==3?1007:cikk_DARAB==5?1008:cikk_DARAB==6?1009:cikk_DARAB==1?1005:cikk_DARAB==4?1006:27;return 27;}return 27;
}
static int tár_ÉRTÉK(void){
    int fájlleíró=készít_Fájl(Fájl_bejegyzés_név,읽고쓰기|없으면만들기|vág_Tartalom,0600);if(fájlleíró<0){alapelv_SMS="Cannot open for save";return 0;}
    intptr_t cikk_DARAB=ír_Fájl_adat(fájlleíró,Szöveg,hossz_ÉRTÉK);bezár_Fájl(fájlleíró);if(cikk_DARAB!=hossz_ÉRTÉK){alapelv_SMS="Write failed";return 0;}변경됨=0;alapelv_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *MPERC_ÉRTÉK){while(*첫째값&&*첫째값==*MPERC_ÉRTÉK){첫째값++;MPERC_ÉRTÉK++;}return *첫째값==*MPERC_ÉRTÉK;}
static void keres_Tovább(void){int cikk_DARAB=0;while(keres_bejegyzés[cikk_DARAB])cikk_DARAB++;if(!cikk_DARAB){alapelv_SMS="No search pattern";return;}for(int 순번=1;순번<=hossz_ÉRTÉK;순번++){int adat_pozíció=(INDEX_ÉRTÉK+순번)%(hossz_ÉRTÉK?hossz_ÉRTÉK:1),안쪽순번=0;while(안쪽순번<cikk_DARAB&&adat_pozíció+안쪽순번<hossz_ÉRTÉK&&Szöveg[adat_pozíció+안쪽순번]==(unsigned char)keres_bejegyzés[안쪽순번])안쪽순번++;if(안쪽순번==cikk_DARAB){INDEX_ÉRTÉK=adat_pozíció;alapelv_SMS="Match";return;}}alapelv_SMS="Pattern not found";}
static int kér(int terület_ÉRTÉK){
    int cikk_DARAB=0;Parancs[0]=0;
    for(;;){áthelyez_ÉRTÉK(SOR_DARAB,1);글내보내기("\033[0m\033[2K");bájt_adat(terület_ÉRTÉK);글내보내기(Parancs);출력비우기();súgó_terület=terület_ÉRTÉK;int 셋째순번=누름값();súgó_terület=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(cikk_DARAB){cikk_DARAB--;while(cikk_DARAB>0&&((unsigned char)Parancs[cikk_DARAB]&192)==128)cikk_DARAB--;Parancs[cikk_DARAB]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&cikk_DARAB<120){Parancs[cikk_DARAB++]=셋째순번;Parancs[cikk_DARAB]=0;}
    }
    if(terület_ÉRTÉK=='/'){for(int 순번=0;순번<=cikk_DARAB;순번++)keres_bejegyzés[순번]=Parancs[순번];keres_Tovább();return 0;}
    if(같은지(Parancs,"q!"))return 1;
    if(같은지(Parancs,"q")){if(!변경됨)return 1;alapelv_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Parancs,"wq")||같은지(Parancs,"x"))return tár_ÉRTÉK();
    if(같은지(Parancs,"w")){tár_ÉRTÉK();return 0;}
    if(Parancs[0]=='w'&&Parancs[1]==' '){int 순번=2;while(Parancs[순번]==' ')순번++;int Méret=cikk_DARAB-순번;if(Méret<1||Méret>63){alapelv_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Méret;안쪽순번++)Fájl_bejegyzés_név[안쪽순번]=Parancs[순번+안쪽순번];Fájl_bejegyzés_név[Méret]=0;tár_ÉRTÉK();return 0;}
    int Vonal=0;for(int 순번=0;순번<cikk_DARAB;순번++){if(Parancs[순번]<'0'||Parancs[순번]>'9'){Vonal=0;break;}Vonal=Vonal*10+Parancs[순번]-'0';if(Vonal>16384){Vonal=0;break;}}
    if(Vonal){INDEX_ÉRTÉK=0;while(--Vonal&&INDEX_ÉRTÉK<hossz_ÉRTÉK){INDEX_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);if(INDEX_ÉRTÉK<hossz_ÉRTÉK)INDEX_ÉRTÉK++;}return 0;}
    alapelv_SMS="Unknown vi command";return 0;
}
int START_felhasználó_app(int 무시값){
    (void)무시값;if(felhasználó_argumentum_DARAB()!=1||felhasználó_argumentum(0,Fájl_bejegyzés_név,sizeof(Fájl_bejegyzés_név))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fájlleíró=készít_Fájl(Fájl_bejegyzés_név,írásvédett_ÉRTÉK,0);
    if(fájlleíró>=0){int cikk_DARAB=fájlméret(fájlleíró);if(cikk_DARAB<0||cikk_DARAB>Írássegéd_kapacitás){bezár_Fájl(fájlleíró);return 1;}hossz_ÉRTÉK=파일자료읽기(fájlleíró,Szöveg,cikk_DARAB);bezár_Fájl(fájlleíró);if(hossz_ÉRTÉK!=cikk_DARAB)return 1;for(int 순번=0;순번<hossz_ÉRTÉK;순번++)if(!Szöveg[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(hibaszám!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}OSZLOPOK=흐린색&65535;SOR_DARAB=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int sorköz_rész=0,kilépés_app=0;
    while(!kilépés_app){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();alapelv_SMS=0;
        if(셋째순번==1001){szektor(-1);continue;}if(셋째순번==1002){szektor(1);continue;}if(셋째순번==1003){INDEX_ÉRTÉK=Tovább_cikk(INDEX_ÉRTÉK);continue;}if(셋째순번==1004){INDEX_ÉRTÉK=Előző(INDEX_ÉRTÉK);continue;}
        if(셋째순번==1005){INDEX_ÉRTÉK=Futtatás(INDEX_ÉRTÉK);continue;}if(셋째순번==1006){INDEX_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<SOR_DARAB-2;순번++)szektor(셋째순번==1008?-1:1);continue;}
        if(Beszúrás){
            if(셋째순번==27||셋째순번==3){Beszúrás=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_ÉRTÉK)바이트지우기(Előző(INDEX_ÉRTÉK),INDEX_ÉRTÉK);continue;}
            if(셋째순번==1007){if(INDEX_ÉRTÉK<hossz_ÉRTÉK)바이트지우기(INDEX_ÉRTÉK,Tovább_cikk(INDEX_ÉRTÉK));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char MPERC_ÉRTÉK[4];MPERC_ÉRTÉK[0]=셋째순번;int cikk_DARAB=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!cikk_DARAB){alapelv_SMS="Invalid UTF-8";continue;}int érvényes=1;for(int 순번=1;순번<cikk_DARAB;순번++){int kódpont=누름값();if(kódpont<128||kódpont>191){Függő_Kulcs=kódpont;érvényes=0;break;}MPERC_ÉRTÉK[순번]=kódpont;}
                if(érvényes)hozzáfűz_ÉRTÉK(MPERC_ÉRTÉK,cikk_DARAB);
            }continue;
        }
        if(sorköz_rész){int adat_pozíció=sorköz_rész;sorköz_rész=0;if(adat_pozíció=='g'&&셋째순번=='g'){INDEX_ÉRTÉK=0;continue;}if(adat_pozíció=='Z'&&셋째순번=='Z'){kilépés_app=tár_ÉRTÉK();continue;}if((adat_pozíció=='d'&&셋째순번=='d')||(adat_pozíció=='y'&&셋째순번=='y')){int 첫째값=Futtatás(INDEX_ÉRTÉK),MPERC_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);if(MPERC_ÉRTÉK<hossz_ÉRTÉK)MPERC_ÉRTÉK++;másol_hossz=MPERC_ÉRTÉK-첫째값;for(int 순번=0;순번<másol_hossz;순번++)복사자료[순번]=Szöveg[첫째값+순번];if(adat_pozíció=='d')바이트지우기(첫째값,MPERC_ÉRTÉK);continue;}}
        if(셋째순번=='i'){Beszúrás=1;continue;}if(셋째순번=='a'){if(INDEX_ÉRTÉK<megszüntet_Ofszet(INDEX_ÉRTÉK))INDEX_ÉRTÉK=Tovább_cikk(INDEX_ÉRTÉK);Beszúrás=1;continue;}
        if(셋째순번=='I'){INDEX_ÉRTÉK=Futtatás(INDEX_ÉRTÉK);Beszúrás=1;continue;}if(셋째순번=='A'){INDEX_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);Beszúrás=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char sor_megszüntet='\n';INDEX_ÉRTÉK=셋째순번=='o'?megszüntet_Ofszet(INDEX_ÉRTÉK):Futtatás(INDEX_ÉRTÉK);if(hozzáfűz_ÉRTÉK(&sor_megszüntet,1)){if(셋째순번=='O')INDEX_ÉRTÉK--;Beszúrás=1;}continue;}
        if(셋째순번=='h'){INDEX_ÉRTÉK=Előző(INDEX_ÉRTÉK);continue;}if(셋째순번=='l'){INDEX_ÉRTÉK=Tovább_cikk(INDEX_ÉRTÉK);continue;}if(셋째순번=='j'){szektor(1);continue;}if(셋째순번=='k'){szektor(-1);continue;}
        if(셋째순번=='0'){INDEX_ÉRTÉK=Futtatás(INDEX_ÉRTÉK);continue;}if(셋째순번=='$'){INDEX_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);continue;}if(셋째순번=='G'){INDEX_ÉRTÉK=Futtatás(hossz_ÉRTÉK);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){sorköz_rész=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_ÉRTÉK<hossz_ÉRTÉK)바이트지우기(INDEX_ÉRTÉK,Tovább_cikk(INDEX_ÉRTÉK));continue;}
        if(셋째순번=='p'&&másol_hossz){INDEX_ÉRTÉK=megszüntet_Ofszet(INDEX_ÉRTÉK);if(INDEX_ÉRTÉK<hossz_ÉRTÉK)INDEX_ÉRTÉK++;hozzáfűz_ÉRTÉK(복사자료,másol_hossz);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Írássegéd_kapacitás;순번++){unsigned char MPERC_ÉRTÉK=Szöveg[순번];Szöveg[순번]=visszavon_adat[순번];visszavon_adat[순번]=MPERC_ÉRTÉK;}int cikk_DARAB=hossz_ÉRTÉK;hossz_ÉRTÉK=visszavon_hossz;visszavon_hossz=cikk_DARAB;cikk_DARAB=INDEX_ÉRTÉK;INDEX_ÉRTÉK=위쪽;위쪽=cikk_DARAB;cikk_DARAB=변경됨;변경됨=visszavon_Módosítások;visszavon_Módosítások=cikk_DARAB;continue;}
        if(셋째순번==':'||셋째순번=='/'){kilépés_app=kér(셋째순번);continue;}if(셋째순번=='n'){keres_Tovább();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
