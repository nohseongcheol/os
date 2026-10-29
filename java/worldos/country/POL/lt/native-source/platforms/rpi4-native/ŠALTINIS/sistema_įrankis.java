// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktinis_duomenys branduolys_VALUE 상태를 읽는 IPv4·ICMP·작업·atmintis_VALUE·RAM saugykla_šaknis 관리 Komanda. */
public final class sistema_įrankis {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int prekė_COUNT() { return 명령해석기.žetonas_COUNT; }
    static void triktis_VALUE(String 안내) { 명령해석기.REZULTATAS=2; 단말.Rašymas(안내); 단말.문자(10); }
    static void KLAIDA(int VALUE) { 명령해석기.KLAIDA(VALUE); }
    static void numeris_įrašas(String Pavadinimas_2, int VALUE) { 단말.Rašymas(Pavadinimas_2); 단말.numeris(VALUE); 단말.문자(10); }
    static int skaitmuo_VALUE(int INDEX, int 한도) {
        if (INDEX>=prekė_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int simbolis_VALUE_068c2631=명령해석기.žetonas_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (simbolis_VALUE_068c2631<0 || simbolis_VALUE_068c2631>9 || VALUE>(한도-simbolis_VALUE_068c2631)/10) return -1;
            VALUE=VALUE*10+simbolis_VALUE_068c2631;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=prekė_COUNT()) return false;
        int VALUE=0, segmentas_VALUE=0, skaitmuo_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int simbolis_VALUE_068c2631=명령해석기.žetonas_VALUE[명령해석기.시작점[INDEX]+순번];
            if (simbolis_VALUE_068c2631=='.') { if (skaitmuo_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|segmentas_VALUE; segmentas_VALUE=skaitmuo_COUNT=0; }
            else { if (simbolis_VALUE_068c2631<'0' || simbolis_VALUE_068c2631>'9' || ++skaitmuo_COUNT>3) return false; segmentas_VALUE=segmentas_VALUE*10+simbolis_VALUE_068c2631-'0'; if(segmentas_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || skaitmuo_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|segmentas_VALUE; return true;
    }
    static void rašymas_ADDRESS(int VALUE) {
        단말.numeris((VALUE>>>24)&255); 단말.문자('.'); 단말.numeris((VALUE>>>16)&255); 단말.문자('.');
        단말.numeris((VALUE>>>8)&255); 단말.문자('.'); 단말.numeris(VALUE&255);
    }
    static void laida_tinklas_būsena() {
        단말.Rašymas(Lenta.tinklas_būsena(20,0)!=0?"en0: ":"sl0: "); 단말.Rašymas(Lenta.tinklas_būsena(3,0)!=0?"UP":"DOWN");
        단말.Rašymas(Lenta.tinklas_būsena(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Rašymas(Lenta.tinklas_būsena(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); rašymas_ADDRESS(Lenta.tinklas_būsena(0,0));
        단말.Rašymas(" netmask "); rašymas_ADDRESS(Lenta.tinklas_būsena(1,0)); 단말.Rašymas(" gateway "); rašymas_ADDRESS(Lenta.tinklas_būsena(2,0)); 단말.문자(10);
        단말.Rašymas("  RX packets "); 단말.numeris(Lenta.tinklas_būsena(4,0)); 단말.Rašymas(" bytes "); 단말.numeris(Lenta.tinklas_būsena(6,0));
        단말.Rašymas(" TX packets "); 단말.numeris(Lenta.tinklas_būsena(5,0)); 단말.Rašymas(" bytes "); 단말.numeris(Lenta.tinklas_būsena(7,0)); 단말.문자(10);
        numeris_įrašas("  dropped ",Lenta.tinklas_būsena(8,0));
    }
    static void rinkinys_ADDRESS(int Paleisti) {
        if (prekė_COUNT()!=Paleisti+3 || !주소읽기(Paleisti)) { triktis_VALUE("사용법: ipconfig set ADDRESS 주소가림 šliuzas_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(Paleisti+1)){triktis_VALUE("Invalid IPv4 netmask");return;} int šablonas_VALUE=ADDRESS_VALUE;
        if(!주소읽기(Paleisti+2)){triktis_VALUE("Invalid IPv4 gateway");return;}
        int REZULTATAS=Lenta.tinklas_Parametrai(0,ADDRESS,šablonas_VALUE,ADDRESS_VALUE);
        if(REZULTATAS<0) { KLAIDA(REZULTATAS); if(REZULTATAS==-16)단말.Rašymas("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Rašymas("IPv4 configuration applied (until reboot)\n"); laida_tinklas_būsena(); }
    }
    static void tinklas_komanda(boolean IP_adresas) {
        if (prekė_COUNT()==1 || prekė_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || prekė_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { laida_tinklas_būsena();return; }
        if (IP_adresas && 같음(1,"route") && (prekė_COUNT()==2 || prekė_COUNT()==3&&같음(2,"show"))) { laida_kelias();return; }
        if (같음(1,"set")) { rinkinys_ADDRESS(2);return; }
        if (prekė_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Lenta.tinklas_Parametrai(같음(1,"up")?1:2,0,0,0);laida_tinklas_būsena();return; }
        if (IP_adresas && prekė_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Lenta.tinklas_Parametrai(같음(5,"up")?1:2,0,0,0);laida_tinklas_būsena();return; }
        triktis_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 šliuzas_VALUE|link set dev sl0 up|down]");
    }
    static void laida_kelias() {
        단말.Rašymas("Destination Netmask Gateway Interface\n");
        rašymas_ADDRESS(Lenta.tinklas_būsena(0,0)&Lenta.tinklas_būsena(1,0));단말.문자(' ');rašymas_ADDRESS(Lenta.tinklas_būsena(1,0));단말.Rašymas(Lenta.tinklas_būsena(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Lenta.tinklas_būsena(2,0)!=0) {단말.Rašymas("0.0.0.0 0.0.0.0 ");rašymas_ADDRESS(Lenta.tinklas_būsena(2,0));단말.Rašymas(Lenta.tinklas_būsena(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void laida_tinklas() {
        단말.Rašymas("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_sritis=Lenta.tinklas_būsena(10,INDEX);if(TYPE_sritis==0)continue;
            단말.Rašymas(TYPE_sritis==1?"TCP ":"UDP ");rašymas_ADDRESS(Lenta.tinklas_būsena(16,INDEX));단말.문자(':');단말.numeris(Lenta.tinklas_būsena(11,INDEX));단말.문자(' ');
            rašymas_ADDRESS(Lenta.tinklas_būsena(12,INDEX));단말.문자(':');단말.numeris(Lenta.tinklas_būsena(13,INDEX));단말.문자(' ');
            int Būsena_VALUE=Lenta.tinklas_būsena(14,INDEX);단말.Rašymas(TYPE_sritis==2?"DATAGRAM":Būsena_VALUE==1?"LISTEN":Būsena_VALUE==2?"ESTABLISHED":Būsena_VALUE==3?"CLOSE_WAIT":Būsena_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.numeris(Lenta.tinklas_būsena(15,INDEX));단말.문자(10);
        }
        단말.Rašymas("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean laukimo_būsena(int 밀리초) {
        int Paleisti=Lenta.밀리초();
        while(Lenta.밀리초()-Paleisti<밀리초) {
            if(셸입출력.대화가능()!=0){int simbolis_VALUE_068c2631=Lenta.직렬읽기();if(simbolis_VALUE_068c2631==3 || simbolis_VALUE_068c2631=='q' || simbolis_VALUE_068c2631=='Q' || simbolis_VALUE_068c2631==27 || simbolis_VALUE_068c2631==-4096)return false;}
            Lenta.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, tikslas=-1;
        for(int vietos_rodyklė=1;vietos_rodyklė<prekė_COUNT();vietos_rodyklė++) {
            if(같음(vietos_rodyklė,"-c")){횟수=skaitmuo_VALUE(++vietos_rodyklė,100);if(횟수<1){triktis_VALUE("ping: -c 1..100");return;}}
            else if(같음(vietos_rodyklė,"-W")){제한=skaitmuo_VALUE(++vietos_rodyklė,10);if(제한<1){triktis_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(tikslas<0)tikslas=vietos_rodyklė;else{triktis_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(tikslas<0 || !주소읽기(tikslas)){triktis_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Rašymas("PING ");rašymas_ADDRESS(ADDRESS);단말.Rašymas(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tvarka_VALUE=1;tvarka_VALUE<=횟수 && 계속;tvarka_VALUE++) {
            int 처리값=Lenta.siųsti_atsakas(ADDRESS,tvarka_VALUE);
            if(처리값<0){KLAIDA(처리값);break;}보낸수++;
            int Paleisti=Lenta.밀리초();
            while(Lenta.응답읽기(0)==-11 && Lenta.밀리초()-Paleisti<제한)if(!laukimo_būsena(1)){계속=false;break;}
            if(!계속)break;
            if(Lenta.응답읽기(0)==0){
                int TIME_VALUE=Lenta.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Rašymas("32 bytes from ");rašymas_ADDRESS(ADDRESS);단말.Rašymas(" seq=");단말.numeris(tvarka_VALUE);단말.Rašymas(" ttl=");단말.numeris(Lenta.응답읽기(2));단말.Rašymas(" time=");단말.numeris(TIME_VALUE);단말.Rašymas(" ms\n");
            }else{단말.Rašymas("Request timeout seq=");단말.numeris(tvarka_VALUE);단말.문자(10);}
            if(tvarka_VALUE<횟수)계속=laukimo_būsena(200);
        }
        단말.numeris(보낸수);단말.Rašymas(" transmitted, ");단말.numeris(RECEIVED_COUNT);단말.Rašymas(" received, ");단말.numeris(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Rašymas("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Rašymas("rtt min/avg/max = ");단말.numeris(최솟값);단말.문자('/');단말.numeris(누적/RECEIVED_COUNT);단말.문자('/');단말.numeris(최댓값);단말.Rašymas(" ms\n");}
        명령해석기.REZULTATAS=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void laida_Veikla() { 단말.Rašymas("up ");단말.numeris(Lenta.밀리초()/1000);단말.Rašymas(" seconds\n"); }
    static void laida_atmintis() {
        numeris_įrašas("ARM RAM KiB (firmware): ",Lenta.užklausa_sistema(0,0));
        numeris_įrašas("Kernel image+BSS+stack KiB: ",Lenta.užklausa_sistema(1,0));
        int bendras_pajėgumas=Lenta.užklausa_sistema(2,0), 사용량=Lenta.užklausa_sistema(3,0);
        단말.Rašymas("AOT heap KiB total/used/free: ");단말.numeris(bendras_pajėgumas);단말.문자('/');단말.numeris(사용량);단말.문자('/');단말.numeris(bendras_pajėgumas-사용량);단말.문자(10);
        numeris_įrašas("Framebuffer KiB: ",Lenta.užklausa_sistema(4,0));
        numeris_įrašas("EL0 arena+session reserve KiB: ",Lenta.užklausa_sistema(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Lenta.užklausa_sistema(22,INDEX);
        numeris_įrašas("EL0 mapped KiB: ",매핑);
        단말.Rašymas("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void laida_Tasks() {
        단말.Rašymas("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Rašymas("1 - RUN - - ");단말.numeris(Lenta.밀리초());단말.Rašymas(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Lenta.užduotis_Būsena(INDEX)>0){단말.numeris(INDEX+1);단말.Rašymas(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Būsena_VALUE=Lenta.užklausa_sistema(20,INDEX);if(Būsena_VALUE==0)continue;
            단말.numeris(Lenta.užklausa_sistema(21,INDEX));단말.문자(' ');단말.numeris(INDEX);단말.Rašymas(Būsena_VALUE==1?" RUN ":" SUSPENDED ");
            단말.numeris(Lenta.užklausa_sistema(22,INDEX));단말.문자(' ');단말.numeris(Lenta.užklausa_sistema(24,INDEX));단말.문자(' ');단말.numeris(Lenta.užklausa_sistema(23,INDEX));단말.문자(' ');
            for(int vietos_rodyklė=0;vietos_rodyklė<288;vietos_rodyklė++){int baitas_VALUE=Lenta.užklausa_sistema(25,INDEX+vietos_rodyklė*4);if(baitas_VALUE==0)break;Lenta.직렬쓰기(baitas_VALUE);}단말.문자(10);
        }
    }
    static void laida_Saugykla() {
        int 칸수=0, duomenys_COUNT=0;
        for(int INDEX=0;INDEX<atmintis_Failai.Failas_COUNT;INDEX++)if(atmintis_Failai.이름길이[INDEX]>0 || atmintis_Failai.nuoroda_COUNT[INDEX]>0){칸수++;duomenys_COUNT+=atmintis_Failai.길이[INDEX];}
        단말.Rašymas("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.numeris(atmintis_Failai.Failas_COUNT*16384);단말.문자(' ');단말.numeris(칸수*16384);단말.문자(' ');단말.numeris((atmintis_Failai.Failas_COUNT-칸수)*16384);단말.문자(' ');단말.numeris(duomenys_COUNT);단말.문자(' ');단말.numeris(칸수);단말.문자('/');단말.numeris(atmintis_Failai.Failas_COUNT);단말.Rašymas(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void laida_būsena() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(prekė_COUNT()>1){if(prekė_COUNT()!=3 || !같음(1,"-n") || (횟수=skaitmuo_VALUE(2,1000))<1){triktis_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 išeiti_programa");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Rašymas("\u001b[2J\u001b[H");
            laida_Veikla();laida_atmintis();laida_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!laukimo_būsena(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void laida_žinynas() {
        단말.Rašymas("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Rašymas(표준말(INDEX));단말.Rašymas(" / ");단말.Rašymas(관리명령.Word_SMS(INDEX));단말.Rašymas(" : ");단말.Rašymas(관리명령.aprašas(INDEX));단말.문자(10);}
        단말.Rašymas("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Rašymas("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Rašymas("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Vykdyti_komanda() {
        int Komanda=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Komanda=INDEX;
        if(같음(0,"ifconfig"))Komanda=0;if(같음(0,"ss"))Komanda=4;
        if(Komanda<0)return false;
        if(Komanda==11){if(같음(1,"net") || 같음(1,"system"))laida_žinynas();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.laida_žinynas();return true;}
        if(Komanda==0 || Komanda==1)tinklas_komanda(Komanda==1);
        else if(Komanda==2)응답시험();
        else if(Komanda==6)laida_būsena();
        else if(prekė_COUNT()!=1){triktis_VALUE("This command takes no arguments; help system");}
        else if(Komanda==3)laida_kelias();else if(Komanda==4)laida_tinklas();else if(Komanda==5)laida_Tasks();else if(Komanda==7)laida_atmintis();else if(Komanda==8)laida_Saugykla();else if(Komanda==9)laida_Veikla();
        else if(Komanda==10)Lenta.전원끄기();
        return true;
    }
}
