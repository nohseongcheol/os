// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
import java.util.ArrayList;
/** wpis_Lista(目錄): 순서가 있는 항목의 모음. 이 판은 ciąg_WARTOŚĆ 목록을 제공한다. */
public final class wpis_Lista {
    private final ArrayList<String> wpis_WARTOŚĆ = new ArrayList<String>();
    public void 더하기(String WARTOŚĆ) { wpis_WARTOŚĆ.add(WARTOŚĆ); }
    public String Odczyt(int zamówić_WARTOŚĆ) { return wpis_WARTOŚĆ.get(zamówić_WARTOŚĆ); }
    public String ZASTĄP_WARTOŚĆ(int zamówić_WARTOŚĆ, String WARTOŚĆ) { return wpis_WARTOŚĆ.set(zamówić_WARTOŚĆ, WARTOŚĆ); }
    public String usunąć_wpis(int zamówić_WARTOŚĆ) { return wpis_WARTOŚĆ.remove(zamówić_WARTOŚĆ); }
    public int Rozmiar() { return wpis_WARTOŚĆ.size(); }
    public boolean 비었는가() { return wpis_WARTOŚĆ.isEmpty(); }
    public void czyścić_Spis_treści() { wpis_WARTOŚĆ.clear(); }
}
