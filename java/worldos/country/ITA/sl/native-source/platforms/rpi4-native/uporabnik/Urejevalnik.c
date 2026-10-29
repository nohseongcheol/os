/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define Urejevalnik_zmogljivost 16384
static unsigned char Besedilo[Urejevalnik_zmogljivost],razveljaviti_podatki[Urejevalnik_zmogljivost],복사자료[Urejevalnik_zmogljivost],KR_podatki[1024];
static int 길이,INDEX_VALUE,맨위,왼쪽,변경됨,Vstavljanje,되돌림길이,위쪽,razveljaviti_Spremembe,되돌림있음,복사길이,사용량,COLUMNS=68,ROW_COUNT=19;
static char Datoteka_vnos_ime[64],Ukaz[128],FIND_vnos[128];
static const char *obvestilo_SMS="NORMAL  i:insert  :w:save  :q:quit";
static unsigned čakajoče_Ključ;
static int spletna_pomoč_območje,stanje_IMAGE,stanje_čakalna_vrsta;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_podatki,사용량,0,0,0);사용량=0;}}
static void bajt_podatki(unsigned koda_znaka){if(stanje_IMAGE){if((koda_znaka&192)!=128){stanje_čakalna_vrsta+=koda_znaka>=196?2:1;}if(stanje_čakalna_vrsta>=COLUMNS)return;}if(사용량==(int)sizeof(KR_podatki))출력비우기();KR_podatki[사용량++]=koda_znaka;}
static void 글내보내기(const char *niz_podatki){while(*niz_podatki)bajt_podatki((unsigned char)*niz_podatki++);}
static void 수치(unsigned element_COUNT){char SECOND_VALUE[12];int 순번=0;do{SECOND_VALUE[순번++]='0'+element_COUNT%10;element_COUNT/=10;}while(element_COUNT);while(순번)bajt_podatki(SECOND_VALUE[--순번]);}
static void premikati_VALUE(int ROW_položaj,int COLUMN_položaj){글내보내기("\033[");수치(ROW_položaj);bajt_podatki(';');수치(COLUMN_položaj);bajt_podatki('H');}
static int 이전항목(int podatki_položaj){if(podatki_položaj){podatki_položaj--;while(podatki_položaj>0&&(Besedilo[podatki_položaj]&192)==128)podatki_položaj--;}return podatki_položaj;}
static int Naprej_element(int podatki_položaj){if(podatki_položaj<길이){podatki_položaj++;while(podatki_položaj<길이&&(Besedilo[podatki_položaj]&192)==128)podatki_položaj++;}return podatki_položaj;}
static int Zaženi(int podatki_položaj){while(podatki_položaj>0&&Besedilo[podatki_položaj-1]!='\n')podatki_položaj--;return podatki_položaj;}
static int končati_klic_odmik(int podatki_položaj){while(podatki_položaj<길이&&Besedilo[podatki_položaj]!='\n')podatki_položaj++;return podatki_položaj;}
static int 너비(unsigned koda_znaka){return koda_znaka>=196?2:1;}
static int COLUMN(int podatki_položaj){int koda_znaka=0;for(int 순번=Zaženi(podatki_položaj);순번<podatki_položaj;순번=Naprej_element(순번))koda_znaka+=Besedilo[순번]=='\t'?4-koda_znaka%4:너비(Besedilo[순번]);return koda_znaka;}
static void točka_preverjanja(void){for(int 순번=0;순번<길이;순번++)razveljaviti_podatki[순번]=Besedilo[순번];되돌림길이=길이;위쪽=INDEX_VALUE;razveljaviti_Spremembe=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){točka_preverjanja();for(int 순번=도착위치;순번<길이;순번++)Besedilo[출발위치+순번-도착위치]=Besedilo[순번];길이-=도착위치-출발위치;INDEX_VALUE=출발위치;변경됨=1;}
static int dodati_VALUE(const unsigned char *niz_podatki,int element_COUNT){if(element_COUNT>Urejevalnik_zmogljivost-길이){obvestilo_SMS="File full (16384 bytes)";return 0;}točka_preverjanja();for(int 순번=길이-1;순번>=INDEX_VALUE;순번--)Besedilo[순번+element_COUNT]=Besedilo[순번];for(int 순번=0;순번<element_COUNT;순번++)Besedilo[INDEX_VALUE+순번]=niz_podatki[순번];길이+=element_COUNT;INDEX_VALUE+=element_COUNT;변경됨=1;return 1;}
static void Navpično(int 차이){int COLUMN_položaj=COLUMN(INDEX_VALUE),podatki_položaj=Zaženi(INDEX_VALUE);if(차이<0){if(!podatki_položaj)return;podatki_položaj=Zaženi(podatki_položaj-1);}else{podatki_položaj=končati_klic_odmik(podatki_položaj);if(podatki_položaj==길이)return;podatki_položaj++;}int koda_znaka=0;while(podatki_položaj<길이&&Besedilo[podatki_položaj]!='\n'&&koda_znaka<COLUMN_položaj){koda_znaka+=Besedilo[podatki_položaj]=='\t'?4-koda_znaka%4:너비(Besedilo[podatki_položaj]);podatki_položaj=Naprej_element(podatki_položaj);}INDEX_VALUE=podatki_položaj;}
static void 화면그리기(void){
    if(INDEX_VALUE>길이)INDEX_VALUE=길이;if(맨위>INDEX_VALUE)맨위=Zaženi(INDEX_VALUE);맨위=Zaženi(맨위);
    int ROW_položaj=0;for(int 순번=맨위;순번<INDEX_VALUE;순번++)if(Besedilo[순번]=='\n')ROW_položaj++;
    while(ROW_položaj>=ROW_COUNT-1){맨위=končati_klic_odmik(맨위);if(맨위<길이)맨위++;ROW_položaj--;}
    int COLUMN_položaj=COLUMN(INDEX_VALUE);if(COLUMN_položaj<왼쪽)왼쪽=COLUMN_položaj;if(COLUMN_položaj-왼쪽>=COLUMNS-1)왼쪽=COLUMN_položaj-COLUMNS+2;
    글내보내기("\033[?25l");int podatki_položaj=맨위;
    for(int 반환값=0;반환값<ROW_COUNT-1;반환값++){
        premikati_VALUE(반환값+1,1);글내보내기("\033[0m\033[2K");int koda_znaka=0,그려진상태=0;
        if(podatki_položaj>=길이&&반환값>ROW_položaj){글내보내기("\033[90m~\033[0m");continue;}
        while(podatki_položaj<길이&&Besedilo[podatki_položaj]!='\n'){
            int Naprej_odmik=Naprej_element(podatki_položaj),너비값=Besedilo[podatki_položaj]=='\t'?4-koda_znaka%4:너비(Besedilo[podatki_položaj]);
            if(koda_znaka>=왼쪽&&koda_znaka-왼쪽+너비값<COLUMNS){
                if(Besedilo[podatki_položaj]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)bajt_podatki(' ');}else if(Besedilo[podatki_položaj]<32||Besedilo[podatki_položaj]==127){bajt_podatki('?');}else for(int 안쪽순번=podatki_položaj;안쪽순번<Naprej_odmik;안쪽순번++)bajt_podatki(Besedilo[안쪽순번]);그려진상태+=너비값;
            }koda_znaka+=너비값;podatki_položaj=Naprej_odmik;
        }
        (void)그려진상태;if(podatki_položaj<길이)podatki_položaj++;
    }
    premikati_VALUE(ROW_COUNT,1);글내보내기("\033[7m\033[2K");stanje_IMAGE=1;stanje_čakalna_vrsta=0;글내보내기(Vstavljanje?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Datoteka_vnos_ime[이름바이트수]&&이름바이트수<30)bajt_podatki(Datoteka_vnos_ime[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int Črtni=1;for(int 순번=0;순번<INDEX_VALUE;순번++)if(Besedilo[순번]=='\n')Črtni++;수치(Črtni);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(obvestilo_SMS){int element_COUNT=0;글내보내기(" | ");while(obvestilo_SMS[element_COUNT]&&element_COUNT<20)bajt_podatki(obvestilo_SMS[element_COUNT++]);}
    stanje_IMAGE=0;글내보내기("\033[0m");premikati_VALUE(ROW_položaj+1,COLUMN_položaj-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(čakajoče_Ključ){int 셋째순번=čakajoče_Ključ;čakajoče_Ključ=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Velikost=사용자호출(16,3,0,0,0,0,0);
        if(COLUMNS!=(int)(Velikost&65535)||ROW_COUNT!=(int)(Velikost>>16)){
            COLUMNS=Velikost&65535;ROW_COUNT=Velikost>>16;화면그리기();
            if(spletna_pomoč_območje){premikati_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podatki(spletna_pomoč_območje);글내보내기(Ukaz);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned sprotno_položaj=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-sprotno_položaj<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){čakajoče_Ključ=셋째순번;return 27;}
    int element_COUNT=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){element_COUNT=element_COUNT*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return element_COUNT==3?1007:element_COUNT==5?1008:element_COUNT==6?1009:element_COUNT==1?1005:element_COUNT==4?1006:27;return 27;}return 27;
}
static int Store_VALUE(void){
    int Datoteka_ročica=odprto_Datoteka(Datoteka_vnos_ime,branje_pisanje|없으면만들기|내용비우기,0600);if(Datoteka_ročica<0){obvestilo_SMS="Cannot open for save";return 0;}
    intptr_t element_COUNT=pisati_Datoteka_podatki(Datoteka_ročica,Besedilo,길이);Zapri_Datoteka(Datoteka_ročica);if(element_COUNT!=길이){obvestilo_SMS="Write failed";return 0;}변경됨=0;obvestilo_SMS="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SECOND_VALUE){while(*첫째값&&*첫째값==*SECOND_VALUE){첫째값++;SECOND_VALUE++;}return *첫째값==*SECOND_VALUE;}
static void FIND_Naprej(void){int element_COUNT=0;while(FIND_vnos[element_COUNT])element_COUNT++;if(!element_COUNT){obvestilo_SMS="No search pattern";return;}for(int 순번=1;순번<=길이;순번++){int podatki_položaj=(INDEX_VALUE+순번)%(길이?길이:1),안쪽순번=0;while(안쪽순번<element_COUNT&&podatki_položaj+안쪽순번<길이&&Besedilo[podatki_položaj+안쪽순번]==(unsigned char)FIND_vnos[안쪽순번])안쪽순번++;if(안쪽순번==element_COUNT){INDEX_VALUE=podatki_položaj;obvestilo_SMS="Match";return;}}obvestilo_SMS="Pattern not found";}
static int poziv(int območje_VALUE){
    int element_COUNT=0;Ukaz[0]=0;
    for(;;){premikati_VALUE(ROW_COUNT,1);글내보내기("\033[0m\033[2K");bajt_podatki(območje_VALUE);글내보내기(Ukaz);출력비우기();spletna_pomoč_območje=območje_VALUE;int 셋째순번=누름값();spletna_pomoč_območje=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(element_COUNT){element_COUNT--;while(element_COUNT>0&&((unsigned char)Ukaz[element_COUNT]&192)==128)element_COUNT--;Ukaz[element_COUNT]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&element_COUNT<120){Ukaz[element_COUNT++]=셋째순번;Ukaz[element_COUNT]=0;}
    }
    if(območje_VALUE=='/'){for(int 순번=0;순번<=element_COUNT;순번++)FIND_vnos[순번]=Ukaz[순번];FIND_Naprej();return 0;}
    if(같은지(Ukaz,"q!"))return 1;
    if(같은지(Ukaz,"q")){if(!변경됨)return 1;obvestilo_SMS="Unsaved: :w or :q!";return 0;}
    if(같은지(Ukaz,"wq")||같은지(Ukaz,"x"))return Store_VALUE();
    if(같은지(Ukaz,"w")){Store_VALUE();return 0;}
    if(Ukaz[0]=='w'&&Ukaz[1]==' '){int 순번=2;while(Ukaz[순번]==' ')순번++;int Velikost=element_COUNT-순번;if(Velikost<1||Velikost>63){obvestilo_SMS="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Velikost;안쪽순번++)Datoteka_vnos_ime[안쪽순번]=Ukaz[순번+안쪽순번];Datoteka_vnos_ime[Velikost]=0;Store_VALUE();return 0;}
    int Črtni=0;for(int 순번=0;순번<element_COUNT;순번++){if(Ukaz[순번]<'0'||Ukaz[순번]>'9'){Črtni=0;break;}Črtni=Črtni*10+Ukaz[순번]-'0';if(Črtni>16384){Črtni=0;break;}}
    if(Črtni){INDEX_VALUE=0;while(--Črtni&&INDEX_VALUE<길이){INDEX_VALUE=končati_klic_odmik(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;}return 0;}
    obvestilo_SMS="Unknown vi command";return 0;
}
int Start_uporabnik_aplikacija(int 무시값){
    (void)무시값;if(uporabnik_argument_COUNT()!=1||uporabnik_argument(0,Datoteka_vnos_ime,sizeof(Datoteka_vnos_ime))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Datoteka_ročica=odprto_Datoteka(Datoteka_vnos_ime,samo_za_branje_VALUE,0);
    if(Datoteka_ročica>=0){int element_COUNT=velikost_datoteke(Datoteka_ročica);if(element_COUNT<0||element_COUNT>Urejevalnik_zmogljivost){Zapri_Datoteka(Datoteka_ročica);return 1;}길이=파일자료읽기(Datoteka_ročica,Besedilo,element_COUNT);Zapri_Datoteka(Datoteka_ročica);if(길이!=element_COUNT)return 1;for(int 순번=0;순번<길이;순번++)if(!Besedilo[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(številka_napake!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}COLUMNS=흐린색&65535;ROW_COUNT=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,izhod_aplikacija=0;
    while(!izhod_aplikacija){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();obvestilo_SMS=0;
        if(셋째순번==1001){Navpično(-1);continue;}if(셋째순번==1002){Navpično(1);continue;}if(셋째순번==1003){INDEX_VALUE=Naprej_element(INDEX_VALUE);continue;}if(셋째순번==1004){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}
        if(셋째순번==1005){INDEX_VALUE=Zaženi(INDEX_VALUE);continue;}if(셋째순번==1006){INDEX_VALUE=končati_klic_odmik(INDEX_VALUE);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<ROW_COUNT-2;순번++)Navpično(셋째순번==1008?-1:1);continue;}
        if(Vstavljanje){
            if(셋째순번==27||셋째순번==3){Vstavljanje=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEX_VALUE)바이트지우기(이전항목(INDEX_VALUE),INDEX_VALUE);continue;}
            if(셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Naprej_element(INDEX_VALUE));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SECOND_VALUE[4];SECOND_VALUE[0]=셋째순번;int element_COUNT=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!element_COUNT){obvestilo_SMS="Invalid UTF-8";continue;}int 유효함=1;for(int 순번=1;순번<element_COUNT;순번++){int koda_znaka=누름값();if(koda_znaka<128||koda_znaka>191){čakajoče_Ključ=koda_znaka;유효함=0;break;}SECOND_VALUE[순번]=koda_znaka;}
                if(유효함)dodati_VALUE(SECOND_VALUE,element_COUNT);
            }continue;
        }
        if(앞부분){int podatki_položaj=앞부분;앞부분=0;if(podatki_položaj=='g'&&셋째순번=='g'){INDEX_VALUE=0;continue;}if(podatki_položaj=='Z'&&셋째순번=='Z'){izhod_aplikacija=Store_VALUE();continue;}if((podatki_položaj=='d'&&셋째순번=='d')||(podatki_položaj=='y'&&셋째순번=='y')){int 첫째값=Zaženi(INDEX_VALUE),SECOND_VALUE=končati_klic_odmik(INDEX_VALUE);if(SECOND_VALUE<길이)SECOND_VALUE++;복사길이=SECOND_VALUE-첫째값;for(int 순번=0;순번<복사길이;순번++)복사자료[순번]=Besedilo[첫째값+순번];if(podatki_položaj=='d')바이트지우기(첫째값,SECOND_VALUE);continue;}}
        if(셋째순번=='i'){Vstavljanje=1;continue;}if(셋째순번=='a'){if(INDEX_VALUE<končati_klic_odmik(INDEX_VALUE))INDEX_VALUE=Naprej_element(INDEX_VALUE);Vstavljanje=1;continue;}
        if(셋째순번=='I'){INDEX_VALUE=Zaženi(INDEX_VALUE);Vstavljanje=1;continue;}if(셋째순번=='A'){INDEX_VALUE=končati_klic_odmik(INDEX_VALUE);Vstavljanje=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char linija_končati_klic='\n';INDEX_VALUE=셋째순번=='o'?končati_klic_odmik(INDEX_VALUE):Zaženi(INDEX_VALUE);if(dodati_VALUE(&linija_končati_klic,1)){if(셋째순번=='O')INDEX_VALUE--;Vstavljanje=1;}continue;}
        if(셋째순번=='h'){INDEX_VALUE=이전항목(INDEX_VALUE);continue;}if(셋째순번=='l'){INDEX_VALUE=Naprej_element(INDEX_VALUE);continue;}if(셋째순번=='j'){Navpično(1);continue;}if(셋째순번=='k'){Navpično(-1);continue;}
        if(셋째순번=='0'){INDEX_VALUE=Zaženi(INDEX_VALUE);continue;}if(셋째순번=='$'){INDEX_VALUE=končati_klic_odmik(INDEX_VALUE);continue;}if(셋째순번=='G'){INDEX_VALUE=Zaženi(길이);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEX_VALUE<길이)바이트지우기(INDEX_VALUE,Naprej_element(INDEX_VALUE));continue;}
        if(셋째순번=='p'&&복사길이){INDEX_VALUE=končati_klic_odmik(INDEX_VALUE);if(INDEX_VALUE<길이)INDEX_VALUE++;dodati_VALUE(복사자료,복사길이);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<Urejevalnik_zmogljivost;순번++){unsigned char SECOND_VALUE=Besedilo[순번];Besedilo[순번]=razveljaviti_podatki[순번];razveljaviti_podatki[순번]=SECOND_VALUE;}int element_COUNT=길이;길이=되돌림길이;되돌림길이=element_COUNT;element_COUNT=INDEX_VALUE;INDEX_VALUE=위쪽;위쪽=element_COUNT;element_COUNT=변경됨;변경됨=razveljaviti_Spremembe;razveljaviti_Spremembe=element_COUNT;continue;}
        if(셋째순번==':'||셋째순번=='/'){izhod_aplikacija=poziv(셋째순번);continue;}if(셋째순번=='n'){FIND_Naprej();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
