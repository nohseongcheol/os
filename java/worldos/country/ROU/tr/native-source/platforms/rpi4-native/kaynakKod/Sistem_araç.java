// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** fiili_veri çekirdek_değer 상태를 읽는 IPv4·ICMP·작업·Bellek_değer·RAM depo_kök 관리 komut. */
public final class Sistem_araç {
    static int ADRES_değer;
    static boolean 같음(int Dizin, String Word_SMS) { return KomutYorumlayıcı.같음(Dizin, Word_SMS); }
    static int öğe_BAĞ_DEĞ_SAY() { return KomutYorumlayıcı.belirteç_BAĞ_DEĞ_SAY; }
    static void hata_değer(String 안내) { KomutYorumlayıcı.sonuç=2; 단말.Yazma(안내); 단말.문자(10); }
    static void hata(int değer) { KomutYorumlayıcı.hata(değer); }
    static void 수항목(String İsim, int değer) { 단말.Yazma(İsim); 단말.수(değer); 단말.문자(10); }
    static int rakam_değer(int Dizin, int 한도) {
        if (Dizin>=öğe_BAĞ_DEĞ_SAY() || KomutYorumlayıcı.süre_değer[Dizin]==0) return -1;
        int değer=0;
        for (int 순번=0; 순번<KomutYorumlayıcı.süre_değer[Dizin]; 순번++) {
            int karakter_değer=KomutYorumlayıcı.belirteç_değer[KomutYorumlayıcı.시작점[Dizin]+순번]-'0';
            if (karakter_değer<0 || karakter_değer>9 || değer>(한도-karakter_değer)/10) return -1;
            değer=değer*10+karakter_değer;
        }
        return değer<=한도?değer:-1;
    }
    static boolean 주소읽기(int Dizin) {
        if (Dizin>=öğe_BAĞ_DEĞ_SAY()) return false;
        int değer=0, öbek_değer=0, rakam_BAĞ_DEĞ_SAY=0, puan_BAĞ_DEĞ_SAY=0;
        for (int 순번=0; 순번<KomutYorumlayıcı.süre_değer[Dizin]; 순번++) {
            int karakter_değer=KomutYorumlayıcı.belirteç_değer[KomutYorumlayıcı.시작점[Dizin]+순번];
            if (karakter_değer=='.') { if (rakam_BAĞ_DEĞ_SAY==0 || ++puan_BAĞ_DEĞ_SAY>3) return false; değer=(değer<<8)|öbek_değer; öbek_değer=rakam_BAĞ_DEĞ_SAY=0; }
            else { if (karakter_değer<'0' || karakter_değer>'9' || ++rakam_BAĞ_DEĞ_SAY>3) return false; öbek_değer=öbek_değer*10+karakter_değer-'0'; if(öbek_değer>255)return false; }
        }
        if (puan_BAĞ_DEĞ_SAY!=3 || rakam_BAĞ_DEĞ_SAY==0) return false;
        ADRES_değer=(değer<<8)|öbek_değer; return true;
    }
    static void yazma_ADRES(int değer) {
        단말.수((değer>>>24)&255); 단말.문자('.'); 단말.수((değer>>>16)&255); 단말.문자('.');
        단말.수((değer>>>8)&255); 단말.문자('.'); 단말.수(değer&255);
    }
    static void şov_ağ_Durum() {
        단말.Yazma(Pano.ağ_Durum(20,0)!=0?"en0: ":"sl0: "); 단말.Yazma(Pano.ağ_Durum(3,0)!=0?"UP":"DOWN");
        단말.Yazma(Pano.ağ_Durum(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        단말.Yazma(Pano.ağ_Durum(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); yazma_ADRES(Pano.ağ_Durum(0,0));
        단말.Yazma(" netmask "); yazma_ADRES(Pano.ağ_Durum(1,0)); 단말.Yazma(" gateway "); yazma_ADRES(Pano.ağ_Durum(2,0)); 단말.문자(10);
        단말.Yazma("  RX packets "); 단말.수(Pano.ağ_Durum(4,0)); 단말.Yazma(" bytes "); 단말.수(Pano.ağ_Durum(6,0));
        단말.Yazma(" TX packets "); 단말.수(Pano.ağ_Durum(5,0)); 단말.Yazma(" bytes "); 단말.수(Pano.ağ_Durum(7,0)); 단말.문자(10);
        수항목("  dropped ",Pano.ağ_Durum(8,0));
    }
    static void küme_ADRES(int çalıştır) {
        if (öğe_BAĞ_DEĞ_SAY()!=çalıştır+3 || !주소읽기(çalıştır)) { hata_değer("사용법: ipconfig set ADRES 주소가림 ağ_geçidi_değer"); return; }
        int ADRES=ADRES_değer;
        if(!주소읽기(çalıştır+1)){hata_değer("Invalid IPv4 netmask");return;} int maske_değer=ADRES_değer;
        if(!주소읽기(çalıştır+2)){hata_değer("Invalid IPv4 gateway");return;}
        int sonuç=Pano.ağ_Ayarlar(0,ADRES,maske_değer,ADRES_değer);
        if(sonuç<0) { hata(sonuç); if(sonuç==-16)단말.Yazma("Close sockets and stop ftpd before changing address.\n"); }
        else { 단말.Yazma("IPv4 configuration applied (until reboot)\n"); şov_ağ_Durum(); }
    }
    static void ağ_komut(boolean IP_adresi) {
        if (öğe_BAĞ_DEĞ_SAY()==1 || öğe_BAĞ_DEĞ_SAY()==2 && (같음(1,"show") || 같음(1,"addr") || 같음(1,"address") || 같음(1,"sl0") || 같음(1,"en0")) || öğe_BAĞ_DEĞ_SAY()==3 && (같음(1,"addr") || 같음(1,"address")) && 같음(2,"show")) { şov_ağ_Durum();return; }
        if (IP_adresi && 같음(1,"route") && (öğe_BAĞ_DEĞ_SAY()==2 || öğe_BAĞ_DEĞ_SAY()==3&&같음(2,"show"))) { şov_yol();return; }
        if (같음(1,"set")) { küme_ADRES(2);return; }
        if (öğe_BAĞ_DEĞ_SAY()==2 && (같음(1,"up") || 같음(1,"down"))) { Pano.ağ_Ayarlar(같음(1,"up")?1:2,0,0,0);şov_ağ_Durum();return; }
        if (IP_adresi && öğe_BAĞ_DEĞ_SAY()==6 && 같음(1,"link") && 같음(2,"set") && 같음(3,"dev") && (같음(4,"sl0")||같음(4,"en0")) && (같음(5,"up") || 같음(5,"down"))) { Pano.ağ_Ayarlar(같음(5,"up")?1:2,0,0,0);şov_ağ_Durum();return; }
        hata_değer("사용법: ip [addr show|route show|set ADRES 주소가림 ağ_geçidi_değer|link set dev sl0 up|down]");
    }
    static void şov_yol() {
        단말.Yazma("Destination Netmask Gateway Interface\n");
        yazma_ADRES(Pano.ağ_Durum(0,0)&Pano.ağ_Durum(1,0));단말.문자(' ');yazma_ADRES(Pano.ağ_Durum(1,0));단말.Yazma(Pano.ağ_Durum(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (Pano.ağ_Durum(2,0)!=0) {단말.Yazma("0.0.0.0 0.0.0.0 ");yazma_ADRES(Pano.ağ_Durum(2,0));단말.Yazma(Pano.ağ_Durum(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void şov_ağ() {
        단말.Yazma("Proto Local Remote State Queued\n");
        for(int Dizin=0;Dizin<32;Dizin++) {
            int TÜR_alan=Pano.ağ_Durum(10,Dizin);if(TÜR_alan==0)continue;
            단말.Yazma(TÜR_alan==1?"TCP ":"UDP ");yazma_ADRES(Pano.ağ_Durum(16,Dizin));단말.문자(':');단말.수(Pano.ağ_Durum(11,Dizin));단말.문자(' ');
            yazma_ADRES(Pano.ağ_Durum(12,Dizin));단말.문자(':');단말.수(Pano.ağ_Durum(13,Dizin));단말.문자(' ');
            int Durum_değer=Pano.ağ_Durum(14,Dizin);단말.Yazma(TÜR_alan==2?"DATAGRAM":Durum_değer==1?"LISTEN":Durum_değer==2?"ESTABLISHED":Durum_değer==3?"CLOSE_WAIT":Durum_değer==4?"ERROR":"UNCONNECTED");
            단말.문자(' ');단말.수(Pano.ağ_Durum(15,Dizin));단말.문자(10);
        }
        단말.Yazma("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean bekleme_durumu(int 밀리초) {
        int çalıştır=Pano.밀리초();
        while(Pano.밀리초()-çalıştır<밀리초) {
            if(셸입출력.bilgi_teknolojisi_devralmak()!=0){int karakter_değer=Pano.직렬읽기();if(karakter_değer==3 || karakter_değer=='q' || karakter_değer=='Q' || karakter_değer==27 || karakter_değer==-4096)return false;}
            Pano.ÖDEME_CPU();
        }
        return true;
    }
    static void test_cevap() {
        int 횟수=4, 제한=1000, hedef=-1;
        for(int konum_dizini=1;konum_dizini<öğe_BAĞ_DEĞ_SAY();konum_dizini++) {
            if(같음(konum_dizini,"-c")){횟수=rakam_değer(++konum_dizini,100);if(횟수<1){hata_değer("ping: -c 1..100");return;}}
            else if(같음(konum_dizini,"-W")){제한=rakam_değer(++konum_dizini,10);if(제한<1){hata_değer("ping: -W 1..10 seconds");return;}제한*=1000;}
            else if(hedef<0)hedef=konum_dizini;else{hata_değer("사용법: ping [-c 횟수] [-W 초] IPv4");return;}
        }
        if(hedef<0 || !주소읽기(hedef)){hata_değer("ping: an IPv4 address is required (DNS is not configured)");return;}
        int ADRES=ADRES_değer, 보낸수=0, GETİRİ_BAĞ_DEĞ_SAY=0, 누적=0, 최솟값=100000, 최댓값=0;
        단말.Yazma("PING ");yazma_ADRES(ADRES);단말.Yazma(" 32 ICMP bytes\n");
        boolean 계속=true;
        for(int düzen_değer=1;düzen_değer<=횟수 && 계속;düzen_değer++) {
            int 처리값=Pano.göndermek_cevap(ADRES,düzen_değer);
            if(처리값<0){hata(처리값);break;}보낸수++;
            int çalıştır=Pano.밀리초();
            while(Pano.응답읽기(0)==-11 && Pano.밀리초()-çalıştır<제한)if(!bekleme_durumu(1)){계속=false;break;}
            if(!계속)break;
            if(Pano.응답읽기(0)==0){
                int zaman_değeri=Pano.응답읽기(1);GETİRİ_BAĞ_DEĞ_SAY++;누적+=zaman_değeri;if(zaman_değeri<최솟값)최솟값=zaman_değeri;if(zaman_değeri>최댓값)최댓값=zaman_değeri;
                단말.Yazma("32 bytes from ");yazma_ADRES(ADRES);단말.Yazma(" seq=");단말.수(düzen_değer);단말.Yazma(" ttl=");단말.수(Pano.응답읽기(2));단말.Yazma(" time=");단말.수(zaman_değeri);단말.Yazma(" ms\n");
            }else{단말.Yazma("Request timeout seq=");단말.수(düzen_değer);단말.문자(10);}
            if(düzen_değer<횟수)계속=bekleme_durumu(200);
        }
        단말.수(보낸수);단말.Yazma(" transmitted, ");단말.수(GETİRİ_BAĞ_DEĞ_SAY);단말.Yazma(" received, ");단말.수(보낸수==0?100:(보낸수-GETİRİ_BAĞ_DEĞ_SAY)*100/보낸수);단말.Yazma("% packet loss\n");
        if(GETİRİ_BAĞ_DEĞ_SAY>0){단말.Yazma("rtt min/avg/max = ");단말.수(최솟값);단말.문자('/');단말.수(누적/GETİRİ_BAĞ_DEĞ_SAY);단말.문자('/');단말.수(최댓값);단말.Yazma(" ms\n");}
        KomutYorumlayıcı.sonuç=계속?(GETİRİ_BAĞ_DEĞ_SAY==0?1:0):130;
    }
    static void şov_Etkinlik() { 단말.Yazma("up ");단말.수(Pano.밀리초()/1000);단말.Yazma(" seconds\n"); }
    static void şov_Bellek() {
        수항목("ARM RAM KiB (firmware): ",Pano.sorgu_Sistem(0,0));
        수항목("Kernel image+BSS+stack KiB: ",Pano.sorgu_Sistem(1,0));
        int toplam_kapasite=Pano.sorgu_Sistem(2,0), 사용량=Pano.sorgu_Sistem(3,0);
        단말.Yazma("AOT heap KiB total/used/free: ");단말.수(toplam_kapasite);단말.문자('/');단말.수(사용량);단말.문자('/');단말.수(toplam_kapasite-사용량);단말.문자(10);
        수항목("Framebuffer KiB: ",Pano.sorgu_Sistem(4,0));
        수항목("EL0 arena+session reserve KiB: ",Pano.sorgu_Sistem(5,0));
        int 매핑=0;for(int Dizin=0;Dizin<4;Dizin++)매핑+=Pano.sorgu_Sistem(22,Dizin);
        수항목("EL0 mapped KiB: ",매핑);
        단말.Yazma("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void şov_Tasks() {
        단말.Yazma("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        단말.Yazma("1 - RUN - - ");단말.수(Pano.밀리초());단말.Yazma(" kernel/shell\n");
        for(int Dizin=1;Dizin<3;Dizin++)if(Pano.Görev_Durum(Dizin)>0){단말.수(Dizin+1);단말.Yazma(" - READY 64 - - kernel-task\n");}
        for(int Dizin=0;Dizin<4;Dizin++){
            int Durum_değer=Pano.sorgu_Sistem(20,Dizin);if(Durum_değer==0)continue;
            단말.수(Pano.sorgu_Sistem(21,Dizin));단말.문자(' ');단말.수(Dizin);단말.Yazma(Durum_değer==1?" RUN ":" SUSPENDED ");
            단말.수(Pano.sorgu_Sistem(22,Dizin));단말.문자(' ');단말.수(Pano.sorgu_Sistem(24,Dizin));단말.문자(' ');단말.수(Pano.sorgu_Sistem(23,Dizin));단말.문자(' ');
            for(int konum_dizini=0;konum_dizini<288;konum_dizini++){int bayt_değer=Pano.sorgu_Sistem(25,Dizin+konum_dizini*4);if(bayt_değer==0)break;Pano.직렬쓰기(bayt_değer);}단말.문자(10);
        }
    }
    static void şov_Depolama() {
        int yuva_BAĞ_DEĞ_SAY=0, veri_BAĞ_DEĞ_SAY=0;
        for(int Dizin=0;Dizin<BellekDosyaları.Dosya_BAĞ_DEĞ_SAY;Dizin++)if(BellekDosyaları.이름길이[Dizin]>0 || BellekDosyaları.Başvuru_BAĞ_DEĞ_SAY[Dizin]>0){yuva_BAĞ_DEĞ_SAY++;veri_BAĞ_DEĞ_SAY+=BellekDosyaları.süre_değer[Dizin];}
        단말.Yazma("Filesystem Total Reserved Available Data Files Mount\nramfs ");단말.수(BellekDosyaları.Dosya_BAĞ_DEĞ_SAY*16384);단말.문자(' ');단말.수(yuva_BAĞ_DEĞ_SAY*16384);단말.문자(' ');단말.수((BellekDosyaları.Dosya_BAĞ_DEĞ_SAY-yuva_BAĞ_DEĞ_SAY)*16384);단말.문자(' ');단말.수(veri_BAĞ_DEĞ_SAY);단말.문자(' ');단말.수(yuva_BAĞ_DEĞ_SAY);단말.문자('/');단말.수(BellekDosyaları.Dosya_BAĞ_DEĞ_SAY);단말.Yazma(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void şov_Durum_bf9821b5() {
        int 횟수=셸입출력.bilgi_teknolojisi_devralmak()!=0?0:1;
        if(öğe_BAĞ_DEĞ_SAY()>1){if(öğe_BAĞ_DEĞ_SAY()!=3 || !같음(1,"-n") || (횟수=rakam_değer(2,1000))<1){hata_değer("사용법: top [-n 1..1000]; q/Ctrl+C로 çıkış_program");return;}}
        for(int dizi_değer=0;횟수==0 || dizi_değer<횟수;dizi_değer++){
            if(셸입출력.bilgi_teknolojisi_devralmak()!=0 && 횟수==0)단말.Yazma("\u001b[2J\u001b[H");
            şov_Etkinlik();şov_Bellek();şov_Tasks();
            if(횟수!=0 && dizi_değer+1>=횟수)break;
            if(!bekleme_durumu(1000))break;
        }
    }
    static String Standart_Word(int Dizin) {
        if(Dizin==0)return "ipconfig";if(Dizin==1)return "ip";if(Dizin==2)return "ping";if(Dizin==3)return "route";if(Dizin==4)return "netstat";
        if(Dizin==5)return "ps";if(Dizin==6)return "top";if(Dizin==7)return "free";if(Dizin==8)return "df";if(Dizin==9)return "uptime";if(Dizin==10)return "poweroff";return "help";
    }
    static void yardım_göster() {
        단말.Yazma("--- Network / system commands ---\n");
        for(int Dizin=0;Dizin<12;Dizin++){단말.Yazma(Standart_Word(Dizin));단말.Yazma(" / ");단말.Yazma(관리명령.Word_SMS(Dizin));단말.Yazma(" : ");단말.Yazma(관리명령.설명(Dizin));단말.문자(10);}
        단말.Yazma("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        단말.Yazma("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        단말.Yazma("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean yürütmek_komut() {
        int komut=-1;
        for(int Dizin=0;Dizin<12;Dizin++)if(같음(0,Standart_Word(Dizin)) || 같음(0,관리명령.Word_SMS(Dizin)))komut=Dizin;
        if(같음(0,"ifconfig"))komut=0;if(같음(0,"ss"))komut=4;
        if(komut<0)return false;
        if(komut==11){if(같음(1,"net") || 같음(1,"system"))yardım_göster();else if(같음(1,"ko") || 같음(1,"input"))KomutYorumlayıcı.한글도움말();else KomutYorumlayıcı.yardım_göster();return true;}
        if(komut==0 || komut==1)ağ_komut(komut==1);
        else if(komut==2)test_cevap();
        else if(komut==6)şov_Durum_bf9821b5();
        else if(öğe_BAĞ_DEĞ_SAY()!=1){hata_değer("This command takes no arguments; help system");}
        else if(komut==3)şov_yol();else if(komut==4)şov_ağ();else if(komut==5)şov_Tasks();else if(komut==7)şov_Bellek();else if(komut==8)şov_Depolama();else if(komut==9)şov_Etkinlik();
        else if(komut==10)Pano.전원끄기();
        return true;
    }
}
