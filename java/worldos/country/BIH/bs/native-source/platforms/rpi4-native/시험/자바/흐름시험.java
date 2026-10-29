// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket gost_VALUE = new Socket("localhost", 9250);
        Socket Spoji_se = server_VALUE.accept();
        if (Spoji_se.getPort() != gost_VALUE.getLocalPort() || gost_VALUE.getPort() != Spoji_se.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 tok_VALUE".getBytes("UTF-8");
        gost_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_stavka = new byte[100];
        int dužina_VALUE = Spoji_se.getInputStream().read(RECEIVED_stavka, 0, RECEIVED_stavka.length);
        System.out.println(dužina_VALUE == 전문.length);
        for (int i = 0; i < dužina_VALUE; i++) if (RECEIVED_stavka[i] != 전문[i]) throw new RuntimeException("Sadržaj_VALUE 불일치");
        Spoji_se.getOutputStream().write(42);
        System.out.println(gost_VALUE.getInputStream().read());
        gost_VALUE.close();
        System.out.println(Spoji_se.getInputStream().read());
        Spoji_se.close(); server_VALUE.close();
        ServerSocket prazno_server = new ServerSocket(9250);
        prazno_server.setSoTimeout(10);
        try { prazno_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        prazno_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
