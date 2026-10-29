// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** attwali_data kernel_VALUE 상태를 읽는 IPv4·ICMP·작업·Memorja_VALUE·RAM 저장소 관리 kmand. */
public final class sistema_għodda {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int element_COUNT() { return 명령해석기.token_COUNT; }
    static void żball_VALUE(String AQRANI_eb81d7d9) { 명령해석기.miżura=2; 단말.kiteb(AQRANI_eb81d7d9); 단말.문자(10); }
    static void żball(int VALUE) { 명령해석기.żball(VALUE); }
    static void 수항목(String isem, int VALUE) { 단말.kiteb(isem); 단말.수(VALUE); 단말.문자(10); }
    static int ċifra_VALUE(int INDEX, int 한도) {
        if (INDEX>=element_COUNT() || 명령해석기.tul_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.tul_VALUE[INDEX]; 순번++) {
            int karattru_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (karattru_VALUE<0 || karattru_VALUE>9 || VALUE>(한도-karattru_VALUE)/10) return -1;
            VALUE=VALUE*10+karattru_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=element_COUNT()) return false;
        int VALUE=0, 덩이=0, ċifra_COUNT=0, punt_COUNT=0;
        for (int 순번=0; 순번<명령해석기.tul_VALUE[INDEX]; 순번++) {
            int karattru_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (karattru_VALUE=='.') { if (ċifra_COUNT==0 || ++punt_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=ċifra_COUNT=0; }
            else { if (karattru_VALUE<'0' || karattru_VALUE>'9' || ++ċifra_COUNT>3) return false; 덩이=덩이*10+karattru_VALUE-'0'; if(덩이>255)return false; }
        }
        if (punt_COUNT!=3 || ċifra_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void kiteb_ADDRESS(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void wera_netwerk_stat() {
        단말.kiteb(bord.netwerk_stat(20,0)!=0?"en0: ":"sl0: "); 단말.kiteb(bord.netwerk_stat(3,0)!=0?"UP":"DOWN");
        단말.kiteb(bord.netwerk_stat(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.kiteb(bord.netwerk_stat(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kiteb_ADDRESS(bord.netwerk_stat(0,0));
        단말.kiteb(" netmask "); kiteb_ADDRESS(bord.netwerk_stat(1,0)); 단말.kiteb(" gateway "); kiteb_ADDRESS(bord.netwerk_stat(2,0)); 단말.문자(10);
        단말.kiteb("  RX packets "); 단말.수(bord.netwerk_stat(4,0)); 단말.kiteb(" bytes "); 단말.수(bord.netwerk_stat(6,0));
        단말.kiteb(" TX packets "); 단말.수(bord.netwerk_stat(5,0)); 단말.kiteb(" bytes "); 단말.수(bord.netwerk_stat(7,0)); 단말.문자(10);
        수항목("  dropped ",bord.netwerk_stat(8,0));
    }
    static void sett_ADDRESS(int serje) {
        if (element_COUNT()!=serje+3 || !주소읽기(serje)) { żball_VALUE("사용법: ipconfig set ADDRESS 주소가림 gateway_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(serje+1)){żball_VALUE("Invalid IPv4 netmask");return;} int maskra_VALUE=ADDRESS_VALUE;
        if(!주소읽기(serje+2)){żball_VALUE("Invalid IPv4 gateway");return;}
        int miżura=bord.netwerk_Settings(0,ADDRESS,maskra_VALUE,ADDRESS_VALUE);
        if(miżura<0) { żball(miżura); if(miżura==-16)단말.kiteb("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.kiteb("IPv4 configuration applied (until reboot)\n"); wera_netwerk_stat(); }
    }
    static void netwerk_kmand(boolean indirizz_IP) {
        if (element_COUNT()==1 || element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { wera_netwerk_stat();return; }
        if (indirizz_IP && 같음(1,"route") && (element_COUNT()==2 || element_COUNT()==3&&같음(2,"show"))) { wera_mogħdija();return; }
        if (같음(1,"set")) { sett_ADDRESS(2);return; }
        if (element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { bord.netwerk_Settings(같음(1,"up")?1:2,0,0,0);wera_netwerk_stat();return; }
        if (indirizz_IP && element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { bord.netwerk_Settings(같음(5,"up")?1:2,0,0,0);wera_netwerk_stat();return; }
        żball_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 gateway_VALUE|link set dev sl0 up|down]");
    }
    static void wera_mogħdija() {
        단말.kiteb("Destination Netmask Gateway Interface\n");
        kiteb_ADDRESS(bord.netwerk_stat(0,0)&bord.netwerk_stat(1,0));단말.문자(' ');kiteb_ADDRESS(bord.netwerk_stat(1,0));단말.kiteb(bord.netwerk_stat(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (bord.netwerk_stat(2,0)!=0) {단말.kiteb("0.0.0.0 0.0.0.0 ");kiteb_ADDRESS(bord.netwerk_stat(2,0));단말.kiteb(bord.netwerk_stat(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void wera_netwerk() {
        단말.kiteb("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kategorija=bord.netwerk_stat(10,INDEX);if(TYPE_kategorija==0)continue;
            단말.kiteb(TYPE_kategorija==1?"TCP ":"UDP ");kiteb_ADDRESS(bord.netwerk_stat(16,INDEX));단말.문자(':');단말.수(bord.netwerk_stat(11,INDEX));단말.문자(' ');
            kiteb_ADDRESS(bord.netwerk_stat(12,INDEX));단말.문자(':');단말.수(bord.netwerk_stat(13,INDEX));단말.문자(' ');
            int stat_VALUE=bord.netwerk_stat(14,INDEX);단말.kiteb(TYPE_kategorija==2?"DATAGRAM":stat_VALUE==1?"LISTEN":stat_VALUE==2?"ESTABLISHED":stat_VALUE==3?"CLOSE_WAIT":stat_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(bord.netwerk_stat(15,INDEX));단말.문자(10);
        }
        단말.kiteb("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int serje=bord.밀리초();
        while(bord.밀리초()-serje<밀리초) {
            if(셸입출력.대화가능()!=0){int karattru_VALUE=bord.직렬읽기();if(karattru_VALUE==3 || karattru_VALUE=='q' || karattru_VALUE=='Q' || karattru_VALUE==27 || karattru_VALUE==-4096)return false;}
            bord.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, mira=-1;
        for(int pożizzjoni_INDEX=1;pożizzjoni_INDEX<element_COUNT();pożizzjoni_INDEX++) {
            if(같음(pożizzjoni_INDEX,"-c")){횟수=ċifra_VALUE(++pożizzjoni_INDEX,100);if(횟수<1){żball_VALUE("ping: -c 1..100");return;}}
            else if(같음(pożizzjoni_INDEX,"-W")){제한=ċifra_VALUE(++pożizzjoni_INDEX,10);if(제한<1){żball_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(mira<0)mira=pożizzjoni_INDEX;else{żball_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(mira<0 || !주소읽기(mira)){żball_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.kiteb("PING ");kiteb_ADDRESS(ADDRESS);단말.kiteb(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ordni_VALUE=1;ordni_VALUE<=횟수 && 계속;ordni_VALUE++) {
            int 처리값=bord.응답보내기(ADDRESS,ordni_VALUE);
            if(처리값<0){żball(처리값);break;}보낸수++;
            int serje=bord.밀리초();
            while(bord.응답읽기(0)==-11 && bord.밀리초()-serje<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(bord.응답읽기(0)==0){
                int TIME_VALUE=bord.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.kiteb("32 bytes from ");kiteb_ADDRESS(ADDRESS);단말.kiteb(" seq=");단말.수(ordni_VALUE);단말.kiteb(" ttl=");단말.수(bord.응답읽기(2));단말.kiteb(" time=");단말.수(TIME_VALUE);단말.kiteb(" ms\n");
            }else{단말.kiteb("Request timeout seq=");단말.수(ordni_VALUE);단말.문자(10);}
            if(ordni_VALUE<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.kiteb(" transmitted, ");단말.수(RECEIVED_COUNT);단말.kiteb(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.kiteb("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.kiteb("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.kiteb(" ms\n");}
        명령해석기.miżura=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void wera_Attività() { 단말.kiteb("up ");단말.수(bord.밀리초()/1000);단말.kiteb(" seconds\n"); }
    static void wera_Memorja() {
        수항목("ARM RAM KiB (firmware): ",bord.query_sistema(0,0));
        수항목("Kernel image+BSS+stack KiB: ",bord.query_sistema(1,0));
        int 총량=bord.query_sistema(2,0), 사용량=bord.query_sistema(3,0);
        단말.kiteb("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",bord.query_sistema(4,0));
        수항목("EL0 arena+session reserve KiB: ",bord.query_sistema(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=bord.query_sistema(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.kiteb("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void wera_Tasks() {
        단말.kiteb("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.kiteb("1 - RUN - - ");단말.수(bord.밀리초());단말.kiteb(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(bord.attività_stat(INDEX)>0){단말.수(INDEX+1);단말.kiteb(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int stat_VALUE=bord.query_sistema(20,INDEX);if(stat_VALUE==0)continue;
            단말.수(bord.query_sistema(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.kiteb(stat_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(bord.query_sistema(22,INDEX));단말.문자(' ');단말.수(bord.query_sistema(24,INDEX));단말.문자(' ');단말.수(bord.query_sistema(23,INDEX));단말.문자(' ');
            for(int pożizzjoni_INDEX=0;pożizzjoni_INDEX<288;pożizzjoni_INDEX++){int byte_VALUE=bord.query_sistema(25,INDEX+pożizzjoni_INDEX*4);if(byte_VALUE==0)break;bord.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void wera_Ħażna() {
        int slott_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Memorja_Fajls.fajl_COUNT;INDEX++)if(Memorja_Fajls.이름길이[INDEX]>0 || Memorja_Fajls.Referenza_COUNT[INDEX]>0){slott_COUNT++;data_COUNT+=Memorja_Fajls.tul_VALUE[INDEX];}
        단말.kiteb("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memorja_Fajls.fajl_COUNT*16384);단말.문자(' ');단말.수(slott_COUNT*16384);단말.문자(' ');단말.수((Memorja_Fajls.fajl_COUNT-slott_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(slott_COUNT);단말.문자('/');단말.수(Memorja_Fajls.fajl_COUNT);단말.kiteb(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void wera_stat_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(element_COUNT()>1){if(element_COUNT()!=3 || !같음(1,"-n") || (횟수=ċifra_VALUE(2,1000))<1){żball_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 ħruġ_programm");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.kiteb("\u001b[2J\u001b[H");
            wera_Attività();wera_Memorja();wera_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void wera_għajnuna() {
        단말.kiteb("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.kiteb(표준말(INDEX));단말.kiteb(" / ");단말.kiteb(관리명령.Word_SMS(INDEX));단말.kiteb(" : ");단말.kiteb(관리명령.설명(INDEX));단말.문자(10);}
        단말.kiteb("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.kiteb("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.kiteb("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean eżegwixxa_kmand() {
        int kmand=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))kmand=INDEX;
        if(같음(0,"ifconfig"))kmand=0;if(같음(0,"ss"))kmand=4;
        if(kmand<0)return false;
        if(kmand==11){if(같음(1,"net") || 같음(1,"system"))wera_għajnuna();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.wera_għajnuna();return true;}
        if(kmand==0 || kmand==1)netwerk_kmand(kmand==1);
        else if(kmand==2)응답시험();
        else if(kmand==6)wera_stat_bf9821b5();
        else if(element_COUNT()!=1){żball_VALUE("This command takes no arguments; help system");}
        else if(kmand==3)wera_mogħdija();else if(kmand==4)wera_netwerk();else if(kmand==5)wera_Tasks();else if(kmand==7)wera_Memorja();else if(kmand==8)wera_Ħażna();else if(kmand==9)wera_Attività();
        else if(kmand==10)bord.전원끄기();
        return true;
    }
}
