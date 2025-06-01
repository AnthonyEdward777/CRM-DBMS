-- leads procedures crm
-- CREATE LEAD
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

-- UPDATE LEAD
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

-- ASSIGN EMPLOYEE TO LEAD
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

-- CHANGE STATUS OF LEAD
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

-- GET LEADS FILTERED
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


-- Create Customer
DELIMITER $$
CREATE PROCEDURE createCustomer(
    IN IN_leadID INT,
    IN IN_personID INT
)
BEGIN
    INSERT INTO customer (leadID, personID, dateCreated, dateUpdated)
    VALUES (IN_leadID, IN_personID, NOW(), NOW());
END$$
DELIMITER ;

-- Update Customer
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

-- Get Customer Profile
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

-- Get Customer Status Journey
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

-- Get Customer Preferences
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

-- Get Customer Product Interests
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


-- Create Employee
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

-- Update Employee
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

-- Get Employee Leads
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

-- Get Employee Follow-Ups
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

-- Create Campaign
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

-- Update Campaign
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

-- Link Source to Campaign
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

-- Get Campaign Performance
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

-- Get Sources for Campaign
DELIMITER $$
CREATE PROCEDURE getSourcesForCampaign(
    IN IN_campaignID INT
)
BEGIN
    SELECT * FROM source WHERE campaignID = IN_campaignID;
END$$
DELIMITER ;




-- Add Product
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

-- Update Product
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

-- Get All Products
DELIMITER $$
CREATE PROCEDURE getProducts()
BEGIN
    SELECT * FROM product;
END$$
DELIMITER ;

-- Get Customer Favorites (interests)
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











-- interaction procedures/functionss

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



-- follow up procedures

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

ALTER TABLE followUp ADD COLUMN completed BOOLEAN DEFAULT FALSE;
ALTER TABLE followUp 
MODIFY COLUMN followUpID INT NOT NULL AUTO_INCREMENT;

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




-- 1. Log a status change
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

-- 2. Get status history for a lead
DELIMITER $$
CREATE PROCEDURE getStatusHistory(IN IN_leadID INT)
BEGIN
    SELECT 
        sh.statusHistoryID,
        s.statusName,
        sh.changeDate,
        CONCAT(p.firstName, ' ', p.lastName) AS changedBy,
        sh.notes
    FROM statusHistory sh
    JOIN status s ON sh.statusID = s.statusID
    JOIN employee e ON sh.changedByEmpID = e.empID
    JOIN person p ON e.personID = p.personID
    WHERE sh.leadID = IN_leadID
    ORDER BY sh.changeDate DESC;
END$$
DELIMITER ;

-- 3. Status counts for dashboard
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



-- 4. Funnel conversion statistics
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

-- 5. Campaign lead count
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

-- 6. Average lead duration per status
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

-- 7. Top product interests
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

-- 8. Budget distribution (Assuming a 'budget' column in 'leads') do this one later fix amounts and currencies
-- DELIMITER $$
-- CREATE PROCEDURE getBudgetDistribution()
-- BEGIN
--     SELECT 
--         CASE 
--             WHEN budget < 1000 THEN 'Under $1k'
--             WHEN budget BETWEEN 1000 AND 4999 THEN '$1k - $5k'
--             WHEN budget BETWEEN 5000 AND 9999 THEN '$5k - $10k'
--             ELSE 'Over $10k'
--         END AS budgetRange,
--         COUNT(*) AS leadCount
--     FROM leads
--     WHERE budget IS NOT NULL
--     GROUP BY budgetRange
--     ORDER BY leadCount DESC;
-- END$$
-- DELIMITER ;


-- other stuff i forgot


DELIMITER //
CREATE PROCEDURE createPerson(
    IN IN_name VARCHAR(255),
    IN IN_email VARCHAR(255),
    IN IN_phone VARCHAR(50)
)
BEGIN
    INSERT INTO Person (name, email, phone)
    VALUES (IN_name, IN_email, IN_phone);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updatePerson(
    IN IN_personID INT,
    IN IN_newName VARCHAR(255),
    IN IN_newEmail VARCHAR(255),
    IN IN_newPhone VARCHAR(50)
)
BEGIN
    UPDATE Person
    SET name = IN_newName,
        email = IN_newEmail,
        phone = IN_newPhone
    WHERE personID = IN_personID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateCustomerPreferences(
    IN IN_custPrefID INT,
    IN IN_contactMethodID INT,
    IN IN_pLanguage VARCHAR(100),
    IN IN_pContactTime VARCHAR(100),
    IN IN_pBudget DECIMAL(10,2)
)
BEGIN
    UPDATE CustomerPreferences
    SET contactMethodID = IN_contactMethodID,
        preferredLanguage = IN_pLanguage,
        preferredContactTime = IN_pContactTime,
        preferredBudget = IN_pBudget
    WHERE custPrefID = IN_custPrefID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE addCustomerProductInterest(
    IN IN_custID INT,
    IN IN_productID INT
)
BEGIN
    INSERT INTO CustomerProductInterest (custID, productID)
    VALUES (IN_custID, IN_productID);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE removeCustomerProductInterest(
    IN IN_custID INT,
    IN IN_productID INT
)
BEGIN
    DELETE FROM CustomerProductInterest
    WHERE custID = IN_custID AND productID = IN_productID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllEmployees()
BEGIN
    SELECT * FROM Employee;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllCustomers()
BEGIN
    SELECT * FROM Customer;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllCampaigns()
BEGIN
    SELECT * FROM Campaign;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllAddressTypes()
BEGIN
    SELECT * FROM AddressType;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllInteractionChannels()
BEGIN
    SELECT * FROM InteractionChannel;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllStatus()
BEGIN
    SELECT * FROM Status;
END //
DELIMITER ;


