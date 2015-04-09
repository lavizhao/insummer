封装完成

    创建LexRank或者TextRank类只需要传入一个question类实例即可
    然后extract()是抽取摘要，返回地址
    该地址给evaluation(path,flags)中，进行rouge评分(flags是指定'lex''text'的，防止评分覆盖
