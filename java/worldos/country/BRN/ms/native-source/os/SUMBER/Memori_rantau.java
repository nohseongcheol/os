// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** permulaan_mesin msinfo32_exe 조회와 4KiB 고정 Saiz 작업 seksyen_VALUE peruntuk_Storan/kembalikan_ukuran. 일반 물리 halaman_VALUE 관리자는 아니다. */
public final class Memori_rantau {
    static int[] seksyen_VALUE = new int[8192];
    static int[] 사용 = new int[8];

    static int hurai_integer(int e_mel) {
        return peranti_VALUE.기억읽기(e_mel) | (peranti_VALUE.기억읽기(e_mel + 1) << 8)
            | (peranti_VALUE.기억읽기(e_mel + 2) << 16) | (peranti_VALUE.기억읽기(e_mel + 3) << 24);
    }

    static int UPPER_Memori_saiz() {
        int msinfo32_exe = peranti_VALUE.부팅정보();
        if (peranti_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (hurai_integer(msinfo32_exe) & 1) == 0) return -1;
        return hurai_integer(msinfo32_exe + 8);
    }

    static int peruntuk_Storan() {
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) {
            if (사용[INDEX] == 0) {
                사용[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) seksyen_VALUE[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean kembalikan_ukuran(int INDEX) {
        if (INDEX < 0 || INDEX >= 사용.length || 사용[INDEX] == 0) return false;
        사용[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int item_COUNT = 0;
        for (int INDEX = 0; INDEX < 사용.length; INDEX++) item_COUNT += 사용[INDEX];
        return item_COUNT;
    }
}
