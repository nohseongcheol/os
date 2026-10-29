// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** savs JVM과 커널의 Logs 관리 기능에 직접 연결되는 Logs. */
public final class Logs extends 화면구성요소 {
    public Logs(String logs_nosaukums, int 폭, int 높이) {
        throw new Statuss_izņēmums("savs JVM의 Latviešu Logs ģenerēt 기능이 필요합니다.");
    }
    public native void Pievienot_elements(화면구성요소 elements_VALUE);
    public native void rādīt_logs();
    public native void Aizvērt();
    public native boolean 보이는가();
}
