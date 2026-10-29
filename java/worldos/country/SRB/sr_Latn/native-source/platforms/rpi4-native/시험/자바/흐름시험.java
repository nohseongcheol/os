// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket gost_VALUE = new Socket("localhost", 9250);
        Socket veze = server_VALUE.accept();
        if (veze.getPort() != gost_VALUE.getLocalPort() || gost_VALUE.getPort() != veze.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] datagram = "한글 tok_VALUE".getBytes("UTF-8");
        gost_VALUE.getOutputStream().write(datagram);
        byte[] RECEIVED_stavka = new byte[100];
        int 길이 = veze.getInputStream().read(RECEIVED_stavka, 0, RECEIVED_stavka.length);
        System.out.println(길이 == datagram.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_stavka[i] != datagram[i]) throw new RuntimeException("Sadržaj_VALUE 불일치");
        veze.getOutputStream().write(42);
        System.out.println(gost_VALUE.getInputStream().read());
        gost_VALUE.close();
        System.out.println(veze.getInputStream().read());
        veze.close(); server_VALUE.close();
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
