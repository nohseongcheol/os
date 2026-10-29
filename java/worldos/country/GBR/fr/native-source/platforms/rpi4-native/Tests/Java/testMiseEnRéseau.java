// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import français.interne.Caractères;
import français.interne.Communication;
public class testMiseEnRéseau {
    public static void main(String[] args) throws Exception {
        DatagramSocket valeurAvantCôté = Communication.ouvrir(9431), valeurRetourArrièreCôté = Communication.ouvrir(9432);
        try {
            Communication.envoyer(valeurAvantCôté, 9432, "Java UDP 한글😀"); System.out.println(Communication.recevoir(valeurRetourArrièreCôté));
            byte[] source = Caractères.encoder("회신"); valeurAvantCôté.send(new DatagramPacket(source, source.length, InetAddress.getByName("localhost"), 9432));
            byte[] valeurReçu = new byte[32]; DatagramPacket datagramme = new DatagramPacket(valeurReçu, valeurReçu.length); valeurRetourArrièreCôté.receive(datagramme);
            System.out.println(datagramme.getLength()); System.out.println(datagramme.getPort()); System.out.println(datagramme.getAddress().getHostAddress());
            System.out.println(valeurRetourArrièreCôté.getLocalPort());
            valeurRetourArrièreCôté.setSoTimeout(10);
            try { valeurRetourArrièreCôté.receive(datagramme); } catch (SocketTimeoutException e) { System.out.println("recevoirValeur valeurTemps 초과"); }
            valeurRetourArrièreCôté.close();
            try { valeurRetourArrièreCôté.receive(datagramme); } catch (java.io.IOException e) { System.out.println("닫힌 Communication"); }
        } finally { valeurAvantCôté.close(); valeurRetourArrièreCôté.close(); }
    }
}
