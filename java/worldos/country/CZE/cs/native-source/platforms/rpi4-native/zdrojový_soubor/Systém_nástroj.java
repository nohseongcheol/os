// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** skutečný_data jádro_HODNOTA 상태를 읽는 IPv4·ICMP·작업·Paměť_HODNOTA·RAM úložiště_kořen 관리 příkaz. */
public final class Systém_nástroj {
    static int ODKAZ_HODNOTA;
    static boolean 같음(int INDEX, String Word_SMS) { return příkaz_interpret.같음(INDEX, Word_SMS); }
    static int zboží_POČET() { return příkaz_interpret.token_POČET; }
    static void selhání_HODNOTA(String 안내) { příkaz_interpret.VÝSLEDEK=2; 단말.Zápis(안내); 단말.문자(10); }
    static void chyba(int HODNOTA) { příkaz_interpret.chyba(HODNOTA); }
    static void číslo_položka(String Název, int HODNOTA) { 단말.Zápis(Název); 단말.číslo(HODNOTA); 단말.문자(10); }
    static int číslice_HODNOTA(int INDEX, int 한도) {
        if (INDEX>=zboží_POČET() || příkaz_interpret.délka_HODNOTA[INDEX]==0) return -1;
        int HODNOTA=0;
        for (int 순번=0; 순번<příkaz_interpret.délka_HODNOTA[INDEX]; 순번++) {
            int znak_HODNOTA=příkaz_interpret.token_HODNOTA[příkaz_interpret.시작점[INDEX]+순번]-'0';
            if (znak_HODNOTA<0 || znak_HODNOTA>9 || HODNOTA>(한도-znak_HODNOTA)/10) return -1;
            HODNOTA=HODNOTA*10+znak_HODNOTA;
        }
        return HODNOTA<=한도?HODNOTA:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=zboží_POČET()) return false;
        int HODNOTA=0, blok_dat_HODNOTA=0, číslice_POČET=0, bod_POČET=0;
        for (int 순번=0; 순번<příkaz_interpret.délka_HODNOTA[INDEX]; 순번++) {
            int znak_HODNOTA=příkaz_interpret.token_HODNOTA[příkaz_interpret.시작점[INDEX]+순번];
            if (znak_HODNOTA=='.') { if (číslice_POČET==0 || ++bod_POČET>3) return false; HODNOTA=(HODNOTA<<8)|blok_dat_HODNOTA; blok_dat_HODNOTA=číslice_POČET=0; }
            else { if (znak_HODNOTA<'0' || znak_HODNOTA>'9' || ++číslice_POČET>3) return false; blok_dat_HODNOTA=blok_dat_HODNOTA*10+znak_HODNOTA-'0'; if(blok_dat_HODNOTA>255)return false; }
        }
        if (bod_POČET!=3 || číslice_POČET==0) return false;
        ODKAZ_HODNOTA=(HODNOTA<<8)|blok_dat_HODNOTA; return true;
    }
    static void zápis_ODKAZ(int HODNOTA) {
        단말.číslo((HODNOTA>>>24)&255); 단말.문자('.'); 단말.číslo((HODNOTA>>>16)&255); 단말.문자('.');
        단말.číslo((HODNOTA>>>8)&255); 단말.문자('.'); 단말.číslo(HODNOTA&255);
    }
    static void zobrazit_síť_stav() {
        단말.Zápis(Panel.síť_stav(20,0)!=0?"en0: ":"sl0: "); 단말.Zápis(Panel.síť_stav(3,0)!=0?"UP":"DOWN");
        단말.Zápis(Panel.síť_stav(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Zápis(Panel.síť_stav(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); zápis_ODKAZ(Panel.síť_stav(0,0));
        단말.Zápis(" netmask "); zápis_ODKAZ(Panel.síť_stav(1,0)); 단말.Zápis(" gateway "); zápis_ODKAZ(Panel.síť_stav(2,0)); 단말.문자(10);
        단말.Zápis("  RX packets "); 단말.číslo(Panel.síť_stav(4,0)); 단말.Zápis(" bytes "); 단말.číslo(Panel.síť_stav(6,0));
        단말.Zápis(" TX packets "); 단말.číslo(Panel.síť_stav(5,0)); 단말.Zápis(" bytes "); 단말.číslo(Panel.síť_stav(7,0)); 단말.문자(10);
        číslo_položka("  dropped ",Panel.síť_stav(8,0));
    }
    static void sada_ODKAZ(int Spustit_2) {
        if (zboží_POČET()!=Spustit_2+3 || !주소읽기(Spustit_2)) { selhání_HODNOTA("사용법: ipconfig set Adresa 주소가림 brána_HODNOTA"); return; }
        int Adresa=ODKAZ_HODNOTA;
        if(!주소읽기(Spustit_2+1)){selhání_HODNOTA("Invalid IPv4 netmask");return;} int maska_HODNOTA=ODKAZ_HODNOTA;
        if(!주소읽기(Spustit_2+2)){selhání_HODNOTA("Invalid IPv4 gateway");return;}
        int VÝSLEDEK=Panel.síť_Nastavení(0,Adresa,maska_HODNOTA,ODKAZ_HODNOTA);
        if(VÝSLEDEK<0) { chyba(VÝSLEDEK); if(VÝSLEDEK==-16)단말.Zápis("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Zápis("IPv4 configuration applied (until reboot)\n"); zobrazit_síť_stav(); }
    }
    static void síť_příkaz(boolean IP_adresa) {
        if (zboží_POČET()==1 || zboží_POČET()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || zboží_POČET()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { zobrazit_síť_stav();return; }
        if (IP_adresa && 같음(1,"route") && (zboží_POČET()==2 || zboží_POČET()==3&&같음(2,"show"))) { zobrazit_cesta();return; }
        if (같음(1,"set")) { sada_ODKAZ(2);return; }
        if (zboží_POČET()==2 && (같음(1,"up") || 같음(1,"down"))) { Panel.síť_Nastavení(같음(1,"up")?1:2,0,0,0);zobrazit_síť_stav();return; }
        if (IP_adresa && zboží_POČET()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Panel.síť_Nastavení(같음(5,"up")?1:2,0,0,0);zobrazit_síť_stav();return; }
        selhání_HODNOTA("사용법: ip [addr show|route show|set Adresa 주소가림 brána_HODNOTA|link set dev sl0 up|down]");
    }
    static void zobrazit_cesta() {
        단말.Zápis("Destination Netmask Gateway Interface\n");
        zápis_ODKAZ(Panel.síť_stav(0,0)&Panel.síť_stav(1,0));단말.문자(' ');zápis_ODKAZ(Panel.síť_stav(1,0));단말.Zápis(Panel.síť_stav(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Panel.síť_stav(2,0)!=0) {단말.Zápis("0.0.0.0 0.0.0.0 ");zápis_ODKAZ(Panel.síť_stav(2,0));단말.Zápis(Panel.síť_stav(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void zobrazit_síť() {
        단말.Zápis("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYP_oblast=Panel.síť_stav(10,INDEX);if(TYP_oblast==0)continue;
            단말.Zápis(TYP_oblast==1?"TCP ":"UDP ");zápis_ODKAZ(Panel.síť_stav(16,INDEX));단말.문자(':');단말.číslo(Panel.síť_stav(11,INDEX));단말.문자(' ');
            zápis_ODKAZ(Panel.síť_stav(12,INDEX));단말.문자(':');단말.číslo(Panel.síť_stav(13,INDEX));단말.문자(' ');
            int Stav_HODNOTA=Panel.síť_stav(14,INDEX);단말.Zápis(TYP_oblast==2?"DATAGRAM":Stav_HODNOTA==1?"LISTEN":Stav_HODNOTA==2?"ESTABLISHED":Stav_HODNOTA==3?"CLOSE_WAIT":Stav_HODNOTA==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.číslo(Panel.síť_stav(15,INDEX));단말.문자(10);
        }
        단말.Zápis("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean čekací_stav(int 밀리초) {
        int Spustit_2=Panel.밀리초();
        while(Panel.밀리초()-Spustit_2<밀리초) {
            if(셸입출력.informační_systémy_interaktivní()!=0){int znak_HODNOTA=Panel.직렬읽기();if(znak_HODNOTA==3 || znak_HODNOTA=='q' || znak_HODNOTA=='Q' || znak_HODNOTA==27 || znak_HODNOTA==-4096)return false;}
            Panel.YIELD_CPU();
        }
        return true;
    }
    static void test_odpověď() {
        int opakování_POČET=4, 제한=1000, cílová_úroveň=-1;
        for(int poziční_index=1;poziční_index<zboží_POČET();poziční_index++) {
            if(같음(poziční_index,"-c")){opakování_POČET=číslice_HODNOTA(++poziční_index,100);if(opakování_POČET<1){selhání_HODNOTA("ping: -c 1..100");return;}}
            else if(같음(poziční_index,"-W")){제한=číslice_HODNOTA(++poziční_index,10);if(제한<1){selhání_HODNOTA("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(cílová_úroveň<0)cílová_úroveň=poziční_index;else{selhání_HODNOTA("사용법: ping [-c opakování_POČET] [-W 초] IPv4");return;}
        }
        if(cílová_úroveň<0 || !주소읽기(cílová_úroveň)){selhání_HODNOTA("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Adresa=ODKAZ_HODNOTA, 보낸수=0, RECEIVED_POČET=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Zápis("PING ");zápis_ODKAZ(Adresa);단말.Zápis(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int pořadí_HODNOTA=1;pořadí_HODNOTA<=opakování_POČET && 계속;pořadí_HODNOTA++) {
            int 처리값=Panel.poslat_odpověď(Adresa,pořadí_HODNOTA);
            if(처리값<0){chyba(처리값);break;}보낸수++;
            int Spustit_2=Panel.밀리초();
            while(Panel.응답읽기(0)==-11 && Panel.밀리초()-Spustit_2<제한)if(!čekací_stav(1)){계속=false;break;}
            if(!계속)break;
            if(Panel.응답읽기(0)==0){
                int časová_hodnota=Panel.응답읽기(1);RECEIVED_POČET++;누적+=časová_hodnota;if(časová_hodnota<최솟값)최솟값=časová_hodnota;if(časová_hodnota>최댓값)최댓값=časová_hodnota;
                단말.Zápis("32 bytes from ");zápis_ODKAZ(Adresa);단말.Zápis(" seq=");단말.číslo(pořadí_HODNOTA);단말.Zápis(" ttl=");단말.číslo(Panel.응답읽기(2));단말.Zápis(" time=");단말.číslo(časová_hodnota);단말.Zápis(" ms\n");
            }else{단말.Zápis("Request timeout seq=");단말.číslo(pořadí_HODNOTA);단말.문자(10);}
            if(pořadí_HODNOTA<opakování_POČET)계속=čekací_stav(200);
        }
        단말.číslo(보낸수);단말.Zápis(" transmitted, ");단말.číslo(RECEIVED_POČET);단말.Zápis(" received, ");단말.číslo(보낸수==0?100:(보낸수-RECEIVED_POČET)*100/보낸수);단말.Zápis("% packet loss\n");
        if(RECEIVED_POČET>0){단말.Zápis("rtt min/avg/max = ");단말.číslo(최솟값);단말.문자('/');단말.číslo(누적/RECEIVED_POČET);단말.문자('/');단말.číslo(최댓값);단말.Zápis(" ms\n");}
        příkaz_interpret.VÝSLEDEK=계속?(RECEIVED_POČET==0?1:0):130;
    }
    static void zobrazit_Aktivita() { 단말.Zápis("up ");단말.číslo(Panel.밀리초()/1000);단말.Zápis(" seconds\n"); }
    static void zobrazit_Paměť() {
        číslo_položka("ARM RAM KiB (firmware): ",Panel.dotaz_Systém(0,0));
        číslo_položka("Kernel image+BSS+stack KiB: ",Panel.dotaz_Systém(1,0));
        int celkem_kapacita=Panel.dotaz_Systém(2,0), 사용량=Panel.dotaz_Systém(3,0);
        단말.Zápis("AOT heap KiB total/used/free: ");단말.číslo(celkem_kapacita);단말.문자('/');단말.číslo(사용량);단말.문자('/');단말.číslo(celkem_kapacita-사용량);단말.문자(10);
        číslo_položka("Framebuffer KiB: ",Panel.dotaz_Systém(4,0));
        číslo_položka("EL0 arena+session reserve KiB: ",Panel.dotaz_Systém(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Panel.dotaz_Systém(22,INDEX);
        číslo_položka("EL0 mapped KiB: ",매핑);
        단말.Zápis("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void zobrazit_Tasks() {
        단말.Zápis("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Zápis("1 - RUN - - ");단말.číslo(Panel.밀리초());단말.Zápis(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Panel.úkol_Stav(INDEX)>0){단말.číslo(INDEX+1);단말.Zápis(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Stav_HODNOTA=Panel.dotaz_Systém(20,INDEX);if(Stav_HODNOTA==0)continue;
            단말.číslo(Panel.dotaz_Systém(21,INDEX));단말.문자(' ');단말.číslo(INDEX);단말.Zápis(Stav_HODNOTA==1?" RUN ":" SUSPENDED ");
            단말.číslo(Panel.dotaz_Systém(22,INDEX));단말.문자(' ');단말.číslo(Panel.dotaz_Systém(24,INDEX));단말.문자(' ');단말.číslo(Panel.dotaz_Systém(23,INDEX));단말.문자(' ');
            for(int poziční_index=0;poziční_index<288;poziční_index++){int bajt_HODNOTA=Panel.dotaz_Systém(25,INDEX+poziční_index*4);if(bajt_HODNOTA==0)break;Panel.직렬쓰기(bajt_HODNOTA);}단말.문자(10);
        }
    }
    static void zobrazit_Storage() {
        int přihrádka_POČET=0, data_POČET=0;
        for(int INDEX=0;INDEX<Paměť_Files.Soubor_POČET;INDEX++)if(Paměť_Files.이름길이[INDEX]>0 || Paměť_Files.odkaz_POČET[INDEX]>0){přihrádka_POČET++;data_POČET+=Paměť_Files.délka_HODNOTA[INDEX];}
        단말.Zápis("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.číslo(Paměť_Files.Soubor_POČET*16384);단말.문자(' ');단말.číslo(přihrádka_POČET*16384);단말.문자(' ');단말.číslo((Paměť_Files.Soubor_POČET-přihrádka_POČET)*16384);단말.문자(' ');단말.číslo(data_POČET);단말.문자(' ');단말.číslo(přihrádka_POČET);단말.문자('/');단말.číslo(Paměť_Files.Soubor_POČET);단말.Zápis(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void zobrazit_stav() {
        int opakování_POČET=셸입출력.informační_systémy_interaktivní()!=0?0:1;
        if(zboží_POČET()>1){if(zboží_POČET()!=3 || !같음(1,"-n") || (opakování_POČET=číslice_HODNOTA(2,1000))<1){selhání_HODNOTA("사용법: top [-n 1..1000]; q/Ctrl+C로 ukončit_program");return;}}
        for(int SEQUENCE_HODNOTA=0;opakování_POČET==0 || SEQUENCE_HODNOTA<opakování_POČET;SEQUENCE_HODNOTA++){
            if(셸입출력.informační_systémy_interaktivní()!=0 && opakování_POČET==0)단말.Zápis("\u001b[2J\u001b[H");
            zobrazit_Aktivita();zobrazit_Paměť();zobrazit_Tasks();
            if(opakování_POČET!=0 && SEQUENCE_HODNOTA+1>=opakování_POČET)break;
            if(!čekací_stav(1000))break;
        }
    }
    static String Standard_Word(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void zobrazit_nápovědu() {
        단말.Zápis("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Zápis(Standard_Word(INDEX));단말.Zápis(" / ");단말.Zápis(관리명령.Word_SMS(INDEX));단말.Zápis(" : ");단말.Zápis(관리명령.설명(INDEX));단말.문자(10);}
        단말.Zápis("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Zápis("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Zápis("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Provést_příkaz() {
        int příkaz=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,Standard_Word(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))příkaz=INDEX;
        if(같음(0,"ifconfig"))příkaz=0;if(같음(0,"ss"))příkaz=4;
        if(příkaz<0)return false;
        if(příkaz==11){if(같음(1,"net") || 같음(1,"system"))zobrazit_nápovědu();else if(같음(1,"ko") || 같음(1,"input"))příkaz_interpret.한글도움말();else příkaz_interpret.zobrazit_nápovědu();return true;}
        if(příkaz==0 || příkaz==1)síť_příkaz(příkaz==1);
        else if(příkaz==2)test_odpověď();
        else if(příkaz==6)zobrazit_stav();
        else if(zboží_POČET()!=1){selhání_HODNOTA("This command takes no arguments; help system");}
        else if(příkaz==3)zobrazit_cesta();else if(příkaz==4)zobrazit_síť();else if(příkaz==5)zobrazit_Tasks();else if(příkaz==7)zobrazit_Paměť();else if(příkaz==8)zobrazit_Storage();else if(příkaz==9)zobrazit_Aktivita();
        else if(příkaz==10)Panel.전원끄기();
        return true;
    }
}
