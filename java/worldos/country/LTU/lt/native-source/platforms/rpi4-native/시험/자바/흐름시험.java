// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket serveris_VALUE = new ServerSocket(9250);
        Socket svečias_VALUE = new Socket("localhost", 9250);
        Socket Prisijungti = serveris_VALUE.accept();
        if (Prisijungti.getPort() != svečias_VALUE.getLocalPort() || svečias_VALUE.getPort() != Prisijungti.getLocalPort()) throw new RuntimeException("jungtis_VALUE 불일치");
        byte[] paketų_kelio_schema = "한글 Stream_VALUE".getBytes("UTF-8");
        svečias_VALUE.getOutputStream().write(paketų_kelio_schema);
        byte[] RECEIVED_prekė = new byte[100];
        int 길이 = Prisijungti.getInputStream().read(RECEIVED_prekė, 0, RECEIVED_prekė.length);
        System.out.println(길이 == paketų_kelio_schema.length);
        for (int i = 0; i < 길이; i++) if (RECEIVED_prekė[i] != paketų_kelio_schema[i]) throw new RuntimeException("Turinys_VALUE 불일치");
        Prisijungti.getOutputStream().write(42);
        System.out.println(svečias_VALUE.getInputStream().read());
        svečias_VALUE.close();
        System.out.println(Prisijungti.getInputStream().read());
        Prisijungti.close(); serveris_VALUE.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
