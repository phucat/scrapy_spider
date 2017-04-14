CREATE TABLE tbl_scraper_data(
    id int not NULL AUTO_INCREMENT primary key,
    phone VARCHAR(50),
    address VARCHAR(250) NOT NULL,
    company VARCHAR(150) NOT NULL,
    email varchar(150) NOT NULL,
    logo_url VARCHAR(250),
    number_of_employees INTEGER(10),
    industry_focus VARCHAR(250),
    scraping_source_id VARCHAR(100),
    link VARCHAR(250),
    origin_country VARCHAR(250),
    year_of_foundation INTEGER(6),
    is_importable CHAR(0)
);
