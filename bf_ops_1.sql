-- MySQL dump 10.13  Distrib 5.7.38, for Linux (x86_64)
--
-- Host: iamIPaddr    Database: ck_ops
-- ------------------------------------------------------
-- Server version	5.7.38

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `ck_ops`
--

/*!40000 DROP DATABASE IF EXISTS `ck_ops`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ck_ops` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `ck_ops`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('iamIPaddrd');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `com_company`
--

DROP TABLE IF EXISTS `com_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `com_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `site` varchar(200) NOT NULL,
  `address` varchar(200) NOT NULL,
  `tel` varchar(50) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `com_company`
--

LOCK TABLES `com_company` WRITE;
/*!40000 ALTER TABLE `com_company` DISABLE KEYS */;
INSERT INTO `com_company` VALUES (1,'beta-cd','https://www.betack.com','成都市高新区**中心W1区5025','iamIPaddr',1,'iamIPaddr 10:58:21',1,'iamIPaddr 10:58:36');
/*!40000 ALTER TABLE `com_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `com_department`
--

DROP TABLE IF EXISTS `com_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `com_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `com_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `com_department`
--

LOCK TABLES `com_department` WRITE;
/*!40000 ALTER TABLE `com_department` DISABLE KEYS */;
INSERT INTO `com_department` VALUES (1,'技术部',1,1,'iamIPaddr 10:59:51',1,'iamIPaddr 10:59:55');
/*!40000 ALTER TABLE `com_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `com_employee`
--

DROP TABLE IF EXISTS `com_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `com_employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `en_name` varchar(20) NOT NULL,
  `phone` bigint(20) NOT NULL,
  `email` varchar(200) NOT NULL,
  `status` int(11) NOT NULL,
  `com_id` int(11) NOT NULL,
  `com_dept_id` int(11) NOT NULL,
  `com_pos_id` int(11) NOT NULL,
  `created_by` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  `updated_by` int(11) NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `en_name` (`en_name`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`),
  KEY `ix_com_employee_com_dept_id` (`com_dept_id`),
  KEY `ix_com_employee_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `com_employee`
--

LOCK TABLES `com_employee` WRITE;
/*!40000 ALTER TABLE `com_employee` DISABLE KEYS */;
INSERT INTO `com_employee` VALUES (1,'林三','colin',iamIPaddr,'colin@betack.com',iamIPaddr,1,'iamIPaddr 11:05:04',1,'iamIPaddr 11:05:08');
/*!40000 ALTER TABLE `com_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(200) NOT NULL,
  `status` enum('NORMAL','LIMIT') DEFAULT NULL,
  `is_valid` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updateed_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pbkdf2:shaiamIPaddr$vFNSMvFv$482aaa322ea4a5cfeiamIPaddrciamIPaddrbiamIPaddrfbbiamIPaddrfeb',NULL,1,'iamIPaddr 12:16:57',NULL,NULL),(2,'colin','pbkdf2:shaiamIPaddr$iFPY5SBD$iamIPaddrcd5ceaaiamIPaddrc8b6eciamIPaddrbiamIPaddrbiamIPaddr',NULL,1,'iamIPaddr 12:48:16','iamIPaddr 12:52:00',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ck_ops'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on iamIPaddr 14:11:03
