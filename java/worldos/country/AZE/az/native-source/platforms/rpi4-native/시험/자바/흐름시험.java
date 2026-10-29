// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket qonaq_VALUE = new Socket("localhost", 9250);
        Socket Bağlan = server_VALUE.accept();
        if (Bağlan.getPort() != qonaq_VALUE.getLocalPort() || qonaq_VALUE.getPort() != Bağlan.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 axın_VALUE".getBytes("UTF-8");
        qonaq_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_element = new byte[100];
        int uzunluq_VALUE = Bağlan.getInputStream().read(RECEIVED_element, 0, RECEIVED_element.length);
        System.out.println(uzunluq_VALUE == 전문.length);
        for (int i = 0; i < uzunluq_VALUE; i++) if (RECEIVED_element[i] != 전문[i]) throw new RuntimeException("Məzmun_VALUE 불일치");
        Bağlan.getOutputStream().write(42);
        System.out.println(qonaq_VALUE.getInputStream().read());
        qonaq_VALUE.close();
        System.out.println(Bağlan.getInputStream().read());
        Bağlan.close(); server_VALUE.close();
        ServerSocket boş_server = new ServerSocket(9250);
        boş_server.setSoTimeout(10);
        try { boş_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        boş_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
