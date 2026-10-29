// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package українська.своє;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 простір_користувача 용어를 보존한다. чинний_елемент 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class файл {
    private файл() {}
    public static byte[] 바이트읽기(String Назва) throws ввід_вивід_виняток {
        try {
        FileInputStream потік_значення = new FileInputStream(Назва);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, значення;
            while ((значення = потік_значення.read()) != -1) { if (수 == 임시.length) throw new ввід_вивід_виняток("файл Розмір 제한"); 임시[수++] = (byte)значення; }
            byte[] результат = new byte[수]; System.arraycopy(임시, 0, результат, 0, 수); return результат;
        } finally { потік_значення.close(); }
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void записування_байт_значення(String Назва, byte[] Вміст_значення) throws ввід_вивід_виняток {
        try {
        FileOutputStream потік_значення = new FileOutputStream(Назва);
        try { for (int цикл_індекс = 0; цикл_індекс < Вміст_значення.length; цикл_індекс++) потік_значення.write(Вміст_значення[цикл_індекс] & 255); } finally { потік_значення.close(); }
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static String Читання(String Назва) throws ввід_вивід_виняток {
        try { return 문자.дешифрувати_дані(바이트읽기(Назва));
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
    public static void Запис(String Назва, String Вміст_значення) throws ввід_вивід_виняток {
        try { записування_байт_значення(Назва, 문자.кодувати(Вміст_значення));
        } catch (java.io.IOException ПОМИЛКА) { throw перетворити_виняток.ввід_вивід(ПОМИЛКА); }
        catch (RuntimeException ПОМИЛКА) { throw перетворити_виняток.Виконати_команда(ПОМИЛКА); }
    }
}
