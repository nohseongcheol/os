// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** awal_mesin msinfo32_exe 조회와 4KiB 고정 Ukuran 작업 seksi_VALUE alokasi_Storage/kembalikan_KR. 일반 물리 halaman_VALUE 관리자는 아니다. */
public final class Memori_wilayah {
    static int[] seksi_VALUE = new int[8192];
    static int[] gunakan_VALUE = new int[8];

    static int urai_bilangan_bulat(int surel) {
        return Ponsel_VALUE.기억읽기(surel) | (Ponsel_VALUE.기억읽기(surel + 1) << 8)
            | (Ponsel_VALUE.기억읽기(surel + 2) << 16) | (Ponsel_VALUE.기억읽기(surel + 3) << 24);
    }

    static int UPPER_Memori_ukuran() {
        int msinfo32_exe = Ponsel_VALUE.부팅정보();
        if (Ponsel_VALUE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (urai_bilangan_bulat(msinfo32_exe) & 1) == 0) return -1;
        return urai_bilangan_bulat(msinfo32_exe + 8);
    }

    static int alokasi_Storage() {
        for (int INDEX = 0; INDEX < gunakan_VALUE.length; INDEX++) {
            if (gunakan_VALUE[INDEX] == 0) {
                gunakan_VALUE[INDEX] = 1;
                for (int slot_entri = 0; slot_entri < 1024; slot_entri++) seksi_VALUE[INDEX * 1024 + slot_entri] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean kembalikan_KR(int INDEX) {
        if (INDEX < 0 || INDEX >= gunakan_VALUE.length || gunakan_VALUE[INDEX] == 0) return false;
        gunakan_VALUE[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int item_COUNT = 0;
        for (int INDEX = 0; INDEX < gunakan_VALUE.length; INDEX++) item_COUNT += gunakan_VALUE[INDEX];
        return item_COUNT;
    }
}
