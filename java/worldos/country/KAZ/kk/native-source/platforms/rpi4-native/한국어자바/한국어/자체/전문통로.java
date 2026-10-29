// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·Арна_енгізу(通路): 경계를 가진 UDP 자료를 주고받는 қатысушы. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { 표준종단 = 통신.Ашу(порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static 전문통로 Ашу(int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { return new 전문통로(порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void жіберу(String мекенжай, int порт_нөмірі, String деректер) throws енгізу_шығару_ерекшелік {
        try { 통신.жіберу(표준종단, мекенжай, порт_нөмірі, деректер);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public String 받기() throws енгізу_шығару_ерекшелік {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void ТАЙМ_АУТ(int 밀리초) throws енгізу_шығару_ерекшелік {
        try { 통신.ТАЙМ_АУТ(표준종단, 밀리초);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public int порт_нөмірі() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void Жабу() { 통신.Жабу(표준종단); }
}
