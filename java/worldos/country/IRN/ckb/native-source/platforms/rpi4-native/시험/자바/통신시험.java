// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.کردنەوە(9431), دواوە_نرخ = 통신.کردنەوە(9432);
        try {
            통신.ناردن(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(دواوە_نرخ));
            byte[] ژێدەر = 문자.부호화("회신"); 앞.send(new DatagramPacket(ژێدەر, ژێدەر.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); دواوە_نرخ.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(دواوە_نرخ.getLocalPort());
            دواوە_نرخ.setSoTimeout(10);
            try { دواوە_نرخ.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 کات_نرخ 초과"); }
            دواوە_نرخ.close();
            try { دواوە_نرخ.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); دواوە_نرخ.close(); }
    }
}
