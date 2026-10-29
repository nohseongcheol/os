// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket freastalaí_VALUE = new ServerSocket(9250);
        Socket aoi_VALUE = new Socket("localhost", 9250);
        Socket Nasc = freastalaí_VALUE.accept();
        if (Nasc.getPort() != aoi_VALUE.getLocalPort() || aoi_VALUE.getPort() != Nasc.getLocalPort()) throw new RuntimeException("port_VALUE 불일치");
        byte[] 전문 = "한글 sruth_VALUE".getBytes("UTF-8");
        aoi_VALUE.getOutputStream().write(전문);
        byte[] RECEIVED_mír = new byte[100];
        int fad_VALUE = Nasc.getInputStream().read(RECEIVED_mír, 0, RECEIVED_mír.length);
        System.out.println(fad_VALUE == 전문.length);
        for (int i = 0; i < fad_VALUE; i++) if (RECEIVED_mír[i] != 전문[i]) throw new RuntimeException("Inneachar_VALUE 불일치");
        Nasc.getOutputStream().write(42);
        System.out.println(aoi_VALUE.getInputStream().read());
        aoi_VALUE.close();
        System.out.println(Nasc.getInputStream().read());
        Nasc.close(); freastalaí_VALUE.close();
        ServerSocket folamh_freastalaí = new ServerSocket(9250);
        folamh_freastalaí.setSoTimeout(10);
        try { folamh_freastalaí.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("TIME_VALUE 제한"); }
        folamh_freastalaí.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
