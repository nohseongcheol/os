// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutschland.JDeuOS.DateiSystem;

public final class dateiInformation {
    private final int größe;
    private final int formArt;

    public dateiInformation(int größe, int formArt) {
        this.größe = größe;
        this.formArt = formArt;
    }

    public int größe() {
        return größe;
    }

    public int formArt() {
        return formArt;
    }
}

