// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import suomi.oma.문자;
import suomi.oma.통신;
public class testi_Verkot {
    public static void main(String[] args) throws Exception {
        DatagramSocket etukamera_ARVO = 통신.Avaa(9431), BACK_ARVO = 통신.Avaa(9432);
        try {
            통신.lähettää(etukamera_ARVO, 9432, "자바 UDP 한글😀"); System.out.println(통신.saada(BACK_ARVO));
            byte[] lähdetiedosto = 문자.koodata("회신"); etukamera_ARVO.send(new DatagramPacket(lähdetiedosto, lähdetiedosto.length, InetAddress.getByName("localhost"), 9432));
            byte[] SAATU_HINTA_ARVO = new byte[32]; DatagramPacket datagrammi = new DatagramPacket(SAATU_HINTA_ARVO, SAATU_HINTA_ARVO.length); BACK_ARVO.receive(datagrammi);
            System.out.println(datagrammi.getLength()); System.out.println(datagrammi.getPort()); System.out.println(datagrammi.getAddress().getHostAddress());
            System.out.println(BACK_ARVO.getLocalPort());
            BACK_ARVO.setSoTimeout(10);
            try { BACK_ARVO.receive(datagrammi); } catch (SocketTimeoutException e) { System.out.println("saada_ARVO AIKA_ARVO 초과"); }
            BACK_ARVO.close();
            try { BACK_ARVO.receive(datagrammi); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { etukamera_ARVO.close(); BACK_ARVO.close(); }
    }
}
