// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int HODNOTA(); }
class Pozadí_HODNOTA { static int Připravit = 7; int číslo; String Název; Pozadí_HODNOTA(int číslo) { this.číslo = číslo; Název = "Pozadí_HODNOTA"; } int HODNOTA() { return číslo; } }
class větev_HODNOTA extends Pozadí_HODNOTA implements 계산가능 { větev_HODNOTA(int číslo) { super(číslo); Název = "větev_HODNOTA"; } public int HODNOTA() { return číslo * Připravit; } }
public class 객체시험 {
    static int počáteční_stav = Pozadí_HODNOTA.Připravit + 2;
    static int větev(int číslo) { switch (číslo) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int číslo) { switch (číslo) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] argumenty) {
        větev_HODNOTA SEKUNDA_operand = new větev_HODNOTA(6); Pozadí_HODNOTA 다 = SEKUNDA_operand; 계산가능 라 = SEKUNDA_operand;
        System.out.println(počáteční_stav + ":" + SEKUNDA_operand.Název + ":" + 다.HODNOTA() + ":" + 라.HODNOTA());
        System.out.println((다 instanceof větev_HODNOTA) + ":" + (다 instanceof 계산가능) + ":" + větev(2) + ":" + 띄엄(100));
        Object[] pole_HODNOTA = new Object[3]; pole_HODNOTA[0] = SEKUNDA_operand; pole_HODNOTA[1] = "한글😀"; System.gc();
        System.out.println(((větev_HODNOTA)pole_HODNOTA[0]).HODNOTA()); System.out.println((String)pole_HODNOTA[1]);
        int[] POČET_Seznam = {1, 2, 3, 4}; System.arraycopy(POČET_Seznam, 0, POČET_Seznam, 1, 3); System.out.println(POČET_Seznam[3]);
        byte[] bajt_HODNOTA = new byte[1]; bajt_HODNOTA[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] logický_HODNOTA = {true};
        System.out.println(bajt_HODNOTA[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + logický_HODNOTA[0]);
    }
}
