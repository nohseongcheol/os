// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket mistieden_VALUE = new Socket("localhost", 9250);
        Socket AQBAD = server_VALUE.accept();
        if (AQBAD.getPort() != mistieden_VALUE.getLocalPort() || mistieden_VALUE.getPort() != AQBAD.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        mistieden_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_element = new byte[100];
        int tul_VALUE = AQBAD.getInputStream().read(RECEIVED_element, 0, RECEIVED_element.length);
        System.out.println(tul_VALUE == 전문.length);
        for (int i = 0; i < tul_VALUE; i++) if (RECEIVED_element[i] != 전문[i]) throw new RuntimeException("Kontenut_VALUE 불일치");
        AQBAD.getOutputStream().write(42);
        System.out.println(mistieden_VALUE.getInputStream().read());
        mistieden_VALUE.close();
        System.out.println(AQBAD.getInputStream().read());
        AQBAD.close(); server_VALUE.close();
        ServerSocket vojt_server = new ServerSocket(9250);
        vojt_server.setSoTimeout(10);
        try { vojt_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        vojt_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
