// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skutočný_údaje jadro_VALUE 상태를 읽는 IPv4·ICMP·작업·Pamäť_VALUE·RAM odkladací_priestor_koreň 관리 Príkaz. */
public final class systém_nástroj {
    static int adresa_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int položka_COUNT() { return 명령해석기.token_COUNT; }
    static void zlyhanie_VALUE(String 안내) { 명령해석기.KR=2; 단말.Zápis(안내); 단말.문자(10); }
    static void chyba(int VALUE) { 명령해석기.chyba(VALUE); }
    static void 수항목(String Názov, int VALUE) { 단말.Zápis(Názov); 단말.수(VALUE); 단말.문자(10); }
    static int číslica_VALUE(int INDEX, int 한도) {
        if (INDEX>=položka_COUNT() || 명령해석기.dĺžka_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.dĺžka_VALUE[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (znak_VALUE<0 || znak_VALUE>9 || VALUE>(한도-znak_VALUE)/10) return -1;
            VALUE=VALUE*10+znak_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=položka_COUNT()) return false;
        int VALUE=0, blok_údajov_VALUE=0, číslica_COUNT=0, bod_COUNT=0;
        for (int 순번=0; 순번<명령해석기.dĺžka_VALUE[INDEX]; 순번++) {
            int znak_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (znak_VALUE=='.') { if (číslica_COUNT==0 || ++bod_COUNT>3) return false; VALUE=(VALUE<<8)|blok_údajov_VALUE; blok_údajov_VALUE=číslica_COUNT=0; }
            else { if (znak_VALUE<'0' || znak_VALUE>'9' || ++číslica_COUNT>3) return false; blok_údajov_VALUE=blok_údajov_VALUE*10+znak_VALUE-'0'; if(blok_údajov_VALUE>255)return false; }
        }
        if (bod_COUNT!=3 || číslica_COUNT==0) return false;
        adresa_VALUE=(VALUE<<8)|blok_údajov_VALUE; return true;
    }
    static void zapísať_adresa(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void zobraziť_sieť_stav() {
        단말.Zápis(Panel.sieť_stav(20,0)!=0?"en0: ":"sl0: "); 단말.Zápis(Panel.sieť_stav(3,0)!=0?"UP":"DOWN");
        단말.Zápis(Panel.sieť_stav(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Zápis(Panel.sieť_stav(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); zapísať_adresa(Panel.sieť_stav(0,0));
        단말.Zápis(" netmask "); zapísať_adresa(Panel.sieť_stav(1,0)); 단말.Zápis(" gateway "); zapísať_adresa(Panel.sieť_stav(2,0)); 단말.문자(10);
        단말.Zápis("  RX packets "); 단말.수(Panel.sieť_stav(4,0)); 단말.Zápis(" bytes "); 단말.수(Panel.sieť_stav(6,0));
        단말.Zápis(" TX packets "); 단말.수(Panel.sieť_stav(5,0)); 단말.Zápis(" bytes "); 단말.수(Panel.sieť_stav(7,0)); 단말.문자(10);
        수항목("  dropped ",Panel.sieť_stav(8,0));
    }
    static void množina_adresa(int Spustiť_2) {
        if (položka_COUNT()!=Spustiť_2+3 || !주소읽기(Spustiť_2)) { zlyhanie_VALUE("사용법: ipconfig set adresa 주소가림 brána_VALUE"); return; }
        int adresa=adresa_VALUE;
        if(!주소읽기(Spustiť_2+1)){zlyhanie_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=adresa_VALUE;
        if(!주소읽기(Spustiť_2+2)){zlyhanie_VALUE("Invalid IPv4 gateway");return;}
        int KR=Panel.sieť_Nastavenia(0,adresa,maska_VALUE,adresa_VALUE);
        if(KR<0) { chyba(KR); if(KR==-16)단말.Zápis("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Zápis("IPv4 configuration applied (until reboot)\n"); zobraziť_sieť_stav(); }
    }
    static void sieť_príkaz(boolean adresa_IP) {
        if (položka_COUNT()==1 || položka_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || položka_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { zobraziť_sieť_stav();return; }
        if (adresa_IP && 같음(1,"route") && (položka_COUNT()==2 || položka_COUNT()==3&&같음(2,"show"))) { zobraziť_cesta();return; }
        if (같음(1,"set")) { množina_adresa(2);return; }
        if (položka_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Panel.sieť_Nastavenia(같음(1,"up")?1:2,0,0,0);zobraziť_sieť_stav();return; }
        if (adresa_IP && položka_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Panel.sieť_Nastavenia(같음(5,"up")?1:2,0,0,0);zobraziť_sieť_stav();return; }
        zlyhanie_VALUE("사용법: ip [addr show|route show|set adresa 주소가림 brána_VALUE|link set dev sl0 up|down]");
    }
    static void zobraziť_cesta() {
        단말.Zápis("Destination Netmask Gateway Interface\n");
        zapísať_adresa(Panel.sieť_stav(0,0)&Panel.sieť_stav(1,0));단말.문자(' ');zapísať_adresa(Panel.sieť_stav(1,0));단말.Zápis(Panel.sieť_stav(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Panel.sieť_stav(2,0)!=0) {단말.Zápis("0.0.0.0 0.0.0.0 ");zapísať_adresa(Panel.sieť_stav(2,0));단말.Zápis(Panel.sieť_stav(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void zobraziť_sieť() {
        단말.Zápis("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int Typ_oblasť=Panel.sieť_stav(10,INDEX);if(Typ_oblasť==0)continue;
            단말.Zápis(Typ_oblasť==1?"TCP ":"UDP ");zapísať_adresa(Panel.sieť_stav(16,INDEX));단말.문자(':');단말.수(Panel.sieť_stav(11,INDEX));단말.문자(' ');
            zapísať_adresa(Panel.sieť_stav(12,INDEX));단말.문자(':');단말.수(Panel.sieť_stav(13,INDEX));단말.문자(' ');
            int Stav_VALUE=Panel.sieť_stav(14,INDEX);단말.Zápis(Typ_oblasť==2?"DATAGRAM":Stav_VALUE==1?"LISTEN":Stav_VALUE==2?"ESTABLISHED":Stav_VALUE==3?"CLOSE_WAIT":Stav_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Panel.sieť_stav(15,INDEX));단말.문자(10);
        }
        단말.Zápis("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stav_čakania(int 밀리초) {
        int Spustiť_2=Panel.밀리초();
        while(Panel.밀리초()-Spustiť_2<밀리초) {
            if(셸입출력.Informačné_systémy_interaktívny()!=0){int znak_VALUE=Panel.직렬읽기();if(znak_VALUE==3 || znak_VALUE=='q' || znak_VALUE=='Q' || znak_VALUE==27 || znak_VALUE==-4096)return false;}
            Panel.YIELD_procesor();
        }
        return true;
    }
    static void test_odpoveď() {
        int 횟수=4, 제한=1000, cieľová_hodnota=-1;
        for(int pozičný_index=1;pozičný_index<položka_COUNT();pozičný_index++) {
            if(같음(pozičný_index,"-c")){횟수=číslica_VALUE(++pozičný_index,100);if(횟수<1){zlyhanie_VALUE("ping: -c 1..100");return;}}
            else if(같음(pozičný_index,"-W")){제한=číslica_VALUE(++pozičný_index,10);if(제한<1){zlyhanie_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cieľová_hodnota<0)cieľová_hodnota=pozičný_index;else{zlyhanie_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(cieľová_hodnota<0 || !주소읽기(cieľová_hodnota)){zlyhanie_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresa=adresa_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Zápis("PING ");zapísať_adresa(adresa);단말.Zápis(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int poradie_VALUE=1;poradie_VALUE<=횟수 && 계속;poradie_VALUE++) {
            int 처리값=Panel.odoslať_odpoveď(adresa,poradie_VALUE);
            if(처리값<0){chyba(처리값);break;}보낸수++;
            int Spustiť_2=Panel.밀리초();
            while(Panel.응답읽기(0)==-11 && Panel.밀리초()-Spustiť_2<제한)if(!stav_čakania(1)){계속=false;break;}
            if(!계속)break;
            if(Panel.응답읽기(0)==0){
                int čas_VALUE=Panel.응답읽기(1);RECEIVED_COUNT++;누적+=čas_VALUE;if(čas_VALUE<최솟값)최솟값=čas_VALUE;if(čas_VALUE>최댓값)최댓값=čas_VALUE;
                단말.Zápis("32 bytes from ");zapísať_adresa(adresa);단말.Zápis(" seq=");단말.수(poradie_VALUE);단말.Zápis(" ttl=");단말.수(Panel.응답읽기(2));단말.Zápis(" time=");단말.수(čas_VALUE);단말.Zápis(" ms\n");
            }else{단말.Zápis("Request timeout seq=");단말.수(poradie_VALUE);단말.문자(10);}
            if(poradie_VALUE<횟수)계속=stav_čakania(200);
        }
        단말.수(보낸수);단말.Zápis(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Zápis(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Zápis("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Zápis("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Zápis(" ms\n");}
        명령해석기.KR=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void zobraziť_Aktivita() { 단말.Zápis("up ");단말.수(Panel.밀리초()/1000);단말.Zápis(" seconds\n"); }
    static void zobraziť_Pamäť() {
        수항목("ARM RAM KiB (firmware): ",Panel.dotaz_systém(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Panel.dotaz_systém(1,0));
        int celkovo_kapacita=Panel.dotaz_systém(2,0), 사용량=Panel.dotaz_systém(3,0);
        단말.Zápis("AOT heap KiB total/used/free: ");단말.수(celkovo_kapacita);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(celkovo_kapacita-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Panel.dotaz_systém(4,0));
        수항목("EL0 arena+session reserve KiB: ",Panel.dotaz_systém(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Panel.dotaz_systém(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Zápis("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void zobraziť_Tasks() {
        단말.Zápis("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Zápis("1 - RUN - - ");단말.수(Panel.밀리초());단말.Zápis(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Panel.úloha_Stav(INDEX)>0){단말.수(INDEX+1);단말.Zápis(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Stav_VALUE=Panel.dotaz_systém(20,INDEX);if(Stav_VALUE==0)continue;
            단말.수(Panel.dotaz_systém(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Zápis(Stav_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Panel.dotaz_systém(22,INDEX));단말.문자(' ');단말.수(Panel.dotaz_systém(24,INDEX));단말.문자(' ');단말.수(Panel.dotaz_systém(23,INDEX));단말.문자(' ');
            for(int pozičný_index=0;pozičný_index<288;pozičný_index++){int Byte_VALUE=Panel.dotaz_systém(25,INDEX+pozičný_index*4);if(Byte_VALUE==0)break;Panel.직렬쓰기(Byte_VALUE);}단말.문자(10);
        }
    }
    static void zobraziť_Úložisko() {
        int 칸수=0, údaje_COUNT=0;
        for(int INDEX=0;INDEX<Pamäť_Súbory.Súbor_COUNT;INDEX++)if(Pamäť_Súbory.이름길이[INDEX]>0 || Pamäť_Súbory.zdroj_COUNT[INDEX]>0){칸수++;údaje_COUNT+=Pamäť_Súbory.dĺžka_VALUE[INDEX];}
        단말.Zápis("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Pamäť_Súbory.Súbor_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Pamäť_Súbory.Súbor_COUNT-칸수)*16384);단말.문자(' ');단말.수(údaje_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Pamäť_Súbory.Súbor_COUNT);단말.Zápis(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void zobraziť_stav() {
        int 횟수=셸입출력.Informačné_systémy_interaktívny()!=0?0:1;
        if(položka_COUNT()>1){if(položka_COUNT()!=3 || !같음(1,"-n") || (횟수=číslica_VALUE(2,1000))<1){zlyhanie_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 ukončiť_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.Informačné_systémy_interaktívny()!=0 && 횟수==0)단말.Zápis("\u001b[2J\u001b[H");
            zobraziť_Aktivita();zobraziť_Pamäť();zobraziť_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!stav_čakania(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void zobraziť_Pomocník() {
        단말.Zápis("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Zápis(표준말(INDEX));단말.Zápis(" / ");단말.Zápis(관리명령.Word_SMS(INDEX));단말.Zápis(" : ");단말.Zápis(관리명령.설명(INDEX));단말.문자(10);}
        단말.Zápis("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Zápis("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Zápis("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Vykonať_príkaz() {
        int Príkaz=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Príkaz=INDEX;
        if(같음(0,"ifconfig"))Príkaz=0;if(같음(0,"ss"))Príkaz=4;
        if(Príkaz<0)return false;
        if(Príkaz==11){if(같음(1,"net") || 같음(1,"system"))zobraziť_Pomocník();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.zobraziť_Pomocník();return true;}
        if(Príkaz==0 || Príkaz==1)sieť_príkaz(Príkaz==1);
        else if(Príkaz==2)test_odpoveď();
        else if(Príkaz==6)zobraziť_stav();
        else if(položka_COUNT()!=1){zlyhanie_VALUE("This command takes no arguments; help system");}
        else if(Príkaz==3)zobraziť_cesta();else if(Príkaz==4)zobraziť_sieť();else if(Príkaz==5)zobraziť_Tasks();else if(Príkaz==7)zobraziť_Pamäť();else if(Príkaz==8)zobraziť_Úložisko();else if(Príkaz==9)zobraziť_Aktivita();
        else if(Príkaz==10)Panel.전원끄기();
        return true;
    }
}
