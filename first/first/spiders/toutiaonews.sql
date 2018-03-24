use spider;
create table if not exists toutiao_news (
item_id bigint not null,
title varchar(300),
tag varchar(300),
tag_url varchar(300),
chinese_tag varchar(100),
source  varchar(200),
source_url varchar(200),
image_url varchar(200),
media_url varchar(200),
media_avatar_url varchar(200),
behot_time long,
group_id long,
middle_image varchar(200),
comments_count int,
video_duration_str varchar(200),
video_play_count int,
video_id long,
primary key(item_id) ) default charset= utf8;

create table if not exists toutiao_imageurls (
id bigint not null,
image_url varchar(200))default charset=utf8;
create table if not exists toutiao_news_labels(id bigint not null,
label varchar(100)) default charset=utf8;
desc toutiao_news;
desc toutiao_imageurls;
desc toutiao_news_labels;

