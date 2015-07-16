/*
Navicat MySQL Data Transfer

Source Server         : localhost_3309
Source Server Version : 50403
Source Host           : localhost:3309
Source Database       : eia

Target Server Type    : MYSQL
Target Server Version : 50403
File Encoding         : 65001

Date: 2015-07-15 21:40:25
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
INSERT INTO `buyers` VALUES ('2', 'steve', '123', 'sdfsad@asu.edu');
INSERT INTO `buyers` VALUES ('4', 'steve2', '123', 'sdfsa2d@asu.edu');
INSERT INTO `buyers` VALUES ('5', 'lily2', '123', 'lily2@asu.edu');

-- ----------------------------
-- Table structure for `category_function`
-- ----------------------------
DROP TABLE IF EXISTS `category_function`;
CREATE TABLE `category_function` (
  `cid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

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
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

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
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of developers
-- ----------------------------
INSERT INTO `developers` VALUES ('1', 'dev1', '123', 'dev1@gmail.com');
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
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of img
-- ----------------------------
INSERT INTO `img` VALUES ('11', 'static/upload\\2861282448.png', '28', '1');
INSERT INTO `img` VALUES ('12', 'static/upload\\2861282448.png', '28', '0');
INSERT INTO `img` VALUES ('13', 'static/upload\\2965213729.png', '29', '1');
INSERT INTO `img` VALUES ('14', 'static/upload\\3063030450', '30', '1');
INSERT INTO `img` VALUES ('15', 'static/upload\\3163382375', '31', '1');
INSERT INTO `img` VALUES ('16', 'static/upload\\3281615953123.jpg', '32', '1');
INSERT INTO `img` VALUES ('17', 'static/upload\\33186321051.png', '33', '1');
INSERT INTO `img` VALUES ('18', 'static/upload\\2861282448.png', '1', '0');
INSERT INTO `img` VALUES ('19', 'static/upload\\2861282448.png', '2', '0');
INSERT INTO `img` VALUES ('20', 'static/upload\\2861282448.png', '7', '0');
INSERT INTO `img` VALUES ('21', 'static/upload\\354068439', '35', '1');
INSERT INTO `img` VALUES ('22', 'static/upload\\3695684534123.jpg', '36', '1');
INSERT INTO `img` VALUES ('23', 'static/upload\\366921661aaa.jpg', '36', '1');
INSERT INTO `img` VALUES ('24', 'http://applatform-domain1.stor.sinaapp.com/3724915482logo.png', '37', '1');
INSERT INTO `img` VALUES ('25', 'http://applatform-domain1.stor.sinaapp.com/3789867408skype.png', '37', '1');
INSERT INTO `img` VALUES ('26', 'http://applatform-domain1.stor.sinaapp.com/3831154460logo.png', '38', '1');
INSERT INTO `img` VALUES ('27', 'http://applatform-domain1.stor.sinaapp.com/3865586991skype.png', '38', '1');

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
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('1', '1', '1', '2015-07-14 20:04:40', '99.99');
INSERT INTO `orders` VALUES ('2', '2', '1', '0000-00-00 00:00:00', null);
INSERT INTO `orders` VALUES ('3', '37', '5', '0000-00-00 00:00:00', null);

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
) ENGINE=MyISAM AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES ('37', 'dev2_app1', '2', 'asvdadsvsadvsadvdvdsvds', '999.00', '', '1', '1');
INSERT INTO `products` VALUES ('38', 'app999', '2', 'csdc', '999.00', '', '2', '1');
