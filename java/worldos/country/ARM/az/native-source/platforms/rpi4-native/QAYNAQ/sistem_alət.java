// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktiki_verilənlər nüvə_VALUE 상태를 읽는 IPv4·ICMP·작업·Yaddaş_VALUE·RAM anbar_kök 관리 Əmr. */
public final class sistem_alət {
    static int ünvan_VALUE;
    static boolean 같음(int INDEX, String Söz_SMS) { return 명령해석기.같음(INDEX, Söz_SMS); }
    static int element_COUNT() { return 명령해석기.nişan_COUNT; }
    static void xəta_VALUE(String OXUMƏNİ_eb81d7d9) { 명령해석기.ölçü=2; 단말.Yazma(OXUMƏNİ_eb81d7d9); 단말.문자(10); }
    static void XƏTA(int VALUE) { 명령해석기.XƏTA(VALUE); }
    static void 수항목(String Ad, int VALUE) { 단말.Yazma(Ad); 단말.수(VALUE); 단말.문자(10); }
    static int rəqəm_VALUE(int INDEX, int 한도) {
        if (INDEX>=element_COUNT() || 명령해석기.uzunluq_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<명령해석기.uzunluq_VALUE[INDEX]; 순번++) {
            int simvol_VALUE_068c2631=명령해석기.nişan_VALUE[명령해석기.시작점[INDEX]+순번]-'0';
            if (simvol_VALUE_068c2631<0 || simvol_VALUE_068c2631>9 || VALUE>(한도-simvol_VALUE_068c2631)/10) return -1;
            VALUE=VALUE*10+simvol_VALUE_068c2631;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=element_COUNT()) return false;
        int VALUE=0, 덩이=0, rəqəm_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<명령해석기.uzunluq_VALUE[INDEX]; 순번++) {
            int simvol_VALUE_068c2631=명령해석기.nişan_VALUE[명령해석기.시작점[INDEX]+순번];
            if (simvol_VALUE_068c2631=='.') { if (rəqəm_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|덩이; 덩이=rəqəm_COUNT=0; }
            else { if (simvol_VALUE_068c2631<'0' || simvol_VALUE_068c2631>'9' || ++rəqəm_COUNT>3) return false; 덩이=덩이*10+simvol_VALUE_068c2631-'0'; if(덩이>255)return false; }
        }
        if (p_COUNT!=3 || rəqəm_COUNT==0) return false;
        ünvan_VALUE=(VALUE<<8)|덩이; return true;
    }
    static void yazmaq_ünvan(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void göstərmək_Şəbəkə_vəziyyət() {
        단말.Yazma(lövhə.Şəbəkə_vəziyyət(20,0)!=0?"en0: ":"sl0: "); 단말.Yazma(lövhə.Şəbəkə_vəziyyət(3,0)!=0?"UP":"DOWN");
        단말.Yazma(lövhə.Şəbəkə_vəziyyət(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Yazma(lövhə.Şəbəkə_vəziyyət(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(0,0));
        단말.Yazma(" netmask "); yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(1,0)); 단말.Yazma(" gateway "); yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(2,0)); 단말.문자(10);
        단말.Yazma("  RX packets "); 단말.수(lövhə.Şəbəkə_vəziyyət(4,0)); 단말.Yazma(" bytes "); 단말.수(lövhə.Şəbəkə_vəziyyət(6,0));
        단말.Yazma(" TX packets "); 단말.수(lövhə.Şəbəkə_vəziyyət(5,0)); 단말.Yazma(" bytes "); 단말.수(lövhə.Şəbəkə_vəziyyət(7,0)); 단말.문자(10);
        수항목("  dropped ",lövhə.Şəbəkə_vəziyyət(8,0));
    }
    static void Dəst_ünvan(int İcra_Et) {
        if (element_COUNT()!=İcra_Et+3 || !주소읽기(İcra_Et)) { xəta_VALUE("사용법: ipconfig set ünvan 주소가림 şlüz_VALUE"); return; }
        int ünvan=ünvan_VALUE;
        if(!주소읽기(İcra_Et+1)){xəta_VALUE("Invalid IPv4 netmask");return;} int maska_VALUE=ünvan_VALUE;
        if(!주소읽기(İcra_Et+2)){xəta_VALUE("Invalid IPv4 gateway");return;}
        int ölçü=lövhə.Şəbəkə_Parametrlər(0,ünvan,maska_VALUE,ünvan_VALUE);
        if(ölçü<0) { XƏTA(ölçü); if(ölçü==-16)단말.Yazma("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Yazma("IPv4 configuration applied (until reboot)\n"); göstərmək_Şəbəkə_vəziyyət(); }
    }
    static void Şəbəkə_əmr(boolean IP_ünvan) {
        if (element_COUNT()==1 || element_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || element_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { göstərmək_Şəbəkə_vəziyyət();return; }
        if (IP_ünvan && 같음(1,"route") && (element_COUNT()==2 || element_COUNT()==3&&같음(2,"show"))) { göstərmək_yol();return; }
        if (같음(1,"set")) { Dəst_ünvan(2);return; }
        if (element_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { lövhə.Şəbəkə_Parametrlər(같음(1,"up")?1:2,0,0,0);göstərmək_Şəbəkə_vəziyyət();return; }
        if (IP_ünvan && element_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { lövhə.Şəbəkə_Parametrlər(같음(5,"up")?1:2,0,0,0);göstərmək_Şəbəkə_vəziyyət();return; }
        xəta_VALUE("사용법: ip [addr show|route show|set ünvan 주소가림 şlüz_VALUE|link set dev sl0 up|down]");
    }
    static void göstərmək_yol() {
        단말.Yazma("Destination Netmask Gateway Interface\n");
        yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(0,0)&lövhə.Şəbəkə_vəziyyət(1,0));단말.문자(' ');yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(1,0));단말.Yazma(lövhə.Şəbəkə_vəziyyət(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (lövhə.Şəbəkə_vəziyyət(2,0)!=0) {단말.Yazma("0.0.0.0 0.0.0.0 ");yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(2,0));단말.Yazma(lövhə.Şəbəkə_vəziyyət(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void göstərmək_Şəbəkə() {
        단말.Yazma("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_sahə=lövhə.Şəbəkə_vəziyyət(10,INDEX);if(TYPE_sahə==0)continue;
            단말.Yazma(TYPE_sahə==1?"TCP ":"UDP ");yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(16,INDEX));단말.문자(':');단말.수(lövhə.Şəbəkə_vəziyyət(11,INDEX));단말.문자(' ');
            yazmaq_ünvan(lövhə.Şəbəkə_vəziyyət(12,INDEX));단말.문자(':');단말.수(lövhə.Şəbəkə_vəziyyət(13,INDEX));단말.문자(' ');
            int vəziyyət_VALUE=lövhə.Şəbəkə_vəziyyət(14,INDEX);단말.Yazma(TYPE_sahə==2?"DATAGRAM":vəziyyət_VALUE==1?"LISTEN":vəziyyət_VALUE==2?"ESTABLISHED":vəziyyət_VALUE==3?"CLOSE_WAIT":vəziyyət_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(lövhə.Şəbəkə_vəziyyət(15,INDEX));단말.문자(10);
        }
        단말.Yazma("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean gözlə_vəziyyət(int 밀리초) {
        int İcra_Et=lövhə.밀리초();
        while(lövhə.밀리초()-İcra_Et<밀리초) {
            if(셸입출력.대화가능()!=0){int simvol_VALUE_068c2631=lövhə.직렬읽기();if(simvol_VALUE_068c2631==3 || simvol_VALUE_068c2631=='q' || simvol_VALUE_068c2631=='Q' || simvol_VALUE_068c2631==27 || simvol_VALUE_068c2631==-4096)return false;}
            lövhə.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, hədəf=-1;
        for(int yerinə_qoymaq_INDEX=1;yerinə_qoymaq_INDEX<element_COUNT();yerinə_qoymaq_INDEX++) {
            if(같음(yerinə_qoymaq_INDEX,"-c")){횟수=rəqəm_VALUE(++yerinə_qoymaq_INDEX,100);if(횟수<1){xəta_VALUE("ping: -c 1..100");return;}}
            else if(같음(yerinə_qoymaq_INDEX,"-W")){제한=rəqəm_VALUE(++yerinə_qoymaq_INDEX,10);if(제한<1){xəta_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(hədəf<0)hədəf=yerinə_qoymaq_INDEX;else{xəta_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(hədəf<0 || !주소읽기(hədəf)){xəta_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ünvan=ünvan_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Yazma("PING ");yazmaq_ünvan(ünvan);단말.Yazma(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ardıcıllıq_VALUE=1;ardıcıllıq_VALUE<=횟수 && 계속;ardıcıllıq_VALUE++) {
            int 처리값=lövhə.göndərmək_video_münasibət(ünvan,ardıcıllıq_VALUE);
            if(처리값<0){XƏTA(처리값);break;}보낸수++;
            int İcra_Et=lövhə.밀리초();
            while(lövhə.응답읽기(0)==-11 && lövhə.밀리초()-İcra_Et<제한)if(!gözlə_vəziyyət(1)){계속=false;break;}
            if(!계속)break;
            if(lövhə.응답읽기(0)==0){
                int TIME_VALUE=lövhə.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Yazma("32 bytes from ");yazmaq_ünvan(ünvan);단말.Yazma(" seq=");단말.수(ardıcıllıq_VALUE);단말.Yazma(" ttl=");단말.수(lövhə.응답읽기(2));단말.Yazma(" time=");단말.수(TIME_VALUE);단말.Yazma(" ms\n");
            }else{단말.Yazma("Request timeout seq=");단말.수(ardıcıllıq_VALUE);단말.문자(10);}
            if(ardıcıllıq_VALUE<횟수)계속=gözlə_vəziyyət(200);
        }
        단말.수(보낸수);단말.Yazma(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Yazma(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Yazma("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Yazma("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Yazma(" ms\n");}
        명령해석기.ölçü=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void göstərmək_Fəaliyyət() { 단말.Yazma("up ");단말.수(lövhə.밀리초()/1000);단말.Yazma(" seconds\n"); }
    static void göstərmək_Yaddaş() {
        수항목("ARM RAM KiB (firmware): ",lövhə.sorğu_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",lövhə.sorğu_sistem(1,0));
        int 총량=lövhə.sorğu_sistem(2,0), 사용량=lövhə.sorğu_sistem(3,0);
        단말.Yazma("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",lövhə.sorğu_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",lövhə.sorğu_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=lövhə.sorğu_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Yazma("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void göstərmək_Tasks() {
        단말.Yazma("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Yazma("1 - RUN - - ");단말.수(lövhə.밀리초());단말.Yazma(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(lövhə.tapşırıq_vəziyyət(INDEX)>0){단말.수(INDEX+1);단말.Yazma(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int vəziyyət_VALUE=lövhə.sorğu_sistem(20,INDEX);if(vəziyyət_VALUE==0)continue;
            단말.수(lövhə.sorğu_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Yazma(vəziyyət_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(lövhə.sorğu_sistem(22,INDEX));단말.문자(' ');단말.수(lövhə.sorğu_sistem(24,INDEX));단말.문자(' ');단말.수(lövhə.sorğu_sistem(23,INDEX));단말.문자(' ');
            for(int yerinə_qoymaq_INDEX=0;yerinə_qoymaq_INDEX<288;yerinə_qoymaq_INDEX++){int bayt_VALUE=lövhə.sorğu_sistem(25,INDEX+yerinə_qoymaq_INDEX*4);if(bayt_VALUE==0)break;lövhə.직렬쓰기(bayt_VALUE);}단말.문자(10);
        }
    }
    static void göstərmək_Yaddaş_deafe149() {
        int slot_COUNT=0, verilənlər_COUNT=0;
        for(int INDEX=0;INDEX<Yaddaş_Fayllar.fayl_COUNT;INDEX++)if(Yaddaş_Fayllar.이름길이[INDEX]>0 || Yaddaş_Fayllar.İstinad_COUNT[INDEX]>0){slot_COUNT++;verilənlər_COUNT+=Yaddaş_Fayllar.uzunluq_VALUE[INDEX];}
        단말.Yazma("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Yaddaş_Fayllar.fayl_COUNT*16384);단말.문자(' ');단말.수(slot_COUNT*16384);단말.문자(' ');단말.수((Yaddaş_Fayllar.fayl_COUNT-slot_COUNT)*16384);단말.문자(' ');단말.수(verilənlər_COUNT);단말.문자(' ');단말.수(slot_COUNT);단말.문자('/');단말.수(Yaddaş_Fayllar.fayl_COUNT);단말.Yazma(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void göstərmək_vəziyyət_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(element_COUNT()>1){if(element_COUNT()!=3 || !같음(1,"-n") || (횟수=rəqəm_VALUE(2,1000))<1){xəta_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 çıxış_proqram");return;}}
        for(int SEQUENCE_VALUE=0;횟수==0 || SEQUENCE_VALUE<횟수;SEQUENCE_VALUE++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Yazma("\u001b[2J\u001b[H");
            göstərmək_Fəaliyyət();göstərmək_Yaddaş();göstərmək_Tasks();
            if(횟수!=0 && SEQUENCE_VALUE+1>=횟수)break;
            if(!gözlə_vəziyyət(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void göstərmək_kömək() {
        단말.Yazma("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Yazma(표준말(INDEX));단말.Yazma(" / ");단말.Yazma(관리명령.Söz_SMS(INDEX));단말.Yazma(" : ");단말.Yazma(관리명령.설명(INDEX));단말.문자(10);}
        단말.Yazma("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Yazma("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Yazma("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean icra_etmək_əmr() {
        int Əmr=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Söz_SMS(INDEX)))Əmr=INDEX;
        if(같음(0,"ifconfig"))Əmr=0;if(같음(0,"ss"))Əmr=4;
        if(Əmr<0)return false;
        if(Əmr==11){if(같음(1,"net") || 같음(1,"system"))göstərmək_kömək();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.göstərmək_kömək();return true;}
        if(Əmr==0 || Əmr==1)Şəbəkə_əmr(Əmr==1);
        else if(Əmr==2)응답시험();
        else if(Əmr==6)göstərmək_vəziyyət_bf9821b5();
        else if(element_COUNT()!=1){xəta_VALUE("This command takes no arguments; help system");}
        else if(Əmr==3)göstərmək_yol();else if(Əmr==4)göstərmək_Şəbəkə();else if(Əmr==5)göstərmək_Tasks();else if(Əmr==7)göstərmək_Yaddaş();else if(Əmr==8)göstərmək_Yaddaş_deafe149();else if(Əmr==9)göstərmək_Fəaliyyət();
        else if(Əmr==10)lövhə.전원끄기();
        return true;
    }
}
