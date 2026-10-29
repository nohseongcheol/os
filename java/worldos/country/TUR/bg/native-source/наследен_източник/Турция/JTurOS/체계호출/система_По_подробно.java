// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Турция.JTurOS.체계호출;

public final class система_По_подробно {
    private final String система_препратка_към_клетка;
    private final String възел_препратка_към_клетка;
    private final String издание_стойност;
    private final String версия_стойност;
    private final String машина;

    public система_По_подробно(String система_препратка_към_клетка, String възел_препратка_към_клетка, String издание_стойност, String версия_стойност, String машина) {
        this.система_препратка_към_клетка = система_препратка_към_клетка;
        this.възел_препратка_към_клетка = възел_препратка_към_клетка;
        this.издание_стойност = издание_стойност;
        this.версия_стойност = версия_стойност;
        this.машина = машина;
    }

    public String система_препратка_към_клетка() { return система_препратка_към_клетка; }
    public String възел_препратка_към_клетка() { return възел_препратка_към_клетка; }
    public String издание_стойност() { return издание_стойност; }
    public String версия_стойност() { return версия_стойност; }
    public String машина() { return машина; }
}
