// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket mbele_thamani = 통신.unda(9431), Nyuma_thamani = 통신.unda(9432);
        try {
            통신.tuma(mbele_thamani, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Nyuma_thamani));
            byte[] chanzo = 문자.부호화("회신"); mbele_thamani.send(new DatagramPacket(chanzo, chanzo.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); Nyuma_thamani.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Nyuma_thamani.getLocalPort());
            Nyuma_thamani.setSoTimeout(10);
            try { Nyuma_thamani.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 saa_thamani_4692cef5 초과"); }
            Nyuma_thamani.close();
            try { Nyuma_thamani.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { mbele_thamani.close(); Nyuma_thamani.close(); }
    }
}
