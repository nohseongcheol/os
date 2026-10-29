// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Regno_Unito.JGbrOS.file_system;

public final class File_info {
    private final int Dimensione;
    private final int forma_Kind;

    public File_info(int Dimensione, int forma_Kind) {
        this.Dimensione = Dimensione;
        this.forma_Kind = forma_Kind;
    }

    public int Dimensione() {
        return Dimensione;
    }

    public int forma_Kind() {
        return forma_Kind;
    }
}

