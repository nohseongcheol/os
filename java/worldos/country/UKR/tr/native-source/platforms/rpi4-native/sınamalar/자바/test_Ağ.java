// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Türkçe.Öz.문자;
import Türkçe.Öz.iletişim;
public class test_Ağ {
    public static void main(String[] args) throws Exception {
        DatagramSocket ön_kamera_değer = iletişim.Aç(9431), BACK_değer = iletişim.Aç(9432);
        try {
            iletişim.göndermek(ön_kamera_değer, 9432, "자바 UDP 한글😀"); System.out.println(iletişim.almak(BACK_değer));
            byte[] kaynakKod = 문자.kodlamak("회신"); ön_kamera_değer.send(new DatagramPacket(kaynakKod, kaynakKod.length, InetAddress.getByName("localhost"), 9432));
            byte[] GETİRİ_değer = new byte[32]; DatagramPacket veri_birimi = new DatagramPacket(GETİRİ_değer, GETİRİ_değer.length); BACK_değer.receive(veri_birimi);
            System.out.println(veri_birimi.getLength()); System.out.println(veri_birimi.getPort()); System.out.println(veri_birimi.getAddress().getHostAddress());
            System.out.println(BACK_değer.getLocalPort());
            BACK_değer.setSoTimeout(10);
            try { BACK_değer.receive(veri_birimi); } catch (SocketTimeoutException e) { System.out.println("almak_değer zaman_değeri 초과"); }
            BACK_değer.close();
            try { BACK_değer.receive(veri_birimi); } catch (java.io.IOException e) { System.out.println("닫힌 iletişim"); }
        } finally { ön_kamera_değer.close(); BACK_değer.close(); }
    }
}
