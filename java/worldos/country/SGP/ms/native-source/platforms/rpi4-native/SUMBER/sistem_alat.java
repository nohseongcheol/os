// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** sebenar_data kernel_VALUE 상태를 읽는 IPv4·ICMP·작업·Memori_VALUE·RAM repositori_akar 관리 Perintah. */
public final class sistem_alat {
    static int e_mel_VALUE;
    static boolean 같음(int INDEX, String Word_SMS) { return pentafsir_perintah.같음(INDEX, Word_SMS); }
    static int item_COUNT() { return pentafsir_perintah.token_COUNT; }
    static void kegagalan_VALUE(String README_eb81d7d9) { pentafsir_perintah.ukuran=2; 단말.Tulis(README_eb81d7d9); 단말.문자(10); }
    static void RALAT(int VALUE) { pentafsir_perintah.RALAT(VALUE); }
    static void 수항목(String Nama, int VALUE) { 단말.Tulis(Nama); 단말.수(VALUE); 단말.문자(10); }
    static int digit_VALUE(int INDEX, int 한도) {
        if (INDEX>=item_COUNT() || pentafsir_perintah.kepanjangan_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<pentafsir_perintah.kepanjangan_VALUE[INDEX]; 순번++) {
            int aksara_VALUE=pentafsir_perintah.token_VALUE[pentafsir_perintah.시작점[INDEX]+순번]-'0';
            if (aksara_VALUE<0 || aksara_VALUE>9 || VALUE>(한도-aksara_VALUE)/10) return -1;
            VALUE=VALUE*10+aksara_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=item_COUNT()) return false;
        int VALUE=0, cebis_VALUE=0, digit_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<pentafsir_perintah.kepanjangan_VALUE[INDEX]; 순번++) {
            int aksara_VALUE=pentafsir_perintah.token_VALUE[pentafsir_perintah.시작점[INDEX]+순번];
            if (aksara_VALUE=='.') { if (digit_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|cebis_VALUE; cebis_VALUE=digit_COUNT=0; }
            else { if (aksara_VALUE<'0' || aksara_VALUE>'9' || ++digit_COUNT>3) return false; cebis_VALUE=cebis_VALUE*10+aksara_VALUE-'0'; if(cebis_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || digit_COUNT==0) return false;
        e_mel_VALUE=(VALUE<<8)|cebis_VALUE; return true;
    }
    static void tulis_e_mel(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void tayang_rangkaian_status() {
        단말.Tulis(Papan.rangkaian_status(20,0)!=0?"en0: ":"sl0: "); 단말.Tulis(Papan.rangkaian_status(3,0)!=0?"UP":"DOWN");
        단말.Tulis(Papan.rangkaian_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Tulis(Papan.rangkaian_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); tulis_e_mel(Papan.rangkaian_status(0,0));
        단말.Tulis(" netmask "); tulis_e_mel(Papan.rangkaian_status(1,0)); 단말.Tulis(" gateway "); tulis_e_mel(Papan.rangkaian_status(2,0)); 단말.문자(10);
        단말.Tulis("  RX packets "); 단말.수(Papan.rangkaian_status(4,0)); 단말.Tulis(" bytes "); 단말.수(Papan.rangkaian_status(6,0));
        단말.Tulis(" TX packets "); 단말.수(Papan.rangkaian_status(5,0)); 단말.Tulis(" bytes "); 단말.수(Papan.rangkaian_status(7,0)); 단말.문자(10);
        수항목("  dropped ",Papan.rangkaian_status(8,0));
    }
    static void set_e_mel(int Jalan) {
        if (item_COUNT()!=Jalan+3 || !주소읽기(Jalan)) { kegagalan_VALUE("사용법: ipconfig set e_mel 주소가림 get_laluan_VALUE"); return; }
        int e_mel=e_mel_VALUE;
        if(!주소읽기(Jalan+1)){kegagalan_VALUE("Invalid IPv4 netmask");return;} int topeng_VALUE=e_mel_VALUE;
        if(!주소읽기(Jalan+2)){kegagalan_VALUE("Invalid IPv4 gateway");return;}
        int ukuran=Papan.rangkaian_Seting(0,e_mel,topeng_VALUE,e_mel_VALUE);
        if(ukuran<0) { RALAT(ukuran); if(ukuran==-16)단말.Tulis("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Tulis("IPv4 configuration applied (until reboot)\n"); tayang_rangkaian_status(); }
    }
    static void rangkaian_perintah(boolean alamat_IP) {
        if (item_COUNT()==1 || item_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { tayang_rangkaian_status();return; }
        if (alamat_IP && 같음(1,"route") && (item_COUNT()==2 || item_COUNT()==3&&같음(2,"show"))) { tayang_laluan();return; }
        if (같음(1,"set")) { set_e_mel(2);return; }
        if (item_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Papan.rangkaian_Seting(같음(1,"up")?1:2,0,0,0);tayang_rangkaian_status();return; }
        if (alamat_IP && item_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Papan.rangkaian_Seting(같음(5,"up")?1:2,0,0,0);tayang_rangkaian_status();return; }
        kegagalan_VALUE("사용법: ip [addr show|route show|set e_mel 주소가림 get_laluan_VALUE|link set dev sl0 up|down]");
    }
    static void tayang_laluan() {
        단말.Tulis("Destination Netmask Gateway Interface\n");
        tulis_e_mel(Papan.rangkaian_status(0,0)&Papan.rangkaian_status(1,0));단말.문자(' ');tulis_e_mel(Papan.rangkaian_status(1,0));단말.Tulis(Papan.rangkaian_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Papan.rangkaian_status(2,0)!=0) {단말.Tulis("0.0.0.0 0.0.0.0 ");tulis_e_mel(Papan.rangkaian_status(2,0));단말.Tulis(Papan.rangkaian_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void tayang_rangkaian() {
        단말.Tulis("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_bidang=Papan.rangkaian_status(10,INDEX);if(TYPE_bidang==0)continue;
            단말.Tulis(TYPE_bidang==1?"TCP ":"UDP ");tulis_e_mel(Papan.rangkaian_status(16,INDEX));단말.문자(':');단말.수(Papan.rangkaian_status(11,INDEX));단말.문자(' ');
            tulis_e_mel(Papan.rangkaian_status(12,INDEX));단말.문자(':');단말.수(Papan.rangkaian_status(13,INDEX));단말.문자(' ');
            int status_VALUE=Papan.rangkaian_status(14,INDEX);단말.Tulis(TYPE_bidang==2?"DATAGRAM":status_VALUE==1?"LISTEN":status_VALUE==2?"ESTABLISHED":status_VALUE==3?"CLOSE_WAIT":status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Papan.rangkaian_status(15,INDEX));단말.문자(10);
        }
        단말.Tulis("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean keadaan_tunggu(int 밀리초) {
        int Jalan=Papan.밀리초();
        while(Papan.밀리초()-Jalan<밀리초) {
            if(셸입출력.teknologi_maklumat_interaktif()!=0){int aksara_VALUE=Papan.직렬읽기();if(aksara_VALUE==3 || aksara_VALUE=='q' || aksara_VALUE=='Q' || aksara_VALUE==27 || aksara_VALUE==-4096)return false;}
            Papan.YIELD_CPU();
        }
        return true;
    }
    static void ujian_respons() {
        int 횟수=4, 제한=1000, sasaran=-1;
        for(int jawatan_INDEX=1;jawatan_INDEX<item_COUNT();jawatan_INDEX++) {
            if(같음(jawatan_INDEX,"-c")){횟수=digit_VALUE(++jawatan_INDEX,100);if(횟수<1){kegagalan_VALUE("ping: -c 1..100");return;}}
            else if(같음(jawatan_INDEX,"-W")){제한=digit_VALUE(++jawatan_INDEX,10);if(제한<1){kegagalan_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(sasaran<0)sasaran=jawatan_INDEX;else{kegagalan_VALUE("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(sasaran<0 || !주소읽기(sasaran)){kegagalan_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int e_mel=e_mel_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Tulis("PING ");tulis_e_mel(e_mel);단말.Tulis(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int tertib_VALUE=1;tertib_VALUE<=횟수 && 계속;tertib_VALUE++) {
            int 처리값=Papan.e_mel_respons(e_mel,tertib_VALUE);
            if(처리값<0){RALAT(처리값);break;}보낸수++;
            int Jalan=Papan.밀리초();
            while(Papan.응답읽기(0)==-11 && Papan.밀리초()-Jalan<제한)if(!keadaan_tunggu(1)){계속=false;break;}
            if(!계속)break;
            if(Papan.응답읽기(0)==0){
                int nilai_masa=Papan.응답읽기(1);RECEIVED_COUNT++;누적+=nilai_masa;if(nilai_masa<최솟값)최솟값=nilai_masa;if(nilai_masa>최댓값)최댓값=nilai_masa;
                단말.Tulis("32 bytes from ");tulis_e_mel(e_mel);단말.Tulis(" seq=");단말.수(tertib_VALUE);단말.Tulis(" ttl=");단말.수(Papan.응답읽기(2));단말.Tulis(" time=");단말.수(nilai_masa);단말.Tulis(" ms\n");
            }else{단말.Tulis("Request timeout seq=");단말.수(tertib_VALUE);단말.문자(10);}
            if(tertib_VALUE<횟수)계속=keadaan_tunggu(200);
        }
        단말.수(보낸수);단말.Tulis(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Tulis(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Tulis("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Tulis("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Tulis(" ms\n");}
        pentafsir_perintah.ukuran=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void tayang_Aktiviti() { 단말.Tulis("up ");단말.수(Papan.밀리초()/1000);단말.Tulis(" seconds\n"); }
    static void tayang_Memori() {
        수항목("ARM RAM KiB (firmware): ",Papan.pertanyaan_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Papan.pertanyaan_sistem(1,0));
        int 총량=Papan.pertanyaan_sistem(2,0), 사용량=Papan.pertanyaan_sistem(3,0);
        단말.Tulis("AOT heap KiB total/used/free: ");단말.수(총량);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(총량-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Papan.pertanyaan_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Papan.pertanyaan_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Papan.pertanyaan_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Tulis("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void tayang_Tasks() {
        단말.Tulis("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Tulis("1 - RUN - - ");단말.수(Papan.밀리초());단말.Tulis(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Papan.tugas_status(INDEX)>0){단말.수(INDEX+1);단말.Tulis(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int status_VALUE=Papan.pertanyaan_sistem(20,INDEX);if(status_VALUE==0)continue;
            단말.수(Papan.pertanyaan_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Tulis(status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Papan.pertanyaan_sistem(22,INDEX));단말.문자(' ');단말.수(Papan.pertanyaan_sistem(24,INDEX));단말.문자(' ');단말.수(Papan.pertanyaan_sistem(23,INDEX));단말.문자(' ');
            for(int jawatan_INDEX=0;jawatan_INDEX<288;jawatan_INDEX++){int bait_VALUE=Papan.pertanyaan_sistem(25,INDEX+jawatan_INDEX*4);if(bait_VALUE==0)break;Papan.직렬쓰기(bait_VALUE);}단말.문자(10);
        }
    }
    static void tayang_Storan() {
        int 칸수=0, data_COUNT=0;
        for(int INDEX=0;INDEX<Memori_Fail.fail_COUNT;INDEX++)if(Memori_Fail.이름길이[INDEX]>0 || Memori_Fail.Rujukan_COUNT[INDEX]>0){칸수++;data_COUNT+=Memori_Fail.kepanjangan_VALUE[INDEX];}
        단말.Tulis("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(Memori_Fail.fail_COUNT*16384);단말.문자(' ');단말.수(칸수*16384);단말.문자(' ');단말.수((Memori_Fail.fail_COUNT-칸수)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(칸수);단말.문자('/');단말.수(Memori_Fail.fail_COUNT);단말.Tulis(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void tayang_status_bf9821b5() {
        int 횟수=셸입출력.teknologi_maklumat_interaktif()!=0?0:1;
        if(item_COUNT()>1){if(item_COUNT()!=3 || !같음(1,"-n") || (횟수=digit_VALUE(2,1000))<1){kegagalan_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 keluar_aplikasi");return;}}
        for(int jujukan_VALUE=0;횟수==0 || jujukan_VALUE<횟수;jujukan_VALUE++){
            if(셸입출력.teknologi_maklumat_interaktif()!=0 && 횟수==0)단말.Tulis("\u001b[2J\u001b[H");
            tayang_Aktiviti();tayang_Memori();tayang_Tasks();
            if(횟수!=0 && jujukan_VALUE+1>=횟수)break;
            if(!keadaan_tunggu(1000))break;
        }
    }
    static String 표준말(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void paparkan_bantuan() {
        단말.Tulis("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Tulis(표준말(INDEX));단말.Tulis(" / ");단말.Tulis(관리명령.Word_SMS(INDEX));단말.Tulis(" : ");단말.Tulis(관리명령.설명(INDEX));단말.문자(10);}
        단말.Tulis("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Tulis("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Tulis("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean laksanakan_perintah() {
        int Perintah=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,표준말(INDEX)) || 같음(0,관리명령.Word_SMS(INDEX)))Perintah=INDEX;
        if(같음(0,"ifconfig"))Perintah=0;if(같음(0,"ss"))Perintah=4;
        if(Perintah<0)return false;
        if(Perintah==11){if(같음(1,"net") || 같음(1,"system"))paparkan_bantuan();else if(같음(1,"ko") || 같음(1,"input"))pentafsir_perintah.한글도움말();else pentafsir_perintah.paparkan_bantuan();return true;}
        if(Perintah==0 || Perintah==1)rangkaian_perintah(Perintah==1);
        else if(Perintah==2)ujian_respons();
        else if(Perintah==6)tayang_status_bf9821b5();
        else if(item_COUNT()!=1){kegagalan_VALUE("This command takes no arguments; help system");}
        else if(Perintah==3)tayang_laluan();else if(Perintah==4)tayang_rangkaian();else if(Perintah==5)tayang_Tasks();else if(Perintah==7)tayang_Memori();else if(Perintah==8)tayang_Storan();else if(Perintah==9)tayang_Aktiviti();
        else if(Perintah==10)Papan.전원끄기();
        return true;
    }
}
