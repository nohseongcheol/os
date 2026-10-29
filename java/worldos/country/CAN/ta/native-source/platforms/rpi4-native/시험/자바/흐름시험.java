// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket சேவையகம்_மதிப்பு = new ServerSocket(9250);
        Socket விருந்தினர்_மதிப்பு = new Socket("localhost", 9250);
        Socket இணைக்க = சேவையகம்_மதிப்பு.accept();
        if (இணைக்க.getPort() != விருந்தினர்_மதிப்பு.getLocalPort() || விருந்தினர்_மதிப்பு.getPort() != இணைக்க.getLocalPort()) throw new RuntimeException("முணையம்_மதிப்பு 불일치");
        byte[] 전문 = "한글 தொடரோடி_மதிப்பு".getBytes("UTF-8");
        விருந்தினர்_மதிப்பு.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int நீளம்_மதிப்பு = இணைக்க.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(நீளம்_மதிப்பு == 전문.length);
        for (int i = 0; i < நீளம்_மதிப்பு; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("உள்ளடக்கம்_மதிப்பு 불일치");
        இணைக்க.getOutputStream().write(42);
        System.out.println(விருந்தினர்_மதிப்பு.getInputStream().read());
        விருந்தினர்_மதிப்பு.close();
        System.out.println(இணைக்க.getInputStream().read());
        இணைக்க.close(); சேவையகம்_மதிப்பு.close();
        ServerSocket வெறுமை_சேவையகம் = new ServerSocket(9250);
        வெறுமை_சேவையகம்.setSoTimeout(10);
        try { வெறுமை_சேவையகம்.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("நேர_மதிப்பு 제한"); }
        வெறுமை_சேவையகம்.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
