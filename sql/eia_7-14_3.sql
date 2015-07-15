# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.24)
# Database: eia
# Generation Time: 2015-07-15 02:28:56 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table buyers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `buyers`;

CREATE TABLE `buyers` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `buyers_k2` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `buyers` WRITE;
/*!40000 ALTER TABLE `buyers` DISABLE KEYS */;

INSERT INTO `buyers` (`uid`, `username`, `password`, `email`)
VALUES
	(1,'lily','123','lily@asu.edu'),
	(2,'steve','123','sdfsad@asu.edu'),
	(4,'steve2','123','sdfsa2d@asu.edu');

/*!40000 ALTER TABLE `buyers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table category_function
# ------------------------------------------------------------

DROP TABLE IF EXISTS `category_function`;

CREATE TABLE `category_function` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `category_function` WRITE;
/*!40000 ALTER TABLE `category_function` DISABLE KEYS */;

INSERT INTO `category_function` (`cid`, `title`, `description`)
VALUES
	(1,'business',NULL),
	(2,'education',NULL),
	(3,'games',NULL),
	(4,'travel',NULL);

/*!40000 ALTER TABLE `category_function` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table category_ui_style
# ------------------------------------------------------------

DROP TABLE IF EXISTS `category_ui_style`;

CREATE TABLE `category_ui_style` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `category_ui_style` WRITE;
/*!40000 ALTER TABLE `category_ui_style` DISABLE KEYS */;

INSERT INTO `category_ui_style` (`cid`, `title`, `description`)
VALUES
	(1,'plain',NULL),
	(2,'metro',NULL);

/*!40000 ALTER TABLE `category_ui_style` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table developers
# ------------------------------------------------------------

DROP TABLE IF EXISTS `developers`;

CREATE TABLE `developers` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `developers_k2` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `developers` WRITE;
/*!40000 ALTER TABLE `developers` DISABLE KEYS */;

INSERT INTO `developers` (`uid`, `username`, `password`, `email`)
VALUES
	(1,'dev1','123','dev1@gmail.com');

/*!40000 ALTER TABLE `developers` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table orders
# ------------------------------------------------------------

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `oid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `price` double(15,2) NOT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;

INSERT INTO `orders` (`oid`, `pid`, `date`, `price`)
VALUES
	(1,1,'2015-07-13 18:30:21',99.99);

/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table products
# ------------------------------------------------------------

DROP TABLE IF EXISTS `products`;

CREATE TABLE `products` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL DEFAULT '',
  `price` double(15,2) NOT NULL,
  `img` varchar(20000) DEFAULT '',
  `c_function` int(11) DEFAULT NULL,
  `c_ui_style` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `products_k1` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;

INSERT INTO `products` (`pid`, `title`, `description`, `price`, `img`, `c_function`, `c_ui_style`)
VALUES
	(1,'airbnb','Rent unique accommodations from local hosts in 190+ countries. Feel at home anywhere you go in the world with Airbnb.',99.99,'',4,1),
	(2,'uno','Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ',19.99,'',3,2),
	(4,'uno2','Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ',29.99,'',4,2),
	(5,'uno3','Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ',39.99,'',4,1),
	(6,'uno4','Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ',49.88,'',4,1);

/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
