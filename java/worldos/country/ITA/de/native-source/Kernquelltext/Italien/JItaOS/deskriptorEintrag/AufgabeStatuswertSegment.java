// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italien.JItaOS.deskriptorEintrag;

/** Verwaltete TSS-Darstellung, die bei x86-Aufgabenwechseln einen privilegierten Stapel bereitstellt. */
public final class AufgabeStatuswertSegment {
    private int stapelNullwertBlock;
    private int stapelNullwertAdresse;
    private int einAusgabeErlaubnisTabellePosition = 104;

    public void bevorrechtigtStapelSetzen(int fragmentWert, int adresse) {
        stapelNullwertBlock = fragmentWert;
        stapelNullwertAdresse = adresse;
    }

    public int stapelNullwertBlock() { return stapelNullwertBlock; }
    public int stapelNullwertAdresse() { return stapelNullwertAdresse; }
    public int einAusgabeErlaubnisTabellePosition() { return einAusgabeErlaubnisTabellePosition; }
}

