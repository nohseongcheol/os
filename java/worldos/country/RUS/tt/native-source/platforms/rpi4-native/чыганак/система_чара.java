// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** фактик_мәгълүмат төш_VALUE 상태를 읽는 IPv4·ICMP·작업·Хәтер_VALUE·RAM 저장소 관리 команда. */
public final class система_чара {
    static int адрес_VALUE;
    static boolean 같음(int INDEX, String Word_СМС) { return 명령해석기.같음(INDEX, Word_СМС); }
    static int элемент_COUNT() { return 명령해석기.токен_COUNT; }
    static void эштән_туктау_VALUE(String Белешмә_файлы_eb81d7d9) { 명령해석기.үлчәм=2; 단말.язу(Белешмә_файлы_eb81d7d9); 단말.문자(10); }
    static void Хата(int VALUE) { 명령해석기.Хата(VALUE); }
    static void 수항목(String исем, int VALUE) { 단말.язу(исем); 단말.수(VALUE); 단말.문자(10); }
    static int сан_VALUE(int INDEX, int 한도) {
        if (INDEX>=элемент_COUNT() || 명령해석기.озынлык_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.озынлык_VALUE[INDEX]; 순번++) {
            int символ_VALUE_068c2631=명령해석기.токен_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (символ_VALUE_068c2631<0 || символ_VALUE_068c2631>9 || VALUE>(한도-символ_VALUE_068c2631)/10) return -1;
            VALUE=VALUE*10+символ_VALUE_068c2631;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=элемент_COUNT()) return false;
        int VALUE=0, 덩이=0, сан_COUNT=0, балл_COUNT=0;
        for (int 순번=0; 순번<명령해석기.озынлык_VALUE[INDEX]; 순번++) {
            int символ_VALUE_068c2631=명령해석기.токен_VALUE[명령해석기.시작점[INDEX]+순번];
            if (символ_VALUE_068c2631=='.') { if (сан_COUNT==0 || ++балл_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=сан_COUNT=0; }
            else { if (символ_VALUE_068c2631<'0' || символ_VALUE_068c2631>'9' || ++сан_COUNT>3) return false; 덩이=덩이*10+символ_VALUE_068c2631-'0'; if(덩이>255)return false; }
        }
        if (балл_COUNT!=3 || сан_COUNT==0) return false;
        адрес_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void язу_адрес(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void күрсәтү_Челтәр_халәт() {
        단말.язу(такта.Челтәр_халәт(20,0)!=0?"en0: ":"sl0: "); 단말.язу(такта.Челтәр_халәт(3,0)!=0?"UP":"DOWN");
        단말.язу(такта.Челтәр_халәт(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.язу(такта.Челтәр_халәт(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); язу_адрес(такта.Челтәр_халәт(0,0));
        단말.язу(" netmask "); язу_адрес(такта.Челтәр_халәт(1,0)); 단말.язу(" gateway "); язу_адрес(такта.Челтәр_халәт(2,0)); 단말.문자(10);
        단말.язу("  RX packets "); 단말.수(такта.Челтәр_халәт(4,0)); 단말.язу(" bytes "); 단말.수(такта.Челтәр_халәт(6,0));
        단말.язу(" TX packets "); 단말.수(такта.Челтәр_халәт(5,0)); 단말.язу(" bytes "); 단말.수(такта.Челтәр_халәт(7,0)); 단말.문자(10);
        수항목("  dropped ",такта.Челтәр_халәт(8,0));
    }
    static void җыелма_адрес(int эшләтү) {
        if (элемент_COUNT()!=эшләтү+3 || !주소읽기(эшләтү)) { эштән_туктау_VALUE("사용법: ipconfig set адрес 주소가림 шлюз_VALUE"); return; }
        int адрес=адрес_VALUE;
        if(!주소읽기(эшләтү+1)){эштән_туктау_VALUE("Invalid IPv4 netmask");return;} int үрнәк_VALUE=адрес_VALUE;
        if(!주소읽기(эшләтү+2)){эштән_туктау_VALUE("Invalid IPv4 gateway");return;}
        int үлчәм=такта.Челтәр_Параметрлар(0,адрес,үрнәк_VALUE,адрес_VALUE);
        if(үлчәм<0) { Хата(үлчәм); if(үлчәм==-16)단말.язу("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.язу("IPv4 configuration applied (until reboot)\n"); күрсәтү_Челтәр_халәт(); }
    }
    static void Челтәр_команда(boolean IP_адрес) {
        if (элемент_COUNT()==1 || элемент_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || элемент_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { күрсәтү_Челтәр_халәт();return; }
        if (IP_адрес && 같음(1,"route") && (элемент_COUNT()==2 || элемент_COUNT()==3&&같음(2,"show"))) { күрсәтү_юл();return; }
        if (같음(1,"set")) { җыелма_адрес(2);return; }
        if (элемент_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { такта.Челтәр_Параметрлар(같음(1,"up")?1:2,0,0,0);күрсәтү_Челтәр_халәт();return; }
        if (IP_адрес && элемент_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { такта.Челтәр_Параметрлар(같음(5,"up")?1:2,0,0,0);күрсәтү_Челтәр_халәт();return; }
        эштән_туктау_VALUE("사용법: ip [addr show|route show|set адрес 주소가림 шлюз_VALUE|link set dev sl0 up|down]");
    }
    static void күрсәтү_юл() {
        단말.язу("Destination Netmask Gateway Interface\n");
        язу_адрес(такта.Челтәр_халәт(0,0)&такта.Челтәр_халәт(1,0));단말.문자(' ');язу_адрес(такта.Челтәр_халәт(1,0));단말.язу(такта.Челтәр_халәт(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (такта.Челтәр_халәт(2,0)!=0) {단말.язу("0.0.0.0 0.0.0.0 ");язу_адрес(такта.Челтәр_халәт(2,0));단말.язу(такта.Челтәр_халәт(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void күрсәтү_Челтәр() {
        단말.язу("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_категория=такта.Челтәр_халәт(10,INDEX);if(TYPE_категория==0)continue;
            단말.язу(TYPE_категория==1?"TCP ":"UDP ");язу_адрес(такта.Челтәр_халәт(16,INDEX));단말.문자(':');단말.수(такта.Челтәр_халәт(11,INDEX));단말.문자(' ');
            язу_адрес(такта.Челтәр_халәт(12,INDEX));단말.문자(':');단말.수(такта.Челтәр_халәт(13,INDEX));단말.문자(' ');
            int халәт_VALUE=такта.Челтәр_халәт(14,INDEX);단말.язу(TYPE_категория==2?"DATAGRAM":халәт_VALUE==1?"LISTEN":халәт_VALUE==2?"ESTABLISHED":халәт_VALUE==3?"CLOSE_WAIT":халәт_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(такта.Челтәр_халәт(15,INDEX));단말.문자(10);
        }
        단말.язу("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int эшләтү=такта.밀리초();
        while(такта.밀리초()-эшләтү<밀리초) {
            if(셸입출력.대화가능()!=0){int символ_VALUE_068c2631=такта.직렬읽기();if(символ_VALUE_068c2631==3 || символ_VALUE_068c2631=='q' || символ_VALUE_068c2631=='Q' || символ_VALUE_068c2631==27 || символ_VALUE_068c2631==-4096)return false;}
            такта.YIELD_процессор();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, максат_кыйммәт=-1;
        for(int урнаштыру_INDEX=1;урнаштыру_INDEX<элемент_COUNT();урнаштыру_INDEX++) {
            if(같음(урнаштыру_INDEX,"-c")){횟수=сан_VALUE(++урнаштыру_INDEX,100);if(횟수<1){эштән_туктау_VALUE("ping: -c 1..100");return;}}
            else if(같음(урнаштыру_INDEX,"-W")){제한=сан_VALUE(++урнаштыру_INDEX,10);if(제한<1){эштән_туктау_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(максат_кыйммәт<0)максат_кыйммәт=урнаштыру_INDEX;else{эштән_туктау_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(максат_кыйммәт<0 || !주소읽기(максат_кыйммәт)){эштән_туктау_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int адрес=адрес_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.язу("PING ");язу_адрес(адрес);단말.язу(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int тәртипкә_салу_VALUE=1;тәртипкә_салу_VALUE<=횟수 && 계속;тәртипкә_салу_VALUE++) {
            int 처리값=такта.응답보내기(адрес,тәртипкә_салу_VALUE);
            if(처리값<0){Хата(처리값);break;}보낸수++;
            int эшләтү=такта.밀리초();
            while(такта.응답읽기(0)==-11 && такта.밀리초()-эшләтү<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(такта.응답읽기(0)==0){
                int TIME_VALUE=такта.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.язу("32 bytes from ");язу_адрес(адрес);단말.язу(" seq=");단말.수(тәртипкә_салу_VALUE);단말.язу(" ttl=");단말.수(такта.응답읽기(2));단말.язу(" time=");단말.수(TIME_VALUE);단말.язу(" ms\n");
            }else{단말.язу("Request timeout seq=");단말.수(тәртипкә_салу_VALUE);단말.문자(10);}
            if(тәртипкә_салу_VALUE<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.язу(" transmitted, ");단말.수(RECEIVED_COUNT);단말.язу(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.язу("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.язу("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.язу(" ms\n");}
        명령해석기.үлчәм=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void күрсәтү_Активлык() { 단말.язу("up ");단말.수(такта.밀리초()/1000);단말.язу(" seconds\n"); }
    static void күрсәтү_Хәтер() {
        수항목("ARM RAM KiB (firmware): ",такта.таләп_система(0,0));
        수항목("Kernel image+BSS+stack KiB: ",такта.таләп_система(1,0));
        int 총량=такта.таләп_система(2,0), 사용량=такта.таләп_система(3,0);
        단말.язу("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",такта.таләп_система(4,0));
        수항목("EL0 arena+session reserve KiB: ",такта.таләп_система(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=такта.таләп_система(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.язу("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void күрсәтү_Tasks() {
        단말.язу("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.язу("1 - RUN - - ");단말.수(такта.밀리초());단말.язу(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(такта.мәсьәлә_халәт(INDEX)>0){단말.수(INDEX+1);단말.язу(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int халәт_VALUE=такта.таләп_система(20,INDEX);if(халәт_VALUE==0)continue;
            단말.수(такта.таләп_система(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.язу(халәт_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(такта.таләп_система(22,INDEX));단말.문자(' ');단말.수(такта.таләп_система(24,INDEX));단말.문자(' ');단말.수(такта.таләп_система(23,INDEX));단말.문자(' ');
            for(int урнаштыру_INDEX=0;урнаштыру_INDEX<288;урнаштыру_INDEX++){int байт_VALUE=такта.таләп_система(25,INDEX+урнаштыру_INDEX*4);if(байт_VALUE==0)break;такта.직렬쓰기(байт_VALUE);}단말.문자(10);
        }
    }
    static void күрсәтү_Саклагыч() {
        int оя_COUNT=0, мәгълүмат_COUNT=0;
        for(int INDEX=0;INDEX<Хәтер_Файллар.файл_COUNT;INDEX++)if(Хәтер_Файллар.이름길이[INDEX]>0 || Хәтер_Файллар.Белешмәлекләр_COUNT[INDEX]>0){оя_COUNT++;мәгълүмат_COUNT+=Хәтер_Файллар.озынлык_VALUE[INDEX];}
        단말.язу("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Хәтер_Файллар.файл_COUNT*16384);단말.문자(' ');단말.수(оя_COUNT*16384);단말.문자(' ');단말.수((Хәтер_Файллар.файл_COUNT-оя_COUNT)*16384);단말.문자(' ');단말.수(мәгълүмат_COUNT);단말.문자(' ');단말.수(оя_COUNT);단말.문자('/');단말.수(Хәтер_Файллар.файл_COUNT);단말.язу(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void күрсәтү_халәт_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(элемент_COUNT()>1){if(элемент_COUNT()!=3 || !같음(1,"-n") || (횟수=сан_VALUE(2,1000))<1){эштән_туктау_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 чыгу_кушымта");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.язу("\u001b[2J\u001b[H");
            күрсәтү_Активлык();күрсәтү_Хәтер();күрсәтү_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void күрсәтү_ярдәм() {
        단말.язу("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.язу(표준말(INDEX));단말.язу(" / ");단말.язу(관리명령.Word_СМС(INDEX));단말.язу(" : ");단말.язу(관리명령.설명(INDEX));단말.문자(10);}
        단말.язу("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.язу("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.язу("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean үтәргә_команда() {
        int команда=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_СМС(INDEX)))команда=INDEX;
        if(같음(0,"ifconfig"))команда=0;if(같음(0,"ss"))команда=4;
        if(команда<0)return false;
        if(команда==11){if(같음(1,"net") || 같음(1,"system"))күрсәтү_ярдәм();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.күрсәтү_ярдәм();return true;}
        if(команда==0 || команда==1)Челтәр_команда(команда==1);
        else if(команда==2)응답시험();
        else if(команда==6)күрсәтү_халәт_bf9821b5();
        else if(элемент_COUNT()!=1){эштән_туктау_VALUE("This command takes no arguments; help system");}
        else if(команда==3)күрсәтү_юл();else if(команда==4)күрсәтү_Челтәр();else if(команда==5)күрсәтү_Tasks();else if(команда==7)күрсәтү_Хәтер();else if(команда==8)күрсәтү_Саклагыч();else if(команда==9)күрсәтү_Активлык();
        else if(команда==10)такта.전원끄기();
        return true;
    }
}
