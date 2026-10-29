// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_значення = new ServerSocket(9250);
        Socket гість_значення = new Socket("localhost", 9250);
        Socket З_єднання = сервер_значення.accept();
        if (З_єднання.getPort() != гість_значення.getLocalPort() || гість_значення.getPort() != З_єднання.getLocalPort()) throw new RuntimeException("порт_значення 불일치");
        byte[] дейтаграма = "한글 потік_значення".getBytes("UTF-8");
        гість_значення.getOutputStream().write(дейтаграма);
        byte[] 받은것 = new byte[100];
        int 길이 = З_єднання.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == дейтаграма.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != дейтаграма[i]) throw new RuntimeException("Вміст_значення 불일치");
        З_єднання.getOutputStream().write(42);
        System.out.println(гість_значення.getInputStream().read());
        гість_значення.close();
        System.out.println(З_єднання.getInputStream().read());
        З_єднання.close(); сервер_значення.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("час_значення 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
