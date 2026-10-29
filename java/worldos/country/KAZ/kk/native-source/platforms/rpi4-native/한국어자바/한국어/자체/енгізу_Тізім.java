// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** енгізу_Тізім(目錄): 순서가 있는 항목의 모음. 이 판은 жол_мән_6ca8363c 목록을 제공한다. */
public final class енгізу_Тізім {
    private final ArrayList<String> енгізу_мән = new ArrayList<String>();
    public void 더하기(String мән) { енгізу_мән.add(мән); }
    public String Оқу(int рет_мән) { return енгізу_мән.get(рет_мән); }
    public String ауыстыру_мән(int рет_мән, String мән) { return енгізу_мән.set(рет_мән, мән); }
    public String өшіру_енгізу(int рет_мән) { return енгізу_мән.remove(рет_мән); }
    public int Өлшемі() { return енгізу_мән.size(); }
    public boolean 비었는가() { return енгізу_мән.isEmpty(); }
    public void тазалау_Мазмұны() { енгізу_мән.clear(); }
}
