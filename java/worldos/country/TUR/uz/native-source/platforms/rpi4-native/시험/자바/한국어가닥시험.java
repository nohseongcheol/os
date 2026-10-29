// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void Ishga_tushirish() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { 합계++; 작업가닥.YIELD_vazifa(); }
    }
    public static void Bajarish() throws 대기중단예외 {
        한국어가닥시험 vazifa_harakat = new 한국어가닥시험();
        작업가닥 oqim_VALUE_5b72a632 = new 작업가닥(vazifa_harakat);
        검사.참인지(!oqim_VALUE_5b72a632.살아있는가(), "Bajarish 전 holat_VALUE_e10195a1");
        검사.참인지(!((Object)oqim_VALUE_5b72a632 instanceof Thread), "표준 가닥과 독립된 format_VALUE");
        oqim_VALUE_5b72a632.Start_vazifa(); oqim_VALUE_5b72a632.기다리기();
        검사.참인지(vazifa_harakat.합계 == 100 && !oqim_VALUE_5b72a632.살아있는가(), "한글 oqim_VALUE_5b72a632 실행과 bir_daqiqa_holat");
        try { oqim_VALUE_5b72a632.Start_vazifa(); 검사.참인지(false, "중복 Bajarish 거부"); }
        catch (oqim_holat_istisno Xato) { 출력.yozmoq_satr("한국어 oqim_VALUE_5b72a632 중복 Bajarish 거부"); }
        작업가닥 Keyingi_oqim = 작업.Bajarish(vazifa_harakat); 작업.기다리기(Keyingi_oqim);
        검사.참인지(vazifa_harakat.합계 == 200 && !작업.살아있는가(Keyingi_oqim), "한국어 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.element_COUNT() == 0, "빈 bajarmoq_buyruq 인수");
        try { 실행인수.Matn(0); 검사.참인지(false, "인수 klip 검사"); }
        catch (범위예외 Xato) { 출력.yozmoq_satr("한국어 인수 klip 거부"); }
        출력.yozmoq_satr("한국어 직접 oqim_VALUE_5b72a632 통과");
    }
}
