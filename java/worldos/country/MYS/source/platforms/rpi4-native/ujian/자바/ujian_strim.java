// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class ujian_strim {
    public static void main(String[] args) throws Exception {
        ServerSocket pelayan_VALUE = new ServerSocket(9250);
        Socket tetamu_VALUE = new Socket("localhost", 9250);
        Socket Sambung = pelayan_VALUE.accept();
        if (Sambung.getPort() != tetamu_VALUE.getLocalPort() || tetamu_VALUE.getPort() != Sambung.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 strim_VALUE".getBytes("UTF-8");
        tetamu_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_item = new byte[100];
        int kepanjangan_VALUE = Sambung.getInputStream().read(RECEIVED_item, 0, RECEIVED_item.length);
        System.out.println(kepanjangan_VALUE == 전문.length);
        for (int i = 0; i < kepanjangan_VALUE; i++) if (RECEIVED_item[i] != 전문[i]) throw new RuntimeException("Kandungan_VALUE 불일치");
        Sambung.getOutputStream().write(42);
        System.out.println(tetamu_VALUE.getInputStream().read());
        tetamu_VALUE.close();
        System.out.println(Sambung.getInputStream().read());
        Sambung.close(); pelayan_VALUE.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("nilai_masa 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
