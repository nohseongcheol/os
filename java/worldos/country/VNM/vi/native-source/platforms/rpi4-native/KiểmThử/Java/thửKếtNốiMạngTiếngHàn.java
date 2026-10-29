// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.*;

/** Kiểm thử giao ước truyền thông bằng cùng mã byte trên OpenJDK và JVM tự xây dựng. */
public class thửKếtNốiMạngTiếngHàn {
    public static void main(String[] cácĐốiSố) throws NgoạiLệĐầuRaĐầuVào {
        nhậnCổng giáTrịCổng = vậnChuyểnKếtNối.mởBộNhận(0);
        KếtNối giáTrịKhách = vậnChuyểnKếtNối.mở("127.0.0.1", giáTrịCổng.sốCổng());
        KếtNối địnhDanhChủSởHữu = giáTrịCổng.nhận();
        giáTrịKhách.hếtGiờ(200); địnhDanhChủSởHữu.hếtGiờ(200);
        CácPhépKiểmTra.đòiHỏi(giáTrịKhách.đãKếtNối() && !giáTrịKhách.làĐãĐóng(), "nốiKết giáTrịTrạngThái");
        CácPhépKiểmTra.đòiHỏi(địnhDanhChủSởHữu.sốCổng() == giáTrịKhách.sốCổngCụcBộ(), "giáTrịĐốiTác sốCổng");
        CácPhépKiểmTra.đòiHỏi(giáTrịKhách.sốCổng() == địnhDanhChủSởHữu.sốCổngCụcBộ(), "phạmViCụcBộ sốCổng");
        LuồngĐầuVào giáTrịVào = địnhDanhChủSởHữu.giáTrịVào(); LuồngĐầuRa trangĐầuRa = giáTrịKhách.ĐầuRa();
        byte[] thôngĐiệp = KýTự.mãHóa("한글 giáTrịLuồng");
        trangĐầuRa.ghi(thôngĐiệp, 0, thôngĐiệp.length); trangĐầuRa.phátGiáTrị();
        byte[] vănBảnĐãNhận = new byte[thôngĐiệp.length];
        int đọcSốLượng = 0;
        while (đọcSốLượng < vănBảnĐãNhận.length) {
            int đọcBổSung = giáTrịVào.đọc(vănBảnĐãNhận, đọcSốLượng, vănBảnĐãNhận.length - đọcSốLượng);
            CácPhépKiểmTra.đòiHỏi(đọcBổSung > 0, "예상하지 않은 Tệp phầnKết"); đọcSốLượng += đọcBổSung;
        }
        CácPhépKiểmTra.đòiHỏi(KýTự.vănBảnBằng(KýTự.giảiMậtMãDữLiệu(vănBảnĐãNhận), "한글 giáTrịLuồng"), "giáTrịPhầnCon 읽기와 ghi");
        trangĐầuRa.ghi(new byte[] {17, 18});
        byte[] đọcNgắnKiểu = new byte[2];
        int đọcĐầuTiên = giáTrịVào.đọc(đọcNgắnKiểu);
        CácPhépKiểmTra.đòiHỏi(đọcĐầuTiên > 0 && đọcNgắnKiểu[0] == 17, "giáTrịMảng đọc");
        if (đọcĐầuTiên == 1) đọcNgắnKiểu[1] = (byte)giáTrịVào.đọc();
        CácPhépKiểmTra.đòiHỏi(đọcNgắnKiểu[1] == 18, "giáTrịSốDư đọc");
        địnhDanhChủSởHữu.ĐầuRa().ghi(255);
        CácPhépKiểmTra.đòiHỏi(giáTrịKhách.giáTrịVào().đọc() == 255, "giáTrịBảngMã 없는 한 giáTrịByte");
        trangĐầuRa.đóng();
        CácPhépKiểmTra.đòiHỏi(giáTrịKhách.làĐãĐóng() && giáTrịVào.đọc() == -1, "닫기와 Tệp phầnKết");
        giáTrịVào.đóng(); CácPhépKiểmTra.đòiHỏi(địnhDanhChủSởHữu.làĐãĐóng(), "giáTrịVào giáTrịLuồng đóng");
        giáTrịKhách.đóng(); địnhDanhChủSởHữu.đóng();
        giáTrịCổng.hếtGiờ(15);
        boolean hếtGiờViệcThựcThi = false;
        try { giáTrịCổng.nhận(); } catch (NgoạiLệHếtGiờChờ lỗiDựKiến) { hếtGiờViệcThựcThi = true; }
        CácPhépKiểmTra.đòiHỏi(hếtGiờViệcThựcThi, "nhậnGiáTrị hếtGiờ");
        giáTrịCổng.đóng(); CácPhépKiểmTra.đòiHỏi(giáTrịCổng.làĐãĐóng(), "nhậnCổng đóng");
        KênhĐiệnDữLiệu điểmCuốiBộNhận = KênhĐiệnDữLiệu.mở(0), điểmCuốiĐangGửi = KênhĐiệnDữLiệu.mở(0);
        điểmCuốiBộNhận.hếtGiờ(200);
        điểmCuốiĐangGửi.gửi("127.0.0.1", điểmCuốiBộNhận.sốCổng(), "điệnDữLiệu 한글");
        CácPhépKiểmTra.đòiHỏi(KýTự.vănBảnBằng(điểmCuốiBộNhận.nhận(), "điệnDữLiệu 한글"), "điệnDữLiệu 송수신");
        điểmCuốiĐangGửi.đóng(); điểmCuốiBộNhận.đóng();
        CácPhépKiểmTra.đòiHỏi(điểmCuốiĐangGửi.làĐãĐóng() && điểmCuốiBộNhận.làĐãĐóng(), "điệnDữLiệu đóng");
        ĐầuRa.ghiDòng("tiếngViệt TruyềnThông xácMinh: nốiKết điệnDữLiệu giáTrịLuồng hếtGiờViệcThựcThi đóng");
    }
}
