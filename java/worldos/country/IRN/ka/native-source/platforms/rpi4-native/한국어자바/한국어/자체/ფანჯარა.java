// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 ფანჯარა 관리 기능에 직접 연결되는 ფანჯარა. */
public final class ფანჯარა extends 화면구성요소 {
    public ფანჯარა(String ფანჯარა_დასახელება, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 ფანჯარა დაგენერირება 기능이 필요합니다.");
    }
    public native void დამატება_ელემენტი(화면구성요소 ელემენტი_მნიშვნელობა);
    public native void ჩვენება_ფანჯარა();
    public native void დახურვა();
    public native boolean 보이는가();
}
