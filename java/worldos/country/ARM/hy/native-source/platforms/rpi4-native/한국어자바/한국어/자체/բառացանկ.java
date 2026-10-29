// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** բառացանկ(辭典): 찾는 Բառ_Գրվածք(열쇠)에 값을 대응시킨다. */
public final class բառացանկ {
    private final HashMap<String, String> մուտքագրում_արժեք = new HashMap<String, String>();
    public String 넣기(String 열쇠, String արժեք) { return մուտքագրում_արժեք.put(열쇠, արժեք); }
    public String գտնել_մուտքագրում(String 열쇠) { return մուտքագրում_արժեք.get(열쇠); }
    public boolean 있는가(String 열쇠) { return մուտքագրում_արժեք.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return մուտքագրում_արժեք.remove(열쇠); }
    public int Չափս() { return մուտքագրում_արժեք.size(); }
    public void մաքրել_բովանդակություն() { մուտքագրում_արժեք.clear(); }
}
