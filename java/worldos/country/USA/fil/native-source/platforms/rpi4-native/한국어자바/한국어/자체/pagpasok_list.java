// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** pagpasok_list(目錄): 순서가 있는 항목의 모음. 이 판은 string_VALUE 목록을 제공한다. */
public final class pagpasok_list {
    private final ArrayList<String> pagpasok_VALUE = new ArrayList<String>();
    public void 더하기(String VALUE) { pagpasok_VALUE.add(VALUE); }
    public String 읽기(int pagkakasunud_sunod_VALUE) { return pagpasok_VALUE.get(pagkakasunud_sunod_VALUE); }
    public String REPLACE_VALUE(int pagkakasunud_sunod_VALUE, String VALUE) { return pagpasok_VALUE.set(pagkakasunud_sunod_VALUE, VALUE); }
    public String burahin_pagpasok(int pagkakasunud_sunod_VALUE) { return pagpasok_VALUE.remove(pagkakasunud_sunod_VALUE); }
    public int sukat_82232621() { return pagpasok_VALUE.size(); }
    public boolean information_technology_walang_laman_VALUE() { return pagpasok_VALUE.isEmpty(); }
    public void i_clear_TOC() { pagpasok_VALUE.clear(); }
}
