// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket zerbitzari_balio = new ServerSocket(9250);
        Socket gonbidatu_balio = new Socket("localhost", 9250);
        Socket Konektatu = zerbitzari_balio.accept();
        if (Konektatu.getPort() != gonbidatu_balio.getLocalPort() || gonbidatu_balio.getPort() != Konektatu.getLocalPort()) throw new RuntimeException("ataka_balio 불일치");
        byte[] 전문 = "한글 Stream_balio".getBytes("UTF-8");
        gonbidatu_balio.getOutputStream().write(전문);
        byte[] RECEIVED_elementu = new byte[100];
        int luzera_balio = Konektatu.getInputStream().read(RECEIVED_elementu, 0, RECEIVED_elementu.length);
        System.out.println(luzera_balio == 전문.length);
        for (int i = 0; i < luzera_balio; i++) if (RECEIVED_elementu[i] != 전문[i]) throw new RuntimeException("eduki_balio 불일치");
        Konektatu.getOutputStream().write(42);
        System.out.println(gonbidatu_balio.getInputStream().read());
        gonbidatu_balio.close();
        System.out.println(Konektatu.getInputStream().read());
        Konektatu.close(); zerbitzari_balio.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ordua_balio 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
