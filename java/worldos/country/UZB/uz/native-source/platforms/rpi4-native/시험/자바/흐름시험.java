// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket server_VALUE = new ServerSocket(9250);
        Socket mehmon_VALUE = new Socket("localhost", 9250);
        Socket Ulanish = server_VALUE.accept();
        if (Ulanish.getPort() != mehmon_VALUE.getLocalPort() || mehmon_VALUE.getPort() != Ulanish.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 oqim_VALUE".getBytes("UTF-8");
        mehmon_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_element = new byte[100];
        int uzunlik_VALUE = Ulanish.getInputStream().read(RECEIVED_element, 0, RECEIVED_element.length);
        System.out.println(uzunlik_VALUE == 전문.length);
        for (int i = 0; i < uzunlik_VALUE; i++) if (RECEIVED_element[i] != 전문[i]) throw new RuntimeException("tarkib_VALUE 불일치");
        Ulanish.getOutputStream().write(42);
        System.out.println(mehmon_VALUE.getInputStream().read());
        mehmon_VALUE.close();
        System.out.println(Ulanish.getInputStream().read());
        Ulanish.close(); server_VALUE.close();
        ServerSocket bo_sh_server = new ServerSocket(9250);
        bo_sh_server.setSoTimeout(10);
        try { bo_sh_server.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        bo_sh_server.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
