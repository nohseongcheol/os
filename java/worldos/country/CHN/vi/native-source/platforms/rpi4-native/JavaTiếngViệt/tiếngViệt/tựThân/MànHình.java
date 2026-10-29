// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Bộ đệm khung hình RGB32 của nhân độc lập, với kích thước chọn lúc khởi động. */
public final class MànHình {
    private MànHình() {}
    public static int giáTrịRộng() { int giáTrị = giáTrịNhân.rộngMànHình(); if (giáTrị < 0) throw new NgoạiLệTrạngThái("Không có bộ đệm hình"); return giáTrị; }
    public static int giáTrịCao() { int giáTrị = giáTrịNhân.caoMànHình(); if (giáTrị < 0) throw new NgoạiLệTrạngThái("Không có bộ đệm hình"); return giáTrị; }
    public static void hìnhChữNhật(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao, int giáTrịMàu) {
        if (vịTríNgang < 0 || vịTríDọc < 0 || khoảngTrảiRộng < 0 || giáTrịCao < 0 || vịTríNgang > giáTrịRộng() || vịTríDọc > giáTrịCao() || khoảngTrảiRộng > giáTrịRộng() - vịTríNgang || giáTrịCao > giáTrịCao() - vịTríDọc) throw new NgoạiLệĐốiSốKhôngHợpLệ("Phạm vi màn hình");
        if (giáTrịNhân.hìnhChữNhật(vịTríNgang, vịTríDọc, khoảngTrảiRộng, giáTrịCao, giáTrịMàu) < 0) throw new NgoạiLệTrạngThái("Không có bộ đệm hình");
    }
    public static void xóaMục(int giáTrịMàu) { hìnhChữNhật(0, 0, giáTrịRộng(), giáTrịCao(), giáTrịMàu); }
    public static void đợi() { if (giáTrịNhân.chờẢnhCho() < 0) throw new NgoạiLệTrạngThái("Cần nhập tương tác"); }
}
