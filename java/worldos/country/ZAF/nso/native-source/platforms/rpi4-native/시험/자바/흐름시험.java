// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket seba_boleng = new ServerSocket(9250);
        Socket moeng_boleng = new Socket("localhost", 9250);
        Socket Ikgokaganye = seba_boleng.accept();
        if (Ikgokaganye.getPort() != moeng_boleng.getLocalPort() || moeng_boleng.getPort() != Ikgokaganye.getLocalPort()) throw new RuntimeException("phote_boleng 불일치");
        byte[] 전문 = "한글 Stream_boleng".getBytes("UTF-8");
        moeng_boleng.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int botelele_boleng = Ikgokaganye.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(botelele_boleng == 전문.length);
        for (int i = 0; i < botelele_boleng; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Diteng_boleng 불일치");
        Ikgokaganye.getOutputStream().write(42);
        System.out.println(moeng_boleng.getInputStream().read());
        moeng_boleng.close();
        System.out.println(Ikgokaganye.getInputStream().read());
        Ikgokaganye.close(); seba_boleng.close();
        ServerSocket hloka_selo_seba = new ServerSocket(9250);
        hloka_selo_seba.setSoTimeout(10);
        try { hloka_selo_seba.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        hloka_selo_seba.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
