// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** Thông điệp IPv4 UDP. Dùng địa chỉ số cho bên ngoài. */
public final class TruyềnThông {
    private TruyềnThông() {}
    public static DatagramSocket mở(int giáTrịCổng) throws NgoạiLệĐầuRaĐầuVào {
        try { return new DatagramSocket(giáTrịCổng);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void gửi(DatagramSocket điểmCuối, int giáTrịCổng, String giáTrịNộiDung) throws NgoạiLệĐầuRaĐầuVào {
        try {
        gửi(điểmCuối, "127.0.0.1", giáTrịCổng, giáTrịNộiDung);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void gửi(DatagramSocket điểmCuối, String địaChỉ, int giáTrịCổng, String giáTrịNộiDung) throws NgoạiLệĐầuRaĐầuVào {
        try {
        byte[] giáTrịByte = KýTự.mãHóa(giáTrịNộiDung);
        điểmCuối.send(new DatagramPacket(giáTrịByte, giáTrịByte.length, InetAddress.getByName(địaChỉ), giáTrịCổng));
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static String nhận(DatagramSocket điểmCuối) throws NgoạiLệĐầuRaĐầuVào {
        try {
        byte[] giáTrịByte = new byte[512]; DatagramPacket điệnDữLiệu = new DatagramPacket(giáTrịByte, giáTrịByte.length); điểmCuối.receive(điệnDữLiệu);
        byte[] kếtQuả = new byte[điệnDữLiệu.getLength()]; System.arraycopy(giáTrịByte, 0, kếtQuả, 0, kếtQuả.length); return KýTự.giảiMậtMãDữLiệu(kếtQuả);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void hếtGiờ(DatagramSocket điểmCuối, int miliGiây) throws NgoạiLệĐầuRaĐầuVào {
        try { điểmCuối.setSoTimeout(miliGiây);
        } catch (java.io.IOException lỗi) { throw chuyểnĐổiNgoạiLệ.đầuRaĐầuVào(lỗi); }
        catch (RuntimeException lỗi) { throw chuyểnĐổiNgoạiLệ.thựcThiLệnh(lỗi); }
    }
    public static void đóng(DatagramSocket điểmCuối) { điểmCuối.close(); }
}
