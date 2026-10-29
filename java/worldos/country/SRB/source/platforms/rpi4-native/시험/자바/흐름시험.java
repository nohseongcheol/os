// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_вриједност = new ServerSocket(9250);
        Socket гост_вриједност = new Socket("localhost", 9250);
        Socket Повежи_се = сервер_вриједност.accept();
        if (Повежи_се.getPort() != гост_вриједност.getLocalPort() || гост_вриједност.getPort() != Повежи_се.getLocalPort()) throw new RuntimeException("порт_вриједност 불일치");
        byte[] 전문 = "한글 ток_вриједност".getBytes("UTF-8");
        гост_вриједност.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int дужина_вриједност = Повежи_се.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(дужина_вриједност == 전문.length);
        for (int i = 0; i < дужина_вриједност; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Садржај_вриједност 불일치");
        Повежи_се.getOutputStream().write(42);
        System.out.println(гост_вриједност.getInputStream().read());
        гост_вриједност.close();
        System.out.println(Повежи_се.getInputStream().read());
        Повежи_се.close(); сервер_вриједност.close();
        ServerSocket празно_сервер = new ServerSocket(9250);
        празно_сервер.setSoTimeout(10);
        try { празно_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("време_вриједност 제한"); }
        празно_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
