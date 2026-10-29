// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** մուտքագրում_Ցուցակ(目錄): 순서가 있는 항목의 모음. 이 판은 տող_արժեք_6ca8363c 목록을 제공한다. */
public final class մուտքագրում_Ցուցակ {
    private final ArrayList<String> մուտքագրում_արժեք = new ArrayList<String>();
    public void 더하기(String արժեք) { մուտքագրում_արժեք.add(արժեք); }
    public String Ընթերցում(int կարգ_արժեք) { return մուտքագրում_արժեք.get(կարգ_արժեք); }
    public String փոխարինել_արժեք(int կարգ_արժեք, String արժեք) { return մուտքագրում_արժեք.set(կարգ_արժեք, արժեք); }
    public String 지우기(int կարգ_արժեք) { return մուտքագրում_արժեք.remove(կարգ_արժեք); }
    public int Չափս() { return մուտքագրում_արժեք.size(); }
    public boolean 비었는가() { return մուտքագրում_արժեք.isEmpty(); }
    public void մաքրել_բովանդակություն() { մուտքագրում_արժեք.clear(); }
}
