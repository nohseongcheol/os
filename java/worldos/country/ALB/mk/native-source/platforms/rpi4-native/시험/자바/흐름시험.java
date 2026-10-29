// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_VALUE = new ServerSocket(9250);
        Socket гостин_VALUE = new Socket("localhost", 9250);
        Socket Врзи_се = сервер_VALUE.accept();
        if (Врзи_се.getPort() != гостин_VALUE.getLocalPort() || гостин_VALUE.getPort() != Врзи_се.getLocalPort()) throw new RuntimeException("порта_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        гостин_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_ставка = new byte[100];
        int должина_VALUE = Врзи_се.getInputStream().read(RECEIVED_ставка, 0, RECEIVED_ставка.length);
        System.out.println(должина_VALUE == 전문.length);
        for (int i = 0; i < должина_VALUE; i++) if (RECEIVED_ставка[i] != 전문[i]) throw new RuntimeException("Содржина_VALUE 불일치");
        Врзи_се.getOutputStream().write(42);
        System.out.println(гостин_VALUE.getInputStream().read());
        гостин_VALUE.close();
        System.out.println(Врзи_се.getInputStream().read());
        Врзи_се.close(); сервер_VALUE.close();
        ServerSocket празно_сервер = new ServerSocket(9250);
        празно_сервер.setSoTimeout(10);
        try { празно_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        празно_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
