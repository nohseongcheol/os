// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** aktual_data kernel_VALUE 상태를 읽는 IPv4·ICMP·작업·Memori_VALUE·RAM repositori_akar 관리 perintah. */
public final class sistem_alat {
    static int surel_VALUE;
    static boolean 같음(int INDEX, String Kata_SMS) { return PenafsirPerintah.같음(INDEX, Kata_SMS); }
    static int item_COUNT() { return PenafsirPerintah.token_COUNT; }
    static void kegagalan_VALUE(String baca_saya_eb81d7d9) { PenafsirPerintah.hasil=2; 단말.Tulis(baca_saya_eb81d7d9); 단말.문자(10); }
    static void galat(int VALUE) { PenafsirPerintah.galat(VALUE); }
    static void 수항목(String Nama_2, int VALUE) { 단말.Tulis(Nama_2); 단말.수(VALUE); 단말.문자(10); }
    static int angka_VALUE(int INDEX, int 한도) {
        if (INDEX>=item_COUNT() || PenafsirPerintah.panjang_VALUE[INDEX]==0) return -1;
        int VALUE=0;
        for (int 순번=0; 순번<PenafsirPerintah.panjang_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=PenafsirPerintah.token_VALUE[PenafsirPerintah.시작점[INDEX]+순번]-'0';
            if (karakter_VALUE<0 || karakter_VALUE>9 || VALUE>(한도-karakter_VALUE)/10) return -1;
            VALUE=VALUE*10+karakter_VALUE;
        }
        return VALUE<=한도?VALUE:-1;
    }
    static boolean 주소읽기(int INDEX) {
        if (INDEX>=item_COUNT()) return false;
        int VALUE=0, gugus_VALUE=0, angka_COUNT=0, p_COUNT=0;
        for (int 순번=0; 순번<PenafsirPerintah.panjang_VALUE[INDEX]; 순번++) {
            int karakter_VALUE=PenafsirPerintah.token_VALUE[PenafsirPerintah.시작점[INDEX]+순번];
            if (karakter_VALUE=='.') { if (angka_COUNT==0 || ++p_COUNT>3) return false; VALUE=(VALUE<<8)|gugus_VALUE; gugus_VALUE=angka_COUNT=0; }
            else { if (karakter_VALUE<'0' || karakter_VALUE>'9' || ++angka_COUNT>3) return false; gugus_VALUE=gugus_VALUE*10+karakter_VALUE-'0'; if(gugus_VALUE>255)return false; }
        }
        if (p_COUNT!=3 || angka_COUNT==0) return false;
        surel_VALUE=(VALUE<<8)|gugus_VALUE; return true;
    }
    static void tulis_surel(int VALUE) {
        단말.수((VALUE>>>24)&255); 단말.문자('.'); 단말.수((VALUE>>>16)&255); 단말.문자('.');
        단말.수((VALUE>>>8)&255); 단말.문자('.'); 단말.수(VALUE&255);
    }
    static void show_jaringan_status() {
        단말.Tulis(Papan.jaringan_status(20,0)!=0?"en0: ":"sl0: "); 단말.Tulis(Papan.jaringan_status(3,0)!=0?"UP":"DOWN");
        단말.Tulis(Papan.jaringan_status(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Tulis(Papan.jaringan_status(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); tulis_surel(Papan.jaringan_status(0,0));
        단말.Tulis(" netmask "); tulis_surel(Papan.jaringan_status(1,0)); 단말.Tulis(" gateway "); tulis_surel(Papan.jaringan_status(2,0)); 단말.문자(10);
        단말.Tulis("  RX packets "); 단말.수(Papan.jaringan_status(4,0)); 단말.Tulis(" bytes "); 단말.수(Papan.jaringan_status(6,0));
        단말.Tulis(" TX packets "); 단말.수(Papan.jaringan_status(5,0)); 단말.Tulis(" bytes "); 단말.수(Papan.jaringan_status(7,0)); 단말.문자(10);
        수항목("  dropped ",Papan.jaringan_status(8,0));
    }
    static void set_surel(int jalankan) {
        if (item_COUNT()!=jalankan+3 || !주소읽기(jalankan)) { kegagalan_VALUE("사용법: ipconfig set surel 주소가림 gateway_VALUE"); return; }
        int surel=surel_VALUE;
        if(!주소읽기(jalankan+1)){kegagalan_VALUE("Invalid IPv4 netmask");return;} int masker_VALUE=surel_VALUE;
        if(!주소읽기(jalankan+2)){kegagalan_VALUE("Invalid IPv4 gateway");return;}
        int hasil=Papan.jaringan_Pengaturan(0,surel,masker_VALUE,surel_VALUE);
        if(hasil<0) { galat(hasil); if(hasil==-16)단말.Tulis("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Tulis("IPv4 configuration applied (until reboot)\n"); show_jaringan_status(); }
    }
    static void jaringan_perintah(boolean alamat_IP) {
        if (item_COUNT()==1 || item_COUNT()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || item_COUNT()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { show_jaringan_status();return; }
        if (alamat_IP && 같음(1,"route") && (item_COUNT()==2 || item_COUNT()==3&&같음(2,"show"))) { show_jalur();return; }
        if (같음(1,"set")) { set_surel(2);return; }
        if (item_COUNT()==2 && (같음(1,"up") || 같음(1,"down"))) { Papan.jaringan_Pengaturan(같음(1,"up")?1:2,0,0,0);show_jaringan_status();return; }
        if (alamat_IP && item_COUNT()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Papan.jaringan_Pengaturan(같음(5,"up")?1:2,0,0,0);show_jaringan_status();return; }
        kegagalan_VALUE("사용법: ip [addr show|route show|set surel 주소가림 gateway_VALUE|link set dev sl0 up|down]");
    }
    static void show_jalur() {
        단말.Tulis("Destination Netmask Gateway Interface\n");
        tulis_surel(Papan.jaringan_status(0,0)&Papan.jaringan_status(1,0));단말.문자(' ');tulis_surel(Papan.jaringan_status(1,0));단말.Tulis(Papan.jaringan_status(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Papan.jaringan_status(2,0)!=0) {단말.Tulis("0.0.0.0 0.0.0.0 ");tulis_surel(Papan.jaringan_status(2,0));단말.Tulis(Papan.jaringan_status(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void show_jaringan() {
        단말.Tulis("Proto Local Remote State Queued\n");
        for(int INDEX=0;INDEX<32;INDEX++) {
            int TYPE_area=Papan.jaringan_status(10,INDEX);if(TYPE_area==0)continue;
            단말.Tulis(TYPE_area==1?"TCP ":"UDP ");tulis_surel(Papan.jaringan_status(16,INDEX));단말.문자(':');단말.수(Papan.jaringan_status(11,INDEX));단말.문자(' ');
            tulis_surel(Papan.jaringan_status(12,INDEX));단말.문자(':');단말.수(Papan.jaringan_status(13,INDEX));단말.문자(' ');
            int Status_VALUE=Papan.jaringan_status(14,INDEX);단말.Tulis(TYPE_area==2?"DATAGRAM":Status_VALUE==1?"LISTEN":Status_VALUE==2?"ESTABLISHED":Status_VALUE==3?"CLOSE_WAIT":Status_VALUE==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Papan.jaringan_status(15,INDEX));단말.문자(10);
        }
        단말.Tulis("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean tunggu_Status(int 밀리초) {
        int jalankan=Papan.밀리초();
        while(Papan.밀리초()-jalankan<밀리초) {
            if(셸입출력.teknologi_informasi_interaktif()!=0){int karakter_VALUE=Papan.직렬읽기();if(karakter_VALUE==3 || karakter_VALUE=='q' || karakter_VALUE=='Q' || karakter_VALUE==27 || karakter_VALUE==-4096)return false;}
            Papan.YIELD_CPU();
        }
        return true;
    }
    static void 응답시험() {
        int pengulangan_COUNT=4, 제한=1000, target=-1;
        for(int posisi_INDEX=1;posisi_INDEX<item_COUNT();posisi_INDEX++) {
            if(같음(posisi_INDEX,"-c")){pengulangan_COUNT=angka_VALUE(++posisi_INDEX,100);if(pengulangan_COUNT<1){kegagalan_VALUE("ping: -c 1..100");return;}}
            else if(같음(posisi_INDEX,"-W")){제한=angka_VALUE(++posisi_INDEX,10);if(제한<1){kegagalan_VALUE("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(target<0)target=posisi_INDEX;else{kegagalan_VALUE("사용법: ping [-c pengulangan_COUNT] [-W 초] IPv4");return;}
        }
        if(target<0 || !주소읽기(target)){kegagalan_VALUE("ping: an IPv4 address is required (DNS is not configured)");return;}
        int surel=surel_VALUE, 보낸수=0, RECEIVED_COUNT=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Tulis("PING ");tulis_surel(surel);단말.Tulis(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int urutan_VALUE=1;urutan_VALUE<=pengulangan_COUNT && 계속;urutan_VALUE++) {
            int 처리값=Papan.kirim_respons(surel,urutan_VALUE);
            if(처리값<0){galat(처리값);break;}보낸수++;
            int jalankan=Papan.밀리초();
            while(Papan.응답읽기(0)==-11 && Papan.밀리초()-jalankan<제한)if(!tunggu_Status(1)){계속=false;break;}
            if(!계속)break;
            if(Papan.응답읽기(0)==0){
                int TIME_VALUE=Papan.응답읽기(1);RECEIVED_COUNT++;누적+=TIME_VALUE;if(TIME_VALUE<최솟값)최솟값=TIME_VALUE;if(TIME_VALUE>최댓값)최댓값=TIME_VALUE;
                단말.Tulis("32 bytes from ");tulis_surel(surel);단말.Tulis(" seq=");단말.수(urutan_VALUE);단말.Tulis(" ttl=");단말.수(Papan.응답읽기(2));단말.Tulis(" time=");단말.수(TIME_VALUE);단말.Tulis(" ms\n");
            }else{단말.Tulis("Request timeout seq=");단말.수(urutan_VALUE);단말.문자(10);}
            if(urutan_VALUE<pengulangan_COUNT)계속=tunggu_Status(200);
        }
        단말.수(보낸수);단말.Tulis(" transmitted, ");단말.수(RECEIVED_COUNT);단말.Tulis(" received, ");단말.수(보낸수==0?100:(보낸수-RECEIVED_COUNT)*100/보낸수);단말.Tulis("% packet loss\n");
        if(RECEIVED_COUNT>0){단말.Tulis("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/RECEIVED_COUNT);단말.문자('/');단말.수(최댓값);단말.Tulis(" ms\n");}
        PenafsirPerintah.hasil=계속?(RECEIVED_COUNT==0?1:0):130;
    }
    static void show_Aktivitas() { 단말.Tulis("up ");단말.수(Papan.밀리초()/1000);단말.Tulis(" seconds\n"); }
    static void show_Memori() {
        수항목("ARM RAM KiB (firmware): ",Papan.kueri_sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Papan.kueri_sistem(1,0));
        int total_kapasitas=Papan.kueri_sistem(2,0), 사용량=Papan.kueri_sistem(3,0);
        단말.Tulis("AOT heap KiB total/used/free: ");단말.수(total_kapasitas);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(total_kapasitas-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Papan.kueri_sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Papan.kueri_sistem(5,0));
        int 매핑=0;for(int INDEX=0;INDEX<4;INDEX++)매핑+=Papan.kueri_sistem(22,INDEX);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Tulis("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void show_Tasks() {
        단말.Tulis("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Tulis("1 - RUN - - ");단말.수(Papan.밀리초());단말.Tulis(" kernel/shell\n");
        for(int INDEX=1;INDEX<3;INDEX++)if(Papan.tugas_Status(INDEX)>0){단말.수(INDEX+1);단말.Tulis(" - READY 64 - - kernel-task\n");}
        for(int INDEX=0;INDEX<4;INDEX++){
            int Status_VALUE=Papan.kueri_sistem(20,INDEX);if(Status_VALUE==0)continue;
            단말.수(Papan.kueri_sistem(21,INDEX));단말.문자(' ');단말.수(INDEX);단말.Tulis(Status_VALUE==1?" RUN ":" SUSPENDED ");
            단말.수(Papan.kueri_sistem(22,INDEX));단말.문자(' ');단말.수(Papan.kueri_sistem(24,INDEX));단말.문자(' ');단말.수(Papan.kueri_sistem(23,INDEX));단말.문자(' ');
            for(int posisi_INDEX=0;posisi_INDEX<288;posisi_INDEX++){int byte_VALUE=Papan.kueri_sistem(25,INDEX+posisi_INDEX*4);if(byte_VALUE==0)break;Papan.직렬쓰기(byte_VALUE);}단말.문자(10);
        }
    }
    static void show_Storage() {
        int slot_COUNT=0, data_COUNT=0;
        for(int INDEX=0;INDEX<BerkasMemori.file_COUNT;INDEX++)if(BerkasMemori.이름길이[INDEX]>0 || BerkasMemori.Referensi_COUNT[INDEX]>0){slot_COUNT++;data_COUNT+=BerkasMemori.panjang_VALUE[INDEX];}
        단말.Tulis("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(BerkasMemori.file_COUNT*16384);단말.문자(' ');단말.수(slot_COUNT*16384);단말.문자(' ');단말.수((BerkasMemori.file_COUNT-slot_COUNT)*16384);단말.문자(' ');단말.수(data_COUNT);단말.문자(' ');단말.수(slot_COUNT);단말.문자('/');단말.수(BerkasMemori.file_COUNT);단말.Tulis(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void show_status() {
        int pengulangan_COUNT=셸입출력.teknologi_informasi_interaktif()!=0?0:1;
        if(item_COUNT()>1){if(item_COUNT()!=3 || !같음(1,"-n") || (pengulangan_COUNT=angka_VALUE(2,1000))<1){kegagalan_VALUE("사용법: top [-n 1..1000]; q/Ctrl+C로 berhenti_apl");return;}}
        for(int urutan_VALUE_e9fa7815=0;pengulangan_COUNT==0 || urutan_VALUE_e9fa7815<pengulangan_COUNT;urutan_VALUE_e9fa7815++){
            if(셸입출력.teknologi_informasi_interaktif()!=0 && pengulangan_COUNT==0)단말.Tulis("\u001b[2J\u001b[H");
            show_Aktivitas();show_Memori();show_Tasks();
            if(pengulangan_COUNT!=0 && urutan_VALUE_e9fa7815+1>=pengulangan_COUNT)break;
            if(!tunggu_Status(1000))break;
        }
    }
    static String standar_Kata(int INDEX) {
        if(INDEX==0)return "ipconfig";if(INDEX==1)return "ip";if(INDEX==2)return "ping";if(INDEX==3)return "route";if(INDEX==4)return "netstat";
        if(INDEX==5)return "ps";if(INDEX==6)return "top";if(INDEX==7)return "free";if(INDEX==8)return "df";if(INDEX==9)return "uptime";if(INDEX==10)return "poweroff";return "help";
    }
    static void tampilkan_bantuan() {
        단말.Tulis("--- Network / system commands ---\n");
        for(int INDEX=0;INDEX<12;INDEX++){단말.Tulis(standar_Kata(INDEX));단말.Tulis(" / ");단말.Tulis(관리명령.Kata_SMS(INDEX));단말.Tulis(" : ");단말.Tulis(관리명령.설명(INDEX));단말.문자(10);}
        단말.Tulis("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Tulis("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Tulis("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean Jalankan_perintah() {
        int perintah=-1;
        for(int INDEX=0;INDEX<12;INDEX++)if(같음(0,standar_Kata(INDEX)) || 같음(0,관리명령.Kata_SMS(INDEX)))perintah=INDEX;
        if(같음(0,"ifconfig"))perintah=0;if(같음(0,"ss"))perintah=4;
        if(perintah<0)return false;
        if(perintah==11){if(같음(1,"net") || 같음(1,"system"))tampilkan_bantuan();else if(같음(1,"ko") || 같음(1,"input"))PenafsirPerintah.한글도움말();else PenafsirPerintah.tampilkan_bantuan();return true;}
        if(perintah==0 || perintah==1)jaringan_perintah(perintah==1);
        else if(perintah==2)응답시험();
        else if(perintah==6)show_status();
        else if(item_COUNT()!=1){kegagalan_VALUE("This command takes no arguments; help system");}
        else if(perintah==3)show_jalur();else if(perintah==4)show_jaringan();else if(perintah==5)show_Tasks();else if(perintah==7)show_Memori();else if(perintah==8)show_Storage();else if(perintah==9)show_Aktivitas();
        else if(perintah==10)Papan.전원끄기();
        return true;
    }
}
