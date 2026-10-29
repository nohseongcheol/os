// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** dearbh_dàta eitean_VALUE 상태를 읽는 IPv4·ICMP·작업·cuimhne_VALUE·RAM 저장소 관리 àithne. */
public final class siostam_inneal {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int nì_COUNT() { return 명령해석기.tòcan_COUNT; }
    static void fàilligeadh_VALUE(String LEUGHMI_eb81d7d9) { 명령해석기.tomhas=2; 단말.sgrìobh(LEUGHMI_eb81d7d9); 단말.문자(10); }
    static void Mearachd(int VALUE) { 명령해석기.Mearachd(VALUE); }
    static void 수항목(String Ainm, int VALUE) { 단말.sgrìobh(Ainm); 단말.수(VALUE); 단말.문자(10); }
    static int figear_VALUE(int INDEX, int 한도) {
        if (INDEX>=nì_COUNT() || 명령해석기.faid_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.faid_VALUE[INDEX]; 순번++) {
            int caractar_VALUE=명령해석기.tòcan_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (caractar_VALUE<0 || caractar_VALUE>9 || VALUE>(한도-caractar_VALUE)/10) return -1;
            VALUE=VALUE*10+caractar_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=nì_COUNT()) return false;
        int VALUE=0, 덩이=0, figear_COUNT=0, puing_COUNT=0;
        for (int 순번=0; 순번<명령해석기.faid_VALUE[INDEX]; 순번++) {
            int caractar_VALUE=명령해석기.tòcan_VALUE[명령해석기.시작점[INDEX]+순번];
            if (caractar_VALUE=='.') { if (figear_COUNT==0 || ++puing_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=figear_COUNT=0; }
            else { if (caractar_VALUE<'0' || caractar_VALUE>'9' || ++figear_COUNT>3) return false; 덩이=덩이*10+caractar_VALUE-'0'; if(덩이>255)return false; }
        }
        if (puing_COUNT!=3 || figear_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void sgrìobh_ADDRESS(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void show_lìonra_cor() {
        단말.sgrìobh(bòrd.lìonra_cor(20,0)!=0?"en0: ":"sl0: "); 단말.sgrìobh(bòrd.lìonra_cor(3,0)!=0?"UP":"DOWN");
        단말.sgrìobh(bòrd.lìonra_cor(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.sgrìobh(bòrd.lìonra_cor(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); sgrìobh_ADDRESS(bòrd.lìonra_cor(0,0));
        단말.sgrìobh(" netmask "); sgrìobh_ADDRESS(bòrd.lìonra_cor(1,0)); 단말.sgrìobh(" gateway "); sgrìobh_ADDRESS(bòrd.lìonra_cor(2,0)); 단말.문자(10);
        단말.sgrìobh("  RX packets "); 단말.수(bòrd.lìonra_cor(4,0)); 단말.sgrìobh(" bytes "); 단말.수(bòrd.lìonra_cor(6,0));
        단말.sgrìobh(" TX packets "); 단말.수(bòrd.lìonra_cor(5,0)); 단말.sgrìobh(" bytes "); 단말.수(bòrd.lìonra_cor(7,0)); 단말.문자(10);
        수항목("  dropped ",bòrd.lìonra_cor(8,0));
    }
    static void seata_ADDRESS(int ruith) {
        if (nì_COUNT()!=ruith+3 || !주소읽기(ruith)) { fàilligeadh_VALUE("사용법: ipconfig set ADDRESS 주소가림 관문"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(ruith+1)){fàilligeadh_VALUE("Invalid IPv4 netmask");return;} int 가림=ADDRESS_VALUE;
        if(!주소읽기(ruith+2)){fàilligeadh_VALUE("Invalid IPv4 gateway");return;}
        int tomhas=bòrd.lìonra_roghainnean(0,ADDRESS,가림,ADDRESS_VALUE);
        if(tomhas<0) { Mearachd(tomhas); if(tomhas==-16)단말.sgrìobh("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.sgrìobh("IPv4 configuration applied (until reboot)\n"); show_lìonra_cor(); }
    }
    static void lìonra_àithne(boolean seòladh_IP) {
        if (nì_COUNT()==1 || nì_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || nì_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { show_lìonra_cor();return; }
        if (seòladh_IP && 같음(1,"route") && (nì_COUNT()==2 || nì_COUNT()==3&&같음(2,"show"))) { show_slighe();return; }
        if (같음(1,"set")) { seata_ADDRESS(2);return; }
        if (nì_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { bòrd.lìonra_roghainnean(같음(1,"up")?1:2,0,0,0);show_lìonra_cor();return; }
        if (seòladh_IP && nì_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { bòrd.lìonra_roghainnean(같음(5,"up")?1:2,0,0,0);show_lìonra_cor();return; }
        fàilligeadh_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 관문|link set dev sl0 up|down]");
    }
    static void show_slighe() {
        단말.sgrìobh("Destination Netmask Gateway Interface\n");
        sgrìobh_ADDRESS(bòrd.lìonra_cor(0,0)&bòrd.lìonra_cor(1,0));단말.문자(' ');sgrìobh_ADDRESS(bòrd.lìonra_cor(1,0));단말.sgrìobh(bòrd.lìonra_cor(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (bòrd.lìonra_cor(2,0)!=0) {단말.sgrìobh("0.0.0.0 0.0.0.0 ");sgrìobh_ADDRESS(bòrd.lìonra_cor(2,0));단말.sgrìobh(bòrd.lìonra_cor(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void show_lìonra() {
        단말.sgrìobh("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_roinn_seòrsa=bòrd.lìonra_cor(10,INDEX);if(TYPE_roinn_seòrsa==0)continue;
            단말.sgrìobh(TYPE_roinn_seòrsa==1?"TCP ":"UDP ");sgrìobh_ADDRESS(bòrd.lìonra_cor(16,INDEX));단말.문자(':');단말.수(bòrd.lìonra_cor(11,INDEX));단말.문자(' ');
            sgrìobh_ADDRESS(bòrd.lìonra_cor(12,INDEX));단말.문자(':');단말.수(bòrd.lìonra_cor(13,INDEX));단말.문자(' ');
            int cor_VALUE=bòrd.lìonra_cor(14,INDEX);단말.sgrìobh(TYPE_roinn_seòrsa==2?"DATAGRAM":cor_VALUE==1?"LISTEN":cor_VALUE==2?"ESTABLISHED":cor_VALUE==3?"CLOSE_WAIT":cor_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(bòrd.lìonra_cor(15,INDEX));단말.문자(10);
        }
        단말.sgrìobh("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean fuirich_cor(int 밀리초) {
        int ruith=bòrd.밀리초();
        while(bòrd.밀리초()-ruith<밀리초) {
            if(셸입출력.대화가능()!=0){int caractar_VALUE=bòrd.직렬읽기();if(caractar_VALUE==3 || caractar_VALUE=='q' || caractar_VALUE=='Q' || caractar_VALUE==27 || caractar_VALUE==-4096)return false;}
            bòrd.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, targaid=-1;
        for(int suidhich_INDEX=1;suidhich_INDEX<nì_COUNT();suidhich_INDEX++) {
            if(같음(suidhich_INDEX,"-c")){횟수=figear_VALUE(++suidhich_INDEX,100);if(횟수<1){fàilligeadh_VALUE("ping: -c 1..100");return;}}
            else if(같음(suidhich_INDEX,"-W")){제한=figear_VALUE(++suidhich_INDEX,10);if(제한<1){fàilligeadh_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(targaid<0)targaid=suidhich_INDEX;else{fàilligeadh_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(targaid<0 || !주소읽기(targaid)){fàilligeadh_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.sgrìobh("PING ");sgrìobh_ADDRESS(ADDRESS);단말.sgrìobh(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int òrdugh_VALUE=1;òrdugh_VALUE<=횟수 && 계속;òrdugh_VALUE++) {
            int 처리값=bòrd.응답보내기(ADDRESS,òrdugh_VALUE);
            if(처리값<0){Mearachd(처리값);break;}보낸수++;
            int ruith=bòrd.밀리초();
            while(bòrd.응답읽기(0)==-11 && bòrd.밀리초()-ruith<제한)if(!fuirich_cor(1)){계속=false;break;}
            if(!계속)break;
            if(bòrd.응답읽기(0)==0){
                int TIME_VALUE=bòrd.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.sgrìobh("32 bytes from ");sgrìobh_ADDRESS(ADDRESS);단말.sgrìobh(" seq=");단말.수(òrdugh_VALUE);단말.sgrìobh(" ttl=");단말.수(bòrd.응답읽기(2));단말.sgrìobh(" time=");단말.수(TIME_VALUE);단말.sgrìobh(" ms\n");
            }else{단말.sgrìobh("Request timeout seq=");단말.수(òrdugh_VALUE);단말.문자(10);}
            if(òrdugh_VALUE<횟수)계속=fuirich_cor(200);
        }
        단말.수(보낸수);단말.sgrìobh(" transmitted, ");단말.수(RECEIVED_COUNT);단말.sgrìobh(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.sgrìobh("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.sgrìobh("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.sgrìobh(" ms\n");}
        명령해석기.tomhas=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void show_gnìomhachd() { 단말.sgrìobh("up ");단말.수(bòrd.밀리초()/1000);단말.sgrìobh(" seconds\n"); }
    static void show_cuimhne() {
        수항목("ARM RAM KiB (firmware): ",bòrd.ceist_siostam(0,0));
        수항목("Kernel image+BSS+stack KiB: ",bòrd.ceist_siostam(1,0));
        int 총량=bòrd.ceist_siostam(2,0), 사용량=bòrd.ceist_siostam(3,0);
        단말.sgrìobh("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",bòrd.ceist_siostam(4,0));
        수항목("EL0 arena+session reserve KiB: ",bòrd.ceist_siostam(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=bòrd.ceist_siostam(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.sgrìobh("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void show_Tasks() {
        단말.sgrìobh("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.sgrìobh("1 - RUN - - ");단말.수(bòrd.밀리초());단말.sgrìobh(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(bòrd.saothair_cor(INDEX)>0){단말.수(INDEX+1);단말.sgrìobh(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int cor_VALUE=bòrd.ceist_siostam(20,INDEX);if(cor_VALUE==0)continue;
            단말.수(bòrd.ceist_siostam(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.sgrìobh(cor_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(bòrd.ceist_siostam(22,INDEX));단말.문자(' ');단말.수(bòrd.ceist_siostam(24,INDEX));단말.문자(' ');단말.수(bòrd.ceist_siostam(23,INDEX));단말.문자(' ');
            for(int suidhich_INDEX=0;suidhich_INDEX<288;suidhich_INDEX++){int baidht_VALUE=bòrd.ceist_siostam(25,INDEX+suidhich_INDEX*4);if(baidht_VALUE==0)break;bòrd.직렬쓰기(baidht_VALUE);}단말.문자(10);
        }
    }
    static void show_stòras() {
        int slot_COUNT=0, dàta_COUNT=0;
        for(int INDEX=0;INDEX<cuimhne_faidhlichean.faidhle_COUNT;INDEX++)if(cuimhne_faidhlichean.이름길이[INDEX]>0 || cuimhne_faidhlichean.fiosrachadh_COUNT[INDEX]>0){slot_COUNT++;dàta_COUNT+=cuimhne_faidhlichean.faid_VALUE[INDEX];}
        단말.sgrìobh("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(cuimhne_faidhlichean.faidhle_COUNT*16384);단말.문자(' ');단말.수(slot_COUNT*16384);단말.문자(' ');단말.수((cuimhne_faidhlichean.faidhle_COUNT-slot_COUNT)*16384);단말.문자(' ');단말.수(dàta_COUNT);단말.문자(' ');단말.수(slot_COUNT);단말.문자('/');단말.수(cuimhne_faidhlichean.faidhle_COUNT);단말.sgrìobh(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void show_cor_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(nì_COUNT()>1){if(nì_COUNT()!=3 || !같음(1,"-n") || (횟수=figear_VALUE(2,1000))<1){fàilligeadh_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 fàg_an_seo_ap");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.sgrìobh("\u001b[2J\u001b[H");
            show_gnìomhachd();show_cuimhne();show_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!fuirich_cor(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void show_cuideachadh() {
        단말.sgrìobh("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.sgrìobh(표준말(INDEX));단말.sgrìobh(" / ");단말.sgrìobh(관리명령.Word_SMS(INDEX));단말.sgrìobh(" : ");단말.sgrìobh(관리명령.설명(INDEX));단말.문자(10);}
        단말.sgrìobh("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.sgrìobh("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.sgrìobh("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean gnìomhaich_àithne() {
        int àithne=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))àithne=INDEX;
        if(같음(0,"ifconfig"))àithne=0;if(같음(0,"ss"))àithne=4;
        if(àithne<0)return false;
        if(àithne==11){if(같음(1,"net") || 같음(1,"system"))show_cuideachadh();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.show_cuideachadh();return true;}
        if(àithne==0 || àithne==1)lìonra_àithne(àithne==1);
        else if(àithne==2)응답시험();
        else if(àithne==6)show_cor_bf9821b5();
        else if(nì_COUNT()!=1){fàilligeadh_VALUE("This command takes no arguments; help system");}
        else if(àithne==3)show_slighe();else if(àithne==4)show_lìonra();else if(àithne==5)show_Tasks();else if(àithne==7)show_cuimhne();else if(àithne==8)show_stòras();else if(àithne==9)show_gnìomhachd();
        else if(àithne==10)bòrd.전원끄기();
        return true;
    }
}
