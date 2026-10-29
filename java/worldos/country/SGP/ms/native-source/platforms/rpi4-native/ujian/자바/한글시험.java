// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.Asli.문자;
import Melayu.Asli.Fail;
import Melayu.Asli.pemasukan_Senarai;
import Melayu.Asli.kamus;
import Melayu.Asli.출력;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        출력.tulis_baris(문자.nyahsulit_data(문자.부호화(인사))); 출력.수쓰기(문자.titik_kod_COUNT("한글😀"));
        Fail.Tulis("한글자료.txt", 인사); 출력.tulis_baris(Fail.Baca("한글자료.txt"));
        pemasukan_Senarai 이름들 = new pemasukan_Senarai(); 이름들.더하기("가람"); 이름들.더하기("누리"); 출력.tulis_baris(이름들.Baca(1));
        kamus 뜻 = new kamus(); 뜻.넣기("가람", "강"); System.gc(); 출력.tulis_baris(뜻.Cari_pemasukan("가람"));
        try { 문자.nyahsulit_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 출력.tulis_baris("UTF-8 RALAT tolak_VALUE"); }
        출력.tulis_baris("Melayu pustaka 완료");
    }
}
