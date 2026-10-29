// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Venäjä.JRusOS.järjestelmäkutsu;

public final class Järjestelmä_Tiedot {
    private final String Järjestelmä_nimi;
    private final String solmu_nimi;
    private final String versio_ARVO_237a4c94;
    private final String versio_ARVO;
    private final String kone;

    public Järjestelmä_Tiedot(String Järjestelmä_nimi, String solmu_nimi, String versio_ARVO_237a4c94, String versio_ARVO, String kone) {
        this.Järjestelmä_nimi = Järjestelmä_nimi;
        this.solmu_nimi = solmu_nimi;
        this.versio_ARVO_237a4c94 = versio_ARVO_237a4c94;
        this.versio_ARVO = versio_ARVO;
        this.kone = kone;
    }

    public String Järjestelmä_nimi() { return Järjestelmä_nimi; }
    public String solmu_nimi() { return solmu_nimi; }
    public String versio_ARVO_237a4c94() { return versio_ARVO_237a4c94; }
    public String versio_ARVO() { return versio_ARVO; }
    public String kone() { return kone; }
}
