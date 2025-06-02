-- WARNING: This script will DROP and RECREATE your 'crm' database,
-- resulting in the loss of all existing data.
-- It implements hard deletes with ON DELETE CASCADE for all foreign keys.

DROP DATABASE IF EXISTS crm;
CREATE DATABASE crm;
USE crm;

-- Table: person
-- Removed isDeleted column
CREATE TABLE person (
    personID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    dateCreated DATETIME,
    dateUpdated DATETIME
);

-- Table: employee
CREATE TABLE employee (
    empID INT AUTO_INCREMENT PRIMARY KEY,
    personID INT,
    role VARCHAR(100),
    dateHired DATETIME,
    dateTerminated DATETIME,
    FOREIGN KEY (personID) REFERENCES person(personID) ON DELETE CASCADE
);

-- Table: addressType
CREATE TABLE addressType (
    typeID INT AUTO_INCREMENT PRIMARY KEY,
    typeName VARCHAR(100)
);

-- Table: address
-- Removed isDeleted column
CREATE TABLE address (
    addressID INT AUTO_INCREMENT PRIMARY KEY,
    personID INT,
    zip VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    typeID INT,
    FOREIGN KEY (personID) REFERENCES person(personID) ON DELETE CASCADE,
    FOREIGN KEY (typeID) REFERENCES addressType(typeID) ON DELETE CASCADE
);

-- Table: campaign
-- Removed isDeleted column
CREATE TABLE campaign (
    campaignID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    startDate DATETIME,
    endDate DATETIME,
    budget DECIMAL(10,2)
);

-- Table: source
-- Removed isDeleted column
CREATE TABLE source (
    sourceID INT AUTO_INCREMENT PRIMARY KEY,
    campaignID INT,
    sourceName VARCHAR(255),
    sourceDesc VARCHAR(1000),
    FOREIGN KEY (campaignID) REFERENCES campaign(campaignID) ON DELETE CASCADE
);

-- Table: status
CREATE TABLE status (
    statusID INT AUTO_INCREMENT PRIMARY KEY,
    statusName VARCHAR(100),
    statusDesc VARCHAR(1000)
);

-- Table: leads
-- Removed isDeleted column
CREATE TABLE leads (
    leadID INT AUTO_INCREMENT PRIMARY KEY,
    sourceID INT,
    statusID INT,
    empID INT,
    personID INT,
    dateCreated DATETIME,
    notes VARCHAR(1000),
    FOREIGN KEY (sourceID) REFERENCES source(sourceID) ON DELETE CASCADE,
    FOREIGN KEY (statusID) REFERENCES status(statusID) ON DELETE CASCADE,
    FOREIGN KEY (empID) REFERENCES employee(empID) ON DELETE CASCADE,
    FOREIGN KEY (personID) REFERENCES person(personID) ON DELETE CASCADE
);

-- Table: customer
-- Removed isDeleted column
CREATE TABLE customer (
    custID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT UNIQUE,
    personID INT,
    dateCreated DATETIME,
    dateUpdated DATETIME,
    FOREIGN KEY (leadID) REFERENCES leads(leadID) ON DELETE CASCADE,
    FOREIGN KEY (personID) REFERENCES person(personID) ON DELETE CASCADE
);

-- Table: contactMethod
CREATE TABLE contactMethod (
    methodID INT AUTO_INCREMENT PRIMARY KEY,
    methodName VARCHAR(100)
);

-- Table: customerPreferences
-- Removed isDeleted column
CREATE TABLE customerPreferences (
    custPrefID INT AUTO_INCREMENT PRIMARY KEY,
    custID INT,
    contactMethodID INT,
    pLanguage VARCHAR(50),
    pContactTime VARCHAR(100),
    pBudget DECIMAL(10,2),
    dateUpdated DATETIME,
    FOREIGN KEY (custID) REFERENCES customer(custID) ON DELETE CASCADE,
    FOREIGN KEY (contactMethodID) REFERENCES contactMethod(methodID) ON DELETE CASCADE
);

-- Table: product
-- Removed isDeleted column
CREATE TABLE product (
    productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productDesc VARCHAR(1000)
);

-- Table: customerProductInterest
CREATE TABLE customerProductInterest (
    custID INT,
    productID INT,
    PRIMARY KEY (custID, productID),
    FOREIGN KEY (custID) REFERENCES customer(custID) ON DELETE CASCADE,
    FOREIGN KEY (productID) REFERENCES product(productID) ON DELETE CASCADE
);

-- Table: interactionChannel
CREATE TABLE interactionChannel (
    channelID INT AUTO_INCREMENT PRIMARY KEY,
    channelName VARCHAR(100)
);

-- Table: interaction
-- Removed isDeleted column
CREATE TABLE interaction (
    interactionID INT AUTO_INCREMENT PRIMARY KEY,
    empID INT,
    custID INT,
    notes VARCHAR(1000),
    channelID INT,
    interactionDate DATETIME,
    FOREIGN KEY (empID) REFERENCES employee(empID) ON DELETE CASCADE,
    FOREIGN KEY (custID) REFERENCES customer(custID) ON DELETE CASCADE,
    FOREIGN KEY (channelID) REFERENCES interactionChannel(channelID) ON DELETE CASCADE
);

-- Table: followUp
-- Removed isDeleted column
CREATE TABLE followUp (
    followUpID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT,
    empID INT,
    notes VARCHAR(1000),
    followUpDate DATETIME,
    FOREIGN KEY (leadID) REFERENCES leads(leadID) ON DELETE CASCADE,
    FOREIGN KEY (empID) REFERENCES employee(empID) ON DELETE CASCADE
);

-- Table: statusHistory
CREATE TABLE statusHistory (
    statusHistoryID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT,
    statusID INT,
    changedByEmpID INT,
    changeDate DATETIME,
    notes VARCHAR(1000),
    FOREIGN KEY (leadID) REFERENCES leads(leadID) ON DELETE CASCADE,
    FOREIGN KEY (statusID) REFERENCES status(statusID) ON DELETE CASCADE,
    FOREIGN KEY (changedByEmpID) REFERENCES employee(empID) ON DELETE CASCADE
);


-- Insert dummy data for person
INSERT INTO person (name, email, phone, dateCreated, dateUpdated) VALUES
('Alice Johnson', 'alice@example.com', '123-456-7890', NOW(), NOW()),
('Bob Smith', 'bob@example.com', '234-567-8901', NOW(), NOW()),
('Charlie Davis', 'charlie@example.com', '345-678-9012', NOW(), NOW()),
('Diana Prince', 'diana@example.com', '456-789-0123', NOW(), NOW());

-- Insert dummy data for employee (linked to person)
INSERT INTO employee (personID, role, dateHired, dateTerminated) VALUES
(1, 'Sales Manager', '2020-01-15', NULL),
(2, 'Support Specialist', '2021-05-10', NULL);

-- Insert dummy data for addressType
INSERT INTO addressType (typeName) VALUES
('Home'),
('Work'),
('Billing');

-- Insert dummy data for address (linked to person and addressType)
INSERT INTO address (personID, zip, city, state, country, typeID) VALUES
(1, '10001', 'New York', 'NY', 'USA', 1),
(2, '90001', 'Los Angeles', 'CA', 'USA', 2),
(3, '60601', 'Chicago', 'IL', 'USA', 3),
(4, '73301', 'Austin', 'TX', 'USA', 1);

-- Insert dummy data for campaign
INSERT INTO campaign (name, startDate, endDate, budget) VALUES
('Spring Sale 2025', '2025-03-01', '2025-03-31', 10000.00),
('Black Friday 2025', '2025-11-20', '2025-11-30', 20000.00);

-- Insert dummy data for source (linked to campaign)
INSERT INTO source (campaignID, sourceName, sourceDesc) VALUES
(1, 'Google Ads', 'Paid search ads'),
(1, 'Facebook Ads', 'Social media campaign'),
(2, 'Email Marketing', 'Newsletter campaign');

-- Insert dummy data for status
INSERT INTO status (statusName, statusDesc) VALUES
('New Lead', 'Initial stage'),
('Contacted', 'Lead contacted'),
('Qualified', 'Qualified as potential customer'),
('Lost', 'Lead lost or unresponsive'),
('Converted', 'Converted to customer');

-- Insert dummy data for leads (linked to source, status, emp, person)
INSERT INTO leads (sourceID, statusID, empID, personID, dateCreated, notes) VALUES
(1, 1, 1, 3, NOW(), 'Interested in product A'),
(2, 2, 2, 4, NOW(), 'Requested demo'),
(3, 3, 1, 2, NOW(), 'High budget lead');

-- Insert dummy data for customer (linked to leads and person)
INSERT INTO customer (leadID, personID, dateCreated, dateUpdated) VALUES
(3, 2, NOW(), NOW());

-- Insert dummy data for contactMethod
INSERT INTO contactMethod (methodName) VALUES
('Email'),
('Phone'),
('SMS'),
('In-Person');

-- Insert dummy data for customerPreferences (linked to customer and contactMethod)
INSERT INTO customerPreferences (custID, contactMethodID, pLanguage, pContactTime, pBudget, dateUpdated) VALUES
(1, 1, 'English', 'Morning', 5000.00, NOW());

-- Insert dummy data for product
INSERT INTO product (productName, productDesc) VALUES
('Product A', 'Description for product A'),
('Product B', 'Description for product B'),
('Product C', 'Description for product C');

-- Insert dummy data for customerProductInterest (linked to customer and product)
INSERT INTO customerProductInterest (custID, productID) VALUES
(1, 1),
(1, 3);

-- Insert dummy data for interactionChannel
INSERT INTO interactionChannel (channelName) VALUES
('Email'),
('Phone Call'),
('Chat'),
('Meeting');

-- Insert dummy data for interaction (linked to employee, customer, interactionChannel)
INSERT INTO interaction (empID, custID, notes, channelID, interactionDate) VALUES
(1, 1, 'Discussed pricing and features', 2, NOW()),
(2, 1, 'Followed up via email', 1, NOW());

-- Insert dummy data for followUp (linked to leads and employees)
INSERT INTO followUp (leadID, empID, notes, followUpDate) VALUES
(1, 1, 'Call to discuss requirements', '2025-06-05'),
(2, 2, 'Send product brochure', '2025-06-07');

-- Insert dummy data for statusHistory (linked to leads, status, employee)
INSERT INTO statusHistory (leadID, statusID, changedByEmpID, changeDate, notes) VALUES
(1, 1, 1, NOW(), 'Lead created'),
(1, 2, 1, NOW(), 'Contacted lead'),
(2, 1, 2, NOW(), 'Lead created');

-- Add completed column to the 'followUp' table and modify primary key
ALTER TABLE followUp MODIFY COLUMN followUpID INT NOT NULL AUTO_INCREMENT;






-- Stored Procedures

DELIMITER $$
CREATE PROCEDURE createLead(
    IN IN_personID INT,
    IN IN_sourceID INT,
    IN IN_empID INT,
    IN IN_statusID INT,
    IN IN_notes VARCHAR(1000)
)
BEGIN
    INSERT INTO leads (personID, sourceID, empID, statusID, dateCreated, notes)
    VALUES (IN_personID, IN_sourceID, IN_empID, IN_statusID, NOW(), IN_notes);
END$$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE updateLead(
    IN IN_leadID INT,
    IN IN_newSourceID INT,
    IN IN_newStatusID INT,
    IN IN_newEmpID INT,
    IN IN_newNotes VARCHAR(1000)
)
BEGIN
    UPDATE leads
    SET sourceID = IN_newSourceID,
        statusID = IN_newStatusID,
        empID = IN_newEmpID,
        notes = IN_newNotes
    WHERE leadID = IN_leadID;
END$$
DELIMITER ;

DELIMITER $$

CREATE PROCEDURE assignLeadToEmployee(
    IN IN_leadID INT,
    IN IN_empID INT
)
BEGIN
    UPDATE leads
    SET empID = IN_empID
    WHERE leadID = IN_leadID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE changeLeadStatus(
    IN IN_leadID INT,
    IN IN_statusID INT
)
BEGIN
    UPDATE leads
    SET statusID = IN_statusID
    WHERE leadID = IN_leadID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getLeads(
    IN IN_empID INT,
    IN IN_statusID INT,
    IN IN_startDate DATE,
    IN IN_endDate DATE
)
BEGIN
    SELECT l.leadID, p.name AS leadName, e.role AS assignedEmployee, s.statusName, l.dateCreated, l.notes
    FROM leads l
    LEFT JOIN person p ON l.personID = p.personID
    LEFT JOIN employee e ON l.empID = e.empID
    LEFT JOIN status s ON l.statusID = s.statusID
    WHERE (IN_empID IS NULL OR l.empID = IN_empID)
      AND (IN_statusID IS NULL OR l.statusID = IN_statusID)
      AND (IN_startDate IS NULL OR l.dateCreated >= IN_startDate)
      AND (IN_endDate IS NULL OR l.dateCreated <= IN_endDate);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS getLeads;

DELIMITER $$
CREATE PROCEDURE getLeads(
    IN IN_empID INT,
    IN IN_statusID INT,
    IN IN_startDate DATE,
    IN IN_endDate DATE
)
BEGIN
    SELECT 
        l.leadID,
        l.personID,
        p.name AS leadName,
        ep.name AS assignedEmployee,  -- Changed to get name from person table through employee
        s.statusName,
        l.dateCreated,
        l.notes,
        l.sourceID,
        l.statusID,
        l.empID,
        p.email,
        p.phone
    FROM leads l
    LEFT JOIN person p ON l.personID = p.personID
    LEFT JOIN employee e ON l.empID = e.empID
    LEFT JOIN person ep ON e.personID = ep.personID  -- Added join to get employee's name
    LEFT JOIN status s ON l.statusID = s.statusID
    WHERE (IN_empID IS NULL OR l.empID = IN_empID)
      AND (IN_statusID IS NULL OR l.statusID = IN_statusID)
      AND (IN_startDate IS NULL OR l.dateCreated >= IN_startDate)
      AND (IN_endDate IS NULL OR l.dateCreated <= IN_endDate);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE createCustomer(
    IN IN_leadID INT,
    IN IN_personID INT
)
BEGIN
    -- Check if a customer already exists for this lead
    IF NOT EXISTS (SELECT 1 FROM customer WHERE leadID = IN_leadID) THEN
        INSERT INTO customer (leadID, personID, dateCreated, dateUpdated)
        VALUES (IN_leadID, IN_personID, NOW(), NOW());
        SELECT TRUE AS success;
    ELSE
        SELECT FALSE AS success;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateCustomer(
    IN IN_custID INT,
    IN IN_personID INT
)
BEGIN
    UPDATE customer
    SET personID = IN_personID,
        dateUpdated = NOW()
    WHERE custID = IN_custID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCustomerProfile(
    IN IN_custID INT
)
BEGIN
    SELECT c.*, p.name, p.email, p.phone
    FROM customer c
    JOIN person p ON c.personID = p.personID
    WHERE c.custID = IN_custID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCustomerStatusJourney(
    IN IN_custID INT
)
BEGIN
    SELECT sh.*, s.statusName
    FROM statusHistory sh
    JOIN status s ON sh.statusID = s.statusID
    JOIN customer c ON c.leadID = sh.leadID
    WHERE c.custID = IN_custID
    ORDER BY sh.changeDate DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCustomerPreferences(
    IN IN_custID INT
)
BEGIN
    SELECT cp.*, cm.methodName
    FROM customerPreferences cp
    JOIN contactMethod cm ON cp.contactMethodID = cm.methodID
    WHERE cp.custID = IN_custID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCustomerProductInterests(
    IN IN_custID INT
)
BEGIN
    SELECT pi.*, p.productName
    FROM customerProductInterest pi
    JOIN product p ON pi.productID = p.productID
    WHERE pi.custID = IN_custID;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE createEmployee(
    IN IN_personID INT,
    IN IN_role VARCHAR(100)
)
BEGIN
    INSERT INTO employee (personID, role, dateHired)
    VALUES (IN_personID, IN_role, NOW());
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateEmployee(
    IN IN_empID INT,
    IN IN_newRole VARCHAR(100)
)
BEGIN
    UPDATE employee
    SET role = IN_newRole
    WHERE empID = IN_empID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getEmployeeLeads(
    IN IN_empID INT
)
BEGIN
    SELECT l.*, p.name AS leadName
    FROM leads l
    JOIN person p ON l.personID = p.personID
    WHERE l.empID = IN_empID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getEmployeeFollowUps(
    IN IN_empID INT
)
BEGIN
    SELECT f.*, l.leadID, p.name AS leadName
    FROM followUp f
    JOIN leads l ON f.leadID = l.leadID
    JOIN person p ON l.personID = p.personID
    WHERE f.empID = IN_empID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE createCampaign(
    IN IN_name VARCHAR(255),
    IN IN_startDate DATETIME,
    IN IN_endDate DATETIME,
    IN IN_budget DECIMAL(10,2)
)
BEGIN
    INSERT INTO campaign (name, startDate, endDate, budget)
    VALUES (IN_name, IN_startDate, IN_endDate, IN_budget);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateCampaign(
    IN IN_campaignID INT,
    IN IN_name VARCHAR(255),
    IN IN_startDate DATETIME,
    IN IN_endDate DATETIME,
    IN IN_budget DECIMAL(10,2)
)
BEGIN
    UPDATE campaign
    SET name = IN_name,
        startDate = IN_startDate,
        endDate = IN_endDate,
        budget = IN_budget
    WHERE campaignID = IN_campaignID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE linkSourceToCampaign(
    IN IN_sourceID INT,
    IN IN_campaignID INT
)
BEGIN
    UPDATE source
    SET campaignID = IN_campaignID
    WHERE sourceID = IN_sourceID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCampaignPerformance(
    IN IN_campaignID INT
)
BEGIN
    SELECT c.name AS campaignName, COUNT(l.leadID) AS totalLeads
    FROM campaign c
    JOIN source s ON c.campaignID = s.campaignID
    JOIN leads l ON l.sourceID = s.sourceID
    WHERE c.campaignID = IN_campaignID
    GROUP BY c.name;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getSourcesForCampaign(
    IN IN_campaignID INT
)
BEGIN
    SELECT * FROM source WHERE campaignID = IN_campaignID;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE addProduct(
    IN IN_productName VARCHAR(255),
    IN IN_productDesc VARCHAR(1000)
)
BEGIN
    INSERT INTO product (productName, productDesc)
    VALUES (IN_productName, IN_productDesc);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE updateProduct(
    IN IN_productID INT,
    IN IN_productName VARCHAR(255),
    IN IN_productDesc VARCHAR(1000)
)
BEGIN
    UPDATE product
    SET productName = IN_productName,
        productDesc = IN_productDesc
    WHERE productID = IN_productID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getProducts()
BEGIN
    SELECT * FROM product;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCustomerFavorites(
    IN IN_custID INT
)
BEGIN
    SELECT p.productID, p.productName, p.productDesc
    FROM customerProductInterest cpi
    JOIN product p ON cpi.productID = p.productID
    WHERE cpi.custID = IN_custID;
END$$
DELIMITER ;


DELIMITER //
CREATE PROCEDURE logInteraction (
    IN p_custID INT,
    IN p_empID INT,
    IN p_channelID INT,
    IN p_notes VARCHAR(255),
    IN p_interactionDate DATETIME
)
BEGIN
    INSERT INTO interaction (custID, empID, channelID, notes, interactionDate)
    VALUES (p_custID, p_empID, p_channelID, p_notes, p_interactionDate);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getCustomerInteractions (
    IN p_custID INT
)
BEGIN
    SELECT
        i.interactionID,
        i.empID,
        e.role AS employeeRole,
        i.notes,
        i.interactionDate,
        ic.channelName
    FROM interaction i
    JOIN interactionChannel ic ON i.channelID = ic.channelID
    JOIN employee e ON i.empID = e.empID
    WHERE i.custID = p_custID
    ORDER BY i.interactionDate DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getEmployeeInteractions (
    IN p_empID INT
)
BEGIN
    SELECT
        i.interactionID,
        i.custID,
        p.name AS customerName,
        i.notes,
        i.interactionDate,
        ic.channelName
    FROM interaction i
    JOIN customer c ON i.custID = c.custID
    JOIN person p ON c.personID = p.personID
    JOIN interactionChannel ic ON i.channelID = ic.channelID
    WHERE i.empID = p_empID
    ORDER BY i.interactionDate DESC;
END //
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE createFollowUp(
    IN p_leadID INT,
    IN p_empID INT,
    IN p_followUpDate DATETIME,
    IN p_notes VARCHAR(1000)
)
BEGIN
    INSERT INTO followUp (leadID, empID, followUpDate, notes)
    VALUES (p_leadID, p_empID, p_followUpDate, p_notes);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE completeFollowUp(
    IN p_followUpID INT
)
BEGIN
    UPDATE followUp
    SET completed = TRUE
    WHERE followUpID = p_followUpID;
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE getPendingFollowUps(
    IN p_empID INT,
    IN p_leadID INT,
    IN p_beforeDate DATETIME
)
BEGIN
    SELECT *
    FROM followUp
    WHERE completed = FALSE
      AND (p_empID IS NULL OR empID = p_empID)
      AND (p_leadID IS NULL OR leadID = p_leadID)
      AND (p_beforeDate IS NULL OR followUpDate <= p_beforeDate);
END$$
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE logStatusChange(
    IN IN_leadID INT,
    IN IN_newStatusID INT,
    IN IN_empID INT,
    IN IN_notes VARCHAR(1000)
)
BEGIN
    INSERT INTO statusHistory (leadID, statusID, changedByEmpID, changeDate, notes)
    VALUES (IN_leadID, IN_newStatusID, IN_empID, NOW(), IN_notes);

    UPDATE leads
    SET statusID = IN_newStatusID
    WHERE leadID = IN_leadID;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getStatusHistory(IN IN_leadID INT)
BEGIN
    SELECT
        sh.statusHistoryID,
        s.statusName,
        sh.changeDate,
        p.name AS changedBy,
        sh.notes
    FROM statusHistory sh
    JOIN status s ON sh.statusID = s.statusID
    JOIN employee e ON sh.changedByEmpID = e.empID
    JOIN person p ON e.personID = p.personID
    WHERE sh.leadID = IN_leadID
    ORDER BY sh.changeDate DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getStatusCounts()
BEGIN
    SELECT
        s.statusName,
        COUNT(*) AS leadCount
    FROM leads l
    JOIN status s ON l.statusID = s.statusID
    GROUP BY s.statusName
    ORDER BY leadCount DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getFunnelConversionStats()
BEGIN
    SELECT
        s.statusName,
        COUNT(*) AS leadCount
    FROM leads l
    JOIN status s ON l.statusID = s.statusID
    GROUP BY s.statusName
    ORDER BY leadCount DESC;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getCampaignLeadCount(IN IN_campaignID INT)
BEGIN
    SELECT
        c.name AS campaignName,
        COUNT(l.leadID) AS leadCount
    FROM campaign c
    JOIN source s ON c.campaignID = s.campaignID
    JOIN leads l ON l.sourceID = s.sourceID
    WHERE c.campaignID = IN_campaignID
    GROUP BY c.name;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getAverageLeadDurationPerStatus()
BEGIN
    SELECT
        s.statusName,
        ROUND(AVG(DATEDIFF(CURDATE(), l.dateCreated)), 1) AS avgDurationDays
    FROM leads l
    JOIN status s ON l.statusID = s.statusID
    GROUP BY s.statusName;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE getTopProductInterests()
BEGIN
    SELECT
        p.productName,
        COUNT(*) AS interestCount
    FROM customerProductInterest cpi
    JOIN product p ON cpi.productID = p.productID
    GROUP BY p.productName
    ORDER BY interestCount DESC
    LIMIT 10;
END$$
DELIMITER ;

-- New: Create Person (Fundamental for Employees, Leads, Customers)
DELIMITER $$
CREATE PROCEDURE createPerson(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_phone VARCHAR(50)
)
BEGIN
    INSERT INTO person (name, email, phone, dateCreated, dateUpdated)
    VALUES (p_name, p_email, p_phone, NOW(), NOW());
    SELECT LAST_INSERT_ID() AS newPersonID;
END$$
DELIMITER ;

-- New: Update Person (for general person details)
DELIMITER $$
CREATE PROCEDURE updatePerson(
    IN p_personID INT,
    IN p_newName VARCHAR(255),
    IN p_newEmail VARCHAR(255),
    IN p_newPhone VARCHAR(50)
)
BEGIN
    UPDATE person
    SET
        name = p_newName,
        email = p_newEmail,
        phone = p_newPhone,
        dateUpdated = NOW()
    WHERE personID = p_personID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Delete Person (Hard delete - will cascade to employee, address, leads, customer)
DELIMITER $$
CREATE PROCEDURE deletePerson(
    IN p_personID INT
)
BEGIN
    DELETE FROM person WHERE personID = p_personID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Total Customers
DELIMITER $$
CREATE PROCEDURE getTotalCustomers()
BEGIN
    SELECT COUNT(custID) AS TotalCustomers
    FROM customer; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Total Conversions (Leads with 'Converted' status)
DELIMITER $$
CREATE PROCEDURE getTotalConversions()
BEGIN
    SELECT COUNT(l.leadID) AS TotalConversions
    FROM leads l
    JOIN status s ON l.statusID = s.statusID
    WHERE s.statusName = 'Converted'; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Count of Active Campaigns
DELIMITER $$
CREATE PROCEDURE getActiveCampaignsCount()
BEGIN
    SELECT COUNT(campaignID) AS ActiveCampaigns
    FROM campaign
    WHERE endDate >= CURDATE() OR endDate IS NULL; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Follow-Ups Due Today
DELIMITER $$
CREATE PROCEDURE getFollowUpsDueToday(IN p_empID INT)
BEGIN
    SELECT
        f.followUpID,
        f.leadID,
        p.name AS leadPersonName,
        f.notes,
        f.followUpDate
    FROM followUp f
    JOIN leads l ON f.leadID = l.leadID
    JOIN person p ON l.personID = p.personID
    WHERE f.completed = FALSE
      AND DATE(f.followUpDate) = CURDATE()
      AND (p_empID IS NULL OR f.empID = p_empID); -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Recent Follow-Ups (for a global timeline/dashboard)
DELIMITER $$
CREATE PROCEDURE getRecentFollowUps(IN p_limit INT)
BEGIN
    SELECT
        f.followUpID,
        f.leadID,
        p.name AS leadPersonName,
        e_person.name AS assignedEmployee,
        f.notes,
        f.followUpDate,
        f.completed
    FROM followUp f
    JOIN leads l ON f.leadID = l.leadID
    JOIN person p ON l.personID = p.personID
    JOIN employee e ON f.empID = e.empID
    JOIN person e_person ON e.personID = e_person.personID
    ORDER BY f.followUpDate DESC
    LIMIT p_limit; -- Added semicolon here
END$$
DELIMITER ;


-- New: Delete Lead (Hard delete - will cascade to statusHistory, followUp)
DELIMITER $$
CREATE PROCEDURE deleteLead(
    IN p_leadID INT
)
BEGIN
    DELETE FROM leads WHERE leadID = p_leadID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Delete Customer (Hard delete - will cascade to customerPreferences, customerProductInterest, interaction)
DELIMITER $$
CREATE PROCEDURE deleteCustomer(
    IN p_custID INT
)
BEGIN
    DELETE FROM customer WHERE custID = p_custID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Update Customer Preferences
DELIMITER $$
CREATE PROCEDURE updateCustomerPreferences(
    IN p_custPrefID INT,
    IN p_contactMethodID INT,
    IN p_pLanguage VARCHAR(50),
    IN p_pContactTime VARCHAR(100),
    IN p_pBudget DECIMAL(10,2)
)
BEGIN
    UPDATE customerPreferences
    SET
        contactMethodID = p_contactMethodID,
        pLanguage = p_pLanguage,
        pContactTime = p_pContactTime,
        pBudget = p_pBudget,
        dateUpdated = NOW()
    WHERE custPrefID = p_custPrefID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get All Customers (with filtering options)
DELIMITER $$
CREATE PROCEDURE getAllCustomers(
    IN p_startDate DATE,
    IN p_endDate DATE,
    IN p_minBudget DECIMAL(10,2),
    IN p_maxBudget DECIMAL(10,2),
    IN p_productID INT
)
BEGIN
    SELECT
        c.custID,
        p.name AS customerName,
        p.email,
        p.phone,
        c.dateCreated,
        cp.pBudget,
        cp.pLanguage
    FROM customer c
    JOIN person p ON c.personID = p.personID
    LEFT JOIN customerPreferences cp ON c.custID = cp.custID
    WHERE (p_startDate IS NULL OR c.dateCreated >= p_startDate)
      AND (p_endDate IS NULL OR c.dateCreated <= p_endDate)
      AND (p_minBudget IS NULL OR cp.pBudget >= p_minBudget)
      AND (p_maxBudget IS NULL OR cp.pBudget <= p_maxBudget)
      AND (p_productID IS NULL OR c.custID IN (SELECT custID FROM customerProductInterest WHERE productID = p_productID)); -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Customer Detailed Profile (combines info from multiple tables)
DELIMITER $$
CREATE PROCEDURE getCustomerDetailedProfile(
    IN p_custID INT
)
BEGIN
    SELECT
        c.custID,
        p.personID,
        p.name,
        p.email,
        p.phone,
        c.dateCreated AS customerCreationDate,
        c.dateUpdated AS customerLastUpdated,
        l.leadID,
        source_t.sourceName,
        campaign_t.name AS campaignName,
        emp_p.name AS assignedEmployeeName,
        emp_t.role AS assignedEmployeeRole,
        cp.custPrefID,
        cm.methodName AS preferredContactMethod,
        cp.pLanguage AS preferredLanguage,
        cp.pContactTime AS preferredContactTime,
        cp.pBudget AS preferredBudget,
        cp.dateUpdated AS preferencesLastUpdated
    FROM customer c
    JOIN person p ON c.personID = p.personID
    LEFT JOIN leads l ON c.leadID = l.leadID
    LEFT JOIN source source_t ON l.sourceID = source_t.sourceID
    LEFT JOIN campaign campaign_t ON source_t.campaignID = campaign_t.campaignID
    LEFT JOIN employee emp_t ON l.empID = emp_t.empID
    LEFT JOIN person emp_p ON emp_t.personID = emp_p.personID
    LEFT JOIN customerPreferences cp ON c.custID = cp.custID
    LEFT JOIN contactMethod cm ON cp.contactMethodID = cm.methodID
    WHERE c.custID = p_custID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Leads for a specific Campaign (can use getLeads with source filter too, but this is explicit)
DELIMITER $$
CREATE PROCEDURE getLeadsForCampaign(
    IN p_campaignID INT
)
BEGIN
    SELECT
        l.leadID,
        p.name AS leadName,
        s.statusName,
        src.sourceName,
        l.dateCreated,
        l.notes
    FROM leads l
    JOIN person p ON l.personID = p.personID
    JOIN status s ON l.statusID = s.statusID
    JOIN source src ON l.sourceID = src.sourceID
    WHERE src.campaignID = p_campaignID; -- Added semicolon here
END$$
DELIMITER ;


-- New: Delete Campaign (Hard delete - will cascade to source)
DELIMITER $$
CREATE PROCEDURE deleteCampaign(
    IN p_campaignID INT
)
BEGIN
    DELETE FROM campaign WHERE campaignID = p_campaignID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Create Source
DELIMITER $$
CREATE PROCEDURE createSource(
    IN p_campaignID INT,
    IN p_sourceName VARCHAR(255),
    IN p_sourceDesc VARCHAR(1000)
)
BEGIN
    INSERT INTO source (campaignID, sourceName, sourceDesc)
    VALUES (p_campaignID, p_sourceName, p_sourceDesc); -- Added semicolon here
END$$
DELIMITER ;

-- New: Update Source
DELIMITER $$
CREATE PROCEDURE updateSource(
    IN p_sourceID INT,
    IN p_newCampaignID INT,
    IN p_newSourceName VARCHAR(255),
    IN p_newSourceDesc VARCHAR(1000)
)
BEGIN
    UPDATE source
    SET
        campaignID = p_newCampaignID,
        sourceName = p_newSourceName,
        sourceDesc = p_newSourceDesc
    WHERE sourceID = p_sourceID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Delete Source (Hard delete - will cascade to leads)
DELIMITER $$
CREATE PROCEDURE deleteSource(
    IN p_sourceID INT
)
BEGIN
    DELETE FROM source WHERE sourceID = p_sourceID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get All Campaigns
DELIMITER $$
CREATE PROCEDURE getAllCampaigns()
BEGIN
    SELECT
        c.campaignID,
        c.name,
        c.startDate,
        c.endDate,
        c.budget,
        COUNT(l.leadID) AS totalLeadsGenerated -- Simple lead count for "ROI" for now
    FROM campaign c
    LEFT JOIN source s ON c.campaignID = s.campaignID
    LEFT JOIN leads l ON s.sourceID = l.sourceID
    GROUP BY c.campaignID, c.name, c.startDate, c.endDate, c.budget; -- Added semicolon here
END$$
DELIMITER ;








-- New: Get All Sources
DELIMITER $$
CREATE PROCEDURE getAllSources()
BEGIN
    SELECT s.*, c.name AS campaignName
    FROM source s
    LEFT JOIN campaign c ON s.campaignID = c.campaignID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Delete Product (Hard delete - will cascade to customerProductInterest)
DELIMITER $$
CREATE PROCEDURE deleteProduct(
    IN p_productID INT
)
BEGIN
    DELETE FROM product WHERE productID = p_productID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get All Employees
DELIMITER $$

CREATE PROCEDURE getAllEmployees()
BEGIN
    SELECT
        e.empID,
        p.name AS employeeName,
        p.email,
        p.phone,
        e.role,
        e.dateHired,
        e.dateTerminated
    FROM employee e
    JOIN person p ON e.personID = p.personID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Employee Details (single employee)
DELIMITER $$
CREATE PROCEDURE getEmployeeDetails(
    IN p_empID INT
)
BEGIN
    SELECT
        e.empID,
        p.personID,
        p.name AS employeeName,
        p.email,
        p.phone,
        e.role,
        e.dateHired,
        e.dateTerminated
    FROM employee e
    JOIN person p ON e.personID = p.personID
    WHERE e.empID = p_empID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Delete Employee (Hard delete - will cascade to leads, interaction, followUp, statusHistory)
DELIMITER $$
CREATE PROCEDURE deleteEmployee(
    IN p_empID INT
)
BEGIN
    DELETE FROM employee WHERE empID = p_empID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get All Follow-Ups (for a calendar view, optionally filtered)
DELIMITER $$
CREATE PROCEDURE getAllFollowUps(
    IN p_startDate DATE,
    IN p_endDate DATE,
    IN p_completed BOOLEAN
)
BEGIN
    SELECT
        f.followUpID,
        f.leadID,
        p.name AS leadPersonName,
        e_person.name AS assignedEmployee,
        f.notes,
        f.followUpDate,
        f.completed
    FROM followUp f
    JOIN leads l ON f.leadID = l.leadID
    JOIN person p ON l.personID = p.personID
    JOIN employee e ON f.empID = e.empID
    JOIN person e_person ON e.personID = e_person.personID
    WHERE (p_startDate IS NULL OR DATE(f.followUpDate) >= p_startDate)
      AND (p_endDate IS NULL OR DATE(f.followUpDate) <= p_endDate)
      AND (p_completed IS NULL OR f.completed = p_completed)
    ORDER BY f.followUpDate ASC; -- Added semicolon here
END$$
DELIMITER ;


-- New: Get Campaign Conversion Funnel
DELIMITER $$
CREATE PROCEDURE getCampaignConversionFunnel(IN p_campaignID INT)
BEGIN
    SELECT
        s.statusName,
        COUNT(DISTINCT l.leadID) AS LeadCount
    FROM leads l
    JOIN status s ON l.statusID = s.statusID
    JOIN source src ON l.sourceID = src.sourceID
    WHERE src.campaignID = p_campaignID
    GROUP BY s.statusName
    ORDER BY s.statusID; -- Added semicolon here
END$$
DELIMITER ;

-- New: Get Lead Source Effectiveness
DELIMITER $$
CREATE PROCEDURE getSourceEffectiveness()
BEGIN
    SELECT
        src.sourceName,
        COUNT(l.leadID) AS TotalLeads,
        SUM(CASE WHEN st.statusName = 'Converted' THEN 1 ELSE 0 END) AS ConvertedLeads,
        (SUM(CASE WHEN st.statusName = 'Converted' THEN 1 ELSE 0 END) * 100.0 / COUNT(l.leadID)) AS ConversionRate
    FROM source src
    LEFT JOIN leads l ON src.sourceID = l.sourceID
    LEFT JOIN status st ON l.statusID = st.statusID
    GROUP BY src.sourceName
    ORDER BY ConversionRate DESC; -- Added semicolon here
END$$
DELIMITER ;

DELIMITER $$

CREATE FUNCTION getTotalLeads()
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total FROM leads;
    RETURN total;
END$$

CREATE FUNCTION getTotalCustomers()
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total FROM customer;
    RETURN total;
END$$

DELIMITER ;

-- New: Get All Contact Methods
DELIMITER $$
CREATE PROCEDURE getAllContactMethods()
BEGIN
    SELECT * FROM contactMethod;
END$$
DELIMITER ;
