// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

public class 한국어예외시험 {
    static void 표준시간제한() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 예외");
    }
    public static void main(String[] 인수) throws 입출력예외 {
        try { throw new 대기시간초과예외("기다림 끝"); }
        catch (대기시간초과예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 주소확인예외("주소 실패"); }
        catch (입출력예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 파일없음예외("Dosya 실패"); }
        catch (java.io.IOException Hata) { 출력.줄쓰기("표준 상위 예외 호환"); }
        try { 표준시간제한(); }
        catch (대기시간초과예외 잘못잡힘) { 출력.줄쓰기("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { 출력.줄쓰기("한국어 예외의 독립된 유형"); }
        try { Dosya.Okuma("없는한글파일"); }
        catch (파일없음예외 Hata) { 출력.줄쓰기("Dosya Hata 한국어 변환"); }
        try { 문자.정수읽기("숫자가아님"); }
        catch (숫자형식예외 Hata) { 출력.줄쓰기("숫자 Hata 한국어 변환"); }
        try { 검사.참인지(false, "검사 실패"); }
        catch (잘못된인수예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 배열범위예외("범위 실패"); }
        catch (범위예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 빈참조예외("빈 참조"); }
        catch (java.lang.RuntimeException Hata) { 출력.줄쓰기("실행 예외 호환"); }
        try { throw new 예외("직접 정의한 설명"); }
        catch (예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 가닥상태예외("가닥상태예외"); }
        catch (가닥상태예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 대기시간초과예외("대기시간초과예외"); }
        catch (대기시간초과예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 배열저장예외("배열저장예외"); }
        catch (배열저장예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 빈참조예외("빈참조예외"); }
        catch (빈참조예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 상태예외("상태예외"); }
        catch (상태예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 예외("예외"); }
        catch (예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 입출력예외("입출력예외"); }
        catch (입출력예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 잘못된인수예외("잘못된인수예외"); }
        catch (잘못된인수예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 주소확인예외("주소확인예외"); }
        catch (주소확인예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        try { throw new 형변환예외("형변환예외"); }
        catch (형변환예외 Hata) { 출력.줄쓰기(Hata.설명()); }
        출력.줄쓰기("한국어 예외 처리 완료");
    }
}
