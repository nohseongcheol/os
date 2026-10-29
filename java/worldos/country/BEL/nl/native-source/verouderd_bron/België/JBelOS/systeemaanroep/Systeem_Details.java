// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package België.JBelOS.systeemaanroep;

public final class Systeem_Details {
    private final String Systeem_naam;
    private final String knooppunt_naam;
    private final String editie_WAARDE;
    private final String versie_WAARDE;
    private final String machine;

    public Systeem_Details(String Systeem_naam, String knooppunt_naam, String editie_WAARDE, String versie_WAARDE, String machine) {
        this.Systeem_naam = Systeem_naam;
        this.knooppunt_naam = knooppunt_naam;
        this.editie_WAARDE = editie_WAARDE;
        this.versie_WAARDE = versie_WAARDE;
        this.machine = machine;
    }

    public String Systeem_naam() { return Systeem_naam; }
    public String knooppunt_naam() { return knooppunt_naam; }
    public String editie_WAARDE() { return editie_WAARDE; }
    public String versie_WAARDE() { return versie_WAARDE; }
    public String machine() { return machine; }
}
