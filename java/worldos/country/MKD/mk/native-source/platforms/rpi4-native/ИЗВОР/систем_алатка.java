// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** реален_податоци јадро_VALUE 상태를 읽는 IPv4·ICMP·작업·Меморија_VALUE·RAM склад_корен 관리 Команда. */
public final class систем_алатка {
    static int адреса_VALUE;
    static boolean 같음(int INDEX, String Word_СМС) { return 명령해석기.같음(INDEX, Word_СМС); }
    static int ставка_COUNT() { return 명령해석기.токен_COUNT; }
    static void неуспех_VALUE(String информации_пред_употреба_eb81d7d9) { 명령해석기.мерка=2; 단말.Запиши(информации_пред_употреба_eb81d7d9); 단말.문자(10); }
    static void ГРЕШКА(int VALUE) { 명령해석기.ГРЕШКА(VALUE); }
    static void 수항목(String Име, int VALUE) { 단말.Запиши(Име); 단말.수(VALUE); 단말.문자(10); }
    static int цифра_VALUE(int INDEX, int 한도) {
        if (INDEX>=ставка_COUNT() || 명령해석기.должина_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.должина_VALUE[INDEX]; 순번++) {
            int знак_VALUE=명령해석기.токен_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (знак_VALUE<0 || знак_VALUE>9 || VALUE>(한도-знак_VALUE)/10) return -1;
            VALUE=VALUE*10+знак_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=ставка_COUNT()) return false;
        int VALUE=0, 덩이=0, цифра_COUNT=0, поен_COUNT=0;
        for (int 순번=0; 순번<명령해석기.должина_VALUE[INDEX]; 순번++) {
            int знак_VALUE=명령해석기.токен_VALUE[명령해석기.시작점[INDEX]+순번];
            if (знак_VALUE=='.') { if (цифра_COUNT==0 || ++поен_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=цифра_COUNT=0; }
            else { if (знак_VALUE<'0' || знак_VALUE>'9' || ++цифра_COUNT>3) return false; 덩이=덩이*10+знак_VALUE-'0'; if(덩이>255)return false; }
        }
        if (поен_COUNT!=3 || цифра_COUNT==0) return false;
        адреса_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void запиши_адреса(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void прикажи_Мрежа_статус() {
        단말.Запиши(табла.Мрежа_статус(20,0)!=0?"en0: ":"sl0: "); 단말.Запиши(табла.Мрежа_статус(3,0)!=0?"UP":"DOWN");
        단말.Запиши(табла.Мрежа_статус(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Запиши(табла.Мрежа_статус(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); запиши_адреса(табла.Мрежа_статус(0,0));
        단말.Запиши(" netmask "); запиши_адреса(табла.Мрежа_статус(1,0)); 단말.Запиши(" gateway "); запиши_адреса(табла.Мрежа_статус(2,0)); 단말.문자(10);
        단말.Запиши("  RX packets "); 단말.수(табла.Мрежа_статус(4,0)); 단말.Запиши(" bytes "); 단말.수(табла.Мрежа_статус(6,0));
        단말.Запиши(" TX packets "); 단말.수(табла.Мрежа_статус(5,0)); 단말.Запиши(" bytes "); 단말.수(табла.Мрежа_статус(7,0)); 단말.문자(10);
        수항목("  dropped ",табла.Мрежа_статус(8,0));
    }
    static void збир_адреса(int Изврши_2) {
        if (ставка_COUNT()!=Изврши_2+3 || !주소읽기(Изврши_2)) { неуспех_VALUE("사용법: ipconfig set адреса 주소가림 капија_VALUE"); return; }
        int адреса=адреса_VALUE;
        if(!주소읽기(Изврши_2+1)){неуспех_VALUE("Invalid IPv4 netmask");return;} int маска_VALUE=адреса_VALUE;
        if(!주소읽기(Изврши_2+2)){неуспех_VALUE("Invalid IPv4 gateway");return;}
        int мерка=табла.Мрежа_Параметри(0,адреса,маска_VALUE,адреса_VALUE);
        if(мерка<0) { ГРЕШКА(мерка); if(мерка==-16)단말.Запиши("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Запиши("IPv4 configuration applied (until reboot)\n"); прикажи_Мрежа_статус(); }
    }
    static void Мрежа_наредба(boolean ИП_адреса) {
        if (ставка_COUNT()==1 || ставка_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || ставка_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { прикажи_Мрежа_статус();return; }
        if (ИП_адреса && 같음(1,"route") && (ставка_COUNT()==2 || ставка_COUNT()==3&&같음(2,"show"))) { прикажи_патека();return; }
        if (같음(1,"set")) { збир_адреса(2);return; }
        if (ставка_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { табла.Мрежа_Параметри(같음(1,"up")?1:2,0,0,0);прикажи_Мрежа_статус();return; }
        if (ИП_адреса && ставка_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { табла.Мрежа_Параметри(같음(5,"up")?1:2,0,0,0);прикажи_Мрежа_статус();return; }
        неуспех_VALUE("사용법: ip [addr show|route show|set адреса 주소가림 капија_VALUE|link set dev sl0 up|down]");
    }
    static void прикажи_патека() {
        단말.Запиши("Destination Netmask Gateway Interface\n");
        запиши_адреса(табла.Мрежа_статус(0,0)&табла.Мрежа_статус(1,0));단말.문자(' ');запиши_адреса(табла.Мрежа_статус(1,0));단말.Запиши(табла.Мрежа_статус(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (табла.Мрежа_статус(2,0)!=0) {단말.Запиши("0.0.0.0 0.0.0.0 ");запиши_адреса(табла.Мрежа_статус(2,0));단말.Запиши(табла.Мрежа_статус(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void прикажи_Мрежа() {
        단말.Запиши("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_област=табла.Мрежа_статус(10,INDEX);if(TYPE_област==0)continue;
            단말.Запиши(TYPE_област==1?"TCP ":"UDP ");запиши_адреса(табла.Мрежа_статус(16,INDEX));단말.문자(':');단말.수(табла.Мрежа_статус(11,INDEX));단말.문자(' ');
            запиши_адреса(табла.Мрежа_статус(12,INDEX));단말.문자(':');단말.수(табла.Мрежа_статус(13,INDEX));단말.문자(' ');
            int статус_VALUE=табла.Мрежа_статус(14,INDEX);단말.Запиши(TYPE_област==2?"DATAGRAM":статус_VALUE==1?"LISTEN":статус_VALUE==2?"ESTABLISHED":статус_VALUE==3?"CLOSE_WAIT":статус_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(табла.Мрежа_статус(15,INDEX));단말.문자(10);
        }
        단말.Запиши("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean почекај_статус(int 밀리초) {
        int Изврши_2=табла.밀리초();
        while(табла.밀리초()-Изврши_2<밀리초) {
            if(셸입출력.информатичка_технологија_интерактивен()!=0){int знак_VALUE=табла.직렬읽기();if(знак_VALUE==3 || знак_VALUE=='q' || знак_VALUE=='Q' || знак_VALUE==27 || знак_VALUE==-4096)return false;}
            табла.YIELD_ЦПУ();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, цел=-1;
        for(int позиционирање_INDEX=1;позиционирање_INDEX<ставка_COUNT();позиционирање_INDEX++) {
            if(같음(позиционирање_INDEX,"-c")){횟수=цифра_VALUE(++позиционирање_INDEX,100);if(횟수<1){неуспех_VALUE("ping: -c 1..100");return;}}
            else if(같음(позиционирање_INDEX,"-W")){제한=цифра_VALUE(++позиционирање_INDEX,10);if(제한<1){неуспех_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(цел<0)цел=позиционирање_INDEX;else{неуспех_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(цел<0 || !주소읽기(цел)){неуспех_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int адреса=адреса_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Запиши("PING ");запиши_адреса(адреса);단말.Запиши(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int редослед_VALUE=1;редослед_VALUE<=횟수 && 계속;редослед_VALUE++) {
            int 처리값=табла.응답보내기(адреса,редослед_VALUE);
            if(처리값<0){ГРЕШКА(처리값);break;}보낸수++;
            int Изврши_2=табла.밀리초();
            while(табла.응답읽기(0)==-11 && табла.밀리초()-Изврши_2<제한)if(!почекај_статус(1)){계속=false;break;}
            if(!계속)break;
            if(табла.응답읽기(0)==0){
                int TIME_VALUE=табла.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Запиши("32 bytes from ");запиши_адреса(адреса);단말.Запиши(" seq=");단말.수(редослед_VALUE);단말.Запиши(" ttl=");단말.수(табла.응답읽기(2));단말.Запиши(" time=");단말.수(TIME_VALUE);단말.Запиши(" ms\n");
            }else{단말.Запиши("Request timeout seq=");단말.수(редослед_VALUE);단말.문자(10);}
            if(редослед_VALUE<횟수)계속=почекај_статус(200);
        }
        단말.수(보낸수);단말.Запиши(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Запиши(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Запиши("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Запиши("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Запиши(" ms\n");}
        명령해석기.мерка=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void прикажи_Активност() { 단말.Запиши("up ");단말.수(табла.밀리초()/1000);단말.Запиши(" seconds\n"); }
    static void прикажи_Меморија() {
        수항목("ARM RAM KiB (firmware): ",табла.прашалник_систем(0,0));
        수항목("Kernel image+BSS+stack KiB: ",табла.прашалник_систем(1,0));
        int 총량=табла.прашалник_систем(2,0), 사용량=табла.прашалник_систем(3,0);
        단말.Запиши("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",табла.прашалник_систем(4,0));
        수항목("EL0 arena+session reserve KiB: ",табла.прашалник_систем(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=табла.прашалник_систем(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Запиши("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void прикажи_Tasks() {
        단말.Запиши("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Запиши("1 - RUN - - ");단말.수(табла.밀리초());단말.Запиши(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(табла.задача_статус(INDEX)>0){단말.수(INDEX+1);단말.Запиши(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int статус_VALUE=табла.прашалник_систем(20,INDEX);if(статус_VALUE==0)continue;
            단말.수(табла.прашалник_систем(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Запиши(статус_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(табла.прашалник_систем(22,INDEX));단말.문자(' ');단말.수(табла.прашалник_систем(24,INDEX));단말.문자(' ');단말.수(табла.прашалник_систем(23,INDEX));단말.문자(' ');
            for(int позиционирање_INDEX=0;позиционирање_INDEX<288;позиционирање_INDEX++){int бајт_VALUE=табла.прашалник_систем(25,INDEX+позиционирање_INDEX*4);if(бајт_VALUE==0)break;табла.직렬쓰기(бајт_VALUE);}단말.문자(10);
        }
    }
    static void прикажи_Склад() {
        int отвор_COUNT=0, податоци_COUNT=0;
        for(int INDEX=0;INDEX<Меморија_Датотеки.датотека_COUNT;INDEX++)if(Меморија_Датотеки.이름길이[INDEX]>0 || Меморија_Датотеки.Референци_COUNT[INDEX]>0){отвор_COUNT++;податоци_COUNT+=Меморија_Датотеки.должина_VALUE[INDEX];}
        단말.Запиши("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Меморија_Датотеки.датотека_COUNT*16384);단말.문자(' ');단말.수(отвор_COUNT*16384);단말.문자(' ');단말.수((Меморија_Датотеки.датотека_COUNT-отвор_COUNT)*16384);단말.문자(' ');단말.수(податоци_COUNT);단말.문자(' ');단말.수(отвор_COUNT);단말.문자('/');단말.수(Меморија_Датотеки.датотека_COUNT);단말.Запиши(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void прикажи_статус_bf9821b5() {
        int 횟수=셸입출력.информатичка_технологија_интерактивен()!=0?0:1;
        if(ставка_COUNT()>1){if(ставка_COUNT()!=3 || !같음(1,"-n") || (횟수=цифра_VALUE(2,1000))<1){неуспех_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 излез_програма");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.информатичка_технологија_интерактивен()!=0 && 횟수==0)단말.Запиши("\u001b[2J\u001b[H");
            прикажи_Активност();прикажи_Меморија();прикажи_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!почекај_статус(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void прикажи_помош() {
        단말.Запиши("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Запиши(표준말(INDEX));단말.Запиши(" / ");단말.Запиши(관리명령.Word_СМС(INDEX));단말.Запиши(" : ");단말.Запиши(관리명령.설명(INDEX));단말.문자(10);}
        단말.Запиши("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Запиши("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Запиши("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Изврши_наредба() {
        int Команда=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_СМС(INDEX)))Команда=INDEX;
        if(같음(0,"ifconfig"))Команда=0;if(같음(0,"ss"))Команда=4;
        if(Команда<0)return false;
        if(Команда==11){if(같음(1,"net") || 같음(1,"system"))прикажи_помош();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.прикажи_помош();return true;}
        if(Команда==0 || Команда==1)Мрежа_наредба(Команда==1);
        else if(Команда==2)응답시험();
        else if(Команда==6)прикажи_статус_bf9821b5();
        else if(ставка_COUNT()!=1){неуспех_VALUE("This command takes no arguments; help system");}
        else if(Команда==3)прикажи_патека();else if(Команда==4)прикажи_Мрежа();else if(Команда==5)прикажи_Tasks();else if(Команда==7)прикажи_Меморија();else if(Команда==8)прикажи_Склад();else if(Команда==9)прикажи_Активност();
        else if(Команда==10)табла.전원끄기();
        return true;
    }
}
