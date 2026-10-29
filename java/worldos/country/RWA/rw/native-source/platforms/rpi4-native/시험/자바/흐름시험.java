// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket seriveri_agaciro = new ServerSocket(9250);
        Socket 손님 = new Socket("localhost", 9250);
        Socket Guhuza = seriveri_agaciro.accept();
        if (Guhuza.getPort() != 손님.getLocalPort() || 손님.getPort() != Guhuza.getLocalPort()) throw new RuntimeException("poti_agaciro 불일치");
        byte[] 전문 = "한글 Stream_agaciro".getBytes("UTF-8");
        손님.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int uburebure_agaciro = Guhuza.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(uburebure_agaciro == 전문.length);
        for (int i = 0; i < uburebure_agaciro; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("Ibirimo_agaciro 불일치");
        Guhuza.getOutputStream().write(42);
        System.out.println(손님.getInputStream().read());
        손님.close();
        System.out.println(Guhuza.getInputStream().read());
        Guhuza.close(); seriveri_agaciro.close();
        ServerSocket irimo_ubusa_seriveri = new ServerSocket(9250);
        irimo_ubusa_seriveri.setSoTimeout(10);
        try { irimo_ubusa_seriveri.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("시간 제한"); }
        irimo_ubusa_seriveri.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
