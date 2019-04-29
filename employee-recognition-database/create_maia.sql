-- 1: 	Create a new Google Cloud SQL project [1]
-- 		Current Project Name: 		maia-backend
-- 		Current SQL Instance Name: 	employee-recognition-database
-- 		Database Name: 				maia
--
-- 2:	Connect to DB using Google Cloud SQL Command Line
-- 		gcloud sql connect employee-recognition-database --user=root
--
-- 3: 	Run the following SQL [2-8]: 

-- Create 'maia' database

create database maia;
use maia;

-- Create users, admins, awards tables

create table if not exists users (user_id int not null primary key auto_increment, first_name varchar(256) not null, last_name varchar(256) not null, email_address varchar(256) not null, password varchar (256) not null, created_timestamp timestamp not null, signature_path varchar(256) default null);
create table if not exists admins (admin_id int not null primary key auto_increment, first_name varchar(256) not null, last_name varchar(256) not null, email_address varchar(256) not null, password varchar(256) not null, created_timestamp timestamp not null); 
create table if not exists awards (award_id int not null primary key auto_increment, authorizing_user_id int,  receiving_user_id int, foreign key (receiving_user_id) references users(user_id) on delete set null on update set null, foreign key (receiving_user_id) references users(user_id) on delete set null on update set null, type enum('week', 'month') not null, distributed boolean not null, awarded_datetime datetime not null);

-- Insert test data into tables 

insert into users (first_name, last_name, email_address, password, created_timestamp, signature_path ) values ('Natasha', 'Kvavle', 'kvavlen@oregonstate.edu', 'encryptme', '2019-04-15 08:52:00', 'kvavlen_sig.jpg');
insert into users (first_name, last_name, email_address, password, created_timestamp, signature_path ) values ('Patrick', 'DeLeon', 'deleonp@oregonstate.edu', 'encryptme', '2019-04-15 08:52:00', 'deleonp_sig.jpg');
insert into admins (first_name, last_name, email_address, password, created_timestamp ) values ('Conner', 'Pappas', 'pappasc@oregonstate.edu', 'encryptme', '2019-04-15 08:52:00'); 
insert into awards (authorizing_user_id, receiving_user_id, type, distributed, awarded_datetime) values (1, 2, 'week', false, '2019-04-27 10:00:00');

-- Create user for api -- no access restrictions will occur between admins/users at the database level

create user if not exists api_user;

-- Privileges: 	SELECT, UPDATE, DELETE admins, awards, users;

grant select, insert, update, delete on admins to api_user;
grant select, insert, update, delete on users to api_user;
grant select, insert, update, delete on awards to api_user;

-- Set passwords for users

set password for api_user = 'tj348$';

-- References
-- [1] https://cloud.google.com/sql/docs/mysql/quickstart 
-- [2] https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line
-- [3] https://dev.mysql.com/doc/refman/5.7/en/create-table.html
-- [4] https://dev.mysql.com/doc/refman/5.7/en/create-table-foreign-keys.html
-- [5] https://dev.mysql.com/doc/refman/5.7/en/enum.html
-- [6] https://dev.mysql.com/doc/refman/8.0/en/datetime.html
-- [7] https://www.w3schools.com/sql/sql_update.asp
-- [8] https://dev.mysql.com/doc/refman/5.7/en/account-management-sql.html (13.7.1.2, 13.7.1.4, 13.7.1.7)