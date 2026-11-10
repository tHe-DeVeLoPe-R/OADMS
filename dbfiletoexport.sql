-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: utw_dms
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `flight_tracker`
--

DROP TABLE IF EXISTS `flight_tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_tracker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL,
  `flight_number` varchar(30) NOT NULL,
  `airline` varchar(50) DEFAULT NULL,
  `route_type` enum('Arrival','Departure') NOT NULL,
  `route_details` varchar(100) DEFAULT NULL,
  `airport` varchar(50) NOT NULL,
  `flight_date` date DEFAULT NULL,
  `flight_time` datetime NOT NULL,
  `pax_count` int(11) NOT NULL,
  `transport_assigned` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'On Time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_tracker`
--

LOCK TABLES `flight_tracker` WRITE;
/*!40000 ALTER TABLE `flight_tracker` DISABLE KEYS */;
INSERT INTO `flight_tracker` VALUES (2,'UTW-OCT-26-2026','PA 470','AIRBLUE','Arrival',NULL,'Jeddah (JED)','2026-10-26','0000-00-00 00:00:00',13,'11 SEATER','Landed'),(3,'UTW-OCT-26-2026','PA 471','AIRBLUE','Departure',NULL,'Jeddah (JED)','2026-11-15','0000-00-00 00:00:00',13,'11 SEATER','On Time');
/*!40000 ALTER TABLE `flight_tracker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotel_transfers`
--

DROP TABLE IF EXISTS `hotel_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_transfers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL,
  `city` enum('Makkah','Madinah') NOT NULL,
  `hotel_name` varchar(100) NOT NULL,
  `check_in_date` date NOT NULL,
  `check_out_date` date NOT NULL,
  `rooms_allocated` int(11) NOT NULL,
  `voucher_status` enum('Confirmed','Pending') DEFAULT 'Confirmed',
  `assigned_coordinator` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_transfers`
--

LOCK TABLES `hotel_transfers` WRITE;
/*!40000 ALTER TABLE `hotel_transfers` DISABLE KEYS */;
INSERT INTO `hotel_transfers` VALUES (1,'UTW-OCT-26-2026','Makkah','HIBBA HIJRA 5','2026-10-26','2026-11-15',3,'Confirmed','MR RIZWAN'),(2,'UTW-OCT-26-2026','Madinah','SAFA BARKA','2026-11-03','2026-11-12',3,'Confirmed','MR AMIR');
/*!40000 ALTER TABLE `hotel_transfers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operational_incidents`
--

DROP TABLE IF EXISTS `operational_incidents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operational_incidents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) DEFAULT NULL,
  `severity` enum('Low','Medium','High','Critical') NOT NULL,
  `category` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `reported_by` varchar(100) NOT NULL,
  `status` enum('Open','In Progress','Resolved') DEFAULT 'Open',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operational_incidents`
--

LOCK TABLES `operational_incidents` WRITE;
/*!40000 ALTER TABLE `operational_incidents` DISABLE KEYS */;
/*!40000 ALTER TABLE `operational_incidents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pilgrim_groups`
--

DROP TABLE IF EXISTS `pilgrim_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pilgrim_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL,
  `group_name` varchar(100) NOT NULL,
  `leader_name` varchar(100) DEFAULT NULL,
  `leader_phone` varchar(30) DEFAULT NULL,
  `total_pax` int(11) DEFAULT 0,
  `arrival_date` date DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `status` varchar(30) DEFAULT 'Active',
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_code` (`group_code`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilgrim_groups`
--

LOCK TABLES `pilgrim_groups` WRITE;
/*!40000 ALTER TABLE `pilgrim_groups` DISABLE KEYS */;
INSERT INTO `pilgrim_groups` VALUES (1,'UTW-OCT-26-2026','21 DAYS','Mr Ghazanfar','+923046629043',23,'2026-10-26',NULL,'Active'),(2,'UTW-NOV-26-2026','21 DAYS','ZAFAR IQBAL','+923004965615',10,'2026-11-27','2026-12-15','Active');
/*!40000 ALTER TABLE `pilgrim_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pilgrims`
--

DROP TABLE IF EXISTS `pilgrims`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pilgrims` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL,
  `name` varchar(150) NOT NULL,
  `reference_by` varchar(150) DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  `contact` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `group_code` (`group_code`),
  KEY `passport_number` (`passport_number`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pilgrims`
--

LOCK TABLES `pilgrims` WRITE;
/*!40000 ALTER TABLE `pilgrims` DISABLE KEYS */;
INSERT INTO `pilgrims` VALUES (1,'UTW-NOV-26-2026','MR ZAFAR IQBAL','SELF','AM1338654','+923004965615','JARANWALA','2026-11-10 04:15:20'),(2,'UTW-NOV-26-2026','MRS FARHAT HANIF','DR HASEEB','DZ6781941','+92 3067044192','SHAHKOT','2026-11-10 04:25:18'),(3,'UTW-NOV-26-2026','MRS SHABANA KOUSAR','DR HASEEB','PK4914661','+92 3067044192','SHAHKOT','2026-11-10 04:40:09'),(4,'UTW-NOV-26-2026','MUHAMMAD HANIF','DR HASEEB','EH6785321','+92 3067044192','SHAHKOT','2026-11-10 04:41:10');
/*!40000 ALTER TABLE `pilgrims` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riaz_permits`
--

DROP TABLE IF EXISTS `riaz_permits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `riaz_permits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL DEFAULT 'GENERAL',
  `passport_number` varchar(50) NOT NULL,
  `visa_number` varchar(50) NOT NULL,
  `pilgrim_whatsapp` varchar(30) DEFAULT NULL,
  `permit_date` date NOT NULL,
  `slot_time` varchar(50) NOT NULL,
  `status` enum('Upcoming','Completed','Missed') NOT NULL DEFAULT 'Upcoming',
  `permit_type` enum('Own Permit','Managed on Wheel Chair','Managed by Cash') NOT NULL DEFAULT 'Own Permit',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `passport_number` (`passport_number`),
  KEY `permit_date` (`permit_date`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riaz_permits`
--

LOCK TABLES `riaz_permits` WRITE;
/*!40000 ALTER TABLE `riaz_permits` DISABLE KEYS */;
INSERT INTO `riaz_permits` VALUES (3,'UTW-OCT-26-2026','CA5783781','MALAIKA ZULFIQAR 6176245807','+923046629043','2026-11-05','08:00AM','Completed','Own Permit','2026-11-09 05:35:36'),(4,'UTW-OCT-26-2026','BU9857152','HINA NASEEM 6176245812','NAN','2026-11-05','08:00 AM','Completed','Own Permit','2026-11-09 05:44:31'),(5,'UTW-OCT-26-2026','DB3134761','RAZIA BIBI','NAN','2026-11-05','10:00 AM','Completed','Own Permit','2026-11-09 05:48:24'),(6,'UTW-OCT-26-2026','UN1858231','6176245810','NAN','2026-11-05','10:00 AM','Completed','Own Permit','2026-11-09 05:49:08'),(7,'UTW-OCT-26-2026','TT5167101','TARIQ HUSSAIN SHAH 6176245802','NAN','2026-11-05','11:20 AM','Completed','Own Permit','2026-11-09 05:50:52'),(8,'UTW-OCT-26-2026','NF1917851','MUHAMMAD ARSHAD  6176245805','NAN','2026-11-05','11:20 AM','Completed','Own Permit','2026-11-09 05:52:02');
/*!40000 ALTER TABLE `riaz_permits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('admin','guide','ops_manager') NOT NULL DEFAULT 'guide',
  `phone` varchar(30) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'adminuser','scrypt:32768:8:1$oPEcRJlLmby10Ic0$51679db2e50ddd185b652fe45b9cf725d4fb2653f9cd1ffdbc898aefe0fe64a636a0c68c7412fcb27573ad6f7a2ed8e1233555a413d52c261789dac1b080e9f0','Zafar Iqbal (Admin)','admin','+92 300 1234567','2026-11-09 04:46:27');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zyarat_logs`
--

DROP TABLE IF EXISTS `zyarat_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zyarat_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_code` varchar(50) NOT NULL,
  `city` enum('Makkah','Madinah') NOT NULL,
  `zyarat_date` date NOT NULL,
  `departure_time` varchar(20) DEFAULT NULL,
  `destination` varchar(150) NOT NULL,
  `bus_number` varchar(50) DEFAULT NULL,
  `driver_name` varchar(100) DEFAULT NULL,
  `driver_phone` varchar(30) DEFAULT NULL,
  `guide_murshid` varchar(100) NOT NULL,
  `booked_pax` int(11) NOT NULL,
  `actual_pax` int(11) NOT NULL,
  `status` enum('Scheduled','Boarding','In Transit','Completed') NOT NULL DEFAULT 'Scheduled',
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zyarat_logs`
--

LOCK TABLES `zyarat_logs` WRITE;
/*!40000 ALTER TABLE `zyarat_logs` DISABLE KEYS */;
INSERT INTO `zyarat_logs` VALUES (3,'UTW-OCT-26-2026','Madinah','2026-11-08','07:30 AM','MADINA PAK HARAM TO HARAM','NAN','NAN','','MEHBOOB BHAI',23,26,'Completed',''),(4,'UTW-OCT-26-2026','Makkah','2026-10-29','07:30 AM','MAKKAH PAK HOTEL TO HOTEL','4242','JANI BHAI','','JANI BHAI',37,37,'Completed','');
/*!40000 ALTER TABLE `zyarat_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-10 10:24:26
