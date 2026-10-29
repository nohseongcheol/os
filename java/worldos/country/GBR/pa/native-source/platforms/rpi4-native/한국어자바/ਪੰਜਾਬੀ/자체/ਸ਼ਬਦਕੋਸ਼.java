// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
import java.util.HashMap;
/** ਸ਼ਬਦਕੋਸ਼(辭典): 찾는 ਸ਼ਬਦ_ਪਾਠ(열쇠)에 값을 대응시킨다. */
public final class ਸ਼ਬਦਕੋਸ਼ {
    private final HashMap<String, String> ਦਾਖਲਾ_ਕੀਮਤ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ਕੀਮਤ) { return ਦਾਖਲਾ_ਕੀਮਤ.put(열쇠, ਕੀਮਤ); }
    public String ਲੱਭੋ_ਦਾਖਲਾ(String 열쇠) { return ਦਾਖਲਾ_ਕੀਮਤ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return ਦਾਖਲਾ_ਕੀਮਤ.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return ਦਾਖਲਾ_ਕੀਮਤ.remove(열쇠); }
    public int ਆਕਾਰ() { return ਦਾਖਲਾ_ਕੀਮਤ.size(); }
    public void ਹਟਾਓ_ਤਤਕਰਾ() { ਦਾਖਲਾ_ਕੀਮਤ.clear(); }
}
