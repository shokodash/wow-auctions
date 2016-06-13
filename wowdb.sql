drop database if exists wowauction;

create database wowauction;

use wowauction;

create table meta0
(
id int not null auto_increment,
timeinsert datetime not null,
timejson varchar(100),
primary key (id)
);

create table data0
(
id int not null auto_increment,
ownerrealm varchar(50),
itemid varchar(30),
bid varchar(30),
meta0id int not null,
primary key (id),
foreign key (meta0id) references meta0(id)
);