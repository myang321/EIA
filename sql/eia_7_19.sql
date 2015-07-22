/*
Navicat MySQL Data Transfer

Source Server         : localhost_3309
Source Server Version : 50403
Source Host           : localhost:3309
Source Database       : eia

Target Server Type    : MYSQL
Target Server Version : 50403
File Encoding         : 65001

Date: 2015-07-19 16:03:06
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
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of buyers
-- ----------------------------
INSERT INTO `buyers` VALUES ('1', 'lily', '123', 'lily@asu.edu');
INSERT INTO `buyers` VALUES ('2', 'steve', '123', 'steve@asu.edu');
INSERT INTO `buyers` VALUES ('4', 'steve2', '123', 'sdfsa2d@asu.edu');
INSERT INTO `buyers` VALUES ('5', 'lily2', '123', 'lily2@asu.edu');

-- ----------------------------
-- Table structure for `category`
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES ('1', 'c_func', 'travel', null);
INSERT INTO `category` VALUES ('2', 'c_func', 'lifestyle', null);
INSERT INTO `category` VALUES ('3', 'c_func', 'travel', null);
INSERT INTO `category` VALUES ('4', 'c_func', 'education', null);
INSERT INTO `category` VALUES ('5', 'c_func', 'multimedia', null);
INSERT INTO `category` VALUES ('6', 'c_func', 'finance', null);
INSERT INTO `category` VALUES ('7', 'c_func', 'social-networking', null);
INSERT INTO `category` VALUES ('8', 'c_func', 'o2o-service', null);
INSERT INTO `category` VALUES ('9', 'c_func', 'information center', null);
INSERT INTO `category` VALUES ('10', 'c_func', 'health', null);
INSERT INTO `category` VALUES ('11', 'c_func', 'entertainment', null);
INSERT INTO `category` VALUES ('12', 'c_ui', 'windows-style', null);
INSERT INTO `category` VALUES ('13', 'c_ui', 'apple-style', null);
INSERT INTO `category` VALUES ('14', 'c_ui', 'Responsive', null);
INSERT INTO `category` VALUES ('15', 'c_ui', 'Horizontal', null);
INSERT INTO `category` VALUES ('16', 'c_ui', 'Cute', null);

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
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of developers
-- ----------------------------
INSERT INTO `developers` VALUES ('1', 'dev1', '123', 'phoenix13sunsi@gmail.com');
INSERT INTO `developers` VALUES ('2', 'dev2', '123', 'dev2@asu.edu');

-- ----------------------------
-- Table structure for `img`
-- ----------------------------
DROP TABLE IF EXISTS `img`;
CREATE TABLE `img` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(2000) NOT NULL,
  `pid` int(11) NOT NULL,
  `front` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of img
-- ----------------------------

-- ----------------------------
-- Table structure for `orders`
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `oid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `buyer_uid` int(11) NOT NULL,
  `date` timestamp NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `price` double(15,2) DEFAULT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------

-- ----------------------------
-- Table structure for `product_category`
-- ----------------------------
DROP TABLE IF EXISTS `product_category`;
CREATE TABLE `product_category` (
  `pid` int(11) NOT NULL,
  `cid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of product_category
-- ----------------------------

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
  PRIMARY KEY (`pid`),
  UNIQUE KEY `products_k1` (`title`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of products
-- ----------------------------
