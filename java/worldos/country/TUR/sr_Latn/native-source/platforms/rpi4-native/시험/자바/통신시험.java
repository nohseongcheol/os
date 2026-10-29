// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket čeona_kamera_VALUE = 통신.otvoren(9431), NAZAD_VALUE = 통신.otvoren(9432);
        try {
            통신.poslati(čeona_kamera_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.primiti(NAZAD_VALUE));
            byte[] izvor = 문자.kodirati("회신"); čeona_kamera_VALUE.send(new DatagramPacket(izvor, izvor.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket datagram = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); NAZAD_VALUE.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(NAZAD_VALUE.getLocalPort());
            NAZAD_VALUE.setSoTimeout(10);
            try { NAZAD_VALUE.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("primiti_VALUE TIME_VALUE 초과"); }
            NAZAD_VALUE.close();
            try { NAZAD_VALUE.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { čeona_kamera_VALUE.close(); NAZAD_VALUE.close(); }
    }
}
