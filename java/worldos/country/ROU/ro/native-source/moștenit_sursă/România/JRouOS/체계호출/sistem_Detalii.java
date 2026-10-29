// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package România.JRouOS.체계호출;

public final class sistem_Detalii {
    private final String sistem_nume;
    private final String nod_nume;
    private final String ediție_VALUE;
    private final String versiune_VALUE;
    private final String mașină;

    public sistem_Detalii(String sistem_nume, String nod_nume, String ediție_VALUE, String versiune_VALUE, String mașină) {
        this.sistem_nume = sistem_nume;
        this.nod_nume = nod_nume;
        this.ediție_VALUE = ediție_VALUE;
        this.versiune_VALUE = versiune_VALUE;
        this.mașină = mașină;
    }

    public String sistem_nume() { return sistem_nume; }
    public String nod_nume() { return nod_nume; }
    public String ediție_VALUE() { return ediție_VALUE; }
    public String versiune_VALUE() { return versiune_VALUE; }
    public String mașină() { return mașină; }
}
