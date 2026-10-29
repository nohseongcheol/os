// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.খোলো(9431), পাছলৈ_মান = 통신.খোলো(9432);
        try {
            통신.ই_মেইল_কৰক(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(পাছলৈ_মান));
            byte[] উৎস = 문자.부호화("회신"); 앞.send(new DatagramPacket(উৎস, উৎস.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); পাছলৈ_মান.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(পাছলৈ_মান.getLocalPort());
            পাছলৈ_মান.setSoTimeout(10);
            try { পাছলৈ_মান.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 시간 초과"); }
            পাছলৈ_মান.close();
            try { পাছলৈ_মান.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); পাছলৈ_মান.close(); }
    }
}
