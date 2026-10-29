// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket serveris_VALUE = new ServerSocket(9250);
        Socket viesis_VALUE = new Socket("localhost", 9250);
        Socket Savienoties = serveris_VALUE.accept();
        if (Savienoties.getPort() != viesis_VALUE.getLocalPort() || viesis_VALUE.getPort() != Savienoties.getLocalPort()) throw new RuntimeException("ports_VALUE 불일치");
        byte[] datogramma = "한글 Stream_VALUE".getBytes("UTF-8");
        viesis_VALUE.getOutputStream().write(datogramma);
        byte[] RECEIVED_krājums = new byte[100];
        int 길이 = Savienoties.getInputStream().read(RECEIVED_krājums, 0, RECEIVED_krājums.length);
        System.out.println(길이 == datogramma.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_krājums[i] != datogramma[i]) throw new RuntimeException("Saturs_VALUE 불일치");
        Savienoties.getOutputStream().write(42);
        System.out.println(viesis_VALUE.getInputStream().read());
        viesis_VALUE.close();
        System.out.println(Savienoties.getInputStream().read());
        Savienoties.close(); serveris_VALUE.close();
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
