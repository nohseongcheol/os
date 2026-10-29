// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** Байланысу(連結)·Арна_енгізу(通路): 상대와 이어진 TCP байт_мән 흐름의 қатысушы. */
public final class қосылым {
    private final java.net.Socket 표준연결;
    қосылым(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static қосылым Ашу(String мекенжай, int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try {
            return new қосылым(new java.net.Socket(мекенжай, порт_нөмірі));
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public кіріс_ағыны 입력() throws енгізу_шығару_ерекшелік {
        try { return new кіріс_ағыны(표준연결.getInputStream());
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public шығыс_ағыны Шығысы() throws енгізу_шығару_ерекшелік {
        try { return new шығыс_ағыны(표준연결.getOutputStream());
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void ТАЙМ_АУТ(int 밀리초) throws енгізу_шығару_ерекшелік {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public int порт_нөмірі() { return 표준연결.getPort(); }
    public int жергілікті_порт_нөмірі() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Жабу() throws енгізу_шығару_ерекшелік {
        try { 표준연결.close();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
