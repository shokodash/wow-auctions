drop database if exists wowauction;
drop user if exists 'testuser';

create database wowauction;
grant all on wowauction.* to 'testuser'@'localhost' identified by 'ThreeFour34$';

use wowauction;

create table meta
(
id int not null auto_increment,
timeinsert datetime not null,
timejson varchar(100),
primary key (id)
);

create table data
(
id int not null auto_increment,
auc varchar(50), 
item varchar(50), 
owner varchar(50), 
ownerrealm varchar(50),
bid varchar(50),
buyout varchar(50), 
quantity varchar(50), 
timeleft varchar(50), 
rand varchar(50), 
seed varchar(50), 
context varchar(50),
metaid int not null,
primary key (id),
foreign key (metaid) references meta(id)
);


