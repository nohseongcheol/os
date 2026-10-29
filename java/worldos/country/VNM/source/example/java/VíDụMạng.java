// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.KếtNối;
import tiếngViệt.tựThân.CácĐốiSố;
import tiếngViệt.tựThân.KênhĐiệnDữLiệu;
import tiếngViệt.tựThân.KýTự;
import tiếngViệt.tựThân.ĐầuRa;
import tiếngViệt.tựThân.CácPhépKiểmTra;
import tiếngViệt.tựThân.LuồngĐầuVào;
import tiếngViệt.tựThân.NgoạiLệĐầuRaĐầuVào;

public class VíDụMạng {
    public static void chạy() throws NgoạiLệĐầuRaĐầuVào {
        // Máy chủ: python3 CôngCụ/vọngLạiVíDụ.py --tcp-port 9000 --udp-port 9001
        KếtNối nốiKết = KếtNối.mở("10.0.2.2", KýTự.phânTíchCúPhápSốNguyên(CácĐốiSố.vănBản(0)));
        try {
            nốiKết.hếtGiờ(700);
            byte[] thôngĐiệp = KýTự.mãHóa("JAVA TCP Tiếng Việt\n");
            nốiKết.ĐầuRa().ghi(thôngĐiệp);
            LuồngĐầuVào giáTrịVào = nốiKết.giáTrịVào();
            for (int trịSố = 0; trịSố < KýTự.sốLượngByte(thôngĐiệp); trịSố++) {
                CácPhépKiểmTra.đòiHỏi(giáTrịVào.đọc() == (thôngĐiệp[trịSố] & 255), "TCP lờiĐáp 불일치");
            }
        } finally { nốiKết.đóng(); }
        KênhĐiệnDữLiệu điểmCuối = KênhĐiệnDữLiệu.mở(0);
        try {
            điểmCuối.hếtGiờ(700);
            điểmCuối.gửi("10.0.2.2", KýTự.phânTíchCúPhápSốNguyên(CácĐốiSố.vănBản(1)), "JAVA UDP Tiếng Việt");
            CácPhépKiểmTra.đòiHỏi(KýTự.vănBảnBằng(điểmCuối.nhận(), "JAVA UDP Tiếng Việt"), "UDP lờiĐáp 불일치");
        } finally { điểmCuối.đóng(); }
        ĐầuRa.ghiDòng("JAVA 네트워크 xácMinh: TCP UDP Tiếng Việt");
    }
}
