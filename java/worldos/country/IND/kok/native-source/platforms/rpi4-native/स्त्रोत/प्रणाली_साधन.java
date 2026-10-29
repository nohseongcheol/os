// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** प्रत्यक्ष_डेटा कर्नेल_मोल 상태를 읽는 IPv4·ICMP·작업·मेमरी_मोल·RAM 저장소 관리 आदेश. */
public final class प्रणाली_साधन {
    static int नामो_मोल;
    static boolean 같음(int INDEX, String Word_SMS) { return 명령해석기.같음(INDEX, Word_SMS); }
    static int आयटम_COUNT() { return 명령해석기.टोकन_COUNT; }
    static void अपेस_मोल(String README_eb81d7d9) { 명령해석기.मेजप=2; 단말.बरोवचें(README_eb81d7d9); 단말.문자(10); }
    static void चूक(int मोल) { 명령해석기.चूक(मोल); }
    static void 수항목(String नांव, int मोल) { 단말.बरोवचें(नांव); 단말.수(मोल); 단말.문자(10); }
    static int अंक_मोल(int INDEX, int 한도) {
        if (INDEX>=आयटम_COUNT() || 명령해석기.लांबाय_मोल[INDEX]==0) return -1;
        int मोल=0;
        for (int 순번=0; 순번<명령해석기.लांबाय_मोल[INDEX]; 순번++) {
            int वर्ण_मोल=명령해석기.टोकन_मोल[명령해석기.시작점[INDEX]+순번]-'0';
            if (वर्ण_मोल<0 || वर्ण_मोल>9 || मोल>(한도-वर्ण_मोल)/10) return -1;
            मोल=मोल*10+वर्ण_मोल;
        }
        return मोल<=한도?मोल:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=आयटम_COUNT()) return false;
        int मोल=0, 덩이=0, अंक_COUNT=0, पॉयंट_COUNT=0;
        for (int 순번=0; 순번<명령해석기.लांबाय_मोल[INDEX]; 순번++) {
            int वर्ण_मोल=명령해석기.टोकन_मोल[명령해석기.시작점[INDEX]+순번];
            if (वर्ण_मोल=='.') { if (अंक_COUNT==0 || ++पॉयंट_COUNT>3) return false; मोल=(मोल<<8)|덩이; 덩이=अंक_COUNT=0; }
            else { if (वर्ण_मोल<'0' || वर्ण_मोल>'9' || ++अंक_COUNT>3) return false; 덩이=덩이*10+वर्ण_मोल-'0'; if(덩이>255)return false; }
        }
        if (पॉयंट_COUNT!=3 || अंक_COUNT==0) return false;
        नामो_मोल=(मोल<<8)|덩이; return true;
    }
    static void बरोवचें_नामो(int मोल) {
        단말.수((मोल>>>24)&255); 단말.문자('.'); 단말.수((मोल>>>16)&255); 단말.문자('.');
        단말.수((मोल>>>8)&255); 단말.문자('.'); 단말.수(मोल&255);
    }
    static void शो_नॅटवर्क_स्थिती() {
        단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(20,0)!=0?"en0: ":"sl0: "); 단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(3,0)!=0?"UP":"DOWN");
        단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(0,0));
        단말.बरोवचें(" netmask "); बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(1,0)); 단말.बरोवचें(" gateway "); बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(2,0)); 단말.문자(10);
        단말.बरोवचें("  RX packets "); 단말.수(बोर्ड.नॅटवर्क_स्थिती(4,0)); 단말.बरोवचें(" bytes "); 단말.수(बोर्ड.नॅटवर्क_स्थिती(6,0));
        단말.बरोवचें(" TX packets "); 단말.수(बोर्ड.नॅटवर्क_स्थिती(5,0)); 단말.बरोवचें(" bytes "); 단말.수(बोर्ड.नॅटवर्क_स्थिती(7,0)); 단말.문자(10);
        수항목("  dropped ",बोर्ड.नॅटवर्क_स्थिती(8,0));
    }
    static void संच_नामो(int चलोवप) {
        if (आयटम_COUNT()!=चलोवप+3 || !주소읽기(चलोवप)) { अपेस_मोल("사용법: ipconfig set नामो 주소가림 गेटवे_मोल"); return; }
        int नामो=नामो_मोल;
        if(!주소읽기(चलोवप+1)){अपेस_मोल("Invalid IPv4 netmask");return;} int मास्क_मोल=नामो_मोल;
        if(!주소읽기(चलोवप+2)){अपेस_मोल("Invalid IPv4 gateway");return;}
        int मेजप=बोर्ड.नॅटवर्क_मांडावळी(0,नामो,मास्क_मोल,नामो_मोल);
        if(मेजप<0) { चूक(मेजप); if(मेजप==-16)단말.बरोवचें("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.बरोवचें("IPv4 configuration applied (until reboot)\n"); शो_नॅटवर्क_स्थिती(); }
    }
    static void नॅटवर्क_आदेश(boolean IP_नामो) {
        if (आयटम_COUNT()==1 || आयटम_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || आयटम_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { शो_नॅटवर्क_स्थिती();return; }
        if (IP_नामो && 같음(1,"route") && (आयटम_COUNT()==2 || आयटम_COUNT()==3&&같음(2,"show"))) { शो_पाथ();return; }
        if (같음(1,"set")) { संच_नामो(2);return; }
        if (आयटम_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { बोर्ड.नॅटवर्क_मांडावळी(같음(1,"up")?1:2,0,0,0);शो_नॅटवर्क_स्थिती();return; }
        if (IP_नामो && आयटम_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { बोर्ड.नॅटवर्क_मांडावळी(같음(5,"up")?1:2,0,0,0);शो_नॅटवर्क_स्थिती();return; }
        अपेस_मोल("사용법: ip [addr show|route show|set नामो 주소가림 गेटवे_मोल|link set dev sl0 up|down]");
    }
    static void शो_पाथ() {
        단말.बरोवचें("Destination Netmask Gateway Interface\n");
        बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(0,0)&बोर्ड.नॅटवर्क_स्थिती(1,0));단말.문자(' ');बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(1,0));단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (बोर्ड.नॅटवर्क_स्थिती(2,0)!=0) {단말.बरोवचें("0.0.0.0 0.0.0.0 ");बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(2,0));단말.बरोवचें(बोर्ड.नॅटवर्क_स्थिती(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void शो_नॅटवर्क() {
        단말.बरोवचें("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_वर्ग=बोर्ड.नॅटवर्क_स्थिती(10,INDEX);if(TYPE_वर्ग==0)continue;
            단말.बरोवचें(TYPE_वर्ग==1?"TCP ":"UDP ");बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(16,INDEX));단말.문자(':');단말.수(बोर्ड.नॅटवर्क_स्थिती(11,INDEX));단말.문자(' ');
            बरोवचें_नामो(बोर्ड.नॅटवर्क_स्थिती(12,INDEX));단말.문자(':');단말.수(बोर्ड.नॅटवर्क_स्थिती(13,INDEX));단말.문자(' ');
            int स्थिती_मोल_e10195a1=बोर्ड.नॅटवर्क_स्थिती(14,INDEX);단말.बरोवचें(TYPE_वर्ग==2?"DATAGRAM":स्थिती_मोल_e10195a1==1?"LISTEN":स्थिती_मोल_e10195a1==2?"ESTABLISHED":स्थिती_मोल_e10195a1==3?"CLOSE_WAIT":स्थिती_मोल_e10195a1==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(बोर्ड.नॅटवर्क_स्थिती(15,INDEX));단말.문자(10);
        }
        단말.बरोवचें("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int चलोवप=बोर्ड.밀리초();
        while(बोर्ड.밀리초()-चलोवप<밀리초) {
            if(셸입출력.대화가능()!=0){int वर्ण_मोल=बोर्ड.직렬읽기();if(वर्ण_मोल==3 || वर्ण_मोल=='q' || वर्ण_मोल=='Q' || वर्ण_मोल==27 || वर्ण_मोल==-4096)return false;}
            बोर्ड.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, लक्ष्य=-1;
        for(int स्थिती_INDEX=1;स्थिती_INDEX<आयटम_COUNT();स्थिती_INDEX++) {
            if(같음(स्थिती_INDEX,"-c")){횟수=अंक_मोल(++स्थिती_INDEX,100);if(횟수<1){अपेस_मोल("ping: -c 1..100");return;}}
            else if(같음(स्थिती_INDEX,"-W")){제한=अंक_मोल(++स्थिती_INDEX,10);if(제한<1){अपेस_मोल("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(लक्ष्य<0)लक्ष्य=स्थिती_INDEX;else{अपेस_मोल("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(लक्ष्य<0 || !주소읽기(लक्ष्य)){अपेस_मोल("ping: an IPv4 address is required (DNS is not configured)");return;}
        int नामो=नामो_मोल, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.बरोवचें("PING ");बरोवचें_नामो(नामो);단말.बरोवचें(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int क्रम_मोल=1;क्रम_मोल<=횟수 && 계속;क्रम_मोल++) {
            int 처리값=बोर्ड.응답보내기(नामो,क्रम_मोल);
            if(처리값<0){चूक(처리값);break;}보낸수++;
            int चलोवप=बोर्ड.밀리초();
            while(बोर्ड.응답읽기(0)==-11 && बोर्ड.밀리초()-चलोवप<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(बोर्ड.응답읽기(0)==0){
                int TIME_मोल=बोर्ड.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_मोल;if(TIME_मोल<최솟값)최솟값=TIME_मोल;if(TIME_मोल>최댓값)최댓값=TIME_मोल;
                단말.बरोवचें("32 bytes from ");बरोवचें_नामो(नामो);단말.बरोवचें(" seq=");단말.수(क्रम_मोल);단말.बरोवचें(" ttl=");단말.수(बोर्ड.응답읽기(2));단말.बरोवचें(" time=");단말.수(TIME_मोल);단말.बरोवचें(" ms\n");
            }else{단말.बरोवचें("Request timeout seq=");단말.수(क्रम_मोल);단말.문자(10);}
            if(क्रम_मोल<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.बरोवचें(" transmitted, ");단말.수(RECEIVED_COUNT);단말.बरोवचें(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.बरोवचें("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.बरोवचें("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.बरोवचें(" ms\n");}
        명령해석기.मेजप=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void शो_कृती() { 단말.बरोवचें("up ");단말.수(बोर्ड.밀리초()/1000);단말.बरोवचें(" seconds\n"); }
    static void शो_मेमरी() {
        수항목("ARM RAM KiB (firmware): ",बोर्ड.क्वॅरी_प्रणाली(0,0));
        수항목("Kernel image+BSS+stack KiB: ",बोर्ड.क्वॅरी_प्रणाली(1,0));
        int 총량=बोर्ड.क्वॅरी_प्रणाली(2,0), 사용량=बोर्ड.क्वॅरी_प्रणाली(3,0);
        단말.बरोवचें("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",बोर्ड.क्वॅरी_प्रणाली(4,0));
        수항목("EL0 arena+session reserve KiB: ",बोर्ड.क्वॅरी_प्रणाली(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=बोर्ड.क्वॅरी_प्रणाली(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.बरोवचें("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void शो_Tasks() {
        단말.बरोवचें("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.बरोवचें("1 - RUN - - ");단말.수(बोर्ड.밀리초());단말.बरोवचें(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(बोर्ड.कार्य_स्थिती(INDEX)>0){단말.수(INDEX+1);단말.बरोवचें(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int स्थिती_मोल_e10195a1=बोर्ड.क्वॅरी_प्रणाली(20,INDEX);if(स्थिती_मोल_e10195a1==0)continue;
            단말.수(बोर्ड.क्वॅरी_प्रणाली(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.बरोवचें(स्थिती_मोल_e10195a1==1?" RUN ":" SUSPENDED ");
            단말.수(बोर्ड.क्वॅरी_प्रणाली(22,INDEX));단말.문자(' ');단말.수(बोर्ड.क्वॅरी_प्रणाली(24,INDEX));단말.문자(' ');단말.수(बोर्ड.क्वॅरी_प्रणाली(23,INDEX));단말.문자(' ');
            for(int स्थिती_INDEX=0;स्थिती_INDEX<288;स्थिती_INDEX++){int बायट_मोल=बोर्ड.क्वॅरी_प्रणाली(25,INDEX+स्थिती_INDEX*4);if(बायट_मोल==0)break;बोर्ड.직렬쓰기(बायट_मोल);}단말.문자(10);
        }
    }
    static void शो_सांठवण() {
        int स्लॉट_COUNT=0, डेटा_COUNT=0;
        for(int INDEX=0;INDEX<मेमरी_फायली.फायल_COUNT;INDEX++)if(मेमरी_फायली.이름길이[INDEX]>0 || मेमरी_फायली.संदर्भ_COUNT[INDEX]>0){स्लॉट_COUNT++;डेटा_COUNT+=मेमरी_फायली.लांबाय_मोल[INDEX];}
        단말.बरोवचें("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(मेमरी_फायली.फायल_COUNT*16384);단말.문자(' ');단말.수(स्लॉट_COUNT*16384);단말.문자(' ');단말.수((मेमरी_फायली.फायल_COUNT-स्लॉट_COUNT)*16384);단말.문자(' ');단말.수(डेटा_COUNT);단말.문자(' ');단말.수(स्लॉट_COUNT);단말.문자('/');단말.수(मेमरी_फायली.फायल_COUNT);단말.बरोवचें(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void शो_स्थिती_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(आयटम_COUNT()>1){if(आयटम_COUNT()!=3 || !같음(1,"-n") || (횟수=अंक_मोल(2,1000))<1){अपेस_मोल("사용법: top [-n 1..1000]; q/Ctrl+C로 सोडचें_एप्लिकेशन");return;}}
        for(int SEQUENCE_मोल=0;횟수==0 || SEQUENCE_मोल<횟수;SEQUENCE_मोल++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.बरोवचें("\u001b[2J\u001b[H");
            शो_कृती();शो_मेमरी();शो_Tasks();
            if(횟수!=0 && SEQUENCE_मोल+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void शो_आदार() {
        단말.बरोवचें("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.बरोवचें(표준말(INDEX));단말.बरोवचें(" / ");단말.बरोवचें(관리명령.Word_SMS(INDEX));단말.बरोवचें(" : ");단말.बरोवचें(관리명령.설명(INDEX));단말.문자(10);}
        단말.बरोवचें("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.बरोवचें("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.बरोवचें("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean पाळो_दिवचो_आदेश() {
        int आदेश=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))आदेश=INDEX;
        if(같음(0,"ifconfig"))आदेश=0;if(같음(0,"ss"))आदेश=4;
        if(आदेश<0)return false;
        if(आदेश==11){if(같음(1,"net") || 같음(1,"system"))शो_आदार();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.शो_आदार();return true;}
        if(आदेश==0 || आदेश==1)नॅटवर्क_आदेश(आदेश==1);
        else if(आदेश==2)응답시험();
        else if(आदेश==6)शो_स्थिती_bf9821b5();
        else if(आयटम_COUNT()!=1){अपेस_मोल("This command takes no arguments; help system");}
        else if(आदेश==3)शो_पाथ();else if(आदेश==4)शो_नॅटवर्क();else if(आदेश==5)शो_Tasks();else if(आदेश==7)शो_मेमरी();else if(आदेश==8)शो_सांठवण();else if(आदेश==9)शो_कृती();
        else if(आदेश==10)बोर्ड.전원끄기();
        return true;
    }
}
