// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** tegelik_andmed tuum_VALUE 상태를 읽는 IPv4·ICMP·작업·Mälu_VALUE·RAM hoidla_juur 관리 Käsk. */
public final class süsteem_tööriist {
    static int ADDRESS_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int kaup_COUNT() { return 명령해석기.luba_COUNT; }
    static void tõrge_VALUE(String 안내) { 명령해석기.TULEMUS=2; 단말.Kirjutamine(안내); 단말.문자(10); }
    static void VIGA(int VALUE) { 명령해석기.VIGA(VALUE); }
    static void number_kirje(String Nimi_2, int VALUE) { 단말.Kirjutamine(Nimi_2); 단말.number(VALUE); 단말.문자(10); }
    static int number_VALUE(int INDEX, int 한도) {
        if (INDEX>=kaup_COUNT() || 명령해석기.길이[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int märk_VALUE=명령해석기.luba_VALUE_eb540501[명령해석기.시작점[INDEX]+순번]-'0';
            if (märk_VALUE<0 || märk_VALUE>9 || VALUE>(한도-märk_VALUE)/10) return -1;
            VALUE=VALUE*10+märk_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=kaup_COUNT()) return false;
        int VALUE=0, kogum_VALUE=0, number_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.길이[INDEX]; 순번++) {
            int märk_VALUE=명령해석기.luba_VALUE_eb540501[명령해석기.시작점[INDEX]+순번];
            if (märk_VALUE=='.') { if (number_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|kogum_VALUE; kogum_VALUE=number_COUNT=0; }
            else { if (märk_VALUE<'0' || märk_VALUE>'9' || ++number_COUNT>3) return false; kogum_VALUE=kogum_VALUE*10+märk_VALUE-'0'; if(kogum_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || number_COUNT==0) return false;
        ADDRESS_VALUE=(VALUE<<8)|kogum_VALUE; return true;
    }
    static void kirjutamine_ADDRESS(int VALUE) {
        단말.number((VALUE>>>24)&255); 단말.문자('.'); 단말.number((VALUE>>>16)&255); 단말.문자('.');
        단말.number((VALUE>>>8)&255); 단말.문자('.'); 단말.number(VALUE&255);
    }
    static void saade_võrk_olek() {
        단말.Kirjutamine(Tahvel.võrk_olek(20,0)!=0?"en0: ":"sl0: "); 단말.Kirjutamine(Tahvel.võrk_olek(3,0)!=0?"UP":"DOWN");
        단말.Kirjutamine(Tahvel.võrk_olek(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Kirjutamine(Tahvel.võrk_olek(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); kirjutamine_ADDRESS(Tahvel.võrk_olek(0,0));
        단말.Kirjutamine(" netmask "); kirjutamine_ADDRESS(Tahvel.võrk_olek(1,0)); 단말.Kirjutamine(" gateway "); kirjutamine_ADDRESS(Tahvel.võrk_olek(2,0)); 단말.문자(10);
        단말.Kirjutamine("  RX packets "); 단말.number(Tahvel.võrk_olek(4,0)); 단말.Kirjutamine(" bytes "); 단말.number(Tahvel.võrk_olek(6,0));
        단말.Kirjutamine(" TX packets "); 단말.number(Tahvel.võrk_olek(5,0)); 단말.Kirjutamine(" bytes "); 단말.number(Tahvel.võrk_olek(7,0)); 단말.문자(10);
        number_kirje("  dropped ",Tahvel.võrk_olek(8,0));
    }
    static void hulk_ADDRESS(int Käivita_2) {
        if (kaup_COUNT()!=Käivita_2+3 || !주소읽기(Käivita_2)) { tõrge_VALUE("사용법: ipconfig set ADDRESS 주소가림 lüüs_VALUE"); return; }
        int ADDRESS=ADDRESS_VALUE;
        if(!주소읽기(Käivita_2+1)){tõrge_VALUE("Invalid IPv4 netmask");return;} int mask_VALUE=ADDRESS_VALUE;
        if(!주소읽기(Käivita_2+2)){tõrge_VALUE("Invalid IPv4 gateway");return;}
        int TULEMUS=Tahvel.võrk_Sätted(0,ADDRESS,mask_VALUE,ADDRESS_VALUE);
        if(TULEMUS<0) { VIGA(TULEMUS); if(TULEMUS==-16)단말.Kirjutamine("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Kirjutamine("IPv4 configuration applied (until reboot)\n"); saade_võrk_olek(); }
    }
    static void võrk_käsk(boolean IP_aadress) {
        if (kaup_COUNT()==1 || kaup_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || kaup_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { saade_võrk_olek();return; }
        if (IP_aadress && 같음(1,"route") && (kaup_COUNT()==2 || kaup_COUNT()==3&&같음(2,"show"))) { saade_tee();return; }
        if (같음(1,"set")) { hulk_ADDRESS(2);return; }
        if (kaup_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Tahvel.võrk_Sätted(같음(1,"up")?1:2,0,0,0);saade_võrk_olek();return; }
        if (IP_aadress && kaup_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Tahvel.võrk_Sätted(같음(5,"up")?1:2,0,0,0);saade_võrk_olek();return; }
        tõrge_VALUE("사용법: ip [addr show|route show|set ADDRESS 주소가림 lüüs_VALUE|link set dev sl0 up|down]");
    }
    static void saade_tee() {
        단말.Kirjutamine("Destination Netmask Gateway Interface\n");
        kirjutamine_ADDRESS(Tahvel.võrk_olek(0,0)&Tahvel.võrk_olek(1,0));단말.문자(' ');kirjutamine_ADDRESS(Tahvel.võrk_olek(1,0));단말.Kirjutamine(Tahvel.võrk_olek(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Tahvel.võrk_olek(2,0)!=0) {단말.Kirjutamine("0.0.0.0 0.0.0.0 ");kirjutamine_ADDRESS(Tahvel.võrk_olek(2,0));단말.Kirjutamine(Tahvel.võrk_olek(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void saade_võrk() {
        단말.Kirjutamine("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_ala=Tahvel.võrk_olek(10,INDEX);if(TYPE_ala==0)continue;
            단말.Kirjutamine(TYPE_ala==1?"TCP ":"UDP ");kirjutamine_ADDRESS(Tahvel.võrk_olek(16,INDEX));단말.문자(':');단말.number(Tahvel.võrk_olek(11,INDEX));단말.문자(' ');
            kirjutamine_ADDRESS(Tahvel.võrk_olek(12,INDEX));단말.문자(':');단말.number(Tahvel.võrk_olek(13,INDEX));단말.문자(' ');
            int Olek_VALUE=Tahvel.võrk_olek(14,INDEX);단말.Kirjutamine(TYPE_ala==2?"DATAGRAM":Olek_VALUE==1?"LISTEN":Olek_VALUE==2?"ESTABLISHED":Olek_VALUE==3?"CLOSE_WAIT":Olek_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.number(Tahvel.võrk_olek(15,INDEX));단말.문자(10);
        }
        단말.Kirjutamine("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean ooteolek(int 밀리초) {
        int Käivita_2=Tahvel.밀리초();
        while(Tahvel.밀리초()-Käivita_2<밀리초) {
            if(셸입출력.대화가능()!=0){int märk_VALUE=Tahvel.직렬읽기();if(märk_VALUE==3 || märk_VALUE=='q' || märk_VALUE=='Q' || märk_VALUE==27 || märk_VALUE==-4096)return false;}
            Tahvel.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, siht=-1;
        for(int asukohaindeks=1;asukohaindeks<kaup_COUNT();asukohaindeks++) {
            if(같음(asukohaindeks,"-c")){횟수=number_VALUE(++asukohaindeks,100);if(횟수<1){tõrge_VALUE("ping: -c 1..100");return;}}
            else if(같음(asukohaindeks,"-W")){제한=number_VALUE(++asukohaindeks,10);if(제한<1){tõrge_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(siht<0)siht=asukohaindeks;else{tõrge_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(siht<0 || !주소읽기(siht)){tõrge_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADDRESS=ADDRESS_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Kirjutamine("PING ");kirjutamine_ADDRESS(ADDRESS);단말.Kirjutamine(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tellimus_VALUE=1;tellimus_VALUE<=횟수 && 계속;tellimus_VALUE++) {
            int 처리값=Tahvel.saatma_vastus(ADDRESS,tellimus_VALUE);
            if(처리값<0){VIGA(처리값);break;}보낸수++;
            int Käivita_2=Tahvel.밀리초();
            while(Tahvel.응답읽기(0)==-11 && Tahvel.밀리초()-Käivita_2<제한)if(!ooteolek(1)){계속=false;break;}
            if(!계속)break;
            if(Tahvel.응답읽기(0)==0){
                int Aeg_VALUE=Tahvel.응답읽기(1);RECEIVED_COUNT++;누적+=Aeg_VALUE;if(Aeg_VALUE<최솟값)최솟값=Aeg_VALUE;if(Aeg_VALUE>최댓값)최댓값=Aeg_VALUE;
                단말.Kirjutamine("32 bytes from ");kirjutamine_ADDRESS(ADDRESS);단말.Kirjutamine(" seq=");단말.number(tellimus_VALUE);단말.Kirjutamine(" ttl=");단말.number(Tahvel.응답읽기(2));단말.Kirjutamine(" time=");단말.number(Aeg_VALUE);단말.Kirjutamine(" ms\n");
            }else{단말.Kirjutamine("Request timeout seq=");단말.number(tellimus_VALUE);단말.문자(10);}
            if(tellimus_VALUE<횟수)계속=ooteolek(200);
        }
        단말.number(보낸수);단말.Kirjutamine(" transmitted, ");단말.number(RECEIVED_COUNT);단말.Kirjutamine(" received, ");단말.number(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Kirjutamine("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Kirjutamine("rtt min/avg/max = ");단말.number(최솟값);단말.문자('/');단말.number(누적/RECEIVED_COUNT);단말.문자('/');단말.number(최댓값);단말.Kirjutamine(" ms\n");}
        명령해석기.TULEMUS=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void saade_Tegevus() { 단말.Kirjutamine("up ");단말.number(Tahvel.밀리초()/1000);단말.Kirjutamine(" seconds\n"); }
    static void saade_Mälu() {
        number_kirje("ARM RAM KiB (firmware): ",Tahvel.päring_süsteem(0,0));
        number_kirje("Kernel image+BSS+stack KiB: ",Tahvel.päring_süsteem(1,0));
        int kokku_võimsus=Tahvel.päring_süsteem(2,0), 사용량=Tahvel.päring_süsteem(3,0);
        단말.Kirjutamine("AOT heap KiB total/used/free: ");단말.number(kokku_võimsus);단말.문자('/');단말.number(사용량);단말.문자('/');단말.number(kokku_võimsus-사용량);단말.문자(10);
        number_kirje("Framebuffer KiB: ",Tahvel.päring_süsteem(4,0));
        number_kirje("EL0 arena+session reserve KiB: ",Tahvel.päring_süsteem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Tahvel.päring_süsteem(22,INDEX);
        number_kirje("EL0 mapped KiB: ",매핑);
        단말.Kirjutamine("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void saade_Tasks() {
        단말.Kirjutamine("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Kirjutamine("1 - RUN - - ");단말.number(Tahvel.밀리초());단말.Kirjutamine(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Tahvel.tööüksus_Olek(INDEX)>0){단말.number(INDEX+1);단말.Kirjutamine(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Olek_VALUE=Tahvel.päring_süsteem(20,INDEX);if(Olek_VALUE==0)continue;
            단말.number(Tahvel.päring_süsteem(21,INDEX));단말.문자(' ');단말.number(INDEX);단말.Kirjutamine(Olek_VALUE==1?" RUN ":" SUSPENDED ");
            단말.number(Tahvel.päring_süsteem(22,INDEX));단말.문자(' ');단말.number(Tahvel.päring_süsteem(24,INDEX));단말.문자(' ');단말.number(Tahvel.päring_süsteem(23,INDEX));단말.문자(' ');
            for(int asukohaindeks=0;asukohaindeks<288;asukohaindeks++){int bait_VALUE=Tahvel.päring_süsteem(25,INDEX+asukohaindeks*4);if(bait_VALUE==0)break;Tahvel.직렬쓰기(bait_VALUE);}단말.문자(10);
        }
    }
    static void saade_salvesti() {
        int 칸수=0, andmed_COUNT=0;
        for(int INDEX=0;INDEX<Mälu_Failid.Fail_COUNT;INDEX++)if(Mälu_Failid.이름길이[INDEX]>0 || Mälu_Failid.viide_COUNT[INDEX]>0){칸수++;andmed_COUNT+=Mälu_Failid.길이[INDEX];}
        단말.Kirjutamine("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.number(Mälu_Failid.Fail_COUNT*16384);단말.문자(' ');단말.number(칸수*16384);단말.문자(' ');단말.number((Mälu_Failid.Fail_COUNT-칸수)*16384);단말.문자(' ');단말.number(andmed_COUNT);단말.문자(' ');단말.number(칸수);단말.문자('/');단말.number(Mälu_Failid.Fail_COUNT);단말.Kirjutamine(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void saade_olek() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(kaup_COUNT()>1){if(kaup_COUNT()!=3 || !같음(1,"-n") || (횟수=number_VALUE(2,1000))<1){tõrge_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 välju_programm");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Kirjutamine("\u001b[2J\u001b[H");
            saade_Tegevus();saade_Mälu();saade_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!ooteolek(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void saade_spikker() {
        단말.Kirjutamine("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Kirjutamine(표준말(INDEX));단말.Kirjutamine(" / ");단말.Kirjutamine(관리명령.Word_SMS(INDEX));단말.Kirjutamine(" : ");단말.Kirjutamine(관리명령.설명(INDEX));단말.문자(10);}
        단말.Kirjutamine("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Kirjutamine("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Kirjutamine("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Täida_käsk() {
        int Käsk=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Käsk=INDEX;
        if(같음(0,"ifconfig"))Käsk=0;if(같음(0,"ss"))Käsk=4;
        if(Käsk<0)return false;
        if(Käsk==11){if(같음(1,"net") || 같음(1,"system"))saade_spikker();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.saade_spikker();return true;}
        if(Käsk==0 || Käsk==1)võrk_käsk(Käsk==1);
        else if(Käsk==2)응답시험();
        else if(Käsk==6)saade_olek();
        else if(kaup_COUNT()!=1){tõrge_VALUE("This command takes no arguments; help system");}
        else if(Käsk==3)saade_tee();else if(Käsk==4)saade_võrk();else if(Käsk==5)saade_Tasks();else if(Käsk==7)saade_Mälu();else if(Käsk==8)saade_salvesti();else if(Käsk==9)saade_Tegevus();
        else if(Käsk==10)Tahvel.전원끄기();
        return true;
    }
}
