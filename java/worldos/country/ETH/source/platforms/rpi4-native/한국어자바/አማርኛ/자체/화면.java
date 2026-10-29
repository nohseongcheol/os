// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 화면(畫面): 부팅 때 선택한 크기의 자체 ዓንኳር_እሴት RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int እሴት = ዓንኳር_እሴት.화면너비(); if (እሴት < 0) throw new ዞን_ልዩነት("프레임버퍼 없음"); return እሴት; }
    public static int 높이() { int እሴት = ዓንኳር_እሴት.화면높이(); if (እሴት < 0) throw new ዞን_ልዩነት("프레임버퍼 없음"); return እሴት; }
    public static void 사각형(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int 높이, int 색) {
        if (가로 < 0 || ቋሚ_በቦታ_አስቀመጠ < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || ቋሚ_በቦታ_አስቀመጠ > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - ቋሚ_በቦታ_አስቀመጠ) throw new ልክ_ያልኾነ_ነጋሪ_እሴት_ልዩነት("화면 ቅንጥብ");
        if (ዓንኳር_እሴት.사각형(가로, ቋሚ_በቦታ_አስቀመጠ, 폭, 높이, 색) < 0) throw new ዞን_ልዩነት("프레임버퍼 없음");
    }
    public static void አስወግድ_ምዝግብ_c8dbc399(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (ዓንኳር_እሴት.그림대기() < 0) throw new ዞን_ልዩነት("በይነተገናኝ 입력 필요"); }
}
