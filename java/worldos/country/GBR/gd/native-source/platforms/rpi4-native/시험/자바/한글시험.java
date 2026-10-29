// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.문자;
import 한국어.자체.faidhle;
import 한국어.자체.cur_a_steach_Liosta;
import 한국어.자체.faclair;
import 한국어.자체.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.sgrìobh_loidhne(문자.dì_chrioptaich_dàta(문자.부호화(인사))); 출력.수쓰기(문자.còd_a_charactair_COUNT("한글😀"));
        faidhle.sgrìobh("한글자료.txt", 인사); 출력.sgrìobh_loidhne(faidhle.읽기("한글자료.txt"));
        cur_a_steach_Liosta 이름들 = new cur_a_steach_Liosta(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.sgrìobh_loidhne(이름들.읽기(1));
        faclair 뜻 = new faclair(); 뜻.넣기("가람", "강"); System.gc(); 출력.sgrìobh_loidhne(뜻.FIND_cur_a_steach("가람"));
        try { 문자.dì_chrioptaich_dàta(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.sgrìobh_loidhne("UTF-8 Mearachd 거부"); }
        출력.sgrìobh_loidhne("한국어 leabhar_lann 완료");
    }
}
