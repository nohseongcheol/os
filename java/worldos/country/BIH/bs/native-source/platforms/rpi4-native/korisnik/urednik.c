/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define 편집용량 16384
static unsigned char Tekst[편집용량],opozvati_radnju_podaci[편집용량],복사자료[편집용량],mjera_podaci[1024];
static int dužina_VALUE,INDEX_VALUE,맨위,왼쪽,변경됨,Umetni,opozvati_radnju_dužina,위쪽,opozvati_radnju_Promjene,되돌림있음,instanca_dužina,사용량,Kolone=68,ROW_COUNT=19;
static char fajl_unos_naziv[64],Naredba[128],FIND_unos[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned na_čekanju_ključ;
static int pomoć_oblast,stanje_IMAGE,stanje_redoslijed;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)mjera_podaci,사용량,0,0,0);사용량=0;}}
static void bajt_podaci(unsigned kôd_znaka){if(stanje_IMAGE){if((kôd_znaka&192)!=128){stanje_redoslijed+=kôd_znaka>=196?2:1;}if(stanje_redoslijed>=Kolone)return;}if(사용량==(int)sizeof(mjera_podaci))출력비우기();mjera_podaci[사용량++]=kôd_znaka;}
static void 글내보내기(const char *string_podaci){while(*string_podaci)bajt_podaci((unsigned char)*string_podaci++);}
static void 수치(unsigned stavka_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+stavka_COUNT%10;stavka_COUNT/=10;}while(stavka_COUNT);while(순번)bajt_podaci(SECOND_VALUE[--순번]);}
static void pomaći_VALUE(int ROW_položaj,int COLUMN_položaj){글내보내기("\033[");수치(ROW_položaj);bajt_podaci(';');수치(COLUMN_položaj);bajt_podaci('H');}
static int 이전항목(int podaci_položaj){if(podaci_položaj){podaci_položaj--;while(podaci_položaj>0&&(Tekst[podaci_položaj]&192)==128)podaci_položaj--;}return podaci_položaj;}
static int Dalje_stavka(int podaci_položaj){if(podaci_položaj<dužina_VALUE){podaci_položaj++;while(podaci_položaj<dužina_VALUE&&(Tekst[podaci_položaj]&192)==128)podaci_položaj++;}return podaci_položaj;}
static int Pokreni(int podaci_položaj){while(podaci_položaj>0&&Tekst[podaci_položaj-1]!='\n')podaci_položaj--;return podaci_položaj;}
static int završiti_Pomak(int podaci_položaj){while(podaci_položaj<dužina_VALUE&&Tekst[podaci_položaj]!='\n')podaci_položaj++;return podaci_položaj;}
static int 너비(unsigned kôd_znaka){return kôd_znaka>=196?2:1;}
static int COLUMN(int podaci_položaj){int kôd_znaka=0;for(int 순번=Pokreni(podaci_položaj);순번<podaci_položaj;순번=Dalje_stavka(순번))kôd_znaka+=Tekst[순번]=='\t'?4-kôd_znaka%4:너비(Tekst[순번]);return kôd_znaka;}
static void tačka_pregleda(void){for(int 순번=0;순번<dužina_VALUE;순번++)opozvati_radnju_podaci[순번]=Tekst[순번];opozvati_radnju_dužina=dužina_VALUE;위쪽=INDEX_VALUE;opozvati_radnju_Promjene=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){tačka_pregleda();for(int 순번=도착위치;순번<dužina_VALUE;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];dužina_VALUE-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int 덧붙이기(const unsigned char *string_podaci,int stavka_COUNT){if(stavka_COUNT>편집용량-dužina_VALUE){알림문="File full (16384 bytes)";return 0;}tačka_pregleda();for(int 순번=dužina_VALUE-1;순번>=INDEX_VALUE;순번--)Tekst[순번+stavka_COUNT]=Tekst[순번];for(int 순번=0;순번<stavka_COUNT;순번++)Tekst[INDEX_VALUE+순번]=string_podaci[순번];dužina_VALUE+=stavka_COUNT;INDEX_VALUE+=stavka_COUNT;변경됨=1;return 1;}
static void Vertikalno(int 차이){int COLUMN_položaj=COLUMN(INDEX_VALUE),podaci_položaj=Pokreni(INDEX_VALUE);if(차이<0){if(!podaci_položaj)return;podaci_položaj=Pokreni(podaci_položaj-1);}else{podaci_položaj=završiti_Pomak(podaci_položaj);if(podaci_položaj==dužina_VALUE)return;podaci_položaj++;}int kôd_znaka=0;while(podaci_položaj<dužina_VALUE&&Tekst[podaci_položaj]!='\n'&&kôd_znaka<COLUMN_položaj){kôd_znaka+=Tekst[podaci_položaj]=='\t'?4-kôd_znaka%4:너비(Tekst[podaci_položaj]);podaci_položaj=Dalje_stavka(podaci_položaj);}INDEX_VALUE=podaci_položaj;}
static void 화면그리기(void){
    if(INDEX_VALUE>dužina_VALUE)INDEX_VALUE=dužina_VALUE;if(맨위>INDEX_VALUE)맨위=Pokreni(INDEX_VALUE);맨위=Pokreni(맨위);
    int ROW_položaj=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')ROW_položaj++;
    while(ROW_položaj>=ROW_COUNT-1){맨위=završiti_Pomak(맨위);if(맨위<dužina_VALUE)맨위++;ROW_položaj--;}
    int COLUMN_položaj=COLUMN(INDEX_VALUE);if(COLUMN_položaj<왼쪽)왼쪽=COLUMN_položaj;if(COLUMN_položaj-왼쪽>=Kolone-1)왼쪽=COLUMN_položaj-Kolone+2;
    글내보내기("\033[?25l");int podaci_položaj=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        pomaći_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int kôd_znaka=0,그려진상태=0;
        if(podaci_položaj>=dužina_VALUE&&반환값>ROW_položaj){글내보내기("\033[90m~\033[0m");continue;}
        while(podaci_položaj<dužina_VALUE&&Tekst[podaci_položaj]!='\n'){
            int Dalje_Pomak=Dalje_stavka(podaci_položaj),너비값=Tekst[podaci_položaj]=='\t'?4-kôd_znaka%4:너비(Tekst[podaci_položaj]);
            if(kôd_znaka>=왼쪽&&kôd_znaka-왼쪽+너비값<Kolone){
                if(Tekst[podaci_položaj]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_podaci(' ');}else if(Tekst[podaci_položaj]<32||Tekst[podaci_položaj]==127){bajt_podaci('?');}else for(int 안쪽순번=podaci_položaj;안쪽순번<Dalje_Pomak;안쪽순번++)bajt_podaci(Tekst[안쪽순번]);그려진상태+=너비값;
            }kôd_znaka+=너비값;podaci_položaj=Dalje_Pomak;
        }
        (void)그려진상태;if(podaci_položaj<dužina_VALUE)podaci_položaj++;
    }
    pomaći_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");stanje_IMAGE=1;stanje_redoslijed=0;글내보내기(Umetni?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(fajl_unos_naziv[이름바이트수]&&이름바이트수<30)bajt_podaci(fajl_unos_naziv[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Linija=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')Linija++;수치(Linija);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int stavka_COUNT=0;글내보내기(" | ");while(알림문[stavka_COUNT]&&stavka_COUNT<20)bajt_podaci(알림문[stavka_COUNT++]);}
    stanje_IMAGE=0;글내보내기("\033[0m");pomaći_VALUE(ROW_položaj+1,COLUMN_položaj-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(na_čekanju_ključ){int 셋째순번=na_čekanju_ključ;na_čekanju_ključ=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Veličina=사용자호출(16,3,0,0,0,0,0);
        if(Kolone!=(int)(Veličina&65535)||ROW_COUNT!=(int)(Veličina>>16)){
            Kolone=Veličina&65535;ROW_COUNT=Veličina>>16;화면그리기();
            if(pomoć_oblast){pomaći_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(pomoć_oblast);글내보내기(Naredba);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned trenutno_položaj=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-trenutno_položaj<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){na_čekanju_ključ=셋째순번;return 27;}
    int stavka_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){stavka_COUNT=stavka_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return stavka_COUNT==3?1007:stavka_COUNT==5?1008:stavka_COUNT==6?1009:stavka_COUNT==1?1005:stavka_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int fajl_hvatište=kreirati_fajl(fajl_unos_naziv,i_za_čitanje_i_za_pisanje|없으면만들기|내용비우기,0600);if(fajl_hvatište<0){알림문="Cannot open for save";return 0;}
    intptr_t stavka_COUNT=pisati_fajl_podaci(fajl_hvatište,Tekst,dužina_VALUE);zatvoriti_fajl(fajl_hvatište);if(stavka_COUNT!=dužina_VALUE){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Dalje(void){int stavka_COUNT=0;while(FIND_unos[stavka_COUNT])stavka_COUNT++;if(!stavka_COUNT){알림문="No search pattern";return;}for(int 순번=1;순번<=dužina_VALUE;순번++){int podaci_položaj=(INDEX_VALUE+순번)%(dužina_VALUE?dužina_VALUE:1),안쪽순번=0;while(안쪽순번<stavka_COUNT&&podaci_položaj+안쪽순번<dužina_VALUE&&Tekst[podaci_položaj+안쪽순번]==(unsigned char)FIND_unos[안쪽순번])안쪽순번++;if(안쪽순번==stavka_COUNT){INDEX_VALUE=podaci_položaj;알림문="Match";return;}}알림문="Pattern not found";}
static int upit(int oblast_VALUE){
    int stavka_COUNT=0;Naredba[0]=0;
    for(;;){pomaći_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podaci(oblast_VALUE);글내보내기(Naredba);출력비우기();pomoć_oblast=oblast_VALUE;int 셋째순번=누름값();pomoć_oblast=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(stavka_COUNT){stavka_COUNT--;while(stavka_COUNT>0&&((unsigned char)Naredba[stavka_COUNT]&192)==128)stavka_COUNT--;Naredba[stavka_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&stavka_COUNT<120){Naredba[stavka_COUNT++]=셋째순번;Naredba[stavka_COUNT]=0;}
    }
    if(oblast_VALUE=='/'){for(int 순번=0;순번<=stavka_COUNT;순번++)FIND_unos[순번]=Naredba[순번];FIND_Dalje();return 0;}
    if(같은지(Naredba,"q!"))return 1;
    if(같은지(Naredba,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(Naredba,"wq")||같은지(Naredba,"x"))return Store_VALUE();
    if(같은지(Naredba,"w")){Store_VALUE();return 0;}
    if(Naredba[0]=='w'&&Naredba[1]==' '){int 순번=2;while(Naredba[순번]==' ')순번++;int Veličina=stavka_COUNT-순번;if(Veličina<1||Veličina>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Veličina;안쪽순번++)fajl_unos_naziv[안쪽순번]=Naredba[순번+안쪽순번];fajl_unos_naziv[Veličina]=0;Store_VALUE();return 0;}
    int Linija=0;for(int 순번=0;순번<stavka_COUNT;순번++){if(Naredba[순번]<'0'||Naredba[순번]>'9'){Linija=0;break;}Linija=Linija*10+Naredba[순번]-'0';if(Linija>16384){Linija=0;break;}}
    if(Linija){INDEX_VALUE=0;while(--Linija&&INDEX_VALUE<dužina_VALUE){INDEX_VALUE=završiti_Pomak(INDEX_VALUE);if(INDEX_VALUE<dužina_VALUE)INDEX_VALUE++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int START_korisnik_program(int 무시값){
    (void)무시값;if(korisnik_argument_COUNT()!=1||korisnik_argument(0,fajl_unos_naziv,sizeof(fajl_unos_naziv))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int fajl_hvatište=kreirati_fajl(fajl_unos_naziv,samo_za_čitanje_VALUE,0);
    if(fajl_hvatište>=0){int stavka_COUNT=fajl_podesiti_veličinu(fajl_hvatište);if(stavka_COUNT<0||stavka_COUNT>편집용량){zatvoriti_fajl(fajl_hvatište);return 1;}dužina_VALUE=파일자료읽기(fajl_hvatište,Tekst,stavka_COUNT);zatvoriti_fajl(fajl_hvatište);if(dužina_VALUE!=stavka_COUNT)return 1;for(int 순번=0;순번<dužina_VALUE;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(broj_greške!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}Kolone=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,izađi_program=0;
    while(!izađi_program){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){Vertikalno(-1);continue;}if(셋째순번==1002){Vertikalno(1);continue;}if(셋째순번==1003){INDEX_VALUE=Dalje_stavka(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Pokreni(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=završiti_Pomak(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Vertikalno(셋째순번==1008?-1:1);continue;}
        if(Umetni){
            if(셋째순번==27||셋째순번==3){Umetni=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<dužina_VALUE)바이트지우기(INDEX_VALUE,Dalje_stavka(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int stavka_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!stavka_COUNT){알림문="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<stavka_COUNT;순번++){int kôd_znaka=누름값();if(kôd_znaka<128||kôd_znaka>191){na_čekanju_ključ=kôd_znaka;유효함=0;break;}SECOND_VALUE[순번]=kôd_znaka;}
                if(유효함)덧붙이기(SECOND_VALUE,stavka_COUNT);
            }continue;
        }
        if(앞부분){int podaci_položaj=앞부분;앞부분=0;if(podaci_položaj=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(podaci_položaj=='Z'&&셋째순번=='Z'){izađi_program=Store_VALUE();continue;}if((podaci_položaj=='d'&&셋째순번=='d')||(podaci_položaj=='y'&&셋째순번=='y')){int 첫째값=Pokreni(INDEX_VALUE),SECOND_VALUE=završiti_Pomak(INDEX_VALUE);if(SECOND_VALUE<dužina_VALUE)SECOND_VALUE++;instanca_dužina=SECOND_VALUE-첫째값;for(int 순번=0;순번<instanca_dužina;순번++)복사자료[순번]=Tekst[첫째값+순번];if(podaci_položaj=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Umetni=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<završiti_Pomak(INDEX_VALUE))INDEX_VALUE=Dalje_stavka(INDEX_VALUE);Umetni=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Pokreni(INDEX_VALUE);Umetni=1;continue;}if(셋째순번=='A'){INDEX_VALUE=završiti_Pomak(INDEX_VALUE);Umetni=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char redak_završiti='\n';INDEX_VALUE=셋째순번=='o'?završiti_Pomak(INDEX_VALUE):Pokreni(INDEX_VALUE);if(덧붙이기(&redak_završiti,1)){if(셋째순번=='O')INDEX_VALUE--;Umetni=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Dalje_stavka(INDEX_VALUE);continue;}if(셋째순번=='j'){Vertikalno(1);continue;}if(셋째순번=='k'){Vertikalno(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Pokreni(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=završiti_Pomak(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Pokreni(dužina_VALUE);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<dužina_VALUE)바이트지우기(INDEX_VALUE,Dalje_stavka(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&instanca_dužina){INDEX_VALUE=završiti_Pomak(INDEX_VALUE);if(INDEX_VALUE<dužina_VALUE)INDEX_VALUE++;덧붙이기(복사자료,instanca_dužina);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<편집용량;순번++){unsigned char SECOND_VALUE=Tekst[순번];Tekst[순번]=opozvati_radnju_podaci[순번];opozvati_radnju_podaci[순번]=SECOND_VALUE;}int stavka_COUNT=dužina_VALUE;dužina_VALUE=opozvati_radnju_dužina;opozvati_radnju_dužina=stavka_COUNT;stavka_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=stavka_COUNT;stavka_COUNT=변경됨;변경됨=opozvati_radnju_Promjene;opozvati_radnju_Promjene=stavka_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){izađi_program=upit(셋째순번);continue;}if(셋째순번=='n'){FIND_Dalje();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
