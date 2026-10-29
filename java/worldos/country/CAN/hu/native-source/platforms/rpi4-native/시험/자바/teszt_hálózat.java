// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import magyar.saját.문자;
import magyar.saját.kommunikáció;
public class teszt_hálózat {
    public static void main(String[] args) throws Exception {
        DatagramSocket elülső_kamera_ÉRTÉK = kommunikáció.Megnyitás(9431), BACK_ÉRTÉK = kommunikáció.Megnyitás(9432);
        try {
            kommunikáció.küld(elülső_kamera_ÉRTÉK, 9432, "자바 UDP 한글😀"); System.out.println(kommunikáció.fogad(BACK_ÉRTÉK));
            byte[] FORRÁS = 문자.kódolás("회신"); elülső_kamera_ÉRTÉK.send(new DatagramPacket(FORRÁS, FORRÁS.length, InetAddress.getByName("localhost"), 9432));
            byte[] KAPOTT_ÉRTÉK = new byte[32]; DatagramPacket datagram = new DatagramPacket(KAPOTT_ÉRTÉK, KAPOTT_ÉRTÉK.length); BACK_ÉRTÉK.receive(datagram);
            System.out.println(datagram.getLength()); System.out.println(datagram.getPort()); System.out.println(datagram.getAddress().getHostAddress());
            System.out.println(BACK_ÉRTÉK.getLocalPort());
            BACK_ÉRTÉK.setSoTimeout(10);
            try { BACK_ÉRTÉK.receive(datagram); } catch (SocketTimeoutException e) { System.out.println("fogad_ÉRTÉK IDŐ_ÉRTÉK 초과"); }
            BACK_ÉRTÉK.close();
            try { BACK_ÉRTÉK.receive(datagram); } catch (java.io.IOException e) { System.out.println("닫힌 kommunikáció"); }
        } finally { elülső_kamera_ÉRTÉK.close(); BACK_ÉRTÉK.close(); }
    }
}
