// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
import java.util.HashMap;
/** słownik(辭典): 찾는 Word_SMS(Klucz_materiał)에 값을 대응시킨다. */
public final class słownik {
    private final HashMap<String, String> wpis_WARTOŚĆ = new HashMap<String, String>();
    public String 넣기(String Klucz_materiał, String WARTOŚĆ) { return wpis_WARTOŚĆ.put(Klucz_materiał, WARTOŚĆ); }
    public String ZNAJDŹ_wpis(String Klucz_materiał) { return wpis_WARTOŚĆ.get(Klucz_materiał); }
    public boolean 있는가(String Klucz_materiał) { return wpis_WARTOŚĆ.containsKey(Klucz_materiał); }
    public String usunąć_wpis(String Klucz_materiał) { return wpis_WARTOŚĆ.remove(Klucz_materiał); }
    public int Rozmiar() { return wpis_WARTOŚĆ.size(); }
    public void czyścić_Spis_treści() { wpis_WARTOŚĆ.clear(); }
}
