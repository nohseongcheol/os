// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket külaline_VALUE = new Socket("localhost", 9250);
        Socket Ühendu = server_VALUE.accept();
        if (Ühendu.getPort() != külaline_VALUE.getLocalPort() || külaline_VALUE.getPort() != Ühendu.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] datagramm = "한글 voog_VALUE".getBytes("UTF-8");
        külaline_VALUE.getOutputStream().write(datagramm);
        byte[] RECEIVED_kaup = new byte[100];
        int 길이 = Ühendu.getInputStream().read(RECEIVED_kaup, 0, RECEIVED_kaup.length);
        System.out.println(길이 == datagramm.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_kaup[i] != datagramm[i]) throw new RuntimeException("Sisu_VALUE 불일치");
        Ühendu.getOutputStream().write(42);
        System.out.println(külaline_VALUE.getInputStream().read());
        külaline_VALUE.close();
        System.out.println(Ühendu.getInputStream().read());
        Ühendu.close(); server_VALUE.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("Aeg_VALUE 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
