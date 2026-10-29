// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionRechercherAdresse : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionRechercherAdresse extends ExceptionSortieEntrée {
    public ExceptionRechercherAdresse() { super(); }
    public ExceptionRechercherAdresse(String description) { super(description); }
    public String description() { return getMessage(); }
}
