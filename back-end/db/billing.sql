/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : billing

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2022-03-14 11:54:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `balance`
-- ----------------------------
DROP TABLE IF EXISTS `balance`;
CREATE TABLE `balance` (
  `user_id` varchar(10) NOT NULL,
  `balance` double(10,2) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of balance
-- ----------------------------
INSERT INTO `balance` VALUES ('0', '1500.00');
INSERT INTO `balance` VALUES ('2', '53964.50');

-- ----------------------------
-- Table structure for `balance_detail`
-- ----------------------------
DROP TABLE IF EXISTS `balance_detail`;
CREATE TABLE `balance_detail` (
  `user_id` varchar(10) NOT NULL,
  `delta` double(10,0) DEFAULT NULL,
  `before` double(10,0) DEFAULT NULL,
  `after` double(10,0) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of balance_detail
-- ----------------------------

-- ----------------------------
-- Table structure for `booking`
-- ----------------------------
DROP TABLE IF EXISTS `booking`;
CREATE TABLE `booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `book_date` date DEFAULT NULL,
  `book_time` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of booking
-- ----------------------------
INSERT INTO `booking` VALUES ('3', '2', '2022-03-09', '7:00-10:00', '2022-03-13 14:45:24', '0');
INSERT INTO `booking` VALUES ('4', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:01', '2');
INSERT INTO `booking` VALUES ('5', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:05', '0');
INSERT INTO `booking` VALUES ('6', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:41', '0');
INSERT INTO `booking` VALUES ('7', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:45', '2');
INSERT INTO `booking` VALUES ('8', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:50', '0');
INSERT INTO `booking` VALUES ('9', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:46:57', '2');
INSERT INTO `booking` VALUES ('10', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:49:21', '0');
INSERT INTO `booking` VALUES ('11', '2', '2022-03-31', '7:00-10:00', '2022-03-13 14:49:32', '2');
INSERT INTO `booking` VALUES ('12', '2', '2022-03-31', '7:00-10:00', '2022-03-13 14:51:53', '0');
INSERT INTO `booking` VALUES ('13', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:51:58', '2');
INSERT INTO `booking` VALUES ('14', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:53:00', '0');
INSERT INTO `booking` VALUES ('15', '2', '2022-03-13', '7:00-10:00', '2022-03-13 14:53:03', '2');
INSERT INTO `booking` VALUES ('16', '2', '2022-03-13', '7:00-10:00', '2022-03-13 19:01:22', '0');
INSERT INTO `booking` VALUES ('17', '0', '2022-03-13', '7:00-10:00', '2022-03-13 14:53:49', '1');
INSERT INTO `booking` VALUES ('18', '2', '2022-03-13', '7:00-10:00', '2022-03-13 19:01:26', '2');
INSERT INTO `booking` VALUES ('19', '2', '2022-03-13', '7:00-10:00', '2022-03-13 19:01:29', '0');
INSERT INTO `booking` VALUES ('20', '2', '2022-03-13', '7:00-10:00', '2022-03-13 19:01:32', '0');
INSERT INTO `booking` VALUES ('21', '2', '2022-03-13', '17:00-19:00', '2022-03-13 19:02:38', '2');
INSERT INTO `booking` VALUES ('22', '2', '2022-03-13', '11:00-13:00', '2022-03-13 19:02:44', '0');
INSERT INTO `booking` VALUES ('23', '2', '2022-03-13', '11:00-13:00', '2022-03-13 19:02:46', '2');
INSERT INTO `booking` VALUES ('24', '2', '2022-03-13', '17:00-19:00', '2022-03-13 19:02:50', '2');
INSERT INTO `booking` VALUES ('25', '2', '2022-03-13', '17:00-19:00', '2022-03-13 19:02:52', '1');

-- ----------------------------
-- Table structure for `items`
-- ----------------------------
DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_type` varchar(255) DEFAULT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `item_price` double(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of items
-- ----------------------------

-- ----------------------------
-- Table structure for `orders`
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(10) DEFAULT NULL,
  `user_name` varchar(32) DEFAULT NULL,
  `sum` double(10,2) DEFAULT NULL,
  `order_type` varchar(10) DEFAULT NULL,
  `items` varchar(2000) DEFAULT NULL,
  `month` int DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `image` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES ('49', '2', 'user', '150.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:00', null);
INSERT INTO `orders` VALUES ('50', '2', 'user', '150.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:11', null);
INSERT INTO `orders` VALUES ('51', '2', 'user', '150.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:20', null);
INSERT INTO `orders` VALUES ('52', '2', 'user', '150.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:29', null);
INSERT INTO `orders` VALUES ('53', '2', 'user', '150.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:36', null);
INSERT INTO `orders` VALUES ('54', '2', 'user', '150.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 1, \"pay\": 150}', '202203', '2022-03-12 20:30:43', null);
INSERT INTO `orders` VALUES ('55', '2', 'user', '142.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 0.95, \"pay\": 142.5}', '202203', '2022-03-12 20:30:56', null);
INSERT INTO `orders` VALUES ('56', '2', 'user', '142.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 0.95, \"pay\": 142.5}', '202203', '2022-03-12 20:31:19', null);
INSERT INTO `orders` VALUES ('57', '2', 'user', '142.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 0.95, \"pay\": 142.5}', '202203', '2022-03-12 20:31:32', null);
INSERT INTO `orders` VALUES ('58', '2', 'user', '142.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 0.95, \"pay\": 142.5}', '202203', '2022-03-12 20:31:41', null);
INSERT INTO `orders` VALUES ('59', '2', 'user', '142.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 6}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 6}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 150, \"volume\": 16, \"discount\": 0.95, \"pay\": 142.5}', '202203', '2022-03-12 20:31:51', null);
INSERT INTO `orders` VALUES ('60', '2', 'user', '112.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 125, \"volume\": 13, \"discount\": 0.9, \"pay\": 112.5}', '202203', '2022-03-12 20:48:53', null);
INSERT INTO `orders` VALUES ('61', '2', 'user', '112.50', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}], \"sum\": 125, \"volume\": 13, \"discount\": 0.9, \"pay\": 112.5}', '202203', '2022-03-12 20:51:58', null);
INSERT INTO `orders` VALUES ('62', '2', 'user', '90.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 4}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 3}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 3}], \"sum\": 100, \"volume\": 10, \"discount\": 0.9, \"pay\": 90}', '202203', '2022-03-13 12:05:57', null);
INSERT INTO `orders` VALUES ('63', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 12:06:18', null);
INSERT INTO `orders` VALUES ('64', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 12:06:31', null);
INSERT INTO `orders` VALUES ('65', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 12:06:44', null);
INSERT INTO `orders` VALUES ('66', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 12:06:58', null);
INSERT INTO `orders` VALUES ('67', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 12:07:39', null);
INSERT INTO `orders` VALUES ('68', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 14:50:05', null);
INSERT INTO `orders` VALUES ('69', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 14:50:22', null);
INSERT INTO `orders` VALUES ('70', '2', 'user', '117.00', 'qr', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 14:50:36', null);
INSERT INTO `orders` VALUES ('71', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 14:51:38', null);
INSERT INTO `orders` VALUES ('72', '2', 'user', '117.00', 'balance', '{\"items\": [{\"type\": \"椭圆菜品\", \"unit\": \"¥10\", \"count\": 5}, {\"type\": \"圆形菜品\", \"unit\": \"¥15\", \"count\": 4}, {\"type\": \"方形菜品\", \"unit\": \"¥5\", \"count\": 4}], \"sum\": 130, \"volume\": 13, \"discount\": 0.9, \"pay\": 117}', '202203', '2022-03-13 18:35:13', null);

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(10) DEFAULT NULL,
  `passwd` varchar(10) DEFAULT NULL,
  `role` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'admin', '123456', 'admin');
INSERT INTO `user` VALUES ('2', 'user', '123456', 'member');
