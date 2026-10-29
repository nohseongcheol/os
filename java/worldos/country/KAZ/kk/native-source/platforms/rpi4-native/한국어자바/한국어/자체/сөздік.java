// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** сөздік(辭典): 찾는 Сөз_Мәтін(열쇠)에 값을 대응시킨다. */
public final class сөздік {
    private final HashMap<String, String> енгізу_мән = new HashMap<String, String>();
    public String 넣기(String 열쇠, String мән) { return енгізу_мән.put(열쇠, мән); }
    public String Табу_енгізу(String 열쇠) { return енгізу_мән.get(열쇠); }
    public boolean 있는가(String 열쇠) { return енгізу_мән.containsKey(열쇠); }
    public String өшіру_енгізу(String 열쇠) { return енгізу_мән.remove(열쇠); }
    public int Өлшемі() { return енгізу_мән.size(); }
    public void тазалау_Мазмұны() { енгізу_мән.clear(); }
}
