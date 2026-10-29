// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Điểm cuối gửi và nhận thông điệp UDP, giữ nguyên ranh giới thông điệp. */
public final class KênhĐiệnDữLiệu {
    private final java.net.DatagramSocket điểmCuốiChuẩn;
    private KênhĐiệnDữLiệu(int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { điểmCuốiChuẩn = TruyềnThông.mở(sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static KênhĐiệnDữLiệu mở(int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return new KênhĐiệnDữLiệu(sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void gửi(String địaChỉ, int sốCổng, String DữLiệu) throws NgoạiLệĐầuRaĐầuVào {
        try { TruyềnThông.gửi(điểmCuốiChuẩn, địaChỉ, sốCổng, DữLiệu);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public String nhận() throws NgoạiLệĐầuRaĐầuVào {
        try { return TruyềnThông.nhận(điểmCuốiChuẩn);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void hếtGiờ(int miliGiây) throws NgoạiLệĐầuRaĐầuVào {
        try { TruyềnThông.hếtGiờ(điểmCuốiChuẩn, miliGiây);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public int sốCổng() { return điểmCuốiChuẩn.getLocalPort(); }
    public boolean làĐãĐóng() { return điểmCuốiChuẩn.isClosed(); }
    public void đóng() { TruyềnThông.đóng(điểmCuốiChuẩn); }
}
