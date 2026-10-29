// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Kênh ghi các byte đi ra theo đúng thứ tự. */
public final class LuồngĐầuRa {
    private final java.io.OutputStream luồngChuẩn;
    LuồngĐầuRa(java.io.OutputStream luồngChuẩn) { this.luồngChuẩn = luồngChuẩn; }
    public void ghi(int giáTrị) throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.write(giáTrị);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void ghi(byte[] DữLiệu) throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.write(DữLiệu);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void ghi(byte[] DữLiệu, int chạy, int độDài) throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.write(DữLiệu, chạy, độDài);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void phátGiáTrị() throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.flush();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void đóng() throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.close();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
