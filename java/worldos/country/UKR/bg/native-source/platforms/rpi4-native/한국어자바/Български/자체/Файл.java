// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 потребител 용어를 보존한다. в_срок_артикул 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Файл {
    private Файл() {}
    public static byte[] 바이트읽기(String Име) throws В_И_изключение {
        try {
        FileInputStream поток_стойност = new FileInputStream(Име);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, стойност;
            while ((стойност = поток_стойност.read()) != -1) { if (수 == 임시.length) throw new В_И_изключение("Файл Размер 제한"); 임시[수++] = (byte)стойност; }
            byte[] РЕЗУЛТАТ = new byte[수]; System.arraycopy(임시, 0, РЕЗУЛТАТ, 0, 수); return РЕЗУЛТАТ;
        } finally { поток_стойност.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void записване_байт_стойност(String Име, byte[] Съдържание_стойност) throws В_И_изключение {
        try {
        FileOutputStream поток_стойност = new FileOutputStream(Име);
        try { for (int цикъл_индекс = 0; цикъл_индекс < Съдържание_стойност.length; цикъл_индекс++) поток_стойност.write(Съдържание_стойност[цикъл_индекс] & 255); } finally { поток_стойност.close(); }
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static String Четене(String Име) throws В_И_изключение {
        try { return 문자.дешифрирам_данни(바이트읽기(Име));
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static void Писане(String Име, String Съдържание_стойност) throws В_И_изключение {
        try { записване_байт_стойност(Име, 문자.кодирам(Съдържание_стойност));
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
}
