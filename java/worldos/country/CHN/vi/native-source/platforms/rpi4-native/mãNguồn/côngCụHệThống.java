// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Lệnh quản trị IPv4, ICMP, tác vụ, bộ nhớ và kho RAM đọc trạng thái thực của nhân. */
public final class côngCụHệThống {
    static int giáTrịĐịaChỉ;
    static boolean vănBảnBằng(int sốHiệu, String vănBảnTừ) { return TrìnhThôngDịchLệnh.vănBảnBằng(sốHiệu, vănBảnTừ); }
    static int sốLượngPhầnMục() { return TrìnhThôngDịchLệnh.sốLượngTừTố; }
    static void giáTrịSựThấtBại(String HướngDẫn) { TrìnhThôngDịchLệnh.kếtQuả=2; VàoRaThiếtBịCuối.ghi(HướngDẫn); VàoRaThiếtBịCuối.KýTự(10); }
    static void lỗi(int giáTrị) { TrìnhThôngDịchLệnh.lỗi(giáTrị); }
    static void mụcSố(String tên, int giáTrị) { VàoRaThiếtBịCuối.ghi(tên); VàoRaThiếtBịCuối.trịSố(giáTrị); VàoRaThiếtBịCuối.KýTự(10); }
    static int giáTrịChữSố(int sốHiệu, int giớiHạnSứcChứa) {
        if (sốHiệu>=sốLượngPhầnMục() || TrìnhThôngDịchLệnh.độDài[sốHiệu]==0) return -1;
        int giáTrị=0;
        for (int chỉSốThứBậc=0; chỉSốThứBậc<TrìnhThôngDịchLệnh.độDài[sốHiệu]; chỉSốThứBậc++) {
            int giáTrịKýTự=TrìnhThôngDịchLệnh.giáTrịTừTố[TrìnhThôngDịchLệnh.điểmĐangBắtChạy[sốHiệu]+chỉSốThứBậc]-'0';
            if (giáTrịKýTự<0 || giáTrịKýTự>9 || giáTrị>(giớiHạnSứcChứa-giáTrịKýTự)/10) return -1;
            giáTrị=giáTrị*10+giáTrịKýTự;
        }
        return giáTrị<=giớiHạnSứcChứa?giáTrị:-1;
    }
    static boolean đọcĐịaChỉ(int sốHiệu) {
        if (sốHiệu>=sốLượngPhầnMục()) return false;
        int giáTrị=0, giáTrịMảnh=0, sốLượngChữSố=0, sốLượngĐiểm=0;
        for (int chỉSốThứBậc=0; chỉSốThứBậc<TrìnhThôngDịchLệnh.độDài[sốHiệu]; chỉSốThứBậc++) {
            int giáTrịKýTự=TrìnhThôngDịchLệnh.giáTrịTừTố[TrìnhThôngDịchLệnh.điểmĐangBắtChạy[sốHiệu]+chỉSốThứBậc];
            if (giáTrịKýTự=='.') { if (sốLượngChữSố==0 || ++sốLượngĐiểm>3) return false; giáTrị=(giáTrị<<8)|giáTrịMảnh; giáTrịMảnh=sốLượngChữSố=0; }
            else { if (giáTrịKýTự<'0' || giáTrịKýTự>'9' || ++sốLượngChữSố>3) return false; giáTrịMảnh=giáTrịMảnh*10+giáTrịKýTự-'0'; if(giáTrịMảnh>255)return false; }
        }
        if (sốLượngĐiểm!=3 || sốLượngChữSố==0) return false;
        giáTrịĐịaChỉ=(giáTrị<<8)|giáTrịMảnh; return true;
    }
    static void ghiĐịaChỉ(int giáTrị) {
        VàoRaThiếtBịCuối.trịSố((giáTrị>>>24)&255); VàoRaThiếtBịCuối.KýTự('.'); VàoRaThiếtBịCuối.trịSố((giáTrị>>>16)&255); VàoRaThiếtBịCuối.KýTự('.');
        VàoRaThiếtBịCuối.trịSố((giáTrị>>>8)&255); VàoRaThiếtBịCuối.KýTự('.'); VàoRaThiếtBịCuối.trịSố(giáTrị&255);
    }
    static void hiệnTìnhTrạngMạng() {
        VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(20,0)!=0?"en0: ":"sl0: "); VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(3,0)!=0?"UP":"DOWN");
        VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(20,0)!=0?" IPv4 GENET mtu 1500":" IPv4 SLIP mtu 1500");
        VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(21,0)!=0?" LINK UP\n  inet ":" LINK DOWN\n  inet "); ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(0,0));
        VàoRaThiếtBịCuối.ghi(" netmask "); ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(1,0)); VàoRaThiếtBịCuối.ghi(" gateway "); ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(2,0)); VàoRaThiếtBịCuối.KýTự(10);
        VàoRaThiếtBịCuối.ghi("  RX packets "); VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(4,0)); VàoRaThiếtBịCuối.ghi(" bytes "); VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(6,0));
        VàoRaThiếtBịCuối.ghi(" TX packets "); VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(5,0)); VàoRaThiếtBịCuối.ghi(" bytes "); VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(7,0)); VàoRaThiếtBịCuối.KýTự(10);
        mụcSố("  dropped ",BoMạch.tìnhTrạngMạng(8,0));
    }
    static void đặtGiáTrịĐịaChỉ(int chạy) {
        if (sốLượngPhầnMục()!=chạy+3 || !đọcĐịaChỉ(chạy)) { giáTrịSựThấtBại("사용법: ipconfig set địaChỉ 주소가림 giáTrịCổngNối"); return; }
        int địaChỉ=giáTrịĐịaChỉ;
        if(!đọcĐịaChỉ(chạy+1)){giáTrịSựThấtBại("Invalid IPv4 netmask");return;} int giáTrịMặtNạ=giáTrịĐịaChỉ;
        if(!đọcĐịaChỉ(chạy+2)){giáTrịSựThấtBại("Invalid IPv4 gateway");return;}
        int kếtQuả=BoMạch.cácThiếtLậpMạng(0,địaChỉ,giáTrịMặtNạ,giáTrịĐịaChỉ);
        if(kếtQuả<0) { lỗi(kếtQuả); if(kếtQuả==-16)VàoRaThiếtBịCuối.ghi("Close sockets and stop ftpd before changing address.\n"); }
        else { VàoRaThiếtBịCuối.ghi("IPv4 configuration applied (until reboot)\n"); hiệnTìnhTrạngMạng(); }
    }
    static void lệnhMạng(boolean địaChỉIP) {
        if (sốLượngPhầnMục()==1 || sốLượngPhầnMục()==2 && (vănBảnBằng(1,"show") || vănBảnBằng(1,"addr") || vănBảnBằng(1,"address") || vănBảnBằng(1,"sl0") || vănBảnBằng(1,"en0")) || sốLượngPhầnMục()==3 && (vănBảnBằng(1,"addr") || vănBảnBằng(1,"address")) && vănBảnBằng(2,"show")) { hiệnTìnhTrạngMạng();return; }
        if (địaChỉIP && vănBảnBằng(1,"route") && (sốLượngPhầnMục()==2 || sốLượngPhầnMục()==3&&vănBảnBằng(2,"show"))) { hiệnĐườngDẫn();return; }
        if (vănBảnBằng(1,"set")) { đặtGiáTrịĐịaChỉ(2);return; }
        if (sốLượngPhầnMục()==2 && (vănBảnBằng(1,"up") || vănBảnBằng(1,"down"))) { BoMạch.cácThiếtLậpMạng(vănBảnBằng(1,"up")?1:2,0,0,0);hiệnTìnhTrạngMạng();return; }
        if (địaChỉIP && sốLượngPhầnMục()==6 && vănBảnBằng(1,"link") && vănBảnBằng(2,"set") && vănBảnBằng(3,"dev") && (vănBảnBằng(4,"sl0")||vănBảnBằng(4,"en0")) && (vănBảnBằng(5,"up") || vănBảnBằng(5,"down"))) { BoMạch.cácThiếtLậpMạng(vănBảnBằng(5,"up")?1:2,0,0,0);hiệnTìnhTrạngMạng();return; }
        giáTrịSựThấtBại("사용법: ip [addr show|route show|set địaChỉ 주소가림 giáTrịCổngNối|link set dev sl0 up|down]");
    }
    static void hiệnĐườngDẫn() {
        VàoRaThiếtBịCuối.ghi("Destination Netmask Gateway Interface\n");
        ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(0,0)&BoMạch.tìnhTrạngMạng(1,0));VàoRaThiếtBịCuối.KýTự(' ');ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(1,0));VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(20,0)!=0?" 0.0.0.0 en0\n":" 0.0.0.0 sl0\n");
        if (BoMạch.tìnhTrạngMạng(2,0)!=0) {VàoRaThiếtBịCuối.ghi("0.0.0.0 0.0.0.0 ");ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(2,0));VàoRaThiếtBịCuối.ghi(BoMạch.tìnhTrạngMạng(20,0)!=0?" en0\n":" sl0\n");}
    }
    static void hiệnMạng() {
        VàoRaThiếtBịCuối.ghi("Proto Local Remote State Queued\n");
        for(int sốHiệu=0;sốHiệu<32;sốHiệu++) {
            int loạiMụcKiểu=BoMạch.tìnhTrạngMạng(10,sốHiệu);if(loạiMụcKiểu==0)continue;
            VàoRaThiếtBịCuối.ghi(loạiMụcKiểu==1?"TCP ":"UDP ");ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(16,sốHiệu));VàoRaThiếtBịCuối.KýTự(':');VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(11,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');
            ghiĐịaChỉ(BoMạch.tìnhTrạngMạng(12,sốHiệu));VàoRaThiếtBịCuối.KýTự(':');VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(13,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');
            int giáTrịTrạngThái=BoMạch.tìnhTrạngMạng(14,sốHiệu);VàoRaThiếtBịCuối.ghi(loạiMụcKiểu==2?"DATAGRAM":giáTrịTrạngThái==1?"LISTEN":giáTrịTrạngThái==2?"ESTABLISHED":giáTrịTrạngThái==3?"CLOSE_WAIT":giáTrịTrạngThái==4?"ERROR":"UNCONNECTED");
            VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(BoMạch.tìnhTrạngMạng(15,sốHiệu));VàoRaThiếtBịCuối.KýTự(10);
        }
        VàoRaThiếtBịCuối.ghi("TCP queue: bytes; UDP queue: datagrams. IPv4 endpoints.\n");
    }
    static boolean chờTrạngThái(int miliGiây) {
        int chạy=BoMạch.miliGiây();
        while(BoMạch.miliGiây()-chạy<miliGiây) {
            if(VàoRaVỏLệnh.làTươngTác()!=0){int giáTrịKýTự=BoMạch.đọcNốiTiếp();if(giáTrịKýTự==3 || giáTrịKýTự=='q' || giáTrịKýTự=='Q' || giáTrịKýTự==27 || giáTrịKýTự==-4096)return false;}
            BoMạch.nhườngBộXửLýTrungTâm();
        }
        return true;
    }
    static void thửPhảnHồi() {
        int sốLượngSựLặp=4, giáTrịGiớiHạn=1000, giáTrịĐốiĐích=-1;
        for(int chỉSốVịTrí=1;chỉSốVịTrí<sốLượngPhầnMục();chỉSốVịTrí++) {
            if(vănBảnBằng(chỉSốVịTrí,"-c")){sốLượngSựLặp=giáTrịChữSố(++chỉSốVịTrí,100);if(sốLượngSựLặp<1){giáTrịSựThấtBại("ping: -c 1..100");return;}}
            else if(vănBảnBằng(chỉSốVịTrí,"-W")){giáTrịGiớiHạn=giáTrịChữSố(++chỉSốVịTrí,10);if(giáTrịGiớiHạn<1){giáTrịSựThấtBại("ping: -W 1..10 seconds");return;}giáTrịGiớiHạn*=1000;}
            else if(giáTrịĐốiĐích<0)giáTrịĐốiĐích=chỉSốVịTrí;else{giáTrịSựThấtBại("사용법: ping [-c sốLượngSựLặp] [-W giáTrịGiây] IPv4");return;}
        }
        if(giáTrịĐốiĐích<0 || !đọcĐịaChỉ(giáTrịĐốiĐích)){giáTrịSựThấtBại("ping: an IPv4 address is required (DNS is not configured)");return;}
        int địaChỉ=giáTrịĐịaChỉ, sốLượngĐãGửi=0, sốLượngĐãNhận=0, giáTrịTíchLũy=0, giớiHạnTốiThiểu=100000, giớiHạnTốiĐa=0;
        VàoRaThiếtBịCuối.ghi("PING ");ghiĐịaChỉ(địaChỉ);VàoRaThiếtBịCuối.ghi(" 32 ICMP bytes\n");
        boolean việcXửLýTiếpTục=true;
        for(int giáTrịThứTự=1;giáTrịThứTự<=sốLượngSựLặp && việcXửLýTiếpTục;giáTrịThứTự++) {
            int giáTrịĐãXửLý=BoMạch.gửiPhảnHồi(địaChỉ,giáTrịThứTự);
            if(giáTrịĐãXửLý<0){lỗi(giáTrịĐãXửLý);break;}sốLượngĐãGửi++;
            int chạy=BoMạch.miliGiây();
            while(BoMạch.đọcPhảnHồi(0)==-11 && BoMạch.miliGiây()-chạy<giáTrịGiớiHạn)if(!chờTrạngThái(1)){việcXửLýTiếpTục=false;break;}
            if(!việcXửLýTiếpTục)break;
            if(BoMạch.đọcPhảnHồi(0)==0){
                int giáTrịThờiGian=BoMạch.đọcPhảnHồi(1);sốLượngĐãNhận++;giáTrịTíchLũy+=giáTrịThờiGian;if(giáTrịThờiGian<giớiHạnTốiThiểu)giớiHạnTốiThiểu=giáTrịThờiGian;if(giáTrịThờiGian>giớiHạnTốiĐa)giớiHạnTốiĐa=giáTrịThờiGian;
                VàoRaThiếtBịCuối.ghi("32 bytes from ");ghiĐịaChỉ(địaChỉ);VàoRaThiếtBịCuối.ghi(" seq=");VàoRaThiếtBịCuối.trịSố(giáTrịThứTự);VàoRaThiếtBịCuối.ghi(" ttl=");VàoRaThiếtBịCuối.trịSố(BoMạch.đọcPhảnHồi(2));VàoRaThiếtBịCuối.ghi(" time=");VàoRaThiếtBịCuối.trịSố(giáTrịThờiGian);VàoRaThiếtBịCuối.ghi(" ms\n");
            }else{VàoRaThiếtBịCuối.ghi("Request timeout seq=");VàoRaThiếtBịCuối.trịSố(giáTrịThứTự);VàoRaThiếtBịCuối.KýTự(10);}
            if(giáTrịThứTự<sốLượngSựLặp)việcXửLýTiếpTục=chờTrạngThái(200);
        }
        VàoRaThiếtBịCuối.trịSố(sốLượngĐãGửi);VàoRaThiếtBịCuối.ghi(" transmitted, ");VàoRaThiếtBịCuối.trịSố(sốLượngĐãNhận);VàoRaThiếtBịCuối.ghi(" received, ");VàoRaThiếtBịCuối.trịSố(sốLượngĐãGửi==0?100:(sốLượngĐãGửi-sốLượngĐãNhận)*100/sốLượngĐãGửi);VàoRaThiếtBịCuối.ghi("% packet loss\n");
        if(sốLượngĐãNhận>0){VàoRaThiếtBịCuối.ghi("rtt min/avg/max = ");VàoRaThiếtBịCuối.trịSố(giớiHạnTốiThiểu);VàoRaThiếtBịCuối.KýTự('/');VàoRaThiếtBịCuối.trịSố(giáTrịTíchLũy/sốLượngĐãNhận);VàoRaThiếtBịCuối.KýTự('/');VàoRaThiếtBịCuối.trịSố(giớiHạnTốiĐa);VàoRaThiếtBịCuối.ghi(" ms\n");}
        TrìnhThôngDịchLệnh.kếtQuả=việcXửLýTiếpTục?(sốLượngĐãNhận==0?1:0):130;
    }
    static void hiệnHoạtĐộng() { VàoRaThiếtBịCuối.ghi("up ");VàoRaThiếtBịCuối.trịSố(BoMạch.miliGiây()/1000);VàoRaThiếtBịCuối.ghi(" seconds\n"); }
    static void hiệnBộNhớ() {
        mụcSố("ARM RAM KiB (firmware): ",BoMạch.hệThốngTruyVấn(0,0));
        mụcSố("Kernel image+BSS+stack KiB: ",BoMạch.hệThốngTruyVấn(1,0));
        int sứcChứaTổngCộng=BoMạch.hệThốngTruyVấn(2,0), sứcChứaĐãDùng=BoMạch.hệThốngTruyVấn(3,0);
        VàoRaThiếtBịCuối.ghi("AOT heap KiB total/used/free: ");VàoRaThiếtBịCuối.trịSố(sứcChứaTổngCộng);VàoRaThiếtBịCuối.KýTự('/');VàoRaThiếtBịCuối.trịSố(sứcChứaĐãDùng);VàoRaThiếtBịCuối.KýTự('/');VàoRaThiếtBịCuối.trịSố(sứcChứaTổngCộng-sứcChứaĐãDùng);VàoRaThiếtBịCuối.KýTự(10);
        mụcSố("Framebuffer KiB: ",BoMạch.hệThốngTruyVấn(4,0));
        mụcSố("EL0 arena+session reserve KiB: ",BoMạch.hệThốngTruyVấn(5,0));
        int giáTrịĐãÁnhXạ=0;for(int sốHiệu=0;sốHiệu<4;sốHiệu++)giáTrịĐãÁnhXạ+=BoMạch.hệThốngTruyVấn(22,sốHiệu);
        mụcSố("EL0 mapped KiB: ",giáTrịĐãÁnhXạ);
        VàoRaThiếtBịCuối.ghi("Heap is part of kernel BSS; reserved pools are not host free RAM.\n");
    }
    static void hiệnCácTácVụ() {
        VàoRaThiếtBịCuối.ghi("PID SLOT STATE MAPPED_KiB RUN_ms AGE_ms COMMAND\n");
        VàoRaThiếtBịCuối.ghi("1 - RUN - - ");VàoRaThiếtBịCuối.trịSố(BoMạch.miliGiây());VàoRaThiếtBịCuối.ghi(" kernel/shell\n");
        for(int sốHiệu=1;sốHiệu<3;sốHiệu++)if(BoMạch.trạngTháiTácVụ(sốHiệu)>0){VàoRaThiếtBịCuối.trịSố(sốHiệu+1);VàoRaThiếtBịCuối.ghi(" - READY 64 - - kernel-task\n");}
        for(int sốHiệu=0;sốHiệu<4;sốHiệu++){
            int giáTrịTrạngThái=BoMạch.hệThốngTruyVấn(20,sốHiệu);if(giáTrịTrạngThái==0)continue;
            VàoRaThiếtBịCuối.trịSố(BoMạch.hệThốngTruyVấn(21,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(sốHiệu);VàoRaThiếtBịCuối.ghi(giáTrịTrạngThái==1?" RUN ":" SUSPENDED ");
            VàoRaThiếtBịCuối.trịSố(BoMạch.hệThốngTruyVấn(22,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(BoMạch.hệThốngTruyVấn(24,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(BoMạch.hệThốngTruyVấn(23,sốHiệu));VàoRaThiếtBịCuối.KýTự(' ');
            for(int chỉSốVịTrí=0;chỉSốVịTrí<288;chỉSốVịTrí++){int giáTrịByte=BoMạch.hệThốngTruyVấn(25,sốHiệu+chỉSốVịTrí*4);if(giáTrịByte==0)break;BoMạch.ghiNốiTiếp(giáTrịByte);}VàoRaThiếtBịCuối.KýTự(10);
        }
    }
    static void hiệnLưuTrữ() {
        int sốLượngÔ=0, sốLượngDữLiệu=0;
        for(int sốHiệu=0;sốHiệu<CácTệpBộNhớ.sốLượngTệp;sốHiệu++)if(CácTệpBộNhớ.độDàiTên[sốHiệu]>0 || CácTệpBộNhớ.sốLượngThamChiếu[sốHiệu]>0){sốLượngÔ++;sốLượngDữLiệu+=CácTệpBộNhớ.độDài[sốHiệu];}
        VàoRaThiếtBịCuối.ghi("Filesystem Total Reserved Available Data Files Mount\nramfs ");VàoRaThiếtBịCuối.trịSố(CácTệpBộNhớ.sốLượngTệp*16384);VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(sốLượngÔ*16384);VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố((CácTệpBộNhớ.sốLượngTệp-sốLượngÔ)*16384);VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(sốLượngDữLiệu);VàoRaThiếtBịCuối.KýTự(' ');VàoRaThiếtBịCuối.trịSố(sốLượngÔ);VàoRaThiếtBịCuối.KýTự('/');VàoRaThiếtBịCuối.trịSố(CácTệpBộNhớ.sốLượngTệp);VàoRaThiếtBịCuối.ghi(" /\nBytes; each occupied slot reserves 16384 bytes. RAM only, not persistent disk.\n");
    }
    static void hiệnTìnhTrạng() {
        int sốLượngSựLặp=VàoRaVỏLệnh.làTươngTác()!=0?0:1;
        if(sốLượngPhầnMục()>1){if(sốLượngPhầnMục()!=3 || !vănBảnBằng(1,"-n") || (sốLượngSựLặp=giáTrịChữSố(2,1000))<1){giáTrịSựThấtBại("사용법: top [-n 1..1000]; q/Ctrl+C로 chươngTrìnhThoátHẳn");return;}}
        for(int giáTrịDãy=0;sốLượngSựLặp==0 || giáTrịDãy<sốLượngSựLặp;giáTrịDãy++){
            if(VàoRaVỏLệnh.làTươngTác()!=0 && sốLượngSựLặp==0)VàoRaThiếtBịCuối.ghi("\u001b[2J\u001b[H");
            hiệnHoạtĐộng();hiệnBộNhớ();hiệnCácTácVụ();
            if(sốLượngSựLặp!=0 && giáTrịDãy+1>=sốLượngSựLặp)break;
            if(!chờTrạngThái(1000))break;
        }
    }
    static String từChuẩn(int sốHiệu) {
        if(sốHiệu==0)return "ipconfig";if(sốHiệu==1)return "ip";if(sốHiệu==2)return "ping";if(sốHiệu==3)return "route";if(sốHiệu==4)return "netstat";
        if(sốHiệu==5)return "ps";if(sốHiệu==6)return "top";if(sốHiệu==7)return "free";if(sốHiệu==8)return "df";if(sốHiệu==9)return "uptime";if(sốHiệu==10)return "poweroff";return "help";
    }
    static void hiệnTrợGiúp() {
        VàoRaThiếtBịCuối.ghi("--- Network / system commands ---\n");
        for(int sốHiệu=0;sốHiệu<12;sốHiệu++){VàoRaThiếtBịCuối.ghi(từChuẩn(sốHiệu));VàoRaThiếtBịCuối.ghi(" / ");VàoRaThiếtBịCuối.ghi(LệnhQuảnTrị.vănBảnTừ(sốHiệu));VàoRaThiếtBịCuối.ghi(" : ");VàoRaThiếtBịCuối.ghi(LệnhQuảnTrị.môTả(sốHiệu));VàoRaThiếtBịCuối.KýTự(10);}
        VàoRaThiếtBịCuối.ghi("ipconfig set ADDRESS NETMASK GATEWAY | ip addr show | ip route show\n");
        VàoRaThiếtBịCuối.ghi("ip link set dev sl0 up|down | ping -c 4 -W 1 IPv4 | top -n 1\n");
        VàoRaThiếtBịCuối.ghi("ifconfig: ipconfig alias; ss: netstat alias. --network enables external QEMU SLIP.\n");
    }
    static boolean thựcThiLệnh() {
        int lệnh=-1;
        for(int sốHiệu=0;sốHiệu<12;sốHiệu++)if(vănBảnBằng(0,từChuẩn(sốHiệu)) || vănBảnBằng(0,LệnhQuảnTrị.vănBảnTừ(sốHiệu)))lệnh=sốHiệu;
        if(vănBảnBằng(0,"ifconfig"))lệnh=0;if(vănBảnBằng(0,"ss"))lệnh=4;
        if(lệnh<0)return false;
        if(lệnh==11){if(vănBảnBằng(1,"net") || vănBảnBằng(1,"system"))hiệnTrợGiúp();else if(vănBảnBằng(1,"ko") || vănBảnBằng(1,"input"))TrìnhThôngDịchLệnh.trợGiúpHangul();else TrìnhThôngDịchLệnh.hiệnTrợGiúp();return true;}
        if(lệnh==0 || lệnh==1)lệnhMạng(lệnh==1);
        else if(lệnh==2)thửPhảnHồi();
        else if(lệnh==6)hiệnTìnhTrạng();
        else if(sốLượngPhầnMục()!=1){giáTrịSựThấtBại("This command takes no arguments; help system");}
        else if(lệnh==3)hiệnĐườngDẫn();else if(lệnh==4)hiệnMạng();else if(lệnh==5)hiệnCácTácVụ();else if(lệnh==7)hiệnBộNhớ();else if(lệnh==8)hiệnLưuTrữ();else if(lệnh==9)hiệnHoạtĐộng();
        else if(lệnh==10)BoMạch.tắtNguồnĐiện();
        return true;
    }
}
