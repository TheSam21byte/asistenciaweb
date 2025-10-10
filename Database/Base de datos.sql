-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: dbia
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `aula`
--

DROP TABLE IF EXISTS `aula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aula` (
  `id_aula` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_aula`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aula`
--

LOCK TABLES `aula` WRITE;
/*!40000 ALTER TABLE `aula` DISABLE KEYS */;
INSERT INTO `aula` VALUES (1,'AV-202ISI','Pabellón B');
/*!40000 ALTER TABLE `aula` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso` (
  `id_curso` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `codigo` varchar(20) DEFAULT NULL,
  `creditos` int DEFAULT NULL,
  `id_docente` bigint DEFAULT NULL,
  PRIMARY KEY (`id_curso`),
  KEY `id_docente` (`id_docente`),
  CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`id_docente`) REFERENCES `docente` (`id_docente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso`
--

LOCK TABLES `curso` WRITE;
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` VALUES (1,'GOBIERNO ELECTRONICO Y DE TECNOLOGIAS DE INFORMACION','SI401',3,1),(2,'ESTRUCTURA DE SISTEMAS OPERATIVOS','SI402',3,2),(3,'AUTOMATAS Y CONTROL DE PROCESOS','SI403',3,3),(4,'CLOUD COMPUTING','SI404',3,4),(5,'DESARROLLO DE SOLUCIONES DE SOFTWARE LIBRE','SI405',3,5),(6,'ADMINISTRACION DE REDES Y TELECOMUNICACIONES','SI406',4,6);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso_periodo`
--

DROP TABLE IF EXISTS `curso_periodo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso_periodo` (
  `id_curso_periodo` bigint NOT NULL AUTO_INCREMENT,
  `id_curso` bigint NOT NULL,
  `id_docente` bigint NOT NULL,
  `id_periodo` bigint NOT NULL,
  PRIMARY KEY (`id_curso_periodo`),
  KEY `id_curso` (`id_curso`),
  KEY `id_docente` (`id_docente`),
  KEY `id_periodo` (`id_periodo`),
  CONSTRAINT `curso_periodo_ibfk_1` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`),
  CONSTRAINT `curso_periodo_ibfk_2` FOREIGN KEY (`id_docente`) REFERENCES `docente` (`id_docente`),
  CONSTRAINT `curso_periodo_ibfk_3` FOREIGN KEY (`id_periodo`) REFERENCES `periodo` (`id_periodo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso_periodo`
--

LOCK TABLES `curso_periodo` WRITE;
/*!40000 ALTER TABLE `curso_periodo` DISABLE KEYS */;
INSERT INTO `curso_periodo` VALUES (1,1,1,1),(2,2,2,1),(3,3,3,1),(4,4,4,1),(5,5,5,1),(6,6,6,1);
/*!40000 ALTER TABLE `curso_periodo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docente`
--

DROP TABLE IF EXISTS `docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `docente` (
  `id_docente` bigint NOT NULL AUTO_INCREMENT,
  `nombres` varchar(100) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `correo_institucional` varchar(100) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_docente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docente`
--

LOCK TABLES `docente` WRITE;
/*!40000 ALTER TABLE `docente` DISABLE KEYS */;
INSERT INTO `docente` VALUES (1,'NATALY CLAUDIA','MIRANDA MONDRAGON','nmirandamondragon@unamad.edu.pe',1),(2,'ALDO','ALARCON SUCASACA','aalarconsucasaca@unamad.edu.pe',1),(3,'JAIME CESAR','PRIETO LUNA','jprietoluna@unamad.edu.pe',1),(4,'JOSE CARLOS','NAVARRO VEGA','jnavarrovega@unamad.edu.pe',1),(5,'DENYS ALBERTO','JARAMILLO PERALTA','djaramilloperalta@unamad.edu.pe',1),(6,'MARIO JESUS','ORMACHEA MEJIA','mormacheamejia@unamad.edu.pe',1);
/*!40000 ALTER TABLE `docente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudiante`
--

DROP TABLE IF EXISTS `estudiante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiante` (
  `id_estudiante` bigint NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) NOT NULL,
  `nombres` varchar(100) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `dni` char(8) DEFAULT NULL,
  `correo_institucional` varchar(100) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_estudiante`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiante`
--

LOCK TABLES `estudiante` WRITE;
/*!40000 ALTER TABLE `estudiante` DISABLE KEYS */;
INSERT INTO `estudiante` VALUES (1,'22121041','Samuel Jose','Sanchez Tambo','12345678','ssancheztambo@unamad.edu.pe',1),(2,'22121032','Alex','Carpio Pereira','12345678','acarpiopereira@unamad.edu.pe',1),(3,'22121039','Angel Rene','Arias Dea','12345677','aariasdea@unamad.edu.pe',1),(4,'22121027','Ian','Solorio Palomino','12345676','isoloriopalomino@unamad.edu.pe',1);
/*!40000 ALTER TABLE `estudiante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evento_acceso`
--

DROP TABLE IF EXISTS `evento_acceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evento_acceso` (
  `id_evento` bigint NOT NULL AUTO_INCREMENT,
  `ts` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_estudiante` bigint DEFAULT NULL,
  `id_aula` bigint NOT NULL,
  `id_periodo` bigint NOT NULL,
  `validado` tinyint(1) NOT NULL,
  `direccion` enum('ENTRA','SALE') DEFAULT NULL,
  `snapshot_path` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id_evento`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_aula` (`id_aula`),
  KEY `id_periodo` (`id_periodo`),
  CONSTRAINT `evento_acceso_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`),
  CONSTRAINT `evento_acceso_ibfk_2` FOREIGN KEY (`id_aula`) REFERENCES `aula` (`id_aula`),
  CONSTRAINT `evento_acceso_ibfk_3` FOREIGN KEY (`id_periodo`) REFERENCES `periodo` (`id_periodo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evento_acceso`
--

LOCK TABLES `evento_acceso` WRITE;
/*!40000 ALTER TABLE `evento_acceso` DISABLE KEYS */;
/*!40000 ALTER TABLE `evento_acceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matricula`
--

DROP TABLE IF EXISTS `matricula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matricula` (
  `id_matricula` bigint NOT NULL AUTO_INCREMENT,
  `id_estudiante` bigint NOT NULL,
  `id_curso` bigint NOT NULL,
  `id_aula` bigint NOT NULL,
  `id_periodo` bigint NOT NULL,
  PRIMARY KEY (`id_matricula`),
  UNIQUE KEY `id_estudiante_2` (`id_estudiante`,`id_curso`,`id_periodo`),
  UNIQUE KEY `id_estudiante_3` (`id_estudiante`,`id_curso`,`id_periodo`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_curso` (`id_curso`),
  KEY `id_aula` (`id_aula`),
  KEY `id_periodo` (`id_periodo`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`),
  CONSTRAINT `matricula_ibfk_3` FOREIGN KEY (`id_aula`) REFERENCES `aula` (`id_aula`),
  CONSTRAINT `matricula_ibfk_4` FOREIGN KEY (`id_periodo`) REFERENCES `periodo` (`id_periodo`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matricula`
--

LOCK TABLES `matricula` WRITE;
/*!40000 ALTER TABLE `matricula` DISABLE KEYS */;
INSERT INTO `matricula` VALUES (1,1,1,1,1),(2,1,2,1,1),(3,1,3,1,1),(4,1,4,1,1),(5,1,5,1,1),(6,1,6,1,1),(7,2,1,1,1),(8,2,2,1,1),(9,2,3,1,1),(10,2,4,1,1),(11,2,5,1,1),(12,2,6,1,1),(13,3,1,1,1),(14,3,2,1,1),(15,3,3,1,1),(16,3,4,1,1),(17,3,5,1,1),(18,3,6,1,1),(19,4,1,1,1),(20,4,2,1,1),(21,4,3,1,1),(22,4,4,1,1),(23,4,5,1,1),(24,4,6,1,1);
/*!40000 ALTER TABLE `matricula` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `periodo`
--

DROP TABLE IF EXISTS `periodo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `periodo` (
  `id_periodo` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id_periodo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `periodo`
--

LOCK TABLES `periodo` WRITE;
/*!40000 ALTER TABLE `periodo` DISABLE KEYS */;
INSERT INTO `periodo` VALUES (1,'2025-1','2025-04-15','2025-06-26');
/*!40000 ALTER TABLE `periodo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rostro`
--

DROP TABLE IF EXISTS `rostro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rostro` (
  `id_rostro` bigint NOT NULL AUTO_INCREMENT,
  `id_estudiante` bigint NOT NULL,
  `id_periodo` bigint DEFAULT NULL,
  `path_relativo` varchar(500) NOT NULL,
  `ts_captura` datetime DEFAULT CURRENT_TIMESTAMP,
  `calidad` float DEFAULT NULL,
  `hash_archivo` char(64) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_rostro`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_periodo` (`id_periodo`),
  CONSTRAINT `rostro_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiante` (`id_estudiante`),
  CONSTRAINT `rostro_ibfk_2` FOREIGN KEY (`id_periodo`) REFERENCES `periodo` (`id_periodo`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rostro`
--

LOCK TABLES `rostro` WRITE;
/*!40000 ALTER TABLE `rostro` DISABLE KEYS */;
INSERT INTO `rostro` VALUES (1,1,1,'D:\\Proyectos\\AsistenciaIA\\output\\2025-1\\22121041','2025-10-09 19:55:04',0.99,'bf5d578d25b5b031f7e7afa80f40d4afe3de0d72b1d098a709d8e9ce9d47a31e',1),(2,2,1,'D:\\Proyectos\\AsistenciaIA\\output\\2025-1\\22121032','2025-10-09 20:45:29',0.99,'6e727e731c4ac33a4c90baa60fc06b651a6a8c8dc876fccd48c1aebfdb7a2ed1',1),(3,3,1,'D:\\Proyectos\\AsistenciaIA\\output\\2025-1\\22121039','2025-10-09 20:46:16',0.99,'d309578c097d9736931963109d83a4af205052c585ec55ce836029831eee4e8f',1);
/*!40000 ALTER TABLE `rostro` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-10  9:08:19
