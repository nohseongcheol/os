// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.उगडचें(9431), फाटीं_मोल = 통신.उगडचें(9432);
        try {
            통신.धाडचें(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(फाटीं_मोल));
            byte[] स्त्रोत = 문자.부호화("회신"); 앞.send(new DatagramPacket(स्त्रोत, स्त्रोत.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_मोल = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_मोल, RECEIVED_मोल.length); फाटीं_मोल.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(फाटीं_मोल.getLocalPort());
            फाटीं_मोल.setSoTimeout(10);
            try { फाटीं_मोल.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_मोल 초과"); }
            फाटीं_मोल.close();
            try { फाटीं_मोल.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); फाटीं_मोल.close(); }
    }
}
