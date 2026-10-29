// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 карыстальнік 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Назва) throws увод_вывад_выключэнне {
        try {
        FileInputStream паток_значэнне = new FileInputStream(Назва);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, значэнне;
            while ((значэнне = паток_значэнне.read()) != -1) { if (수 == 임시.length) throw new увод_вывад_выключэнне("Файл Памер 제한"); 임시[수++] = (byte)значэнне; }
            byte[] 결과 = new byte[수]; System.arraycopy(임시, 0, 결과, 0, 수); return 결과;
        } finally { паток_значэнне.close(); }
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void напісаць_байт_значэнне(String Назва, byte[] кантэнт_значэнне) throws увод_вывад_выключэнне {
        try {
        FileOutputStream паток_значэнне = new FileOutputStream(Назва);
        try { for (int цыкл_індэкс = 0; цыкл_індэкс < кантэнт_значэнне.length; цыкл_індэкс++) паток_значэнне.write(кантэнт_значэнне[цыкл_індэкс] & 255); } finally { паток_значэнне.close(); }
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static String Чытанне(String Назва) throws увод_вывад_выключэнне {
        try { return 문자.расшыфраваць_дадзеныя(바이트읽기(Назва));
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
    public static void Запіс(String Назва, String кантэнт_значэнне) throws увод_вывад_выключэнне {
        try { напісаць_байт_значэнне(Назва, 문자.부호화(кантэнт_значэнне));
        } catch (java.io.IOException ПАМЫЛКА) { throw 예외변환.увод_вывад(ПАМЫЛКА); }
        catch (RuntimeException ПАМЫЛКА) { throw 예외변환.выканаць_каманда(ПАМЫЛКА); }
    }
}
