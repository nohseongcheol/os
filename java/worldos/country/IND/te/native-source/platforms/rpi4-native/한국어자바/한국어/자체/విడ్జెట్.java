// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 కార్యం_మూల్యం. */
public final class విడ్జెట్ {
    private విడ్జెట్() {}
    public static void 나중에실행(실행할일 విధి_చర్య) { ఈవెంట్_నిరీక్షణ_క్రమం.나중에실행(విధి_చర్య); }
    public static లేబుల్ టాగ్_మూల్యం(String పాఠ్యము, int 가로, int నిలువు_స్థాయి, int 폭, int 높이) {
        return new లేబుల్(పాఠ్యము, 가로, నిలువు_స్థాయి, 폭, 높이);
    }
    public static బటన్ బటన్(String పాఠ్యము, int 가로, int నిలువు_స్థాయి, int 폭, int 높이, 동작받이 받이) {
        return new బటన్(పాఠ్యము, 가로, నిలువు_స్థాయి, 폭, 높이, 받이);
    }
    public static పాఠం_ఫీల్డ్ పాఠం_ఫీల్డ్(String పాఠ్యము, int 가로, int నిలువు_స్థాయి, int 폭, int 높이) {
        return new పాఠం_ఫీల్డ్(పాఠ్యము, 가로, నిలువు_స్థాయి, 폭, 높이);
    }
}
