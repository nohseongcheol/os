// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сървър_стойност = new ServerSocket(9250);
        Socket гост_стойност = new Socket("localhost", 9250);
        Socket Свързване = сървър_стойност.accept();
        if (Свързване.getPort() != гост_стойност.getLocalPort() || гост_стойност.getPort() != Свързване.getLocalPort()) throw new RuntimeException("порт_стойност 불일치");
        byte[] дейтаграма = "한글 поток_стойност".getBytes("UTF-8");
        гост_стойност.getOutputStream().write(дейтаграма);
        byte[] 받은것 = new byte[100];
        int 길이 = Свързване.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == дейтаграма.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != дейтаграма[i]) throw new RuntimeException("Съдържание_стойност 불일치");
        Свързване.getOutputStream().write(42);
        System.out.println(гост_стойност.getInputStream().read());
        гост_стойност.close();
        System.out.println(Свързване.getInputStream().read());
        Свързване.close(); сървър_стойност.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("час_стойност 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
