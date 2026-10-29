// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 Fail. 원본 edit_VALUE/bina_sumber kegagalan_VALUE 시 기존 파일을 보존한다. */
public final class Memori_sistem_fail {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] saiz_Senarai = new int[8];
    static int[] buka_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nama = new int[64];
    static int[] edit_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean limpahan_VALUE = false;
    static int edit_saiz = 0;

    static boolean cek_nama(int[] aksara_VALUE, int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 1 || kepanjangan_VALUE > 63) return false;
        for (int 수 = 0; 수 < kepanjangan_VALUE; 수++) {
            int VALUE = aksara_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return aksara_VALUE[0] != '.';
    }

    static int Cari_pemasukan(int[] aksara_VALUE, int kepanjangan_VALUE) {
        if (!cek_nama(aksara_VALUE, kepanjangan_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + kepanjangan_VALUE] == 0;
            for (int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) if (이름들[수 * 64 + 칸] != aksara_VALUE[칸]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int stor_VALUE(int[] aksara_VALUE, int kepanjangan_VALUE, int[] data, int Saiz) {
        if (!cek_nama(aksara_VALUE, kepanjangan_VALUE) || Saiz < 0 || Saiz > data.length) return -22;
        if (Saiz > 최대크기) return -90;
        int INDEX = Cari_pemasukan(aksara_VALUE, kepanjangan_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && buka_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int e_mel = peranti_VALUE.fail_Memori() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Saiz; 수++) peranti_VALUE.tulis_Memori(e_mel + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < kepanjangan_VALUE ? aksara_VALUE[수] : 0;
        saiz_Senarai[INDEX] = Saiz;
        return Saiz;
    }

    static void pemasukan_Senarai() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int 칸 = 0; 칸 < 64 && 이름들[수 * 64 + 칸] != 0; 칸++) SMS_Terminal.문자(이름들[수 * 64 + 칸]);
            SMS_Terminal.Tulis("  "); SMS_Terminal.수쓰기(saiz_Senarai[수]); SMS_Terminal.Tulis("bait_VALUE\n");
        }
        SMS_Terminal.Tulis(Storan_peranti_hubungan.teknologi_maklumat_Ada_9e72441a ? "Fail 8칸, 파일당 16384바이트; sync로 stor_VALUE 장치에 보존\n"
            : "임시 Fail 8칸, 파일당 16384바이트; 다시 시작하면 사라짐\n");
    }

    static void Perintah(int[] 입력, int Jalan, int kepanjangan_VALUE, int Aksi) {
        while (Jalan < kepanjangan_VALUE && 입력[Jalan] == ' ') Jalan++;
        int 끝 = kepanjangan_VALUE;
        while (끝 > Jalan && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - Jalan;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Tulis("올바르지 않은 Fail Nama\n"); return; }
        for (int 칸 = 0; 칸 < 64; 칸++) Nama[칸] = 칸 < 수 ? 입력[Jalan + 칸] : 0;
        int INDEX = Cari_pemasukan(Nama, 수);
        if (INDEX == -22) { SMS_Terminal.Tulis("올바르지 않은 Fail Nama\n"); return; }
        if (Aksi == 0) {
            편집중 = true; edit_saiz = 0; limpahan_VALUE = false;
            SMS_Terminal.Tulis("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Tulis("파일을 찾을 수 없습니다\n");
        else if (Aksi == 1) {
            int e_mel = peranti_VALUE.fail_Memori() + INDEX * 최대크기;
            for (int 칸 = 0; 칸 < saiz_Senarai[INDEX]; 칸++) SMS_Terminal.문자(peranti_VALUE.기억읽기(e_mel + 칸));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; saiz_Senarai[INDEX] = 0; SMS_Terminal.Tulis("파일을 지웠습니다\n"); }
    }

    static boolean teknologi_maklumat_EXACT(int[] 입력, int kepanjangan_VALUE, String 문구) {
        if (kepanjangan_VALUE != 문구.length()) return false;
        for (int 칸 = 0; 칸 < kepanjangan_VALUE; 칸++) if (입력[칸] != 문구.charAt(칸)) return false;
        return true;
    }

    static void Diedit_baris(int[] 입력, int kepanjangan_VALUE, boolean baris_limpahan) {
        if (teknologi_maklumat_EXACT(입력, kepanjangan_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Tulis("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (teknologi_maklumat_EXACT(입력, kepanjangan_VALUE, ".save")) {
            편집중 = false;
            if (limpahan_VALUE) { SMS_Terminal.Tulis("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nama[수] != 0) 수++;
            int ukuran = stor_VALUE(Nama, 수, edit_VALUE, edit_saiz);
            SMS_Terminal.Tulis(ukuran >= 0 ? "보존한 bait_VALUE 수: " : "보존 kegagalan_VALUE: ");
            SMS_Terminal.수쓰기(ukuran); SMS_Terminal.문자(10);
        } else if (baris_limpahan || kepanjangan_VALUE + 1 > 최대크기 - edit_saiz) limpahan_VALUE = true;
        else {
            for (int 수 = 0; 수 < kepanjangan_VALUE; 수++) edit_VALUE[edit_saiz++] = 입력[수];
            edit_VALUE[edit_saiz++] = 10;
        }
    }

    static void 예제(String Fail, String Kandungan_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Nama[수] = 수 < Fail.length() ? Fail.charAt(수) : 0;
        for (int 수 = 0; 수 < Kandungan_VALUE.length(); 수++) edit_VALUE[수] = Kandungan_VALUE.charAt(수);
        stor_VALUE(Nama, Fail.length(), edit_VALUE, Kandungan_VALUE.length());
    }

    static void Sediakan() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int Kumpulan_VALUE = peranti_VALUE.자바파일묶음(), Saiz = peranti_VALUE.자바파일묶음크기();
        if (Saiz < 8 || 실행관리.수(Kumpulan_VALUE) != 0x464a4b4a) { SMS_Terminal.Tulis("올바르지 않은 Java Fail Kumpulan_VALUE\n"); return; }
        int item_COUNT = 실행관리.수(Kumpulan_VALUE + 4);
        if (item_COUNT < 0 || item_COUNT > 8 || item_COUNT > (Saiz - 8) / 72) { SMS_Terminal.Tulis("올바르지 않은 Java Fail pemasukan_Senarai\n"); return; }
        for (int 수 = 0; 수 < item_COUNT; 수++) {
            int pemasukan_VALUE = Kumpulan_VALUE + 8 + 수 * 72, kepanjangan_VALUE = 0;
            for (int 칸 = 0; 칸 < 64; 칸++) Nama[칸] = peranti_VALUE.기억읽기(pemasukan_VALUE + 칸);
            while (kepanjangan_VALUE < 64 && Nama[kepanjangan_VALUE] != 0) kepanjangan_VALUE++;
            int Kedudukan = 실행관리.수(pemasukan_VALUE + 64), saiz_fail = 실행관리.수(pemasukan_VALUE + 68);
            if (!cek_nama(Nama, kepanjangan_VALUE) || saiz_fail < 0 || saiz_fail > 최대크기 || Kedudukan < 8 + item_COUNT * 72 || Kedudukan > Saiz - saiz_fail) {
                SMS_Terminal.Tulis("올바르지 않은 Java Fail pemasukan_VALUE\n"); return;
            }
            for (int 칸 = 0; 칸 < saiz_fail; 칸++) edit_VALUE[칸] = peranti_VALUE.기억읽기(Kumpulan_VALUE + Kedudukan + 칸);
            if (stor_VALUE(Nama, kepanjangan_VALUE, edit_VALUE, saiz_fail) < 0) { SMS_Terminal.Tulis("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
