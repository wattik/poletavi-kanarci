-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;

CREATE SCHEMA `KANARCI`;


-- ************************************** `SOURCES`

CREATE TABLE `SOURCES`
(
 `SOURCE_ID`      NUMERIC NOT NULL AUTO_INCREMENT ,
 `SOURCE_NAME`    VARCHAR(50) NOT NULL ,
 `SOURCE_TEXT_ID` VARCHAR(10) NOT NULL ,

PRIMARY KEY (`SOURCE_ID`)
);





-- ************************************** `TOPICS`

CREATE TABLE `TOPICS`
(
 `TOPIC_ID`          NUMERIC NOT NULL AUTO_INCREMENT ,
 `TOPIC_NAME`        VARCHAR(50) NOT NULL ,
 `TOPIC_DESCRIPTION` VARCHAR(200) NOT NULL ,

PRIMARY KEY (`TOPIC_ID`)
);





-- ************************************** `RECORDS`

CREATE TABLE `RECORDS`
(
 `RECORD_ID`         NOT NULL COMMENT 'Automatically generated primary key identifier.' ,
 `SOURCE_ID`        NUMERIC NOT NULL COMMENT 'Source ID' ,
 `TOPIC_ID`         NUMERIC NOT NULL COMMENT 'Topic ID' ,
 `ENTRY_ID`         VARCHAR(50) COMMENT 'Id of the entry, has different format for different sources.' ,
 `URL`              VARCHAR(100) COMMENT 'Full link of the record.' ,
 `AUTHOR`           VARCHAR(100) COMMENT 'Author name of the record. Can be used for filtering users as "NBABot" etc.' ,
 `TITLE`            VARCHAR(250) COMMENT 'Title of the record, used in sources like Google News or Reddit. Twitter data have null as a title.' ,
 `TEXT`             VARCHAR(3000) COMMENT 'Text of the record ' ,
 `CREATED_DATETIME` DATETIME COMMENT 'Datetime the record was published' ,
 `COMMENT_NUMBER`   NUMERIC COMMENT 'Number of comments' ,
 `UPVOTE_NUMBER`    NUMERIC COMMENT 'Number of upvotes / favorites' ,
 `DOWNVOTE_NUMBER`  NUMERIC COMMENT 'Number of downvotes' ,
 `RETWEET_NUMBER`   NUMERIC COMMENT 'Number of retweets' ,
 `IS_RESPONSE`      VARCHAR(1) COMMENT 'Flag determining whether record is a retweet or reply to other record. {'Y', 'N', 'X'}' ,
 `QUERY`            VARCHAR(50) COMMENT 'Crawler query used to generate record' ,
 `DATE_INSERTED`    DATE NOT NULL COMMENT 'Audit attribute for tracking data flow' ,

PRIMARY KEY (`RECORD_ID`),
KEY `fkIdx_121` (`SOURCE_ID`),
CONSTRAINT `FK_120` FOREIGN KEY `fkIdx_121` (`SOURCE_ID`) REFERENCES `SOURCES` (`SOURCE_ID`),
KEY `fkIdx_162` (`TOPIC_ID`),
CONSTRAINT `FK_162` FOREIGN KEY `fkIdx_162` (`TOPIC_ID`) REFERENCES `TOPICS` (`TOPIC_ID`),
KEY `REC_IDX1` (`SOURCE_ID`, `CREATED_DATETIME`),
KEY `REC_IDX2` (`DATE_INSERTED`, `SOURCE_ID`)
);





