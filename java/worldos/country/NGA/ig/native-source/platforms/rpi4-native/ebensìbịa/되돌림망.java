// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 òkpùkpù_valuu: 단일 mkpụrụobī_kọmpùta_valuu 안의 IPv4/UDP 루프백 dògharịa_valuu.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * mèdebe_akara 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] pọọt_valuu = new int[8];
    static int[] àdreèsì = new int[8];
    static int[] 앞 = new int[8];
    static int[] 개수 = new int[8];
    static int[] 받은창구 = new int[8];
    static int[] ogologo_valuu = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] datà = new int[32 * 512];
    static int[] zìgaā_valuu = new int[512];
    static int 다음창구 = 49152;
    static int nkwàdo_eziokwū(int indèks) { return indèks >= 32 && indèks < 40 && 사용[indèks - 32] != 0 ? indèks - 32 : -1; }
    static boolean 겹침(int indèks) {
        for (int oghere_ndebà = 0; oghere_ndebà < 8; oghere_ndebà++) if (사용[oghere_ndebà] != 0 && pọọt_valuu[oghere_ndebà] == indèks) return true;
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
    public static int mepụta_ndebà(int 영역, int 종류, int ngō_valuu) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (ngō_valuu != 0 && ngō_valuu != 17)) return -93;
        for (int oghere_ndebà = 0; oghere_ndebà < 8; oghere_ndebà++) if (사용[oghere_ndebà] == 0) {
            사용[oghere_ndebà] = 1; pọọt_valuu[oghere_ndebà] = 0; àdreèsì[oghere_ndebà] = 0; 앞[oghere_ndebà] = 0; 개수[oghere_ndebà] = 0; 받은창구[oghere_ndebà] = 0;
            return oghere_ndebà + 32;
        }
        return -24;
    }
    public static int 묶기(int indèks, int Netwọọkụ_àdreèsì, int 창구번호) {
        int oghere_ndebà = nkwàdo_eziokwū(indèks);
        if (oghere_ndebà < 0) return -9;
        if (Netwọọkụ_àdreèsì != 0 && Netwọọkụ_àdreèsì != 0x7f000001) return -99;
        if (pọọt_valuu[oghere_ndebà] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        pọọt_valuu[oghere_ndebà] = 창구번호; àdreèsì[oghere_ndebà] = Netwọọkụ_àdreèsì; return 0;
    }
    public static int 자료넣기(int indèks, int valuu) {
        if (indèks < 0 || indèks >= 512) return -22;
        zìgaā_valuu[indèks] = valuu & 255; return 0;
    }
    public static int 자료읽기(int indèks) { return indèks >= 0 && indèks < 512 ? zìgaā_valuu[indèks] : -22; }
    public static int zìga(int indèks, int Netwọọkụ_àdreèsì, int 창구번호, int Ụhara) {
        int oghere_ndebà = nkwàdo_eziokwū(indèks);
        if (oghere_ndebà < 0) return -9;
        if (Netwọọkụ_àdreèsì != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (Ụhara < 0 || Ụhara > 512) return -90;
        if (pọọt_valuu[oghere_ndebà] == 0) {
            int 결과 = 묶기(indèks, 0x7f000001, 0);
            if (결과 < 0) return 결과;
        }
        int ebemwèga_valuu = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && pọọt_valuu[후보] == 창구번호) ebemwèga_valuu = 후보;
        if (ebemwèga_valuu < 0) return -111;
        if (개수[ebemwèga_valuu] == 4) return -11;
        int 자리 = ebemwèga_valuu * 4 + (앞[ebemwèga_valuu] + 개수[ebemwèga_valuu]) % 4;
        for (int baịtị_valuu = 0; baịtị_valuu < Ụhara; baịtị_valuu++) datà[자리 * 512 + baịtị_valuu] = zìgaā_valuu[baịtị_valuu];
        ogologo_valuu[자리] = Ụhara; 보낸창구[자리] = pọọt_valuu[oghere_ndebà]; 개수[ebemwèga_valuu]++;
        return Ụhara;
    }
    public static int 받기(int indèks, int 용량) {
        int oghere_ndebà = nkwàdo_eziokwū(indèks);
        if (oghere_ndebà < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (개수[oghere_ndebà] == 0) return -11;
        int 자리 = oghere_ndebà * 4 + 앞[oghere_ndebà];
        int Ụhara = ogologo_valuu[자리] < 용량 ? ogologo_valuu[자리] : 용량;
        for (int baịtị_valuu = 0; baịtị_valuu < Ụhara; baịtị_valuu++) zìgaā_valuu[baịtị_valuu] = datà[자리 * 512 + baịtị_valuu];
        받은창구[oghere_ndebà] = 보낸창구[자리]; 앞[oghere_ndebà] = (앞[oghere_ndebà] + 1) % 4; 개수[oghere_ndebà]--;
        return Ụhara;
    }
    public static int 창구읽기(int indèks) { int oghere_ndebà = nkwàdo_eziokwū(indèks); return oghere_ndebà < 0 ? -9 : pọọt_valuu[oghere_ndebà]; }
    public static int 주소읽기(int indèks) { int oghere_ndebà = nkwàdo_eziokwū(indèks); return oghere_ndebà < 0 ? -9 : àdreèsì[oghere_ndebà]; }
    public static int 보낸곳(int indèks) { int oghere_ndebà = nkwàdo_eziokwū(indèks); return oghere_ndebà < 0 ? -9 : 받은창구[oghere_ndebà]; }
    public static int Mechie(int indèks) {
        int oghere_ndebà = nkwàdo_eziokwū(indèks); if (oghere_ndebà < 0) return -9;
        사용[oghere_ndebà] = 0; 개수[oghere_ndebà] = 0; pọọt_valuu[oghere_ndebà] = 0; return 0;
    }
}
