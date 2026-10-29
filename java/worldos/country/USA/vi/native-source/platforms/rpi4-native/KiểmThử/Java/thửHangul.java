// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import tiếngViệt.tựThân.KýTự;
import tiếngViệt.tựThân.Tệp;
import tiếngViệt.tựThân.danhSáchMục;
import tiếngViệt.tựThân.TừĐiển;
import tiếngViệt.tựThân.ĐầuRa;
public class thửHangul {
    public static void main(String[] a) throws Exception {
        String LờiChào = "안녕하세요 · 日本語 · العربية · 😀";
        ĐầuRa.ghiDòng(KýTự.giảiMậtMãDữLiệu(KýTự.mãHóa(LờiChào))); ĐầuRa.ghiSố(KýTự.sốLượngĐiểmMã("한글😀"));
        Tệp.ghi("한글자료.txt", LờiChào); ĐầuRa.ghiDòng(Tệp.đọc("한글자료.txt"));
        danhSáchMục danhSáchCácTên = new danhSáchMục(); danhSáchCácTên.thêmCácGiáTrị("가람"); danhSáchCácTên.thêmCácGiáTrị("누리"); ĐầuRa.ghiDòng(danhSáchCácTên.đọc(1));
        TừĐiển giáTrịÝNghĩa = new TừĐiển(); giáTrịÝNghĩa.đặtGiáTrị("가람", "강"); System.gc(); ĐầuRa.ghiDòng(giáTrịÝNghĩa.tìmMục("가람"));
        try { KýTự.giảiMậtMãDữLiệu(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { ĐầuRa.ghiDòng("UTF-8 lỗi từChốiGiáTrị"); }
        ĐầuRa.ghiDòng("tiếngViệt thưViện làĐầyĐủ");
    }
}
