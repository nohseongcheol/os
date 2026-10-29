// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class datenstromPrüfung {
    public static void main(String[] args) throws Exception {
        ServerSocket dienstanbieterWert = new ServerSocket(9250);
        Socket gastWert = new Socket("localhost", 9250);
        Socket verbinden = dienstanbieterWert.accept();
        if (verbinden.getPort() != gastWert.getLocalPort() || gastWert.getPort() != verbinden.getLocalPort()) throw new RuntimeException("portWert 불일치");
        byte[] datagramm = "한글 datenstromWert".getBytes("UTF-8");
        gastWert.getOutputStream().write(datagramm);
        byte[] empfangenWertElementeintrag = new byte[100];
        int Länge = verbinden.getInputStream().read(empfangenWertElementeintrag, 0, empfangenWertElementeintrag.length);
        System.out.println(Länge == datagramm.length);
        for (int i = 0; i < Länge; i++) if (empfangenWertElementeintrag[i] != datagramm[i]) throw new RuntimeException("inhaltswertWert 불일치");
        verbinden.getOutputStream().write(42);
        System.out.println(gastWert.getInputStream().read());
        gastWert.close();
        System.out.println(verbinden.getInputStream().read());
        verbinden.close(); dienstanbieterWert.close();
        ServerSocket leerwertDienstanbieter = new ServerSocket(9250);
        leerwertDienstanbieter.setSoTimeout(10);
        try { leerwertDienstanbieter.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("zeitWert grenzwertWert"); }
        leerwertDienstanbieter.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS istNichtUnterstützt"); }
        System.out.println("STREAM PASS");
    }
}
