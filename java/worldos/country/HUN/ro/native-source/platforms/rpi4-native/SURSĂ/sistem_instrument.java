// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_date nucleu_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorie_VALUE·RAM depozit_rădăcină 관리 Comandă. */
public final class sistem_instrument {
    static int adresa_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int element_COUNT() { return 명령해석기.token_COUNT; }
    static void eroare_VALUE(String 안내) { 명령해석기.KR=2; 단말.Scriere(안내); 단말.문자(10); }
    static void eroare(int VALUE) { 명령해석기.eroare(VALUE); }
    static void 수항목(String Nume, int VALUE) { 단말.Scriere(Nume); 단말.수(VALUE); 단말.문자(10); }
    static int cifră_VALUE(int INDEX, int 한도) {
        if (INDEX>=element_COUNT() || 명령해석기.lungime_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.lungime_VALUE[INDEX]; 순번++) {
            int caracter_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (caracter_VALUE<0 || caracter_VALUE>9 || VALUE>(한도-caracter_VALUE)/10) return -1;
            VALUE=VALUE*10+caracter_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=element_COUNT()) return false;
        int VALUE=0, bloc_VALUE=0, cifră_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.lungime_VALUE[INDEX]; 순번++) {
            int caracter_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (caracter_VALUE=='.') { if (cifră_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|bloc_VALUE; bloc_VALUE=cifră_COUNT=0; }
            else { if (caracter_VALUE<'0' || caracter_VALUE>'9' || ++cifră_COUNT>3) return false; bloc_VALUE=bloc_VALUE*10+caracter_VALUE-'0'; if(bloc_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || cifră_COUNT==0) return false;
        adresa_VALUE=(VALUE<<8)|bloc_VALUE; return true;
    }
    static void scriere_adresa(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void afișa_rețea_stare() {
        단말.Scriere(Avizier.rețea_stare(20,0)!=0?"en0: ":"sl0: "); 단말.Scriere(Avizier.rețea_stare(3,0)!=0?"UP":"DOWN");
        단말.Scriere(Avizier.rețea_stare(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Scriere(Avizier.rețea_stare(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); scriere_adresa(Avizier.rețea_stare(0,0));
        단말.Scriere(" netmask "); scriere_adresa(Avizier.rețea_stare(1,0)); 단말.Scriere(" gateway "); scriere_adresa(Avizier.rețea_stare(2,0)); 단말.문자(10);
        단말.Scriere("  RX packets "); 단말.수(Avizier.rețea_stare(4,0)); 단말.Scriere(" bytes "); 단말.수(Avizier.rețea_stare(6,0));
        단말.Scriere(" TX packets "); 단말.수(Avizier.rețea_stare(5,0)); 단말.Scriere(" bytes "); 단말.수(Avizier.rețea_stare(7,0)); 단말.문자(10);
        수항목("  dropped ",Avizier.rețea_stare(8,0));
    }
    static void set_adresa(int Pornește) {
        if (element_COUNT()!=Pornește+3 || !주소읽기(Pornește)) { eroare_VALUE("사용법: ipconfig set adresa 주소가림 gateway_VALUE"); return; }
        int adresa=adresa_VALUE;
        if(!주소읽기(Pornește+1)){eroare_VALUE("Invalid IPv4 netmask");return;} int mască_VALUE=adresa_VALUE;
        if(!주소읽기(Pornește+2)){eroare_VALUE("Invalid IPv4 gateway");return;}
        int KR=Avizier.rețea_Setări(0,adresa,mască_VALUE,adresa_VALUE);
        if(KR<0) { eroare(KR); if(KR==-16)단말.Scriere("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Scriere("IPv4 configuration applied (until reboot)\n"); afișa_rețea_stare(); }
    }
    static void rețea_comandă(boolean adresă_IP) {
        if (element_COUNT()==1 || element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { afișa_rețea_stare();return; }
        if (adresă_IP && 같음(1,"route") && (element_COUNT()==2 || element_COUNT()==3&&같음(2,"show"))) { afișa_cale();return; }
        if (같음(1,"set")) { set_adresa(2);return; }
        if (element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Avizier.rețea_Setări(같음(1,"up")?1:2,0,0,0);afișa_rețea_stare();return; }
        if (adresă_IP && element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Avizier.rețea_Setări(같음(5,"up")?1:2,0,0,0);afișa_rețea_stare();return; }
        eroare_VALUE("사용법: ip [addr show|route show|set adresa 주소가림 gateway_VALUE|link set dev sl0 up|down]");
    }
    static void afișa_cale() {
        단말.Scriere("Destination Netmask Gateway Interface\n");
        scriere_adresa(Avizier.rețea_stare(0,0)&Avizier.rețea_stare(1,0));단말.문자(' ');scriere_adresa(Avizier.rețea_stare(1,0));단말.Scriere(Avizier.rețea_stare(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Avizier.rețea_stare(2,0)!=0) {단말.Scriere("0.0.0.0 0.0.0.0 ");scriere_adresa(Avizier.rețea_stare(2,0));단말.Scriere(Avizier.rețea_stare(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void afișa_rețea() {
        단말.Scriere("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int Tip_zonă=Avizier.rețea_stare(10,INDEX);if(Tip_zonă==0)continue;
            단말.Scriere(Tip_zonă==1?"TCP ":"UDP ");scriere_adresa(Avizier.rețea_stare(16,INDEX));단말.문자(':');단말.수(Avizier.rețea_stare(11,INDEX));단말.문자(' ');
            scriere_adresa(Avizier.rețea_stare(12,INDEX));단말.문자(':');단말.수(Avizier.rețea_stare(13,INDEX));단말.문자(' ');
            int Stare_VALUE=Avizier.rețea_stare(14,INDEX);단말.Scriere(Tip_zonă==2?"DATAGRAM":Stare_VALUE==1?"LISTEN":Stare_VALUE==2?"ESTABLISHED":Stare_VALUE==3?"CLOSE_WAIT":Stare_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Avizier.rețea_stare(15,INDEX));단말.문자(10);
        }
        단말.Scriere("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean stare_de_așteptare(int 밀리초) {
        int Pornește=Avizier.밀리초();
        while(Avizier.밀리초()-Pornește<밀리초) {
            if(셸입출력.대화가능()!=0){int caracter_VALUE=Avizier.직렬읽기();if(caracter_VALUE==3 || caracter_VALUE=='q' || caracter_VALUE=='Q' || caracter_VALUE==27 || caracter_VALUE==-4096)return false;}
            Avizier.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, țintă=-1;
        for(int index_de_poziție=1;index_de_poziție<element_COUNT();index_de_poziție++) {
            if(같음(index_de_poziție,"-c")){횟수=cifră_VALUE(++index_de_poziție,100);if(횟수<1){eroare_VALUE("ping: -c 1..100");return;}}
            else if(같음(index_de_poziție,"-W")){제한=cifră_VALUE(++index_de_poziție,10);if(제한<1){eroare_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(țintă<0)țintă=index_de_poziție;else{eroare_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(țintă<0 || !주소읽기(țintă)){eroare_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int adresa=adresa_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Scriere("PING ");scriere_adresa(adresa);단말.Scriere(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordine_VALUE=1;ordine_VALUE<=횟수 && 계속;ordine_VALUE++) {
            int 처리값=Avizier.trimite_răspuns(adresa,ordine_VALUE);
            if(처리값<0){eroare(처리값);break;}보낸수++;
            int Pornește=Avizier.밀리초();
            while(Avizier.응답읽기(0)==-11 && Avizier.밀리초()-Pornește<제한)if(!stare_de_așteptare(1)){계속=false;break;}
            if(!계속)break;
            if(Avizier.응답읽기(0)==0){
                int oră_VALUE=Avizier.응답읽기(1);RECEIVED_COUNT++;누적+=oră_VALUE;if(oră_VALUE<최솟값)최솟값=oră_VALUE;if(oră_VALUE>최댓값)최댓값=oră_VALUE;
                단말.Scriere("32 bytes from ");scriere_adresa(adresa);단말.Scriere(" seq=");단말.수(ordine_VALUE);단말.Scriere(" ttl=");단말.수(Avizier.응답읽기(2));단말.Scriere(" time=");단말.수(oră_VALUE);단말.Scriere(" ms\n");
            }else{단말.Scriere("Request timeout seq=");단말.수(ordine_VALUE);단말.문자(10);}
            if(ordine_VALUE<횟수)계속=stare_de_așteptare(200);
        }
        단말.수(보낸수);단말.Scriere(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Scriere(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Scriere("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Scriere("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Scriere(" ms\n");}
        명령해석기.KR=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void afișa_Activitate() { 단말.Scriere("up ");단말.수(Avizier.밀리초()/1000);단말.Scriere(" seconds\n"); }
    static void afișa_Memorie() {
        수항목("ARM RAM KiB (firmware): ",Avizier.interoga_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Avizier.interoga_sistem(1,0));
        int total_capacitate=Avizier.interoga_sistem(2,0), 사용량=Avizier.interoga_sistem(3,0);
        단말.Scriere("AOT heap KiB total/used/free: ");단말.수(total_capacitate);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(total_capacitate-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Avizier.interoga_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Avizier.interoga_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Avizier.interoga_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Scriere("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void afișa_Tasks() {
        단말.Scriere("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Scriere("1 - RUN - - ");단말.수(Avizier.밀리초());단말.Scriere(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Avizier.sarcină_Stare(INDEX)>0){단말.수(INDEX+1);단말.Scriere(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Stare_VALUE=Avizier.interoga_sistem(20,INDEX);if(Stare_VALUE==0)continue;
            단말.수(Avizier.interoga_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Scriere(Stare_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Avizier.interoga_sistem(22,INDEX));단말.문자(' ');단말.수(Avizier.interoga_sistem(24,INDEX));단말.문자(' ');단말.수(Avizier.interoga_sistem(23,INDEX));단말.문자(' ');
            for(int index_de_poziție=0;index_de_poziție<288;index_de_poziție++){int byte_VALUE=Avizier.interoga_sistem(25,INDEX+index_de_poziție*4);if(byte_VALUE==0)break;Avizier.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void afișa_Stocare() {
        int 칸수=0, date_COUNT=0;
        for(int INDEX=0;INDEX<Memorie_Fișiere.Fișier_COUNT;INDEX++)if(Memorie_Fișiere.이름길이[INDEX]>0 || Memorie_Fișiere.referință_COUNT[INDEX]>0){칸수++;date_COUNT+=Memorie_Fișiere.lungime_VALUE[INDEX];}
        단말.Scriere("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorie_Fișiere.Fișier_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memorie_Fișiere.Fișier_COUNT-칸수)*16384);단말.문자(' ');단말.수(date_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memorie_Fișiere.Fișier_COUNT);단말.Scriere(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void afișa_stare() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(element_COUNT()>1){if(element_COUNT()!=3 || !같음(1,"-n") || (횟수=cifră_VALUE(2,1000))<1){eroare_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 ieșire_program");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Scriere("\u001b[2J\u001b[H");
            afișa_Activitate();afișa_Memorie();afișa_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!stare_de_așteptare(1000))break;
        }
    }
    static String Standard_Word(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void afișa_ajutor() {
        단말.Scriere("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Scriere(Standard_Word(INDEX));단말.Scriere(" / ");단말.Scriere(관리명령.Word_SMS(INDEX));단말.Scriere(" : ");단말.Scriere(관리명령.설명(INDEX));단말.문자(10);}
        단말.Scriere("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Scriere("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Scriere("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean executa_comandă() {
        int Comandă=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,Standard_Word(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Comandă=INDEX;
        if(같음(0,"ifconfig"))Comandă=0;if(같음(0,"ss"))Comandă=4;
        if(Comandă<0)return false;
        if(Comandă==11){if(같음(1,"net") || 같음(1,"system"))afișa_ajutor();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.afișa_ajutor();return true;}
        if(Comandă==0 || Comandă==1)rețea_comandă(Comandă==1);
        else if(Comandă==2)응답시험();
        else if(Comandă==6)afișa_stare();
        else if(element_COUNT()!=1){eroare_VALUE("This command takes no arguments; help system");}
        else if(Comandă==3)afișa_cale();else if(Comandă==4)afișa_rețea();else if(Comandă==5)afișa_Tasks();else if(Comandă==7)afișa_Memorie();else if(Comandă==8)afișa_Stocare();else if(Comandă==9)afișa_Activitate();
        else if(Comandă==10)Avizier.전원끄기();
        return true;
    }
}
