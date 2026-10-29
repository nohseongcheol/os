// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket সার্ভার_মান = new ServerSocket(9250);
        Socket অতিথি_মান = new Socket("localhost", 9250);
        Socket সংযোগ_স্থাপনা = সার্ভার_মান.accept();
        if (সংযোগ_স্থাপনা.getPort() != অতিথি_মান.getLocalPort() || অতিথি_মান.getPort() != সংযোগ_স্থাপনা.getLocalPort()) throw new RuntimeException("পোর্ট_মান 불일치");
        byte[] 전문 = "한글 প্রবাহ_মান".getBytes("UTF-8");
        অতিথি_মান.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int দৈর্ঘ্য_মান = সংযোগ_স্থাপনা.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(দৈর্ঘ্য_মান == 전문.length);
        for (int i = 0; i < দৈর্ঘ্য_মান; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("সামগ্রি_মান 불일치");
        সংযোগ_স্থাপনা.getOutputStream().write(42);
        System.out.println(অতিথি_মান.getInputStream().read());
        অতিথি_মান.close();
        System.out.println(সংযোগ_স্থাপনা.getInputStream().read());
        সংযোগ_স্থাপনা.close(); সার্ভার_মান.close();
        ServerSocket খালি_সার্ভার = new ServerSocket(9250);
        খালি_সার্ভার.setSoTimeout(10);
        try { খালি_সার্ভার.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("সময়_মান 제한"); }
        খালি_সার্ভার.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
