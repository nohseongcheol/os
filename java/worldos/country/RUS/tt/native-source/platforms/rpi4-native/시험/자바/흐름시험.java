// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_VALUE = new ServerSocket(9250);
        Socket кунак_VALUE = new Socket("localhost", 9250);
        Socket ялгау = сервер_VALUE.accept();
        if (ялгау.getPort() != кунак_VALUE.getLocalPort() || кунак_VALUE.getPort() != ялгау.getLocalPort()) throw new RuntimeException("порт_VALUE 불일치");
        byte[] 전문 = "한글 агым_VALUE".getBytes("UTF-8");
        кунак_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_элемент = new byte[100];
        int озынлык_VALUE = ялгау.getInputStream().read(RECEIVED_элемент, 0, RECEIVED_элемент.length);
        System.out.println(озынлык_VALUE == 전문.length);
        for (int i = 0; i < озынлык_VALUE; i++) if (RECEIVED_элемент[i] != 전문[i]) throw new RuntimeException("Эчтәлек_VALUE 불일치");
        ялгау.getOutputStream().write(42);
        System.out.println(кунак_VALUE.getInputStream().read());
        кунак_VALUE.close();
        System.out.println(ялгау.getInputStream().read());
        ялгау.close(); сервер_VALUE.close();
        ServerSocket Буш_сервер = new ServerSocket(9250);
        Буш_сервер.setSoTimeout(10);
        try { Буш_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        Буш_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
