/*
Navicat MySQL Data Transfer

Source Server         : localhost_3309
Source Server Version : 50403
Source Host           : localhost:3309
Source Database       : eia

Target Server Type    : MYSQL
Target Server Version : 50403
File Encoding         : 65001

Date: 2015-07-14 22:12:54
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `buyers`
-- ----------------------------
DROP TABLE IF EXISTS `buyers`;
CREATE TABLE `buyers` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `buyers_k2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buyers
-- ----------------------------
INSERT INTO `buyers` VALUES ('1', 'lily', '123', 'lily@asu.edu');
INSERT INTO `buyers` VALUES ('2', 'steve', '123', 'sdfsad@asu.edu');
INSERT INTO `buyers` VALUES ('4', 'steve2', '123', 'sdfsa2d@asu.edu');

-- ----------------------------
-- Table structure for `category_function`
-- ----------------------------
DROP TABLE IF EXISTS `category_function`;
CREATE TABLE `category_function` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of category_function
-- ----------------------------
INSERT INTO `category_function` VALUES ('1', 'business', null);
INSERT INTO `category_function` VALUES ('2', 'education', null);
INSERT INTO `category_function` VALUES ('3', 'games', null);
INSERT INTO `category_function` VALUES ('4', 'travel', null);

-- ----------------------------
-- Table structure for `category_ui_style`
-- ----------------------------
DROP TABLE IF EXISTS `category_ui_style`;
CREATE TABLE `category_ui_style` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of category_ui_style
-- ----------------------------
INSERT INTO `category_ui_style` VALUES ('1', 'plain', null);
INSERT INTO `category_ui_style` VALUES ('2', 'metro', null);

-- ----------------------------
-- Table structure for `developers`
-- ----------------------------
DROP TABLE IF EXISTS `developers`;
CREATE TABLE `developers` (
  `uid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `developers_k2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of developers
-- ----------------------------
INSERT INTO `developers` VALUES ('1', 'dev1', '123', 'dev1@gmail.com');

-- ----------------------------
-- Table structure for `orders`
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `oid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `buyer_uid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `price` double(15,2) NOT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('1', '1', '1', '2015-07-14 20:04:40', '99.99');

-- ----------------------------
-- Table structure for `products`
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `pid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `dev_uid` int(11) NOT NULL,
  `description` varchar(1000) NOT NULL DEFAULT '',
  `price` double(15,2) NOT NULL,
  `img` varchar(20000) DEFAULT '',
  `c_function` int(11) DEFAULT NULL,
  `c_ui_style` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `products_k1` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES ('1', 'airbnb', '1', 'Rent unique accommodations from local hosts in 190+ countries. Feel at home anywhere you go in the world with Airbnb.', '99.99', '', '4', '1');
INSERT INTO `products` VALUES ('2', 'uno', '1', 'Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ', '19.99', '', '3', '2');
INSERT INTO `products` VALUES ('4', 'uno2', '1', 'Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ', '29.99', '', '4', '2');
INSERT INTO `products` VALUES ('5', 'uno3', '1', 'Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ', '39.99', '', '4', '1');
INSERT INTO `products` VALUES ('6', 'uno4', '1', 'Uno (/ˈuːnoʊ/; from Italian and Spanish for \'one\') is an American card game which is played with a specially printed deck (see Mau Mau for an almost identical game played with normal playing cards). ', '49.88', '', '4', '1');
