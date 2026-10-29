// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Italiano.nativo.문자;
import Italiano.nativo.comunicazione;
public class test_Rete {
    public static void main(String[] args) throws Exception {
        DatagramSocket frontale_VALORE = comunicazione.Apri(9431), BACK_VALORE = comunicazione.Apri(9432);
        try {
            comunicazione.inviare(frontale_VALORE, 9432, "자바 UDP 한글😀"); System.out.println(comunicazione.ricevere(BACK_VALORE));
            byte[] codiceSorgente = 문자.codificare("회신"); frontale_VALORE.send(new DatagramPacket(codiceSorgente, codiceSorgente.length, InetAddress.getByName("localhost"), 9432));
            byte[] RICEV_SCAD_VALORE = new byte[32]; DatagramPacket datagramma = new DatagramPacket(RICEV_SCAD_VALORE, RICEV_SCAD_VALORE.length); BACK_VALORE.receive(datagramma);
            System.out.println(datagramma.getLength()); System.out.println(datagramma.getPort()); System.out.println(datagramma.getAddress().getHostAddress());
            System.out.println(BACK_VALORE.getLocalPort());
            BACK_VALORE.setSoTimeout(10);
            try { BACK_VALORE.receive(datagramma); } catch (SocketTimeoutException e) { System.out.println("ricevere_VALORE valore 초과"); }
            BACK_VALORE.close();
            try { BACK_VALORE.receive(datagramma); } catch (java.io.IOException e) { System.out.println("닫힌 comunicazione"); }
        } finally { frontale_VALORE.close(); BACK_VALORE.close(); }
    }
}
