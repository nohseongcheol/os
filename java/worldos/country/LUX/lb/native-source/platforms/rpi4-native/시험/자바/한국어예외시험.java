// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

public class 한국어예외시험 {
    static void Standard_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 예외");
    }
    public static void main(String[] 인수) throws 입출력예외 {
        try { throw new 대기시간초과예외("Waart_Status 끝"); }
        catch (대기시간초과예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 주소확인예외("Adress Feeler_VALUE"); }
        catch (입출력예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 파일없음예외("Fichier Feeler_VALUE"); }
        catch (java.io.IOException Feeler) { 출력.schreiwen_Zeil("표준 상위 예외 호환"); }
        try { Standard_TIMEOUT(); }
        catch (대기시간초과예외 잘못잡힘) { 출력.schreiwen_Zeil("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { 출력.schreiwen_Zeil("한국어 예외의 독립된 TYPE_Kategorie"); }
        try { Fichier.읽기("없는한글파일"); }
        catch (파일없음예외 Feeler) { 출력.schreiwen_Zeil("Fichier Feeler 한국어 CONVERT_VALUE"); }
        try { 문자.analyséieren_Ganzzuel("숫자가아님"); }
        catch (숫자형식예외 Feeler) { 출력.schreiwen_Zeil("Ziffer_VALUE Feeler 한국어 CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 Feeler_VALUE"); }
        catch (잘못된인수예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 배열범위예외("Clip Feeler_VALUE"); }
        catch (범위예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 빈참조예외("빈 Referenzen"); }
        catch (java.lang.RuntimeException Feeler) { 출력.schreiwen_Zeil("ausféieren_Befeel 예외 호환"); }
        try { throw new 예외("직접 정의한 설명"); }
        catch (예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 가닥상태예외("가닥상태예외"); }
        catch (가닥상태예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 대기시간초과예외("대기시간초과예외"); }
        catch (대기시간초과예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new ARRAY_Store_Feeler("ARRAY_Store_Feeler"); }
        catch (ARRAY_Store_Feeler Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 빈참조예외("빈참조예외"); }
        catch (빈참조예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 상태예외("상태예외"); }
        catch (상태예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 예외("예외"); }
        catch (예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 입출력예외("입출력예외"); }
        catch (입출력예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 잘못된인수예외("잘못된인수예외"); }
        catch (잘못된인수예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 주소확인예외("주소확인예외"); }
        catch (주소확인예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        try { throw new 형변환예외("형변환예외"); }
        catch (형변환예외 Feeler) { 출력.schreiwen_Zeil(Feeler.설명()); }
        출력.schreiwen_Zeil("한국어 예외 Prozess_VALUE_Agab 완료");
    }
}
