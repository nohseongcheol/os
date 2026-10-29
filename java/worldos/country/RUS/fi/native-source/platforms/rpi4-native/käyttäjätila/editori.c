/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "호출.h"
#include "파일규약.h"
#define editori_kapasiteetti 16384
static unsigned char teksti[editori_kapasiteetti],kumota_data[editori_kapasiteetti],복사자료[editori_kapasiteetti],KR_data[1024];
static int kesto_ARVO,INDEKSI_ARVO,맨위,왼쪽,변경됨,Lisää,kumota_kesto,위쪽,kumota_Muutokset,되돌림있음,kopioida_kesto,사용량,SARAKKEET=68,RIVI_LASKE=19;
static char Tiedosto_merkintä_nimi[64],komento[128],ETSI_merkintä[128];
static const char *알림문="NORMAL  i:insert  :w:save  :q:quit";
static unsigned Odottaa_Avain;
static int ohje_alue,Tila_KUVA,Tila_jono;
static void 출력비우기(void){if(사용량){사용자호출(1,1,(uintptr_t)KR_data,사용량,0,0,0);사용량=0;}}
static void tavu_data(unsigned merkkikoodi){if(Tila_KUVA){if((merkkikoodi&192)!=128){Tila_jono+=merkkikoodi>=196?2:1;}if(Tila_jono>=SARAKKEET)return;}if(사용량==(int)sizeof(KR_data))출력비우기();KR_data[사용량++]=merkkikoodi;}
static void 글내보내기(const char *merkkijono_data){while(*merkkijono_data)tavu_data((unsigned char)*merkkijono_data++);}
static void 수치(unsigned kohde_LASKE){char SEKUNNIT_ARVO[12];int 순번=0;do{SEKUNNIT_ARVO[순번++]='0'+kohde_LASKE%10;kohde_LASKE/=10;}while(kohde_LASKE);while(순번)tavu_data(SEKUNNIT_ARVO[--순번]);}
static void siirrä_ARVO_83b651b8(int RIVI_toimi,int SARAKE_toimi){글내보내기("\033[");수치(RIVI_toimi);tavu_data(';');수치(SARAKE_toimi);tavu_data('H');}
static int Edellinen(int data_toimi){if(data_toimi){data_toimi--;while(data_toimi>0&&(teksti[data_toimi]&192)==128)data_toimi--;}return data_toimi;}
static int Seuraava_kohde(int data_toimi){if(data_toimi<kesto_ARVO){data_toimi++;while(data_toimi<kesto_ARVO&&(teksti[data_toimi]&192)==128)data_toimi++;}return data_toimi;}
static int Suorita_2(int data_toimi){while(data_toimi>0&&teksti[data_toimi-1]!='\n')data_toimi--;return data_toimi;}
static int lopettaa_puhelu_SIIRTYMÄ(int data_toimi){while(data_toimi<kesto_ARVO&&teksti[data_toimi]!='\n')data_toimi++;return data_toimi;}
static int 너비(unsigned merkkikoodi){return merkkikoodi>=196?2:1;}
static int SARAKE(int data_toimi){int merkkikoodi=0;for(int 순번=Suorita_2(data_toimi);순번<data_toimi;순번=Seuraava_kohde(순번))merkkikoodi+=teksti[순번]=='\t'?4-merkkikoodi%4:너비(teksti[순번]);return merkkikoodi;}
static void tarkistuspiste(void){for(int 순번=0;순번<kesto_ARVO;순번++)kumota_data[순번]=teksti[순번];kumota_kesto=kesto_ARVO;위쪽=INDEKSI_ARVO;kumota_Muutokset=변경됨;되돌림있음=1;}
static void 바이트지우기(int 출발위치,int 도착위치){tarkistuspiste();for(int 순번=도착위치;순번<kesto_ARVO;순번++)teksti[출발위치+순번-도착위치]=teksti[순번];kesto_ARVO-=도착위치-출발위치;INDEKSI_ARVO=출발위치;변경됨=1;}
static int liitä_ARVO(const unsigned char *merkkijono_data,int kohde_LASKE){if(kohde_LASKE>editori_kapasiteetti-kesto_ARVO){알림문="File full (16384 bytes)";return 0;}tarkistuspiste();for(int 순번=kesto_ARVO-1;순번>=INDEKSI_ARVO;순번--)teksti[순번+kohde_LASKE]=teksti[순번];for(int 순번=0;순번<kohde_LASKE;순번++)teksti[INDEKSI_ARVO+순번]=merkkijono_data[순번];kesto_ARVO+=kohde_LASKE;INDEKSI_ARVO+=kohde_LASKE;변경됨=1;return 1;}
static void toimiala(int 차이){int SARAKE_toimi=SARAKE(INDEKSI_ARVO),data_toimi=Suorita_2(INDEKSI_ARVO);if(차이<0){if(!data_toimi)return;data_toimi=Suorita_2(data_toimi-1);}else{data_toimi=lopettaa_puhelu_SIIRTYMÄ(data_toimi);if(data_toimi==kesto_ARVO)return;data_toimi++;}int merkkikoodi=0;while(data_toimi<kesto_ARVO&&teksti[data_toimi]!='\n'&&merkkikoodi<SARAKE_toimi){merkkikoodi+=teksti[data_toimi]=='\t'?4-merkkikoodi%4:너비(teksti[data_toimi]);data_toimi=Seuraava_kohde(data_toimi);}INDEKSI_ARVO=data_toimi;}
static void 화면그리기(void){
    if(INDEKSI_ARVO>kesto_ARVO)INDEKSI_ARVO=kesto_ARVO;if(맨위>INDEKSI_ARVO)맨위=Suorita_2(INDEKSI_ARVO);맨위=Suorita_2(맨위);
    int RIVI_toimi=0;for(int 순번=맨위;순번<INDEKSI_ARVO;순번++)if(teksti[순번]=='\n')RIVI_toimi++;
    while(RIVI_toimi>=RIVI_LASKE-1){맨위=lopettaa_puhelu_SIIRTYMÄ(맨위);if(맨위<kesto_ARVO)맨위++;RIVI_toimi--;}
    int SARAKE_toimi=SARAKE(INDEKSI_ARVO);if(SARAKE_toimi<왼쪽)왼쪽=SARAKE_toimi;if(SARAKE_toimi-왼쪽>=SARAKKEET-1)왼쪽=SARAKE_toimi-SARAKKEET+2;
    글내보내기("\033[?25l");int data_toimi=맨위;
    for(int 반환값=0;반환값<RIVI_LASKE-1;반환값++){
        siirrä_ARVO_83b651b8(반환값+1,1);글내보내기("\033[0m\033[2K");int merkkikoodi=0,그려진상태=0;
        if(data_toimi>=kesto_ARVO&&반환값>RIVI_toimi){글내보내기("\033[90m~\033[0m");continue;}
        while(data_toimi<kesto_ARVO&&teksti[data_toimi]!='\n'){
            int Seuraava_SIIRTYMÄ=Seuraava_kohde(data_toimi),너비값=teksti[data_toimi]=='\t'?4-merkkikoodi%4:너비(teksti[data_toimi]);
            if(merkkikoodi>=왼쪽&&merkkikoodi-왼쪽+너비값<SARAKKEET){
                if(teksti[data_toimi]=='\t'){for(int 안쪽순번=0;안쪽순번<너비값;안쪽순번++)tavu_data(' ');}else if(teksti[data_toimi]<32||teksti[data_toimi]==127){tavu_data('?');}else for(int 안쪽순번=data_toimi;안쪽순번<Seuraava_SIIRTYMÄ;안쪽순번++)tavu_data(teksti[안쪽순번]);그려진상태+=너비값;
            }merkkikoodi+=너비값;data_toimi=Seuraava_SIIRTYMÄ;
        }
        (void)그려진상태;if(data_toimi<kesto_ARVO)data_toimi++;
    }
    siirrä_ARVO_83b651b8(RIVI_LASKE,1);글내보내기("\033[7m\033[2K");Tila_KUVA=1;Tila_jono=0;글내보내기(Lisää?"INSERT ":"NORMAL ");
    int 이름바이트수=0;while(Tiedosto_merkintä_nimi[이름바이트수]&&이름바이트수<30)tavu_data(Tiedosto_merkintä_nimi[이름바이트수++]);글내보내기(변경됨?" [+] ":" ");
    글내보내기("L");int syöterivi=1;for(int 순번=0;순번<INDEKSI_ARVO;순번++)if(teksti[순번]=='\n')syöterivi++;수치(syöterivi);글내보내기(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(알림문){int kohde_LASKE=0;글내보내기(" | ");while(알림문[kohde_LASKE]&&kohde_LASKE<20)tavu_data(알림문[kohde_LASKE++]);}
    Tila_KUVA=0;글내보내기("\033[0m");siirrä_ARVO_83b651b8(RIVI_toimi+1,SARAKE_toimi-왼쪽+1);글내보내기("\033[?25h");출력비우기();
}
static int 누름값(void){
    if(Odottaa_Avain){int 셋째순번=Odottaa_Avain;Odottaa_Avain=0;return 셋째순번;}
    for(;;){
        int 셋째순번=사용자호출(16,1,0,0,0,0,0);
        unsigned Koko=사용자호출(16,3,0,0,0,0,0);
        if(SARAKKEET!=(int)(Koko&65535)||RIVI_LASKE!=(int)(Koko>>16)){
            SARAKKEET=Koko&65535;RIVI_LASKE=Koko>>16;화면그리기();
            if(ohje_alue){siirrä_ARVO_83b651b8(RIVI_LASKE,1);글내보내기("\033[0m\033[2K");tavu_data(ohje_alue);글내보내기(komento);출력비우기();}
        }
        if(셋째순번>=0)return 셋째순번;
    }
}
static int 탈출됨(void){
    unsigned nykyinen_toimi=사용자호출(7,0,0,0,0,0,0);int 셋째순번=-1;
    while((unsigned)사용자호출(7,0,0,0,0,0,0)-nykyinen_toimi<100){셋째순번=사용자호출(16,1,0,0,0,0,0);if(셋째순번>=0)break;}
    if(셋째순번<0)return 27;if(셋째순번!='['&&셋째순번!='O'){Odottaa_Avain=셋째순번;return 27;}
    int kohde_LASKE=0;for(int 순번=0;순번<12;순번++){셋째순번=누름값();if(셋째순번>='0'&&셋째순번<='9'){kohde_LASKE=kohde_LASKE*10+셋째순번-'0';continue;}if(셋째순번=='A')return 1001;if(셋째순번=='B')return 1002;if(셋째순번=='C')return 1003;if(셋째순번=='D')return 1004;if(셋째순번=='H')return 1005;if(셋째순번=='F')return 1006;if(셋째순번=='~')return kohde_LASKE==3?1007:kohde_LASKE==5?1008:kohde_LASKE==6?1009:kohde_LASKE==1?1005:kohde_LASKE==4?1006:27;return 27;}return 27;
}
static int Store_ARVO(void){
    int Tiedosto_kahva=avata_Tiedosto(Tiedosto_merkintä_nimi,luku_ja_kirjoitus|없으면만들기|내용비우기,0600);if(Tiedosto_kahva<0){알림문="Cannot open for save";return 0;}
    intptr_t kohde_LASKE=kirjoitus_Tiedosto_data(Tiedosto_kahva,teksti,kesto_ARVO);Sulje_Tiedosto(Tiedosto_kahva);if(kohde_LASKE!=kesto_ARVO){알림문="Write failed";return 0;}변경됨=0;알림문="Saved (RAM)";return 1;
}
static int 같은지(const char *첫째값,const char *SEKUNNIT_ARVO){while(*첫째값&&*첫째값==*SEKUNNIT_ARVO){첫째값++;SEKUNNIT_ARVO++;}return *첫째값==*SEKUNNIT_ARVO;}
static void ETSI_Seuraava(void){int kohde_LASKE=0;while(ETSI_merkintä[kohde_LASKE])kohde_LASKE++;if(!kohde_LASKE){알림문="No search pattern";return;}for(int 순번=1;순번<=kesto_ARVO;순번++){int data_toimi=(INDEKSI_ARVO+순번)%(kesto_ARVO?kesto_ARVO:1),안쪽순번=0;while(안쪽순번<kohde_LASKE&&data_toimi+안쪽순번<kesto_ARVO&&teksti[data_toimi+안쪽순번]==(unsigned char)ETSI_merkintä[안쪽순번])안쪽순번++;if(안쪽순번==kohde_LASKE){INDEKSI_ARVO=data_toimi;알림문="Match";return;}}알림문="Pattern not found";}
static int kehote(int alue_ARVO){
    int kohde_LASKE=0;komento[0]=0;
    for(;;){siirrä_ARVO_83b651b8(RIVI_LASKE,1);글내보내기("\033[0m\033[2K");tavu_data(alue_ARVO);글내보내기(komento);출력비우기();ohje_alue=alue_ARVO;int 셋째순번=누름값();ohje_alue=0;
        if(셋째순번==27||셋째순번==3)return 0;if(셋째순번==13||셋째순번==10)break;
        if(셋째순번==127||셋째순번==8){if(kohde_LASKE){kohde_LASKE--;while(kohde_LASKE>0&&((unsigned char)komento[kohde_LASKE]&192)==128)kohde_LASKE--;komento[kohde_LASKE]=0;}continue;}
        if(셋째순번>=32&&셋째순번<256&&kohde_LASKE<120){komento[kohde_LASKE++]=셋째순번;komento[kohde_LASKE]=0;}
    }
    if(alue_ARVO=='/'){for(int 순번=0;순번<=kohde_LASKE;순번++)ETSI_merkintä[순번]=komento[순번];ETSI_Seuraava();return 0;}
    if(같은지(komento,"q!"))return 1;
    if(같은지(komento,"q")){if(!변경됨)return 1;알림문="Unsaved: :w or :q!";return 0;}
    if(같은지(komento,"wq")||같은지(komento,"x"))return Store_ARVO();
    if(같은지(komento,"w")){Store_ARVO();return 0;}
    if(komento[0]=='w'&&komento[1]==' '){int 순번=2;while(komento[순번]==' ')순번++;int Koko=kohde_LASKE-순번;if(Koko<1||Koko>63){알림문="Invalid file name";return 0;}for(int 안쪽순번=0;안쪽순번<Koko;안쪽순번++)Tiedosto_merkintä_nimi[안쪽순번]=komento[순번+안쪽순번];Tiedosto_merkintä_nimi[Koko]=0;Store_ARVO();return 0;}
    int syöterivi=0;for(int 순번=0;순번<kohde_LASKE;순번++){if(komento[순번]<'0'||komento[순번]>'9'){syöterivi=0;break;}syöterivi=syöterivi*10+komento[순번]-'0';if(syöterivi>16384){syöterivi=0;break;}}
    if(syöterivi){INDEKSI_ARVO=0;while(--syöterivi&&INDEKSI_ARVO<kesto_ARVO){INDEKSI_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);if(INDEKSI_ARVO<kesto_ARVO)INDEKSI_ARVO++;}return 0;}
    알림문="Unknown vi command";return 0;
}
int alku_käyttäjä_ohjelma(int 무시값){
    (void)무시값;if(käyttäjä_argumentti_LASKE()!=1||käyttäjä_argumentti(0,Tiedosto_merkintä_nimi,sizeof(Tiedosto_merkintä_nimi))<0){글내보내기("Usage: vi FILE\n");출력비우기();return 2;}
    int Tiedosto_kahva=avata_Tiedosto(Tiedosto_merkintä_nimi,vain_luku_ARVO,0);
    if(Tiedosto_kahva>=0){int kohde_LASKE=tiedostokoko(Tiedosto_kahva);if(kohde_LASKE<0||kohde_LASKE>editori_kapasiteetti){Sulje_Tiedosto(Tiedosto_kahva);return 1;}kesto_ARVO=lukea_Tiedosto_data(Tiedosto_kahva,teksti,kohde_LASKE);Sulje_Tiedosto(Tiedosto_kahva);if(kesto_ARVO!=kohde_LASKE)return 1;for(int 순번=0;순번<kesto_ARVO;순번++)if(!teksti[순번]){글내보내기("vi: NUL byte in text file\n");출력비우기();return 1;}}
    else if(virhenumero!=2){글내보내기("vi: cannot read file\n");출력비우기();return 1;}
    int 흐린색=사용자호출(16,0,0,0,0,0,0);if(흐린색<0){글내보내기("vi: use a standalone interactive command\n");출력비우기();return 1;}SARAKKEET=흐린색&65535;RIVI_LASKE=(unsigned)흐린색>>16;
    글내보내기("\033[2J\033[H");출력비우기();
    int 앞부분=0,lopeta_ohjelma=0;
    while(!lopeta_ohjelma){화면그리기();int 셋째순번=누름값();if(셋째순번==27)셋째순번=탈출됨();알림문=0;
        if(셋째순번==1001){toimiala(-1);continue;}if(셋째순번==1002){toimiala(1);continue;}if(셋째순번==1003){INDEKSI_ARVO=Seuraava_kohde(INDEKSI_ARVO);continue;}if(셋째순번==1004){INDEKSI_ARVO=Edellinen(INDEKSI_ARVO);continue;}
        if(셋째순번==1005){INDEKSI_ARVO=Suorita_2(INDEKSI_ARVO);continue;}if(셋째순번==1006){INDEKSI_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);continue;}
        if(셋째순번==1008||셋째순번==1009){for(int 순번=0;순번<RIVI_LASKE-2;순번++)toimiala(셋째순번==1008?-1:1);continue;}
        if(Lisää){
            if(셋째순번==27||셋째순번==3){Lisää=0;continue;}
            if(셋째순번==127||셋째순번==8){if(INDEKSI_ARVO)바이트지우기(Edellinen(INDEKSI_ARVO),INDEKSI_ARVO);continue;}
            if(셋째순번==1007){if(INDEKSI_ARVO<kesto_ARVO)바이트지우기(INDEKSI_ARVO,Seuraava_kohde(INDEKSI_ARVO));continue;}
            if(셋째순번==13)셋째순번=10;if(셋째순번==10||셋째순번==9||(셋째순번>=32&&셋째순번<256)){
                unsigned char SEKUNNIT_ARVO[4];SEKUNNIT_ARVO[0]=셋째순번;int kohde_LASKE=셋째순번<128?1:셋째순번>=0xc2&&셋째순번<0xe0?2:셋째순번<0xf0?3:셋째순번<=0xf4?4:0;
                if(!kohde_LASKE){알림문="Invalid UTF-8";continue;}int kelvollinen=1;for(int 순번=1;순번<kohde_LASKE;순번++){int merkkikoodi=누름값();if(merkkikoodi<128||merkkikoodi>191){Odottaa_Avain=merkkikoodi;kelvollinen=0;break;}SEKUNNIT_ARVO[순번]=merkkikoodi;}
                if(kelvollinen)liitä_ARVO(SEKUNNIT_ARVO,kohde_LASKE);
            }continue;
        }
        if(앞부분){int data_toimi=앞부분;앞부분=0;if(data_toimi=='g'&&셋째순번=='g'){INDEKSI_ARVO=0;continue;}if(data_toimi=='Z'&&셋째순번=='Z'){lopeta_ohjelma=Store_ARVO();continue;}if((data_toimi=='d'&&셋째순번=='d')||(data_toimi=='y'&&셋째순번=='y')){int 첫째값=Suorita_2(INDEKSI_ARVO),SEKUNNIT_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);if(SEKUNNIT_ARVO<kesto_ARVO)SEKUNNIT_ARVO++;kopioida_kesto=SEKUNNIT_ARVO-첫째값;for(int 순번=0;순번<kopioida_kesto;순번++)복사자료[순번]=teksti[첫째값+순번];if(data_toimi=='d')바이트지우기(첫째값,SEKUNNIT_ARVO);continue;}}
        if(셋째순번=='i'){Lisää=1;continue;}if(셋째순번=='a'){if(INDEKSI_ARVO<lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO))INDEKSI_ARVO=Seuraava_kohde(INDEKSI_ARVO);Lisää=1;continue;}
        if(셋째순번=='I'){INDEKSI_ARVO=Suorita_2(INDEKSI_ARVO);Lisää=1;continue;}if(셋째순번=='A'){INDEKSI_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);Lisää=1;continue;}
        if(셋째순번=='o'||셋째순번=='O'){unsigned char rivi_lopettaa_puhelu='\n';INDEKSI_ARVO=셋째순번=='o'?lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO):Suorita_2(INDEKSI_ARVO);if(liitä_ARVO(&rivi_lopettaa_puhelu,1)){if(셋째순번=='O')INDEKSI_ARVO--;Lisää=1;}continue;}
        if(셋째순번=='h'){INDEKSI_ARVO=Edellinen(INDEKSI_ARVO);continue;}if(셋째순번=='l'){INDEKSI_ARVO=Seuraava_kohde(INDEKSI_ARVO);continue;}if(셋째순번=='j'){toimiala(1);continue;}if(셋째순번=='k'){toimiala(-1);continue;}
        if(셋째순번=='0'){INDEKSI_ARVO=Suorita_2(INDEKSI_ARVO);continue;}if(셋째순번=='$'){INDEKSI_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);continue;}if(셋째순번=='G'){INDEKSI_ARVO=Suorita_2(kesto_ARVO);continue;}
        if(셋째순번=='g'||셋째순번=='d'||셋째순번=='y'||셋째순번=='Z'){앞부분=셋째순번;continue;}
        if(셋째순번=='x'||셋째순번==1007){if(INDEKSI_ARVO<kesto_ARVO)바이트지우기(INDEKSI_ARVO,Seuraava_kohde(INDEKSI_ARVO));continue;}
        if(셋째순번=='p'&&kopioida_kesto){INDEKSI_ARVO=lopettaa_puhelu_SIIRTYMÄ(INDEKSI_ARVO);if(INDEKSI_ARVO<kesto_ARVO)INDEKSI_ARVO++;liitä_ARVO(복사자료,kopioida_kesto);continue;}
        if(셋째순번=='u'&&되돌림있음){for(int 순번=0;순번<editori_kapasiteetti;순번++){unsigned char SEKUNNIT_ARVO=teksti[순번];teksti[순번]=kumota_data[순번];kumota_data[순번]=SEKUNNIT_ARVO;}int kohde_LASKE=kesto_ARVO;kesto_ARVO=kumota_kesto;kumota_kesto=kohde_LASKE;kohde_LASKE=INDEKSI_ARVO;INDEKSI_ARVO=위쪽;위쪽=kohde_LASKE;kohde_LASKE=변경됨;변경됨=kumota_Muutokset;kumota_Muutokset=kohde_LASKE;continue;}
        if(셋째순번==':'||셋째순번=='/'){lopeta_ohjelma=kehote(셋째순번);continue;}if(셋째순번=='n'){ETSI_Seuraava();continue;}
    }
    글내보내기("\033[0m\033[?25h\033[2J\033[H");출력비우기();사용자호출(16,2,0,0,0,0,0);return 0;
}
