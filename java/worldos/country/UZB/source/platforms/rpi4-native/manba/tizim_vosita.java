// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** real_ma_lumotlar o_zak_VALUE 상태를 읽는 IPv4·ICMP·작업·Xotira_VALUE·RAM repozitoriy_ildiz 관리 Buyruq. */
public final class tizim_vosita {
    static int manzil_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int element_COUNT() { return 명령해석기.token_COUNT; }
    static void to_xtab_qolish_VALUE(String ma_lumot_fayli_eb81d7d9) { 명령해석기.o_lchov=2; 단말.Yozish(ma_lumot_fayli_eb81d7d9); 단말.문자(10); }
    static void Xato(int VALUE) { 명령해석기.Xato(VALUE); }
    static void 수항목(String Nomi, int VALUE) { 단말.Yozish(Nomi); 단말.수(VALUE); 단말.문자(10); }
    static int raqam_VALUE(int INDEX, int 한도) {
        if (INDEX>=element_COUNT() || 명령해석기.uzunlik_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.uzunlik_VALUE[INDEX]; 순번++) {
            int belgi_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (belgi_VALUE<0 || belgi_VALUE>9 || VALUE>(한도-belgi_VALUE)/10) return -1;
            VALUE=VALUE*10+belgi_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=element_COUNT()) return false;
        int VALUE=0, 덩이=0, raqam_COUNT=0, nuqta_COUNT=0;
        for (int 순번=0; 순번<명령해석기.uzunlik_VALUE[INDEX]; 순번++) {
            int belgi_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (belgi_VALUE=='.') { if (raqam_COUNT==0 || ++nuqta_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=raqam_COUNT=0; }
            else { if (belgi_VALUE<'0' || belgi_VALUE>'9' || ++raqam_COUNT>3) return false; 덩이=덩이*10+belgi_VALUE-'0'; if(덩이>255)return false; }
        }
        if (nuqta_COUNT!=3 || raqam_COUNT==0) return false;
        manzil_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void yozmoq_manzil(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void ko_rsatmoq_Tarmoq_holat() {
        단말.Yozish(yozuv_taxtasi.Tarmoq_holat(20,0)!=0?"en0: ":"sl0: "); 단말.Yozish(yozuv_taxtasi.Tarmoq_holat(3,0)!=0?"UP":"DOWN");
        단말.Yozish(yozuv_taxtasi.Tarmoq_holat(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Yozish(yozuv_taxtasi.Tarmoq_holat(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(0,0));
        단말.Yozish(" netmask "); yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(1,0)); 단말.Yozish(" gateway "); yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(2,0)); 단말.문자(10);
        단말.Yozish("  RX packets "); 단말.수(yozuv_taxtasi.Tarmoq_holat(4,0)); 단말.Yozish(" bytes "); 단말.수(yozuv_taxtasi.Tarmoq_holat(6,0));
        단말.Yozish(" TX packets "); 단말.수(yozuv_taxtasi.Tarmoq_holat(5,0)); 단말.Yozish(" bytes "); 단말.수(yozuv_taxtasi.Tarmoq_holat(7,0)); 단말.문자(10);
        수항목("  dropped ",yozuv_taxtasi.Tarmoq_holat(8,0));
    }
    static void to_plam_manzil(int Bajarish) {
        if (element_COUNT()!=Bajarish+3 || !주소읽기(Bajarish)) { to_xtab_qolish_VALUE("사용법: ipconfig set manzil 주소가림 shluz_VALUE"); return; }
        int manzil=manzil_VALUE;
        if(!주소읽기(Bajarish+1)){to_xtab_qolish_VALUE("Invalid IPv4 netmask");return;} int niqob_VALUE=manzil_VALUE;
        if(!주소읽기(Bajarish+2)){to_xtab_qolish_VALUE("Invalid IPv4 gateway");return;}
        int o_lchov=yozuv_taxtasi.Tarmoq_Sozlamalar(0,manzil,niqob_VALUE,manzil_VALUE);
        if(o_lchov<0) { Xato(o_lchov); if(o_lchov==-16)단말.Yozish("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Yozish("IPv4 configuration applied (until reboot)\n"); ko_rsatmoq_Tarmoq_holat(); }
    }
    static void Tarmoq_buyruq(boolean IP_manzil) {
        if (element_COUNT()==1 || element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { ko_rsatmoq_Tarmoq_holat();return; }
        if (IP_manzil && 같음(1,"route") && (element_COUNT()==2 || element_COUNT()==3&&같음(2,"show"))) { ko_rsatmoq_yo_l();return; }
        if (같음(1,"set")) { to_plam_manzil(2);return; }
        if (element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { yozuv_taxtasi.Tarmoq_Sozlamalar(같음(1,"up")?1:2,0,0,0);ko_rsatmoq_Tarmoq_holat();return; }
        if (IP_manzil && element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { yozuv_taxtasi.Tarmoq_Sozlamalar(같음(5,"up")?1:2,0,0,0);ko_rsatmoq_Tarmoq_holat();return; }
        to_xtab_qolish_VALUE("사용법: ip [addr show|route show|set manzil 주소가림 shluz_VALUE|link set dev sl0 up|down]");
    }
    static void ko_rsatmoq_yo_l() {
        단말.Yozish("Destination Netmask Gateway Interface\n");
        yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(0,0)&yozuv_taxtasi.Tarmoq_holat(1,0));단말.문자(' ');yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(1,0));단말.Yozish(yozuv_taxtasi.Tarmoq_holat(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (yozuv_taxtasi.Tarmoq_holat(2,0)!=0) {단말.Yozish("0.0.0.0 0.0.0.0 ");yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(2,0));단말.Yozish(yozuv_taxtasi.Tarmoq_holat(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void ko_rsatmoq_Tarmoq() {
        단말.Yozish("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_toifa=yozuv_taxtasi.Tarmoq_holat(10,INDEX);if(TYPE_toifa==0)continue;
            단말.Yozish(TYPE_toifa==1?"TCP ":"UDP ");yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(16,INDEX));단말.문자(':');단말.수(yozuv_taxtasi.Tarmoq_holat(11,INDEX));단말.문자(' ');
            yozmoq_manzil(yozuv_taxtasi.Tarmoq_holat(12,INDEX));단말.문자(':');단말.수(yozuv_taxtasi.Tarmoq_holat(13,INDEX));단말.문자(' ');
            int holat_VALUE_e10195a1=yozuv_taxtasi.Tarmoq_holat(14,INDEX);단말.Yozish(TYPE_toifa==2?"DATAGRAM":holat_VALUE_e10195a1==1?"LISTEN":holat_VALUE_e10195a1==2?"ESTABLISHED":holat_VALUE_e10195a1==3?"CLOSE_WAIT":holat_VALUE_e10195a1==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(yozuv_taxtasi.Tarmoq_holat(15,INDEX));단말.문자(10);
        }
        단말.Yozish("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean bir_daqiqa_holat(int 밀리초) {
        int Bajarish=yozuv_taxtasi.밀리초();
        while(yozuv_taxtasi.밀리초()-Bajarish<밀리초) {
            if(셸입출력.대화가능()!=0){int belgi_VALUE=yozuv_taxtasi.직렬읽기();if(belgi_VALUE==3 || belgi_VALUE=='q' || belgi_VALUE=='Q' || belgi_VALUE==27 || belgi_VALUE==-4096)return false;}
            yozuv_taxtasi.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, nishon=-1;
        for(int holat_INDEX=1;holat_INDEX<element_COUNT();holat_INDEX++) {
            if(같음(holat_INDEX,"-c")){횟수=raqam_VALUE(++holat_INDEX,100);if(횟수<1){to_xtab_qolish_VALUE("ping: -c 1..100");return;}}
            else if(같음(holat_INDEX,"-W")){제한=raqam_VALUE(++holat_INDEX,10);if(제한<1){to_xtab_qolish_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(nishon<0)nishon=holat_INDEX;else{to_xtab_qolish_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(nishon<0 || !주소읽기(nishon)){to_xtab_qolish_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int manzil=manzil_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Yozish("PING ");yozmoq_manzil(manzil);단말.Yozish(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tartib_VALUE=1;tartib_VALUE<=횟수 && 계속;tartib_VALUE++) {
            int 처리값=yozuv_taxtasi.응답보내기(manzil,tartib_VALUE);
            if(처리값<0){Xato(처리값);break;}보낸수++;
            int Bajarish=yozuv_taxtasi.밀리초();
            while(yozuv_taxtasi.응답읽기(0)==-11 && yozuv_taxtasi.밀리초()-Bajarish<제한)if(!bir_daqiqa_holat(1)){계속=false;break;}
            if(!계속)break;
            if(yozuv_taxtasi.응답읽기(0)==0){
                int TIME_VALUE=yozuv_taxtasi.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Yozish("32 bytes from ");yozmoq_manzil(manzil);단말.Yozish(" seq=");단말.수(tartib_VALUE);단말.Yozish(" ttl=");단말.수(yozuv_taxtasi.응답읽기(2));단말.Yozish(" time=");단말.수(TIME_VALUE);단말.Yozish(" ms\n");
            }else{단말.Yozish("Request timeout seq=");단말.수(tartib_VALUE);단말.문자(10);}
            if(tartib_VALUE<횟수)계속=bir_daqiqa_holat(200);
        }
        단말.수(보낸수);단말.Yozish(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Yozish(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Yozish("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Yozish("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Yozish(" ms\n");}
        명령해석기.o_lchov=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void ko_rsatmoq_harakat() { 단말.Yozish("up ");단말.수(yozuv_taxtasi.밀리초()/1000);단말.Yozish(" seconds\n"); }
    static void ko_rsatmoq_Xotira() {
        수항목("ARM RAM KiB (firmware): ",yozuv_taxtasi.so_rov_tizim(0,0));
        수항목("Kernel image+BSS+stack KiB: ",yozuv_taxtasi.so_rov_tizim(1,0));
        int 총량=yozuv_taxtasi.so_rov_tizim(2,0), 사용량=yozuv_taxtasi.so_rov_tizim(3,0);
        단말.Yozish("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",yozuv_taxtasi.so_rov_tizim(4,0));
        수항목("EL0 arena+session reserve KiB: ",yozuv_taxtasi.so_rov_tizim(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=yozuv_taxtasi.so_rov_tizim(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Yozish("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void ko_rsatmoq_Tasks() {
        단말.Yozish("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Yozish("1 - RUN - - ");단말.수(yozuv_taxtasi.밀리초());단말.Yozish(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(yozuv_taxtasi.vazifa_holat(INDEX)>0){단말.수(INDEX+1);단말.Yozish(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int holat_VALUE_e10195a1=yozuv_taxtasi.so_rov_tizim(20,INDEX);if(holat_VALUE_e10195a1==0)continue;
            단말.수(yozuv_taxtasi.so_rov_tizim(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Yozish(holat_VALUE_e10195a1==1?" RUN ":" SUSPENDED ");
            단말.수(yozuv_taxtasi.so_rov_tizim(22,INDEX));단말.문자(' ');단말.수(yozuv_taxtasi.so_rov_tizim(24,INDEX));단말.문자(' ');단말.수(yozuv_taxtasi.so_rov_tizim(23,INDEX));단말.문자(' ');
            for(int holat_INDEX=0;holat_INDEX<288;holat_INDEX++){int bayt_VALUE=yozuv_taxtasi.so_rov_tizim(25,INDEX+holat_INDEX*4);if(bayt_VALUE==0)break;yozuv_taxtasi.직렬쓰기(bayt_VALUE);}단말.문자(10);
        }
    }
    static void ko_rsatmoq_Xotira_deafe149() {
        int in_COUNT=0, ma_lumotlar_COUNT=0;
        for(int INDEX=0;INDEX<Xotira_Fayllar.fayl_COUNT;INDEX++)if(Xotira_Fayllar.이름길이[INDEX]>0 || Xotira_Fayllar.Ma_lumotnomalar_COUNT[INDEX]>0){in_COUNT++;ma_lumotlar_COUNT+=Xotira_Fayllar.uzunlik_VALUE[INDEX];}
        단말.Yozish("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Xotira_Fayllar.fayl_COUNT*16384);단말.문자(' ');단말.수(in_COUNT*16384);단말.문자(' ');단말.수((Xotira_Fayllar.fayl_COUNT-in_COUNT)*16384);단말.문자(' ');단말.수(ma_lumotlar_COUNT);단말.문자(' ');단말.수(in_COUNT);단말.문자('/');단말.수(Xotira_Fayllar.fayl_COUNT);단말.Yozish(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void ko_rsatmoq_holat_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(element_COUNT()>1){if(element_COUNT()!=3 || !같음(1,"-n") || (횟수=raqam_VALUE(2,1000))<1){to_xtab_qolish_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 tugatish_ilova");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Yozish("\u001b[2J\u001b[H");
            ko_rsatmoq_harakat();ko_rsatmoq_Xotira();ko_rsatmoq_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!bir_daqiqa_holat(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void ko_rsatmoq_yordam() {
        단말.Yozish("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Yozish(표준말(INDEX));단말.Yozish(" / ");단말.Yozish(관리명령.Word_SMS(INDEX));단말.Yozish(" : ");단말.Yozish(관리명령.설명(INDEX));단말.문자(10);}
        단말.Yozish("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Yozish("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Yozish("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean bajarmoq_buyruq() {
        int Buyruq=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Buyruq=INDEX;
        if(같음(0,"ifconfig"))Buyruq=0;if(같음(0,"ss"))Buyruq=4;
        if(Buyruq<0)return false;
        if(Buyruq==11){if(같음(1,"net") || 같음(1,"system"))ko_rsatmoq_yordam();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.ko_rsatmoq_yordam();return true;}
        if(Buyruq==0 || Buyruq==1)Tarmoq_buyruq(Buyruq==1);
        else if(Buyruq==2)응답시험();
        else if(Buyruq==6)ko_rsatmoq_holat_bf9821b5();
        else if(element_COUNT()!=1){to_xtab_qolish_VALUE("This command takes no arguments; help system");}
        else if(Buyruq==3)ko_rsatmoq_yo_l();else if(Buyruq==4)ko_rsatmoq_Tarmoq();else if(Buyruq==5)ko_rsatmoq_Tasks();else if(Buyruq==7)ko_rsatmoq_Xotira();else if(Buyruq==8)ko_rsatmoq_Xotira_deafe149();else if(Buyruq==9)ko_rsatmoq_harakat();
        else if(Buyruq==10)yozuv_taxtasi.전원끄기();
        return true;
    }
}
