// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 لهر_ارزښت: 단일 نوغی_ارزښت 안의 IPv4/UDP 루프백 لېږدول_ارزښت.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * پاى_ټکى 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] درشل_ارزښت = new int[8];
    static int[] پته = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] اوږدوالى_ارزښت = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] اومتوک = new int[32 * 512];
    static int[] 전달 = new int[512];
    static int 다음창구 = 49152;
    static int 확인(int لړیال) { return لړیال >= 32 && لړیال < 40 && 사용[لړیال - 32] != 0 ? لړیال - 32 : -1; }
    static boolean 겹침(int لړیال) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && درشل_ارزښت[칸] == لړیال) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int 만들기(int 영역, int 종류, int کیس_ارزښت) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (کیس_ارزښت != 0 && کیس_ارزښت != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; درشل_ارزښت[칸] = 0; پته[칸] = 0; 앞[칸] = 0; 개수[칸] = 0; 받은창구[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int 묶기(int لړیال, int جال_پته, int 창구번호) {
        int 칸 = 확인(لړیال);
        if (칸 < 0) return -9;
        if (جال_پته != 0 && جال_پته != 0x7f000001) return -99;
        if (درشل_ارزښت[칸] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        درشل_ارزښت[칸] = 창구번호; پته[칸] = جال_پته; return 0;
    }
    public static int 자료넣기(int لړیال, int ارزښت) {
        if (لړیال < 0 || لړیال >= 512) return -22;
        전달[لړیال] = ارزښت & 255; return 0;
    }
    public static int 자료읽기(int لړیال) { return لړیال >= 0 && لړیال < 512 ? 전달[لړیال] : -22; }
    public static int استول(int لړیال, int جال_پته, int 창구번호, int کچ) {
        int 칸 = 확인(لړیال);
        if (칸 < 0) return -9;
        if (جال_پته != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (کچ < 0 || کچ > 512) return -90;
        if (درشل_ارزښت[칸] == 0) {
            int 결과 = 묶기(لړیال, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int موخه_ارزښت = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && درشل_ارزښت[후보] == 창구번호) موخه_ارزښت = 후보;
        if (موخه_ارزښت < 0) return -111;
        if (개수[موخه_ارزښت] == 4) return -11;
        int 자리 = موخه_ارزښت * 4 + (앞[موخه_ارزښت] + 개수[موخه_ارزښت]) % 4;
        for (int بايټ_ارزښت = 0; بايټ_ارزښت < کچ; بايټ_ارزښت++) اومتوک[자리 * 512 + بايټ_ارزښت] = 전달[بايټ_ارزښت];
        اوږدوالى_ارزښت[자리] = کچ; 보낸창구[자리] = درشل_ارزښت[칸]; 개수[موخه_ارزښت]++;
        return کچ;
    }
    public static int 받기(int لړیال, int 용량) {
        int 칸 = 확인(لړیال);
        if (칸 < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[칸] == 0) return -11;
        int 자리 = 칸 * 4 + 앞[칸];
        int کچ = اوږدوالى_ارزښت[자리] < 용량 ? اوږدوالى_ارزښت[자리] : 용량;
        for (int بايټ_ارزښت = 0; بايټ_ارزښت < کچ; بايټ_ارزښت++) 전달[بايټ_ارزښت] = اومتوک[자리 * 512 + بايټ_ارزښت];
        받은창구[칸] = 보낸창구[자리]; 앞[칸] = (앞[칸] + 1) % 4; 개수[칸]--;
        return کچ;
    }
    public static int 창구읽기(int لړیال) { int 칸 = 확인(لړیال); return 칸 < 0 ? -9 : درشل_ارزښت[칸]; }
    public static int 주소읽기(int لړیال) { int 칸 = 확인(لړیال); return 칸 < 0 ? -9 : پته[칸]; }
    public static int 보낸곳(int لړیال) { int 칸 = 확인(لړیال); return 칸 < 0 ? -9 : 받은창구[칸]; }
    public static int بندول(int لړیال) {
        int 칸 = 확인(لړیال); if (칸 < 0) return -9;
        사용[칸] = 0; 개수[칸] = 0; درشل_ارزښت[칸] = 0; return 0;
    }
}
