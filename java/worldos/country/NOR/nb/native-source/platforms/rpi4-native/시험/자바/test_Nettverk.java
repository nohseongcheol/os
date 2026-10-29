// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import norsk.eget.문자;
import norsk.eget.통신;
public class test_Nettverk {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontkamera_VERDI = 통신.Åpne(9431), TILBAKE_VERDI = 통신.Åpne(9432);
        try {
            통신.sende(frontkamera_VERDI, 9432, "자바 UDP 한글😀"); System.out.println(통신.motta(TILBAKE_VERDI));
            byte[] KILDE = 문자.부호화("회신"); frontkamera_VERDI.send(new DatagramPacket(KILDE, KILDE.length, InetAddress.getByName("localhost"), 9432));
            byte[] MOTTATT_AVKAST_VERDI = new byte[32]; DatagramPacket datagram = new DatagramPacket(MOTTATT_AVKAST_VERDI, MOTTATT_AVKAST_VERDI.length); TILBAKE_VERDI.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(TILBAKE_VERDI.getLocalPort());
            TILBAKE_VERDI.setSoTimeout(10);
            try { TILBAKE_VERDI.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("motta_VERDI TID_VERDI 초과"); }
            TILBAKE_VERDI.close();
            try { TILBAKE_VERDI.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { frontkamera_VERDI.close(); TILBAKE_VERDI.close(); }
    }
}
