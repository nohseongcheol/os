// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class WerkzeugEintrag {
    public static int ausführenVorgang() {
        return Benutzer.werkzeugNummer() == 0 ? JavaÜbersetzer.ausführenVorgang() : VirtuelleJavaMaschine.ausführenVorgang();
    }
}
