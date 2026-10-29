// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package België.JBelOS.작업;

import België.JBelOS.Geheugen_regio.Paginabeheer;
import België.JBelOS.bestandssysteem.파일서술자표;

public final class Proces_WAARDE {
    private final int id_WAARDE;
    private final int bovenliggend_id;
    private final Paginabeheer.adresruimte adresruimte;
    private final 파일서술자표 파일서술자;
    private Proces_Status Status_WAARDE = Proces_Status.Bereid_voor;
    private int afsluitcode;
    private int app_pauze = 0x06000000;
    private int uitvoerbewerking_START_ADRES;
    private String[] uitvoerbewerking_argument = new String[0];
    private String[] omgeving_WAARDE = new String[0];

    Proces_WAARDE(int id_WAARDE, int bovenliggend_id, Paginabeheer.adresruimte adresruimte, 파일서술자표 파일서술자) {
        this.id_WAARDE = id_WAARDE;
        this.bovenliggend_id = bovenliggend_id;
        this.adresruimte = adresruimte;
        this.파일서술자 = 파일서술자;
    }

    public int id_WAARDE() {
        return id_WAARDE;
    }

    public int bovenliggend_id() {
        return bovenliggend_id;
    }

    public Paginabeheer.adresruimte adresruimte() {
        return adresruimte;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public Proces_Status Status_WAARDE() {
        return Status_WAARDE;
    }

    public void set_Status(Proces_Status 새상태) {
        Status_WAARDE = 새상태;
    }

    public int afsluitcode() {
        return afsluitcode;
    }

    public void Einde_app(int WAARDE) {
        afsluitcode = WAARDE & 0xff;
        Status_WAARDE = Proces_Status.Einde_app;
    }

    public int app_pauze() {
        return app_pauze;
    }

    public void set_app_pauze(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_pauze = 새끝;
    }

    public void set_uitvoerbewerking_context(int START_ADRES, String[] parameter_argument, String[] omgeving) {
        uitvoerbewerking_START_ADRES = START_ADRES;
        uitvoerbewerking_argument = parameter_argument.clone();
        omgeving_WAARDE = omgeving.clone();
    }

    public int uitvoerbewerking_START_ADRES() { return uitvoerbewerking_START_ADRES; }
    public String[] uitvoerbewerking_argument() { return uitvoerbewerking_argument.clone(); }
    public String[] omgeving_WAARDE() { return omgeving_WAARDE.clone(); }
}
