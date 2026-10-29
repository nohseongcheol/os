// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionSortieEntrée : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionSortieEntrée extends java.io.IOException {
    public ExceptionSortieEntrée() { super(); }
    public ExceptionSortieEntrée(String description) { super(description); }
    public String description() { return getMessage(); }
}
