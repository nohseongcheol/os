// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket സെര്_വര്_മൂല്യം = new ServerSocket(9250);
        Socket അതിഥി_മൂല്യം = new Socket("localhost", 9250);
        Socket കണക്ടു്_ചെയ്യുക = സെര്_വര്_മൂല്യം.accept();
        if (കണക്ടു്_ചെയ്യുക.getPort() != അതിഥി_മൂല്യം.getLocalPort() || അതിഥി_മൂല്യം.getPort() != കണക്ടു്_ചെയ്യുക.getLocalPort()) throw new RuntimeException("പോര്_ട്ട്_മൂല്യം 불일치");
        byte[] 전문 = "한글 സ്ട്രീം_മൂല്യം".getBytes("UTF-8");
        അതിഥി_മൂല്യം.getOutputStream().write(전문);
        byte[] 받은것 = new byte[100];
        int ദൈര്_ഘ്യം_മൂല്യം = കണക്ടു്_ചെയ്യുക.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(ദൈര്_ഘ്യം_മൂല്യം == 전문.length);
        for (int i = 0; i < ദൈര്_ഘ്യം_മൂല്യം; i++) if (받은것[i] != 전문[i]) throw new RuntimeException("ഉള്ളടക്കം_മൂല്യം 불일치");
        കണക്ടു്_ചെയ്യുക.getOutputStream().write(42);
        System.out.println(അതിഥി_മൂല്യം.getInputStream().read());
        അതിഥി_മൂല്യം.close();
        System.out.println(കണക്ടു്_ചെയ്യുക.getInputStream().read());
        കണക്ടു്_ചെയ്യുക.close(); സെര്_വര്_മൂല്യം.close();
        ServerSocket ശൂന്യം_സെര്_വര് = new ServerSocket(9250);
        ശൂന്യം_സെര്_വര്.setSoTimeout(10);
        try { ശൂന്യം_സെര്_വര്.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("സമയ_മൂല്യം 제한"); }
        ശൂന്യം_സെര്_വര്.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
