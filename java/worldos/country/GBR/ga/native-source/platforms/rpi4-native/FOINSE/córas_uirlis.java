// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** iarbhír_sonraí eithne_VALUE 상태를 읽는 IPv4·ICMP·작업·Cuimhne_VALUE·RAM 저장소 관리 Ordú. */
public final class córas_uirlis {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int mír_COUNT() { return 명령해석기.licín_COUNT; }
    static void teip_VALUE(String LÉIGHMÉ_eb81d7d9) { 명령해석기.tomhas=2; 단말.Scríobh(LÉIGHMÉ_eb81d7d9); 단말.문자(10); }
    static void ERREÁID(int VALUE) { 명령해석기.ERREÁID(VALUE); }
    static void 수항목(String Ainm, int VALUE) { 단말.Scríobh(Ainm); 단말.수(VALUE); 단말.문자(10); }
    static int digit_VALUE(int INDEX, int 한도) {
        if (INDEX>=mír_COUNT() || 명령해석기.fad_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.fad_VALUE[INDEX]; 순번++) {
            int carachtar_VALUE=명령해석기.licín_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (carachtar_VALUE<0 || carachtar_VALUE>9 || VALUE>(한도-carachtar_VALUE)/10) return -1;
            VALUE=VALUE*10+carachtar_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=mír_COUNT()) return false;
        int VALUE=0, 덩이=0, digit_COUNT=0, pointe_COUNT=0;
        for (int 순번=0; 순번<명령해석기.fad_VALUE[INDEX]; 순번++) {
            int carachtar_VALUE=명령해석기.licín_VALUE[명령해석기.시작점[INDEX]+순번];
            if (carachtar_VALUE=='.') { if (digit_COUNT==0 || ++pointe_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=digit_COUNT=0; }
            else { if (carachtar_VALUE<'0' || carachtar_VALUE>'9' || ++digit_COUNT>3) return false; 덩이=덩이*10+carachtar_VALUE-'0'; if(덩이>255)return false; }
        }
        if (pointe_COUNT!=3 || digit_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void scríobh_ADDRESS(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void seó_Líonra_staid() {
        단말.Scríobh(clár.Líonra_staid(20,0)!=0?"en0: ":"sl0: "); 단말.Scríobh(clár.Líonra_staid(3,0)!=0?"UP":"DOWN");
        단말.Scríobh(clár.Líonra_staid(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Scríobh(clár.Líonra_staid(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); scríobh_ADDRESS(clár.Líonra_staid(0,0));
        단말.Scríobh(" netmask "); scríobh_ADDRESS(clár.Líonra_staid(1,0)); 단말.Scríobh(" gateway "); scríobh_ADDRESS(clár.Líonra_staid(2,0)); 단말.문자(10);
        단말.Scríobh("  RX packets "); 단말.수(clár.Líonra_staid(4,0)); 단말.Scríobh(" bytes "); 단말.수(clár.Líonra_staid(6,0));
        단말.Scríobh(" TX packets "); 단말.수(clár.Líonra_staid(5,0)); 단말.Scríobh(" bytes "); 단말.수(clár.Líonra_staid(7,0)); 단말.문자(10);
        수항목("  dropped ",clár.Líonra_staid(8,0));
    }
    static void tacar_ADDRESS(int Rith_2) {
        if (mír_COUNT()!=Rith_2+3 || !주소읽기(Rith_2)) { teip_VALUE("사용법: ipconfig set ADDRESS 주소가림 geata_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(Rith_2+1)){teip_VALUE("Invalid IPv4 netmask");return;} int masc_VALUE=ADDRESS_VALUE;
        if(!주소읽기(Rith_2+2)){teip_VALUE("Invalid IPv4 gateway");return;}
        int tomhas=clár.Líonra_Socruithe(0,ADDRESS,masc_VALUE,ADDRESS_VALUE);
        if(tomhas<0) { ERREÁID(tomhas); if(tomhas==-16)단말.Scríobh("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Scríobh("IPv4 configuration applied (until reboot)\n"); seó_Líonra_staid(); }
    }
    static void Líonra_ordú(boolean seoladh_IP) {
        if (mír_COUNT()==1 || mír_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || mír_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { seó_Líonra_staid();return; }
        if (seoladh_IP && 같음(1,"route") && (mír_COUNT()==2 || mír_COUNT()==3&&같음(2,"show"))) { seó_cosán();return; }
        if (같음(1,"set")) { tacar_ADDRESS(2);return; }
        if (mír_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { clár.Líonra_Socruithe(같음(1,"up")?1:2,0,0,0);seó_Líonra_staid();return; }
        if (seoladh_IP && mír_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { clár.Líonra_Socruithe(같음(5,"up")?1:2,0,0,0);seó_Líonra_staid();return; }
        teip_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 geata_VALUE|link set dev sl0 up|down]");
    }
    static void seó_cosán() {
        단말.Scríobh("Destination Netmask Gateway Interface\n");
        scríobh_ADDRESS(clár.Líonra_staid(0,0)&clár.Líonra_staid(1,0));단말.문자(' ');scríobh_ADDRESS(clár.Líonra_staid(1,0));단말.Scríobh(clár.Líonra_staid(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (clár.Líonra_staid(2,0)!=0) {단말.Scríobh("0.0.0.0 0.0.0.0 ");scríobh_ADDRESS(clár.Líonra_staid(2,0));단말.Scríobh(clár.Líonra_staid(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void seó_Líonra() {
        단말.Scríobh("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_catagóir=clár.Líonra_staid(10,INDEX);if(TYPE_catagóir==0)continue;
            단말.Scríobh(TYPE_catagóir==1?"TCP ":"UDP ");scríobh_ADDRESS(clár.Líonra_staid(16,INDEX));단말.문자(':');단말.수(clár.Líonra_staid(11,INDEX));단말.문자(' ');
            scríobh_ADDRESS(clár.Líonra_staid(12,INDEX));단말.문자(':');단말.수(clár.Líonra_staid(13,INDEX));단말.문자(' ');
            int staid_VALUE=clár.Líonra_staid(14,INDEX);단말.Scríobh(TYPE_catagóir==2?"DATAGRAM":staid_VALUE==1?"LISTEN":staid_VALUE==2?"ESTABLISHED":staid_VALUE==3?"CLOSE_WAIT":staid_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(clár.Líonra_staid(15,INDEX));단말.문자(10);
        }
        단말.Scríobh("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Rith_2=clár.밀리초();
        while(clár.밀리초()-Rith_2<밀리초) {
            if(셸입출력.teicneolaíocht_faisnéise_idirghníomhach()!=0){int carachtar_VALUE=clár.직렬읽기();if(carachtar_VALUE==3 || carachtar_VALUE=='q' || carachtar_VALUE=='Q' || carachtar_VALUE==27 || carachtar_VALUE==-4096)return false;}
            clár.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, sprioc=-1;
        for(int suíomh_INDEX=1;suíomh_INDEX<mír_COUNT();suíomh_INDEX++) {
            if(같음(suíomh_INDEX,"-c")){횟수=digit_VALUE(++suíomh_INDEX,100);if(횟수<1){teip_VALUE("ping: -c 1..100");return;}}
            else if(같음(suíomh_INDEX,"-W")){제한=digit_VALUE(++suíomh_INDEX,10);if(제한<1){teip_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(sprioc<0)sprioc=suíomh_INDEX;else{teip_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(sprioc<0 || !주소읽기(sprioc)){teip_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Scríobh("PING ");scríobh_ADDRESS(ADDRESS);단말.Scríobh(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ord_VALUE=1;ord_VALUE<=횟수 && 계속;ord_VALUE++) {
            int 처리값=clár.응답보내기(ADDRESS,ord_VALUE);
            if(처리값<0){ERREÁID(처리값);break;}보낸수++;
            int Rith_2=clár.밀리초();
            while(clár.응답읽기(0)==-11 && clár.밀리초()-Rith_2<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(clár.응답읽기(0)==0){
                int TIME_VALUE=clár.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Scríobh("32 bytes from ");scríobh_ADDRESS(ADDRESS);단말.Scríobh(" seq=");단말.수(ord_VALUE);단말.Scríobh(" ttl=");단말.수(clár.응답읽기(2));단말.Scríobh(" time=");단말.수(TIME_VALUE);단말.Scríobh(" ms\n");
            }else{단말.Scríobh("Request timeout seq=");단말.수(ord_VALUE);단말.문자(10);}
            if(ord_VALUE<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Scríobh(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Scríobh(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Scríobh("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Scríobh("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Scríobh(" ms\n");}
        명령해석기.tomhas=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void seó_Gníomhaíocht() { 단말.Scríobh("up ");단말.수(clár.밀리초()/1000);단말.Scríobh(" seconds\n"); }
    static void seó_Cuimhne() {
        수항목("ARM RAM KiB (firmware): ",clár.iarratas_córas(0,0));
        수항목("Kernel image+BSS+stack KiB: ",clár.iarratas_córas(1,0));
        int 총량=clár.iarratas_córas(2,0), 사용량=clár.iarratas_córas(3,0);
        단말.Scríobh("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",clár.iarratas_córas(4,0));
        수항목("EL0 arena+session reserve KiB: ",clár.iarratas_córas(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=clár.iarratas_córas(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Scríobh("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void seó_Tasks() {
        단말.Scríobh("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Scríobh("1 - RUN - - ");단말.수(clár.밀리초());단말.Scríobh(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(clár.tasc_staid(INDEX)>0){단말.수(INDEX+1);단말.Scríobh(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int staid_VALUE=clár.iarratas_córas(20,INDEX);if(staid_VALUE==0)continue;
            단말.수(clár.iarratas_córas(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Scríobh(staid_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(clár.iarratas_córas(22,INDEX));단말.문자(' ');단말.수(clár.iarratas_córas(24,INDEX));단말.문자(' ');단말.수(clár.iarratas_córas(23,INDEX));단말.문자(' ');
            for(int suíomh_INDEX=0;suíomh_INDEX<288;suíomh_INDEX++){int beart_VALUE=clár.iarratas_córas(25,INDEX+suíomh_INDEX*4);if(beart_VALUE==0)break;clár.직렬쓰기(beart_VALUE);}단말.문자(10);
        }
    }
    static void seó_Stóras() {
        int spás_COUNT=0, sonraí_COUNT=0;
        for(int INDEX=0;INDEX<Cuimhne_Comhaid.comhad_COUNT;INDEX++)if(Cuimhne_Comhaid.이름길이[INDEX]>0 || Cuimhne_Comhaid.Leabhair_thagartha_COUNT[INDEX]>0){spás_COUNT++;sonraí_COUNT+=Cuimhne_Comhaid.fad_VALUE[INDEX];}
        단말.Scríobh("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Cuimhne_Comhaid.comhad_COUNT*16384);단말.문자(' ');단말.수(spás_COUNT*16384);단말.문자(' ');단말.수((Cuimhne_Comhaid.comhad_COUNT-spás_COUNT)*16384);단말.문자(' ');단말.수(sonraí_COUNT);단말.문자(' ');단말.수(spás_COUNT);단말.문자('/');단말.수(Cuimhne_Comhaid.comhad_COUNT);단말.Scríobh(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void seó_staid_bf9821b5() {
        int 횟수=셸입출력.teicneolaíocht_faisnéise_idirghníomhach()!=0?0:1;
        if(mír_COUNT()>1){if(mír_COUNT()!=3 || !같음(1,"-n") || (횟수=digit_VALUE(2,1000))<1){teip_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 scoir_clár_55b3a1cd");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.teicneolaíocht_faisnéise_idirghníomhach()!=0 && 횟수==0)단말.Scríobh("\u001b[2J\u001b[H");
            seó_Gníomhaíocht();seó_Cuimhne();seó_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void seó_cabhair() {
        단말.Scríobh("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Scríobh(표준말(INDEX));단말.Scríobh(" / ");단말.Scríobh(관리명령.Word_SMS(INDEX));단말.Scríobh(" : ");단말.Scríobh(관리명령.설명(INDEX));단말.문자(10);}
        단말.Scríobh("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Scríobh("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Scríobh("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Rith_ordú() {
        int Ordú=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Ordú=INDEX;
        if(같음(0,"ifconfig"))Ordú=0;if(같음(0,"ss"))Ordú=4;
        if(Ordú<0)return false;
        if(Ordú==11){if(같음(1,"net") || 같음(1,"system"))seó_cabhair();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.seó_cabhair();return true;}
        if(Ordú==0 || Ordú==1)Líonra_ordú(Ordú==1);
        else if(Ordú==2)응답시험();
        else if(Ordú==6)seó_staid_bf9821b5();
        else if(mír_COUNT()!=1){teip_VALUE("This command takes no arguments; help system");}
        else if(Ordú==3)seó_cosán();else if(Ordú==4)seó_Líonra();else if(Ordú==5)seó_Tasks();else if(Ordú==7)seó_Cuimhne();else if(Ordú==8)seó_Stóras();else if(Ordú==9)seó_Gníomhaíocht();
        else if(Ordú==10)clár.전원끄기();
        return true;
    }
}
