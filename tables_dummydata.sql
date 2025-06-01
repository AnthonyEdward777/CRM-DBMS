create database crm;
use crm;

CREATE TABLE person (
    personID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    dateCreated DATETIME,
    dateUpdated DATETIME
);

CREATE TABLE employee (
    empID INT AUTO_INCREMENT PRIMARY KEY,
    personID INT,
    role VARCHAR(100),
    dateHired DATETIME,
    dateTerminated DATETIME,
    FOREIGN KEY (personID) REFERENCES person(personID)
);

CREATE TABLE addressType (
    typeID INT AUTO_INCREMENT PRIMARY KEY,
    typeName VARCHAR(100)
);

CREATE TABLE address (
    addressID INT AUTO_INCREMENT PRIMARY KEY,
    personID INT,
    zip VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    typeID INT,
    FOREIGN KEY (personID) REFERENCES person(personID),
    FOREIGN KEY (typeID) REFERENCES addressType(typeID)
);

CREATE TABLE campaign (
    campaignID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    startDate DATETIME,
    endDate DATETIME,
    budget DECIMAL(10,2)
);

CREATE TABLE source (
    sourceID INT AUTO_INCREMENT PRIMARY KEY,
    campaignID INT,
    sourceName VARCHAR(255),
    sourceDesc VARCHAR(1000),
    FOREIGN KEY (campaignID) REFERENCES campaign(campaignID)
);

CREATE TABLE status (
    statusID INT AUTO_INCREMENT PRIMARY KEY,
    statusName VARCHAR(100),
    statusDesc VARCHAR(1000)
);

CREATE TABLE leads (
    leadID INT AUTO_INCREMENT PRIMARY KEY,
    sourceID INT,
    statusID INT,
    empID INT,
    personID INT,
    dateCreated DATETIME,
    notes VARCHAR(1000),
    FOREIGN KEY (sourceID) REFERENCES source(sourceID),
    FOREIGN KEY (statusID) REFERENCES status(statusID),
    FOREIGN KEY (empID) REFERENCES employee(empID),
    FOREIGN KEY (personID) REFERENCES person(personID)
);

CREATE TABLE customer (
    custID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT,
    personID INT,
    dateCreated DATETIME,
    dateUpdated DATETIME,
    FOREIGN KEY (leadID) REFERENCES leads(leadID),
    FOREIGN KEY (personID) REFERENCES person(personID)
);

CREATE TABLE contactMethod (
    methodID INT AUTO_INCREMENT PRIMARY KEY,
    methodName VARCHAR(100)
);

CREATE TABLE customerPreferences (
    custPrefID INT AUTO_INCREMENT PRIMARY KEY,
    custID INT,
    contactMethodID INT,
    pLanguage VARCHAR(50),
    pContactTime VARCHAR(100),
    pBudget DECIMAL(10,2),
    dateUpdated DATETIME,
    FOREIGN KEY (custID) REFERENCES customer(custID),
    FOREIGN KEY (contactMethodID) REFERENCES contactMethod(methodID)
);

CREATE TABLE product (
    productID INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255),
    productDesc VARCHAR(1000)
);

CREATE TABLE customerProductInterest (
    custID INT,
    productID INT,
    PRIMARY KEY (custID, productID),
    FOREIGN KEY (custID) REFERENCES customer(custID),
    FOREIGN KEY (productID) REFERENCES product(productID)
);

CREATE TABLE interactionChannel (
    channelID INT AUTO_INCREMENT PRIMARY KEY,
    channelName VARCHAR(100)
);

CREATE TABLE interaction (
    interactionID INT AUTO_INCREMENT PRIMARY KEY,
    empID INT,
    custID INT,
    notes VARCHAR(1000),
    channelID INT,
    interactionDate DATETIME,
    FOREIGN KEY (empID) REFERENCES employee(empID),
    FOREIGN KEY (custID) REFERENCES customer(custID),
    FOREIGN KEY (channelID) REFERENCES interactionChannel(channelID)
);

CREATE TABLE followUp (
    followUpID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT,
    empID INT,
    notes VARCHAR(1000),
    followUpDate DATETIME,
    FOREIGN KEY (leadID) REFERENCES leads(leadID),
    FOREIGN KEY (empID) REFERENCES employee(empID)
);

CREATE TABLE statusHistory (
    statusHistoryID INT AUTO_INCREMENT PRIMARY KEY,
    leadID INT,
    statusID INT,
    changedByEmpID INT,
    changeDate DATETIME,
    notes VARCHAR(1000),
    FOREIGN KEY (leadID) REFERENCES leads(leadID),
    FOREIGN KEY (statusID) REFERENCES status(statusID),
    FOREIGN KEY (changedByEmpID) REFERENCES employee(empID)
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