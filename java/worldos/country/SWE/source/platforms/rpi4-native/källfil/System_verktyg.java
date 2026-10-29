// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** verklig_data kärna_värde 상태를 읽는 IPv4·ICMP·작업·Minne_värde·RAM centrallager_rot 관리 kommando. */
public final class System_verktyg {
    static int ADRESS_värde;
    static boolean 같음(int INDEX, String Ord_SMS) { return 명령해석기.같음(INDEX, Ord_SMS); }
    static int objekt_ANTAL() { return 명령해석기.kod_ANTAL; }
    static void fel_värde(String VIKTIGT_eb81d7d9) { 명령해석기.RESULTAT=2; 단말.Skriv(VIKTIGT_eb81d7d9); 단말.문자(10); }
    static void fel(int värde) { 명령해석기.fel(värde); }
    static void nummer_post(String Namn, int värde) { 단말.Skriv(Namn); 단말.nummer(värde); 단말.문자(10); }
    static int siffra_värde(int INDEX, int 한도) {
        if (INDEX>=objekt_ANTAL() || 명령해석기.längd_värde[INDEX]==0) return -1;
        int värde=0;
        for (int 순번=0; 순번<명령해석기.längd_värde[INDEX]; 순번++) {
            int tecken_värde=명령해석기.kod_värde[명령해석기.시작점[INDEX]+순번]-'0';
            if (tecken_värde<0 || tecken_värde>9 || värde>(한도-tecken_värde)/10) return -1;
            värde=värde*10+tecken_värde;
        }
        return värde<=한도?värde:-1;
    }
    static boolean läsa_ADRESS(int INDEX) {
        if (INDEX>=objekt_ANTAL()) return false;
        int värde=0, segment_värde=0, siffra_ANTAL=0, peka_ANTAL=0;
        for (int 순번=0; 순번<명령해석기.längd_värde[INDEX]; 순번++) {
            int tecken_värde=명령해석기.kod_värde[명령해석기.시작점[INDEX]+순번];
            if (tecken_värde=='.') { if (siffra_ANTAL==0 || ++peka_ANTAL>3) return false; värde=(värde<<8)|segment_värde; segment_värde=siffra_ANTAL=0; }
            else { if (tecken_värde<'0' || tecken_värde>'9' || ++siffra_ANTAL>3) return false; segment_värde=segment_värde*10+tecken_värde-'0'; if(segment_värde>255)return false; }
        }
        if (peka_ANTAL!=3 || siffra_ANTAL==0) return false;
        ADRESS_värde=(värde<<8)|segment_värde; return true;
    }
    static void skriva_ADRESS(int värde) {
        단말.nummer((värde>>>24)&255); 단말.문자('.'); 단말.nummer((värde>>>16)&255); 단말.문자('.');
        단말.nummer((värde>>>8)&255); 단말.문자('.'); 단말.nummer(värde&255);
    }
    static void visa_nätverk_status() {
        단말.Skriv(Tavla.nätverk_status(20,0)!=0?"en0: ":"sl0: "); 단말.Skriv(Tavla.nätverk_status(3,0)!=0?"UP":"DOWN");
        단말.Skriv(Tavla.nätverk_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skriv(Tavla.nätverk_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skriva_ADRESS(Tavla.nätverk_status(0,0));
        단말.Skriv(" netmask "); skriva_ADRESS(Tavla.nätverk_status(1,0)); 단말.Skriv(" gateway "); skriva_ADRESS(Tavla.nätverk_status(2,0)); 단말.문자(10);
        단말.Skriv("  RX packets "); 단말.nummer(Tavla.nätverk_status(4,0)); 단말.Skriv(" bytes "); 단말.nummer(Tavla.nätverk_status(6,0));
        단말.Skriv(" TX packets "); 단말.nummer(Tavla.nätverk_status(5,0)); 단말.Skriv(" bytes "); 단말.nummer(Tavla.nätverk_status(7,0)); 단말.문자(10);
        nummer_post("  dropped ",Tavla.nätverk_status(8,0));
    }
    static void uppsättning_ADRESS(int Kör) {
        if (objekt_ANTAL()!=Kör+3 || !läsa_ADRESS(Kör)) { fel_värde("사용법: ipconfig set Adress 주소가림 gateway_värde"); return; }
        int Adress=ADRESS_värde;
        if(!läsa_ADRESS(Kör+1)){fel_värde("Invalid IPv4 netmask");return;} int mask_värde=ADRESS_värde;
        if(!läsa_ADRESS(Kör+2)){fel_värde("Invalid IPv4 gateway");return;}
        int RESULTAT=Tavla.nätverk_Inställningar(0,Adress,mask_värde,ADRESS_värde);
        if(RESULTAT<0) { fel(RESULTAT); if(RESULTAT==-16)단말.Skriv("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skriv("IPv4 configuration applied (until reboot)\n"); visa_nätverk_status(); }
    }
    static void nätverk_kommando(boolean IP_adress) {
        if (objekt_ANTAL()==1 || objekt_ANTAL()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || objekt_ANTAL()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { visa_nätverk_status();return; }
        if (IP_adress && 같음(1,"route") && (objekt_ANTAL()==2 || objekt_ANTAL()==3&&같음(2,"show"))) { visa_väg();return; }
        if (같음(1,"set")) { uppsättning_ADRESS(2);return; }
        if (objekt_ANTAL()==2 && (같음(1,"up") || 같음(1,"down"))) { Tavla.nätverk_Inställningar(같음(1,"up")?1:2,0,0,0);visa_nätverk_status();return; }
        if (IP_adress && objekt_ANTAL()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tavla.nätverk_Inställningar(같음(5,"up")?1:2,0,0,0);visa_nätverk_status();return; }
        fel_värde("사용법: ip [addr show|route show|set Adress 주소가림 gateway_värde|link set dev sl0 up|down]");
    }
    static void visa_väg() {
        단말.Skriv("Destination Netmask Gateway Interface\n");
        skriva_ADRESS(Tavla.nätverk_status(0,0)&Tavla.nätverk_status(1,0));단말.문자(' ');skriva_ADRESS(Tavla.nätverk_status(1,0));단말.Skriv(Tavla.nätverk_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tavla.nätverk_status(2,0)!=0) {단말.Skriv("0.0.0.0 0.0.0.0 ");skriva_ADRESS(Tavla.nätverk_status(2,0));단말.Skriv(Tavla.nätverk_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void visa_nätverk() {
        단말.Skriv("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int Typ_område=Tavla.nätverk_status(10,INDEX);if(Typ_område==0)continue;
            단말.Skriv(Typ_område==1?"TCP ":"UDP ");skriva_ADRESS(Tavla.nätverk_status(16,INDEX));단말.문자(':');단말.nummer(Tavla.nätverk_status(11,INDEX));단말.문자(' ');
            skriva_ADRESS(Tavla.nätverk_status(12,INDEX));단말.문자(':');단말.nummer(Tavla.nätverk_status(13,INDEX));단말.문자(' ');
            int status_värde=Tavla.nätverk_status(14,INDEX);단말.Skriv(Typ_område==2?"DATAGRAM":status_värde==1?"LISTEN":status_värde==2?"ESTABLISHED":status_värde==3?"CLOSE_WAIT":status_värde==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.nummer(Tavla.nätverk_status(15,INDEX));단말.문자(10);
        }
        단말.Skriv("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean tillståndet_Vänta(int 밀리초) {
        int Kör=Tavla.밀리초();
        while(Tavla.밀리초()-Kör<밀리초) {
            if(셸입출력.informationsteknik_interaktiv()!=0){int tecken_värde=Tavla.직렬읽기();if(tecken_värde==3 || tecken_värde=='q' || tecken_värde=='Q' || tecken_värde==27 || tecken_värde==-4096)return false;}
            Tavla.NOMAVK_CPU();
        }
        return true;
    }
    static void test_svar() {
        int repetition_ANTAL=4, 제한=1000, mål=-1;
        for(int positionsindex=1;positionsindex<objekt_ANTAL();positionsindex++) {
            if(같음(positionsindex,"-c")){repetition_ANTAL=siffra_värde(++positionsindex,100);if(repetition_ANTAL<1){fel_värde("ping: -c 1..100");return;}}
            else if(같음(positionsindex,"-W")){제한=siffra_värde(++positionsindex,10);if(제한<1){fel_värde("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mål<0)mål=positionsindex;else{fel_värde("사용법: ping [-c repetition_ANTAL] [-W 초] IPv4");return;}
        }
        if(mål<0 || !läsa_ADRESS(mål)){fel_värde("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Adress=ADRESS_värde, 보낸수=0, BELOPP_ANTAL=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skriv("PING ");skriva_ADRESS(Adress);단말.Skriv(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int order_värde=1;order_värde<=repetition_ANTAL && 계속;order_värde++) {
            int 처리값=Tavla.skicka_svar(Adress,order_värde);
            if(처리값<0){fel(처리값);break;}보낸수++;
            int Kör=Tavla.밀리초();
            while(Tavla.läsa_svar(0)==-11 && Tavla.밀리초()-Kör<제한)if(!tillståndet_Vänta(1)){계속=false;break;}
            if(!계속)break;
            if(Tavla.läsa_svar(0)==0){
                int tid_värde=Tavla.läsa_svar(1);BELOPP_ANTAL++;누적+=tid_värde;if(tid_värde<최솟값)최솟값=tid_värde;if(tid_värde>최댓값)최댓값=tid_värde;
                단말.Skriv("32 bytes from ");skriva_ADRESS(Adress);단말.Skriv(" seq=");단말.nummer(order_värde);단말.Skriv(" ttl=");단말.nummer(Tavla.läsa_svar(2));단말.Skriv(" time=");단말.nummer(tid_värde);단말.Skriv(" ms\n");
            }else{단말.Skriv("Request timeout seq=");단말.nummer(order_värde);단말.문자(10);}
            if(order_värde<repetition_ANTAL)계속=tillståndet_Vänta(200);
        }
        단말.nummer(보낸수);단말.Skriv(" transmitted, ");단말.nummer(BELOPP_ANTAL);단말.Skriv(" received, ");단말.nummer(보낸수==0?100:(보낸수-BELOPP_ANTAL)*100/보낸수);단말.Skriv("% packet loss\n");
        if(BELOPP_ANTAL>0){단말.Skriv("rtt min/avg/max = ");단말.nummer(최솟값);단말.문자('/');단말.nummer(누적/BELOPP_ANTAL);단말.문자('/');단말.nummer(최댓값);단말.Skriv(" ms\n");}
        명령해석기.RESULTAT=계속?(BELOPP_ANTAL==0?1:0):130;
    }
    static void visa_Aktivitet() { 단말.Skriv("up ");단말.nummer(Tavla.밀리초()/1000);단말.Skriv(" seconds\n"); }
    static void visa_Minne() {
        nummer_post("ARM RAM KiB (firmware): ",Tavla.fråga_System(0,0));
        nummer_post("Kernel image+BSS+stack KiB: ",Tavla.fråga_System(1,0));
        int summa_kapacitet=Tavla.fråga_System(2,0), 사용량=Tavla.fråga_System(3,0);
        단말.Skriv("AOT heap KiB total/used/free: ");단말.nummer(summa_kapacitet);단말.문자('/');단말.nummer(사용량);단말.문자('/');단말.nummer(summa_kapacitet-사용량);단말.문자(10);
        nummer_post("Framebuffer KiB: ",Tavla.fråga_System(4,0));
        nummer_post("EL0 arena+session reserve KiB: ",Tavla.fråga_System(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tavla.fråga_System(22,INDEX);
        nummer_post("EL0 mapped KiB: ",매핑);
        단말.Skriv("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void visa_Tasks() {
        단말.Skriv("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skriv("1 - RUN - - ");단말.nummer(Tavla.밀리초());단말.Skriv(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tavla.uppgift_status(INDEX)>0){단말.nummer(INDEX+1);단말.Skriv(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int status_värde=Tavla.fråga_System(20,INDEX);if(status_värde==0)continue;
            단말.nummer(Tavla.fråga_System(21,INDEX));단말.문자(' ');단말.nummer(INDEX);단말.Skriv(status_värde==1?" RUN ":" SUSPENDED ");
            단말.nummer(Tavla.fråga_System(22,INDEX));단말.문자(' ');단말.nummer(Tavla.fråga_System(24,INDEX));단말.문자(' ');단말.nummer(Tavla.fråga_System(23,INDEX));단말.문자(' ');
            for(int positionsindex=0;positionsindex<288;positionsindex++){int byte_värde=Tavla.fråga_System(25,INDEX+positionsindex*4);if(byte_värde==0)break;Tavla.직렬쓰기(byte_värde);}단말.문자(10);
        }
    }
    static void visa_minne() {
        int fack_ANTAL=0, data_ANTAL=0;
        for(int INDEX=0;INDEX<Minne_Filer.fil_ANTAL;INDEX++)if(Minne_Filer.이름길이[INDEX]>0 || Minne_Filer.referens_ANTAL[INDEX]>0){fack_ANTAL++;data_ANTAL+=Minne_Filer.längd_värde[INDEX];}
        단말.Skriv("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.nummer(Minne_Filer.fil_ANTAL*16384);단말.문자(' ');단말.nummer(fack_ANTAL*16384);단말.문자(' ');단말.nummer((Minne_Filer.fil_ANTAL-fack_ANTAL)*16384);단말.문자(' ');단말.nummer(data_ANTAL);단말.문자(' ');단말.nummer(fack_ANTAL);단말.문자('/');단말.nummer(Minne_Filer.fil_ANTAL);단말.Skriv(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void visa_status_bf9821b5() {
        int repetition_ANTAL=셸입출력.informationsteknik_interaktiv()!=0?0:1;
        if(objekt_ANTAL()>1){if(objekt_ANTAL()!=3 || !같음(1,"-n") || (repetition_ANTAL=siffra_värde(2,1000))<1){fel_värde("사용법: top [-n 1..1000]; q/Ctrl+C로 avsluta_app");return;}}
        for(int SEKVENS_värde=0;repetition_ANTAL==0 || SEKVENS_värde<repetition_ANTAL;SEKVENS_värde++){
            if(셸입출력.informationsteknik_interaktiv()!=0 && repetition_ANTAL==0)단말.Skriv("\u001b[2J\u001b[H");
            visa_Aktivitet();visa_Minne();visa_Tasks();
            if(repetition_ANTAL!=0 && SEKVENS_värde+1>=repetition_ANTAL)break;
            if(!tillståndet_Vänta(1000))break;
        }
    }
    static String Standard_Ord(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void visa_hjälp() {
        단말.Skriv("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Skriv(Standard_Ord(INDEX));단말.Skriv(" / ");단말.Skriv(관리명령.Ord_SMS(INDEX));단말.Skriv(" : ");단말.Skriv(관리명령.설명(INDEX));단말.문자(10);}
        단말.Skriv("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skriv("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skriv("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean köra_kommando() {
        int kommando=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,Standard_Ord(INDEX)) || 같음(0,관리명령.Ord_SMS(INDEX)))kommando=INDEX;
        if(같음(0,"ifconfig"))kommando=0;if(같음(0,"ss"))kommando=4;
        if(kommando<0)return false;
        if(kommando==11){if(같음(1,"net") || 같음(1,"system"))visa_hjälp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.visa_hjälp();return true;}
        if(kommando==0 || kommando==1)nätverk_kommando(kommando==1);
        else if(kommando==2)test_svar();
        else if(kommando==6)visa_status_bf9821b5();
        else if(objekt_ANTAL()!=1){fel_värde("This command takes no arguments; help system");}
        else if(kommando==3)visa_väg();else if(kommando==4)visa_nätverk();else if(kommando==5)visa_Tasks();else if(kommando==7)visa_Minne();else if(kommando==8)visa_minne();else if(kommando==9)visa_Aktivitet();
        else if(kommando==10)Tavla.전원끄기();
        return true;
    }
}
