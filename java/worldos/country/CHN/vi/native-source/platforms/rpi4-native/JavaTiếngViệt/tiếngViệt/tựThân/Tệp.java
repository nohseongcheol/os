// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** Giữ khái niệm tệp quen thuộc. Kho hiện tại là tệp RAM mất khi khởi động lại. */
public final class Tệp {
    private Tệp() {}
    public static byte[] đọcGiáTrịByte(String tên) throws NgoạiLệĐầuRaĐầuVào {
        try {
        FileInputStream giáTrịLuồng = new FileInputStream(tên);
        try {
            byte[] giáTrịTạm = new byte[16384]; int trịSố = 0, giáTrị;
            while ((giáTrị = giáTrịLuồng.read()) != -1) { if (trịSố == giáTrịTạm.length) throw new NgoạiLệĐầuRaĐầuVào("Giới hạn kích thước tệp"); giáTrịTạm[trịSố++] = (byte)giáTrị; }
            byte[] kếtQuả = new byte[trịSố]; System.arraycopy(giáTrịTạm, 0, kếtQuả, 0, trịSố); return kếtQuả;
        } finally { giáTrịLuồng.close(); }
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void ghiGiáTrịByte(String tên, byte[] giáTrịNộiDung) throws NgoạiLệĐầuRaĐầuVào {
        try {
        FileOutputStream giáTrịLuồng = new FileOutputStream(tên);
        try { for (int chỉSốVòngLặp = 0; chỉSốVòngLặp < giáTrịNộiDung.length; chỉSốVòngLặp++) giáTrịLuồng.write(giáTrịNộiDung[chỉSốVòngLặp] & 255); } finally { giáTrịLuồng.close(); }
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static String đọc(String tên) throws NgoạiLệĐầuRaĐầuVào {
        try { return KýTự.giảiMậtMãDữLiệu(đọcGiáTrịByte(tên));
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void ghi(String tên, String giáTrịNộiDung) throws NgoạiLệĐầuRaĐầuVào {
        try { ghiGiáTrịByte(tên, KýTự.mãHóa(giáTrịNộiDung));
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
}
