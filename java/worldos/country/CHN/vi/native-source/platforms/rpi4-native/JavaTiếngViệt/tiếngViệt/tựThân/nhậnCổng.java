// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Tiếp nhận kết nối TCP đến. */
public final class nhậnCổng {
    private final java.net.ServerSocket cổngChuẩn;
    private nhậnCổng(int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { cổngChuẩn = new java.net.ServerSocket(sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static nhậnCổng mở(int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return new nhậnCổng(sốCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public KếtNối nhận() throws NgoạiLệĐầuRaĐầuVào {
        try { return new KếtNối(cổngChuẩn.accept());
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public int sốCổng() { return cổngChuẩn.getLocalPort(); }
    public void hếtGiờ(int miliGiây) throws NgoạiLệĐầuRaĐầuVào {
        try { cổngChuẩn.setSoTimeout(miliGiây);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public boolean làĐãĐóng() { return cổngChuẩn.isClosed(); }
    public void đóng() throws NgoạiLệĐầuRaĐầuVào {
        try { cổngChuẩn.close();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
