// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class testi_virta {
    public static void main(String[] args) throws Exception {
        ServerSocket palvelin_ARVO = new ServerSocket(9250);
        Socket vieras_ARVO = new Socket("localhost", 9250);
        Socket Yhdistä = palvelin_ARVO.accept();
        if (Yhdistä.getPort() != vieras_ARVO.getLocalPort() || vieras_ARVO.getPort() != Yhdistä.getLocalPort()) throw new RuntimeException("portti_ARVO 불일치");
        byte[] datagrammi = "한글 virta_ARVO".getBytes("UTF-8");
        vieras_ARVO.getOutputStream().write(datagrammi);
        byte[] SAATU_HINTA_kohde = new byte[100];
        int kesto_ARVO = Yhdistä.getInputStream().read(SAATU_HINTA_kohde, 0, SAATU_HINTA_kohde.length);
        System.out.println(kesto_ARVO == datagrammi.length);
        for (int i = 0; i < kesto_ARVO; i++) if (SAATU_HINTA_kohde[i] != datagrammi[i]) throw new RuntimeException("Sisältö_ARVO 불일치");
        Yhdistä.getOutputStream().write(42);
        System.out.println(vieras_ARVO.getInputStream().read());
        vieras_ARVO.close();
        System.out.println(Yhdistä.getInputStream().read());
        Yhdistä.close(); palvelin_ARVO.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("AIKA_ARVO 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
