// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bulgarien.JBgrOS.Betriebskern;

/** Einzige Grenze zwischen Java-verwaltetem Kernel und CPU-spezifischem Code. */
public interface hardwareWert {
    void seriellAusgabe(String inhaltswertWert);

    int portByteLesen(int hardwarePortNummer);

    void portByteSchreiben(int hardwarePortNummer, int Wert);

    void anhaltenCPU();
}

