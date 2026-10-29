// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket þjónn_VALUE = new ServerSocket(9250);
        Socket gestur_VALUE = new Socket("localhost", 9250);
        Socket Tengjast = þjónn_VALUE.accept();
        if (Tengjast.getPort() != gestur_VALUE.getLocalPort() || gestur_VALUE.getPort() != Tengjast.getLocalPort()) throw new RuntimeException("gátt_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        gestur_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_vara = new byte[100];
        int lengd_VALUE = Tengjast.getInputStream().read(RECEIVED_vara, 0, RECEIVED_vara.length);
        System.out.println(lengd_VALUE == 전문.length);
        for (int i = 0; i < lengd_VALUE; i++) if (RECEIVED_vara[i] != 전문[i]) throw new RuntimeException("Efni_VALUE 불일치");
        Tengjast.getOutputStream().write(42);
        System.out.println(gestur_VALUE.getInputStream().read());
        gestur_VALUE.close();
        System.out.println(Tengjast.getInputStream().read());
        Tengjast.close(); þjónn_VALUE.close();
        ServerSocket autt_þjónn = new ServerSocket(9250);
        autt_þjónn.setSoTimeout(10);
        try { autt_þjónn.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        autt_þjónn.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
