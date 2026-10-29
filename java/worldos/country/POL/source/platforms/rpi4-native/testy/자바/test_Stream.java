// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class test_Stream {
    public static void main(String[] args) throws Exception {
        ServerSocket serwer_WARTOŚĆ = new ServerSocket(9250);
        Socket gość_WARTOŚĆ = new Socket("localhost", 9250);
        Socket Połącz = serwer_WARTOŚĆ.accept();
        if (Połącz.getPort() != gość_WARTOŚĆ.getLocalPort() || gość_WARTOŚĆ.getPort() != Połącz.getLocalPort()) throw new RuntimeException("port_WARTOŚĆ 불일치");
        byte[] datagram = "한글 Stream_WARTOŚĆ".getBytes("UTF-8");
        gość_WARTOŚĆ.getOutputStream().write(datagram);
        byte[] KWOTA_WYKUP_towar = new byte[100];
        int długość_WARTOŚĆ = Połącz.getInputStream().read(KWOTA_WYKUP_towar, 0, KWOTA_WYKUP_towar.length);
        System.out.println(długość_WARTOŚĆ == datagram.length);
        for (int i = 0; i < długość_WARTOŚĆ; i++) if (KWOTA_WYKUP_towar[i] != datagram[i]) throw new RuntimeException("treść_WARTOŚĆ_cb0f2404 불일치");
        Połącz.getOutputStream().write(42);
        System.out.println(gość_WARTOŚĆ.getInputStream().read());
        gość_WARTOŚĆ.close();
        System.out.println(Połącz.getInputStream().read());
        Połącz.close(); serwer_WARTOŚĆ.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("wartość_czasu 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
