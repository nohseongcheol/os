// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket алдыңғы_камера_мән = 통신.Ашу(9431), АРТҚА_мән = 통신.Ашу(9432);
        try {
            통신.жіберу(алдыңғы_камера_мән, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(АРТҚА_мән));
            byte[] Неден = 문자.부호화("회신"); алдыңғы_камера_мән.send(new DatagramPacket(Неден, Неден.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); АРТҚА_мән.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(АРТҚА_мән.getLocalPort());
            АРТҚА_мән.setSoTimeout(10);
            try { АРТҚА_мән.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 уақыт_мән 초과"); }
            АРТҚА_мән.close();
            try { АРТҚА_мән.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { алдыңғы_камера_мән.close(); АРТҚА_мән.close(); }
    }
}
