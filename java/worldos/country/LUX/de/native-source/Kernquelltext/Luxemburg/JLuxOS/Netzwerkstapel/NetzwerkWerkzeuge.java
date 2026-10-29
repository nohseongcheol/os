// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburg.JLuxOS.Netzwerkstapel;

/** Gemeinsame Hilfen für Bytereihenfolge und Prüfsummen der Ethernet/ARP/IPv4/ICMP/UDP-Schichten. */
public final class NetzwerkWerkzeuge {
    private NetzwerkWerkzeuge() {
    }

    public static int großByteordnungKurz(byte[] Daten, int position) {
        bereichPrüfen(Daten, position, 2);
        return ((Daten[position] & 0xff) << 8) | (Daten[position + 1] & 0xff);
    }

    public static long großByteordnungGanzzahl(byte[] Daten, int position) {
        bereichPrüfen(Daten, position, 4);
        return ((long) (Daten[position] & 0xff) << 24)
                | ((long) (Daten[position + 1] & 0xff) << 16)
                | ((long) (Daten[position + 2] & 0xff) << 8)
                | (Daten[position + 3] & 0xffL);
    }

    public static int internetKontrollsumme(byte[] Daten, int ausführenVorgang, int Länge) {
        bereichPrüfen(Daten, ausführenVorgang, Länge);
        long summeWert = 0;
        int endung = ausführenVorgang + Länge;
        int position = ausführenVorgang;
        while (position + 1 < endung) {
            summeWert += großByteordnungKurz(Daten, position);
            position += 2;
        }
        if (position < endung) {
            summeWert += (Daten[position] & 0xff) << 8;
        }
        while ((summeWert >>> 16) != 0) {
            summeWert = (summeWert & 0xffff) + (summeWert >>> 16);
        }
        return (int) (~summeWert) & 0xffff;
    }

    public static boolean istEthernetRahmen(byte[] Daten) {
        return Daten != null && Daten.length >= 14;
    }

    public static int ethernetObererProtokoll(byte[] Daten) {
        if (!istEthernetRahmen(Daten)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return großByteordnungKurz(Daten, 12);
    }

    public static boolean istIPVersion4Protokoll(byte[] Daten, int position) {
        if (Daten == null || position < 0 || Daten.length - position < 20) {
            return false;
        }
        int versionWert = (Daten[position] >>> 4) & 0xf;
        int kopfLänge = (Daten[position] & 0xf) * 4;
        return versionWert == 4 && kopfLänge >= 20 && Daten.length - position >= kopfLänge;
    }

    private static void bereichPrüfen(byte[] Daten, int ausführenVorgang, int Länge) {
        if (Daten == null || ausführenVorgang < 0 || Länge < 0 || ausführenVorgang > Daten.length - Länge) {
            throw new IllegalArgumentException("Netzwerkstapel Daten 범위를 벗어났습니다.");
        }
    }
}

