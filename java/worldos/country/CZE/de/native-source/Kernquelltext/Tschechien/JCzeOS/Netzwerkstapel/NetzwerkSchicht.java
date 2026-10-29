// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tschechien.JCzeOS.Netzwerkstapel;

import java.util.HashMap;
import java.util.Map;

/** Zentrale Empfangsverteilung für Ethernet, ARP, IPv4, ICMP, UDP und TCP. */
public final class NetzwerkSchicht {
    @FunctionalInterface
    public interface datenBehandler {
        void prozessWertEintrag(byte[] Daten, int ausführenVorgang, int Länge);
    }

    private final Map<Integer, datenBehandler> EthernetBehandler = new HashMap<Integer, datenBehandler>();
    private final Map<Integer, datenBehandler> InternetProtokollBehandler = new HashMap<Integer, datenBehandler>();
    private final Map<Integer, datenBehandler> benutzerDatenEinheitBehandler = new HashMap<Integer, datenBehandler>();
    private final Map<Integer, datenBehandler> DatenübermittlungSteuerungBehandler = new HashMap<Integer, datenBehandler>();

    public void ethernetRegister(int artWert, datenBehandler Behandler) {
        EthernetBehandler.put(Integer.valueOf(artWert & 0xffff), Behandler);
    }

    public void internetProtokollRegister(int vertragWert, datenBehandler Behandler) {
        InternetProtokollBehandler.put(Integer.valueOf(vertragWert & 0xff), Behandler);
    }

    public void benutzerDatenEinheitRegister(int hardwarePort, datenBehandler Behandler) {
        benutzerDatenEinheitBehandler.put(Integer.valueOf(hardwarePort & 0xffff), Behandler);
    }

    public void datenübermittlungSteuerungRegister(int hardwarePort, datenBehandler Behandler) {
        DatenübermittlungSteuerungBehandler.put(Integer.valueOf(hardwarePort & 0xffff), Behandler);
    }

    public boolean ethernetEmpfangen(byte[] rahmenIndex) {
        if (!NetzwerkWerkzeuge.istEthernetRahmen(rahmenIndex)) {
            return false;
        }
        int artWert = NetzwerkWerkzeuge.ethernetObererProtokoll(rahmenIndex);
        datenBehandler DirektBehandler = EthernetBehandler.get(Integer.valueOf(artWert));
        if (DirektBehandler != null) {
            DirektBehandler.prozessWertEintrag(rahmenIndex, 14, rahmenIndex.length - 14);
            return true;
        }
        return artWert == 0x0800 && internetPaketEmpfangen(rahmenIndex, 14);
    }

    private boolean internetPaketEmpfangen(byte[] Daten, int ausführenVorgang) {
        if (!NetzwerkWerkzeuge.istIPVersion4Protokoll(Daten, ausführenVorgang)) {
            return false;
        }
        int kopfLänge = (Daten[ausführenVorgang] & 0x0f) * 4;
        int gesamtwertLänge = NetzwerkWerkzeuge.großByteordnungKurz(Daten, ausführenVorgang + 2);
        if (gesamtwertLänge < kopfLänge || ausführenVorgang + gesamtwertLänge > Daten.length) {
            return false;
        }
        int vertragWert = Daten[ausführenVorgang + 9] & 0xff;
        int inhaltswertStarten = ausführenVorgang + kopfLänge;
        int inhaltswertLänge = gesamtwertLänge - kopfLänge;
        datenBehandler DirektBehandler = InternetProtokollBehandler.get(Integer.valueOf(vertragWert));
        if (DirektBehandler != null) {
            DirektBehandler.prozessWertEintrag(Daten, inhaltswertStarten, inhaltswertLänge);
            return true;
        }
        if (inhaltswertLänge < 4) {
            return false;
        }
        int zielPortNummer = NetzwerkWerkzeuge.großByteordnungKurz(Daten, inhaltswertStarten + 2);
        Map<Integer, datenBehandler> portTabelle = vertragWert == 17 ? benutzerDatenEinheitBehandler : vertragWert == 6 ? DatenübermittlungSteuerungBehandler : null;
        if (portTabelle == null) {
            return false;
        }
        datenBehandler portBehandler = portTabelle.get(Integer.valueOf(zielPortNummer));
        if (portBehandler == null) {
            return false;
        }
        portBehandler.prozessWertEintrag(Daten, inhaltswertStarten, inhaltswertLänge);
        return true;
    }
}

