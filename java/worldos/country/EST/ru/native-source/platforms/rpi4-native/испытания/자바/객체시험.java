// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface 계산가능 { int ЗНАЧЕН(); }
class фон_ЗНАЧЕН { static int Подготовить = 7; int 수; String Название; фон_ЗНАЧЕН(int 수) { this.수 = 수; Название = "фон_ЗНАЧЕН"; } int ЗНАЧЕН() { return 수; } }
class ветвь_ЗНАЧЕН extends фон_ЗНАЧЕН implements 계산가능 { ветвь_ЗНАЧЕН(int 수) { super(수); Название = "ветвь_ЗНАЧЕН"; } public int ЗНАЧЕН() { return 수 * Подготовить; } }
public class 객체시험 {
    static int начальное_состояние = фон_ЗНАЧЕН.Подготовить + 2;
    static int ветвь(int 수) { switch (수) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int 띄엄(int 수) { switch (수) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] аргументы) {
        ветвь_ЗНАЧЕН СЕКУНДЫ_операнд = new ветвь_ЗНАЧЕН(6); фон_ЗНАЧЕН 다 = СЕКУНДЫ_операнд; 계산가능 라 = СЕКУНДЫ_операнд;
        System.out.println(начальное_состояние + ":" + СЕКУНДЫ_операнд.Название + ":" + 다.ЗНАЧЕН() + ":" + 라.ЗНАЧЕН());
        System.out.println((다 instanceof ветвь_ЗНАЧЕН) + ":" + (다 instanceof 계산가능) + ":" + ветвь(2) + ":" + 띄엄(100));
        Object[] МАССИВ_ЗНАЧЕН = new Object[3]; МАССИВ_ЗНАЧЕН[0] = СЕКУНДЫ_операнд; МАССИВ_ЗНАЧЕН[1] = "한글😀"; System.gc();
        System.out.println(((ветвь_ЗНАЧЕН)МАССИВ_ЗНАЧЕН[0]).ЗНАЧЕН()); System.out.println((String)МАССИВ_ЗНАЧЕН[1]);
        int[] СЧЁТ_Список = {1, 2, 3, 4}; System.arraycopy(СЧЁТ_Список, 0, СЧЁТ_Список, 1, 3); System.out.println(СЧЁТ_Список[3]);
        byte[] байт_ЗНАЧЕН = new byte[1]; байт_ЗНАЧЕН[0] = (byte)255; char[] 문자 = {'한'}; short[] 짧음 = {(short)65535}; boolean[] логический_ЗНАЧЕН = {true};
        System.out.println(байт_ЗНАЧЕН[0] + ":" + 문자[0] + ":" + 짧음[0] + ":" + логический_ЗНАЧЕН[0]);
    }
}
