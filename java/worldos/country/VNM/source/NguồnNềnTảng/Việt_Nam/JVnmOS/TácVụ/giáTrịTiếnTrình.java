// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Việt_Nam.JVnmOS.TácVụ;

import Việt_Nam.JVnmOS.VùngNhớ.BộQuảnLýTrang;
import Việt_Nam.JVnmOS.HệThốngTệp.bảngTraBộMôTảTệp;

public final class giáTrịTiếnTrình {
    private final int giáTrịĐịnhDanh;
    private final int địnhDanhCha;
    private final BộQuảnLýTrang.KhôngGianĐịaChỉ KhôngGianĐịaChỉ;
    private final bảngTraBộMôTảTệp bộMôTảTệp;
    private trạngTháiTiếnTrình giáTrịTrạngThái = trạngTháiTiếnTrình.chuẩnBị;
    private int mãRa;
    private int ngắtChươngTrình = 0x06000000;
    private int địaChỉBắtChạyViệcThựcThi;
    private String[] đốiSốViệcThựcThi = new String[0];
    private String[] giáTrịMôiTrường = new String[0];

    giáTrịTiếnTrình(int giáTrịĐịnhDanh, int địnhDanhCha, BộQuảnLýTrang.KhôngGianĐịaChỉ KhôngGianĐịaChỉ, bảngTraBộMôTảTệp bộMôTảTệp) {
        this.giáTrịĐịnhDanh = giáTrịĐịnhDanh;
        this.địnhDanhCha = địnhDanhCha;
        this.KhôngGianĐịaChỉ = KhôngGianĐịaChỉ;
        this.bộMôTảTệp = bộMôTảTệp;
    }

    public int giáTrịĐịnhDanh() {
        return giáTrịĐịnhDanh;
    }

    public int địnhDanhCha() {
        return địnhDanhCha;
    }

    public BộQuảnLýTrang.KhôngGianĐịaChỉ KhôngGianĐịaChỉ() {
        return KhôngGianĐịaChỉ;
    }

    public bảngTraBộMôTảTệp bộMôTảTệp() {
        return bộMôTảTệp;
    }

    public trạngTháiTiếnTrình giáTrịTrạngThái() {
        return giáTrịTrạngThái;
    }

    public void đặtGiáTrịTrạngThái(trạngTháiTiếnTrình trạngTháiMới) {
        giáTrịTrạngThái = trạngTháiMới;
    }

    public int mãRa() {
        return mãRa;
    }

    public void chươngTrìnhRa(int giáTrị) {
        mãRa = giáTrị & 0xff;
        giáTrịTrạngThái = trạngTháiTiếnTrình.chươngTrìnhRa;
    }

    public int ngắtChươngTrình() {
        return ngắtChươngTrình;
    }

    public void đặtGiáTrịNgắtChươngTrình(int kếtThúcMới) {
        if (kếtThúcMới < 0x06000000 || kếtThúcMới > 0x07000000) {
            throw new IllegalArgumentException("ChươngTrình phầnKết 범위를 벗어났습니다.");
        }
        ngắtChươngTrình = kếtThúcMới;
    }

    public void đặtGiáTrịNgữCảnhViệcThựcThi(int bắtChạyĐịaChỉ, String[] đốiSốThamSố, String[] môiTrường) {
        địaChỉBắtChạyViệcThựcThi = bắtChạyĐịaChỉ;
        đốiSốViệcThựcThi = đốiSốThamSố.clone();
        giáTrịMôiTrường = môiTrường.clone();
    }

    public int địaChỉBắtChạyViệcThựcThi() { return địaChỉBắtChạyViệcThựcThi; }
    public String[] đốiSốViệcThựcThi() { return đốiSốViệcThựcThi.clone(); }
    public String[] giáTrịMôiTrường() { return giáTrịMôiTrường.clone(); }
}
