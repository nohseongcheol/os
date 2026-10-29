// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Kênh đọc các byte đi vào theo đúng thứ tự. */
public final class LuồngĐầuVào {
    private final java.io.InputStream luồngChuẩn;
    LuồngĐầuVào(java.io.InputStream luồngChuẩn) { this.luồngChuẩn = luồngChuẩn; }
    public int đọc() throws NgoạiLệĐầuRaĐầuVào {
        try { return luồngChuẩn.read();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public int đọc(byte[] DữLiệu) throws NgoạiLệĐầuRaĐầuVào {
        try { return luồngChuẩn.read(DữLiệu);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public int đọc(byte[] DữLiệu, int chạy, int độDài) throws NgoạiLệĐầuRaĐầuVào {
        try { return luồngChuẩn.read(DữLiệu, chạy, độDài);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public void đóng() throws NgoạiLệĐầuRaĐầuVào {
        try { luồngChuẩn.close();
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
