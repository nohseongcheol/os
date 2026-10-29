// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionCommunication : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionCommunication extends ExceptionSortieEntrée {
    public ExceptionCommunication() { super(); }
    public ExceptionCommunication(String description) { super(description); }
    public String description() { return getMessage(); }
}
