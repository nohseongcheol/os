// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 세션 동안 유지되는 8개 berkas. 원본 Edit_VALUE/bangun_sumber kegagalan_VALUE 시 기존 파일을 보존한다. */
public final class Memori_sistem_berkas {
    static final int 최대크기 = 16384;
    static int[] 이름들 = new int[8 * 64];
    static int[] ukuran_Daftar = new int[8];
    static int[] buat_COUNT = new int[8], 허가들 = new int[8];
    static int[] Nama_2 = new int[64];
    static int[] Edit_VALUE = new int[최대크기];
    static boolean 편집중 = false;
    static boolean luapan_VALUE = false;
    static int Edit_ukuran = 0;

    static boolean cek_nama(int[] karakter_VALUE, int panjang_VALUE) {
        if (panjang_VALUE < 1 || panjang_VALUE > 63) return false;
        for (int 수 = 0; 수 < panjang_VALUE; 수++) {
            int VALUE = karakter_VALUE[수];
            if (!(VALUE >= 'a' && VALUE <= 'z') && !(VALUE >= 'A' && VALUE <= 'Z')
                && !(VALUE >= '0' && VALUE <= '9') && VALUE != '_' && VALUE != '-' && VALUE != '.') return false;
        }
        return karakter_VALUE[0] != '.';
    }

    static int FIND_entri(int[] karakter_VALUE, int panjang_VALUE) {
        if (!cek_nama(karakter_VALUE, panjang_VALUE)) return -22;
        for (int 수 = 0; 수 < 8; 수++) {
            boolean 같음 = 이름들[수 * 64 + panjang_VALUE] == 0;
            for (int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) if (이름들[수 * 64 + slot_entri] != karakter_VALUE[slot_entri]) 같음 = false;
            if (같음) return 수;
        }
        return -2;
    }

    static int Store_VALUE(int[] karakter_VALUE, int panjang_VALUE, int[] data, int Ukuran) {
        if (!cek_nama(karakter_VALUE, panjang_VALUE) || Ukuran < 0 || Ukuran > data.length) return -22;
        if (Ukuran > 최대크기) return -90;
        int INDEX = FIND_entri(karakter_VALUE, panjang_VALUE);
        if (INDEX == -2) {
            for (int 수 = 0; 수 < 8 && INDEX < 0; 수++) if (이름들[수 * 64] == 0 && buat_COUNT[수] == 0) INDEX = 수;
            if (INDEX >= 0) 허가들[INDEX] = 438;
        }
        if (INDEX < 0) return -28;
        int surel = Ponsel_VALUE.file_Memori() + INDEX * 최대크기;
        for (int 수 = 0; 수 < Ukuran; 수++) Ponsel_VALUE.tulis_Memori(surel + 수, data[수]);
        for (int 수 = 0; 수 < 64; 수++) 이름들[INDEX * 64 + 수] = 수 < panjang_VALUE ? karakter_VALUE[수] : 0;
        ukuran_Daftar[INDEX] = Ukuran;
        return Ukuran;
    }

    static void entri_Daftar() {
        for (int 수 = 0; 수 < 8; 수++) if (이름들[수 * 64] != 0) {
            for (int slot_entri = 0; slot_entri < 64 && 이름들[수 * 64 + slot_entri] != 0; slot_entri++) SMS_Terminal.문자(이름들[수 * 64 + slot_entri]);
            SMS_Terminal.Tulis("  "); SMS_Terminal.수쓰기(ukuran_Daftar[수]); SMS_Terminal.Tulis("byte_VALUE\n");
        }
        SMS_Terminal.Tulis(Storage_Ponsel_koneksi.teknologi_informasi_Aktif_9e72441a ? "berkas 8칸, 파일당 16384바이트; sync로 Store_VALUE 장치에 보존\n"
            : "임시 berkas 8칸, 파일당 16384바이트; coba_lagi_VALUE 시작하면 사라짐\n");
    }

    static void perintah(int[] 입력, int jalankan, int panjang_VALUE, int Aksi) {
        while (jalankan < panjang_VALUE && 입력[jalankan] == ' ') jalankan++;
        int 끝 = panjang_VALUE;
        while (끝 > jalankan && 입력[끝 - 1] == ' ') 끝--;
        int 수 = 끝 - jalankan;
        if (수 < 1 || 수 > 63) { SMS_Terminal.Tulis("올바르지 않은 berkas Nama_2\n"); return; }
        for (int slot_entri = 0; slot_entri < 64; slot_entri++) Nama_2[slot_entri] = slot_entri < 수 ? 입력[jalankan + slot_entri] : 0;
        int INDEX = FIND_entri(Nama_2, 수);
        if (INDEX == -22) { SMS_Terminal.Tulis("올바르지 않은 berkas Nama_2\n"); return; }
        if (Aksi == 0) {
            편집중 = true; Edit_ukuran = 0; luapan_VALUE = false;
            SMS_Terminal.Tulis("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (INDEX < 0) SMS_Terminal.Tulis("파일을 찾을 수 없습니다\n");
        else if (Aksi == 1) {
            int surel = Ponsel_VALUE.file_Memori() + INDEX * 최대크기;
            for (int slot_entri = 0; slot_entri < ukuran_Daftar[INDEX]; slot_entri++) SMS_Terminal.문자(Ponsel_VALUE.기억읽기(surel + slot_entri));
            SMS_Terminal.문자(10);
        } else { 이름들[INDEX * 64] = 0; ukuran_Daftar[INDEX] = 0; SMS_Terminal.Tulis("파일을 지웠습니다\n"); }
    }

    static boolean teknologi_informasi_EXACT(int[] 입력, int panjang_VALUE, String 문구) {
        if (panjang_VALUE != 문구.length()) return false;
        for (int slot_entri = 0; slot_entri < panjang_VALUE; slot_entri++) if (입력[slot_entri] != 문구.charAt(slot_entri)) return false;
        return true;
    }

    static void Diedit_baris(int[] 입력, int panjang_VALUE, boolean baris_luapan) {
        if (teknologi_informasi_EXACT(입력, panjang_VALUE, ".cancel")) {
            편집중 = false; SMS_Terminal.Tulis("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (teknologi_informasi_EXACT(입력, panjang_VALUE, ".save")) {
            편집중 = false;
            if (luapan_VALUE) { SMS_Terminal.Tulis("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int 수 = 0;
            while (수 < 64 && Nama_2[수] != 0) 수++;
            int hasil = Store_VALUE(Nama_2, 수, Edit_VALUE, Edit_ukuran);
            SMS_Terminal.Tulis(hasil >= 0 ? "보존한 byte_VALUE 수: " : "보존 kegagalan_VALUE: ");
            SMS_Terminal.수쓰기(hasil); SMS_Terminal.문자(10);
        } else if (baris_luapan || panjang_VALUE + 1 > 최대크기 - Edit_ukuran) luapan_VALUE = true;
        else {
            for (int 수 = 0; 수 < panjang_VALUE; 수++) Edit_VALUE[Edit_ukuran++] = 입력[수];
            Edit_VALUE[Edit_ukuran++] = 10;
        }
    }

    static void 예제(String berkas, String Isi_VALUE) {
        for (int 수 = 0; 수 < 64; 수++) Nama_2[수] = 수 < berkas.length() ? berkas.charAt(수) : 0;
        for (int 수 = 0; 수 < Isi_VALUE.length(); 수++) Edit_VALUE[수] = Isi_VALUE.charAt(수);
        Store_VALUE(Nama_2, berkas.length(), Edit_VALUE, Isi_VALUE.length());
    }

    static void Siapkan() {
        예제("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int grup_VALUE = Ponsel_VALUE.자바파일묶음(), Ukuran = Ponsel_VALUE.자바파일묶음크기();
        if (Ukuran < 8 || 실행관리.수(grup_VALUE) != 0x464a4b4a) { SMS_Terminal.Tulis("올바르지 않은 Java berkas grup_VALUE\n"); return; }
        int item_COUNT = 실행관리.수(grup_VALUE + 4);
        if (item_COUNT < 0 || item_COUNT > 8 || item_COUNT > (Ukuran - 8) / 72) { SMS_Terminal.Tulis("올바르지 않은 Java berkas entri_Daftar\n"); return; }
        for (int 수 = 0; 수 < item_COUNT; 수++) {
            int entri_VALUE = grup_VALUE + 8 + 수 * 72, panjang_VALUE = 0;
            for (int slot_entri = 0; slot_entri < 64; slot_entri++) Nama_2[slot_entri] = Ponsel_VALUE.기억읽기(entri_VALUE + slot_entri);
            while (panjang_VALUE < 64 && Nama_2[panjang_VALUE] != 0) panjang_VALUE++;
            int posisi = 실행관리.수(entri_VALUE + 64), ukuran_file = 실행관리.수(entri_VALUE + 68);
            if (!cek_nama(Nama_2, panjang_VALUE) || ukuran_file < 0 || ukuran_file > 최대크기 || posisi < 8 + item_COUNT * 72 || posisi > Ukuran - ukuran_file) {
                SMS_Terminal.Tulis("올바르지 않은 Java berkas entri_VALUE\n"); return;
            }
            for (int slot_entri = 0; slot_entri < ukuran_file; slot_entri++) Edit_VALUE[slot_entri] = Ponsel_VALUE.기억읽기(grup_VALUE + posisi + slot_entri);
            if (Store_VALUE(Nama_2, panjang_VALUE, Edit_VALUE, ukuran_file) < 0) { SMS_Terminal.Tulis("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
