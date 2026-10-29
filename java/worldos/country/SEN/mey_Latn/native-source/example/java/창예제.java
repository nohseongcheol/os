// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.창;
import 한국어.자체.글표지;
import 한국어.자체.입력칸;
import 한국어.자체.단추;
import 한국어.자체.화면일정;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing 창: mey_Latn 입력 → 단추 → 안내 글 갱신. */
public class 창예제 implements 실행할일, 동작받이 {
    private 창 인사창;
    private 입력칸 이름입력;
    private 글표지 인사말;
    private int 인사횟수;

    public void 창열기() {
        인사창 = new 창("mey_Latn Swing", 460, 300);
        인사창.담기(new 글표지("mey_Latn", 20, 20, 420, 28));
        이름입력 = new 입력칸("mey_Latn", 20, 64, 420, 30);
        인사말 = new 글표지("mey_Latn", 20, 152, 420, 28);
        인사창.담기(이름입력);
        인사창.담기(new 단추("인사하기", 20, 108, 180, 32, this));
        인사창.담기(인사말);
        인사창.담기(new 글표지("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.보이기();
        출력.줄쓰기("GUI 예제 준비: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.글쓰기("mey_Latn, " + 이름입력.글읽기() + "님! (" + 인사횟수 + ")");
        출력.줄쓰기("GUI 인사: " + 인사말.글읽기());
    }

    public void 실행하기() { 창열기(); }
    public void 동작받기(동작알림 알림) {
        출력.줄쓰기("동작 알림: " + 알림.명령글());
        인사하기();
    }
    public static void 시작() {
        화면일정.나중에실행(new 창예제());
    }
}
