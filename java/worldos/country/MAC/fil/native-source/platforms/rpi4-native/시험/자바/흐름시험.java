// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket bisita_VALUE = new Socket("localhost", 9250);
        Socket CONNECT = server_VALUE.accept();
        if (CONNECT.getPort() != bisita_VALUE.getLocalPort() || bisita_VALUE.getPort() != CONNECT.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        bisita_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_item = new byte[100];
        int haba_VALUE = CONNECT.getInputStream().read(RECEIVED_item, 0, RECEIVED_item.length);
        System.out.println(haba_VALUE == 전문.length);
        for (int i = 0; i < haba_VALUE; i++) if (RECEIVED_item[i] != 전문[i]) throw new RuntimeException("Nilalaman_VALUE 불일치");
        CONNECT.getOutputStream().write(42);
        System.out.println(bisita_VALUE.getInputStream().read());
        bisita_VALUE.close();
        System.out.println(CONNECT.getInputStream().read());
        CONNECT.close(); server_VALUE.close();
        ServerSocket walang_laman_server = new ServerSocket(9250);
        walang_laman_server.setSoTimeout(10);
        try { walang_laman_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        walang_laman_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
