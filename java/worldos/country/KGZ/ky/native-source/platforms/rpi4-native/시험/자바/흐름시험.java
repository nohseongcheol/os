// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_маани = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket Туташуу = сервер_маани.accept();
        if (Туташуу.getPort() != 손님.getLocalPort() || 손님.getPort() != Туташуу.getLocalPort()) throw new RuntimeException("порт_маани 불일치");
        byte[] 전문 = "한글 агым_маани".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int узундук_маани = Туташуу.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(узундук_маани == 전문.length);
        for (int i = 0; i < узундук_маани; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Мазмун_маани 불일치");
        Туташуу.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(Туташуу.getInputStream().read());
        Туташуу.close(); сервер_маани.close();
        ServerSocket бош_сервер = new ServerSocket(9250);
        бош_сервер.setSoTimeout(10);
        try { бош_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        бош_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
