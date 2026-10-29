// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** totoo_data kernel_VALUE 상태를 읽는 IPv4·ICMP·작업·Memory_VALUE·RAM repository_root 관리 utos. */
public final class system_tool {
    static int email_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int item_COUNT() { return 명령해석기.token_COUNT; }
    static void pagpalya_VALUE(String BASAHINAKO_eb81d7d9) { 명령해석기.sukat=2; 단말.sumulat(BASAHINAKO_eb81d7d9); 단말.문자(10); }
    static void error(int VALUE) { 명령해석기.error(VALUE); }
    static void 수항목(String pangalan, int VALUE) { 단말.sumulat(pangalan); 단말.수(VALUE); 단말.문자(10); }
    static int digit_VALUE(int INDEX, int 한도) {
        if (INDEX>=item_COUNT() || 명령해석기.haba_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.haba_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (karakter_VALUE<0 || karakter_VALUE>9 || VALUE>(한도-karakter_VALUE)/10) return -1;
            VALUE=VALUE*10+karakter_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=item_COUNT()) return false;
        int VALUE=0, 덩이=0, digit_COUNT=0, point_COUNT=0;
        for (int 순번=0; 순번<명령해석기.haba_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=명령해석기.token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (karakter_VALUE=='.') { if (digit_COUNT==0 || ++point_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=digit_COUNT=0; }
            else { if (karakter_VALUE<'0' || karakter_VALUE>'9' || ++digit_COUNT>3) return false; 덩이=덩이*10+karakter_VALUE-'0'; if(덩이>255)return false; }
        }
        if (point_COUNT!=3 || digit_COUNT==0) return false;
        email_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void sumulat_email(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void ipakita_Network_katayuan() {
        단말.sumulat(board.Network_katayuan(20,0)!=0?"en0: ":"sl0: "); 단말.sumulat(board.Network_katayuan(3,0)!=0?"UP":"DOWN");
        단말.sumulat(board.Network_katayuan(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.sumulat(board.Network_katayuan(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); sumulat_email(board.Network_katayuan(0,0));
        단말.sumulat(" netmask "); sumulat_email(board.Network_katayuan(1,0)); 단말.sumulat(" gateway "); sumulat_email(board.Network_katayuan(2,0)); 단말.문자(10);
        단말.sumulat("  RX packets "); 단말.수(board.Network_katayuan(4,0)); 단말.sumulat(" bytes "); 단말.수(board.Network_katayuan(6,0));
        단말.sumulat(" TX packets "); 단말.수(board.Network_katayuan(5,0)); 단말.sumulat(" bytes "); 단말.수(board.Network_katayuan(7,0)); 단말.문자(10);
        수항목("  dropped ",board.Network_katayuan(8,0));
    }
    static void set_email(int run) {
        if (item_COUNT()!=run+3 || !주소읽기(run)) { pagpalya_VALUE("사용법: ipconfig set email 주소가림 entrada_VALUE"); return; }
        int email=email_VALUE;
        if(!주소읽기(run+1)){pagpalya_VALUE("Invalid IPv4 netmask");return;} int mask_VALUE=email_VALUE;
        if(!주소읽기(run+2)){pagpalya_VALUE("Invalid IPv4 gateway");return;}
        int sukat=board.Network_Mga_Setting(0,email,mask_VALUE,email_VALUE);
        if(sukat<0) { error(sukat); if(sukat==-16)단말.sumulat("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.sumulat("IPv4 configuration applied (until reboot)\n"); ipakita_Network_katayuan(); }
    }
    static void Network_utos(boolean IP_address) {
        if (item_COUNT()==1 || item_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { ipakita_Network_katayuan();return; }
        if (IP_address && 같음(1,"route") && (item_COUNT()==2 || item_COUNT()==3&&같음(2,"show"))) { ipakita_path();return; }
        if (같음(1,"set")) { set_email(2);return; }
        if (item_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { board.Network_Mga_Setting(같음(1,"up")?1:2,0,0,0);ipakita_Network_katayuan();return; }
        if (IP_address && item_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { board.Network_Mga_Setting(같음(5,"up")?1:2,0,0,0);ipakita_Network_katayuan();return; }
        pagpalya_VALUE("사용법: ip [addr show|route show|set email 주소가림 entrada_VALUE|link set dev sl0 up|down]");
    }
    static void ipakita_path() {
        단말.sumulat("Destination Netmask Gateway Interface\n");
        sumulat_email(board.Network_katayuan(0,0)&board.Network_katayuan(1,0));단말.문자(' ');sumulat_email(board.Network_katayuan(1,0));단말.sumulat(board.Network_katayuan(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (board.Network_katayuan(2,0)!=0) {단말.sumulat("0.0.0.0 0.0.0.0 ");sumulat_email(board.Network_katayuan(2,0));단말.sumulat(board.Network_katayuan(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void ipakita_Network() {
        단말.sumulat("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_kategorya=board.Network_katayuan(10,INDEX);if(TYPE_kategorya==0)continue;
            단말.sumulat(TYPE_kategorya==1?"TCP ":"UDP ");sumulat_email(board.Network_katayuan(16,INDEX));단말.문자(':');단말.수(board.Network_katayuan(11,INDEX));단말.문자(' ');
            sumulat_email(board.Network_katayuan(12,INDEX));단말.문자(':');단말.수(board.Network_katayuan(13,INDEX));단말.문자(' ');
            int katayuan_VALUE=board.Network_katayuan(14,INDEX);단말.sumulat(TYPE_kategorya==2?"DATAGRAM":katayuan_VALUE==1?"LISTEN":katayuan_VALUE==2?"ESTABLISHED":katayuan_VALUE==3?"CLOSE_WAIT":katayuan_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(board.Network_katayuan(15,INDEX));단말.문자(10);
        }
        단말.sumulat("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean maghintay_katayuan(int 밀리초) {
        int run=board.밀리초();
        while(board.밀리초()-run<밀리초) {
            if(셸입출력.information_technology_tumutugon_interactive()!=0){int karakter_VALUE=board.직렬읽기();if(karakter_VALUE==3 || karakter_VALUE=='q' || karakter_VALUE=='Q' || karakter_VALUE==27 || karakter_VALUE==-4096)return false;}
            board.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, layunin=-1;
        for(int posisyon_INDEX=1;posisyon_INDEX<item_COUNT();posisyon_INDEX++) {
            if(같음(posisyon_INDEX,"-c")){횟수=digit_VALUE(++posisyon_INDEX,100);if(횟수<1){pagpalya_VALUE("ping: -c 1..100");return;}}
            else if(같음(posisyon_INDEX,"-W")){제한=digit_VALUE(++posisyon_INDEX,10);if(제한<1){pagpalya_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(layunin<0)layunin=posisyon_INDEX;else{pagpalya_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(layunin<0 || !주소읽기(layunin)){pagpalya_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int email=email_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.sumulat("PING ");sumulat_email(email);단말.sumulat(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int pagkakasunud_sunod_VALUE=1;pagkakasunud_sunod_VALUE<=횟수 && 계속;pagkakasunud_sunod_VALUE++) {
            int 처리값=board.응답보내기(email,pagkakasunud_sunod_VALUE);
            if(처리값<0){error(처리값);break;}보낸수++;
            int run=board.밀리초();
            while(board.응답읽기(0)==-11 && board.밀리초()-run<제한)if(!maghintay_katayuan(1)){계속=false;break;}
            if(!계속)break;
            if(board.응답읽기(0)==0){
                int TIME_VALUE=board.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.sumulat("32 bytes from ");sumulat_email(email);단말.sumulat(" seq=");단말.수(pagkakasunud_sunod_VALUE);단말.sumulat(" ttl=");단말.수(board.응답읽기(2));단말.sumulat(" time=");단말.수(TIME_VALUE);단말.sumulat(" ms\n");
            }else{단말.sumulat("Request timeout seq=");단말.수(pagkakasunud_sunod_VALUE);단말.문자(10);}
            if(pagkakasunud_sunod_VALUE<횟수)계속=maghintay_katayuan(200);
        }
        단말.수(보낸수);단말.sumulat(" transmitted, ");단말.수(RECEIVED_COUNT);단말.sumulat(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.sumulat("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.sumulat("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.sumulat(" ms\n");}
        명령해석기.sukat=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void ipakita_Aktibidad() { 단말.sumulat("up ");단말.수(board.밀리초()/1000);단말.sumulat(" seconds\n"); }
    static void ipakita_Memory() {
        수항목("ARM RAM KiB (firmware): ",board.query_system(0,0));
        수항목("Kernel image+BSS+stack KiB: ",board.query_system(1,0));
        int 총량=board.query_system(2,0), 사용량=board.query_system(3,0);
        단말.sumulat("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",board.query_system(4,0));
        수항목("EL0 arena+session reserve KiB: ",board.query_system(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=board.query_system(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.sumulat("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void ipakita_Tasks() {
        단말.sumulat("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.sumulat("1 - RUN - - ");단말.수(board.밀리초());단말.sumulat(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(board.gawain_katayuan(INDEX)>0){단말.수(INDEX+1);단말.sumulat(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int katayuan_VALUE=board.query_system(20,INDEX);if(katayuan_VALUE==0)continue;
            단말.수(board.query_system(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.sumulat(katayuan_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(board.query_system(22,INDEX));단말.문자(' ');단말.수(board.query_system(24,INDEX));단말.문자(' ');단말.수(board.query_system(23,INDEX));단말.문자(' ');
            for(int posisyon_INDEX=0;posisyon_INDEX<288;posisyon_INDEX++){int byte_VALUE=board.query_system(25,INDEX+posisyon_INDEX*4);if(byte_VALUE==0)break;board.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void ipakita_Storage() {
        int espasyo_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Memory_Mga_File.file_COUNT;INDEX++)if(Memory_Mga_File.이름길이[INDEX]>0 || Memory_Mga_File.Sanggunian_COUNT[INDEX]>0){espasyo_COUNT++;data_COUNT+=Memory_Mga_File.haba_VALUE[INDEX];}
        단말.sumulat("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memory_Mga_File.file_COUNT*16384);단말.문자(' ');단말.수(espasyo_COUNT*16384);단말.문자(' ');단말.수((Memory_Mga_File.file_COUNT-espasyo_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(espasyo_COUNT);단말.문자('/');단말.수(Memory_Mga_File.file_COUNT);단말.sumulat(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void ipakita_katayuan_bf9821b5() {
        int 횟수=셸입출력.information_technology_tumutugon_interactive()!=0?0:1;
        if(item_COUNT()>1){if(item_COUNT()!=3 || !같음(1,"-n") || (횟수=digit_VALUE(2,1000))<1){pagpalya_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 lumabas_app");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.information_technology_tumutugon_interactive()!=0 && 횟수==0)단말.sumulat("\u001b[2J\u001b[H");
            ipakita_Aktibidad();ipakita_Memory();ipakita_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!maghintay_katayuan(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void ipakita_tulong() {
        단말.sumulat("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.sumulat(표준말(INDEX));단말.sumulat(" / ");단말.sumulat(관리명령.Word_SMS(INDEX));단말.sumulat(" : ");단말.sumulat(관리명령.설명(INDEX));단말.문자(10);}
        단말.sumulat("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.sumulat("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.sumulat("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Mag_execute_utos() {
        int utos=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))utos=INDEX;
        if(같음(0,"ifconfig"))utos=0;if(같음(0,"ss"))utos=4;
        if(utos<0)return false;
        if(utos==11){if(같음(1,"net") || 같음(1,"system"))ipakita_tulong();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.ipakita_tulong();return true;}
        if(utos==0 || utos==1)Network_utos(utos==1);
        else if(utos==2)응답시험();
        else if(utos==6)ipakita_katayuan_bf9821b5();
        else if(item_COUNT()!=1){pagpalya_VALUE("This command takes no arguments; help system");}
        else if(utos==3)ipakita_path();else if(utos==4)ipakita_Network();else if(utos==5)ipakita_Tasks();else if(utos==7)ipakita_Memory();else if(utos==8)ipakita_Storage();else if(utos==9)ipakita_Aktibidad();
        else if(utos==10)board.전원끄기();
        return true;
    }
}
