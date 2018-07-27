#!/usr/bin/python
# -*- coding: UTF-8 -*-

book = [
    {'name': u'男生网文', 'major': [
        {'name': u'玄幻奇幻', 'minor': [u'仙侠', u'修真', u'洪荒', u'丹药', u'神话', u'玄幻', u'奇幻', u'魔界',
                                    u'升级', u'废柴', u'异界', u'阵法', u'召唤', u'精灵', u'无敌', u'诛仙', u'龙族', u'蜀山', u'西游']},
        {'name': u'都市异能', 'minor': [u'修真', u'废柴', u'美女', u'种马', u'鉴宝', u'赌石', u'腹黑', u'商战',
                                    u'爽文', u'重生', u'热血', u'黑道', u'佣兵', u'校花', u'兵王', u'逆袭', u'奇遇', u'YY', u'一男多女']},
        {'name': u'历史风云', 'minor': [u'架空', u'三国', u'民国', u'宋朝', u'隋唐', u'明朝', u'战国', u'清朝',
                                    u'权谋', u'争霸', u'抗日', u'军阀', u'无敌', u'帝王', u'爽文', u'战争', u'官场', u'将军', u'特种兵']},
        {'name': u'官场职场', 'minor': [u'商战', u'官场', u'职场',
                                    u'重生', u'励志', u'权谋', u'爽文', u'穿越', u'热血']},
        {'name': u'军事战争', 'minor': [u'军旅', u'兵王', u'特工', u'民国', u'争霸', u'爽文', u'抗日', u'抗美',
                                    u'重生', u'穿越', u'三国', u'谍战', u'越战', u'解放战', u'鸦片战', u'远征军', u'特种兵', u'狙击手', u'一二战']},
        {'name': u'无限流派', 'minor': [u'科幻', u'未来', u'热血', u'位面', u'爽文', u'宅男', u'奇遇', u'系统',
                                    u'争霸', u'召唤', u'生存', u'轮回', u'斗智', u'变身', u'升级', u'技术', u'游戏', u'空间', u'动漫']},
        {'name': u'武侠奇缘', 'minor': [u'仙侠', u'古龙', u'架空', u'搞笑', u'复仇', u'热血', u'穿越',
                                    u'爽文', u'同人', u'重生', u'奇遇', u'修真', u'斗智', u'少林', u'争霸', u'升级', u'扮猪吃虎']},
        {'name': u'科幻时空', 'minor': [u'星际', u'机甲', u'无限', u'热血', u'末世', u'未来', u'丧尸', u'位面',
                                    u'爽文', u'僵尸', u'系统', u'异界', u'召唤', u'空间', u'变异', u'无敌', u'奇遇', u'异能', u'异次元']},
        {'name': u'游戏竞技', 'minor': [u'魔兽', u'LOL', u'热血', u'爽文', u'争霸', u'升级', u'系统', u'无敌', u'机甲', u'养成', u'体育', u'足球', u'篮球', u'空间', u'位面', u'技术'
                                    ]},
        {'name': u'转世重生', 'minor': [u'架空', u'三国', u'明朝', u'争霸', u'爽文', u'都市', u'战争', u'种田',
                                    u'搞笑', u'异能', u'复仇', u'腹黑', u'权谋', u'官场', u'极品', u'美女', u'热血', u'异界', u'扮猪吃虎']},
        {'name': u'同人小说', 'minor': [u'动漫', u'影视', u'武侠', u'游戏', u'EXO', u'TFBOYS', u'王俊凯',
                                    u'韩娱', u'火影', u'综漫', u'HP', u'网王', u'龙珠', u'海贼王', u'红楼梦', u'猎人', u'家教']},
        {'name': u'古典仙侠', 'minor': [u'洪荒', u'神话', u'丹药', u'上古', u'法宝', u'争霸', u'修真', u'热血',
                                    u'升级', u'爽文', u'无敌', u'逆天', u'复仇', u'阵法', u'轮回', u'凡人', u'天才', u'魔兽', u'蜀山']},
        {'name': u'乡村生活', 'minor': [u'现代', u'种田',
                                    u'爽文', u'奇遇', u'热血', u'重生', u'搞笑', u'农民']}
    ]
    },
    {'name': u'女生网文', 'major': [
        {'name': u'都市言情', 'minor': [u'豪门', u'总裁', u'明星', u'高干', u'军婚', u'首席', u'腹黑', u'虐恋',
                                    u'专情', u'契约', u'复仇', u'黑道', u'宠文', u'宝宝', u'婚姻', u'少爷', u'霸道', u'恶魔', u'酷男']},
        {'name': u'古风古言', 'minor': [u'架空', u'腹黑', u'复仇', u'虐恋', u'专情', u'废柴', u'冤家', u'搞笑',
                                    u'清穿', u'宠文', u'唯美', u'代嫁', u'霸道', u'皇后', u'王爷', u'皇妃', u'帝王', u'将军', u'嫡女']},
        {'name': u'穿越重生', 'minor': [u'魂穿', u'清穿', u'架空', u'腹黑', u'搞笑', u'专情', u'复仇', u'废柴',
                                    u'女强', u'冤家', u'虐恋', u'民国', u'异界', u'种田', u'宠文', u'帝王', u'皇后', u'宫斗', u'古穿今']},
        {'name': u'悬疑灵异', 'minor': [u'盗墓', u'推理', u'僵尸', u'鬼怪', u'阴阳', u'侦探', u'诡异',
                                    u'探险', u'法师', u'风水', u'亡灵', u'道士', u'丧尸', u'末世', u'变异', u'死神', u'赶尸']},
        {'name': u'种田经商', 'minor': [u'穿越', u'搞笑', u'专情', u'古言', u'空间', u'重生',
                                    u'布衣', u'励志', u'宅斗', u'宠文', u'腹黑', u'爽文', u'女强', u'皇妃', u'轻松']},
        {'name': u'宫廷宅斗', 'minor': [u'穿越', u'重生', u'帝王', u'皇后', u'复仇', u'专情',
                                    u'女强', u'腹黑', u'虐恋', u'爽文', u'权谋', u'冤家', u'公主', u'架空', u'皇妃']},
        {'name': u'青春校园', 'minor': [u'纯爱', u'恶魔', u'校草', u'贵族', u'酷男', u'黑道', u'专情', u'腹黑',
                                    u'虐恋', u'唯美', u'搞笑', u'霸道', u'冤家', u'明星', u'宠文', u'暗恋', u'王子', u'公主', u'灰姑娘']},
        {'name': u'幻想言情', 'minor': [u'仙侠', u'腹黑', u'虐恋', u'女强', u'搞笑', u'纯爱', u'专情',
                                    u'宠文', u'复仇', u'冤家', u'狐仙', u'修真', u'架空', u'穿越', u'重生', u'异能', u'动漫', u'吸血鬼']},
        {'name': u'耽美百合', 'minor': [u'纯爱', u'耽美', u'百合', u'生子',
                                    u'强强', u'年下', u'宠文', u'冤家', u'腹黑', u'虐恋', u'重生', u'同人']},
        {'name': u'女尊王朝', 'minor': [u'穿越', u'重生', u'帝王', u'腹黑', u'复仇', u'专情', u'架空',
                                    u'宫斗', u'爽文', u'种田', u'古言', u'虐恋', u'将军', u'宠文', u'搞笑', u'玄幻', u'异能']},
        {'name': u'网游情缘', 'minor': [u'网游', u'游戏', u'专情']},
        {'name': u'短篇小说', 'minor': []}
    ]
    },
    {'name': u'出版读物', 'major': [
        {'name': u'名家经典', 'minor': [u'古典文学', u'外国名著']},
        {'name': u'散文诗歌', 'minor': []},
        {'name': u'影视文学', 'minor': []},
        {'name': u'畅销小说', 'minor': []},
        {'name': u'社科科普', 'minor': []},
        {'name': u'励志成功', 'minor': []},
        {'name': u'社会百态', 'minor': []},
        {'name': u'教育教辅', 'minor': []},
        {'name': u'养生保健', 'minor': []},
        {'name': u'生活休闲', 'minor': []},
        {'name': u'传记纪实', 'minor': []},
        {'name': u'童话寓言', 'minor': []},
        {'name': u'婚姻两性', 'minor': []},
        {'name': u'经管理财', 'minor': []},
        {'name': u'历史百科', 'minor': []},
        {'name': u'美食旅行', 'minor': []}
    ]
    }
]

private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQCpsOUR/BUIJvkuVn0Xuu/r4GLSLDw4rA7C/cF1XMfba7Wxly7z\n76uGFuLHDrYHmKYnYwc8XeVnV/2ur+Db7k3YGg78turtDQOGM1Cn1koY4mRXuT0P\nGaE5V++/5uczZYRt+YA6IgdYbeNn4rd1VZBSlcYdzspnkVfrZMYdB+NHcQIDAQAB\nAoGBAI6pc8yM/DmgWnoEqKKcvTy3px0/p1mV/csdf9nlqPjmMxkdG5Jl+vR+pSXp\nTkxQn9AZR2oPHuClb1e/8fG1Bae8mpFa1ew6OydxcKA8Id8N4Scq80L899nSqBiI\nyytnRDd3iWQQKRNW4T5+T0ibuwZisu77yKwUgpGMtsMokU9hAkEAytdNNi1suSNr\nY8WjrVEH9rwX9F9lxcr2SwGE+Vo0w7qBbG2rgjDELublwi3dxSXOHjbv6GEyB5qa\n2jk1D50yDQJBANYpiuJACbBsMPFZVKE+5NtDpK0X9Cshu3E06bdizj5lyMalIU8g\nk+4oPewGwhnC7RMJLFOGhxfWgaMSa/3wpfUCQGDrMtdaKQLlK6DGhIiBmT6JbSC0\nnFo/uiLonPLP6TpEWSbH2BUi2/pVFR8M71QN1kiVk1gDaPY9JxRyFSpav9kCQQCm\nbsRrDd85xurGNWkKoqkSKWBp0GrFtkJIORnElbm4TjuY/K2FI8ky1P1CVwIzKQQ6\nve8/vhVwlhhLFb7tKz6dAkBEdMzvtJH/07rk0PEM+ggru1HgV5q6dmABHQohOq2R\nQt39E4mlnZ6ePeOsx4GDnssYob1lv8xghU2PJyA6n+e2\n-----END RSA PRIVATE KEY-----'
