// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_мән = new ServerSocket(9250);
        Socket қонақ_мән = new Socket("localhost", 9250);
        Socket Байланысу = сервер_мән.accept();
        if (Байланысу.getPort() != қонақ_мән.getLocalPort() || қонақ_мән.getPort() != Байланысу.getLocalPort()) throw new RuntimeException("порт_мән 불일치");
        byte[] 전문 = "한글 ағым_мән".getBytes("UTF-8");
        қонақ_мән.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ұзындық_мән = Байланысу.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ұзындық_мән == 전문.length);
        for (int i = 0; i < ұзындық_мән; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("мазмұн_мән 불일치");
        Байланысу.getOutputStream().write(42);
        System.out.println(қонақ_мән.getInputStream().read());
        қонақ_мән.close();
        System.out.println(Байланысу.getInputStream().read());
        Байланысу.close(); сервер_мән.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("уақыт_мән 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
