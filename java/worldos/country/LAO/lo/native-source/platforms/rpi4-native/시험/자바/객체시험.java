// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ຄ່າ(); }
class ພື້ນຫຼັງ_ຄ່າ { static int ກະ_ກຽມ = 7; int 수; String ຊື່; ພື້ນຫຼັງ_ຄ່າ(int 수) { this.수 = 수; ຊື່ = "ພື້ນຫຼັງ_ຄ່າ"; } int ຄ່າ() { return 수; } }
class ສາຂາ_ຄ່າ extends ພື້ນຫຼັງ_ຄ່າ implements 계산가능 { ສາຂາ_ຄ່າ(int 수) { super(수); ຊື່ = "ສາຂາ_ຄ່າ"; } public int ຄ່າ() { return 수 * ກະ_ກຽມ; } }
public class 객체시험 {
    static int 초기 = ພື້ນຫຼັງ_ຄ່າ.ກະ_ກຽມ + 2;
    static int ສາຂາ(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] 인수) {
        ສາຂາ_ຄ່າ 나 = new ສາຂາ_ຄ່າ(6); ພື້ນຫຼັງ_ຄ່າ 다 = 나; 계산가능 라 = 나;
        System.out.println(초기 + ":" + 나.ຊື່ + ":" + 다.ຄ່າ() + ":" + 라.ຄ່າ());
        System.out.println((다 instanceof ສາຂາ_ຄ່າ) + ":" + (다 instanceof 계산가능) + ":" + ສາຂາ(2) + ":" + 띄엄(100));
        Object[] ການຈັດຄ່າຮອບວຽນ_ຄ່າ = new Object[3]; ການຈັດຄ່າຮອບວຽນ_ຄ່າ[0] = 나; ການຈັດຄ່າຮອບວຽນ_ຄ່າ[1] = "한글😀"; System.gc();
        System.out.println(((ສາຂາ_ຄ່າ)ການຈັດຄ່າຮອບວຽນ_ຄ່າ[0]).ຄ່າ()); System.out.println((String)ການຈັດຄ່າຮອບວຽນ_ຄ່າ[1]);
        int[] 수들 = {1, 2, 3, 4}; System.arraycopy(수들, 0, 수들, 1, 3); System.out.println(수들[3]);
        byte[] ໄບ_ຄ່າ = new byte[1]; ໄບ_ຄ່າ[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] 참거짓 = {true};
        System.out.println(ໄບ_ຄ່າ[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + 참거짓[0]);
    }
}
