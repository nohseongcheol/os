// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** todellinen_data ydin_ARVO 상태를 읽는 IPv4·ICMP·작업·Muisti_ARVO·RAM säilö_juuri 관리 komento. */
public final class Järjestelmä_työkalu {
    static int OSOITE_ARVO;
    static boolean 같음(int INDEKSI, String Word_SMS) { return 명령해석기.같음(INDEKSI, Word_SMS); }
    static int kohde_LASKE() { return 명령해석기.tunnus_LASKE; }
    static void virhe_ARVO(String Lueminut_eb81d7d9) { 명령해석기.TULOS=2; 단말.Kirjoitus(Lueminut_eb81d7d9); 단말.문자(10); }
    static void VIRHE(int ARVO) { 명령해석기.VIRHE(ARVO); }
    static void numero_merkintä(String Nimi, int ARVO) { 단말.Kirjoitus(Nimi); 단말.numero(ARVO); 단말.문자(10); }
    static int numero_ARVO(int INDEKSI, int 한도) {
        if (INDEKSI>=kohde_LASKE() || 명령해석기.kesto_ARVO[INDEKSI]==0) return -1;
        int ARVO=0;
        for (int 순번=0; 순번<명령해석기.kesto_ARVO[INDEKSI]; 순번++) {
            int merkki_ARVO=명령해석기.tunnus_ARVO_eb540501[명령해석기.시작점[INDEKSI]+순번]-'0';
            if (merkki_ARVO<0 || merkki_ARVO>9 || ARVO>(한도-merkki_ARVO)/10) return -1;
            ARVO=ARVO*10+merkki_ARVO;
        }
        return ARVO<=한도?ARVO:-1;
    }
    static boolean lukea_OSOITE(int INDEKSI) {
        if (INDEKSI>=kohde_LASKE()) return false;
        int ARVO=0, lohko_ARVO=0, numero_LASKE=0, piste_LASKE=0;
        for (int 순번=0; 순번<명령해석기.kesto_ARVO[INDEKSI]; 순번++) {
            int merkki_ARVO=명령해석기.tunnus_ARVO_eb540501[명령해석기.시작점[INDEKSI]+순번];
            if (merkki_ARVO=='.') { if (numero_LASKE==0 || ++piste_LASKE>3) return false; ARVO=(ARVO<<8)|lohko_ARVO; lohko_ARVO=numero_LASKE=0; }
            else { if (merkki_ARVO<'0' || merkki_ARVO>'9' || ++numero_LASKE>3) return false; lohko_ARVO=lohko_ARVO*10+merkki_ARVO-'0'; if(lohko_ARVO>255)return false; }
        }
        if (piste_LASKE!=3 || numero_LASKE==0) return false;
        OSOITE_ARVO=(ARVO<<8)|lohko_ARVO; return true;
    }
    static void kirjoitus_OSOITE(int ARVO) {
        단말.numero((ARVO>>>24)&255); 단말.문자('.'); 단말.numero((ARVO>>>16)&255); 단말.문자('.');
        단말.numero((ARVO>>>8)&255); 단말.문자('.'); 단말.numero(ARVO&255);
    }
    static void näyttää_verkko_tila() {
        단말.Kirjoitus(Taulu.verkko_tila(20,0)!=0?"en0: ":"sl0: "); 단말.Kirjoitus(Taulu.verkko_tila(3,0)!=0?"UP":"DOWN");
        단말.Kirjoitus(Taulu.verkko_tila(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Kirjoitus(Taulu.verkko_tila(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kirjoitus_OSOITE(Taulu.verkko_tila(0,0));
        단말.Kirjoitus(" netmask "); kirjoitus_OSOITE(Taulu.verkko_tila(1,0)); 단말.Kirjoitus(" gateway "); kirjoitus_OSOITE(Taulu.verkko_tila(2,0)); 단말.문자(10);
        단말.Kirjoitus("  RX packets "); 단말.numero(Taulu.verkko_tila(4,0)); 단말.Kirjoitus(" bytes "); 단말.numero(Taulu.verkko_tila(6,0));
        단말.Kirjoitus(" TX packets "); 단말.numero(Taulu.verkko_tila(5,0)); 단말.Kirjoitus(" bytes "); 단말.numero(Taulu.verkko_tila(7,0)); 단말.문자(10);
        numero_merkintä("  dropped ",Taulu.verkko_tila(8,0));
    }
    static void ryhmä_OSOITE(int Suorita_2) {
        if (kohde_LASKE()!=Suorita_2+3 || !lukea_OSOITE(Suorita_2)) { virhe_ARVO("사용법: ipconfig set OSOITE 주소가림 yhdyskäytävä_ARVO"); return; }
        int OSOITE=OSOITE_ARVO;
        if(!lukea_OSOITE(Suorita_2+1)){virhe_ARVO("Invalid IPv4 netmask");return;} int peite_ARVO=OSOITE_ARVO;
        if(!lukea_OSOITE(Suorita_2+2)){virhe_ARVO("Invalid IPv4 gateway");return;}
        int TULOS=Taulu.verkko_Asetukset(0,OSOITE,peite_ARVO,OSOITE_ARVO);
        if(TULOS<0) { VIRHE(TULOS); if(TULOS==-16)단말.Kirjoitus("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Kirjoitus("IPv4 configuration applied (until reboot)\n"); näyttää_verkko_tila(); }
    }
    static void verkko_komento(boolean IP_osoite) {
        if (kohde_LASKE()==1 || kohde_LASKE()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || kohde_LASKE()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { näyttää_verkko_tila();return; }
        if (IP_osoite && 같음(1,"route") && (kohde_LASKE()==2 || kohde_LASKE()==3&&같음(2,"show"))) { näyttää_polku();return; }
        if (같음(1,"set")) { ryhmä_OSOITE(2);return; }
        if (kohde_LASKE()==2 && (같음(1,"up") || 같음(1,"down"))) { Taulu.verkko_Asetukset(같음(1,"up")?1:2,0,0,0);näyttää_verkko_tila();return; }
        if (IP_osoite && kohde_LASKE()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Taulu.verkko_Asetukset(같음(5,"up")?1:2,0,0,0);näyttää_verkko_tila();return; }
        virhe_ARVO("사용법: ip [addr show|route show|set OSOITE 주소가림 yhdyskäytävä_ARVO|link set dev sl0 up|down]");
    }
    static void näyttää_polku() {
        단말.Kirjoitus("Destination Netmask Gateway Interface\n");
        kirjoitus_OSOITE(Taulu.verkko_tila(0,0)&Taulu.verkko_tila(1,0));단말.문자(' ');kirjoitus_OSOITE(Taulu.verkko_tila(1,0));단말.Kirjoitus(Taulu.verkko_tila(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Taulu.verkko_tila(2,0)!=0) {단말.Kirjoitus("0.0.0.0 0.0.0.0 ");kirjoitus_OSOITE(Taulu.verkko_tila(2,0));단말.Kirjoitus(Taulu.verkko_tila(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void näyttää_verkko() {
        단말.Kirjoitus("Proto Local Remote State Queued\n");
        for(int INDEKSI=0;INDEKSI<32;INDEKSI++) {
            int TYYPPI_alue=Taulu.verkko_tila(10,INDEKSI);if(TYYPPI_alue==0)continue;
            단말.Kirjoitus(TYYPPI_alue==1?"TCP ":"UDP ");kirjoitus_OSOITE(Taulu.verkko_tila(16,INDEKSI));단말.문자(':');단말.numero(Taulu.verkko_tila(11,INDEKSI));단말.문자(' ');
            kirjoitus_OSOITE(Taulu.verkko_tila(12,INDEKSI));단말.문자(':');단말.numero(Taulu.verkko_tila(13,INDEKSI));단말.문자(' ');
            int Tila_ARVO=Taulu.verkko_tila(14,INDEKSI);단말.Kirjoitus(TYYPPI_alue==2?"DATAGRAM":Tila_ARVO==1?"LISTEN":Tila_ARVO==2?"ESTABLISHED":Tila_ARVO==3?"CLOSE_WAIT":Tila_ARVO==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.numero(Taulu.verkko_tila(15,INDEKSI));단말.문자(10);
        }
        단말.Kirjoitus("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean odotustila(int 밀리초) {
        int Suorita_2=Taulu.밀리초();
        while(Taulu.밀리초()-Suorita_2<밀리초) {
            if(셸입출력.tietojärjestelmät_vuorovaikutteinen()!=0){int merkki_ARVO=Taulu.직렬읽기();if(merkki_ARVO==3 || merkki_ARVO=='q' || merkki_ARVO=='Q' || merkki_ARVO==27 || merkki_ARVO==-4096)return false;}
            Taulu.TUOTTO_suoritin();
        }
        return true;
    }
    static void testi_vastaus() {
        int toisto_LASKE=4, 제한=1000, tavoite=-1;
        for(int sijainti=1;sijainti<kohde_LASKE();sijainti++) {
            if(같음(sijainti,"-c")){toisto_LASKE=numero_ARVO(++sijainti,100);if(toisto_LASKE<1){virhe_ARVO("ping: -c 1..100");return;}}
            else if(같음(sijainti,"-W")){제한=numero_ARVO(++sijainti,10);if(제한<1){virhe_ARVO("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(tavoite<0)tavoite=sijainti;else{virhe_ARVO("사용법: ping [-c toisto_LASKE] [-W 초] IPv4");return;}
        }
        if(tavoite<0 || !lukea_OSOITE(tavoite)){virhe_ARVO("ping: an IPv4 address is required (DNS is not configured)");return;}
        int OSOITE=OSOITE_ARVO, 보낸수=0, SAATU_HINTA_LASKE=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Kirjoitus("PING ");kirjoitus_OSOITE(OSOITE);단말.Kirjoitus(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tilata_ARVO=1;tilata_ARVO<=toisto_LASKE && 계속;tilata_ARVO++) {
            int 처리값=Taulu.lähettää_vastaus(OSOITE,tilata_ARVO);
            if(처리값<0){VIRHE(처리값);break;}보낸수++;
            int Suorita_2=Taulu.밀리초();
            while(Taulu.lukea_vastaus(0)==-11 && Taulu.밀리초()-Suorita_2<제한)if(!odotustila(1)){계속=false;break;}
            if(!계속)break;
            if(Taulu.lukea_vastaus(0)==0){
                int AIKA_ARVO=Taulu.lukea_vastaus(1);SAATU_HINTA_LASKE++;누적+=AIKA_ARVO;if(AIKA_ARVO<최솟값)최솟값=AIKA_ARVO;if(AIKA_ARVO>최댓값)최댓값=AIKA_ARVO;
                단말.Kirjoitus("32 bytes from ");kirjoitus_OSOITE(OSOITE);단말.Kirjoitus(" seq=");단말.numero(tilata_ARVO);단말.Kirjoitus(" ttl=");단말.numero(Taulu.lukea_vastaus(2));단말.Kirjoitus(" time=");단말.numero(AIKA_ARVO);단말.Kirjoitus(" ms\n");
            }else{단말.Kirjoitus("Request timeout seq=");단말.numero(tilata_ARVO);단말.문자(10);}
            if(tilata_ARVO<toisto_LASKE)계속=odotustila(200);
        }
        단말.numero(보낸수);단말.Kirjoitus(" transmitted, ");단말.numero(SAATU_HINTA_LASKE);단말.Kirjoitus(" received, ");단말.numero(보낸수==0?100:(보낸수-SAATU_HINTA_LASKE)*100/보낸수);단말.Kirjoitus("% packet loss\n");
        if(SAATU_HINTA_LASKE>0){단말.Kirjoitus("rtt min/avg/max = ");단말.numero(최솟값);단말.문자('/');단말.numero(누적/SAATU_HINTA_LASKE);단말.문자('/');단말.numero(최댓값);단말.Kirjoitus(" ms\n");}
        명령해석기.TULOS=계속?(SAATU_HINTA_LASKE==0?1:0):130;
    }
    static void näyttää_tehtävä() { 단말.Kirjoitus("up ");단말.numero(Taulu.밀리초()/1000);단말.Kirjoitus(" seconds\n"); }
    static void näyttää_Muisti() {
        numero_merkintä("ARM RAM KiB (firmware): ",Taulu.kysely_Järjestelmä(0,0));
        numero_merkintä("Kernel image+BSS+stack KiB: ",Taulu.kysely_Järjestelmä(1,0));
        int summa_kapasiteetti=Taulu.kysely_Järjestelmä(2,0), 사용량=Taulu.kysely_Järjestelmä(3,0);
        단말.Kirjoitus("AOT heap KiB total/used/free: ");단말.numero(summa_kapasiteetti);단말.문자('/');단말.numero(사용량);단말.문자('/');단말.numero(summa_kapasiteetti-사용량);단말.문자(10);
        numero_merkintä("Framebuffer KiB: ",Taulu.kysely_Järjestelmä(4,0));
        numero_merkintä("EL0 arena+session reserve KiB: ",Taulu.kysely_Järjestelmä(5,0));
        int 매핑=0;for(int INDEKSI=0;INDEKSI<4;INDEKSI++)매핑+=Taulu.kysely_Järjestelmä(22,INDEKSI);
        numero_merkintä("EL0 mapped KiB: ",매핑);
        단말.Kirjoitus("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void näyttää_Tasks() {
        단말.Kirjoitus("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Kirjoitus("1 - RUN - - ");단말.numero(Taulu.밀리초());단말.Kirjoitus(" kernel/shell\n");
        for(int INDEKSI=1;INDEKSI<3;INDEKSI++)if(Taulu.tehtävä_Tila(INDEKSI)>0){단말.numero(INDEKSI+1);단말.Kirjoitus(" - READY 64 - - kernel-task\n");}
        for(int INDEKSI=0;INDEKSI<4;INDEKSI++){
            int Tila_ARVO=Taulu.kysely_Järjestelmä(20,INDEKSI);if(Tila_ARVO==0)continue;
            단말.numero(Taulu.kysely_Järjestelmä(21,INDEKSI));단말.문자(' ');단말.numero(INDEKSI);단말.Kirjoitus(Tila_ARVO==1?" RUN ":" SUSPENDED ");
            단말.numero(Taulu.kysely_Järjestelmä(22,INDEKSI));단말.문자(' ');단말.numero(Taulu.kysely_Järjestelmä(24,INDEKSI));단말.문자(' ');단말.numero(Taulu.kysely_Järjestelmä(23,INDEKSI));단말.문자(' ');
            for(int sijainti=0;sijainti<288;sijainti++){int tavu_ARVO=Taulu.kysely_Järjestelmä(25,INDEKSI+sijainti*4);if(tavu_ARVO==0)break;Taulu.직렬쓰기(tavu_ARVO);}단말.문자(10);
        }
    }
    static void näyttää_Tallennus() {
        int paikka_LASKE=0, data_LASKE=0;
        for(int INDEKSI=0;INDEKSI<Muisti_Files.Tiedosto_LASKE;INDEKSI++)if(Muisti_Files.이름길이[INDEKSI]>0 || Muisti_Files.viite_LASKE[INDEKSI]>0){paikka_LASKE++;data_LASKE+=Muisti_Files.kesto_ARVO[INDEKSI];}
        단말.Kirjoitus("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.numero(Muisti_Files.Tiedosto_LASKE*16384);단말.문자(' ');단말.numero(paikka_LASKE*16384);단말.문자(' ');단말.numero((Muisti_Files.Tiedosto_LASKE-paikka_LASKE)*16384);단말.문자(' ');단말.numero(data_LASKE);단말.문자(' ');단말.numero(paikka_LASKE);단말.문자('/');단말.numero(Muisti_Files.Tiedosto_LASKE);단말.Kirjoitus(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void näyttää_tila() {
        int toisto_LASKE=셸입출력.tietojärjestelmät_vuorovaikutteinen()!=0?0:1;
        if(kohde_LASKE()>1){if(kohde_LASKE()!=3 || !같음(1,"-n") || (toisto_LASKE=numero_ARVO(2,1000))<1){virhe_ARVO("사용법: top [-n 1..1000]; q/Ctrl+C로 lopeta_ohjelma");return;}}
        for(int JONO_ARVO=0;toisto_LASKE==0 || JONO_ARVO<toisto_LASKE;JONO_ARVO++){
            if(셸입출력.tietojärjestelmät_vuorovaikutteinen()!=0 && toisto_LASKE==0)단말.Kirjoitus("\u001b[2J\u001b[H");
            näyttää_tehtävä();näyttää_Muisti();näyttää_Tasks();
            if(toisto_LASKE!=0 && JONO_ARVO+1>=toisto_LASKE)break;
            if(!odotustila(1000))break;
        }
    }
    static String Vakio_Word(int INDEKSI) {
        if(INDEKSI==0)return "ipconfig";if(INDEKSI==1)return "ip";if(INDEKSI==2)return "ping";if(INDEKSI==3)return "route";if(INDEKSI==4)return "netstat";
        if(INDEKSI==5)return "ps";if(INDEKSI==6)return "top";if(INDEKSI==7)return "free";if(INDEKSI==8)return "df";if(INDEKSI==9)return "uptime";if(INDEKSI==10)return "poweroff";return "help";
    }
    static void näytä_ohje() {
        단말.Kirjoitus("--- Network / system commands ---\n");
        for(int INDEKSI=0;INDEKSI<12;INDEKSI++){단말.Kirjoitus(Vakio_Word(INDEKSI));단말.Kirjoitus(" / ");단말.Kirjoitus(관리명령.Word_SMS(INDEKSI));단말.Kirjoitus(" : ");단말.Kirjoitus(관리명령.설명(INDEKSI));단말.문자(10);}
        단말.Kirjoitus("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Kirjoitus("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Kirjoitus("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Suorita_komento() {
        int komento=-1;
        for(int INDEKSI=0;INDEKSI<12;INDEKSI++)if(같음(0,Vakio_Word(INDEKSI)) || 같음(0,관리명령.Word_SMS(INDEKSI)))komento=INDEKSI;
        if(같음(0,"ifconfig"))komento=0;if(같음(0,"ss"))komento=4;
        if(komento<0)return false;
        if(komento==11){if(같음(1,"net") || 같음(1,"system"))näytä_ohje();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.näytä_ohje();return true;}
        if(komento==0 || komento==1)verkko_komento(komento==1);
        else if(komento==2)testi_vastaus();
        else if(komento==6)näyttää_tila();
        else if(kohde_LASKE()!=1){virhe_ARVO("This command takes no arguments; help system");}
        else if(komento==3)näyttää_polku();else if(komento==4)näyttää_verkko();else if(komento==5)näyttää_Tasks();else if(komento==7)näyttää_Muisti();else if(komento==8)näyttää_Tallennus();else if(komento==9)näyttää_tehtävä();
        else if(komento==10)Taulu.전원끄기();
        return true;
    }
}
