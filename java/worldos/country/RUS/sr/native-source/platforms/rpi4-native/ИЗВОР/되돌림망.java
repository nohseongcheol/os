// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 계층: 단일 커널 안의 IPv4/UDP 루프백 전송.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * 끝점 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] 창구 = new int[8];
    static int[] 주소 = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] 자료 = new int[32 * 512];
    static int[] 전달 = new int[512];
    static int 다음창구 = 49152;
    static int 확인(int 번호) { return 번호 >= 32 && 번호 < 40 && 사용[번호 - 32] != 0 ? 번호 - 32 : -1; }
    static boolean 겹침(int 번호) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && 창구[칸] == 번호) return true;
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
    public static int 만들기(int 영역, int 종류, int 규약) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (규약 != 0 && 규약 != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; 창구[칸] = 0; 주소[칸] = 0; 앞[칸] = 0; 개수[칸] = 0; 받은창구[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int 묶기(int 번호, int 망주소, int 창구번호) {
        int 칸 = 확인(번호);
        if (칸 < 0) return -9;
        if (망주소 != 0 && 망주소 != 0x7f000001) return -99;
        if (창구[칸] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        창구[칸] = 창구번호; 주소[칸] = 망주소; return 0;
    }
    public static int 자료넣기(int 번호, int 값) {
        if (번호 < 0 || 번호 >= 512) return -22;
        전달[번호] = 값 & 255; return 0;
    }
    public static int 자료읽기(int 번호) { return 번호 >= 0 && 번호 < 512 ? 전달[번호] : -22; }
    public static int 보내기(int 번호, int 망주소, int 창구번호, int Величина) {
        int 칸 = 확인(번호);
        if (칸 < 0) return -9;
        if (망주소 != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Величина < 0 || Величина > 512) return -90;
        if (창구[칸] == 0) {
            int ИСХОД = 묶기(번호, 0x7f000001, 0);
            if (ИСХОД < 0) return ИСХОД;
        }
        int 목적 = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && 창구[후보] == 창구번호) 목적 = 후보;
        if (목적 < 0) return -111;
        if (개수[목적] == 4) return -11;
        int 자리 = 목적 * 4 + (앞[목적] + 개수[목적]) % 4;
        for (int 바이트 = 0; 바이트 < Величина; 바이트++) 자료[자리 * 512 + 바이트] = 전달[바이트];
        길이[자리] = Величина; 보낸창구[자리] = 창구[칸]; 개수[목적]++;
        return Величина;
    }
    public static int 받기(int 번호, int 용량) {
        int 칸 = 확인(번호);
        if (칸 < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[칸] == 0) return -11;
        int 자리 = 칸 * 4 + 앞[칸];
        int Величина = 길이[자리] < 용량 ? 길이[자리] : 용량;
        for (int 바이트 = 0; 바이트 < Величина; 바이트++) 전달[바이트] = 자료[자리 * 512 + 바이트];
        받은창구[칸] = 보낸창구[자리]; 앞[칸] = (앞[칸] + 1) % 4; 개수[칸]--;
        return Величина;
    }
    public static int 창구읽기(int 번호) { int 칸 = 확인(번호); return 칸 < 0 ? -9 : 창구[칸]; }
    public static int 주소읽기(int 번호) { int 칸 = 확인(번호); return 칸 < 0 ? -9 : 주소[칸]; }
    public static int 보낸곳(int 번호) { int 칸 = 확인(번호); return 칸 < 0 ? -9 : 받은창구[칸]; }
    public static int Затворен(int 번호) {
        int 칸 = 확인(번호); if (칸 < 0) return -9;
        사용[칸] = 0; 개수[칸] = 0; 창구[칸] = 0; return 0;
    }
}
