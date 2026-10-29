// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
import java.util.ArrayList;
/** položka_Zoznam(目錄): 순서가 있는 항목의 모음. 이 판은 reťazec_VALUE 목록을 제공한다. */
public final class položka_Zoznam {
    private final ArrayList<String> položka_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { položka_VALUE.add(VALUE); }
    public String Čítanie(int poradie_VALUE) { return položka_VALUE.get(poradie_VALUE); }
    public String REPLACE_VALUE(int poradie_VALUE, String VALUE) { return položka_VALUE.set(poradie_VALUE, VALUE); }
    public String vymazať_položka(int poradie_VALUE) { return položka_VALUE.remove(poradie_VALUE); }
    public int Veľkosť() { return položka_VALUE.size(); }
    public boolean Informačné_systémy_prázdny_VALUE() { return položka_VALUE.isEmpty(); }
    public void vymazať_Obsah() { položka_VALUE.clear(); }
}
