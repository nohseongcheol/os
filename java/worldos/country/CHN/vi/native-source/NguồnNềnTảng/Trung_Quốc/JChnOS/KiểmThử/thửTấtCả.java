// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Trung_Quốc.JChnOS.KiểmThử;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Trung_Quốc.JChnOS.VùngNhớ.BộQuảnLýBộNhớ;
import Trung_Quốc.JChnOS.VùngNhớ.BộQuảnLýTrang;
import Trung_Quốc.JChnOS.giáTrịVào.sựKiệnĐầuVào;
import Trung_Quốc.JChnOS.TácVụ.giáTrịTiếnTrình;
import Trung_Quốc.JChnOS.LờiGọiHệThống.LờiGọiHệThống;
import Trung_Quốc.JChnOS.HệThốngTệp.BộNạpTệpThựcThi;
import Trung_Quốc.JChnOS.Nhân.Nhân;
import Trung_Quốc.JChnOS.Chủ.PhầnCứngChủ;
import Trung_Quốc.JChnOS.ngắtXửLý.BộQuảnLýNgắtXửLý;
import Trung_Quốc.JChnOS.mụcBộMôTả.BảngTraBộMôTảToànCục;
import Trung_Quốc.JChnOS.thiếtBịLưuTrữ.PhầnGắnCôngNghệNângCao;
import Trung_Quốc.JChnOS.ThiếtBị.BộQuảnLýĐườngTruyềnChungNgoạiVi;
import Trung_Quốc.JChnOS.NgănXếpMạng.CácCôngCụMạng;
import Trung_Quốc.JChnOS.NgănXếpMạng.TầngMạng;
import Trung_Quốc.JChnOS.ThiếtBị.ĐồngHồ;
import Trung_Quốc.JChnOS.mụcBộMôTả.ĐoạnVùngTrạngTháiTácVụ;
import Trung_Quốc.JChnOS.MànHình.hiểnThịKýTự;
import Trung_Quốc.JChnOS.HệThốngTệp.bảngTraPhânVùngChínhThức;

public final class thửTấtCả {
    private static int sốLượngQua;

    private thửTấtCả() {
    }

    public static void main(String[] đốiSốThamSố) {
        PhầnCứngChủ ThiếtBị = new PhầnCứngChủ();
        Nhân giáTrịNhân = new Nhân(ThiếtBị);
        giáTrịNhân.chạy();

        thửBộNhớ(giáTrịNhân);
        thửQuảnTrịTrang(giáTrịNhân);
        thửCácTiếnTrìnhVàCácTệp(giáTrịNhân);
        thửELF(giáTrịNhân);
        thửĐầuVào(giáTrịNhân);
        thửPhầnCứng(ThiếtBị);
        thửCácBộMôTảVàCácNgắt();
        thửKếtNốiMạngVàLưuTrữ();
        thửĐồngHồVàMànHình();

        System.out.println("JChnOS KiểmThử giáTrịQua: " + sốLượngQua);
    }

    private static void thửBộNhớ(Nhân giáTrịNhân) {
        BộQuảnLýBộNhớ giáTrịBộQuảnLý = giáTrịNhân.VùngNhớ();
        int địaChỉĐầuTiên = giáTrịBộQuảnLý.cấpPhátĐãCănChỉnh(100, 64);
        xácMinh((địaChỉĐầuTiên & 63) == 0, "giáTrịCănChỉnh cấpPhátLưuTrữ");
        giáTrịBộQuảnLý.ghiGiáTrịByte(địaChỉĐầuTiên, (byte) 0x5a);
        xácMinh(giáTrịBộQuảnLý.đọcGiáTrịByte(địaChỉĐầuTiên) == (byte) 0x5a, "물리 VùngNhớ 읽고 ghi");
        int dùngTrướcKhi = giáTrịBộQuảnLý.cỡĐãDùng();
        giáTrịBộQuảnLý.giảiPhóngLưuTrữ(địaChỉĐầuTiên);
        xácMinh(giáTrịBộQuảnLý.cỡĐãDùng() < dùngTrướcKhi, "VùngNhớ giảiPhóngLưuTrữ");
    }

    private static void thửQuảnTrịTrang(Nhân giáTrịNhân) {
        BộQuảnLýTrang giáTrịBộQuảnLý = giáTrịNhân.quảnTrịTrang();
        BộQuảnLýTrang.KhôngGianĐịaChỉ khôngGianCha = giáTrịBộQuảnLý.khôngGianĐịaChỉMới();
        giáTrịBộQuảnLý.trangÁnhXạ(khôngGianCha, 0x1000, true);
        giáTrịBộQuảnLý.ghiGiáTrịByte(khôngGianCha, 0x1010, (byte) 7);
        BộQuảnLýTrang.KhôngGianĐịaChỉ khôngGianCon = giáTrịBộQuảnLý.ghiBậtTrạngTháiSaoChépNhânBản(khôngGianCha);
        giáTrịBộQuảnLý.ghiGiáTrịByte(khôngGianCon, 0x1010, (byte) 9);
        xácMinh(giáTrịBộQuảnLý.đọcGiáTrịByte(khôngGianCha, 0x1010) == 7, "ghi 시 saoChépGiáTrị giáTrịCha 격리");
        xácMinh(giáTrịBộQuảnLý.đọcGiáTrịByte(khôngGianCon, 0x1010) == 9, "ghi 시 saoChépGiáTrị giáTrịCon ghi");
    }

    private static void thửCácTiếnTrìnhVàCácTệp(Nhân giáTrịNhân) {
        byte[] giáTrịNộiDung = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        giáTrịNhân.HệThốngTệp().thêmCuốiTệp("KiểmThử", giáTrịNộiDung);
        giáTrịTiếnTrình giáTrịCha = giáTrịNhân.tiếnTrìnhĐầuTiên();
        LờiGọiHệThống gọiThựcHiện = giáTrịNhân.LờiGọiHệThống();
        int mụcBộMôTả = gọiThựcHiện.mở(giáTrịCha, "/KiểmThử", LờiGọiHệThống.đọcCờChỉ);
        xácMinh(mụcBộMôTả >= 3, "Tệp mở");

        byte[] nhậnĐích = new byte[giáTrịNộiDung.length];
        xácMinh(gọiThựcHiện.đọc(giáTrịCha, mụcBộMôTả, nhậnĐích, nhậnĐích.length) == giáTrịNộiDung.length, "Tệp đọc");
        xácMinh(Arrays.equals(giáTrịNộiDung, nhậnĐích), "Tệp giáTrịNộiDung");
        xácMinh(gọiThựcHiện.vịTríDiChuyển(giáTrịCha, mụcBộMôTả, 0, LờiGọiHệThống.tìmKiếmBắtChạy) == 0, "Tệp vịTrí giáTrịDiChuyển");

        int bộMôTảĐãNhânBản = gọiThựcHiện.bộMôTảBảnSao(giáTrịCha, mụcBộMôTả);
        xácMinh(bộMôTảĐãNhânBản >= 0, "mụcBộMôTả giáTrịNhânBản");
        giáTrịTiếnTrình giáTrịCon = gọiThựcHiện.tiếnTrìnhNhânBản(giáTrịCha);
        xácMinh(giáTrịCon.giáTrịĐịnhDanh() != giáTrịCha.giáTrịĐịnhDanh(), "giáTrịTiếnTrình giáTrịĐịnhDanh 분리");
        xácMinh(giáTrịCon.địnhDanhCha() == giáTrịCha.giáTrịĐịnhDanh(), "giáTrịCha giáTrịTiếnTrình giáTrịĐịnhDanh");
        xácMinh(gọiThựcHiện.đóng(giáTrịCon, mụcBộMôTả) == 0 && giáTrịCha.bộMôTảTệp().làMở(mụcBộMôTả), "giáTrịCon đóng 격리");

        int kếtThúcTrướcĐó = gọiThựcHiện.tăngNgắtChươngTrình(giáTrịCha, 8192);
        xácMinh(kếtThúcTrướcĐó == 0x06000000, "ChươngTrình phầnKết 늘리기");
        xácMinh(giáTrịCha.ngắtChươngTrình() == 0x06002000, "ChươngTrình phầnKết 반영");
        xácMinh(giáTrịCon.ngắtChươngTrình() == 0x06000000, "과정별 ChươngTrình phầnKết 격리");

        giáTrịCon.chươngTrìnhRa(7);
        xácMinh(gọiThựcHiện.chờConCho(giáTrịCha, giáTrịCon.giáTrịĐịnhDanh(), false) == (7 << 8), "giáTrịCon chươngTrìnhRa đợi");
        xácMinh(gọiThựcHiện.làTruyCậpĐược("KiểmThử", 1) == -13, "thựcThiLệnh giáTrịQuyền từChốiGiáTrị");
        xácMinh(gọiThựcHiện.địnhDanhNgườiDùng() == 0 && gọiThựcHiện.địnhDanhNhóm() == 0, "사용자와 무리 giáTrịĐịnhDanh");
        xácMinh("/".equals(gọiThựcHiện.danhSáchTácVụHiệnTại(2)) && gọiThựcHiện.danhSáchTácVụChuyển("/") == 0, "phầnMụcHiệnTại TácVụ danhSáchMục");
        xácMinh(gọiThựcHiện.làThiếtBịCuối(giáTrịCha, 1), "표준 ĐầuRa VàoRaThiếtBịCuối");
        xácMinh("JChnOS".equals(gọiThựcHiện.cácChiTiếtHệThống().tênHệThống()), "giáTrịHệThốngĐiềuHành thôngTinHệThống");
    }

    private static void thửELF(Nhân giáTrịNhân) {
        byte[] DữLiệu = new byte[92];
        DữLiệu[0] = 0x7f;
        DữLiệu[1] = 'E';
        DữLiệu[2] = 'L';
        DữLiệu[3] = 'F';
        DữLiệu[4] = 1;
        DữLiệu[5] = 1;
        ghiGiáTrịSốNguyên(DữLiệu, 24, 0x04001000);
        ghiGiáTrịSốNguyên(DữLiệu, 32, 52);
        ghiSốNguyênNgắnKiểu(DữLiệu, 46, 40);
        ghiSốNguyênNgắnKiểu(DữLiệu, 48, 1);
        ghiGiáTrịSốNguyên(DữLiệu, 56, 8);
        ghiGiáTrịSốNguyên(DữLiệu, 60, 2);
        ghiGiáTrịSốNguyên(DữLiệu, 64, 0x04002000);
        ghiGiáTrịSốNguyên(DữLiệu, 72, 64);

        BộNạpTệpThựcThi.ảnh giáTrịẢnh = new BộNạpTệpThựcThi().CácPhépKiểmTra(DữLiệu);
        xácMinh(giáTrịẢnh.bắtChạyĐịaChỉ() == 0x04001000, "ELF chạy địaChỉ");
        xácMinh(giáTrịẢnh.danhSáchCácMụcĐoạn().size() == 1 && giáTrịẢnh.danhSáchCácMụcĐoạn().get(0).giáTrịLoại() == 8, "ELF 빈 DữLiệu giáTrịMụcĐoạn");
        int mụcBộMôTả = giáTrịNhân.LờiGọiHệThống().mở(giáTrịNhân.tiếnTrìnhĐầuTiên(), "KiểmThử", LờiGọiHệThống.đọcCờChỉ);
        xácMinh(giáTrịNhân.LờiGọiHệThống().điềuKhiểnTệp(giáTrịNhân.tiếnTrìnhĐầuTiên(), mụcBộMôTả, 2, 1) == 0, "thựcThiLệnh 시 đóng cácThiếtLập");
        xácMinh(giáTrịNhân.LờiGọiHệThống().thựcThiLệnh(giáTrịNhân.tiếnTrìnhĐầuTiên(), DữLiệu, new String[] {"KiểmThử", "값"}, new String[] {"NgônNgữ=tiếngViệt"}) == 0, "ELF thựcThiLệnh giáTrịẢnh 적재");
        xácMinh(giáTrịNhân.tiếnTrìnhĐầuTiên().địaChỉBắtChạyViệcThựcThi() == 0x04001000, "thựcThiLệnh chạy địaChỉ 반영");
        xácMinh(giáTrịNhân.tiếnTrìnhĐầuTiên().đốiSốViệcThựcThi().length == 2 && giáTrịNhân.tiếnTrìnhĐầuTiên().giáTrịMôiTrường().length == 1, "thựcThiLệnh 인자와 môiTrường");
        xácMinh(!giáTrịNhân.tiếnTrìnhĐầuTiên().bộMôTảTệp().làMở(mụcBộMôTả), "thựcThiLệnh 시 mụcBộMôTả đóng");
        xácMinh(giáTrịNhân.quảnTrịTrang().đọcGiáTrịByte(giáTrịNhân.tiếnTrìnhĐầuTiên().KhôngGianĐịaChỉ(), 0x04002000) == 0, "빈 DữLiệu giáTrịMụcĐoạn toánHạngKhôngSố khởiTạo");
    }

    private static void thửĐầuVào(Nhân giáTrịNhân) {
        giáTrịNhân.QuảnTrịĐầuVào().xuốngPhím('가');
        giáTrịNhân.QuảnTrịĐầuVào().chuyểnĐộngChuột(3, -2);
        sựKiệnĐầuVào sựKiệnĐầuTiên = giáTrịNhân.QuảnTrịĐầuVào().sựKiệnKếTiếp();
        sựKiệnĐầuVào sựKiệnThứHai = giáTrịNhân.QuảnTrịĐầuVào().sựKiệnKếTiếp();
        xácMinh(sựKiệnĐầuTiên.loạiSựKiện() == sựKiệnĐầuVào.giáTrịLoại.xuốngPhím, "자판 sựKiện");
        xácMinh(sựKiệnThứHai.giáTrịĐầuTiên() == 3 && sựKiệnThứHai.giáTrịThứHai() == -2, "쥐 giáTrịDiChuyển sựKiện");
    }

    private static void thửPhầnCứng(PhầnCứngChủ ThiếtBị) {
        ThiếtBị.ghiByteCổng(0x3f8, 0xab);
        xácMinh(ThiếtBị.đọcByteCổng(0x3f8) == 0xab, "cổngPhầnCứng đầuRaĐầuVào giáTrịRanhGiới");
        xácMinh(ThiếtBị.nhậtKýNốiTiếp().contains("JChnOS"), "giáTrịNốiTiếp bảnGhiNhậtKý");
    }

    private static void thửCácBộMôTảVàCácNgắt() {
        BộQuảnLýNgắtXửLý giáTrịBộQuảnLý = new BộQuảnLýNgắtXửLý();
        giáTrịBộQuảnLý.thanhGhiMục(0x21, địaChỉLưuTrữ -> địaChỉLưuTrữ + 4);
        giáTrịBộQuảnLý.bật();
        xácMinh(giáTrịBộQuảnLý.phânPhốiGiáTrị(0x21, 100) == 104, "ngắtXửLý phânPhốiGiáTrị");
        giáTrịBộQuảnLý.ngừngKíchHoạt();
        xácMinh(giáTrịBộQuảnLý.phânPhốiGiáTrị(0x21, 100) == 100, "ngắtXửLý ngừngKíchHoạt");

        BảngTraBộMôTảToànCục bảngTraBộMôTả = new BảngTraBộMôTảToànCục();
        bảngTraBộMôTả.đặtGiáTrịGiáTrịMặcĐịnh();
        xácMinh(bảngTraBộMôTả.danhSáchCácĐoạn().size() == 5, "전역 bảngTraBộMôTả");
        ĐoạnVùngTrạngTháiTácVụ trạngTháiTácVụ = new ĐoạnVùngTrạngTháiTácVụ();
        trạngTháiTácVụ.đặtGiáTrịNgănXếpCóĐặcQuyền(0x10, 0x800000);
        xácMinh(trạngTháiTácVụ.khốiKhôngSốNgănXếp() == 0x10 && trạngTháiTácVụ.địaChỉKhôngSốNgănXếp() == 0x800000, "TácVụ giáTrịTrạngThái giáTrịMụcĐoạn");
    }

    private static void thửKếtNốiMạngVàLưuTrữ() {
        PhầnGắnCôngNghệNângCao thiếtBịLưuTrữ = new PhầnGắnCôngNghệNângCao(4, false);
        byte[] ghiĐếnDữLiệu = new byte[PhầnGắnCôngNghệNângCao.cỡMụcĐoạn];
        byte[] đọcGiáTrịDữLiệu = new byte[PhầnGắnCôngNghệNângCao.cỡMụcĐoạn];
        ghiĐếnDữLiệu[17] = 42;
        thiếtBịLưuTrữ.ghi(2, ghiĐếnDữLiệu);
        thiếtBịLưuTrữ.đọc(2, đọcGiáTrịDữLiệu);
        xácMinh(đọcGiáTrịDữLiệu[17] == 42, "ATA giáTrịMụcĐoạn 읽고 ghi");

        BộQuảnLýĐườngTruyềnChungNgoạiVi ngoạiVi = new BộQuảnLýĐườngTruyềnChungNgoạiVi();
        ngoạiVi.giáTrịĐãPhátHiện(new BộQuảnLýĐườngTruyềnChungNgoạiVi.ThiếtBị(0x1022, 0x2000, 0xc000, 11));
        xácMinh(ngoạiVi.tìmMục(0x1022, 0x2000) != null, "주변 ThiếtBị tìmMục");

        byte[] khungEthernet = new byte[34];
        khungEthernet[12] = 0x08;
        khungEthernet[13] = 0x00;
        khungEthernet[14] = 0x45;
        xácMinh(CácCôngCụMạng.giaoThứcThượngEthernet(khungEthernet) == 0x0800, "이더넷 상위 giáTrịQuyƯớc");
        xácMinh(CácCôngCụMạng.làGiaoThức4PhiênBảnIP(khungEthernet, 14), "상호통신망규약 4판");
        xácMinh(CácCôngCụMạng.tổngKiểmLiênMạng(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 tổngKiểm");

        byte[] mụcĐoạnĐầuTiên = new byte[512];
        mụcĐoạnĐầuTiên[510] = 0x55;
        mụcĐoạnĐầuTiên[511] = (byte) 0xaa;
        mụcĐoạnĐầuTiên[450] = 0x0b;
        ghiGiáTrịSốNguyên(mụcĐoạnĐầuTiên, 454, 63);
        ghiGiáTrịSốNguyên(mụcĐoạnĐầuTiên, 458, 1024);
        xácMinh(new bảngTraPhânVùngChínhThức().đọc(mụcĐoạnĐầuTiên).size() == 1, "giáTrịMặcĐịnh 분할 영역표");

        TầngMạng giáTrịTầng = new TầngMạng();
        int[] sốLượngĐãNhận = new int[1];
        giáTrịTầng.thanhGhiĐơnVịDữLiệuNgườiDùng(7, (DữLiệu, chạy, độDài) -> sốLượngĐãNhận[0]++);
        byte[] chỉSốKhung = new byte[14 + 20 + 8];
        chỉSốKhung[12] = 0x08;
        chỉSốKhung[13] = 0x00;
        chỉSốKhung[14] = 0x45;
        chỉSốKhung[16] = 0;
        chỉSốKhung[17] = 28;
        chỉSốKhung[23] = 17;
        chỉSốKhung[36] = 0;
        chỉSốKhung[37] = 7;
        xácMinh(giáTrịTầng.nhậnEthernet(chỉSốKhung) && sốLượngĐãNhận[0] == 1, "NgườiDùng DữLiệu giáTrịĐơnVị phânPhốiGiáTrị");
    }

    private static void thửĐồngHồVàMànHình() {
        hiểnThịKýTự MànHình = new hiểnThịKýTự();
        MànHình.ĐầuRa("가나\n다");
        xácMinh(MànHình.KýTự(0, 0) == '가' && MànHình.KýTự(0, 1) == '다', "KýTự MànHình ĐầuRa");
        ĐồngHồ ĐồngHồ = new ĐồngHồ(100);
        for (int sốHiệu = 0; sốHiệu < 10; sốHiệu++) {
            ĐồngHồ.giáTrịNhịp();
        }
        xácMinh(ĐồngHồ.miliGiâyĐãTrôi() == 100, "ĐồngHồ giáTrịNhịp chuyểnĐổiGiáTrị");
    }

    private static void ghiGiáTrịSốNguyên(byte[] DữLiệu, int vịTrí, int giáTrị) {
        DữLiệu[vịTrí] = (byte) giáTrị;
        DữLiệu[vịTrí + 1] = (byte) (giáTrị >>> 8);
        DữLiệu[vịTrí + 2] = (byte) (giáTrị >>> 16);
        DữLiệu[vịTrí + 3] = (byte) (giáTrị >>> 24);
    }

    private static void ghiSốNguyênNgắnKiểu(byte[] DữLiệu, int vịTrí, int giáTrị) {
        DữLiệu[vịTrí] = (byte) giáTrị;
        DữLiệu[vịTrí + 1] = (byte) (giáTrị >>> 8);
    }

    private static void xácMinh(boolean điềuKiện, String tên) {
        if (!điềuKiện) {
            throw new AssertionError("giáTrịSựThấtBại: " + tên);
        }
        sốLượngQua++;
        System.out.println("giáTrịQua: " + tên);
    }
}
