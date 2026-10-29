// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Niederlande.JNldOS.Eingabewert;

public final class eingabeEreignis {
    public enum artWert {
        tasteAbwärts,
        tasteAufwärts,
        mausBewegung,
        mausSchaltflächeGedrückt,
        mausSchaltflächeFreigegeben
    }

    private final artWert ereignisArt;
    private final int ersterWert;
    private final int zweiterWert;

    public eingabeEreignis(artWert ereignisArt, int ersterWert, int zweiterWert) {
        this.ereignisArt = ereignisArt;
        this.ersterWert = ersterWert;
        this.zweiterWert = zweiterWert;
    }

    public artWert ereignisArt() {
        return ereignisArt;
    }

    public int ersterWert() {
        return ersterWert;
    }

    public int zweiterWert() {
        return zweiterWert;
    }
}

