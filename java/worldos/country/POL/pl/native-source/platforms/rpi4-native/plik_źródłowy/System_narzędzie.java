// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** rzeczywisty_dane jądro_WARTOŚĆ 상태를 읽는 IPv4·ICMP·작업·Pamięć_WARTOŚĆ·RAM repozytorium_korzeń 관리 polecenie. */
public final class System_narzędzie {
    static int ADRES_WARTOŚĆ;
    static boolean 같음(int INDEKS, String Word_SMS) { return polecenie_interpreter.같음(INDEKS, Word_SMS); }
    static int towar_ILE_LICZB() { return polecenie_interpreter.token_ILE_LICZB; }
    static void awaria_WARTOŚĆ(String plik_README_eb81d7d9) { polecenie_interpreter.WYNIK=2; 단말.Zapis(plik_README_eb81d7d9); 단말.문자(10); }
    static void błąd(int WARTOŚĆ) { polecenie_interpreter.błąd(WARTOŚĆ); }
    static void identyfikator_wpis(String Nazwa, int WARTOŚĆ) { 단말.Zapis(Nazwa); 단말.identyfikator(WARTOŚĆ); 단말.문자(10); }
    static int cyfra_WARTOŚĆ(int INDEKS, int 한도) {
        if (INDEKS>=towar_ILE_LICZB() || polecenie_interpreter.długość_WARTOŚĆ[INDEKS]==0) return -1;
        int WARTOŚĆ=0;
        for (int 순번=0; 순번<polecenie_interpreter.długość_WARTOŚĆ[INDEKS]; 순번++) {
            int znak_WARTOŚĆ=polecenie_interpreter.token_WARTOŚĆ[polecenie_interpreter.시작점[INDEKS]+순번]-'0';
            if (znak_WARTOŚĆ<0 || znak_WARTOŚĆ>9 || WARTOŚĆ>(한도-znak_WARTOŚĆ)/10) return -1;
            WARTOŚĆ=WARTOŚĆ*10+znak_WARTOŚĆ;
        }
        return WARTOŚĆ<=한도?WARTOŚĆ:-1;
    }
    static boolean 주소읽기(int INDEKS) {
        if (INDEKS>=towar_ILE_LICZB()) return false;
        int WARTOŚĆ=0, fragment_WARTOŚĆ=0, cyfra_ILE_LICZB=0, punkt_ILE_LICZB=0;
        for (int 순번=0; 순번<polecenie_interpreter.długość_WARTOŚĆ[INDEKS]; 순번++) {
            int znak_WARTOŚĆ=polecenie_interpreter.token_WARTOŚĆ[polecenie_interpreter.시작점[INDEKS]+순번];
            if (znak_WARTOŚĆ=='.') { if (cyfra_ILE_LICZB==0 || ++punkt_ILE_LICZB>3) return false; WARTOŚĆ=(WARTOŚĆ<<8)|fragment_WARTOŚĆ; fragment_WARTOŚĆ=cyfra_ILE_LICZB=0; }
            else { if (znak_WARTOŚĆ<'0' || znak_WARTOŚĆ>'9' || ++cyfra_ILE_LICZB>3) return false; fragment_WARTOŚĆ=fragment_WARTOŚĆ*10+znak_WARTOŚĆ-'0'; if(fragment_WARTOŚĆ>255)return false; }
        }
        if (punkt_ILE_LICZB!=3 || cyfra_ILE_LICZB==0) return false;
        ADRES_WARTOŚĆ=(WARTOŚĆ<<8)|fragment_WARTOŚĆ; return true;
    }
    static void zapis_ADRES(int WARTOŚĆ) {
        단말.identyfikator((WARTOŚĆ>>>24)&255); 단말.문자('.'); 단말.identyfikator((WARTOŚĆ>>>16)&255); 단말.문자('.');
        단말.identyfikator((WARTOŚĆ>>>8)&255); 단말.문자('.'); 단말.identyfikator(WARTOŚĆ&255);
    }
    static void program_sieć_stan() {
        단말.Zapis(Tablica.sieć_stan(20,0)!=0?"en0: ":"sl0: "); 단말.Zapis(Tablica.sieć_stan(3,0)!=0?"UP":"DOWN");
        단말.Zapis(Tablica.sieć_stan(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Zapis(Tablica.sieć_stan(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); zapis_ADRES(Tablica.sieć_stan(0,0));
        단말.Zapis(" netmask "); zapis_ADRES(Tablica.sieć_stan(1,0)); 단말.Zapis(" gateway "); zapis_ADRES(Tablica.sieć_stan(2,0)); 단말.문자(10);
        단말.Zapis("  RX packets "); 단말.identyfikator(Tablica.sieć_stan(4,0)); 단말.Zapis(" bytes "); 단말.identyfikator(Tablica.sieć_stan(6,0));
        단말.Zapis(" TX packets "); 단말.identyfikator(Tablica.sieć_stan(5,0)); 단말.Zapis(" bytes "); 단말.identyfikator(Tablica.sieć_stan(7,0)); 단말.문자(10);
        identyfikator_wpis("  dropped ",Tablica.sieć_stan(8,0));
    }
    static void set_ADRES(int Uruchom_2) {
        if (towar_ILE_LICZB()!=Uruchom_2+3 || !주소읽기(Uruchom_2)) { awaria_WARTOŚĆ("사용법: ipconfig set Adres 주소가림 brama_WARTOŚĆ"); return; }
        int Adres=ADRES_WARTOŚĆ;
        if(!주소읽기(Uruchom_2+1)){awaria_WARTOŚĆ("Invalid IPv4 netmask");return;} int maska_WARTOŚĆ=ADRES_WARTOŚĆ;
        if(!주소읽기(Uruchom_2+2)){awaria_WARTOŚĆ("Invalid IPv4 gateway");return;}
        int WYNIK=Tablica.sieć_Ustawienia(0,Adres,maska_WARTOŚĆ,ADRES_WARTOŚĆ);
        if(WYNIK<0) { błąd(WYNIK); if(WYNIK==-16)단말.Zapis("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Zapis("IPv4 configuration applied (until reboot)\n"); program_sieć_stan(); }
    }
    static void sieć_polecenie(boolean adres_IP) {
        if (towar_ILE_LICZB()==1 || towar_ILE_LICZB()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || towar_ILE_LICZB()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { program_sieć_stan();return; }
        if (adres_IP && 같음(1,"route") && (towar_ILE_LICZB()==2 || towar_ILE_LICZB()==3&&같음(2,"show"))) { program_ścieżka();return; }
        if (같음(1,"set")) { set_ADRES(2);return; }
        if (towar_ILE_LICZB()==2 && (같음(1,"up") || 같음(1,"down"))) { Tablica.sieć_Ustawienia(같음(1,"up")?1:2,0,0,0);program_sieć_stan();return; }
        if (adres_IP && towar_ILE_LICZB()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tablica.sieć_Ustawienia(같음(5,"up")?1:2,0,0,0);program_sieć_stan();return; }
        awaria_WARTOŚĆ("사용법: ip [addr show|route show|set Adres 주소가림 brama_WARTOŚĆ|link set dev sl0 up|down]");
    }
    static void program_ścieżka() {
        단말.Zapis("Destination Netmask Gateway Interface\n");
        zapis_ADRES(Tablica.sieć_stan(0,0)&Tablica.sieć_stan(1,0));단말.문자(' ');zapis_ADRES(Tablica.sieć_stan(1,0));단말.Zapis(Tablica.sieć_stan(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tablica.sieć_stan(2,0)!=0) {단말.Zapis("0.0.0.0 0.0.0.0 ");zapis_ADRES(Tablica.sieć_stan(2,0));단말.Zapis(Tablica.sieć_stan(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void program_sieć() {
        단말.Zapis("Proto Local Remote State Queued\n");
        for(int INDEKS=0;INDEKS<32;INDEKS++) {
            int TYP_obszar=Tablica.sieć_stan(10,INDEKS);if(TYP_obszar==0)continue;
            단말.Zapis(TYP_obszar==1?"TCP ":"UDP ");zapis_ADRES(Tablica.sieć_stan(16,INDEKS));단말.문자(':');단말.identyfikator(Tablica.sieć_stan(11,INDEKS));단말.문자(' ');
            zapis_ADRES(Tablica.sieć_stan(12,INDEKS));단말.문자(':');단말.identyfikator(Tablica.sieć_stan(13,INDEKS));단말.문자(' ');
            int Stan_WARTOŚĆ=Tablica.sieć_stan(14,INDEKS);단말.Zapis(TYP_obszar==2?"DATAGRAM":Stan_WARTOŚĆ==1?"LISTEN":Stan_WARTOŚĆ==2?"ESTABLISHED":Stan_WARTOŚĆ==3?"CLOSE_WAIT":Stan_WARTOŚĆ==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.identyfikator(Tablica.sieć_stan(15,INDEKS));단말.문자(10);
        }
        단말.Zapis("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stan_oczekiwania(int 밀리초) {
        int Uruchom_2=Tablica.밀리초();
        while(Tablica.밀리초()-Uruchom_2<밀리초) {
            if(셸입출력.systemy_informacyjne_interakcyjny()!=0){int znak_WARTOŚĆ=Tablica.직렬읽기();if(znak_WARTOŚĆ==3 || znak_WARTOŚĆ=='q' || znak_WARTOŚĆ=='Q' || znak_WARTOŚĆ==27 || znak_WARTOŚĆ==-4096)return false;}
            Tablica.Dochód_CPU();
        }
        return true;
    }
    static void test_odpowiedź() {
        int powtórzenie_ILE_LICZB=4, 제한=1000, wartość_docelowa=-1;
        for(int indeks_pozycji=1;indeks_pozycji<towar_ILE_LICZB();indeks_pozycji++) {
            if(같음(indeks_pozycji,"-c")){powtórzenie_ILE_LICZB=cyfra_WARTOŚĆ(++indeks_pozycji,100);if(powtórzenie_ILE_LICZB<1){awaria_WARTOŚĆ("ping: -c 1..100");return;}}
            else if(같음(indeks_pozycji,"-W")){제한=cyfra_WARTOŚĆ(++indeks_pozycji,10);if(제한<1){awaria_WARTOŚĆ("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(wartość_docelowa<0)wartość_docelowa=indeks_pozycji;else{awaria_WARTOŚĆ("사용법: ping [-c powtórzenie_ILE_LICZB] [-W 초] IPv4");return;}
        }
        if(wartość_docelowa<0 || !주소읽기(wartość_docelowa)){awaria_WARTOŚĆ("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Adres=ADRES_WARTOŚĆ, 보낸수=0, KWOTA_WYKUP_ILE_LICZB=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Zapis("PING ");zapis_ADRES(Adres);단말.Zapis(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int zamówić_WARTOŚĆ=1;zamówić_WARTOŚĆ<=powtórzenie_ILE_LICZB && 계속;zamówić_WARTOŚĆ++) {
            int 처리값=Tablica.wysłać_odpowiedź(Adres,zamówić_WARTOŚĆ);
            if(처리값<0){błąd(처리값);break;}보낸수++;
            int Uruchom_2=Tablica.밀리초();
            while(Tablica.응답읽기(0)==-11 && Tablica.밀리초()-Uruchom_2<제한)if(!stan_oczekiwania(1)){계속=false;break;}
            if(!계속)break;
            if(Tablica.응답읽기(0)==0){
                int wartość_czasu=Tablica.응답읽기(1);KWOTA_WYKUP_ILE_LICZB++;누적+=wartość_czasu;if(wartość_czasu<최솟값)최솟값=wartość_czasu;if(wartość_czasu>최댓값)최댓값=wartość_czasu;
                단말.Zapis("32 bytes from ");zapis_ADRES(Adres);단말.Zapis(" seq=");단말.identyfikator(zamówić_WARTOŚĆ);단말.Zapis(" ttl=");단말.identyfikator(Tablica.응답읽기(2));단말.Zapis(" time=");단말.identyfikator(wartość_czasu);단말.Zapis(" ms\n");
            }else{단말.Zapis("Request timeout seq=");단말.identyfikator(zamówić_WARTOŚĆ);단말.문자(10);}
            if(zamówić_WARTOŚĆ<powtórzenie_ILE_LICZB)계속=stan_oczekiwania(200);
        }
        단말.identyfikator(보낸수);단말.Zapis(" transmitted, ");단말.identyfikator(KWOTA_WYKUP_ILE_LICZB);단말.Zapis(" received, ");단말.identyfikator(보낸수==0?100:(보낸수-KWOTA_WYKUP_ILE_LICZB)*100/보낸수);단말.Zapis("% packet loss\n");
        if(KWOTA_WYKUP_ILE_LICZB>0){단말.Zapis("rtt min/avg/max = ");단말.identyfikator(최솟값);단말.문자('/');단말.identyfikator(누적/KWOTA_WYKUP_ILE_LICZB);단말.문자('/');단말.identyfikator(최댓값);단말.Zapis(" ms\n");}
        polecenie_interpreter.WYNIK=계속?(KWOTA_WYKUP_ILE_LICZB==0?1:0):130;
    }
    static void program_Aktywność() { 단말.Zapis("up ");단말.identyfikator(Tablica.밀리초()/1000);단말.Zapis(" seconds\n"); }
    static void program_Pamięć() {
        identyfikator_wpis("ARM RAM KiB (firmware): ",Tablica.zapytanie_System(0,0));
        identyfikator_wpis("Kernel image+BSS+stack KiB: ",Tablica.zapytanie_System(1,0));
        int suma_pojemność=Tablica.zapytanie_System(2,0), 사용량=Tablica.zapytanie_System(3,0);
        단말.Zapis("AOT heap KiB total/used/free: ");단말.identyfikator(suma_pojemność);단말.문자('/');단말.identyfikator(사용량);단말.문자('/');단말.identyfikator(suma_pojemność-사용량);단말.문자(10);
        identyfikator_wpis("Framebuffer KiB: ",Tablica.zapytanie_System(4,0));
        identyfikator_wpis("EL0 arena+session reserve KiB: ",Tablica.zapytanie_System(5,0));
        int 매핑=0;for(int INDEKS=0;INDEKS<4;INDEKS++)매핑+=Tablica.zapytanie_System(22,INDEKS);
        identyfikator_wpis("EL0 mapped KiB: ",매핑);
        단말.Zapis("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void program_Tasks() {
        단말.Zapis("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Zapis("1 - RUN - - ");단말.identyfikator(Tablica.밀리초());단말.Zapis(" kernel/shell\n");
        for(int INDEKS=1;INDEKS<3;INDEKS++)if(Tablica.zadanie_Stan(INDEKS)>0){단말.identyfikator(INDEKS+1);단말.Zapis(" - READY 64 - - kernel-task\n");}
        for(int INDEKS=0;INDEKS<4;INDEKS++){
            int Stan_WARTOŚĆ=Tablica.zapytanie_System(20,INDEKS);if(Stan_WARTOŚĆ==0)continue;
            단말.identyfikator(Tablica.zapytanie_System(21,INDEKS));단말.문자(' ');단말.identyfikator(INDEKS);단말.Zapis(Stan_WARTOŚĆ==1?" RUN ":" SUSPENDED ");
            단말.identyfikator(Tablica.zapytanie_System(22,INDEKS));단말.문자(' ');단말.identyfikator(Tablica.zapytanie_System(24,INDEKS));단말.문자(' ');단말.identyfikator(Tablica.zapytanie_System(23,INDEKS));단말.문자(' ');
            for(int indeks_pozycji=0;indeks_pozycji<288;indeks_pozycji++){int bajt_WARTOŚĆ=Tablica.zapytanie_System(25,INDEKS+indeks_pozycji*4);if(bajt_WARTOŚĆ==0)break;Tablica.직렬쓰기(bajt_WARTOŚĆ);}단말.문자(10);
        }
    }
    static void program_Pamięć_deafe149() {
        int gniazdo_ILE_LICZB=0, dane_ILE_LICZB=0;
        for(int INDEKS=0;INDEKS<Pamięć_Files.Plik_ILE_LICZB;INDEKS++)if(Pamięć_Files.이름길이[INDEKS]>0 || Pamięć_Files.odwołanie_ILE_LICZB[INDEKS]>0){gniazdo_ILE_LICZB++;dane_ILE_LICZB+=Pamięć_Files.długość_WARTOŚĆ[INDEKS];}
        단말.Zapis("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.identyfikator(Pamięć_Files.Plik_ILE_LICZB*16384);단말.문자(' ');단말.identyfikator(gniazdo_ILE_LICZB*16384);단말.문자(' ');단말.identyfikator((Pamięć_Files.Plik_ILE_LICZB-gniazdo_ILE_LICZB)*16384);단말.문자(' ');단말.identyfikator(dane_ILE_LICZB);단말.문자(' ');단말.identyfikator(gniazdo_ILE_LICZB);단말.문자('/');단말.identyfikator(Pamięć_Files.Plik_ILE_LICZB);단말.Zapis(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void program_stan() {
        int powtórzenie_ILE_LICZB=셸입출력.systemy_informacyjne_interakcyjny()!=0?0:1;
        if(towar_ILE_LICZB()>1){if(towar_ILE_LICZB()!=3 || !같음(1,"-n") || (powtórzenie_ILE_LICZB=cyfra_WARTOŚĆ(2,1000))<1){awaria_WARTOŚĆ("사용법: top [-n 1..1000]; q/Ctrl+C로 zakończ_program");return;}}
        for(int SEKWENCJA_WARTOŚĆ=0;powtórzenie_ILE_LICZB==0 || SEKWENCJA_WARTOŚĆ<powtórzenie_ILE_LICZB;SEKWENCJA_WARTOŚĆ++){
            if(셸입출력.systemy_informacyjne_interakcyjny()!=0 && powtórzenie_ILE_LICZB==0)단말.Zapis("\u001b[2J\u001b[H");
            program_Aktywność();program_Pamięć();program_Tasks();
            if(powtórzenie_ILE_LICZB!=0 && SEKWENCJA_WARTOŚĆ+1>=powtórzenie_ILE_LICZB)break;
            if(!stan_oczekiwania(1000))break;
        }
    }
    static String Standard_Word(int INDEKS) {
        if(INDEKS==0)return "ipconfig";if(INDEKS==1)return "ip";if(INDEKS==2)return "ping";if(INDEKS==3)return "route";if(INDEKS==4)return "netstat";
        if(INDEKS==5)return "ps";if(INDEKS==6)return "top";if(INDEKS==7)return "free";if(INDEKS==8)return "df";if(INDEKS==9)return "uptime";if(INDEKS==10)return "poweroff";return "help";
    }
    static void pokaż_pomoc() {
        단말.Zapis("--- Network / system commands ---\n");
        for(int INDEKS=0;INDEKS<12;INDEKS++){단말.Zapis(Standard_Word(INDEKS));단말.Zapis(" / ");단말.Zapis(관리명령.Word_SMS(INDEKS));단말.Zapis(" : ");단말.Zapis(관리명령.설명(INDEKS));단말.문자(10);}
        단말.Zapis("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Zapis("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Zapis("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Wykonaj_polecenie() {
        int polecenie=-1;
        for(int INDEKS=0;INDEKS<12;INDEKS++)if(같음(0,Standard_Word(INDEKS)) || 같음(0,관리명령.Word_SMS(INDEKS)))polecenie=INDEKS;
        if(같음(0,"ifconfig"))polecenie=0;if(같음(0,"ss"))polecenie=4;
        if(polecenie<0)return false;
        if(polecenie==11){if(같음(1,"net") || 같음(1,"system"))pokaż_pomoc();else if(같음(1,"ko") || 같음(1,"input"))polecenie_interpreter.한글도움말();else polecenie_interpreter.pokaż_pomoc();return true;}
        if(polecenie==0 || polecenie==1)sieć_polecenie(polecenie==1);
        else if(polecenie==2)test_odpowiedź();
        else if(polecenie==6)program_stan();
        else if(towar_ILE_LICZB()!=1){awaria_WARTOŚĆ("This command takes no arguments; help system");}
        else if(polecenie==3)program_ścieżka();else if(polecenie==4)program_sieć();else if(polecenie==5)program_Tasks();else if(polecenie==7)program_Pamięć();else if(polecenie==8)program_Pamięć_deafe149();else if(polecenie==9)program_Aktywność();
        else if(polecenie==10)Tablica.전원끄기();
        return true;
    }
}
