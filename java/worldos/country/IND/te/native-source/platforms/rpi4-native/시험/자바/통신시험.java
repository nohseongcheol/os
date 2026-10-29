// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ముందు_మూల్యం = 통신.తెరువు(9431), వెనుకకు_మూల్యం = 통신.తెరువు(9432);
        try {
            통신.పంపు(ముందు_మూల్యం, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(వెనుకకు_మూల్యం));
            byte[] వనరు = 문자.부호화("회신"); ముందు_మూల్యం.send(new DatagramPacket(వనరు, వనరు.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); వెనుకకు_మూల్యం.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(వెనుకకు_మూల్యం.getLocalPort());
            వెనుకకు_మూల్యం.setSoTimeout(10);
            try { వెనుకకు_మూల్యం.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 సమయం_మూల్యం 초과"); }
            వెనుకకు_మూల్యం.close();
            try { వెనుకకు_మూల్యం.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ముందు_మూల్యం.close(); వెనుకకు_మూల్యం.close(); }
    }
}
