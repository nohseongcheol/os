// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.체계호출;

public final class sistema_Išsami_informacija {
    private final String sistema_pavadinimas;
    private final String mazgas_pavadinimas;
    private final String leidimas_VALUE;
    private final String versija_VALUE;
    private final String mašina;

    public sistema_Išsami_informacija(String sistema_pavadinimas, String mazgas_pavadinimas, String leidimas_VALUE, String versija_VALUE, String mašina) {
        this.sistema_pavadinimas = sistema_pavadinimas;
        this.mazgas_pavadinimas = mazgas_pavadinimas;
        this.leidimas_VALUE = leidimas_VALUE;
        this.versija_VALUE = versija_VALUE;
        this.mašina = mašina;
    }

    public String sistema_pavadinimas() { return sistema_pavadinimas; }
    public String mazgas_pavadinimas() { return mazgas_pavadinimas; }
    public String leidimas_VALUE() { return leidimas_VALUE; }
    public String versija_VALUE() { return versija_VALUE; }
    public String mašina() { return mašina; }
}
