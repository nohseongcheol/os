// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket 서버 = new ServerSocket(9250);
        Socket अतिथि_मान = new Socket("localhost", 9250);
        Socket जोड़ना = 서버.accept();
        if (जोड़ना.getPort() != अतिथि_मान.getLocalPort() || अतिथि_मान.getPort() != जोड़ना.getLocalPort()) throw new RuntimeException("पोर्ट_मान 불일치");
        byte[] स्वतंत्रसंदेश = "한글 स्ट्रीम_मान".getBytes("UTF-8");
        अतिथि_मान.getOutputStream().write(स्वतंत्रसंदेश);
        byte[] 받은것 = new byte[100];
        int 길이 = जोड़ना.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == स्वतंत्रसंदेश.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != स्वतंत्रसंदेश[i]) throw new RuntimeException("सामग्री_मान 불일치");
        जोड़ना.getOutputStream().write(42);
        System.out.println(अतिथि_मान.getInputStream().read());
        अतिथि_मान.close();
        System.out.println(जोड़ना.getInputStream().read());
        जोड़ना.close(); 서버.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("समय_उपयोगिता 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
