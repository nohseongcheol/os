/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define korrektor_võimsus 16384
static unsigned char Tekst[korrektor_võimsus],tagasi_võtma_andmed[korrektor_võimsus],복사자료[korrektor_võimsus],näitaja_andmed[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,Lisa_8e07c86f,되돌림길이,위쪽,tagasi_võtma_Muudatused,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Fail_kirje_nimetus[64],Käsk[128],FIND_kirje[128];
static const char *teatamine_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned ootel_Võti;
static int spikker_ala,Olek_pilt,Olek_järjekord;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)näitaja_andmed,사용량,0,0,0);사용량=0;}}
static void bait_andmed(unsigned koodipunkt){if(Olek_pilt){if((koodipunkt&192)!=128){Olek_järjekord+=koodipunkt>=196?2:1;}if(Olek_järjekord>=COLUMNS)return;}if(사용량==(int)sizeof(näitaja_andmed))출력비우기();näitaja_andmed[사용량++]=koodipunkt;}
static void 글내보내기(const char *string_andmed){while(*string_andmed)bait_andmed((unsigned char)*string_andmed++);}
static void 수치(unsigned kaup_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+kaup_COUNT%10;kaup_COUNT/=10;}while(kaup_COUNT);while(순번)bait_andmed(SECOND_VALUE[--순번]);}
static void liigutama_VALUE(int ROW_ametikoht,int veerg_ametikoht){글내보내기("\033[");수치(ROW_ametikoht);bait_andmed(';');수치(veerg_ametikoht);bait_andmed('H');}
static int 이전항목(int andmed_ametikoht){if(andmed_ametikoht){andmed_ametikoht--;while(andmed_ametikoht>0&&(Tekst[andmed_ametikoht]&192)==128)andmed_ametikoht--;}return andmed_ametikoht;}
static int Edasi_kaup(int andmed_ametikoht){if(andmed_ametikoht<길이){andmed_ametikoht++;while(andmed_ametikoht<길이&&(Tekst[andmed_ametikoht]&192)==128)andmed_ametikoht++;}return andmed_ametikoht;}
static int Käivita_2(int andmed_ametikoht){while(andmed_ametikoht>0&&Tekst[andmed_ametikoht-1]!='\n')andmed_ametikoht--;return andmed_ametikoht;}
static int lõpeta_kõne_nihe(int andmed_ametikoht){while(andmed_ametikoht<길이&&Tekst[andmed_ametikoht]!='\n')andmed_ametikoht++;return andmed_ametikoht;}
static int 너비(unsigned koodipunkt){return koodipunkt>=196?2:1;}
static int veerg(int andmed_ametikoht){int koodipunkt=0;for(int 순번=Käivita_2(andmed_ametikoht);순번<andmed_ametikoht;순번=Edasi_kaup(순번))koodipunkt+=Tekst[순번]=='\t'?4-koodipunkt%4:너비(Tekst[순번]);return koodipunkt;}
static void kontrollpunkt(void){for(int 순번=0;순번<길이;순번++)tagasi_võtma_andmed[순번]=Tekst[순번];되돌림길이=길이;위쪽=INDEX_VALUE;tagasi_võtma_Muudatused=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){kontrollpunkt();for(int 순번=도착위치;순번<길이;순번++)Tekst[출발위치+순번-도착위치]=Tekst[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int Lisa_VALUE(const unsigned char *string_andmed,int kaup_COUNT){if(kaup_COUNT>korrektor_võimsus-길이){teatamine_SMS="File full (16384 bytes)";return 0;}kontrollpunkt();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)Tekst[순번+kaup_COUNT]=Tekst[순번];for(int 순번=0;순번<kaup_COUNT;순번++)Tekst[INDEX_VALUE+순번]=string_andmed[순번];길이+=kaup_COUNT;INDEX_VALUE+=kaup_COUNT;변경됨=1;return 1;}
static void vertikaal(int 차이){int veerg_ametikoht=veerg(INDEX_VALUE),andmed_ametikoht=Käivita_2(INDEX_VALUE);if(차이<0){if(!andmed_ametikoht)return;andmed_ametikoht=Käivita_2(andmed_ametikoht-1);}else{andmed_ametikoht=lõpeta_kõne_nihe(andmed_ametikoht);if(andmed_ametikoht==길이)return;andmed_ametikoht++;}int koodipunkt=0;while(andmed_ametikoht<길이&&Tekst[andmed_ametikoht]!='\n'&&koodipunkt<veerg_ametikoht){koodipunkt+=Tekst[andmed_ametikoht]=='\t'?4-koodipunkt%4:너비(Tekst[andmed_ametikoht]);andmed_ametikoht=Edasi_kaup(andmed_ametikoht);}INDEX_VALUE=andmed_ametikoht;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=Käivita_2(INDEX_VALUE);맨위=Käivita_2(맨위);
    int ROW_ametikoht=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')ROW_ametikoht++;
    while(ROW_ametikoht>=ROW_COUNT-1){맨위=lõpeta_kõne_nihe(맨위);if(맨위<길이)맨위++;ROW_ametikoht--;}
    int veerg_ametikoht=veerg(INDEX_VALUE);if(veerg_ametikoht<왼쪽)왼쪽=veerg_ametikoht;if(veerg_ametikoht-왼쪽>=COLUMNS-1)왼쪽=veerg_ametikoht-COLUMNS+2;
    글내보내기("\033[?25l");int andmed_ametikoht=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        liigutama_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int koodipunkt=0,그려진상태=0;
        if(andmed_ametikoht>=길이&&반환값>ROW_ametikoht){글내보내기("\033[90m~\033[0m");continue;}
        while(andmed_ametikoht<길이&&Tekst[andmed_ametikoht]!='\n'){
            int Edasi_nihe=Edasi_kaup(andmed_ametikoht),너비값=Tekst[andmed_ametikoht]=='\t'?4-koodipunkt%4:너비(Tekst[andmed_ametikoht]);
            if(koodipunkt>=왼쪽&&koodipunkt-왼쪽+너비값<COLUMNS){
                if(Tekst[andmed_ametikoht]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bait_andmed(' ');}else if(Tekst[andmed_ametikoht]<32||Tekst[andmed_ametikoht]==127){bait_andmed('?');}else for(int 안쪽순번=andmed_ametikoht;안쪽순번<Edasi_nihe;안쪽순번++)bait_andmed(Tekst[안쪽순번]);그려진상태+=너비값;
            }koodipunkt+=너비값;andmed_ametikoht=Edasi_nihe;
        }
        (void)그려진상태;if(andmed_ametikoht<길이)andmed_ametikoht++;
    }
    liigutama_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");Olek_pilt=1;Olek_järjekord=0;글내보내기(Lisa_8e07c86f?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Fail_kirje_nimetus[이름바이트수]&&이름바이트수<30)bait_andmed(Fail_kirje_nimetus[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Joon=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Tekst[순번]=='\n')Joon++;수치(Joon);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(teatamine_SMS){int kaup_COUNT=0;글내보내기(" | ");while(teatamine_SMS[kaup_COUNT]&&kaup_COUNT<20)bait_andmed(teatamine_SMS[kaup_COUNT++]);}
    Olek_pilt=0;글내보내기("\033[0m");liigutama_VALUE(ROW_ametikoht+1,veerg_ametikoht-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(ootel_Võti){int 셋째순번=ootel_Võti;ootel_Võti=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Suurus=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Suurus&65535)||ROW_COUNT!=(int)(Suurus>>16)){
            COLUMNS=Suurus&65535;ROW_COUNT=Suurus>>16;화면그리기();
            if(spikker_ala){liigutama_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bait_andmed(spikker_ala);글내보내기(Käsk);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned tähtaja_piires_ametikoht=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-tähtaja_piires_ametikoht<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){ootel_Võti=셋째순번;return 27;}
    int kaup_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){kaup_COUNT=kaup_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return kaup_COUNT==3?1007:kaup_COUNT==5?1008:kaup_COUNT==6?1009:kaup_COUNT==1?1005:kaup_COUNT==4?1006:27;return 27;}return 27;
}
static int salv_VALUE(void){
    int Fail_pide=avama_Fail(Fail_kirje_nimetus,읽고쓰기|없으면만들기|lühendama_Sisu,0600);if(Fail_pide<0){teatamine_SMS="Cannot open for save";return 0;}
    intptr_t kaup_COUNT=kirjutamine_Fail_andmed(Fail_pide,Tekst,길이);Sule_Fail(Fail_pide);if(kaup_COUNT!=길이){teatamine_SMS="Write failed";return 0;}변경됨=0;teatamine_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Edasi(void){int kaup_COUNT=0;while(FIND_kirje[kaup_COUNT])kaup_COUNT++;if(!kaup_COUNT){teatamine_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int andmed_ametikoht=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<kaup_COUNT&&andmed_ametikoht+안쪽순번<길이&&Tekst[andmed_ametikoht+안쪽순번]==(unsigned char)FIND_kirje[안쪽순번])안쪽순번++;if(안쪽순번==kaup_COUNT){INDEX_VALUE=andmed_ametikoht;teatamine_SMS="Match";return;}}teatamine_SMS="Pattern not found";}
static int viip(int ala_VALUE){
    int kaup_COUNT=0;Käsk[0]=0;
    for(;;){liigutama_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bait_andmed(ala_VALUE);글내보내기(Käsk);출력비우기();spikker_ala=ala_VALUE;int 셋째순번=누름값();spikker_ala=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(kaup_COUNT){kaup_COUNT--;while(kaup_COUNT>0&&((unsigned char)Käsk[kaup_COUNT]&192)==128)kaup_COUNT--;Käsk[kaup_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&kaup_COUNT<120){Käsk[kaup_COUNT++]=셋째순번;Käsk[kaup_COUNT]=0;}
    }
    if(ala_VALUE=='/'){for(int 순번=0;순번<=kaup_COUNT;순번++)FIND_kirje[순번]=Käsk[순번];FIND_Edasi();return 0;}
    if(같은지(Käsk,"q!"))return 1;
    if(같은지(Käsk,"q")){if(!변경됨)return 1;teatamine_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Käsk,"wq")||같은지(Käsk,"x"))return salv_VALUE();
    if(같은지(Käsk,"w")){salv_VALUE();return 0;}
    if(Käsk[0]=='w'&&Käsk[1]==' '){int 순번=2;while(Käsk[순번]==' ')순번++;int Suurus=kaup_COUNT-순번;if(Suurus<1||Suurus>63){teatamine_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Suurus;안쪽순번++)Fail_kirje_nimetus[안쪽순번]=Käsk[순번+안쪽순번];Fail_kirje_nimetus[Suurus]=0;salv_VALUE();return 0;}
    int Joon=0;for(int 순번=0;순번<kaup_COUNT;순번++){if(Käsk[순번]<'0'||Käsk[순번]>'9'){Joon=0;break;}Joon=Joon*10+Käsk[순번]-'0';if(Joon>16384){Joon=0;break;}}
    if(Joon){INDEX_VALUE=0;while(--Joon&&INDEX_VALUE<길이){INDEX_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    teatamine_SMS="Unknown vi command";return 0;
}
int START_kasutaja_programm(int 무시값){
    (void)무시값;if(kasutaja_argument_COUNT()!=1||kasutaja_argument(0,Fail_kirje_nimetus,sizeof(Fail_kirje_nimetus))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Fail_pide=avama_Fail(Fail_kirje_nimetus,kirjutuskaitstud_VALUE,0);
    if(Fail_pide>=0){int kaup_COUNT=faili_maht(Fail_pide);if(kaup_COUNT<0||kaup_COUNT>korrektor_võimsus){Sule_Fail(Fail_pide);return 1;}길이=파일자료읽기(Fail_pide,Tekst,kaup_COUNT);Sule_Fail(Fail_pide);if(길이!=kaup_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!Tekst[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(tõrke_number!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,välju_programm=0;
    while(!välju_programm){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();teatamine_SMS=0;
        if(셋째순번==1001){vertikaal(-1);continue;}if(셋째순번==1002){vertikaal(1);continue;}if(셋째순번==1003){INDEX_VALUE=Edasi_kaup(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Käivita_2(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)vertikaal(셋째순번==1008?-1:1);continue;}
        if(Lisa_8e07c86f){
            if(셋째순번==27||셋째순번==3){Lisa_8e07c86f=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Edasi_kaup(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int kaup_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!kaup_COUNT){teatamine_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<kaup_COUNT;순번++){int koodipunkt=누름값();if(koodipunkt<128||koodipunkt>191){ootel_Võti=koodipunkt;유효함=0;break;}SECOND_VALUE[순번]=koodipunkt;}
                if(유효함)Lisa_VALUE(SECOND_VALUE,kaup_COUNT);
            }continue;
        }
        if(앞부분){int andmed_ametikoht=앞부분;앞부분=0;if(andmed_ametikoht=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(andmed_ametikoht=='Z'&&셋째순번=='Z'){välju_programm=salv_VALUE();continue;}if((andmed_ametikoht=='d'&&셋째순번=='d')||(andmed_ametikoht=='y'&&셋째순번=='y')){int 첫째값=Käivita_2(INDEX_VALUE),SECOND_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=Tekst[첫째값+순번];if(andmed_ametikoht=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Lisa_8e07c86f=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<lõpeta_kõne_nihe(INDEX_VALUE))INDEX_VALUE=Edasi_kaup(INDEX_VALUE);Lisa_8e07c86f=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Käivita_2(INDEX_VALUE);Lisa_8e07c86f=1;continue;}if(셋째순번=='A'){INDEX_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);Lisa_8e07c86f=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char liin_lõpeta_kõne='\n';INDEX_VALUE=셋째순번=='o'?lõpeta_kõne_nihe(INDEX_VALUE):Käivita_2(INDEX_VALUE);if(Lisa_VALUE(&liin_lõpeta_kõne,1)){if(셋째순번=='O')INDEX_VALUE--;Lisa_8e07c86f=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Edasi_kaup(INDEX_VALUE);continue;}if(셋째순번=='j'){vertikaal(1);continue;}if(셋째순번=='k'){vertikaal(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Käivita_2(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Käivita_2(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Edasi_kaup(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=lõpeta_kõne_nihe(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;Lisa_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<korrektor_võimsus;순번++){unsigned char SECOND_VALUE=Tekst[순번];Tekst[순번]=tagasi_võtma_andmed[순번];tagasi_võtma_andmed[순번]=SECOND_VALUE;}int kaup_COUNT=길이;길이=되돌림길이;되돌림길이=kaup_COUNT;kaup_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=kaup_COUNT;kaup_COUNT=변경됨;변경됨=tagasi_võtma_Muudatused;tagasi_võtma_Muudatused=kaup_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){välju_programm=viip(셋째순번);continue;}if(셋째순번=='n'){FIND_Edasi();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
