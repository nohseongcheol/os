// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket 서버 = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket نښلېدل = 서버.accept();
        if (نښلېدل.getPort() != 손님.getLocalPort() || 손님.getPort() != نښلېدل.getLocalPort()) throw new RuntimeException("درشل_ارزښت 불일치");
        byte[] 전문 = "한글 بهنګ_ارزښت".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int اوږدوالى_ارزښت = نښلېدل.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(اوږدوالى_ارزښت == 전문.length);
        for (int i = 0; i < اوږدوالى_ارزښت; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("منځپانګه_ارزښت 불일치");
        نښلېدل.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(نښلېدل.getInputStream().read());
        نښلېدل.close(); 서버.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
