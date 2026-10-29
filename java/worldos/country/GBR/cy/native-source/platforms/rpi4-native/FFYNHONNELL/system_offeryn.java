// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** go_iawn_data cnewyllyn_VALUE 상태를 읽는 IPv4·ICMP·작업·Cof_VALUE·RAM 저장소 관리 Gorchymyn. */
public final class system_offeryn {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int eitem_COUNT() { return 명령해석기.tocyn_COUNT_3176ee99; }
    static void methiant_VALUE(String GWYBODAETH_eb81d7d9) { 명령해석기.mesur=2; 단말.Ysgrifennu(GWYBODAETH_eb81d7d9); 단말.문자(10); }
    static void Gwall(int VALUE) { 명령해석기.Gwall(VALUE); }
    static void 수항목(String Enw, int VALUE) { 단말.Ysgrifennu(Enw); 단말.수(VALUE); 단말.문자(10); }
    static int digid_VALUE(int INDEX, int 한도) {
        if (INDEX>=eitem_COUNT() || 명령해석기.hyd_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.hyd_VALUE[INDEX]; 순번++) {
            int nod_VALUE=명령해석기.tocyn_VALUE_eb540501[명령해석기.시작점[INDEX]+순번]-'0';
            if (nod_VALUE<0 || nod_VALUE>9 || VALUE>(한도-nod_VALUE)/10) return -1;
            VALUE=VALUE*10+nod_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=eitem_COUNT()) return false;
        int VALUE=0, 덩이=0, digid_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.hyd_VALUE[INDEX]; 순번++) {
            int nod_VALUE=명령해석기.tocyn_VALUE_eb540501[명령해석기.시작점[INDEX]+순번];
            if (nod_VALUE=='.') { if (digid_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=digid_COUNT=0; }
            else { if (nod_VALUE<'0' || nod_VALUE>'9' || ++digid_COUNT>3) return false; 덩이=덩이*10+nod_VALUE-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || digid_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void ysgrifennu_ADDRESS(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void sioe_Rhwydwaith_cyflwr() {
        단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(20,0)!=0?"en0: ":"sl0: "); 단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(3,0)!=0?"UP":"DOWN");
        단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(0,0));
        단말.Ysgrifennu(" netmask "); ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(1,0)); 단말.Ysgrifennu(" gateway "); ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(2,0)); 단말.문자(10);
        단말.Ysgrifennu("  RX packets "); 단말.수(bwrdd.Rhwydwaith_cyflwr(4,0)); 단말.Ysgrifennu(" bytes "); 단말.수(bwrdd.Rhwydwaith_cyflwr(6,0));
        단말.Ysgrifennu(" TX packets "); 단말.수(bwrdd.Rhwydwaith_cyflwr(5,0)); 단말.Ysgrifennu(" bytes "); 단말.수(bwrdd.Rhwydwaith_cyflwr(7,0)); 단말.문자(10);
        수항목("  dropped ",bwrdd.Rhwydwaith_cyflwr(8,0));
    }
    static void set_ADDRESS(int Gweithredu_2) {
        if (eitem_COUNT()!=Gweithredu_2+3 || !주소읽기(Gweithredu_2)) { methiant_VALUE("사용법: ipconfig set ADDRESS 주소가림 adwy_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(Gweithredu_2+1)){methiant_VALUE("Invalid IPv4 netmask");return;} int masgio_VALUE=ADDRESS_VALUE;
        if(!주소읽기(Gweithredu_2+2)){methiant_VALUE("Invalid IPv4 gateway");return;}
        int mesur=bwrdd.Rhwydwaith_Gosodiadau(0,ADDRESS,masgio_VALUE,ADDRESS_VALUE);
        if(mesur<0) { Gwall(mesur); if(mesur==-16)단말.Ysgrifennu("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Ysgrifennu("IPv4 configuration applied (until reboot)\n"); sioe_Rhwydwaith_cyflwr(); }
    }
    static void Rhwydwaith_gorchymyn(boolean cyfeiriad_IP) {
        if (eitem_COUNT()==1 || eitem_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || eitem_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { sioe_Rhwydwaith_cyflwr();return; }
        if (cyfeiriad_IP && 같음(1,"route") && (eitem_COUNT()==2 || eitem_COUNT()==3&&같음(2,"show"))) { sioe_llwybr();return; }
        if (같음(1,"set")) { set_ADDRESS(2);return; }
        if (eitem_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { bwrdd.Rhwydwaith_Gosodiadau(같음(1,"up")?1:2,0,0,0);sioe_Rhwydwaith_cyflwr();return; }
        if (cyfeiriad_IP && eitem_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { bwrdd.Rhwydwaith_Gosodiadau(같음(5,"up")?1:2,0,0,0);sioe_Rhwydwaith_cyflwr();return; }
        methiant_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 adwy_VALUE|link set dev sl0 up|down]");
    }
    static void sioe_llwybr() {
        단말.Ysgrifennu("Destination Netmask Gateway Interface\n");
        ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(0,0)&bwrdd.Rhwydwaith_cyflwr(1,0));단말.문자(' ');ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(1,0));단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (bwrdd.Rhwydwaith_cyflwr(2,0)!=0) {단말.Ysgrifennu("0.0.0.0 0.0.0.0 ");ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(2,0));단말.Ysgrifennu(bwrdd.Rhwydwaith_cyflwr(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void sioe_Rhwydwaith() {
        단말.Ysgrifennu("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_ardal=bwrdd.Rhwydwaith_cyflwr(10,INDEX);if(TYPE_ardal==0)continue;
            단말.Ysgrifennu(TYPE_ardal==1?"TCP ":"UDP ");ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(16,INDEX));단말.문자(':');단말.수(bwrdd.Rhwydwaith_cyflwr(11,INDEX));단말.문자(' ');
            ysgrifennu_ADDRESS(bwrdd.Rhwydwaith_cyflwr(12,INDEX));단말.문자(':');단말.수(bwrdd.Rhwydwaith_cyflwr(13,INDEX));단말.문자(' ');
            int cyflwr_VALUE=bwrdd.Rhwydwaith_cyflwr(14,INDEX);단말.Ysgrifennu(TYPE_ardal==2?"DATAGRAM":cyflwr_VALUE==1?"LISTEN":cyflwr_VALUE==2?"ESTABLISHED":cyflwr_VALUE==3?"CLOSE_WAIT":cyflwr_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(bwrdd.Rhwydwaith_cyflwr(15,INDEX));단말.문자(10);
        }
        단말.Ysgrifennu("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean aros_cyflwr(int 밀리초) {
        int Gweithredu_2=bwrdd.밀리초();
        while(bwrdd.밀리초()-Gweithredu_2<밀리초) {
            if(셸입출력.technoleg_gwybodaeth_rhyngweithiol()!=0){int nod_VALUE=bwrdd.직렬읽기();if(nod_VALUE==3 || nod_VALUE=='q' || nod_VALUE=='Q' || nod_VALUE==27 || nod_VALUE==-4096)return false;}
            bwrdd.atal_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, targed=-1;
        for(int safle_INDEX=1;safle_INDEX<eitem_COUNT();safle_INDEX++) {
            if(같음(safle_INDEX,"-c")){횟수=digid_VALUE(++safle_INDEX,100);if(횟수<1){methiant_VALUE("ping: -c 1..100");return;}}
            else if(같음(safle_INDEX,"-W")){제한=digid_VALUE(++safle_INDEX,10);if(제한<1){methiant_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(targed<0)targed=safle_INDEX;else{methiant_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(targed<0 || !주소읽기(targed)){methiant_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Ysgrifennu("PING ");ysgrifennu_ADDRESS(ADDRESS);단말.Ysgrifennu(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int trefn_VALUE=1;trefn_VALUE<=횟수 && 계속;trefn_VALUE++) {
            int 처리값=bwrdd.응답보내기(ADDRESS,trefn_VALUE);
            if(처리값<0){Gwall(처리값);break;}보낸수++;
            int Gweithredu_2=bwrdd.밀리초();
            while(bwrdd.응답읽기(0)==-11 && bwrdd.밀리초()-Gweithredu_2<제한)if(!aros_cyflwr(1)){계속=false;break;}
            if(!계속)break;
            if(bwrdd.응답읽기(0)==0){
                int TIME_VALUE=bwrdd.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Ysgrifennu("32 bytes from ");ysgrifennu_ADDRESS(ADDRESS);단말.Ysgrifennu(" seq=");단말.수(trefn_VALUE);단말.Ysgrifennu(" ttl=");단말.수(bwrdd.응답읽기(2));단말.Ysgrifennu(" time=");단말.수(TIME_VALUE);단말.Ysgrifennu(" ms\n");
            }else{단말.Ysgrifennu("Request timeout seq=");단말.수(trefn_VALUE);단말.문자(10);}
            if(trefn_VALUE<횟수)계속=aros_cyflwr(200);
        }
        단말.수(보낸수);단말.Ysgrifennu(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Ysgrifennu(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Ysgrifennu("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Ysgrifennu("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Ysgrifennu(" ms\n");}
        명령해석기.mesur=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void sioe_Gweithgarwch() { 단말.Ysgrifennu("up ");단말.수(bwrdd.밀리초()/1000);단말.Ysgrifennu(" seconds\n"); }
    static void sioe_Cof() {
        수항목("ARM RAM KiB (firmware): ",bwrdd.ymholiad_system(0,0));
        수항목("Kernel image+BSS+stack KiB: ",bwrdd.ymholiad_system(1,0));
        int 총량=bwrdd.ymholiad_system(2,0), 사용량=bwrdd.ymholiad_system(3,0);
        단말.Ysgrifennu("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",bwrdd.ymholiad_system(4,0));
        수항목("EL0 arena+session reserve KiB: ",bwrdd.ymholiad_system(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=bwrdd.ymholiad_system(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Ysgrifennu("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void sioe_Tasks() {
        단말.Ysgrifennu("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Ysgrifennu("1 - RUN - - ");단말.수(bwrdd.밀리초());단말.Ysgrifennu(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(bwrdd.tasg_cyflwr(INDEX)>0){단말.수(INDEX+1);단말.Ysgrifennu(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int cyflwr_VALUE=bwrdd.ymholiad_system(20,INDEX);if(cyflwr_VALUE==0)continue;
            단말.수(bwrdd.ymholiad_system(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Ysgrifennu(cyflwr_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(bwrdd.ymholiad_system(22,INDEX));단말.문자(' ');단말.수(bwrdd.ymholiad_system(24,INDEX));단말.문자(' ');단말.수(bwrdd.ymholiad_system(23,INDEX));단말.문자(' ');
            for(int safle_INDEX=0;safle_INDEX<288;safle_INDEX++){int beit_VALUE=bwrdd.ymholiad_system(25,INDEX+safle_INDEX*4);if(beit_VALUE==0)break;bwrdd.직렬쓰기(beit_VALUE);}단말.문자(10);
        }
    }
    static void sioe_Storio() {
        int slot_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Cof_Ffeil.ffeil_COUNT;INDEX++)if(Cof_Ffeil.이름길이[INDEX]>0 || Cof_Ffeil.cyfeiriad_COUNT[INDEX]>0){slot_COUNT++;data_COUNT+=Cof_Ffeil.hyd_VALUE[INDEX];}
        단말.Ysgrifennu("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Cof_Ffeil.ffeil_COUNT*16384);단말.문자(' ');단말.수(slot_COUNT*16384);단말.문자(' ');단말.수((Cof_Ffeil.ffeil_COUNT-slot_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(slot_COUNT);단말.문자('/');단말.수(Cof_Ffeil.ffeil_COUNT);단말.Ysgrifennu(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void sioe_cyflwr_bf9821b5() {
        int 횟수=셸입출력.technoleg_gwybodaeth_rhyngweithiol()!=0?0:1;
        if(eitem_COUNT()>1){if(eitem_COUNT()!=3 || !같음(1,"-n") || (횟수=digid_VALUE(2,1000))<1){methiant_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 gadael_Rhaglen_55b3a1cd");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.technoleg_gwybodaeth_rhyngweithiol()!=0 && 횟수==0)단말.Ysgrifennu("\u001b[2J\u001b[H");
            sioe_Gweithgarwch();sioe_Cof();sioe_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!aros_cyflwr(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void sioe_help() {
        단말.Ysgrifennu("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Ysgrifennu(표준말(INDEX));단말.Ysgrifennu(" / ");단말.Ysgrifennu(관리명령.Word_SMS(INDEX));단말.Ysgrifennu(" : ");단말.Ysgrifennu(관리명령.설명(INDEX));단말.문자(10);}
        단말.Ysgrifennu("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Ysgrifennu("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Ysgrifennu("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Gweithredu_gorchymyn() {
        int Gorchymyn=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Gorchymyn=INDEX;
        if(같음(0,"ifconfig"))Gorchymyn=0;if(같음(0,"ss"))Gorchymyn=4;
        if(Gorchymyn<0)return false;
        if(Gorchymyn==11){if(같음(1,"net") || 같음(1,"system"))sioe_help();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.sioe_help();return true;}
        if(Gorchymyn==0 || Gorchymyn==1)Rhwydwaith_gorchymyn(Gorchymyn==1);
        else if(Gorchymyn==2)응답시험();
        else if(Gorchymyn==6)sioe_cyflwr_bf9821b5();
        else if(eitem_COUNT()!=1){methiant_VALUE("This command takes no arguments; help system");}
        else if(Gorchymyn==3)sioe_llwybr();else if(Gorchymyn==4)sioe_Rhwydwaith();else if(Gorchymyn==5)sioe_Tasks();else if(Gorchymyn==7)sioe_Cof();else if(Gorchymyn==8)sioe_Storio();else if(Gorchymyn==9)sioe_Gweithgarwch();
        else if(Gorchymyn==10)bwrdd.전원끄기();
        return true;
    }
}
