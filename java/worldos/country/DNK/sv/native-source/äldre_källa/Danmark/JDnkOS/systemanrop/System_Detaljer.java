// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.systemanrop;

public final class System_Detaljer {
    private final String System_namn;
    private final String nod_namn;
    private final String utgåva_värde;
    private final String version_värde;
    private final String dator;

    public System_Detaljer(String System_namn, String nod_namn, String utgåva_värde, String version_värde, String dator) {
        this.System_namn = System_namn;
        this.nod_namn = nod_namn;
        this.utgåva_värde = utgåva_värde;
        this.version_värde = version_värde;
        this.dator = dator;
    }

    public String System_namn() { return System_namn; }
    public String nod_namn() { return nod_namn; }
    public String utgåva_värde() { return utgåva_värde; }
    public String version_värde() { return version_värde; }
    public String dator() { return dator; }
}
