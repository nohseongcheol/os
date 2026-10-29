// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket gost_VALUE = new Socket("localhost", 9250);
        Socket Spoji_se = server_VALUE.accept();
        if (Spoji_se.getPort() != gost_VALUE.getLocalPort() || gost_VALUE.getPort() != Spoji_se.getLocalPort()) throw new RuntimeException("prebaciti_VALUE 불일치");
        byte[] datogram = "한글 tok_VALUE".getBytes("UTF-8");
        gost_VALUE.getOutputStream().write(datogram);
        byte[] RECEIVED_artikl = new byte[100];
        int 길이 = Spoji_se.getInputStream().read(RECEIVED_artikl, 0, RECEIVED_artikl.length);
        System.out.println(길이 == datogram.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_artikl[i] != datogram[i]) throw new RuntimeException("Sadržaj_VALUE 불일치");
        Spoji_se.getOutputStream().write(42);
        System.out.println(gost_VALUE.getInputStream().read());
        gost_VALUE.close();
        System.out.println(Spoji_se.getInputStream().read());
        Spoji_se.close(); server_VALUE.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
