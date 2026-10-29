// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktuell_Daten Kernel_VALUE 상태를 읽는 IPv4·ICMP·작업·Späicher_VALUE·RAM 저장소 관리 Befeel. */
public final class System_Tool {
    static int Adress_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int Element_COUNT() { return 명령해석기.Token_COUNT; }
    static void Feeler_VALUE(String LIESMECH_eb81d7d9) { 명령해석기.Mooss=2; 단말.schreiwen(LIESMECH_eb81d7d9); 단말.문자(10); }
    static void Feeler(int VALUE) { 명령해석기.Feeler(VALUE); }
    static void 수항목(String Numm, int VALUE) { 단말.schreiwen(Numm); 단말.수(VALUE); 단말.문자(10); }
    static int Ziffer_VALUE(int INDEX, int 한도) {
        if (INDEX>=Element_COUNT() || 명령해석기.Längt_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.Längt_VALUE[INDEX]; 순번++) {
            int Zeechen_VALUE=명령해석기.Token_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (Zeechen_VALUE<0 || Zeechen_VALUE>9 || VALUE>(한도-Zeechen_VALUE)/10) return -1;
            VALUE=VALUE*10+Zeechen_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=Element_COUNT()) return false;
        int VALUE=0, 덩이=0, Ziffer_COUNT=0, Punkt_COUNT=0;
        for (int 순번=0; 순번<명령해석기.Längt_VALUE[INDEX]; 순번++) {
            int Zeechen_VALUE=명령해석기.Token_VALUE[명령해석기.시작점[INDEX]+순번];
            if (Zeechen_VALUE=='.') { if (Ziffer_COUNT==0 || ++Punkt_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=Ziffer_COUNT=0; }
            else { if (Zeechen_VALUE<'0' || Zeechen_VALUE>'9' || ++Ziffer_COUNT>3) return false; 덩이=덩이*10+Zeechen_VALUE-'0'; if(덩이>255)return false; }
        }
        if (Punkt_COUNT!=3 || Ziffer_COUNT==0) return false;
        Adress_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void schreiwen_Adress(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void Show_Reseau_Status() {
        단말.schreiwen(Board.Reseau_Status(20,0)!=0?"en0: ":"sl0: "); 단말.schreiwen(Board.Reseau_Status(3,0)!=0?"UP":"DOWN");
        단말.schreiwen(Board.Reseau_Status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.schreiwen(Board.Reseau_Status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); schreiwen_Adress(Board.Reseau_Status(0,0));
        단말.schreiwen(" netmask "); schreiwen_Adress(Board.Reseau_Status(1,0)); 단말.schreiwen(" gateway "); schreiwen_Adress(Board.Reseau_Status(2,0)); 단말.문자(10);
        단말.schreiwen("  RX packets "); 단말.수(Board.Reseau_Status(4,0)); 단말.schreiwen(" bytes "); 단말.수(Board.Reseau_Status(6,0));
        단말.schreiwen(" TX packets "); 단말.수(Board.Reseau_Status(5,0)); 단말.schreiwen(" bytes "); 단말.수(Board.Reseau_Status(7,0)); 단말.문자(10);
        수항목("  dropped ",Board.Reseau_Status(8,0));
    }
    static void Saz_Adress(int Laf) {
        if (Element_COUNT()!=Laf+3 || !주소읽기(Laf)) { Feeler_VALUE("사용법: ipconfig set Adress 주소가림 Gateway_VALUE"); return; }
        int Adress=Adress_VALUE;
        if(!주소읽기(Laf+1)){Feeler_VALUE("Invalid IPv4 netmask");return;} int Mask_VALUE=Adress_VALUE;
        if(!주소읽기(Laf+2)){Feeler_VALUE("Invalid IPv4 gateway");return;}
        int Mooss=Board.Reseau_Astellungen(0,Adress,Mask_VALUE,Adress_VALUE);
        if(Mooss<0) { Feeler(Mooss); if(Mooss==-16)단말.schreiwen("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.schreiwen("IPv4 configuration applied (until reboot)\n"); Show_Reseau_Status(); }
    }
    static void Reseau_Befeel(boolean IP_Adress) {
        if (Element_COUNT()==1 || Element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || Element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { Show_Reseau_Status();return; }
        if (IP_Adress && 같음(1,"route") && (Element_COUNT()==2 || Element_COUNT()==3&&같음(2,"show"))) { Show_Wee();return; }
        if (같음(1,"set")) { Saz_Adress(2);return; }
        if (Element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Board.Reseau_Astellungen(같음(1,"up")?1:2,0,0,0);Show_Reseau_Status();return; }
        if (IP_Adress && Element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Board.Reseau_Astellungen(같음(5,"up")?1:2,0,0,0);Show_Reseau_Status();return; }
        Feeler_VALUE("사용법: ip [addr show|route show|set Adress 주소가림 Gateway_VALUE|link set dev sl0 up|down]");
    }
    static void Show_Wee() {
        단말.schreiwen("Destination Netmask Gateway Interface\n");
        schreiwen_Adress(Board.Reseau_Status(0,0)&Board.Reseau_Status(1,0));단말.문자(' ');schreiwen_Adress(Board.Reseau_Status(1,0));단말.schreiwen(Board.Reseau_Status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Board.Reseau_Status(2,0)!=0) {단말.schreiwen("0.0.0.0 0.0.0.0 ");schreiwen_Adress(Board.Reseau_Status(2,0));단말.schreiwen(Board.Reseau_Status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void Show_Reseau() {
        단말.schreiwen("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_Kategorie=Board.Reseau_Status(10,INDEX);if(TYPE_Kategorie==0)continue;
            단말.schreiwen(TYPE_Kategorie==1?"TCP ":"UDP ");schreiwen_Adress(Board.Reseau_Status(16,INDEX));단말.문자(':');단말.수(Board.Reseau_Status(11,INDEX));단말.문자(' ');
            schreiwen_Adress(Board.Reseau_Status(12,INDEX));단말.문자(':');단말.수(Board.Reseau_Status(13,INDEX));단말.문자(' ');
            int Status_VALUE=Board.Reseau_Status(14,INDEX);단말.schreiwen(TYPE_Kategorie==2?"DATAGRAM":Status_VALUE==1?"LISTEN":Status_VALUE==2?"ESTABLISHED":Status_VALUE==3?"CLOSE_WAIT":Status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Board.Reseau_Status(15,INDEX));단말.문자(10);
        }
        단말.schreiwen("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean Waart_Status(int 밀리초) {
        int Laf=Board.밀리초();
        while(Board.밀리초()-Laf<밀리초) {
            if(셸입출력.대화가능()!=0){int Zeechen_VALUE=Board.직렬읽기();if(Zeechen_VALUE==3 || Zeechen_VALUE=='q' || Zeechen_VALUE=='Q' || Zeechen_VALUE==27 || Zeechen_VALUE==-4096)return false;}
            Board.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, Zil=-1;
        for(int positionéieren_INDEX=1;positionéieren_INDEX<Element_COUNT();positionéieren_INDEX++) {
            if(같음(positionéieren_INDEX,"-c")){횟수=Ziffer_VALUE(++positionéieren_INDEX,100);if(횟수<1){Feeler_VALUE("ping: -c 1..100");return;}}
            else if(같음(positionéieren_INDEX,"-W")){제한=Ziffer_VALUE(++positionéieren_INDEX,10);if(제한<1){Feeler_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(Zil<0)Zil=positionéieren_INDEX;else{Feeler_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(Zil<0 || !주소읽기(Zil)){Feeler_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int Adress=Adress_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.schreiwen("PING ");schreiwen_Adress(Adress);단말.schreiwen(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int Reiefolleg_VALUE=1;Reiefolleg_VALUE<=횟수 && 계속;Reiefolleg_VALUE++) {
            int 처리값=Board.응답보내기(Adress,Reiefolleg_VALUE);
            if(처리값<0){Feeler(처리값);break;}보낸수++;
            int Laf=Board.밀리초();
            while(Board.응답읽기(0)==-11 && Board.밀리초()-Laf<제한)if(!Waart_Status(1)){계속=false;break;}
            if(!계속)break;
            if(Board.응답읽기(0)==0){
                int TIME_VALUE=Board.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.schreiwen("32 bytes from ");schreiwen_Adress(Adress);단말.schreiwen(" seq=");단말.수(Reiefolleg_VALUE);단말.schreiwen(" ttl=");단말.수(Board.응답읽기(2));단말.schreiwen(" time=");단말.수(TIME_VALUE);단말.schreiwen(" ms\n");
            }else{단말.schreiwen("Request timeout seq=");단말.수(Reiefolleg_VALUE);단말.문자(10);}
            if(Reiefolleg_VALUE<횟수)계속=Waart_Status(200);
        }
        단말.수(보낸수);단말.schreiwen(" transmitted, ");단말.수(RECEIVED_COUNT);단말.schreiwen(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.schreiwen("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.schreiwen("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.schreiwen(" ms\n");}
        명령해석기.Mooss=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void Show_Aktivitéit() { 단말.schreiwen("up ");단말.수(Board.밀리초()/1000);단말.schreiwen(" seconds\n"); }
    static void Show_Späicher() {
        수항목("ARM RAM KiB (firmware): ",Board.Requête_System(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Board.Requête_System(1,0));
        int 총량=Board.Requête_System(2,0), 사용량=Board.Requête_System(3,0);
        단말.schreiwen("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Board.Requête_System(4,0));
        수항목("EL0 arena+session reserve KiB: ",Board.Requête_System(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Board.Requête_System(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.schreiwen("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void Show_Tasks() {
        단말.schreiwen("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.schreiwen("1 - RUN - - ");단말.수(Board.밀리초());단말.schreiwen(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Board.To_do_Status(INDEX)>0){단말.수(INDEX+1);단말.schreiwen(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Status_VALUE=Board.Requête_System(20,INDEX);if(Status_VALUE==0)continue;
            단말.수(Board.Requête_System(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.schreiwen(Status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Board.Requête_System(22,INDEX));단말.문자(' ');단말.수(Board.Requête_System(24,INDEX));단말.문자(' ');단말.수(Board.Requête_System(23,INDEX));단말.문자(' ');
            for(int positionéieren_INDEX=0;positionéieren_INDEX<288;positionéieren_INDEX++){int Byte_VALUE=Board.Requête_System(25,INDEX+positionéieren_INDEX*4);if(Byte_VALUE==0)break;Board.직렬쓰기(Byte_VALUE);}단말.문자(10);
        }
    }
    static void Show_Späicher_deafe149() {
        int Slot_COUNT=0, Daten_COUNT=0;
        for(int INDEX=0;INDEX<Späicher_Fichieren.Fichier_COUNT;INDEX++)if(Späicher_Fichieren.이름길이[INDEX]>0 || Späicher_Fichieren.Referenzen_COUNT[INDEX]>0){Slot_COUNT++;Daten_COUNT+=Späicher_Fichieren.Längt_VALUE[INDEX];}
        단말.schreiwen("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Späicher_Fichieren.Fichier_COUNT*16384);단말.문자(' ');단말.수(Slot_COUNT*16384);단말.문자(' ');단말.수((Späicher_Fichieren.Fichier_COUNT-Slot_COUNT)*16384);단말.문자(' ');단말.수(Daten_COUNT);단말.문자(' ');단말.수(Slot_COUNT);단말.문자('/');단말.수(Späicher_Fichieren.Fichier_COUNT);단말.schreiwen(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void Show_Status_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(Element_COUNT()>1){if(Element_COUNT()!=3 || !같음(1,"-n") || (횟수=Ziffer_VALUE(2,1000))<1){Feeler_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 verloossen_App");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.schreiwen("\u001b[2J\u001b[H");
            Show_Aktivitéit();Show_Späicher();Show_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!Waart_Status(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void Show_Hëllef() {
        단말.schreiwen("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.schreiwen(표준말(INDEX));단말.schreiwen(" / ");단말.schreiwen(관리명령.Word_SMS(INDEX));단말.schreiwen(" : ");단말.schreiwen(관리명령.설명(INDEX));단말.문자(10);}
        단말.schreiwen("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.schreiwen("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.schreiwen("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean ausféieren_Befeel() {
        int Befeel=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Befeel=INDEX;
        if(같음(0,"ifconfig"))Befeel=0;if(같음(0,"ss"))Befeel=4;
        if(Befeel<0)return false;
        if(Befeel==11){if(같음(1,"net") || 같음(1,"system"))Show_Hëllef();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.Show_Hëllef();return true;}
        if(Befeel==0 || Befeel==1)Reseau_Befeel(Befeel==1);
        else if(Befeel==2)응답시험();
        else if(Befeel==6)Show_Status_bf9821b5();
        else if(Element_COUNT()!=1){Feeler_VALUE("This command takes no arguments; help system");}
        else if(Befeel==3)Show_Wee();else if(Befeel==4)Show_Reseau();else if(Befeel==5)Show_Tasks();else if(Befeel==7)Show_Späicher();else if(Befeel==8)Show_Späicher_deafe149();else if(Befeel==9)Show_Aktivitéit();
        else if(Befeel==10)Board.전원끄기();
        return true;
    }
}
