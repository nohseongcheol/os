// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class testFlux {
    public static void main(String[] args) throws Exception {
        ServerSocket valeurServeur = new ServerSocket(9250);
        Socket valeurInvité = new Socket("localhost", 9250);
        Socket connecter = valeurServeur.accept();
        if (connecter.getPort() != valeurInvité.getLocalPort() || valeurInvité.getPort() != connecter.getLocalPort()) throw new RuntimeException("valeurPort 불일치");
        byte[] datagramme = "한글 valeurFlux".getBytes("UTF-8");
        valeurInvité.getOutputStream().write(datagramme);
        byte[] élémentListeReçu = new byte[100];
        int longueur = connecter.getInputStream().read(élémentListeReçu, 0, élémentListeReçu.length);
        System.out.println(longueur == datagramme.length);
        for (int i = 0; i < longueur; i++) if (élémentListeReçu[i] != datagramme[i]) throw new RuntimeException("valeurContenuValeur 불일치");
        connecter.getOutputStream().write(42);
        System.out.println(valeurInvité.getInputStream().read());
        valeurInvité.close();
        System.out.println(connecter.getInputStream().read());
        connecter.close(); valeurServeur.close();
        ServerSocket serveurVide = new ServerSocket(9250);
        serveurVide.setSoTimeout(10);
        try { serveurVide.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("valeurTemps valeurLimite"); }
        serveurVide.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS estNonPrisEnCharge"); }
        System.out.println("STREAM PASS");
    }
}
