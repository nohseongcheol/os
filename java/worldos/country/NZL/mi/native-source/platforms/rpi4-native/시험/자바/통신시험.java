// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Reo_Māori.자체.문자;
import Reo_Māori.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.Huaki(9431), Hoki_uara = 통신.Huaki(9432);
        try {
            통신.tuku(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Hoki_uara));
            byte[] pūtake = 문자.부호화("회신"); 앞.send(new DatagramPacket(pūtake, pūtake.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_uara = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_uara, RECEIVED_uara.length); Hoki_uara.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Hoki_uara.getLocalPort());
            Hoki_uara.setSoTimeout(10);
            try { Hoki_uara.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_uara 초과"); }
            Hoki_uara.close();
            try { Hoki_uara.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); Hoki_uara.close(); }
    }
}
