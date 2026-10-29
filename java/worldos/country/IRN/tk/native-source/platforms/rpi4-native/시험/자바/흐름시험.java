// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket serwer_baha = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket Birikme = serwer_baha.accept();
        if (Birikme.getPort() != 손님.getLocalPort() || 손님.getPort() != Birikme.getLocalPort()) throw new RuntimeException("port_baha 불일치");
        byte[] 전문 = "한글 Stream_baha".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int dowamlylyk_baha = Birikme.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(dowamlylyk_baha == 전문.length);
        for (int i = 0; i < dowamlylyk_baha; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Mazmun_baha 불일치");
        Birikme.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(Birikme.getInputStream().read());
        Birikme.close(); serwer_baha.close();
        ServerSocket boş_serwer = new ServerSocket(9250);
        boş_serwer.setSoTimeout(10);
        try { boş_serwer.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        boş_serwer.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
