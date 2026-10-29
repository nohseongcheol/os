import tiếngViệt

def chào(tên):
    lờiChào = "안녕하세요 " + tên
    tiếngViệt.ghiTệp("LờiChào.txt", lờiChào)
    tiếngViệt.ĐầuRa(tiếngViệt.giảiMãVănBản(tiếngViệt.đọcTệp("LờiChào.txt")))

chào("누리")
