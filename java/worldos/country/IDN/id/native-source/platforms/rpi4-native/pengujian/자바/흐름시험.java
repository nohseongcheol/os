// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket tamu_VALUE = new Socket("localhost", 9250);
        Socket Sambung = server_VALUE.accept();
        if (Sambung.getPort() != tamu_VALUE.getLocalPort() || tamu_VALUE.getPort() != Sambung.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        tamu_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_item = new byte[100];
        int panjang_VALUE = Sambung.getInputStream().read(RECEIVED_item, 0, RECEIVED_item.length);
        System.out.println(panjang_VALUE == 전문.length);
        for (int i = 0; i < panjang_VALUE; i++) if (RECEIVED_item[i] != 전문[i]) throw new RuntimeException("Isi_VALUE 불일치");
        Sambung.getOutputStream().write(42);
        System.out.println(tamu_VALUE.getInputStream().read());
        tamu_VALUE.close();
        System.out.println(Sambung.getInputStream().read());
        Sambung.close(); server_VALUE.close();
        ServerSocket kosong_server = new ServerSocket(9250);
        kosong_server.setSoTimeout(10);
        try { kosong_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        kosong_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
