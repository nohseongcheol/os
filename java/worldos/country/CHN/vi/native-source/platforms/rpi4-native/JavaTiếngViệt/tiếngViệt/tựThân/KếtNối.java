// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Điểm cuối của luồng byte TCP đã kết nối với bên đối tác. */
public final class KếtNối {
    private final java.net.Socket cầuNốiThưViệnChuẩn;
    KếtNối(java.net.Socket cầuNốiThưViệnChuẩn) { this.cầuNốiThưViệnChuẩn = cầuNốiThưViệnChuẩn; }
    public static KếtNối mở(String địaChỉ, int sốCổng) throws NgoạiLệĐầuRaĐầuVào {
        try {
            return new KếtNối(new java.net.Socket(địaChỉ, sốCổng));
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public LuồngĐầuVào giáTrịVào() throws NgoạiLệĐầuRaĐầuVào {
        try { return new LuồngĐầuVào(cầuNốiThưViệnChuẩn.getInputStream());
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public LuồngĐầuRa ĐầuRa() throws NgoạiLệĐầuRaĐầuVào {
        try { return new LuồngĐầuRa(cầuNốiThưViệnChuẩn.getOutputStream());
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void hếtGiờ(int miliGiây) throws NgoạiLệĐầuRaĐầuVào {
        try { cầuNốiThưViệnChuẩn.setSoTimeout(miliGiây);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public int sốCổng() { return cầuNốiThưViệnChuẩn.getPort(); }
    public int sốCổngCụcBộ() { return cầuNốiThưViệnChuẩn.getLocalPort(); }
    public boolean làĐãĐóng() { return cầuNốiThưViệnChuẩn.isClosed(); }
    public boolean đãKếtNối() { return cầuNốiThưViệnChuẩn.isConnected(); }
    public void đóng() throws NgoạiLệĐầuRaĐầuVào {
        try { cầuNốiThưViệnChuẩn.close();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
