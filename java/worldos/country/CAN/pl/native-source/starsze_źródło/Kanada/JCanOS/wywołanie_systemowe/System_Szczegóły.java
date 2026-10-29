// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.wywołanie_systemowe;

public final class System_Szczegóły {
    private final String System_nazwa;
    private final String węzeł_nazwa;
    private final String wersja_WARTOŚĆ_237a4c94;
    private final String wersja_WARTOŚĆ;
    private final String maszyna;

    public System_Szczegóły(String System_nazwa, String węzeł_nazwa, String wersja_WARTOŚĆ_237a4c94, String wersja_WARTOŚĆ, String maszyna) {
        this.System_nazwa = System_nazwa;
        this.węzeł_nazwa = węzeł_nazwa;
        this.wersja_WARTOŚĆ_237a4c94 = wersja_WARTOŚĆ_237a4c94;
        this.wersja_WARTOŚĆ = wersja_WARTOŚĆ;
        this.maszyna = maszyna;
    }

    public String System_nazwa() { return System_nazwa; }
    public String węzeł_nazwa() { return węzeł_nazwa; }
    public String wersja_WARTOŚĆ_237a4c94() { return wersja_WARTOŚĆ_237a4c94; }
    public String wersja_WARTOŚĆ() { return wersja_WARTOŚĆ; }
    public String maszyna() { return maszyna; }
}
