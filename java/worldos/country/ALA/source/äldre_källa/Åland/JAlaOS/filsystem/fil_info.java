// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Åland.JAlaOS.filsystem;

public final class fil_info {
    private final int Storlek;
    private final int form_variant;

    public fil_info(int Storlek, int form_variant) {
        this.Storlek = Storlek;
        this.form_variant = form_variant;
    }

    public int Storlek() {
        return Storlek;
    }

    public int form_variant() {
        return form_variant;
    }
}

