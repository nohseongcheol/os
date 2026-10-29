// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** raun_gögn kjarni_VALUE 상태를 읽는 IPv4·ICMP·작업·Minni_VALUE·RAM gagnageymsla_rót 관리 Skipun. */
public final class kerfi_verkfæri {
    static int slóð_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int vara_COUNT() { return 명령해석기.tákn_COUNT; }
    static void bilun_VALUE(String LESTUMIG_eb81d7d9) { 명령해석기.NIÐURSTAÐA=2; 단말.Skrift(LESTUMIG_eb81d7d9); 단말.문자(10); }
    static void Villa(int VALUE) { 명령해석기.Villa(VALUE); }
    static void númer_færsla(String Heiti, int VALUE) { 단말.Skrift(Heiti); 단말.númer(VALUE); 단말.문자(10); }
    static int tölustafur_VALUE(int INDEX, int 한도) {
        if (INDEX>=vara_COUNT() || 명령해석기.lengd_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.lengd_VALUE[INDEX]; 순번++) {
            int stafur_VALUE=명령해석기.tákn_VALUE_eb540501[명령해석기.시작점[INDEX]+순번]-'0';
            if (stafur_VALUE<0 || stafur_VALUE>9 || VALUE>(한도-stafur_VALUE)/10) return -1;
            VALUE=VALUE*10+stafur_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=vara_COUNT()) return false;
        int VALUE=0, 덩이=0, tölustafur_COUNT=0, P_COUNT=0;
        for (int 순번=0; 순번<명령해석기.lengd_VALUE[INDEX]; 순번++) {
            int stafur_VALUE=명령해석기.tákn_VALUE_eb540501[명령해석기.시작점[INDEX]+순번];
            if (stafur_VALUE=='.') { if (tölustafur_COUNT==0 || ++P_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=tölustafur_COUNT=0; }
            else { if (stafur_VALUE<'0' || stafur_VALUE>'9' || ++tölustafur_COUNT>3) return false; 덩이=덩이*10+stafur_VALUE-'0'; if(덩이>255)return false; }
        }
        if (P_COUNT!=3 || tölustafur_COUNT==0) return false;
        slóð_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void skrifa_slóð(int VALUE) {
        단말.númer((VALUE>>>24)&255); 단말.문자('.'); 단말.númer((VALUE>>>16)&255); 단말.문자('.');
        단말.númer((VALUE>>>8)&255); 단말.문자('.'); 단말.númer(VALUE&255);
    }
    static void sýna_Net_staða() {
        단말.Skrift(bretti.Net_staða(20,0)!=0?"en0: ":"sl0: "); 단말.Skrift(bretti.Net_staða(3,0)!=0?"UP":"DOWN");
        단말.Skrift(bretti.Net_staða(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Skrift(bretti.Net_staða(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); skrifa_slóð(bretti.Net_staða(0,0));
        단말.Skrift(" netmask "); skrifa_slóð(bretti.Net_staða(1,0)); 단말.Skrift(" gateway "); skrifa_slóð(bretti.Net_staða(2,0)); 단말.문자(10);
        단말.Skrift("  RX packets "); 단말.númer(bretti.Net_staða(4,0)); 단말.Skrift(" bytes "); 단말.númer(bretti.Net_staða(6,0));
        단말.Skrift(" TX packets "); 단말.númer(bretti.Net_staða(5,0)); 단말.Skrift(" bytes "); 단말.númer(bretti.Net_staða(7,0)); 단말.문자(10);
        númer_færsla("  dropped ",bretti.Net_staða(8,0));
    }
    static void sett_slóð(int Keyra_2) {
        if (vara_COUNT()!=Keyra_2+3 || !주소읽기(Keyra_2)) { bilun_VALUE("사용법: ipconfig set slóð 주소가림 gátt_VALUE_cfee51e8"); return; }
        int slóð=slóð_VALUE;
        if(!주소읽기(Keyra_2+1)){bilun_VALUE("Invalid IPv4 netmask");return;} int sía_VALUE_3fef50ae=slóð_VALUE;
        if(!주소읽기(Keyra_2+2)){bilun_VALUE("Invalid IPv4 gateway");return;}
        int NIÐURSTAÐA=bretti.Net_Stillingar(0,slóð,sía_VALUE_3fef50ae,slóð_VALUE);
        if(NIÐURSTAÐA<0) { Villa(NIÐURSTAÐA); if(NIÐURSTAÐA==-16)단말.Skrift("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Skrift("IPv4 configuration applied (until reboot)\n"); sýna_Net_staða(); }
    }
    static void Net_skipun(boolean IP_tala) {
        if (vara_COUNT()==1 || vara_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || vara_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { sýna_Net_staða();return; }
        if (IP_tala && 같음(1,"route") && (vara_COUNT()==2 || vara_COUNT()==3&&같음(2,"show"))) { sýna_slóð();return; }
        if (같음(1,"set")) { sett_slóð(2);return; }
        if (vara_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { bretti.Net_Stillingar(같음(1,"up")?1:2,0,0,0);sýna_Net_staða();return; }
        if (IP_tala && vara_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { bretti.Net_Stillingar(같음(5,"up")?1:2,0,0,0);sýna_Net_staða();return; }
        bilun_VALUE("사용법: ip [addr show|route show|set slóð 주소가림 gátt_VALUE_cfee51e8|link set dev sl0 up|down]");
    }
    static void sýna_slóð() {
        단말.Skrift("Destination Netmask Gateway Interface\n");
        skrifa_slóð(bretti.Net_staða(0,0)&bretti.Net_staða(1,0));단말.문자(' ');skrifa_slóð(bretti.Net_staða(1,0));단말.Skrift(bretti.Net_staða(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (bretti.Net_staða(2,0)!=0) {단말.Skrift("0.0.0.0 0.0.0.0 ");skrifa_slóð(bretti.Net_staða(2,0));단말.Skrift(bretti.Net_staða(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void sýna_Net() {
        단말.Skrift("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_tegund=bretti.Net_staða(10,INDEX);if(TYPE_tegund==0)continue;
            단말.Skrift(TYPE_tegund==1?"TCP ":"UDP ");skrifa_slóð(bretti.Net_staða(16,INDEX));단말.문자(':');단말.númer(bretti.Net_staða(11,INDEX));단말.문자(' ');
            skrifa_slóð(bretti.Net_staða(12,INDEX));단말.문자(':');단말.númer(bretti.Net_staða(13,INDEX));단말.문자(' ');
            int staða_VALUE_e10195a1=bretti.Net_staða(14,INDEX);단말.Skrift(TYPE_tegund==2?"DATAGRAM":staða_VALUE_e10195a1==1?"LISTEN":staða_VALUE_e10195a1==2?"ESTABLISHED":staða_VALUE_e10195a1==3?"CLOSE_WAIT":staða_VALUE_e10195a1==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.númer(bretti.Net_staða(15,INDEX));단말.문자(10);
        }
        단말.Skrift("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean Bíddu_staða(int 밀리초) {
        int Keyra_2=bretti.밀리초();
        while(bretti.밀리초()-Keyra_2<밀리초) {
            if(셸입출력.upplýsingatækni_gagnvirkur()!=0){int stafur_VALUE=bretti.직렬읽기();if(stafur_VALUE==3 || stafur_VALUE=='q' || stafur_VALUE=='Q' || stafur_VALUE==27 || stafur_VALUE==-4096)return false;}
            bretti.YIELD_örgjörvi();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, markmið=-1;
        for(int staða_INDEX=1;staða_INDEX<vara_COUNT();staða_INDEX++) {
            if(같음(staða_INDEX,"-c")){횟수=tölustafur_VALUE(++staða_INDEX,100);if(횟수<1){bilun_VALUE("ping: -c 1..100");return;}}
            else if(같음(staða_INDEX,"-W")){제한=tölustafur_VALUE(++staða_INDEX,10);if(제한<1){bilun_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(markmið<0)markmið=staða_INDEX;else{bilun_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(markmið<0 || !주소읽기(markmið)){bilun_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int slóð=slóð_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Skrift("PING ");skrifa_slóð(slóð);단말.Skrift(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int röð_VALUE=1;röð_VALUE<=횟수 && 계속;röð_VALUE++) {
            int 처리값=bretti.응답보내기(slóð,röð_VALUE);
            if(처리값<0){Villa(처리값);break;}보낸수++;
            int Keyra_2=bretti.밀리초();
            while(bretti.응답읽기(0)==-11 && bretti.밀리초()-Keyra_2<제한)if(!Bíddu_staða(1)){계속=false;break;}
            if(!계속)break;
            if(bretti.응답읽기(0)==0){
                int TIME_VALUE=bretti.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Skrift("32 bytes from ");skrifa_slóð(slóð);단말.Skrift(" seq=");단말.númer(röð_VALUE);단말.Skrift(" ttl=");단말.númer(bretti.응답읽기(2));단말.Skrift(" time=");단말.númer(TIME_VALUE);단말.Skrift(" ms\n");
            }else{단말.Skrift("Request timeout seq=");단말.númer(röð_VALUE);단말.문자(10);}
            if(röð_VALUE<횟수)계속=Bíddu_staða(200);
        }
        단말.númer(보낸수);단말.Skrift(" transmitted, ");단말.númer(RECEIVED_COUNT);단말.Skrift(" received, ");단말.númer(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Skrift("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Skrift("rtt min/avg/max = ");단말.númer(최솟값);단말.문자('/');단말.númer(누적/RECEIVED_COUNT);단말.문자('/');단말.númer(최댓값);단말.Skrift(" ms\n");}
        명령해석기.NIÐURSTAÐA=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void sýna_Virkni() { 단말.Skrift("up ");단말.númer(bretti.밀리초()/1000);단말.Skrift(" seconds\n"); }
    static void sýna_Minni() {
        númer_færsla("ARM RAM KiB (firmware): ",bretti.fyrirspurn_kerfi(0,0));
        númer_færsla("Kernel image+BSS+stack KiB: ",bretti.fyrirspurn_kerfi(1,0));
        int samtala_afkastageta=bretti.fyrirspurn_kerfi(2,0), 사용량=bretti.fyrirspurn_kerfi(3,0);
        단말.Skrift("AOT heap KiB total/used/free: ");단말.númer(samtala_afkastageta);단말.문자('/');단말.númer(사용량);단말.문자('/');단말.númer(samtala_afkastageta-사용량);단말.문자(10);
        númer_færsla("Framebuffer KiB: ",bretti.fyrirspurn_kerfi(4,0));
        númer_færsla("EL0 arena+session reserve KiB: ",bretti.fyrirspurn_kerfi(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=bretti.fyrirspurn_kerfi(22,INDEX);
        númer_færsla("EL0 mapped KiB: ",매핑);
        단말.Skrift("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void sýna_Tasks() {
        단말.Skrift("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Skrift("1 - RUN - - ");단말.númer(bretti.밀리초());단말.Skrift(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(bretti.verk_staða(INDEX)>0){단말.númer(INDEX+1);단말.Skrift(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int staða_VALUE_e10195a1=bretti.fyrirspurn_kerfi(20,INDEX);if(staða_VALUE_e10195a1==0)continue;
            단말.númer(bretti.fyrirspurn_kerfi(21,INDEX));단말.문자(' ');단말.númer(INDEX);단말.Skrift(staða_VALUE_e10195a1==1?" RUN ":" SUSPENDED ");
            단말.númer(bretti.fyrirspurn_kerfi(22,INDEX));단말.문자(' ');단말.númer(bretti.fyrirspurn_kerfi(24,INDEX));단말.문자(' ');단말.númer(bretti.fyrirspurn_kerfi(23,INDEX));단말.문자(' ');
            for(int staða_INDEX=0;staða_INDEX<288;staða_INDEX++){int bæti_VALUE=bretti.fyrirspurn_kerfi(25,INDEX+staða_INDEX*4);if(bæti_VALUE==0)break;bretti.직렬쓰기(bæti_VALUE);}단말.문자(10);
        }
    }
    static void sýna_geymsla() {
        int rauf_COUNT=0, gögn_COUNT=0;
        for(int INDEX=0;INDEX<Minni_Skrár.skrá_COUNT;INDEX++)if(Minni_Skrár.이름길이[INDEX]>0 || Minni_Skrár.tilvísun_COUNT[INDEX]>0){rauf_COUNT++;gögn_COUNT+=Minni_Skrár.lengd_VALUE[INDEX];}
        단말.Skrift("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.númer(Minni_Skrár.skrá_COUNT*16384);단말.문자(' ');단말.númer(rauf_COUNT*16384);단말.문자(' ');단말.númer((Minni_Skrár.skrá_COUNT-rauf_COUNT)*16384);단말.문자(' ');단말.númer(gögn_COUNT);단말.문자(' ');단말.númer(rauf_COUNT);단말.문자('/');단말.númer(Minni_Skrár.skrá_COUNT);단말.Skrift(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void sýna_staða_bf9821b5() {
        int 횟수=셸입출력.upplýsingatækni_gagnvirkur()!=0?0:1;
        if(vara_COUNT()>1){if(vara_COUNT()!=3 || !같음(1,"-n") || (횟수=tölustafur_VALUE(2,1000))<1){bilun_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 hætta_forrit");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.upplýsingatækni_gagnvirkur()!=0 && 횟수==0)단말.Skrift("\u001b[2J\u001b[H");
            sýna_Virkni();sýna_Minni();sýna_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!Bíddu_staða(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void sýna_hjálp() {
        단말.Skrift("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Skrift(표준말(INDEX));단말.Skrift(" / ");단말.Skrift(관리명령.Word_SMS(INDEX));단말.Skrift(" : ");단말.Skrift(관리명령.설명(INDEX));단말.문자(10);}
        단말.Skrift("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Skrift("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Skrift("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean keyra_skipun() {
        int Skipun=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Skipun=INDEX;
        if(같음(0,"ifconfig"))Skipun=0;if(같음(0,"ss"))Skipun=4;
        if(Skipun<0)return false;
        if(Skipun==11){if(같음(1,"net") || 같음(1,"system"))sýna_hjálp();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.sýna_hjálp();return true;}
        if(Skipun==0 || Skipun==1)Net_skipun(Skipun==1);
        else if(Skipun==2)응답시험();
        else if(Skipun==6)sýna_staða_bf9821b5();
        else if(vara_COUNT()!=1){bilun_VALUE("This command takes no arguments; help system");}
        else if(Skipun==3)sýna_slóð();else if(Skipun==4)sýna_Net();else if(Skipun==5)sýna_Tasks();else if(Skipun==7)sýna_Minni();else if(Skipun==8)sýna_geymsla();else if(Skipun==9)sýna_Virkni();
        else if(Skipun==10)bretti.전원끄기();
        return true;
    }
}
