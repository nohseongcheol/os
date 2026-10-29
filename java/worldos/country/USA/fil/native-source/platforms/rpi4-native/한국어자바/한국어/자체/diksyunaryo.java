// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** diksyunaryo(辭典): 찾는 Word_SMS(열쇠)에 값을 대응시킨다. */
public final class diksyunaryo {
    private final HashMap<String, String> pagpasok_VALUE = new HashMap<String, String>();
    public String 넣기(String 열쇠, String VALUE) { return pagpasok_VALUE.put(열쇠, VALUE); }
    public String FIND_pagpasok(String 열쇠) { return pagpasok_VALUE.get(열쇠); }
    public boolean 있는가(String 열쇠) { return pagpasok_VALUE.containsKey(열쇠); }
    public String burahin_pagpasok(String 열쇠) { return pagpasok_VALUE.remove(열쇠); }
    public int sukat_82232621() { return pagpasok_VALUE.size(); }
    public void i_clear_TOC() { pagpasok_VALUE.clear(); }
}
