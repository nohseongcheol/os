// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Български.자체;

/** дейтаграма(電文)·Канал_запис(通路): 경계를 가진 UDP 자료를 주고받는 участник. */
public final class дейтаграма_Канал {
    private final java.net.DatagramSocket 표준종단;
    private дейтаграма_Канал(int номер_на_порт) throws В_И_изключение {
        try { 표준종단 = 통신.Отваряне(номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public static дейтаграма_Канал Отваряне(int номер_на_порт) throws В_И_изключение {
        try { return new дейтаграма_Канал(номер_на_порт);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void изпращам(String адрес, int номер_на_порт, String данни) throws В_И_изключение {
        try { 통신.изпращам(표준종단, адрес, номер_на_порт, данни);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public String получавам() throws В_И_изключение {
        try { return 통신.получавам(표준종단);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public void време_на_изчакване(int 밀리초) throws В_И_изключение {
        try { 통신.време_на_изчакване(표준종단, 밀리초);
        } catch (java.io.IOException ГРЕШКА) { throw преобразувам_изключение.В_И(ГРЕШКА); }
        catch (RuntimeException ГРЕШКА) { throw преобразувам_изключение.изпълнявам_команда(ГРЕШКА); }
    }
    public int номер_на_порт() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Затворен() { 통신.Затворен(표준종단); }
}
