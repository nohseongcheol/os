// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.체계호출;

public final class sistēma_Detalizēti {
    private final String sistēma_nosaukums;
    private final String mezgls_nosaukums;
    private final String izdevums_VALUE;
    private final String versija_VALUE;
    private final String mašīna;

    public sistēma_Detalizēti(String sistēma_nosaukums, String mezgls_nosaukums, String izdevums_VALUE, String versija_VALUE, String mašīna) {
        this.sistēma_nosaukums = sistēma_nosaukums;
        this.mezgls_nosaukums = mezgls_nosaukums;
        this.izdevums_VALUE = izdevums_VALUE;
        this.versija_VALUE = versija_VALUE;
        this.mašīna = mašīna;
    }

    public String sistēma_nosaukums() { return sistēma_nosaukums; }
    public String mezgls_nosaukums() { return mezgls_nosaukums; }
    public String izdevums_VALUE() { return izdevums_VALUE; }
    public String versija_VALUE() { return versija_VALUE; }
    public String mašīna() { return mašīna; }
}
