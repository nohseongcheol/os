// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Na_hakika_Tarin_bayani Kwara_Daraja 상태를 읽는 IPv4·ICMP·작업·Mahardatar_kwamfuta_Daraja·RAM 저장소 관리 Umarni. */
public final class na_ura_kayan_aiki {
    static int imel_Daraja;
    static boolean 같음(int Indes, String Microsoft_Word_SMS) { return 명령해석기.같음(Indes, Microsoft_Word_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void Kasa_aiki_Daraja(String README_eb81d7d9) { 명령해석기.결과=2; 단말.Yi_Rubutu(README_eb81d7d9); 단말.문자(10); }
    static void Kuskure(int Daraja) { 명령해석기.Kuskure(Daraja); }
    static void 수항목(String Suna, int Daraja) { 단말.Yi_Rubutu(Suna); 단말.수(Daraja); 단말.문자(10); }
    static int lamba_Daraja(int Indes, int 한도) {
        if (Indes>=개수() || 명령해석기.Tsawo_Daraja[Indes]==0) return -1;
        int Daraja=0;
        for (int 순번=0; 순번<명령해석기.Tsawo_Daraja[Indes]; 순번++) {
            int Harafi_Daraja=명령해석기.token_Daraja[명령해석기.시작점[Indes]+순번]-'0';
            if (Harafi_Daraja<0 || Harafi_Daraja>9 || Daraja>(한도-Harafi_Daraja)/10) return -1;
            Daraja=Daraja*10+Harafi_Daraja;
        }
        return Daraja<=한도?Daraja:-1;
    }
    static boolean 주소읽기(int Indes) {
        if (Indes>=개수()) return false;
        int Daraja=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.Tsawo_Daraja[Indes]; 순번++) {
            int Harafi_Daraja=명령해석기.token_Daraja[명령해석기.시작점[Indes]+순번];
            if (Harafi_Daraja=='.') { if (숫자수==0 || ++점수>3) return false; Daraja=(Daraja<<8)|덩이; 덩이=숫자수=0; }
            else { if (Harafi_Daraja<'0' || Harafi_Daraja>'9' || ++숫자수>3) return false; 덩이=덩이*10+Harafi_Daraja-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        imel_Daraja=(Daraja<<8)|덩이; return true;
    }
    static void Rubuta_imel(int Daraja) {
        단말.수((Daraja>>>24)&255); 단말.문자('.'); 단말.수((Daraja>>>16)&255); 단말.문자('.');
        단말.수((Daraja>>>8)&255); 단말.문자('.'); 단말.수(Daraja&255);
    }
    static void Nuna_Hanyar_sadarwa_samuwa() {
        단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(20,0)!=0?"en0: ":"sl0: "); 단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(3,0)!=0?"UP":"DOWN");
        단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); Rubuta_imel(보드.Hanyar_sadarwa_samuwa(0,0));
        단말.Yi_Rubutu(" netmask "); Rubuta_imel(보드.Hanyar_sadarwa_samuwa(1,0)); 단말.Yi_Rubutu(" gateway "); Rubuta_imel(보드.Hanyar_sadarwa_samuwa(2,0)); 단말.문자(10);
        단말.Yi_Rubutu("  RX packets "); 단말.수(보드.Hanyar_sadarwa_samuwa(4,0)); 단말.Yi_Rubutu(" bytes "); 단말.수(보드.Hanyar_sadarwa_samuwa(6,0));
        단말.Yi_Rubutu(" TX packets "); 단말.수(보드.Hanyar_sadarwa_samuwa(5,0)); 단말.Yi_Rubutu(" bytes "); 단말.수(보드.Hanyar_sadarwa_samuwa(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Hanyar_sadarwa_samuwa(8,0));
    }
    static void zubi_imel(int Tafiyar_da) {
        if (개수()!=Tafiyar_da+3 || !주소읽기(Tafiyar_da)) { Kasa_aiki_Daraja("사용법: ipconfig set imel 주소가림 Mashiga_Daraja"); return; }
        int imel=imel_Daraja;
        if(!주소읽기(Tafiyar_da+1)){Kasa_aiki_Daraja("Invalid IPv4 netmask");return;} int Burtu_Daraja=imel_Daraja;
        if(!주소읽기(Tafiyar_da+2)){Kasa_aiki_Daraja("Invalid IPv4 gateway");return;}
        int 결과=보드.Hanyar_sadarwa_Saituna(0,imel,Burtu_Daraja,imel_Daraja);
        if(결과<0) { Kuskure(결과); if(결과==-16)단말.Yi_Rubutu("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Yi_Rubutu("IPv4 configuration applied (until reboot)\n"); Nuna_Hanyar_sadarwa_samuwa(); }
    }
    static void Hanyar_sadarwa_Umarni(boolean adireshin_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { Nuna_Hanyar_sadarwa_samuwa();return; }
        if (adireshin_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { Nuna_Hanyar_shiga();return; }
        if (같음(1,"set")) { zubi_imel(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Hanyar_sadarwa_Saituna(같음(1,"up")?1:2,0,0,0);Nuna_Hanyar_sadarwa_samuwa();return; }
        if (adireshin_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Hanyar_sadarwa_Saituna(같음(5,"up")?1:2,0,0,0);Nuna_Hanyar_sadarwa_samuwa();return; }
        Kasa_aiki_Daraja("사용법: ip [addr show|route show|set imel 주소가림 Mashiga_Daraja|link set dev sl0 up|down]");
    }
    static void Nuna_Hanyar_shiga() {
        단말.Yi_Rubutu("Destination Netmask Gateway Interface\n");
        Rubuta_imel(보드.Hanyar_sadarwa_samuwa(0,0)&보드.Hanyar_sadarwa_samuwa(1,0));단말.문자(' ');Rubuta_imel(보드.Hanyar_sadarwa_samuwa(1,0));단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Hanyar_sadarwa_samuwa(2,0)!=0) {단말.Yi_Rubutu("0.0.0.0 0.0.0.0 ");Rubuta_imel(보드.Hanyar_sadarwa_samuwa(2,0));단말.Yi_Rubutu(보드.Hanyar_sadarwa_samuwa(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void Nuna_Hanyar_sadarwa() {
        단말.Yi_Rubutu("Proto Local Remote State Queued\n");
        for(int Indes=0;Indes<32;Indes++) {
            int rubuta_ɓangare=보드.Hanyar_sadarwa_samuwa(10,Indes);if(rubuta_ɓangare==0)continue;
            단말.Yi_Rubutu(rubuta_ɓangare==1?"TCP ":"UDP ");Rubuta_imel(보드.Hanyar_sadarwa_samuwa(16,Indes));단말.문자(':');단말.수(보드.Hanyar_sadarwa_samuwa(11,Indes));단말.문자(' ');
            Rubuta_imel(보드.Hanyar_sadarwa_samuwa(12,Indes));단말.문자(':');단말.수(보드.Hanyar_sadarwa_samuwa(13,Indes));단말.문자(' ');
            int Matsayi_Daraja=보드.Hanyar_sadarwa_samuwa(14,Indes);단말.Yi_Rubutu(rubuta_ɓangare==2?"DATAGRAM":Matsayi_Daraja==1?"LISTEN":Matsayi_Daraja==2?"ESTABLISHED":Matsayi_Daraja==3?"CLOSE_WAIT":Matsayi_Daraja==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Hanyar_sadarwa_samuwa(15,Indes));단말.문자(10);
        }
        단말.Yi_Rubutu("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean jira_Matsayi(int 밀리초) {
        int Tafiyar_da=보드.밀리초();
        while(보드.밀리초()-Tafiyar_da<밀리초) {
            if(셸입출력.kimiyar_bayanai_Shigar_da_umarni_na_kwamfuta()!=0){int Harafi_Daraja=보드.직렬읽기();if(Harafi_Daraja==3 || Harafi_Daraja=='q' || Harafi_Daraja=='Q' || Harafi_Daraja==27 || Harafi_Daraja==-4096)return false;}
            보드.ɗan_tsai_da_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, tageti=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=lamba_Daraja(++자리,100);if(횟수<1){Kasa_aiki_Daraja("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=lamba_Daraja(++자리,10);if(제한<1){Kasa_aiki_Daraja("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(tageti<0)tageti=자리;else{Kasa_aiki_Daraja("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(tageti<0 || !주소읽기(tageti)){Kasa_aiki_Daraja("ping: an IPv4 address is required (DNS is not configured)");return;}
        int imel=imel_Daraja, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Yi_Rubutu("PING ");Rubuta_imel(imel);단말.Yi_Rubutu(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int Hanyar_jejjerawa_Daraja=1;Hanyar_jejjerawa_Daraja<=횟수 && 계속;Hanyar_jejjerawa_Daraja++) {
            int 처리값=보드.응답보내기(imel,Hanyar_jejjerawa_Daraja);
            if(처리값<0){Kuskure(처리값);break;}보낸수++;
            int Tafiyar_da=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Tafiyar_da<제한)if(!jira_Matsayi(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int lokaci_Daraja=보드.응답읽기(1);받은수++;누적+=lokaci_Daraja;if(lokaci_Daraja<최솟값)최솟값=lokaci_Daraja;if(lokaci_Daraja>최댓값)최댓값=lokaci_Daraja;
                단말.Yi_Rubutu("32 bytes from ");Rubuta_imel(imel);단말.Yi_Rubutu(" seq=");단말.수(Hanyar_jejjerawa_Daraja);단말.Yi_Rubutu(" ttl=");단말.수(보드.응답읽기(2));단말.Yi_Rubutu(" time=");단말.수(lokaci_Daraja);단말.Yi_Rubutu(" ms\n");
            }else{단말.Yi_Rubutu("Request timeout seq=");단말.수(Hanyar_jejjerawa_Daraja);단말.문자(10);}
            if(Hanyar_jejjerawa_Daraja<횟수)계속=jira_Matsayi(200);
        }
        단말.수(보낸수);단말.Yi_Rubutu(" transmitted, ");단말.수(받은수);단말.Yi_Rubutu(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Yi_Rubutu("% packet loss\n");
        if(받은수>0){단말.Yi_Rubutu("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Yi_Rubutu(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void Nuna_Aiki() { 단말.Yi_Rubutu("up ");단말.수(보드.밀리초()/1000);단말.Yi_Rubutu(" seconds\n"); }
    static void Nuna_Mahardatar_kwamfuta() {
        수항목("ARM RAM KiB (firmware): ",보드.Matantanci_na_ura(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.Matantanci_na_ura(1,0));
        int 총량=보드.Matantanci_na_ura(2,0), 사용량=보드.Matantanci_na_ura(3,0);
        단말.Yi_Rubutu("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.Matantanci_na_ura(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.Matantanci_na_ura(5,0));
        int 매핑=0;for(int Indes=0;Indes<4;Indes++)매핑+=보드.Matantanci_na_ura(22,Indes);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Yi_Rubutu("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void Nuna_Aiyuka() {
        단말.Yi_Rubutu("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Yi_Rubutu("1 - RUN - - ");단말.수(보드.밀리초());단말.Yi_Rubutu(" kernel/shell\n");
        for(int Indes=1;Indes<3;Indes++)if(보드.aiki_Matsayi(Indes)>0){단말.수(Indes+1);단말.Yi_Rubutu(" - READY 64 - - kernel-task\n");}
        for(int Indes=0;Indes<4;Indes++){
            int Matsayi_Daraja=보드.Matantanci_na_ura(20,Indes);if(Matsayi_Daraja==0)continue;
            단말.수(보드.Matantanci_na_ura(21,Indes));단말.문자(' ');단말.수(Indes);단말.Yi_Rubutu(Matsayi_Daraja==1?" RUN ":" SUSPENDED ");
            단말.수(보드.Matantanci_na_ura(22,Indes));단말.문자(' ');단말.수(보드.Matantanci_na_ura(24,Indes));단말.문자(' ');단말.수(보드.Matantanci_na_ura(23,Indes));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int bayit_Daraja=보드.Matantanci_na_ura(25,Indes+자리*4);if(bayit_Daraja==0)break;보드.직렬쓰기(bayit_Daraja);}단말.문자(10);
        }
    }
    static void Nuna_Wurin_adana() {
        int 칸수=0, 자료수=0;
        for(int Indes=0;Indes<Mahardatar_kwamfuta_Fayiloli.파일수;Indes++)if(Mahardatar_kwamfuta_Fayiloli.이름길이[Indes]>0 || Mahardatar_kwamfuta_Fayiloli.참조수[Indes]>0){칸수++;자료수+=Mahardatar_kwamfuta_Fayiloli.Tsawo_Daraja[Indes];}
        단말.Yi_Rubutu("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Mahardatar_kwamfuta_Fayiloli.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Mahardatar_kwamfuta_Fayiloli.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Mahardatar_kwamfuta_Fayiloli.파일수);단말.Yi_Rubutu(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void Nuna_samuwa() {
        int 횟수=셸입출력.kimiyar_bayanai_Shigar_da_umarni_na_kwamfuta()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=lamba_Daraja(2,1000))<1){Kasa_aiki_Daraja("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int JERI_Daraja=0;횟수==0 || JERI_Daraja<횟수;JERI_Daraja++){
            if(셸입출력.kimiyar_bayanai_Shigar_da_umarni_na_kwamfuta()!=0 && 횟수==0)단말.Yi_Rubutu("\u001b[2J\u001b[H");
            Nuna_Aiki();Nuna_Mahardatar_kwamfuta();Nuna_Aiyuka();
            if(횟수!=0 && JERI_Daraja+1>=횟수)break;
            if(!jira_Matsayi(1000))break;
        }
    }
    static String 표준말(int Indes) {
        if(Indes==0)return "ipconfig";if(Indes==1)return "ip";if(Indes==2)return "ping";if(Indes==3)return "route";if(Indes==4)return "netstat";
        if(Indes==5)return "ps";if(Indes==6)return "top";if(Indes==7)return "free";if(Indes==8)return "df";if(Indes==9)return "uptime";if(Indes==10)return "poweroff";return "help";
    }
    static void Nuna_Taimako() {
        단말.Yi_Rubutu("--- Network / system commands ---\n");
        for(int Indes=0;Indes<12;Indes++){단말.Yi_Rubutu(표준말(Indes));단말.Yi_Rubutu(" / ");단말.Yi_Rubutu(관리명령.Microsoft_Word_SMS(Indes));단말.Yi_Rubutu(" : ");단말.Yi_Rubutu(관리명령.설명(Indes));단말.문자(10);}
        단말.Yi_Rubutu("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Yi_Rubutu("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Yi_Rubutu("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean gudanar_Umarni() {
        int Umarni=-1;
        for(int Indes=0;Indes<12;Indes++)if(같음(0,표준말(Indes)) || 같음(0,관리명령.Microsoft_Word_SMS(Indes)))Umarni=Indes;
        if(같음(0,"ifconfig"))Umarni=0;if(같음(0,"ss"))Umarni=4;
        if(Umarni<0)return false;
        if(Umarni==11){if(같음(1,"net") || 같음(1,"system"))Nuna_Taimako();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.Nuna_Taimako();return true;}
        if(Umarni==0 || Umarni==1)Hanyar_sadarwa_Umarni(Umarni==1);
        else if(Umarni==2)응답시험();
        else if(Umarni==6)Nuna_samuwa();
        else if(개수()!=1){Kasa_aiki_Daraja("This command takes no arguments; help system");}
        else if(Umarni==3)Nuna_Hanyar_shiga();else if(Umarni==4)Nuna_Hanyar_sadarwa();else if(Umarni==5)Nuna_Aiyuka();else if(Umarni==7)Nuna_Mahardatar_kwamfuta();else if(Umarni==8)Nuna_Wurin_adana();else if(Umarni==9)Nuna_Aiki();
        else if(Umarni==10)보드.전원끄기();
        return true;
    }
}
