DROP TABLE IF EXISTS medal;

CREATE TABLE medal (
  id INT NOT NULL AUTO_INCREMENT,
  medal_name varchar(50) DEFAULT NULL,
  CONSTRAINT pk_medal PRIMARY KEY (id)
);



INSERT INTO medal (id, medal_name)
VALUES (1,'Gold'),
(2,'Silver'),
(3,'Bronze'),
(4,'NA');


DROP TABLE IF EXISTS noc_region;

CREATE TABLE noc_region (
  id INT NOT NULL AUTO_INCREMENT,
  noc VARCHAR(5) DEFAULT NULL,
  region_name VARCHAR(200) DEFAULT NULL,
  CONSTRAINT pk_nocregion PRIMARY KEY (id)
);


INSERT INTO noc_region (id, noc, region_name) VALUES
(1,'AFG','Afghanistan'),
(2,'AHO','Netherlands Antilles'),
(3,'ALB','Albania'),
(4,'ALG','Algeria'),
(5,'AND','Andorra'),
(6,'ANG','Angola'),
(7,'ANT','Antigua and Barbuda'),
(8,'ANZ','Australasia'),
(9,'ARG','Argentina'),
(10,'ARM','Armenia'),
(11,'ARU','Aruba'),
(12,'ASA','American Samoa'),
(13,'AUS','Australia'),
(14,'AUT','Austria'),
(15,'AZE','Azerbaijan'),
(16,'BAH','Bahamas'),
(17,'BAN','Bangladesh'),
(18,'BAR','Barbados'),
(19,'BDI','Burundi'),
(20,'BEL','Belgium'),
(21,'BEN','Benin'),
(22,'BER','Bermuda'),
(23,'BHU','Bhutan'),
(24,'BIH','Bosnia and Herzegovina'),
(25,'BIZ','Belize'),
(26,'BLR','Belarus'),
(27,'BOH','Bohemia'),
(28,'BOL','Boliva'),
(29,'BOT','Botswana'),
(30,'BRA','Brazil'),
(31,'BRN','Bahrain'),
(32,'BRU','Brunei'),
(33,'BUL','Bulgaria'),
(34,'BUR','Burkina Faso'),
(35,'CAF','Central African Republic'),
(36,'CAM','Cambodia'),
(37,'CAN','Canada'),
(38,'CAY','Cayman Islands'),
(39,'CGO','Republic of Congo'),
(40,'CHA','Chad'),
(41,'CHI','Chile'),
(42,'CHN','China'),
(43,'CIV','Ivory Coast'),
(44,'CMR','Cameroon'),
(45,'COD','Democratic Republic of the Congo'),
(46,'COK','Cook Islands'),
(47,'COL','Colombia'),
(48,'COM','Comoros'),
(49,'CPV','Cape Verde'),
(50,'CRC','Costa Rica'),
(51,'CRO','Croatia'),
(52,'CRT','Crete'),
(53,'CUB','Cuba'),
(54,'CYP','Cyprus'),
(55,'CZE','Czech Republic'),
(56,'DEN','Denmark'),
(57,'DJI','Djibouti'),
(58,'DMA','Dominica'),
(59,'DOM','Dominican Republic'),
(60,'ECU','Ecuador'),
(61,'EGY','Egypt'),
(62,'ERI','Eritrea'),
(63,'ESA','El Salvador'),
(64,'ESP','Spain'),
(65,'EST','Estonia'),
(66,'ETH','Ethiopia'),
(67,'EUN','Unified Team'),
(68,'FIJ','Fiji'),
(69,'FIN','Finland'),
(70,'FRA','France'),
(71,'FRG','West Germany'),
(72,'FSM','Micronesia'),
(73,'GAB','Gabon'),
(74,'GAM','Gambia'),
(75,'GBR','UK'),
(76,'GBS','Guinea-Bissau'),
(77,'GDR','East Germany'),
(78,'GEO','Georgia'),
(79,'GEQ','Equatorial Guinea'),
(80,'GER','Germany'),
(81,'GHA','Ghana'),
(82,'GRE','Greece'),
(83,'GRN','Grenada'),
(84,'GUA','Guatemala'),
(85,'GUI','Guinea'),
(86,'GUM','Guam'),
(87,'GUY','Guyana'),
(88,'HAI','Haiti'),
(89,'HKG','Hong Kong'),
(90,'HON','Honduras'),
(91,'HUN','Hungary'),
(92,'INA','Indonesia'),
(93,'IND','India'),
(94,'IOA','Individual Olympic Athletes'),
(95,'IRI','Iran'),
(96,'IRL','Ireland'),
(97,'IRQ','Iraq'),
(98,'ISL','Iceland'),
(99,'ISR','Israel'),
(100,'ISV','Virgin Islands'),
(101,'ITA','Italy'),
(102,'IVB','Virgin Islands, British'),
(103,'JAM','Jamaica'),
(104,'JOR','Jordan'),
(105,'JPN','Japan'),
(106,'KAZ','Kazakhstan'),
(107,'KEN','Kenya'),
(108,'KGZ','Kyrgyzstan'),
(109,'KIR','Kiribati'),
(110,'KOR','South Korea'),
(111,'KOS','Kosovo'),
(112,'KSA','Saudi Arabia'),
(113,'KUW','Kuwait'),
(114,'LAO','Laos'),
(115,'LAT','Latvia'),
(116,'LBA','Libya'),
(117,'LBR','Liberia'),
(118,'LCA','Saint Lucia'),
(119,'LES','Lesotho'),
(120,'LIB','Lebanon'),
(121,'LIE','Liechtenstein'),
(122,'LTU','Lithuania'),
(123,'LUX','Luxembourg'),
(124,'MAD','Madagascar'),
(125,'MAL','Malaya'),
(126,'MAR','Morocco'),
(127,'MAS','Malaysia'),
(128,'MAW','Malawi'),
(129,'MDA','Moldova'),
(130,'MDV','Maldives'),
(131,'MEX','Mexico'),
(132,'MGL','Mongolia'),
(133,'MHL','Marshall Islands'),
(134,'MKD','Macedonia'),
(135,'MLI','Mali'),
(136,'MLT','Malta'),
(137,'MNE','Montenegro'),
(138,'MON','Monaco'),
(139,'MOZ','Mozambique'),
(140,'MRI','Mauritius'),
(141,'MTN','Mauritania'),
(142,'MYA','Myanmar'),
(143,'NAM','Namibia'),
(144,'NBO','North Borneo'),
(145,'NCA','Nicaragua'),
(146,'NED','Netherlands'),
(147,'NEP','Nepal'),
(148,'NFL','Newfoundland'),
(149,'NGR','Nigeria'),
(150,'NIG','Niger'),
(151,'NOR','Norway'),
(152,'NRU','Nauru'),
(153,'NZL','New Zealand'),
(154,'OMA','Oman'),
(155,'PAK','Pakistan'),
(156,'PAN','Panama'),
(157,'PAR','Paraguay'),
(158,'PER','Peru'),
(159,'PHI','Philippines'),
(160,'PLE','Palestine'),
(161,'PLW','Palau'),
(162,'PNG','Papua New Guinea'),
(163,'POL','Poland'),
(164,'POR','Portugal'),
(165,'PRK','North Korea'),
(166,'PUR','Puerto Rico'),
(167,'QAT','Qatar'),
(168,'RHO','Zimbabwe (Rhodesia)'),
(169,'ROT','Refugee Olympic Team'),
(170,'ROU','Romania'),
(171,'RSA','South Africa'),
(172,'RUS','Russia'),
(173,'RWA','Rwanda'),
(174,'SAA','Saar'),
(175,'SAM','Samoa'),
(176,'SCG','Serbia and Montenegro'),
(177,'SEN','Senegal'),
(178,'SEY','Seychelles'),
(179,'SIN','Singapore'),
(180,'SKN','Turks and Caicos Islands'),
(181,'SLE','Sierra Leone'),
(182,'SLO','Slovenia'),
(183,'SMR','San Marino'),
(184,'SOL','Solomon Islands'),
(185,'SOM','Somalia'),
(186,'SRB','Serbia'),
(187,'SRI','Sri Lanka'),
(188,'SSD','South Sudan'),
(189,'STP','Sao Tome and Principe'),
(190,'SUD','Sudan'),
(191,'SUI','Switzerland'),
(192,'SUR','Suriname'),
(193,'SVK','Slovakia'),
(194,'SWE','Sweden'),
(195,'SWZ','Swaziland'),
(196,'SYR','Syria'),
(197,'TAN','Tanzania'),
(198,'TCH','Czechoslovakia'),
(199,'TGA','Tonga'),
(200,'THA','Thailand'),
(201,'TJK','Tajikistan'),
(202,'TKM','Turkmenistan'),
(203,'TLS','Timor-Leste'),
(204,'TOG','Togo'),
(205,'TPE','Taiwan'),
(206,'TTO','Trinidad and Tobago'),
(207,'TUN','Tunisia'),
(208,'TUR','Turkey'),
(209,'TUV','Tuvalu'),
(210,'UAE','United Arab Emirates'),
(211,'UAR','United Arab Republic'),
(212,'UGA','Uganda'),
(213,'UKR','Ukraine'),
(214,'UNK','Unknown'),
(215,'URS','Soviet Union'),
(216,'URU','Uruguay'),
(217,'USA','USA'),
(218,'UZB','Uzbekistan'),
(219,'VAN','Vanuatu'),
(220,'VEN','Venezuela'),
(221,'VIE','Vietnam'),
(222,'VIN','Saint Vincent'),
(223,'VNM','Vietnam (pre)'),
(224,'WIF','West Indies Federation'),
(225,'YAR','North Yemen'),
(226,'YEM','Yemen'),
(227,'YMD','South Yemen'),
(228,'YUG','Yugoslavia'),
(229,'ZAM','Zambia'),
(230,'ZIM','Zimbabwe'),
(256,'SGP','Singapore');


DROP TABLE IF EXISTS sport;

CREATE TABLE sport (
  id INT NOT NULL AUTO_INCREMENT,
  sport_name VARCHAR(200) DEFAULT NULL,
  CONSTRAINT pk_sport PRIMARY KEY (id)
);


INSERT INTO sport (id, sport_name) VALUES
(1,'Aeronautics'),
(2,'Alpine Skiing'),
(3,'Alpinism'),
(4,'Archery'),
(5,'Art Competitions'),
(6,'Athletics'),
(7,'Badminton'),
(8,'Baseball'),
(9,'Basketball'),
(10,'Basque Pelota'),
(11,'Beach Volleyball'),
(12,'Biathlon'),
(13,'Bobsleigh'),
(14,'Boxing'),
(15,'Canoeing'),
(16,'Cricket'),
(17,'Croquet'),
(18,'Cross Country Skiing'),
(19,'Curling'),
(20,'Cycling'),
(21,'Diving'),
(22,'Equestrianism'),
(23,'Fencing'),
(24,'Figure Skating'),
(25,'Football'),
(26,'Freestyle Skiing'),
(27,'Golf'),
(28,'Gymnastics'),
(29,'Handball'),
(30,'Hockey'),
(31,'Ice Hockey'),
(32,'Jeu De Paume'),
(33,'Judo'),
(34,'Lacrosse'),
(35,'Luge'),
(36,'Military Ski Patrol'),
(37,'Modern Pentathlon'),
(38,'Motorboating'),
(39,'Nordic Combined'),
(40,'Polo'),
(41,'Racquets'),
(42,'Rhythmic Gymnastics'),
(43,'Roque'),
(44,'Rowing'),
(45,'Rugby'),
(46,'Rugby Sevens'),
(47,'Sailing'),
(48,'Shooting'),
(49,'Short Track Speed Skating'),
(50,'Skeleton'),
(51,'Ski Jumping'),
(52,'Snowboarding'),
(53,'Softball'),
(54,'Speed Skating'),
(55,'Swimming'),
(56,'Synchronized Swimming'),
(57,'Table Tennis'),
(58,'Taekwondo'),
(59,'Tennis'),
(60,'Trampolining'),
(61,'Triathlon'),
(62,'Tug-Of-War'),
(63,'Volleyball'),
(64,'Water Polo'),
(65,'Weightlifting'),
(66,'Wrestling');


DROP TABLE IF EXISTS city;

CREATE TABLE city (
  id INT NOT NULL AUTO_INCREMENT,
  city_name varchar(200) DEFAULT NULL,
  CONSTRAINT pk_city PRIMARY KEY (id)
);



INSERT INTO city (id, city_name) VALUES
(1,'Barcelona'),
(2,'London'),
(3,'Antwerpen'),
(4,'Paris'),
(5,'Calgary'),
(6,'Albertville'),
(7,'Lillehammer'),
(8,'Los Angeles'),
(9,'Salt Lake City'),
(10,'Helsinki'),
(11,'Lake Placid'),
(12,'Sydney'),
(13,'Atlanta'),
(14,'Stockholm'),
(15,'Sochi'),
(16,'Nagano'),
(17,'Torino'),
(18,'Beijing'),
(19,'Rio de Janeiro'),
(20,'Athina'),
(21,'Squaw Valley'),
(22,'Innsbruck'),
(23,'Sarajevo'),
(24,'Mexico City'),
(25,'Munich'),
(26,'Seoul'),
(27,'Berlin'),
(28,'Oslo'),
(29,'Cortina d\'Ampezzo'),
(30,'Melbourne'),
(31,'Roma'),
(32,'Amsterdam'),
(33,'Montreal'),
(34,'Moskva'),
(35,'Tokyo'),
(36,'Vancouver'),
(37,'Grenoble'),
(38,'Sapporo'),
(39,'Chamonix'),
(40,'St. Louis'),
(41,'Sankt Moritz'),
(42,'Garmisch-Partenkirchen');
