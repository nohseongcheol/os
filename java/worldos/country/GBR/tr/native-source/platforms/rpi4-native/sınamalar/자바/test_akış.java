// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_akış {
    public static void main(String[] args) throws Exception {
        ServerSocket sunucu_değer = new ServerSocket(9250);
        Socket konuk_değer = new Socket("localhost", 9250);
        Socket Bağlan = sunucu_değer.accept();
        if (Bağlan.getPort() != konuk_değer.getLocalPort() || konuk_değer.getPort() != Bağlan.getLocalPort()) throw new RuntimeException("taşımak_değer 불일치");
        byte[] veri_birimi = "한글 akış_değer".getBytes("UTF-8");
        konuk_değer.getOutputStream().write(veri_birimi);
        byte[] GETİRİ_öğe = new byte[100];
        int süre_değer = Bağlan.getInputStream().read(GETİRİ_öğe, 0, GETİRİ_öğe.length);
        System.out.println(süre_değer == veri_birimi.length);
        for (int i = 0; i < süre_değer; i++) if (GETİRİ_öğe[i] != veri_birimi[i]) throw new RuntimeException("içerik_değer 불일치");
        Bağlan.getOutputStream().write(42);
        System.out.println(konuk_değer.getInputStream().read());
        konuk_değer.close();
        System.out.println(Bağlan.getInputStream().read());
        Bağlan.close(); sunucu_değer.close();
        ServerSocket boş_sunucu = new ServerSocket(9250);
        boş_sunucu.setSoTimeout(10);
        try { boş_sunucu.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("zaman_değeri 제한"); }
        boş_sunucu.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
