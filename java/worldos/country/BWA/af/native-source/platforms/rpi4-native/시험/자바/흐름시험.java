// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket bediener_VALUE = new ServerSocket(9250);
        Socket gas_VALUE = new Socket("localhost", 9250);
        Socket Koppel = bediener_VALUE.accept();
        if (Koppel.getPort() != gas_VALUE.getLocalPort() || gas_VALUE.getPort() != Koppel.getLocalPort()) throw new RuntimeException("ombou_VALUE 불일치");
        byte[] 전문 = "한글 Stream_VALUE".getBytes("UTF-8");
        gas_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_item = new byte[100];
        int lengte_VALUE = Koppel.getInputStream().read(RECEIVED_item, 0, RECEIVED_item.length);
        System.out.println(lengte_VALUE == 전문.length);
        for (int i = 0; i < lengte_VALUE; i++) if (RECEIVED_item[i] != 전문[i]) throw new RuntimeException("Inhoud_VALUE 불일치");
        Koppel.getOutputStream().write(42);
        System.out.println(gas_VALUE.getInputStream().read());
        gas_VALUE.close();
        System.out.println(Koppel.getInputStream().read());
        Koppel.close(); bediener_VALUE.close();
        ServerSocket leeg_bediener = new ServerSocket(9250);
        leeg_bediener.setSoTimeout(10);
        try { leeg_bediener.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("tyd_VALUE 제한"); }
        leeg_bediener.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
