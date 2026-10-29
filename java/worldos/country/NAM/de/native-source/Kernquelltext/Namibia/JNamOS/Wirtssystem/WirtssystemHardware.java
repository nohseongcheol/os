// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Namibia.JNamOS.Wirtssystem;

import java.util.HashMap;
import java.util.Map;
import Namibia.JNamOS.Betriebskern.hardwareWert;

/** Hardwareersatz für deterministische Tests des verwalteten Kernels auf einer gewöhnlichen JVM. */
public final class WirtssystemHardware implements hardwareWert {
    private final Map<Integer, Integer> hardwarePortWert = new HashMap<Integer, Integer>();
    private final StringBuilder seriellProtokolldatei = new StringBuilder();

    @Override
    public void seriellAusgabe(String inhaltswertWert) {
        seriellProtokolldatei.append(inhaltswertWert);
        System.out.print(inhaltswertWert);
    }

    @Override
    public int portByteLesen(int hardwarePortNummer) {
        Integer Wert = hardwarePortWert.get(Integer.valueOf(hardwarePortNummer));
        return Wert == null ? 0 : Wert.intValue();
    }

    @Override
    public void portByteSchreiben(int hardwarePortNummer, int Wert) {
        hardwarePortWert.put(Integer.valueOf(hardwarePortNummer), Integer.valueOf(Wert & 0xff));
    }

    @Override
    public void anhaltenCPU() {
        // In Host-Tests sofort zurückkehren, statt auf das nächste Ereignis zu warten.
    }

    public String seriellProtokolldatei() {
        return seriellProtokolldatei.toString();
    }
}

