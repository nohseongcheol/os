// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.체계호출;

public final class System_Detaljer {
    private final String System_navn;
    private final String node_navn;
    private final String utgave_Edition_VERDI;
    private final String versjon_VERDI;
    private final String maskin;

    public System_Detaljer(String System_navn, String node_navn, String utgave_Edition_VERDI, String versjon_VERDI, String maskin) {
        this.System_navn = System_navn;
        this.node_navn = node_navn;
        this.utgave_Edition_VERDI = utgave_Edition_VERDI;
        this.versjon_VERDI = versjon_VERDI;
        this.maskin = maskin;
    }

    public String System_navn() { return System_navn; }
    public String node_navn() { return node_navn; }
    public String utgave_Edition_VERDI() { return utgave_Edition_VERDI; }
    public String versjon_VERDI() { return versjon_VERDI; }
    public String maskin() { return maskin; }
}
