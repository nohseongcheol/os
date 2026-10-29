// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eyona_yenzekileyo_iingcombolo ikheneli_ixabiso 상태를 읽는 IPv4·ICMP·작업·imemori_ixabiso·RAM 저장소 관리 Umyalelo. */
public final class inkqubo_isixhobo_sokutayipha {
    static int idilesi_ixabiso;
    static boolean 같음(int indeksa, String Igama_I_SMS) { return 명령해석기.같음(indeksa, Igama_I_SMS); }
    static int 개수() { return 명령해석기.토큰수; }
    static void ukungaphumeleli_ixabiso(String i_README_eb81d7d9) { 명령해석기.결과=2; 단말.Bhala(i_README_eb81d7d9); 단말.문자(10); }
    static void Impazamo(int ixabiso) { 명령해석기.Impazamo(ixabiso); }
    static void 수항목(String Igama, int ixabiso) { 단말.Bhala(Igama); 단말.수(ixabiso); 단말.문자(10); }
    static int inani_ixabiso(int indeksa, int 한도) {
        if (indeksa>=개수() || 명령해석기.ubude_ixabiso[indeksa]==0) return -1;
        int ixabiso=0;
        for (int 순번=0; 순번<명령해석기.ubude_ixabiso[indeksa]; 순번++) {
            int ikharakhtha_ixabiso=명령해석기.ithokeni_ixabiso[명령해석기.시작점[indeksa]+순번]-'0';
            if (ikharakhtha_ixabiso<0 || ikharakhtha_ixabiso>9 || ixabiso>(한도-ikharakhtha_ixabiso)/10) return -1;
            ixabiso=ixabiso*10+ikharakhtha_ixabiso;
        }
        return ixabiso<=한도?ixabiso:-1;
    }
    static boolean 주소읽기(int indeksa) {
        if (indeksa>=개수()) return false;
        int ixabiso=0, 덩이=0, 숫자수=0, 점수=0;
        for (int 순번=0; 순번<명령해석기.ubude_ixabiso[indeksa]; 순번++) {
            int ikharakhtha_ixabiso=명령해석기.ithokeni_ixabiso[명령해석기.시작점[indeksa]+순번];
            if (ikharakhtha_ixabiso=='.') { if (숫자수==0 || ++점수>3) return false; ixabiso=(ixabiso<<8)|덩이; 덩이=숫자수=0; }
            else { if (ikharakhtha_ixabiso<'0' || ikharakhtha_ixabiso>'9' || ++숫자수>3) return false; 덩이=덩이*10+ikharakhtha_ixabiso-'0'; if(덩이>255)return false; }
        }
        if (점수!=3 || 숫자수==0) return false;
        idilesi_ixabiso=(ixabiso<<8)|덩이; return true;
    }
    static void bhala_idilesi(int ixabiso) {
        단말.수((ixabiso>>>24)&255); 단말.문자('.'); 단말.수((ixabiso>>>16)&255); 단말.문자('.');
        단말.수((ixabiso>>>8)&255); 단말.문자('.'); 단말.수(ixabiso&255);
    }
    static void bonisa_Inethiwekhi_imo() {
        단말.Bhala(보드.Inethiwekhi_imo(20,0)!=0?"en0: ":"sl0: "); 단말.Bhala(보드.Inethiwekhi_imo(3,0)!=0?"UP":"DOWN");
        단말.Bhala(보드.Inethiwekhi_imo(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Bhala(보드.Inethiwekhi_imo(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); bhala_idilesi(보드.Inethiwekhi_imo(0,0));
        단말.Bhala(" netmask "); bhala_idilesi(보드.Inethiwekhi_imo(1,0)); 단말.Bhala(" gateway "); bhala_idilesi(보드.Inethiwekhi_imo(2,0)); 단말.문자(10);
        단말.Bhala("  RX packets "); 단말.수(보드.Inethiwekhi_imo(4,0)); 단말.Bhala(" bytes "); 단말.수(보드.Inethiwekhi_imo(6,0));
        단말.Bhala(" TX packets "); 단말.수(보드.Inethiwekhi_imo(5,0)); 단말.Bhala(" bytes "); 단말.수(보드.Inethiwekhi_imo(7,0)); 단말.문자(10);
        수항목("  dropped ",보드.Inethiwekhi_imo(8,0));
    }
    static void isethi_idilesi(int Phumeza) {
        if (개수()!=Phumeza+3 || !주소읽기(Phumeza)) { ukungaphumeleli_ixabiso("사용법: ipconfig set idilesi 주소가림 isango_lekhompyutha_ixabiso"); return; }
        int idilesi=idilesi_ixabiso;
        if(!주소읽기(Phumeza+1)){ukungaphumeleli_ixabiso("Invalid IPv4 netmask");return;} int imaskhi_ixabiso=idilesi_ixabiso;
        if(!주소읽기(Phumeza+2)){ukungaphumeleli_ixabiso("Invalid IPv4 gateway");return;}
        int 결과=보드.Inethiwekhi_Iisetingi(0,idilesi,imaskhi_ixabiso,idilesi_ixabiso);
        if(결과<0) { Impazamo(결과); if(결과==-16)단말.Bhala("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Bhala("IPv4 configuration applied (until reboot)\n"); bonisa_Inethiwekhi_imo(); }
    }
    static void Inethiwekhi_umyalelo(boolean idilesi_ye_IP) {
        if (개수()==1 || 개수()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || 개수()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { bonisa_Inethiwekhi_imo();return; }
        if (idilesi_ye_IP && 같음(1,"route") && (개수()==2 || 개수()==3&&같음(2,"show"))) { bonisa_indlela();return; }
        if (같음(1,"set")) { isethi_idilesi(2);return; }
        if (개수()==2 && (같음(1,"up") || 같음(1,"down"))) { 보드.Inethiwekhi_Iisetingi(같음(1,"up")?1:2,0,0,0);bonisa_Inethiwekhi_imo();return; }
        if (idilesi_ye_IP && 개수()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { 보드.Inethiwekhi_Iisetingi(같음(5,"up")?1:2,0,0,0);bonisa_Inethiwekhi_imo();return; }
        ukungaphumeleli_ixabiso("사용법: ip [addr show|route show|set idilesi 주소가림 isango_lekhompyutha_ixabiso|link set dev sl0 up|down]");
    }
    static void bonisa_indlela() {
        단말.Bhala("Destination Netmask Gateway Interface\n");
        bhala_idilesi(보드.Inethiwekhi_imo(0,0)&보드.Inethiwekhi_imo(1,0));단말.문자(' ');bhala_idilesi(보드.Inethiwekhi_imo(1,0));단말.Bhala(보드.Inethiwekhi_imo(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (보드.Inethiwekhi_imo(2,0)!=0) {단말.Bhala("0.0.0.0 0.0.0.0 ");bhala_idilesi(보드.Inethiwekhi_imo(2,0));단말.Bhala(보드.Inethiwekhi_imo(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void bonisa_Inethiwekhi() {
        단말.Bhala("Proto Local Remote State Queued\n");
        for(int indeksa=0;indeksa<32;indeksa++) {
            int uhlobo_udidi=보드.Inethiwekhi_imo(10,indeksa);if(uhlobo_udidi==0)continue;
            단말.Bhala(uhlobo_udidi==1?"TCP ":"UDP ");bhala_idilesi(보드.Inethiwekhi_imo(16,indeksa));단말.문자(':');단말.수(보드.Inethiwekhi_imo(11,indeksa));단말.문자(' ');
            bhala_idilesi(보드.Inethiwekhi_imo(12,indeksa));단말.문자(':');단말.수(보드.Inethiwekhi_imo(13,indeksa));단말.문자(' ');
            int imo_ixabiso=보드.Inethiwekhi_imo(14,indeksa);단말.Bhala(uhlobo_udidi==2?"DATAGRAM":imo_ixabiso==1?"LISTEN":imo_ixabiso==2?"ESTABLISHED":imo_ixabiso==3?"CLOSE_WAIT":imo_ixabiso==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(보드.Inethiwekhi_imo(15,indeksa));단말.문자(10);
        }
        단말.Bhala("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean 기다림(int 밀리초) {
        int Phumeza=보드.밀리초();
        while(보드.밀리초()-Phumeza<밀리초) {
            if(셸입출력.대화가능()!=0){int ikharakhtha_ixabiso=보드.직렬읽기();if(ikharakhtha_ixabiso==3 || ikharakhtha_ixabiso=='q' || ikharakhtha_ixabiso=='Q' || ikharakhtha_ixabiso==27 || ikharakhtha_ixabiso==-4096)return false;}
            보드.misa_okwexeshana_i_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int 횟수=4, 제한=1000, ithagethi=-1;
        for(int 자리=1;자리<개수();자리++) {
            if(같음(자리,"-c")){횟수=inani_ixabiso(++자리,100);if(횟수<1){ukungaphumeleli_ixabiso("ping: -c 1..100");return;}}
            else if(같음(자리,"-W")){제한=inani_ixabiso(++자리,10);if(제한<1){ukungaphumeleli_ixabiso("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(ithagethi<0)ithagethi=자리;else{ukungaphumeleli_ixabiso("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(ithagethi<0 || !주소읽기(ithagethi)){ukungaphumeleli_ixabiso("ping: an IPv4 address is required (DNS is not configured)");return;}
        int idilesi=idilesi_ixabiso, 보낸수=0, 받은수=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Bhala("PING ");bhala_idilesi(idilesi);단말.Bhala(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int ulandelelwano_ixabiso=1;ulandelelwano_ixabiso<=횟수 && 계속;ulandelelwano_ixabiso++) {
            int 처리값=보드.응답보내기(idilesi,ulandelelwano_ixabiso);
            if(처리값<0){Impazamo(처리값);break;}보낸수++;
            int Phumeza=보드.밀리초();
            while(보드.응답읽기(0)==-11 && 보드.밀리초()-Phumeza<제한)if(!기다림(1)){계속=false;break;}
            if(!계속)break;
            if(보드.응답읽기(0)==0){
                int 시간=보드.응답읽기(1);받은수++;누적+=시간;if(시간<최솟값)최솟값=시간;if(시간>최댓값)최댓값=시간;
                단말.Bhala("32 bytes from ");bhala_idilesi(idilesi);단말.Bhala(" seq=");단말.수(ulandelelwano_ixabiso);단말.Bhala(" ttl=");단말.수(보드.응답읽기(2));단말.Bhala(" time=");단말.수(시간);단말.Bhala(" ms\n");
            }else{단말.Bhala("Request timeout seq=");단말.수(ulandelelwano_ixabiso);단말.문자(10);}
            if(ulandelelwano_ixabiso<횟수)계속=기다림(200);
        }
        단말.수(보낸수);단말.Bhala(" transmitted, ");단말.수(받은수);단말.Bhala(" received, ");단말.수(보낸수==0?100:(보낸수-받은수)*100/보낸수);단말.Bhala("% packet loss\n");
        if(받은수>0){단말.Bhala("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/받은수);단말.문자('/');단말.수(최댓값);단말.Bhala(" ms\n");}
        명령해석기.결과=계속?(받은수==0?1:0):130;
    }
    static void bonisa_Umsebenzi() { 단말.Bhala("up ");단말.수(보드.밀리초()/1000);단말.Bhala(" seconds\n"); }
    static void bonisa_imemori() {
        수항목("ARM RAM KiB (firmware): ",보드.umbuzo_inkqubo(0,0));
        수항목("Kernel image+BSS+stack KiB: ",보드.umbuzo_inkqubo(1,0));
        int 총량=보드.umbuzo_inkqubo(2,0), 사용량=보드.umbuzo_inkqubo(3,0);
        단말.Bhala("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",보드.umbuzo_inkqubo(4,0));
        수항목("EL0 arena+session reserve KiB: ",보드.umbuzo_inkqubo(5,0));
        int 매핑=0;for(int indeksa=0;indeksa<4;indeksa++)매핑+=보드.umbuzo_inkqubo(22,indeksa);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Bhala("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void 작업보기() {
        단말.Bhala("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Bhala("1 - RUN - - ");단말.수(보드.밀리초());단말.Bhala(" kernel/shell\n");
        for(int indeksa=1;indeksa<3;indeksa++)if(보드.umsebenzi_imo(indeksa)>0){단말.수(indeksa+1);단말.Bhala(" - READY 64 - - kernel-task\n");}
        for(int indeksa=0;indeksa<4;indeksa++){
            int imo_ixabiso=보드.umbuzo_inkqubo(20,indeksa);if(imo_ixabiso==0)continue;
            단말.수(보드.umbuzo_inkqubo(21,indeksa));단말.문자(' ');단말.수(indeksa);단말.Bhala(imo_ixabiso==1?" RUN ":" SUSPENDED ");
            단말.수(보드.umbuzo_inkqubo(22,indeksa));단말.문자(' ');단말.수(보드.umbuzo_inkqubo(24,indeksa));단말.문자(' ');단말.수(보드.umbuzo_inkqubo(23,indeksa));단말.문자(' ');
            for(int 자리=0;자리<288;자리++){int ibhayithi_ixabiso=보드.umbuzo_inkqubo(25,indeksa+자리*4);if(ibhayithi_ixabiso==0)break;보드.직렬쓰기(ibhayithi_ixabiso);}단말.문자(10);
        }
    }
    static void bonisa_Ugcino() {
        int 칸수=0, 자료수=0;
        for(int indeksa=0;indeksa<imemori_Iifayile.파일수;indeksa++)if(imemori_Iifayile.이름길이[indeksa]>0 || imemori_Iifayile.참조수[indeksa]>0){칸수++;자료수+=imemori_Iifayile.ubude_ixabiso[indeksa];}
        단말.Bhala("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(imemori_Iifayile.파일수*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((imemori_Iifayile.파일수-칸수)*16384);단말.문자(' ');단말.수(자료수);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(imemori_Iifayile.파일수);단말.Bhala(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void bonisa_imo_bf9821b5() {
        int 횟수=셸입출력.대화가능()!=0?0:1;
        if(개수()>1){if(개수()!=3 || !같음(1,"-n") || (횟수=inani_ixabiso(2,1000))<1){ukungaphumeleli_ixabiso("사용법: top [-n 1..1000]; q/Ctrl+C로 끝내기");return;}}
        for(int ULANDELELWANO_ixabiso=0;횟수==0 || ULANDELELWANO_ixabiso<횟수;ULANDELELWANO_ixabiso++){
            if(셸입출력.대화가능()!=0 && 횟수==0)단말.Bhala("\u001b[2J\u001b[H");
            bonisa_Umsebenzi();bonisa_imemori();작업보기();
            if(횟수!=0 && ULANDELELWANO_ixabiso+1>=횟수)break;
            if(!기다림(1000))break;
        }
    }
    static String 표준말(int indeksa) {
        if(indeksa==0)return "ipconfig";if(indeksa==1)return "ip";if(indeksa==2)return "ping";if(indeksa==3)return "route";if(indeksa==4)return "netstat";
        if(indeksa==5)return "ps";if(indeksa==6)return "top";if(indeksa==7)return "free";if(indeksa==8)return "df";if(indeksa==9)return "uptime";if(indeksa==10)return "poweroff";return "help";
    }
    static void bonisa_uncedo() {
        단말.Bhala("--- Network / system commands ---\n");
        for(int indeksa=0;indeksa<12;indeksa++){단말.Bhala(표준말(indeksa));단말.Bhala(" / ");단말.Bhala(관리명령.Igama_I_SMS(indeksa));단말.Bhala(" : ");단말.Bhala(관리명령.설명(indeksa));단말.문자(10);}
        단말.Bhala("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Bhala("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Bhala("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean ukwenza_umyalelo() {
        int Umyalelo=-1;
        for(int indeksa=0;indeksa<12;indeksa++)if(같음(0,표준말(indeksa)) || 같음(0,관리명령.Igama_I_SMS(indeksa)))Umyalelo=indeksa;
        if(같음(0,"ifconfig"))Umyalelo=0;if(같음(0,"ss"))Umyalelo=4;
        if(Umyalelo<0)return false;
        if(Umyalelo==11){if(같음(1,"net") || 같음(1,"system"))bonisa_uncedo();else if(같음(1,"ko") || 같음(1,"input"))명령해석기.한글도움말();else 명령해석기.bonisa_uncedo();return true;}
        if(Umyalelo==0 || Umyalelo==1)Inethiwekhi_umyalelo(Umyalelo==1);
        else if(Umyalelo==2)응답시험();
        else if(Umyalelo==6)bonisa_imo_bf9821b5();
        else if(개수()!=1){ukungaphumeleli_ixabiso("This command takes no arguments; help system");}
        else if(Umyalelo==3)bonisa_indlela();else if(Umyalelo==4)bonisa_Inethiwekhi();else if(Umyalelo==5)작업보기();else if(Umyalelo==7)bonisa_imemori();else if(Umyalelo==8)bonisa_Ugcino();else if(Umyalelo==9)bonisa_Umsebenzi();
        else if(Umyalelo==10)보드.전원끄기();
        return true;
    }
}
