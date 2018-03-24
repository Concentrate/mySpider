import pymysql

# 头条news item
#     新闻item
# {
#     single_mode: false,
#     middle_mode: true,
#     more_mode: true,
#     tag: "news",
#     tag_url: "search/?keyword=%E5%85%B6%E5%AE%83",
#     title: "以前喝水的只能叫水壶，今年流行这样的保温杯，热水能保温几天",
#     chinese_tag: "其它",
#     source: "换个活法儿",
#     group_source: 7,
#     image_url: "//p3.pstatp.com/list/pgc-image/1521872528489bdcbfffbf3",
#     media_url: "/c/user/71746844397/",
#     media_avatar_url: "//p3.pstatp.com/large/3ecb0003cedb70ff7b0b",
#     image_list: [
#         {
#             url: "//p3.pstatp.com/list/190x124/pgc-image/1521872528489bdcbfffbf3"
#         },
#         {
#             url: "//p9.pstatp.com/list/190x124/pgc-image/152187236741293d934ec7a"
#         },
#         {
#             url: "//p3.pstatp.com/list/190x124/pgc-image/1521872495247cc1a26f349"
#         },
#         {
#             url: "//p3.pstatp.com/list/190x124/pgc-image/1521872528489bdcbfffbf3"
#         }
#     ],
#     gallary_image_count: 10,
#     source_url: "/group/6536392961465254404/",
#     article_genre: "gallery",
#     item_id: "6536392961465254404",
#     is_feed_ad: false,
#     behot_time: 1521873301,
#     has_gallery: true,
#     group_id: "6536392961465254404",
#     middle_image: "http://p3.pstatp.com/list/pgc-image/1521872528489bdcbfffbf3"
# },

# video item
# {
#     single_mode: true,
#     abstract: "非洲妈妈背着孩子做饭",
#     middle_mode: true,
#     more_mode: false,
#     tag: "video_motherbaby",
#     has_gallery: false,
#     label: [
#         "非洲"
#     ],
#     tag_url: "video",
#     title: "非洲妈妈背着孩子做饭",
#     has_video: true,
#     chinese_tag: "视频",
#     source: "我咋那么美捏",
#     group_source: 2,
#     comments_count: 14,
#     media_url: "/c/user/84921339042/",
#     media_avatar_url: "//p2.pstatp.com/large/587800161de6db610192",
#     video_duration_str: "00:11",
#     source_url: "/group/6536090696900674055/",
#     article_genre: "video",
#     item_id: "6536090696900674055",
#     is_feed_ad: false,
#     video_id: "4619ed920db7460fa73576830e9060f8",
#     behot_time: 1521873286,
#     image_url: "//p3.pstatp.com/list/190x124/71150009f0a9792fefc1",
#     video_play_count: 163716,
#     group_id: "6536090696900674055",
#     middle_image: "http://p3.pstatp.com/list/71150009f0a9792fefc1"
# }

con = pymysql.connect(host="localhost", user="ldy", password="abcd1234",
                      database="spider", charset="utf8")
cursor = con.cursor()


def storeToutiaoNewsInDataBase(data):
    for tmp in data:
        try:
            ex_sql1 = '''
            insert into toutiao_news(item_id,title,tag,tag_url,chinese_tag,source,source_url,image_url,media_url,
            media_avatar_url,behot_time,group_id,middle_image,comments_count,video_duration_str,video_play_count,video_id)
            VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}","{12}","{13}","{14}","{15}","{16}")
            '''
            sql_insert_images = '''
            insert into toutiao_imageurls(id,image_url) VALUES (%s,%s)
            '''
            sql_labels = '''
            insert into toutiao_news_labels(id,label)VALUES (%s,%s)
            '''

            real_sql = ex_sql1.format(
                tmp.get("item_id"), tmp.get("title", ""), tmp.get("tag"), tmp.get("tag_url"), tmp.get("chinese_tag"),
                tmp.get("source"), "https://www.toutiao.com" + tmp.get("source_url"), tmp.get("image_url"),
                tmp.get("media_url"), tmp.get("media_avatar_url"),
                tmp.get("behot_time", 0), tmp.get("group_id", 0), tmp.get("middle_image"), tmp.get("comments_count", 0),
                tmp.get("video_duration"),
                tmp.get("video_play_count", 0), tmp.get("video_id", 0))
            print("real sql is {0}".format(real_sql))
            images_list = tmp.get("image_list")
            result = cursor.execute(real_sql)
            print("execute result is %s" % result)
            if images_list and len(images_list) > 1:
                for a1 in images_list:
                    cursor.execute(sql_insert_images, (tmp.get("item_id"), str(a1)))
            label_list = tmp.get("label")
            if label_list and len(label_list) >= 1:
                for a1 in label_list:
                    cursor.execute(sql_labels, (tmp.get("item_id"), str(a1)))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
