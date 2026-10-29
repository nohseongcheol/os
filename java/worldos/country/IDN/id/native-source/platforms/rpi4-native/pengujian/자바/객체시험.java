// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int VALUE(); }
class wallpaper_VALUE { static int Siapkan = 7; int 수; String Nama_2; wallpaper_VALUE(int 수) { this.수 = 수; Nama_2 = "wallpaper_VALUE"; } int VALUE() { return 수; } }
class cabang_VALUE extends wallpaper_VALUE implements 계산가능 { cabang_VALUE(int 수) { super(수); Nama_2 = "cabang_VALUE"; } public int VALUE() { return 수 * Siapkan; } }
public class 객체시험 {
    static int keadaan_awal = wallpaper_VALUE.Siapkan + 2;
    static int cabang(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumen) {
        cabang_VALUE SECOND_operand = new cabang_VALUE(6); wallpaper_VALUE 다 = SECOND_operand; 계산가능 라 = SECOND_operand;
        System.out.println(keadaan_awal + ":" + SECOND_operand.Nama_2 + ":" + 다.VALUE() + ":" + 라.VALUE());
        System.out.println((다 instanceof cabang_VALUE) + ":" + (다 instanceof 계산가능) + ":" + cabang(2) + ":" + 띄엄(100));
        Object[] ARRAY_VALUE = new Object[3]; ARRAY_VALUE[0] = SECOND_operand; ARRAY_VALUE[1] = "한글😀"; System.gc();
        System.out.println(((cabang_VALUE)ARRAY_VALUE[0]).VALUE()); System.out.println((String)ARRAY_VALUE[1]);
        int[] COUNT_Daftar = {1, 2, 3, 4}; System.arraycopy(COUNT_Daftar, 0, COUNT_Daftar, 1, 3); System.out.println(COUNT_Daftar[3]);
        byte[] byte_VALUE = new byte[1]; byte_VALUE[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] Boolean_VALUE = {true};
        System.out.println(byte_VALUE[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + Boolean_VALUE[0]);
    }
}
