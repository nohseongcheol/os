// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
import java.util.ArrayList;
/** sarrera_Zerrenda(目錄): 순서가 있는 항목의 모음. 이 판은 kate_balio 목록을 제공한다. */
public final class sarrera_Zerrenda {
    private final ArrayList<String> sarrera_balio = new ArrayList<String>();
    public void 더하기(String balio) { sarrera_balio.add(balio); }
    public String Irakurri(int ordena_balio) { return sarrera_balio.get(ordena_balio); }
    public String ORDEZTU_balio(int ordena_balio, String balio) { return sarrera_balio.set(ordena_balio, balio); }
    public String ezabatu_sarrera(int ordena_balio) { return sarrera_balio.remove(ordena_balio); }
    public int Tamaina() { return sarrera_balio.size(); }
    public boolean 비었는가() { return sarrera_balio.isEmpty(); }
    public void garbitu_Edukia() { sarrera_balio.clear(); }
}
